DROP TABLE IF EXISTS JOUER_INSTRU;
DROP TABLE IF EXISTS INSTRUMENT;
DROP TABLE IF EXISTS ARTISTE;
DROP TABLE IF EXISTS OCCUPER;
DROP TABLE IF EXISTS HEBERGEMENT;
DROP TABLE IF EXISTS EFFECTUER;
DROP TABLE IF EXISTS ACTIVITE_ANNEXE;
DROP TABLE IF EXISTS TYPE_ACTIVITE_ANNEXE;
DROP TABLE IF EXISTS RESERVER;
DROP TABLE IF EXISTS CONCERT;
DROP TABLE IF EXISTS BILLET;
DROP TABLE IF EXISTS LIEUX;
DROP TABLE IF EXISTS FAVORISER_STYLE;
DROP TABLE IF EXISTS FAVORISER_GROUPE;
DROP TABLE IF EXISTS GROUPE;
DROP TABLE IF EXISTS FESTIVALIER;
DROP TABLE IF EXISTS STYLE_MUSIQUE;
DROP TABLE IF EXISTS TYPE_MUSIQUE;



CREATE TABLE ACTIVITE_ANNEXE (
  idActAnn int,
  descriptionActAnn VARCHAR(500),
  dateActAnn date NOT NULL,
  dureeActAnn float(2,1) NOT NULL,
  idTypeActAnn int NOT NULL,
  idLieu int NOT NULL,
  constraint PK_ACTIVITE_ANNEXE PRIMARY KEY (idActAnn),
  constraint TIME_ACTIVITE_ANNEXE CHECK (dureeActAnn > 0)
);

CREATE TABLE ARTISTE (
  idArt int,
  nomArt VARCHAR(500) NOT NULL,
  idGr int NOT NULL,
  constraint PK_ARTISTE PRIMARY KEY (idArt)
);

CREATE TABLE BILLET (
  idBil int,
  dureeValBil float(3,1) NOT NULL,
  idFest int NOT NULL,
  constraint PK_BILLET PRIMARY KEY (idBil)
);

CREATE TABLE EFFECTUER (
  idGr int,
  idActAnn int,
  constraint PK_EFFECTUER PRIMARY KEY (idGr, idActAnn)
);

CREATE TABLE FAVORISER_GROUPE (
  idFest int,
  idGr int,
  constraint PK_FAVORISER_GROUPE PRIMARY KEY (idFest, idGr)
);

CREATE TABLE FAVORISER_STYLE (
  idFest int,
  idStyle int,
  constraint PK_FAVORISER_STYLE PRIMARY KEY (idFest, idStyle)
);

CREATE TABLE FESTIVALIER (
  idFest int,
  prenomFest varchar(20),
  nomFest varchar(50) NOT NULL,
  constraint PK_FESTIVALIER PRIMARY KEY (idFest)
);

CREATE TABLE GROUPE (
  idGr int,
  nomGr VARCHAR(500) NOT NULL,
  descriptionGr VARCHAR(500),
  photosGr VARCHAR(42),
  reseauxGr VARCHAR(500),
  idStyle int NOT NULL,
  constraint PK_GROUPE PRIMARY KEY (idGr)
);

CREATE TABLE HEBERGEMENT (
  idHeberg int,
  libelleHeberg varchar(50) NOT NULL,
  capaciteHeberg int NOT NULL,
  constraint PK_HEBERGEMENT PRIMARY KEY (idHeberg),
  constraint CAPACITE_HEBERGEMENT CHECK (capaciteHeberg > 0)
);

CREATE TABLE INSTRUMENT (
  idInstr int,
  instrument varchar(30),
  constraint PK_INSTRUMENT PRIMARY KEY (idInstr)
);

CREATE TABLE JOUER_INSTRU (
  idArt int,
  idInstr int,
  constraint PK_JOUER_INSTRU PRIMARY KEY (idArt, idInstr)
);

CREATE TABLE LIEUX (
  idLieu int,
  lieu VARCHAR(500) NOT NULL,
  capaciteLieu int NOT NULL,
  photosLieu VARCHAR(42),
  constraint PK_LIEUX PRIMARY KEY (idLieu),
  constraint CAPACITE_LIEU CHECK (capaciteLieu > 0)
);

CREATE TABLE OCCUPER (
  idGr int,
  idHeberg int,
  dateHeberg date NOT NULL,
  constraint PK_OCCUPER PRIMARY KEY (idGr, idHeberg)
  -- constraint DATE_HEBERGEMENT CHECK (dateHeberg >= NOW())
);

CREATE TABLE CONCERT (
  idConcert int,
  dateConcert date NOT NULL,
  dureeConcert float(2,1) NOT NULL,
  dureeMontage float(2,1) NOT NULL,
  dureeDemontage float(2,1) NOT NULL,
  idGr int NOT NULL,
  idLieu int NOT NULL,
  constraint PK_CONCERT PRIMARY KEY (idConcert),
  -- constraint DATE_CONCERT CHECK (dateConcert >= NOW()),
  constraint DUREE_CONCERT CHECK (dureeConcert > 0),
  constraint DUREE_MONTAGE CHECK (dureeMontage > 0),
  constraint DUREE_DEMONTAGE CHECK (dureeDemontage > 0)
);

CREATE TABLE RESERVER (
  idConcert int,
  idBil int,
  constraint PK_RESERVER PRIMARY KEY (idConcert, idBil)
  -- constraint BILLET_VALIDE CHECK (getDureeBilletRestante(idBil) > idBil)
);

CREATE TABLE STYLE_MUSIQUE (
  idStyle int,
  style varchar(30) NOT NULL,
  idType int NOT NULL,
  constraint PK_STYLE_MUSIQUE PRIMARY KEY (idStyle)
);

CREATE TABLE TYPE_ACTIVITE_ANNEXE (
  idTypeActAnn int,
  activite VARCHAR(500) NOT NULL,
  constraint PK_TYPE_ACTIVITE_ANNEXE PRIMARY KEY (idTypeActAnn)
);

CREATE TABLE TYPE_MUSIQUE (
  idType int,
  typeMus varchar(30) NOT NULL,
  constraint PK_TYPE_MUSIQUE PRIMARY KEY (idType)
);

ALTER TABLE ACTIVITE_ANNEXE ADD FOREIGN KEY (idLieu) REFERENCES LIEUX (idLieu);
ALTER TABLE ACTIVITE_ANNEXE ADD FOREIGN KEY (idTypeActAnn) REFERENCES TYPE_ACTIVITE_ANNEXE (idTypeActAnn);
ALTER TABLE ARTISTE ADD FOREIGN KEY (idGr) REFERENCES GROUPE (idGr);
ALTER TABLE BILLET ADD FOREIGN KEY (idFest) REFERENCES FESTIVALIER (idFest);
ALTER TABLE EFFECTUER ADD FOREIGN KEY (idActAnn) REFERENCES ACTIVITE_ANNEXE (idActAnn);
ALTER TABLE EFFECTUER ADD FOREIGN KEY (idGr) REFERENCES GROUPE (idGr);
ALTER TABLE FAVORISER_GROUPE ADD FOREIGN KEY (idGr) REFERENCES GROUPE (idGr);
ALTER TABLE FAVORISER_GROUPE ADD FOREIGN KEY (idFest) REFERENCES FESTIVALIER (idFest);
ALTER TABLE FAVORISER_STYLE ADD FOREIGN KEY (idStyle) REFERENCES STYLE_MUSIQUE (idStyle);
ALTER TABLE FAVORISER_STYLE ADD FOREIGN KEY (idFest) REFERENCES FESTIVALIER (idFest);
ALTER TABLE GROUPE ADD FOREIGN KEY (idStyle) REFERENCES STYLE_MUSIQUE (idStyle);
ALTER TABLE JOUER_INSTRU ADD FOREIGN KEY (idInstr) REFERENCES INSTRUMENT (idInstr);
ALTER TABLE JOUER_INSTRU ADD FOREIGN KEY (idArt) REFERENCES ARTISTE (idArt);
-- ALTER TABLE LIEUX ADD FOREIGN KEY (idLieu_1) REFERENCES LIEUX (idLieu);
ALTER TABLE OCCUPER ADD FOREIGN KEY (idHeberg) REFERENCES HEBERGEMENT (idHeberg);
ALTER TABLE OCCUPER ADD FOREIGN KEY (idGr) REFERENCES GROUPE (idGr);
ALTER TABLE CONCERT ADD FOREIGN KEY (idLieu) REFERENCES LIEUX (idLieu);
ALTER TABLE CONCERT ADD FOREIGN KEY (idGr) REFERENCES GROUPE (idGr);
ALTER TABLE RESERVER ADD FOREIGN KEY (idBil) REFERENCES BILLET (idBil);
ALTER TABLE RESERVER ADD FOREIGN KEY (idConcert) REFERENCES CONCERT (idConcert);
ALTER TABLE STYLE_MUSIQUE ADD FOREIGN KEY (idType) REFERENCES TYPE_MUSIQUE (idType);


DELIMITER |

create or replace trigger compareDureeBillet before insert on RESERVER for each row
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
  end if;
  SELECT dureeConcert into dureeC FROM CONCERT WHERE idConcert = new.idConcert;
  if dureeRestante < dureeC then
    set mes = concat('Réservation impossible billet ', new.idBil, ': Concert trop long pour la validité restante du billet');
    signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
  end if;
end|

DELIMITER ;