import click
from .app import app, db
from .models import Festivalier, FavoriserGroupe, FavoriserStyle, Groupe, Photo, StyleMusique, ActiviteAnnexe, FavoriserGroupe, FavoriserStyle, Festivalier, Photo, Groupe, StyleMusique, ActiviteAnnexe
from hashlib import sha256



@app.cli.command()
def syncdb():
    """Create all missing tables"""
    db.create_all()
    user1 = Festivalier(id_fest=1 ,prenom_fest="Karim",nom_fest="Poulet", mail_fest = "b@gmail.com", mdp_fest = sha256("b".encode()).hexdigest())

    db.session.add(user1)
    db.session.commit()
