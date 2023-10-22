DROP TABLE IF EXISTS JOUER_INSTRU;
DROP TABLE IF EXISTS INSTRUMENT;
DROP TABLE IF EXISTS ARTISTE;
DROP TABLE IF EXISTS OCCUPER;
DROP TABLE IF EXISTS HEBERGEMENT;
DROP TABLE IF EXISTS PARTICIPER;
DROP TABLE IF EXISTS ACTIVITE_ANNEXE;
DROP TABLE IF EXISTS TYPE_ACTIVITE_ANNEXE;
DROP TABLE IF EXISTS RESERVER;
DROP TABLE IF EXISTS CONCERT;
DROP TABLE IF EXISTS BILLET;
DROP TABLE IF EXISTS DEPLACER;
DROP TABLE IF EXISTS LIEUX;
DROP TABLE IF EXISTS FAVORISER_STYLE;
DROP TABLE IF EXISTS FAVORISER_GROUPE;
DROP TABLE IF EXISTS PHOTO;
DROP TABLE IF EXISTS GROUPE;
DROP TABLE IF EXISTS FESTIVALIER;
DROP TABLE IF EXISTS STYLE_MUSIQUE;
DROP TABLE IF EXISTS TYPE_MUSIQUE;



CREATE TABLE ACTIVITE_ANNEXE (
  idActAnn int,
  descriptionActAnn VARCHAR(500),
  dateDebutActAnn datetime NOT NULL,
  dateFinActAnn datetime NOT NULL,
  idTypeActAnn int NOT NULL,
  idLieu int NOT NULL,
  constraint PK_ACTIVITE_ANNEXE PRIMARY KEY (idActAnn)
);

CREATE TABLE ARTISTE (
  idArt int,
  nomArt VARCHAR(500) NOT NULL,
  idGr int NOT NULL,
  constraint PK_ARTISTE PRIMARY KEY (idArt)
);

CREATE TABLE BILLET (
  idBil int,
  dureeValBil int NOT NULL,
  idProprietaire int NOT NULL,
  constraint PK_BILLET PRIMARY KEY (idBil)
);

CREATE TABLE PARTICIPER (
  idGr int,
  idActAnn int,
  constraint PK_PARTICIPER PRIMARY KEY (idGr, idActAnn)
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
  prenomFest varchar(20) NOT NULL,
  nomFest varchar(50) NOT NULL,
  constraint PK_FESTIVALIER PRIMARY KEY (idFest)
);

CREATE TABLE PHOTO (
  idPhoto int,
  idGr int,
  photo blob,
  constraint PK_PHOTO PRIMARY KEY (idPhoto)
);

CREATE TABLE GROUPE (
  idGr int,
  nomGr VARCHAR(500) NOT NULL,
  descriptionGr VARCHAR(500),
  reseauxGr VARCHAR(500),
  idStyle int NOT NULL,
  constraint PK_GROUPE PRIMARY KEY (idGr)
);

CREATE TABLE HEBERGEMENT (
  idHeberg int,
  libelleHeberg varchar(50) NOT NULL,
  capaciteHeberg int NOT NULL,
  constraint PK_HEBERGEMENT PRIMARY KEY (idHeberg),
  constraint CAPACITE_HEBERGEMENT_POSITIVE CHECK (capaciteHeberg > 0)
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
  constraint PK_LIEUX PRIMARY KEY (idLieu),
  constraint CAPACITE_LIEU_POSITIVE CHECK (capaciteLieu > 0)
);

CREATE TABLE DEPLACER (
  idLieuDepart int,
  idLieuArrivee int,
  tempsDeTrajet int,
  constraint PK_DEPLACER PRIMARY KEY (idLieuDepart, idLieuArrivee)
);

CREATE TABLE OCCUPER (
  idGr int,
  idHeberg int,
  dateHeberg date NOT NULL,
  constraint PK_OCCUPER PRIMARY KEY (idGr, idHeberg)
);

CREATE TABLE CONCERT (
  idConcert int,
  dateDebutConcert datetime NOT NULL,
  dateFinConcert datetime NOT NULL,
  dureeMontage int NOT NULL,
  dureeDemontage int NOT NULL,
  idGr int NOT NULL,
  idLieu int NOT NULL,
  constraint PK_CONCERT PRIMARY KEY (idConcert),
  constraint DUREE_DEMONTAGE_POSITIVE CHECK (dureeDemontage > 0),
  constraint CONCERT_APRES_14H CHECK (TIME(dateDebutConcert) >= STR_TO_DATE('14:00:00', '%H:%i:%s'))
  -- constraint CONCERT_AVANT_4H CHECK (TIME(dateDebutConcert + dateFinConcert) <= STR_TO_DATE('04:00:00', '%H:%i:%s'))
);

CREATE TABLE RESERVER (
  idConcert int,
  idBil int,
  constraint PK_RESERVER PRIMARY KEY (idConcert, idBil)
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
ALTER TABLE BILLET ADD FOREIGN KEY (idProprietaire) REFERENCES FESTIVALIER (idFest);
ALTER TABLE PARTICIPER ADD FOREIGN KEY (idActAnn) REFERENCES ACTIVITE_ANNEXE (idActAnn);
ALTER TABLE PARTICIPER ADD FOREIGN KEY (idGr) REFERENCES GROUPE (idGr);
ALTER TABLE FAVORISER_GROUPE ADD FOREIGN KEY (idGr) REFERENCES GROUPE (idGr);
ALTER TABLE FAVORISER_GROUPE ADD FOREIGN KEY (idFest) REFERENCES FESTIVALIER (idFest);
ALTER TABLE FAVORISER_STYLE ADD FOREIGN KEY (idStyle) REFERENCES STYLE_MUSIQUE (idStyle);
ALTER TABLE FAVORISER_STYLE ADD FOREIGN KEY (idFest) REFERENCES FESTIVALIER (idFest);
ALTER TABLE GROUPE ADD FOREIGN KEY (idStyle) REFERENCES STYLE_MUSIQUE (idStyle);
ALTER TABLE JOUER_INSTRU ADD FOREIGN KEY (idInstr) REFERENCES INSTRUMENT (idInstr);
ALTER TABLE JOUER_INSTRU ADD FOREIGN KEY (idArt) REFERENCES ARTISTE (idArt);
ALTER TABLE OCCUPER ADD FOREIGN KEY (idHeberg) REFERENCES HEBERGEMENT (idHeberg);
ALTER TABLE OCCUPER ADD FOREIGN KEY (idGr) REFERENCES GROUPE (idGr);
ALTER TABLE CONCERT ADD FOREIGN KEY (idLieu) REFERENCES LIEUX (idLieu);
ALTER TABLE CONCERT ADD FOREIGN KEY (idGr) REFERENCES GROUPE (idGr);
ALTER TABLE RESERVER ADD FOREIGN KEY (idBil) REFERENCES BILLET (idBil);
ALTER TABLE RESERVER ADD FOREIGN KEY (idConcert) REFERENCES CONCERT (idConcert);
ALTER TABLE STYLE_MUSIQUE ADD FOREIGN KEY (idType) REFERENCES TYPE_MUSIQUE (idType);
ALTER TABLE DEPLACER ADD FOREIGN KEY (idLieuDepart) REFERENCES LIEUX (idLieu);
ALTER TABLE DEPLACER ADD FOREIGN KEY (idLieuArrivee) REFERENCES LIEUX (idLieu);
ALTER TABLE PHOTO ADD FOREIGN KEY (idGr) REFERENCES GROUPE (idGr);
