import click
from .app import app, db
from .models import FavoriserArtiste,Festivalier,Deplacer,Reserver,Concert,Occuper,Hebergement,Participer,Billet,Lieu,TypeActiviteAnnexe,JouerInstru ,Instrument, Artiste, TypeMusique, FavoriserGroupe, FavoriserStyle, Groupe, Photo, StyleMusique, ActiviteAnnexe, FavoriserGroupe, FavoriserStyle, Festivalier, Photo, Groupe, StyleMusique, ActiviteAnnexe
from hashlib import sha256
from datetime import datetime




@app.cli.command()
def syncdb():
    """Create all missing tables"""
    db.create_all()

    user = Festivalier(id_fest=0, prenom_fest="ad", nom_fest="ad", mail_fest="admin@gmail.com", mdp_fest=sha256("admin".encode()).hexdigest(), num_fest="982732837")    
    db.session.add(user)

    user1 = Festivalier(id_fest=1, prenom_fest="Karim", nom_fest="Poulet", mail_fest="b@gmail.com", 
                        mdp_fest=sha256("b".encode()).hexdigest(), num_fest="982732837")
    db.session.add(user1)

    type1 = TypeMusique(id_type=1, type_mus="Rock")
    db.session.add(type1)

    style1 = StyleMusique(id_style=1, style="Hard Rock", id_type=1)
    db.session.add(style1)

    style2 = StyleMusique(id_style=2, style="electro", id_type=1)
    db.session.add(style2)

    group = Groupe(id_gr=0, nom_gr="solo", description_gr="A rock band", reseaux_gr="www.therockers.com", id_style=1)
    db.session.add(group)

    group1 = Groupe(id_gr=1, nom_gr="The Rockers", description_gr="A rock band", reseaux_gr="www.therockers.com", id_style=1)
    db.session.add(group1)

    group2 = Groupe(id_gr=3, nom_gr="The caca", description_gr="A rock band", reseaux_gr="www.therockers.com", id_style=1)
    db.session.add(group2)

    artist1 = Artiste(id_art=1, nom_art="Rocky", id_gr=1)
    db.session.add(artist1)

    artist2 = Artiste(id_art=2, nom_art="Mimi", id_gr=1)
    db.session.add(artist2)

    instr1 = Instrument(id_instr=1, instrument="Guitar")
    db.session.add(instr1)

    jouer1 = JouerInstru(id_art=1, id_instr=1)
    db.session.add(jouer1)

    act1 = ActiviteAnnexe(id_act_ann=1, description_act_ann="Fun activity", date_debut_act_ann=datetime.now(), 
                          date_fin_act_ann=datetime.now(), id_type_act_ann=1, id_lieu=1)
    db.session.add(act1)

    type_act1 = TypeActiviteAnnexe(id_type_act_ann=1, activite="Music")
    db.session.add(type_act1)

    lieu1 = Lieu(id_lieu=1, lieu="Concert Hall", capacite_lieu=500)
    db.session.add(lieu1)

    billet1 = Billet(id_bil=1, duree_val_bil=3, id_proprietaire=1, date_achat_bil=datetime.now().date())
    db.session.add(billet1)

    part1 = Participer(id_gr=1, id_act_ann=1)
    db.session.add(part1)

    photo1 = Photo(id_photo=1, id_gr=1, photo=b'\x00\x01\x02\x03')
    db.session.add(photo1)

    heberg1 = Hebergement(id_heberg=1, libelle_heberg="Hotel", capacite_heberg=100)
    db.session.add(heberg1)

    occ1 = Occuper(id_gr=1, id_heberg=1, date_heberg=datetime.now().date())
    db.session.add(occ1)

    concert1 = Concert(id_concert=1, date_debut_concert=datetime.now(), date_fin_concert=datetime.now(), 
                       duree_montage=2, duree_demontage=2, id_gr=1, id_lieu=1)
    db.session.add(concert1)

    res1 = Reserver(id_concert=1, id_bil=1)
    db.session.add(res1)

    dep1 = Deplacer(id_lieu_depart=1, id_lieu_arrivee=2, temps_de_trajet=30)
    db.session.add(dep1)

    db.session.commit()