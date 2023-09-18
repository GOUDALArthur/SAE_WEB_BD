USE 'GROUPES';

CREATE TABLE 'ACTIVITE_ANNEXE' (
  'idActAnn' int,
  'description' varchar2,
  'dateActAnn' date NOT NULL,
  'dureeActAnn' int NOT NULL,
  'idTypeActAnn' int,
  'idLieu' int,
  constraint PK_ACTIVITE_ANNEXE PRIMARY KEY ('idActAnn')
);

CREATE TABLE 'ARTISTE' (
  'idArt' int,
  'nomArt' varchar2 NOT NULL,
  'idGr' int,
  constraint PK_ARTISTE PRIMARY KEY ('idArt')
);

CREATE TABLE 'BILLET' (
  'idBil' int,
  'dureeValBil' int NOT NULL,
  'idFest' int,
  constraint PK_BILLET PRIMARY KEY ('idBil')
);

CREATE TABLE 'EFFECTUER' (
  'idGr' int,
  'idActAnn' int,
  constraint PK_EFFECTUER PRIMARY KEY ('idGr', 'idActAnn')
);

CREATE TABLE 'FAVORISER_GROUPE' (
  'idFest' int,
  'idGr' int,
  constraint PK_FAVORISER_GROUPE PRIMARY KEY ('idFest', 'idGr')
);

CREATE TABLE 'FAVORISER_STYLE' (
  'idFest' int,
  'idStyle' int,
  constraint PK_FAVORISER_STYLE PRIMARY KEY ('idFest', 'idStyle')
);

CREATE TABLE 'FESTIVALIER' (
  'idFest' int,
  'prenomFest' varchar(20),
  'nomFest' varchar(50) NOT NULL,
  constraint PK_FESTIVALIER PRIMARY KEY ('idFest')
);

CREATE TABLE 'GROUPE' (
  'idGr' int,
  'nomGr' varchar2 NOT NULL,
  'descriptionGr' varchar2,
  'photosGr' VARCHAR(42),
  'reseauxGr' varchar2,
  'idStyle' int,
  constraint PK_GROUPE PRIMARY KEY ('idGr')
);

CREATE TABLE 'HEBERGEMENT' (
  'idHeberg' int,
  'libelleHeberg' varchar(50) NOT NULL,
  'capaciteHeberg' int NOT NULL,
  constraint PK_HEBERGEMENT PRIMARY KEY ('idHeberg')
);

CREATE TABLE 'INSTRUMENT' (
  'idInstr' int,
  'instrument' varchar(30),
  constraint PK_INSTRUMENT PRIMARY KEY ('idInstr')
);

CREATE TABLE 'JOUER_INSTRU' (
  'idArt' int,
  'idInstr' int,
  constraint PK_JOUER_INSTRU PRIMARY KEY ('idArt', 'idInstr')
);

CREATE TABLE 'LIEUX' (
  'idLieu' int,
  'lieu' varchar2 NOT NULL,
  'capacite' int NOT NULL,
  'photosLieu' VARCHAR(42),
  constraint PK_LIEUX PRIMARY KEY ('idLieu')
);

CREATE TABLE 'OCCUPER' (
  'idGr' int,
  'idHeberg' int,
  'dateHeberg' date,
  constraint PK_OCCUPER PRIMARY KEY ('idGr', 'idHeberg')
);

CREATE TABLE 'CONCERT' (
  'idConcert' int,
  'dateConcert' date NOT NULL,
  'dureeConcert' int NOT NULL,
  'dureeMontage' int NOT NULL,
  'dureeDemontage' int NOT NULL,
  'idGr' int,
  'idLieu' int,
  constraint PK_CONCERT PRIMARY KEY ('idConcert')
);

CREATE TABLE 'RESERVER' (
  'idConcert' int,
  'idBil' int,
  constraint PK_RESERVER PRIMARY KEY ('idConcert', 'idBil')
);

CREATE TABLE 'STYLE_MUSIQUE' (
  'idStyle' int,
  'style' varchar(30) NOT NULL,
  'idType' int,
  constraint PK_STYLE_MUSIQUE PRIMARY KEY ('idStyle')
);

CREATE TABLE 'TYPE_ACTIVITE_ANNEXE' (
  'idTypeActAnn' int,
  'activite' varchar2 NOT NULL,
  constraint PK_TYPE_ACTIVITE_ANNEXE PRIMARY KEY ('idTypeActAnn')
);

CREATE TABLE 'TYPE_MUSIQUE' (
  'idType' int,
  'type' varchar(30) NOT NULL,
  constraint PK_TYPE_MUSIQUE PRIMARY KEY ('idType')
);

ALTER TABLE 'ACTIVITE_ANNEXE' ADD FOREIGN KEY ('idLieu') REFERENCES 'LIEUX' ('idLieu');
ALTER TABLE 'ACTIVITE_ANNEXE' ADD FOREIGN KEY ('idTypeActAnn') REFERENCES 'TYPE_ACTIVITE_ANNEXE' ('idTypeActAnn');
ALTER TABLE 'ARTISTE' ADD FOREIGN KEY ('idGr') REFERENCES 'GROUPE' ('idGr');
ALTER TABLE 'BILLET' ADD FOREIGN KEY ('idFest') REFERENCES 'FESTIVALIER' ('idFest');
ALTER TABLE 'EFFECTUER' ADD FOREIGN KEY ('idActAnn') REFERENCES 'ACTIVITE_ANNEXE' ('idActAnn');
ALTER TABLE 'EFFECTUER' ADD FOREIGN KEY ('idGr') REFERENCES 'GROUPE' ('idGr');
ALTER TABLE 'FAVORISER_GROUPE' ADD FOREIGN KEY ('idGr') REFERENCES 'GROUPE' ('idGr');
ALTER TABLE 'FAVORISER_GROUPE' ADD FOREIGN KEY ('idFest') REFERENCES 'FESTIVALIER' ('idFest');
ALTER TABLE 'FAVORISER_STYLE' ADD FOREIGN KEY ('idStyle') REFERENCES 'STYLE_MUSIQUE' ('idStyle');
ALTER TABLE 'FAVORISER_STYLE' ADD FOREIGN KEY ('idFest') REFERENCES 'FESTIVALIER' ('idFest');
ALTER TABLE 'GROUPE' ADD FOREIGN KEY ('idStyle') REFERENCES 'STYLE_MUSIQUE' ('idStyle');
ALTER TABLE 'JOUER_INSTRU' ADD FOREIGN KEY ('idInstr') REFERENCES 'INSTRUMENT' ('idInstr');
ALTER TABLE 'JOUER_INSTRU' ADD FOREIGN KEY ('idArt') REFERENCES 'ARTISTE' ('idArt');
ALTER TABLE 'LIEUX' ADD FOREIGN KEY ('idLieu_1') REFERENCES 'LIEUX' ('idLieu');
ALTER TABLE 'OCCUPER' ADD FOREIGN KEY ('idHeberg') REFERENCES 'HEBERGEMENT' ('idHeberg');
ALTER TABLE 'OCCUPER' ADD FOREIGN KEY ('idGr') REFERENCES 'GROUPE' ('idGr');
ALTER TABLE 'CONCERT' ADD FOREIGN KEY ('idLieu') REFERENCES 'LIEUX' ('idLieu');
ALTER TABLE 'CONCERT' ADD FOREIGN KEY ('idGr') REFERENCES 'GROUPE' ('idGr');
ALTER TABLE 'RESERVER' ADD FOREIGN KEY ('idBil') REFERENCES 'BILLET' ('idBil');
ALTER TABLE 'RESERVER' ADD FOREIGN KEY ('idConcert') REFERENCES 'CONCERT' ('idConcert');
ALTER TABLE 'STYLE_MUSIQUE' ADD FOREIGN KEY ('idType') REFERENCES 'TYPE_MUSIQUE' ('idType');