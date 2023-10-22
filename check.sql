DELIMITER |

create or replace function tailleGroupe(idGroupe int) returns int
begin
  declare res int;
  SELECT COUNT(*) into res FROM GROUPE NATURAL JOIN ARTISTE WHERE idGr = idGroupe;
  return res;
end|

-- Retourne la date du dernier évènement (concert ou activité) d'un groupe en fonction d'une heure donnée
create or replace function finDernierEvenementGroupe(idGroupe int, heure datetime) returns datetime
begin
  declare dateDernierConcert datetime;
  declare dateDerniereActAnn datetime;

  SELECT dateFinConcert into dateDernierConcert FROM CONCERT WHERE idGr = idGroupe AND dateDebutConcert > heure ORDER BY dateDebutConcert LIMIT 1;
  SELECT dateFinActAnn into dateDerniereActAnn FROM ACTIVITE_ANNEXE NATURAL JOIN PARTICIPER WHERE idGr = idGroupe AND dateActAnn > heure ORDER BY dureeActAnn LIMIT 1;
  if dateDernierConcert < dateDerniereActAnn then
    return dateDernierConcert;
  elseif dateDerniereActAnn < dateDernierConcert then
    return dateDerniereActAnn;
  end if;
  return null;
end|

-- Retourne la date du prochaine évènement (concert ou activité) d'un groupe en fonction d'une heure donnée
create or replace function debutProchainEvenementGroupe(idGroupe int, heure datetime) returns datetime
begin
  declare dateProchainConcert datetime;
  declare dateProchaineActAnn datetime;

  SELECT dateDebutConcert into dateProchainConcert FROM CONCERT WHERE idGr = idGroupe AND dateDebutConcert < heure ORDER BY dateDebutConcert DESC LIMIT 1;
  SELECT dateDebutActAnn into dateProchaineActAnn FROM ACTIVITE_ANNEXE NATURAL JOIN PARTICIPER WHERE idGr = idGroupe AND dateActAnn < heure ORDER BY dureeActAnn LIMIT 1;
  if dateProchainConcert < dateProchaineActAnn then
    return dateProchainConcert;
  elseif dateProchaineActAnn < dateProchainConcert then
    return dateProchaineActAnn;
  end if;
  return null;
end|

-- Retourne la date du dernier évènement (concert ou activité) d'un lieu en fonction d'une heure donnée
create or replace function finDernierEvenementLieu(idL int, heure datetime) returns datetime
begin
  declare dateDernierConcert datetime;
  declare demontage int;
  declare dateDerniereActAnn datetime;

  SELECT dateFinConcert, dureeDemontage into dateDernierConcert, demontage FROM CONCERT NATURAL JOIN LIEUX WHERE idLieu = idL AND dateDebutConcert > heure ORDER BY dateDebutConcert LIMIT 1;
  SELECT dateFinActAnn into dateDerniereActAnn FROM ACTIVITE_ANNEXE NATURAL JOIN LIEUX WHERE idLieu = idL AND dateActAnn > heure ORDER BY dureeActAnn LIMIT 1;
  if dateDernierConcert < dateDerniereActAnn then
    set dateDernierConcert = ADDDATE(dateDernierConcert, INTERVAL demontage MINUTE);
    return dateDernierConcert;
  elseif dateDerniereActAnn < dateDernierConcert then
    return dateDerniereActAnn;
  end if;
  return null;
end|

-- Retourne la date du prochain évènement (concert ou activité) d'un lieu en fonction d'une heure donnée
create or replace function debutProchainEvenementLieu(idL int, heure datetime) returns datetime
begin
  declare dateProchainConcert datetime;
  declare montage int;
  declare dateProchaineActAnn datetime;

  SELECT dateDebutConcert, dureeMontage into dateProchainConcert, montage FROM CONCERT NATURAL JOIN LIEUX WHERE idLieu = idL AND dateDebutConcert < heure ORDER BY dateDebutConcert DESC LIMIT 1;
  SELECT dateActAnn into dateProchaineActAnn FROM ACTIVITE_ANNEXE NATURAL JOIN LIEUX WHERE idLieu = idL AND dateActAnn < heure ORDER BY dureeActAnn LIMIT 1;
  if dateProchainConcert < dateProchaineActAnn then
    set dateProchainConcert = SUBDATE(dateProchainConcert, INTERVAL montage MINUTE);
    return dateProchainConcert;
  elseif dateProchaineActAnn < dateProchainConcert then
    return dateProchaineActAnn;
  end if;
  return null;
end|

-- Retourne l'identifiant du lieu corresondant à une évènement donnée (définit par un groupe et une heure)
-- Le paramètre dernierOuProchain : 'D' (dernier) si recherche de l'évènement précédent l'heure donnée
--                               ou 'P' (prochain) si recherche de l'évènement suivant l'heure donnée
create or replace function getIdentifiantLieu(idGroupe int, heure datetime, dernierOuProchain char(1)) returns int
begin
  declare res int;

  -- recherche de l'évènement précédent l'heure donnée
  if dernierOuProchain = 'D' then
    SELECT idLieu into res FROM LIEUX NATURAL JOIN CONCERT WHERE idGr = idGroupe AND dateFinConcert = heure;
    if res is null then
      SELECT idLieu into res FROM LIEUX NATURAL JOIN ACTIVITE_ANNEXE NATURAL JOIN PARTICIPER WHERE idGr = idGroupe AND dateFinActAnn = heure;
    end if;
    return res;
  
  -- recherche de l'évènement suivant l'heure donnée
  elseif dernierOuProchain = 'P' then
    SELECT idLieu into res FROM LIEUX NATURAL JOIN CONCERT WHERE idGr = idGroupe AND dateDebutConcert = heure;
    if res is null then
      SELECT idLieu into res FROM LIEUX NATURAL JOIN ACTIVITE_ANNEXE NATURAL JOIN PARTICIPER WHERE idGr = idGroupe AND dateDebutActAnn = heure;
    end if;
    return res;
  end if;
  return null;
end|

-- Vérifie si un billet compte suffisament de durée restante pour réserver une place dans un concert
create or replace trigger dureeBilletValide before insert on RESERVER for each row
begin
  declare dureeReservee int;
  declare dureeBillet int;
  declare dureeRestante int;
  declare dureeConcertDemande int;
  declare mes varchar(100);

  -- Récupère la durée des concerts déjà réservés et la durée de validité du billet
  SELECT SUM(dureeConcert), dureeValBil into dureeReservee, dureeBillet FROM CONCERT NATURAL JOIN RESERVER NATURAL JOIN BILLET WHERE idBil = new.idBil;
  -- Récupère la durrée du concert demandé
  SELECT TIMESTAMPDIFF(MINUTE, dateDebutConcert, dateFinConcert) into dureeConcertDemande FROM CONCERT WHERE idConcert = new.idConcert;
  set dureeRestante = dureeBillet - dureeReservee;
  if dureeRestante <= 0 then
    set mes = concat('Réservation impossible billet ', new.idBil, ': Billet déjà consommé');
    signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
  elseif dureeRestante < dureeConcertDemande then
    set mes = concat('Réservation impossible billet ', new.idBil, ': Concert trop long pour la validité restante du billet');
    signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
  end if;
end|

-- Vérifie si un hébergement compte suffisament de places pour acceuillir un groupe
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

-- Trigger empêchant la duplication de données. Le déplacement entre deux lieux est trié par ordre alphabétique
-- Autorise seulement d'entrer le déplacement du lieu A vers le lieu B
-- Empêche d'entrer le déplacement du lieu B vers le lieu A
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

-- Vérifie si un concert entre dans l'agenda du groupe entre son dernier évènement (concert ou activité) et son prochain évènement
create or replace trigger groupeDisponibleConcert before insert on CONCERT for each row
begin
  declare dernierEvenement datetime;
  declare prochainEvenement datetime;
  declare lieu int;
  declare dernierTempsTrajet int;
  declare prochainTempsTrajet int;
  declare mes varchar(100);

  set dernierEvenement = finDernierEvenementGroupe(new.idGr, new.dateDebutConcert);
  set lieu = getIdentifiantLieu(new.idGr, dernierEvenement, 'D');
  if dernierEvenement is not null then
    -- Récupération du temps de trajet entre les deux lieus
    SELECT tempsDeTrajet into dernierTempsTrajet FROM DEPLACER
      WHERE (idLieuDepart = lieu AND idLieuArrivee = new.idLieu) OR (idLieuDepart = new.idLieu AND idLieuArrivee = lieu);
    -- Addition de la date de fin du dernier évènement et du temps de trajet comparé au début du nouveau concert
    if ADDDATE(dernierEvenement, INTERVAL dernierTempsTrajet MINUTE) < new.dateDebutConcert then
      set mes = concat('Insertion concert ', new.idConcert, ' impossible : date trop proche du dernier évènement du groupe ', new.idGr);
      signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
    end if;
  end if;

  set prochainEvenement = debutProchainEvenementGroupe(new.idGr, new.dateDebutConcert);
  set lieu = getIdentifiantLieu(new.idGr, prochainEvenement, 'P');
  if prochainEvenement is not null then
    -- Récupération du temps de trajet entre les deux lieus
    SELECT tempsDeTrajet into prochainTempsTrajet FROM DEPLACER
      WHERE (idLieuDepart = lieu AND idLieuArrivee = new.idLieu) OR (idLieuDepart = new.idLieu AND idLieuArrivee = lieu);
    -- Addition de la date de fin du nouveau concert et du temps de trajet comparé au début du prochaine évènement
    if ADDDATE(new.dateFinConcert, INTERVAL prochainTempsTrajet MINUTE) < prochainEvenement then
      set mes = concat('Insertion concert ', new.idConcert, ' impossible : date trop proche du prochain évènement du groupe ', new.idGr);
      signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
    end if;
  end if;
end|

-- Vérifie si une activité entre dans l'agenda du groupe entre son dernier évènement (concert ou activité) et son prochain évènement
create or replace trigger groupeDisponibleActivite before insert on PARTICIPER for each row
begin
  declare lieuAct int;
  declare dateDebutAct datetime;
  declare dateFinAct datetime;
  declare dernierEvenement datetime;
  declare prochainEvenement datetime;
  declare provenance int;
  declare destination int;
  declare dernierTempsTrajet int;
  declare prochainTempsTrajet int;
  declare mes varchar(100);

  SELECT dateDebutActAnn, dateFinActAnn, idLieu into dateDebutAct, dateFinAct, lieuAct FROM ACTIVITE_ANNEXE WHERE idActAnn = new.idActAnn;

  set dernierEvenement = finDernierEvenementGroupe(new.idGr, dateDebutAct);
  set provenance = getIdentifiantLieu(new.idGr, dernierEvenement, 'D');
  if dernierEvenement is not null then
    -- Récupération du temps de trajet entre les deux lieus
    SELECT tempsDeTrajet into dernierTempsTrajet FROM DEPLACER
      WHERE (idLieuDepart = provenance AND idLieuArrivee = lieuAct) OR (idLieuDepart = lieuAct AND idLieuArrivee = provenance);
    -- Addition de la date de fin du dernier évènement et du temps de trajet comparé au début de la nouvelle activité
    if ADDDATE(dernierEvenement, INTERVAL dernierTempsTrajet MINUTE) < dateDebutAct then
      set mes = concat('Insertion participation du groupe ', new.idGr, " à l'activité ", new.idActAnn, ' impossible : date trop proche du dernier évènement du groupe');
      signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
    end if;
  end if;

  set prochainEvenement = debutProchainEvenementGroupe(new.idGr, dateDebutAct);
  set destination = getIdentifiantLieu(new.idGr, prochainEvenement, 'P');
  if prochainEvenement is not null then
    -- Récupération du temps de trajet entre les deux lieus
    SELECT tempsDeTrajet into prochainTempsTrajet FROM DEPLACER
      WHERE (idLieuDepart = destination AND idLieuArrivee = lieuAct) OR (idLieuDepart = lieuAct AND idLieuArrivee = destination);
    -- Addition de la date de fin de la nouvelle activité et du temps de trajet comparé au début du prochain évènement
    if ADDDATE(dateFinAct, INTERVAL prochainTempsTrajet MINUTE) < prochainEvenement then
      set mes = concat('Insertion participation du groupe ', new.idGr, " à l'activité ", new.idActAnn, ' impossible : date trop proche du prochain évènement du groupe');
      signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
    end if;
  end if;
end|

-- Vérifie si un concert entre dans l'agenda d'un lieu entre son dernier évènement (concert ou activité) et son prochain évènement
create or replace trigger lieuDisponibleConcert before insert on CONCERT for each row
begin
  declare lieu int;
  declare dernierEvenement datetime;
  declare prochainEvenement datetime;
  declare dernierTempsTrajet int;
  declare prochainTempsTrajet int;
  declare mes varchar(100);

  set dernierEvenement = finDernierEvenementLieu(new.idLieu, new.dateDebutConcert);
  set lieu = getIdentifiantLieu(new.idLieu, dernierEvenement, 'D');
  if dernierEvenement is not null then
    -- Récupération du temps de trajet entre les deux lieus
    SELECT tempsDeTrajet into dernierTempsTrajet FROM DEPLACER
      WHERE (idLieuDepart = lieu AND idLieuArrivee = new.idLieu) OR (idLieuDepart = new.idLieu AND idLieuArrivee = lieu);
    -- Addition de la date de fin du dernier évènement et du temps de trajet comparé au début du nouveau concert
    if ADDDATE(dernierEvenement, INTERVAL dernierTempsTrajet MINUTE) < new.dateDebutConcert then
      set mes = concat('Insertion concert ', new.idConcert, ' impossible : date trop proche du dernier évènement du groupe ', new.idGr);
      signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
    end if;
  end if;

  set prochainEvenement = debutProchainEvenementGroupe(new.idGr, new.dateDebutConcert);
  set lieu = getIdentifiantLieu(new.idGr, prochainEvenement, 'P');
  if prochainEvenement is not null then
    -- Récupération du temps de trajet entre les deux lieus
    SELECT tempsDeTrajet into prochainTempsTrajet FROM DEPLACER
      WHERE (idLieuDepart = lieu AND idLieuArrivee = new.idLieu) OR (idLieuDepart = new.idLieu AND idLieuArrivee = lieu);
    -- Addition de la date de fin du nouveau concert et du temps de trajet comparé au début du prochaine évènement
    if ADDDATE(new.dateFinConcert, INTERVAL prochainTempsTrajet MINUTE) < prochainEvenement then
      set mes = concat('Insertion concert ', new.idConcert, ' impossible : date trop proche du prochain évènement du groupe ', new.idGr);
      signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
    end if;
  end if;
end|

-- Vérifie si une activité entre dans l'agenda d'un lieu entre son dernier évènement (concert ou activité) et son prochain évènement
create or replace trigger lieuDisponibleActivite before insert on PARTICIPER for each row
begin
  declare lieuAct int;
  declare dateDebutAct datetime;
  declare dateFinAct datetime;
  declare dernierEvenement datetime;
  declare prochainEvenement datetime;
  declare provenance int;
  declare destination int;
  declare dernierTempsTrajet int;
  declare prochainTempsTrajet int;
  declare mes varchar(100);

  SELECT dateDebutActAnn, dateFinActAnn, idLieu into dateDebutAct, dateFinAct, lieuAct FROM ACTIVITE_ANNEXE WHERE idActAnn = new.idActAnn;

  set dernierEvenement = finDernierEvenementGroupe(new.idGr, dateDebutAct);
  set provenance = getIdentifiantLieu(new.idGr, dernierEvenement, 'D');
  if dernierEvenement is not null then
    -- Récupération du temps de trajet entre les deux lieus
    SELECT tempsDeTrajet into dernierTempsTrajet FROM DEPLACER
      WHERE (idLieuDepart = provenance AND idLieuArrivee = lieuAct) OR (idLieuDepart = lieuAct AND idLieuArrivee = provenance);
    -- Addition de la date de fin du dernier évènement et du temps de trajet comparé au début de la nouvelle activité
    if ADDDATE(dernierEvenement, INTERVAL dernierTempsTrajet MINUTE) < dateDebutAct then
      set mes = concat('Insertion participation du groupe ', new.idGr, " à l'activité ", new.idActAnn, ' impossible : date trop proche du dernier évènement du groupe');
      signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
    end if;
  end if;

  set prochainEvenement = debutProchainEvenementGroupe(new.idGr, dateDebutAct);
  set destination = getIdentifiantLieu(new.idGr, prochainEvenement, 'P');
  if prochainEvenement is not null then
    -- Récupération du temps de trajet entre les deux lieus
    SELECT tempsDeTrajet into prochainTempsTrajet FROM DEPLACER
      WHERE (idLieuDepart = destination AND idLieuArrivee = lieuAct) OR (idLieuDepart = lieuAct AND idLieuArrivee = destination);
    -- Addition de la date de fin de la nouvelle activité et du temps de trajet comparé au début du prochaine évènement
    if ADDDATE(dateFinAct, INTERVAL prochainTempsTrajet MINUTE) < prochainEvenement then
      set mes = concat('Insertion participation du groupe ', new.idGr, " à l'activité ", new.idActAnn, ' impossible : date trop proche du prochain évènement du groupe');
      signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
    end if;
  end if;
end|

DELIMITER ;