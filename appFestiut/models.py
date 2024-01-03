from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///festival.db'
db = SQLAlchemy(app)

class ActiviteAnnexe(db.Model):
    __tablename__ = 'ACTIVITE_ANNEXE'

    idActAnn = db.Column(db.Integer, primary_key=True)
    descriptionActAnn = db.Column(db.String(500))
    dateDebutActAnn = db.Column(db.DateTime, nullable=False)
    dateFinActAnn = db.Column(db.DateTime, nullable=False)
    idTypeActAnn = db.Column(db.Integer, db.ForeignKey('TYPE_ACTIVITE_ANNEXE.idTypeActAnn'), nullable=False)
    idLieu = db.Column(db.Integer, db.ForeignKey('LIEUX.idLieu'), nullable=False)

class Artiste(db.Model):
    __tablename__ = 'ARTISTE'

    idArt = db.Column(db.Integer, primary_key=True)
    nomArt = db.Column(db.String(500), nullable=False)
    idGr = db.Column(db.Integer, db.ForeignKey('GROUPE.idGr'), nullable=False)
    
class Billet(db.Model):
    __tablename__ = 'BILLET'

    idBil = db.Column(db.Integer, primary_key=True)
    dureeValBil = db.Column(db.Integer, nullable=False)
    idProprietaire = db.Column(db.Integer, db.ForeignKey('FESTIVALIER.idFest'), nullable=False)

class Participer(db.Model):
    __tablename__ = 'PARTICIPER'

    idGr = db.Column(db.Integer, db.ForeignKey('GROUPE.idGr'), primary_key=True)
    idActAnn = db.Column(db.Integer, db.ForeignKey('ACTIVITE_ANNEXE.idActAnn'), primary_key=True)

class FavoriserGroupe(db.Model):
    __tablename__ = 'FAVORISER_GROUPE'

    idFest = db.Column(db.Integer, db.ForeignKey('FESTIVALIER.idFest'), primary_key=True)
    idGr = db.Column(db.Integer, db.ForeignKey('GROUPE.idGr'), primary_key=True)

class FavoriserStyle(db.Model):
    __tablename__ = 'FAVORISER_STYLE'

    idFest = db.Column(db.Integer, db.ForeignKey('FESTIVALIER.idFest'), primary_key=True)
    idStyle = db.Column(db.Integer, db.ForeignKey('STYLE_MUSIQUE.idStyle'), primary_key=True)

class Festivalier(db.Model):
    __tablename__ = 'FESTIVALIER'

    idFest = db.Column(db.Integer, primary_key=True)
    prenomFest = db.Column(db.String(20), nullable=False)
    nomFest = db.Column(db.String(50), nullable=False)

class Photo(db.Model):
    __tablename__ = 'PHOTO'

    idPhoto = db.Column(db.Integer, primary_key=True)
    idGr = db.Column(db.Integer, db.ForeignKey('GROUPE.idGr'), nullable=False)
    photo = db.Column(db.BLOB)

class Groupe(db.Model):
    __tablename__ = 'GROUPE'

    idGr = db.Column(db.Integer, primary_key=True)
    nomGr = db.Column(db.String(500), nullable=False)
    descriptionGr = db.Column(db.String(500))
    reseauxGr = db.Column(db.String(500))
    idStyle = db.Column(db.Integer, db.ForeignKey('STYLE_MUSIQUE.idStyle'), nullable=False)

class Hebergement(db.Model):
    __tablename__ = 'HEBERGEMENT'

    idHeberg = db.Column(db.Integer, primary_key=True)
    libelleHeberg = db.Column(db.String(50), nullable=False)
    capaciteHeberg = db.Column(db.Integer, nullable=False)

class Instrument(db.Model):
    __tablename__ = 'INSTRUMENT'

    idInstr = db.Column(db.Integer, primary_key=True)
    instrument = db.Column(db.String(30))

class JouerInstru(db.Model):
    __tablename__ = 'JOUER_INSTRU'

    idArt = db.Column(db.Integer, db.ForeignKey('ARTISTE.idArt'), primary_key=True)
    idInstr = db.Column(db.Integer, db.ForeignKey('INSTRUMENT.idInstr'), primary_key=True)

class Lieux(db.Model):
    __tablename__ = 'LIEUX'

    idLieu = db.Column(db.Integer, primary_key=True)
    lieu = db.Column(db.String(500), nullable=False)
    capaciteLieu = db.Column(db.Integer, nullable=False)

class Deplacer(db.Model):
    __tablename__ = 'DEPLACER'

    idLieuDepart = db.Column(db.Integer, db.ForeignKey('LIEUX.idLieu'), primary_key=True)
    idLieuArrivee = db.Column(db.Integer, db.ForeignKey('LIEUX.idLieu'), primary_key=True)
    tempsDeTrajet = db.Column(db.Integer, nullable=False)

class Occuper(db.Model):
    __tablename__ = 'OCCUPER'

    idGr = db.Column(db.Integer, db.ForeignKey('GROUPE.idGr'), primary_key=True)
    idHeberg = db.Column(db.Integer, db.ForeignKey('HEBERGEMENT.idHeberg'), primary_key=True)
    dateHeberg = db.Column(db.Date, nullable=False)

class Concert(db.Model):
    __tablename__ = 'CONCERT'

    idConcert = db.Column(db.Integer, primary_key=True)
    dateDebutConcert = db.Column(db.DateTime, nullable=False)
    dateFinConcert = db.Column(db.DateTime, nullable=False)
    dureeMontage = db.Column(db.Integer, nullable=False)
    dureeDemontage = db.Column(db.Integer, nullable=False)
    idGr = db.Column(db.Integer, db.ForeignKey('GROUPE.idGr'), nullable=False)
    idLieu = db.Column(db.Integer, db.ForeignKey('LIEUX.idLieu'), nullable=False)

class Reserver(db.Model):
    __tablename__ = 'RESERVER'

    idConcert = db.Column(db.Integer, db.ForeignKey('CONCERT.idConcert'), primary_key=True)
    idBil = db.Column(db.Integer, db.ForeignKey('BILLET.idBil'), primary_key=True)

class StyleMusique(db.Model):
    __tablename__ = 'STYLE_MUSIQUE'

    idStyle = db.Column(db.Integer, primary_key=True)
    style = db.Column(db.String(30), nullable=False)
    idType = db.Column(db.Integer, db.ForeignKey('TYPE_MUSIQUE.idType'), nullable=False)

class TypeActiviteAnnexe(db.Model):
    __tablename__ = 'TYPE_ACTIVITE_ANNEXE'

    idTypeActAnn = db.Column(db.Integer, primary_key=True)
    activite = db.Column(db.String(500), nullable=False)

class TypeMusique(db.Model):
    __tablename__ = 'TYPE_MUSIQUE'

    idType = db.Column(db.Integer, primary_key=True)
    typeMus = db.Column(db.String(30), nullable=False)
    
    

