from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PrimaryKeyConstraint, ForeignKeyConstraint
from flask_login import UserMixin
from .app import db, login_manager

class ActiviteAnnexe(db.Model):
    __tablename__ = 'activite_annexe'
    __table_args__ = (
        PrimaryKeyConstraint('id_act_ann'),
        ForeignKeyConstraint(['id_type_act_ann'], ['type_activite_annexe.id_type_act_ann']),
        ForeignKeyConstraint(['id_gr'], ['groupe.id_gr']),
        ForeignKeyConstraint(['id_lieu'], ['lieu.id_lieu'])
    )

    id_act_ann = db.Column(db.Integer)
    description_act_ann = db.Column(db.String(500))
    date_debut_act_ann = db.Column(db.DateTime, nullable=False)
    date_fin_act_ann = db.Column(db.DateTime, nullable=False)
    id_type_act_ann = db.Column(db.Integer, nullable=False)
    id_gr = db.Column(db.Integer, nullable=False)
    id_lieu = db.Column(db.Integer, nullable=False)

class Artiste(db.Model):
    __tablename__ = 'artiste'
    __table_args__ = (
        PrimaryKeyConstraint('id_art'),
        ForeignKeyConstraint(['id_gr'], ['groupe.id_gr'])
    )

    id_art = db.Column(db.Integer)
    nom_art = db.Column(db.String(500), nullable=False)
    id_gr = db.Column(db.Integer, nullable=False)

    def get_name(self):
        return self.nom_art

class Billet(db.Model):
    __tablename__ = 'billet'
    __table_args__ = (
        PrimaryKeyConstraint('id_bil'),
        ForeignKeyConstraint(['id_proprietaire'], ['festivalier.id_fest'])
    )

    id_bil = db.Column(db.Integer)
    duree_val_bil = db.Column(db.Integer, nullable=False)
    id_proprietaire = db.Column(db.Integer, nullable=False)
    date_achat_bil = db.Column(db.Date, nullable=False)

class Participer(db.Model):
    __tablename__ = 'participer'
    __table_args__ = (
        PrimaryKeyConstraint('id_gr', 'id_act_ann'),
        ForeignKeyConstraint(['id_gr'], ['groupe.id_gr']),
        ForeignKeyConstraint(['id_act_ann'], ['activite_annexe.id_act_ann'])
    )

    id_gr = db.Column(db.Integer, nullable=False)
    id_act_ann = db.Column(db.Integer, nullable=False)

class FavoriserGroupe(db.Model):
    __tablename__ = 'favoriser_groupe'
    __table_args__ = (
        PrimaryKeyConstraint('id_fest', 'id_gr'),
        ForeignKeyConstraint(['id_fest'], ['festivalier.id_fest']),
        ForeignKeyConstraint(['id_gr'], ['groupe.id_gr'])
    )

    id_fest = db.Column(db.Integer, nullable=False)
    id_gr = db.Column(db.Integer, nullable=False)

class FavoriserArtiste(db.Model):
    __tablename__ = 'favoriser_artiste'
    __table_args__ = (
        PrimaryKeyConstraint('id_fest', 'id_art'),
        ForeignKeyConstraint(['id_fest'], ['festivalier.id_fest']),
        ForeignKeyConstraint(['id_art'], ['artiste.id_art'])
    )

    id_fest = db.Column(db.Integer, nullable=False)
    id_art = db.Column(db.Integer, nullable=False)


class FavoriserStyle(db.Model):
    __tablename__ = 'favoriser_style'
    __table_args__ = (
        PrimaryKeyConstraint('id_fest', 'id_style'),
        ForeignKeyConstraint(['id_fest'], ['festivalier.id_fest']),
        ForeignKeyConstraint(['id_style'], ['style_musique.id_style'])
    )

    id_fest = db.Column(db.Integer, nullable=False)
    id_style = db.Column(db.Integer, nullable=False)

class Festivalier(db.Model, UserMixin):
    __tablename__ = 'festivalier'
    __table_args__ = (
        PrimaryKeyConstraint('id_fest'),
    )

    id_fest = db.Column(db.String(10))
    prenom_fest = db.Column(db.String(20), nullable=False)
    nom_fest = db.Column(db.String(50), nullable=False)
    mail_fest = db.Column(db.String(50), nullable=False)
    num_fest = db.Column(db.String(10), nullable=False)
    mdp_fest = db.Column(db.String(50), nullable=False)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id_fest)

class Photo(db.Model):
    __tablename__ = 'photo'
    __table_args__ = (
        PrimaryKeyConstraint('id_photo'),
        ForeignKeyConstraint(['id_gr'], ['groupe.id_gr'])
    )

    id_photo = db.Column(db.Integer)
    id_gr = db.Column(db.Integer, nullable=False)
    photo = db.Column(db.BLOB)

class GroupeStyleAssociation(db.Model):
    __tablename__ = 'groupe_style_association'
    id_groupe = db.Column(db.Integer, db.ForeignKey('groupe.id_gr'), primary_key=True)
    id_style = db.Column(db.Integer, db.ForeignKey('style_musique.id_style'), primary_key=True)
    groupe = db.relationship('Groupe', back_populates='styles')
    style = db.relationship('StyleMusique', back_populates='groupes')

class Groupe(db.Model):
    __tablename__ = 'groupe'
    __table_args__ = (
        PrimaryKeyConstraint('id_gr'),
    )

    id_gr = db.Column(db.Integer)
    nom_gr = db.Column(db.String(500), nullable=False)
    description_gr = db.Column(db.String(500))
    reseaux_gr = db.Column(db.String(500))
    styles = db.relationship('GroupeStyleAssociation', back_populates='groupe')

    def get_name(self):
        return self.nom_gr

class Hebergement(db.Model):
    __tablename__ = 'hebergement'
    __table_args__ = (
        PrimaryKeyConstraint('id_heberg'),
    )

    id_heberg = db.Column(db.Integer)
    libelle_heberg = db.Column(db.String(50), nullable=False)
    capacite_heberg = db.Column(db.Integer, nullable=False)

class Instrument(db.Model):
    __tablename__ = 'instrument'
    __table_args__ = (
        PrimaryKeyConstraint('id_instr'),
    )

    id_instr = db.Column(db.Integer)
    instrument = db.Column(db.String(30))

class JouerInstru(db.Model):
    __tablename__ = 'jouer_instru'
    __table_args__ = (
        PrimaryKeyConstraint('id_art', 'id_instr'),
        ForeignKeyConstraint(['id_art'], ['artiste.id_art']),
        ForeignKeyConstraint(['id_instr'], ['instrument.id_instr'])
    )

    id_art = db.Column(db.Integer, nullable=False)
    id_instr = db.Column(db.Integer, nullable=False)

class Lieu(db.Model):
    __tablename__ = 'lieu'
    __table_args__ = (
        PrimaryKeyConstraint('id_lieu'),
    )

    id_lieu = db.Column(db.Integer)
    lieu = db.Column(db.String(500), nullable=False)
    capacite_lieu = db.Column(db.Integer, nullable=False)

class Deplacer(db.Model):
    __tablename__ = 'deplacer'
    __table_args__ = (
        PrimaryKeyConstraint('id_lieu_depart', 'id_lieu_arrivee'),
        ForeignKeyConstraint(['id_lieu_depart'], ['lieu.id_lieu']),
        ForeignKeyConstraint(['id_lieu_arrivee'], ['lieu.id_lieu'])
    )

    id_lieu_depart = db.Column(db.Integer, nullable=False)
    id_lieu_arrivee = db.Column(db.Integer, nullable=False)
    temps_de_trajet = db.Column(db.Integer, nullable=False)

class Occuper(db.Model):
    __tablename__ = 'occuper'
    __table_args__ = (
        PrimaryKeyConstraint('id_gr', 'id_heberg', 'date_heberg'),
        ForeignKeyConstraint(['id_gr'], ['groupe.id_gr']),
        ForeignKeyConstraint(['id_heberg'], ['hebergement.id_heberg'])
    )

    id_gr = db.Column(db.Integer, nullable=False)
    id_heberg = db.Column(db.Integer, nullable=False)
    date_heberg = db.Column(db.Date, nullable=False)

class Concert(db.Model):
    __tablename__ = 'concert'
    __table_args__ = (
        PrimaryKeyConstraint('id_concert'),
        ForeignKeyConstraint(['id_gr'], ['groupe.id_gr']),
        ForeignKeyConstraint(['id_lieu'], ['lieu.id_lieu'])
    )

    id_concert = db.Column(db.Integer)
    date_debut_concert = db.Column(db.DateTime, nullable=False)
    date_fin_concert = db.Column(db.DateTime, nullable=False)
    duree_montage = db.Column(db.Integer, nullable=False)
    duree_demontage = db.Column(db.Integer, nullable=False)
    id_gr = db.Column(db.Integer, nullable=False)
    id_lieu = db.Column(db.Integer, nullable=False)

class Reserver(db.Model):
    __tablename__ = 'reserver'
    __table_args__ = (
        PrimaryKeyConstraint('id_concert', 'id_bil'),
        ForeignKeyConstraint(['id_concert'], ['concert.id_concert']),
        ForeignKeyConstraint(['id_bil'], ['billet.id_bil'])
    )

    id_concert = db.Column(db.Integer, nullable=False)
    id_bil = db.Column(db.Integer, nullable=False)

class StyleMusique(db.Model):
    __tablename__ = 'style_musique'
    __table_args__ = (
        PrimaryKeyConstraint('id_style'),
        ForeignKeyConstraint(['id_type'], ['type_musique.id_type'])
    )

    id_style = db.Column(db.Integer)
    style = db.Column(db.String(30), nullable=False)
    id_type = db.Column(db.Integer, nullable=False)
    groupes = db.relationship('GroupeStyleAssociation', back_populates='style')

    def get_name(self):
        return self.nom_style


class TypeActiviteAnnexe(db.Model):
    __tablename__ = 'type_activite_annexe'
    __table_args__ = (
        PrimaryKeyConstraint('id_type_act_ann'),
    )

    id_type_act_ann = db.Column(db.Integer)
    activite = db.Column(db.String(500), nullable=False)

class TypeMusique(db.Model):
    __tablename__ = 'type_musique'
    __table_args__ = (
        PrimaryKeyConstraint('id_type'),
    )

    id_type = db.Column(db.Integer)
    type = db.Column(db.String(30), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return Festivalier.query.get(int(user_id))
