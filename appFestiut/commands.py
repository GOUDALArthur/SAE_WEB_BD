import click
from .app import app, db
from .models import GroupeStyleAssociation, FavoriserArtiste,Festivalier,Deplacer,Reserver,Concert,Occuper,Hebergement,Participer,Billet,Lieu,TypeActiviteAnnexe,JouerInstru ,Instrument, Artiste, TypeMusique, FavoriserGroupe, FavoriserStyle, Groupe, Photo, StyleMusique, ActiviteAnnexe, FavoriserGroupe, FavoriserStyle, Festivalier, Photo, Groupe, StyleMusique, ActiviteAnnexe
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

    type1 = TypeMusique(id_type=6, type="Rock")
    db.session.add(type1)

    artist1 = Artiste(id_art=1, nom_art="Rocky", id_gr=1)
    db.session.add(artist1)

    artist2 = Artiste(id_art=2, nom_art="Mimi", id_gr=1)
    db.session.add(artist2)

    instr1 = Instrument(id_instr=1, instrument="Guitar")
    db.session.add(instr1)

    jouer1 = JouerInstru(id_art=1, id_instr=1)
    db.session.add(jouer1)

    act1 = ActiviteAnnexe(id_act_ann=1, titre_act_ann = "Visite du lac de Patate" ,  description_act_ann="Fun activity", date_debut_act_ann=datetime.now(), 
                          date_fin_act_ann=datetime.now(), id_type_act_ann=1, id_lieu=1)
    db.session.add(act1)

    type_act1 = TypeActiviteAnnexe(id_type_act_ann=1, activite="Music")
    db.session.add(type_act1)


    billet1 = Billet(id_bil=1, duree_val_bil=3, id_proprietaire=1, date_achat_bil=datetime.now().date())
    db.session.add(billet1)

    part1 = Participer(id_gr=1, id_act_ann=1)
    db.session.add(part1)

    photo1 = Photo(id_photo=1, id_gr=1, photo=b'\x00\x01\x02\x03')
    db.session.add(photo1)


    occ1 = Occuper(id_gr=1, id_heberg=1, date_heberg=datetime.now().date())
    db.session.add(occ1)

    concert1 = Concert(id_concert=1, date_debut_concert=datetime.now(), date_fin_concert=datetime.now(), 
                       duree_montage=2, duree_demontage=2, id_gr=1, id_lieu=1)
    db.session.add(concert1)

    res1 = Reserver(id_concert=1, id_bil=1)
    db.session.add(res1)
    
    
    db.session.add(TypeMusique(id_type=1, type="Pop"))
    db.session.add(TypeMusique(id_type=2, type="RB"))
    db.session.add(TypeMusique(id_type=3, type="Hip-Hop"))
    db.session.add(TypeMusique(id_type=4, type="Reggeaton"))
    db.session.add(TypeMusique(id_type=5, type="Rock"))

    db.session.add(StyleMusique(id_style=1, style="Pop", id_type=1))
    db.session.add(StyleMusique(id_style=2, style="Dance-Pop", id_type=1))
    db.session.add(StyleMusique(id_style=3, style="Pop Rock", id_type=1))
    db.session.add(StyleMusique(id_style=4, style="Alternative", id_type=1))
    db.session.add(StyleMusique(id_style=5, style="Indie Pop", id_type=1))
    db.session.add(StyleMusique(id_style=6, style="Electropop", id_type=1))
    db.session.add(StyleMusique(id_style=7, style="Synth-Pop", id_type=1))
    db.session.add(StyleMusique(id_style=8, style="Pop", id_type=2))
    db.session.add(StyleMusique(id_style=9, style="Alternatif", id_type=2))
    db.session.add(StyleMusique(id_style=10, style="Rap", id_type=3))
    db.session.add(StyleMusique(id_style=11, style="Trap", id_type=3))
    db.session.add(StyleMusique(id_style=12, style="Hip-Hop", id_type=3))
    db.session.add(StyleMusique(id_style=13, style="Reggeaton", id_type=4))
    db.session.add(StyleMusique(id_style=14, style="K-Pop", id_type=1))
    db.session.add(StyleMusique(id_style=15, style="Alternatif", id_type=5))
    db.session.add(StyleMusique(id_style=16, style="Soul", id_type=2))


    db.session.add(Groupe(id_gr=1, nom_gr="Billie Eilish", description_gr="Billie Eilish Pirate Baird O'Connell, née le 18 décembre 2001 à Los Angeles, est une autrice-compositrice-interprète américaine. Elle commence à chanter très jeune et écrit ses premières chansons à l'âge de 11 ans, inspirée par les artistes de Lana Del Rey et d'Avril Lavigne. Elle est révélée en 2016 par le single Ocean Eyes, publié sur SoundCloud.", reseaux_gr="https://www.instagram.com/billieeilish/"))
    db.session.add(Groupe(id_gr=2, nom_gr="The Weeknd", description_gr="Abel Makkonen Tesfaye, dit The Weeknd, né le 16 février 1990 à Toronto, au Canada, est un auteur-compositeur-interprète, musicien et producteur canadien. Il publie plusieurs morceaux sur YouTube sous le nom de The Weeknd en 2010 et sort l'année suivante les mixtapes House of Balloons, Thursday et Echoes of Silence, ainsi que la compilation Trilogy en 2012.", reseaux_gr="https://www.instagram.com/theweeknd/"))
    db.session.add(Groupe(id_gr=3, nom_gr="Dua Lipa", description_gr="Dua Lipa, née le 22 août 1995 à Londres, est une autrice-compositrice-interprète et mannequin britannique. En 2015, elle signe avec Warner Bros. Records et publie son premier single, New Love, peu de temps après. En décembre 2016, un documentaire sur sa vie et sa carrière est diffusé sur la chaîne YouTube de The Fader.", reseaux_gr="https://www.instagram.com/dualipa/"))
    db.session.add(Groupe(id_gr=4, nom_gr="Post Malone", description_gr="Austin Richard Post, dit Post Malone, né le 4 juillet 1995 à Syracuse, dans l'État de New York, est un rappeur, chanteur et producteur américain. Il se fait connaître en 2015 avec le titre White Iverson, publié sur sa page SoundCloud, qui cumule plus de 800 millions de vues sur YouTube.", reseaux_gr="https://www.instagram.com/postmalone/"))
    db.session.add(Groupe(id_gr=5, nom_gr="BTS", description_gr="BTS, également connu sous le nom de Bangtan Sonyeondan, est un groupe de K-pop sud-coréen formé en 2013 par Big Hit Entertainment. Le groupe est composé de sept membres, à savoir RM, Jin, Suga, J-Hope, Jimin, V et Jungkook. BTS est reconnu pour ses performances énergiques et ses paroles engagées, et il est devenu un phénomène mondial de la musique pop.", reseaux_gr="https://www.instagram.com/bts.bighitofficial/"))
    db.session.add(Groupe(id_gr=6, nom_gr="Megan Thee Stallion", description_gr="Megan Jovon Ruth Pete, dite Megan Thee Stallion, née le 15 février 1995 à San Antonio, au Texas, est une rappeuse, auteure-compositrice-interprète et actrice américaine. Elle signe au label indépendant 1501 Certified Entertainment en 2018, et sort les mixtapes Fever en 2019 et Suga en 2020.", reseaux_gr="https://www.instagram.com/theestallion/"))
    db.session.add(Groupe(id_gr=7, nom_gr="Harry Styles", description_gr="Harry Edward Styles, né le 1er février 1994 à Redditch, dans le Worcestershire, est un chanteur, parolier et acteur britannique. Membre de la formation One Direction, il est révélé par l'émission The X Factor au Royaume-Uni en 2010.", reseaux_gr="https://www.instagram.com/harrystyles/"))
    db.session.add(Groupe(id_gr=8, nom_gr="Taylor Swift", description_gr="Taylor Alison Swift, née le 13 décembre 1989 à Reading, en Pennsylvanie, est une autrice-compositrice-interprète et actrice américaine. Elle est sous contrat avec le label indépendant Big Machine Records, et est la plus jeune artiste à avoir signé avec la maison d'édition de musique Sony/ATV Music Publishing.", reseaux_gr="https://www.instagram.com/taylorswift/"))
    db.session.add(Groupe(id_gr=9, nom_gr="Bad Bunny", description_gr="Benito Antonio Martínez Ocasio, dit Bad Bunny, né le 10 mars 1994 à San Juan, à Porto Rico, est un rappeur, chanteur et auteur-compositeur portoricain. Il est considéré comme l'un des artistes latinos les plus populaires au monde.", reseaux_gr="https://www.instagram.com/badbunnypr/"))
    db.session.add(Groupe(id_gr=10, nom_gr="Ariana Grande", description_gr="Ariana Grande-Butera, dite Ariana Grande, née le 26 juin 1993 à Boca Raton, en Floride, est une actrice et autrice-compositrice-interprète américaine. Elle commence sa carrière en 2008, à l'âge de 15 ans, en jouant le rôle de Charlotte dans la comédie musicale 13 à Broadway.", reseaux_gr="https://www.instagram.com/arianagrande/"))
    db.session.add(Groupe(id_gr=11, nom_gr="Drake", description_gr="Aubrey Drake Graham, dit Drake, né le 24 octobre 1986 à Toronto, au Canada, est un rappeur, chanteur, auteur-compositeur-interprète, producteur, acteur et entrepreneur canadien. Il est le fondateur du label OVO Sound.", reseaux_gr="https://www.instagram.com/champagnepapi/"))
    db.session.add(Groupe(id_gr=12, nom_gr="Cardi B", description_gr="Belcalis Marlenis Almánzar, dite Cardi B, née le 11 octobre 1992 dans le Bronx à New York, est une rappeuse, autrice-compositrice et actrice américaine. Elle est devenue célèbre en 2017 grâce à son titre Bodak Yellow.", reseaux_gr="https://www.instagram.com/iamcardib/"))
    db.session.add(Groupe(id_gr=13, nom_gr="Dababy", description_gr="Jonathan Lyndale Kirk, dit DaBaby, né le 22 décembre 1991 à Cleveland, dans l'Ohio, est un rappeur et auteur-compositeur-interprète américain. Il se fait connaître en 2019 avec son deuxième album studio, Kirk, qui débute en tête du Billboard 200.", reseaux_gr="https://www.instagram.com/dababy/"))
    db.session.add(Groupe(id_gr=14, nom_gr="Doja Cat", description_gr="Amala Ratna Zandile Dlamini, dite Doja Cat, née le 21 octobre 1995 à Los Angeles, en Californie, est une rappeuse, chanteuse, auteure-compositrice-interprète et productrice américaine. Elle se fait connaître en 2018 avec son single Mooo!, qui devient viral sur YouTube.", reseaux_gr="https://www.instagram.com/dojacat/"))
    db.session.add(Groupe(id_gr=15, nom_gr="Justin Bieber", description_gr="Justin Drew Bieber, né le 1er mars 1994 à London, en Ontario, est un auteur-compositeur-interprète et acteur canadien. L'agent artistique Scooter Braun le repère en 2008, après avoir visionné ses vidéos sur YouTube, et le présente au chanteur Usher, qui lui permet de signer chez le label RBMG, une coentreprise de Scooter et Usher, puis chez Island Records.", reseaux_gr="https://www.instagram.com/justinbieber/"))
    db.session.add(Groupe(id_gr=16, nom_gr="Lady Gaga", description_gr="Stefani Joanne Angelina Germanotta, dite Lady Gaga, née le 28 mars 1986 dans le quartier de Manhattan, à New York, est une auteure-compositrice-interprète et actrice américaine. Élevée à New York, elle étudie au couvent du Sacré-Cœur puis parvient à être sélectionnée pour la prestigieuse Tisch School of the Arts de l'université de New York.", reseaux_gr="https://www.instagram.com/ladygaga/"))
    db.session.add(Groupe(id_gr=17, nom_gr="Travis Scott", description_gr="Jacques Berman Webster II, dit Travis Scott, né le 30 avril 1992 à Houston, au Texas, est un rappeur, chanteur, producteur et réalisateur artistique américain. Il commence sa carrière en 2008, à l'âge de 16 ans, sous le nom de scène de Travis Scott.", reseaux_gr="https://www.instagram.com/travisscott/"))
    db.session.add(Groupe(id_gr=18, nom_gr="Miley Cyrus", description_gr="Miley Ray Cyrus, de son vrai nom Destiny Hope Cyrus, née le 23 novembre 1992 à Nashville, dans le Tennessee, est une auteure-compositrice-interprète et actrice américaine. Elle rencontre la célébrité à l'adolescence en incarnant Miley Stewart / Hannah Montana dans une série de Disney Channel, Hannah Montana, où elle joue avec son père Billy Ray Cyrus.", reseaux_gr="https://www.instagram.com/mileycyrus/"))
    db.session.add(Groupe(id_gr=19, nom_gr="Kanye West", description_gr="Kanye Omari West, né le 8 juin 1977 à Atlanta, en Géorgie, est un rappeur, auteur-compositeur-interprète, réalisateur artistique, réalisateur, scénariste, acteur, producteur de cinéma et de télévision américain, originaire de Chicago, dans l'Illinois. Il est marié à Kim Kardashian depuis 2014.", reseaux_gr="https://www.instagram.com/kanyewest/"))
    db.session.add(Groupe(id_gr=20, nom_gr="Imagine Dragons", description_gr="Imagine Dragons est un groupe de rock alternatif américain, originaire de Las Vegas, dans le Nevada. Imagine Dragons est formé en 2008 alors que le chanteur Dan Reynolds est à l'université Brigham Young. Le groupe compte au total quatre albums studio : Night Visions en 2012, Smoke + Mirrors en 2015, Evolve en 2017 et Origins en 2018.", reseaux_gr="https://www.instagram.com/imaginedragons/"))

    db.session.add(GroupeStyleAssociation(id_groupe=1, id_style=4))
    db.session.add(GroupeStyleAssociation(id_groupe=2, id_style=8))
    db.session.add(GroupeStyleAssociation(id_groupe=2, id_style=9))
    db.session.add(GroupeStyleAssociation(id_groupe=3, id_style=4))
    db.session.add(GroupeStyleAssociation(id_groupe=4, id_style=10))
    db.session.add(GroupeStyleAssociation(id_groupe=5, id_style=14))
    db.session.add(GroupeStyleAssociation(id_groupe=6, id_style=11))
    db.session.add(GroupeStyleAssociation(id_groupe=7, id_style=3))
    db.session.add(GroupeStyleAssociation(id_groupe=8, id_style=5))
    db.session.add(GroupeStyleAssociation(id_groupe=9, id_style=13))
    db.session.add(GroupeStyleAssociation(id_groupe=10, id_style=6))
    db.session.add(GroupeStyleAssociation(id_groupe=10, id_style=8))
    db.session.add(GroupeStyleAssociation(id_groupe=11, id_style=11))
    db.session.add(GroupeStyleAssociation(id_groupe=12, id_style=11))
    db.session.add(GroupeStyleAssociation(id_groupe=13, id_style=11))
    db.session.add(GroupeStyleAssociation(id_groupe=14, id_style=6))
    db.session.add(GroupeStyleAssociation(id_groupe=15, id_style=3))
    db.session.add(GroupeStyleAssociation(id_groupe=16, id_style=7))
    db.session.add(GroupeStyleAssociation(id_groupe=17, id_style=11))
    db.session.add(GroupeStyleAssociation(id_groupe=18, id_style=1))
    db.session.add(GroupeStyleAssociation(id_groupe=19, id_style=12))
    db.session.add(GroupeStyleAssociation(id_groupe=20, id_style=3))
    db.session.add(GroupeStyleAssociation(id_groupe=20, id_style=15))


    db.session.add(Lieu(id_lieu=1, lieu="Scène Principale", capacite_lieu=10000))
    db.session.add(Lieu(id_lieu=2, lieu="Scène secondaire", capacite_lieu=3000))
    db.session.add(Lieu(id_lieu=3, lieu="Zone Chill", capacite_lieu=500))
    db.session.add(Lieu(id_lieu=4, lieu="Salle Intime", capacite_lieu=1000))
    db.session.add(Lieu(id_lieu=5, lieu="Plateau radio", capacite_lieu=0))
    temps_de_trajet = {
        (1, 2): 10,
        (1, 3): 15,
        (1, 4): 20,
        (1, 5): 25,

        (2, 3): 8,
        (2, 4): 18,
        (2, 5): 30,

        (3, 4): 12,
        (3, 5): 22,

        (4, 5): 15
    }
    for (id_lieu_depart, id_lieu_arrivee), temps in temps_de_trajet.items():
        db.session.add(Deplacer(
            id_lieu_depart=id_lieu_depart,
            id_lieu_arrivee=id_lieu_arrivee,
            temps_de_trajet=temps
        ))


    db.session.add(Artiste(id_art=24, nom_art="Billie Eilish", id_gr=1))
    db.session.add(Artiste(id_art=25, nom_art="The Weeknd", id_gr=2))
    db.session.add(Artiste(id_art=3, nom_art="Dua Lipa", id_gr=3))
    db.session.add(Artiste(id_art=4, nom_art="Post Malone", id_gr=4))
    db.session.add(Artiste(id_art=5, nom_art="BTS", id_gr=5))
    db.session.add(Artiste(id_art=6, nom_art="Megan Thee Stallion", id_gr=6))
    db.session.add(Artiste(id_art=7, nom_art="Harry Styles", id_gr=7))
    db.session.add(Artiste(id_art=8, nom_art="Taylor Swift", id_gr=8))
    db.session.add(Artiste(id_art=9, nom_art="Bad Bunny", id_gr=9))
    db.session.add(Artiste(id_art=10, nom_art="Ariana Grande", id_gr=10))
    db.session.add(Artiste(id_art=11, nom_art="Drake", id_gr=11))
    db.session.add(Artiste(id_art=12, nom_art="Cardi B", id_gr=12))
    db.session.add(Artiste(id_art=13, nom_art="Dababy", id_gr=13))
    db.session.add(Artiste(id_art=14, nom_art="Doja Cat", id_gr=14))
    db.session.add(Artiste(id_art=15, nom_art="Justin Bieber", id_gr=15))
    db.session.add(Artiste(id_art=16, nom_art="Lady Gaga", id_gr=16))
    db.session.add(Artiste(id_art=17, nom_art="Travis Scott", id_gr=17))
    db.session.add(Artiste(id_art=18, nom_art="Miley Cyrus", id_gr=18))
    db.session.add(Artiste(id_art=19, nom_art="Kanye West", id_gr=19))
    db.session.add(Artiste(id_art=20, nom_art="Dan Reynolds", id_gr=20))
    db.session.add(Artiste(id_art=21, nom_art="Wayne Sermon", id_gr=20))
    db.session.add(Artiste(id_art=22, nom_art="Ben McKee", id_gr=20))
    db.session.add(Artiste(id_art=23, nom_art="Daniel Platzman", id_gr=20))

    db.session.commit()

    db.session.commit()