DELIMITER |

create or replace function tailleGroupe(idGroupe int) returns int
begin
  declare res int;
  SELECT COUNT(*) into res FROM GROUPE NATURAL JOIN ARTISTE WHERE idGr = idGroupe;
  return res;
end|

create or replace function finDernierEvenement(idGroupe int, heure datetime) returns datetime
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

create or replace function debutProchainEvenement(idGroupe int, heure datetime) returns datetime
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
        SELECT dureeConcert into dureeProchainConcert FROM CONCERT WHERE idConcert = dernierConcert;
        set dateProchainConcert = ADDDATE(dateProchainConcert, INTERVAL dureeProchainConcert MINUTE);
        return dateProchainConcert;
    elseif dateProchaineActAnn < dateProchainConcert then
        SELECT dureeActAnn into dureeProchaineActAnn FROM ACTIVITE_ANNEXE WHERE idActAnn = derniereActAnn;
        set dateProchaineActAnn = ADDDATE(dateProchaineActAnn, INTERVAL dureeProchaineActAnn MINUTE);
        return dateProchaineActAnn;
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

DELIMITER ;