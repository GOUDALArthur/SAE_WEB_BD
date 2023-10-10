DELIMITER |

create or replace function tailleGroupe(idGroupe int) returns int
begin
  declare res int;
  SELECT COUNT(*) into res FROM GROUPE NATURAL JOIN ARTISTE WHERE idGr = idGroupe;
  return res;
end|


create or replace function finDernierEvenementGroupe(idGroupe int, heure datetime) returns datetime
begin
  declare dernierConcert int;
  declare dateDernierConcert datetime;
  declare dureeDernierConcert int;
  declare derniereActAnn int;
  declare dateDerniereActAnn datetime;
  declare dureeDerniereActAnn int;

  SELECT idConcert, dateConcert into dernierConcert, dateDernierConcert FROM CONCERT WHERE idGr = idGroupe AND dateConcert > heure ORDER BY dateConcert LIMIT 1;
  SELECT idActAnn, dateActAnn into derniereActAnn, dateDerniereActAnn FROM ACTIVITE_ANNEXE NATURAL JOIN PARTICIPER WHERE idGr = idGroupe AND dateActAnn > heure ORDER BY dureeActAnn LIMIT 1;
  if dateDernierConcert < dateDerniereActAnn then
      SELECT dureeConcert into dureeDernierConcert FROM CONCERT WHERE idConcert = dernierConcert;
      set dateDernierConcert = ADDDATE(dateDernierConcert, INTERVAL dureeDernierConcert MINUTE);
      return dateDernierConcert;
  elseif dateDerniereActAnn < dateDernierConcert then
      SELECT dureeActAnn into dureeDerniereActAnn FROM ACTIVITE_ANNEXE WHERE idActAnn = derniereActAnn;
      set dateDerniereActAnn = ADDDATE(dateDerniereActAnn, INTERVAL dureeDerniereActAnn MINUTE);
      return dateDerniereActAnn;
  end if;
  return null;
end|


create or replace function debutProchainEvenementGroupe(idGroupe int, heure datetime) returns datetime
begin
  declare prochainConcert int;
  declare dateProchainConcert datetime;
  declare dureeProchainConcert int;
  declare prochaineActAnn int;
  declare dateProchaineActAnn datetime;
  declare dureeProchaineActAnn int;

  SELECT idConcert, dateConcert into prochainConcert, dateProchainConcert FROM CONCERT WHERE idGr = idGroupe AND dateConcert < heure ORDER BY dateConcert DESC LIMIT 1;
  SELECT idActAnn, dateActAnn into prochaineActAnn, dateProchaineActAnn FROM ACTIVITE_ANNEXE NATURAL JOIN PARTICIPER WHERE idGr = idGroupe AND dateActAnn < heure ORDER BY dureeActAnn LIMIT 1;
  if dateProchainConcert < dateProchaineActAnn then
      return dateProchainConcert;
  elseif dateProchaineActAnn < dateProchainConcert then
      return dateProchaineActAnn;
  end if;
  return null;
end|


create or replace function getIdentifiantLieu(idGroupe int, heure datetime, dernierOuProchain char(1)) returns int
begin
  declare res int;

  if dernierOuProchain = 'D' then
    SELECT idLieu into res FROM LIEUX NATURAL JOIN CONCERT WHERE idGr = idGroupe AND ADDDATE(dateConcert, INTERVAL dureeConcert MINUTE) = heure;
    if res is null then
      SELECT idLieu into res FROM LIEUX NATURAL JOIN ACTIVITE_ANNEXE NATURAL JOIN PARTICIPER WHERE idGr = idGroupe AND ADDDATE(dateActAnn, INTERVAL dureeActAnn MINUTE) = heure;
    end if;
    return res;
  
  elseif dernierOuProchain = 'P' then
    SELECT idLieu into res FROM LIEUX NATURAL JOIN CONCERT WHERE idGr = idGroupe AND dateConcert = heure;
    if res is null then
      SELECT idLieu into res FROM LIEUX NATURAL JOIN ACTIVITE_ANNEXE NATURAL JOIN PARTICIPER WHERE idGr = idGroupe AND dateActAnn = heure;
    end if;
    return res;
  end if;
  return null;
end|


create or replace trigger dureeBilletValide before insert on RESERVER for each row
begin
  declare dureeReservee float;
  declare dureeBillet float;
  declare dureeRestante float;
  declare dureeC float;
  declare mes varchar(100);

  SELECT SUM(dureeConcert) into dureeReservee FROM CONCERT NATURAL JOIN RESERVER WHERE idBil = new.idBil;
  SELECT dureeValBil into dureeBillet FROM BILLET WHERE idBil = new.idBil;
  set dureeRestante = dureeBillet - dureeReservee;
  if dureeRestante <= 0 then
    set mes = concat('Réservation impossible billet ', new.idBil, ': Billet déjà consommé');
    signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
  elseif dureeRestante < dureeC then
    SELECT dureeConcert into dureeC FROM CONCERT WHERE idConcert = new.idConcert;
    set mes = concat('Réservation impossible billet ', new.idBil, ': Concert trop long pour la validité restante du billet');
    signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
  end if;
end|


create or replace trigger herbergementDisponible before insert on OCCUPER for each row
begin
  declare capaciteHebergement int;
  declare placesOccupees int;
  declare placesRestantes int;
  declare tailleGroupe int;
  declare mes varchar(100);

  SELECT capaciteHeberg into capaciteHebergement FROM HEBERGEMENT WHERE idHeberg = new.idHeberg;
  set tailleGroupe = tailleGroupe(new.idGr);
  SELECT SUM(tailleGroupe(idGr)) into placesOccupees FROM HEBERGEMENT NATURAL JOIN GROUPE WHERE idHeberg = new.idHeberg;
  set placesRestantes = capaciteHebergement - placesOccupees;
  if placesRestantes = 0 then
    set mes = concat('Hébergement impossible, logement ', new.idHeberg, ' est complet.');
    signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
  elseif placesRestantes < tailleGroupe then
    set mes = concat('Hébergement impossible, logement ', new.idHeberg, ' a trop peu de places disponibles.');
    signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
  end if;
end|


create or replace trigger sensInsertionDeplacer before insert on DEPLACER for each row
begin
  declare lieuDepart varchar(500);
  declare lieuArrivee varchar(500);
  declare mes varchar(100);

  SELECT lieu into lieuDepart FROM LIEUX WHERE idLieu = new.idLieuDepart;
  SELECT lieu into lieuArrivee FROM LIEUX WHERE idLieu = new.idLieuArrivee;
  if lieuArrivee < lieuDepart then
    set mes = concat('Insertion impossible déplacement entre lieu ', new.idLieuDepart, ' et ', new.idLieuArrivee, '. Inversez les deux lieux pour insérer.');
    signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
  end if;
end|


create or replace trigger groupeDisponibleConcert before insert on CONCERT for each row
begin
  declare dernierEvenement datetime;
  declare prochainEvenement datetime;
  declare lieu int;
  declare dernierTempsTrajet int;
  declare prochainTempsTrajet int;
  declare mes varchar(100);

  set dernierEvenement = finDernierEvenementGroupe(new.idGr);
  set lieu = getIdentifiantLieu(new.idGr, dernierEvenement, 'D');
  SELECT tempsDeTrajet into dernierTempsTrajet FROM DEPLACER WHERE (idLieuDepart = lieu AND idLieuArrivee = new.idLieu) OR (idLieuDepart = new.idLieu AND idLieuArrivee = lieu);
  if dernierEvenement is not null then
    if ADDDATE(dernierEvenement, INTERVAL dernierTempsTrajet MINUTE) < new.dateConcert then
      set mes = concat('Insertion concert ', new.idConcert, ' impossible : date trop proche du dernier évènement du groupe ', new.idGr);
      signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
    end if;
  end if;

  set prochainEvenement = debutProchainEvenementGroupe(new.idGr);
  set lieu = getIdentifiantLieu(new.idGr, prochainEvenement, 'P');
  SELECT tempsDeTrajet into prochainTempsTrajet FROM DEPLACER WHERE (idLieuDepart = lieu AND idLieuArrivee = new.idLieu) OR (idLieuDepart = new.idLieu AND idLieuArrivee = lieu);
  if prochainEvenement is not null then
    if ADDDATE(ADDDATE(new.dateConcert, INTERVAL new.dureeConcert MINUTE), INTERVAL prochainTempsTrajet MINUTE) < prochainEvenement then
      set mes = concat('Insertion concert ', new.idConcert, ' impossible : date trop proche du prochain évènement du groupe ', new.idGr);
      signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
    end if;
  end if;
end|


create or replace trigger groupeDisponibleActivite before insert on PARTICIPER for each row
begin
  declare lieuAct int;
  declare dateAct datetime;
  declare dureeAct int;
  declare dernierEvenement datetime;
  declare prochainEvenement datetime;
  declare provenance int;
  declare destination int;
  declare dernierTempsTrajet int;
  declare prochainTempsTrajet int;
  declare mes varchar(100);

  SELECT dateActAnn, dureeActAnn, idLieu into dateAct, dureeAct, lieuAct FROM ACTIVITE_ANNEXE WHERE idActAnn = new.idActAnn;

  set dernierEvenement = finDernierEvenementGroupe(new.idGr);
  set provenance = getIdentifiantLieu(new.idGr, dernierEvenement, 'D');
  SELECT tempsDeTrajet into dernierTempsTrajet FROM DEPLACER WHERE (idLieuDepart = provenance AND idLieuArrivee = lieuAct) OR (idLieuDepart = lieuAct AND idLieuArrivee = provenance);
  if dernierEvenement is not null then
    if ADDDATE(dernierEvenement, INTERVAL dernierTempsTrajet MINUTE) < dateAct then
      set mes = concat('Insertion participation du groupe ', new.idGr, " à l'activité ", new.idActAnn, ' impossible : date trop proche du dernier évènement du groupe');
      signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
    end if;
  end if;

  set prochainEvenement = debutProchainEvenementGroupe(new.idGr);
  set destination = getIdentifiantLieu(new.idGr, prochainEvenement, 'P');
  SELECT tempsDeTrajet into prochainTempsTrajet FROM DEPLACER WHERE (idLieuDepart = destination AND idLieuArrivee = lieuAct) OR (idLieuDepart = lieuAct AND idLieuArrivee = destination);
  if prochainEvenement is not null then
    if ADDDATE(ADDDATE(dateAct, INTERVAL dureeAct MINUTE), INTERVAL prochainTempsTrajet MINUTE) < prochainEvenement then
      set mes = concat('Insertion participation du groupe ', new.idGr, " à l'activité ", new.idActAnn, ' impossible : date trop proche du prochain évènement du groupe');
      signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
    end if;
  end if;
end|

DELIMITER ;