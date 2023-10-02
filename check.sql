DELIMITER |

create or replace function tailleGroupe(idGroupe int) returns int
begin
  declare res int;
  SELECT COUNT(*) into res FROM GROUPE NATURAL JOIN ARTISTE WHERE idGr = idGroupe;
  return res;
end|

create or replace function finDerniereEvenement(idGroupe int, heure datetime) returns datetime
begin
    declare dernierConcert datetime;
    declare derniereActAnn datetime;
    SELECT dateConcert into dernierConcert FROM CONCERT WHERE idGr = idGroupe ORDER BY dateConcert LIMIT 1;
    SELECT dureeActAnn into derniereActAnn FROM ACTIVITE_ANNEXE NATURAL JOIN PARTICIPER 

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