
import datetime
from re import RegexFlag
from flask import redirect, render_template, request, url_for
from . import *
from flask_login import login_user , current_user, logout_user, login_required
from wtforms import EmailField, StringField, HiddenField, PasswordField, DateField,SelectField,SelectMultipleField,TextAreaField
from wtforms.validators import InputRequired, Email, Length, EqualTo, ValidationError
from flask_wtf import FlaskForm
from hashlib import sha256
from .models import *
from flask import request, flash
from datetime import timedelta , datetime
from sqlalchemy import desc





@app.route("/")
def home():
    if current_user.is_authenticated:
        return render_template("page_connecter.html")
    else:
        return render_template("home.html")
    
@app.route("/logout/")
def logout():
    """Pour se déconnecter"""
    logout_user()
    return redirect(url_for("home"))

class LoginForm(FlaskForm):
    mail = StringField("Email",validators=[InputRequired()])
    password = PasswordField("Password",validators=[InputRequired()])
    next = HiddenField()

    def get_authenticated_user(self):
        """Renvoie l'utilisateur connecté """
        user = Festivalier.query.filter_by(mail_fest=self.mail.data).first()
        if user is None:
            return None
        musicien_mdp = user.mdp_fest
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()                    
        return user if passwd == musicien_mdp else None

@app.route("/login/", methods=("GET", "POST",))
def login():
    """Affiche la page de login
    """
    f = LoginForm()
    if not f.is_submitted():
        f.next.data = request.args.get("next")

    elif f.validate_on_submit():

        if f.mail.data == "admin@gmail.com" and f.password.data == "admin":
            user = Festivalier.query.filter_by(mail_fest="admin@gmail.com").first()
            login_user(user)
            next = f.next.data or url_for("home")
            return redirect(next)
        
    
        else:
            user = f.get_authenticated_user()
            if user:
                login_user(user)
                next = f.next.data or url_for("home")
                return redirect(next)
    return render_template("login.html",form=f)



@app.route("/billet/", methods=("GET", "POST"))
def acheter():
    """Affiche la page de login"""
    
    return render_template("billet.html")

class AjoutBillet(FlaskForm):
    jours = StringField("Jours",validators=[InputRequired()])
    id_proprietaire = StringField("Id proprietaire",validators=[InputRequired()])
    next = HiddenField()
    
    
@app.route('/confirmation_billet', methods=['POST'])
def confirmation_billet():
    form = AjoutBillet(request.form)
    if current_user.is_authenticated:
        ticket_type = request.form.get('ticket_type')
        if ticket_type == 'days':
            jours = form.jours.data
            id_proprietaire = form.id_proprietaire.data
            return render_template("payment_days.html", jours=jours,id_proprietaire=id_proprietaire, form=form)
        else:
            return render_template("payment_all.html", jours=100, form=form)
    else:
        return redirect(url_for('login'))

@app.route('/buy_ticket', methods=['POST'])
def enregistrement_billet():
    form = AjoutBillet(request.form)
    if form.validate_on_submit():
        jours = int(request.form.get('jours'))
        id_proprietaire = int(request.form.get('id_proprietaire'))

        billet = Billet(duree_val_bil=jours, id_proprietaire=id_proprietaire, date_achat_bil=datetime.datetime.now().date())

        try:
            
            db.session.add(billet)
            db.session.commit()
        except Exception as e:
            print("Error adding billet to database:", e)
            db.session.rollback()

        return render_template("home.html")
    else:
        print("Form errors:", form.errors)
    return render_template("billet.html", form=form)




class RegisterForm(FlaskForm):
    nom = StringField("Nom", validators=[InputRequired()])
    prenom = StringField("Prenom", validators=[InputRequired()])
    mail = EmailField("Mail", validators=[InputRequired()])
    num = StringField("Numéro", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    next = HiddenField()
    
import tkinter
from tkinter import messagebox

def afficher_popup(message):
    root = tkinter.Tk()
    root.withdraw()
    messagebox.showinfo("Message", message)
    root.destroy()

    

@app.route("/create-user/", methods=("GET","POST",))
def creer_user():
    """Affiche le formulaire de création d'un utilisateur
    """
    form =RegisterForm()
    if form.is_submitted():
        existing_user = Festivalier.query.filter_by(mail_fest=form.mail.data).first()
        if existing_user:
            afficher_popup('Ce mail est déjà utilisé,veuillez utiliser un autre.')
            return render_template("register.html", form=form)
        
        password_hash = sha256(form.password.data.encode()).hexdigest()
        new_personne = Festivalier(mail_fest=form.mail.data,mdp_fest=password_hash,nom_fest=form.nom.data,prenom_fest=form.prenom.data,num_fest=form.num.data)

        try:
            
            db.session.add(new_personne)
            db.session.commit()
            login_user(new_personne)
        except Exception as e:
            print("Error adding billet to database:", e)
            db.session.rollback()

        return redirect(url_for("home"))
    return render_template("register.html", form=form)


class ChangeProfilForm(FlaskForm):
    nom = StringField("Nom")
    prenom = StringField("Prenom")
    mail = EmailField("Mail")
    num = StringField("Numero")
    password = PasswordField("Password")
    next = HiddenField()


@app.route("/change-profil/",methods=("GET","POST",))
def changer_profil():
    """Affiche le formulaire de mise à jour de profil
    """
    u  = current_user.id_fest
    user = Festivalier.query.get(u) 
    f = ChangeProfilForm()

    if f.is_submitted():
        existing_user = Festivalier.query.filter(Festivalier.mail_fest==f.mail.data, Festivalier.id_fest!=u).first()

        if existing_user:
            afficher_popup('Ce mail est déjà utilisé,veuillez utiliser un autre.')
            return render_template("profil.html", form=f)
        
        if f.password.data !="":
            password_hash = sha256(f.password.data.encode()).hexdigest()
            user.mdp_fest = password_hash
        user.nom_fest = f.nom.data
        user.prenom_fest = f.prenom.data
        user.num_fest =  f.num.data
        user.mail_fest = f.mail.data

        db.session.commit()
        return redirect(url_for("home"))
    return render_template("profil.html", form=f)


@app.route("/tickes/")
def mes_tickets():
    """Affiche les billets achetés par l'utilisateur actuel
    """
    user_id = current_user.id_fest
    tickets = Billet.query.filter_by(id_proprietaire=user_id).all()

    return render_template("tickets.html", tickets=tickets, timedelta=timedelta)

from flask import jsonify

from flask import request

@app.route('/search', methods=['POST'])
def search():
    search_term = request.form.get('searched')

    groupes = Groupe.query.filter(Groupe.nom_gr.contains(search_term)).all()
    artistes = Artiste.query.filter(Artiste.nom_art.contains(search_term)).all()
    styles = StyleMusique.query.filter(StyleMusique.style.contains(search_term)).all()

    results = groupes + artistes + styles

    return render_template('search.html', results=results, search_term=search_term)


@app.route('/add_to_favorites', methods=['POST'])
def add_to_favorites():
    id = request.form.get('id')
    type = request.form.get('type')
    print(type)
    print(id)

    if type == 'group':
        favorite = FavoriserGroupe.query.filter_by(id_fest=current_user.id_fest, id_gr=id).first()

        if favorite:
            return jsonify({'message': 'Group already in favorites'}), 400

        new_favorite = FavoriserGroupe(id_fest=current_user.id_fest, id_gr=id)
    elif type == 'style':
        favorite = FavoriserStyle.query.filter_by(id_fest=current_user.id_fest, id_style=id).first()

        if favorite:
            return jsonify({'message': 'Style already in favorites'}), 400

        new_favorite = FavoriserStyle(id_fest=current_user.id_fest, id_style=id)
        
    elif type == 'artist':
        favorite = FavoriserArtiste.query.filter_by(id_fest=current_user.id_fest, id_art=id).first()

        if favorite:
            return jsonify({'message': 'Artist already in favorites'}), 400

        new_favorite = FavoriserArtiste(id_fest=current_user.id_fest, id_art=id)
    
    else:
        return jsonify({'message': 'Invalid type'}), 400

    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({'message': f'{type.capitalize()} added to favorites'}), 200



def avoir_favorites():
    favorite_groups = FavoriserGroupe.query.filter_by(id_fest=current_user.id_fest).all()
    favorite_groups = [(Groupe.query.get(favorite.id_gr), 'group') for favorite in favorite_groups]

    favorite_styles = FavoriserStyle.query.filter_by(id_fest=current_user.id_fest).all()
    favorite_styles = [(StyleMusique.query.get(favorite.id_style), 'style') for favorite in favorite_styles]

    favorite_artists = FavoriserArtiste.query.filter_by(id_fest=current_user.id_fest).all()
    favorite_artists = [(Artiste.query.get(favorite.id_art), 'artist') for favorite in favorite_artists]

    favorites = favorite_groups + favorite_styles + favorite_artists

    return favorites

@app.route('/favorites', methods=['GET'])
@login_required
def get_favorites():
    favorites = avoir_favorites()
    return render_template('favori.html', favorites=favorites)

@app.route('/remove_favorite/<int:favorite_id>', methods=['POST'])
@login_required
def remove_favorite(favorite_id):
    favorite_type = request.args.get('type')

    print(favorite_type)
    print(favorite_id)

    if favorite_type == 'group':
        favorite = FavoriserGroupe.query.get((current_user.id_fest, favorite_id))
    elif favorite_type == 'style':
        favorite = FavoriserStyle.query.get((current_user.id_fest, favorite_id))
    elif favorite_type == 'artist':
        favorite = FavoriserArtiste.query.get((current_user.id_fest, favorite_id))

    if favorite:
        db.session.delete(favorite)
        db.session.commit()

    favorites = avoir_favorites()
    return render_template('favori.html', favorites=favorites)

@app.route('/ajout_artiste', methods=['GET','POST'])
def get_page_artiste():
    return render_template('ajoutArtiste.html')

@app.route('/add_artist', methods=['GET','POST'])
def add_artist():
    artist_name = request.form.get('nom_art')

    existing_artist = Artiste.query.filter_by(nom_art=artist_name).first()
    if existing_artist:
        afficher_popup('Cet artiste existe déja.')
        return render_template('ajoutArtiste.html')


    new_artist = Artiste(nom_art=artist_name, id_gr=0)
    db.session.add(new_artist)
    db.session.commit()

    afficher_popup('Artiste ajouté.')
    return render_template('ajoutArtiste.html')


def get_style():
    styles = StyleMusique.query.all()
    for style in styles:
        type_musique = TypeMusique.query.filter_by(id_type=style.id_type).first()
        style.type_name = type_musique.type if type_musique else "No type"
    return styles

@app.route('/ajout_groupe', methods=['GET','POST'])
def get_page_groupe():   
    return render_template('ajoutGroupe.html', styles=get_style())

    
@app.route('/add_group', methods=['GET','POST'])
def add_group():





    styles = db.session.query(StyleMusique, TypeMusique).join(TypeMusique, StyleMusique.id_type == TypeMusique.id_type).all()
    group_name = request.form.get('nom_gr')
    description_gr = request.form.get('description_gr')
    reseau_gr = request.form.get('reseau_gr')
    style_id = request.form.getlist('style')
    print(style_id)

    existing_group = Groupe.query.filter_by(nom_gr=group_name).first()
    if existing_group:
        afficher_popup('Ce groupe existe déja.')
        return render_template('ajoutGroupe.html', styles=get_style())
    new_group = Groupe(nom_gr=group_name, description_gr=description_gr, reseaux_gr=reseau_gr)
    
    db.session.add(new_group)
    db.session.commit()
    for style_ids in style_id:
        asso_style = GroupeStyleAssociation(id_groupe=new_group.id_gr, id_style=style_ids)
        db.session.add(asso_style)
        db.session.commit()
    afficher_popup('Groupe ajouté.')
    return render_template('ajoutGroupe.html', styles=get_style())


@app.route('/ajout_activite', methods=['GET','POST'])
def get_page_activite():
    lieu = Lieu.query.all()
    type_acti = TypeActiviteAnnexe.query.all()
    return render_template('ajoutActivite.html', lieu=lieu, type_acti=type_acti)


@app.route('/add_activity', methods=['GET','POST'])
def add_activity():
    lieu = Lieu.query.all()
    type_acti = TypeActiviteAnnexe.query.all()
    if request.method == 'POST':
        titre_act_ann = request.form.get('titre_act_ann')
        description_act_ann = request.form.get('description_act_ann')
        date_debut_act_ann = datetime.strptime(request.form.get('date_debut_act_ann'), '%Y-%m-%dT%H:%M')
        date_fin_act_ann = datetime.strptime(request.form.get('date_fin_act_ann'), '%Y-%m-%dT%H:%M')
        id_type_act_ann = request.form.get('id_type_act_ann')
        id_lieu = request.form.get('id_lieu')

        if date_debut_act_ann >= date_fin_act_ann:
            afficher_popup('La date de début doit être inférieure à la date de fin.')
            return render_template('ajoutActivite.html', lieu=lieu, type_acti=type_acti)

        new_activity = ActiviteAnnexe(titre_act_ann=titre_act_ann,description_act_ann=description_act_ann, date_debut_act_ann=date_debut_act_ann, date_fin_act_ann=date_fin_act_ann, id_type_act_ann=id_type_act_ann, id_lieu=id_lieu)
        db.session.add(new_activity)
        db.session.commit()

        afficher_popup('Activité ajoutée.')
        return render_template('ajoutActivite.html', lieu=lieu, type_acti=type_acti)
    
@app.route('/ajout_concert', methods=['GET','POST'])
def get_page_concert():
    lieu = Lieu.query.all()
    groupe = Groupe.query.all()
    return render_template('ajoutConcert.html', lieu=lieu, groupe=groupe)

@app.route('/add_concert', methods=['GET','POST'])
def add_concert():
    lieu = Lieu.query.all()
    groupe = Groupe.query.all()
    if request.method == 'POST':
        date_debut_concert = datetime.strptime(request.form.get('date_debut_concert'), '%Y-%m-%dT%H:%M')
        date_fin_concert = datetime.strptime(request.form.get('date_fin_concert'), '%Y-%m-%dT%H:%M')
        duree_montage = int(request.form.get('duree_montage'))
        duree_demontage = int(request.form.get('duree_demontage'))
        id_gr = request.form.get('id_gr')
        id_lieu = request.form.get('id_lieu')

        if date_debut_concert >= date_fin_concert:
            afficher_popup('La date de début doit être inférieure à la date de fin.')
            return render_template('ajoutConcert.html', lieu=lieu, groupe=groupe)
                # Vérification si le groupe est disponible pour assurer le concert
        dernier_concert = (
            Concert.query
            .filter(Concert.id_gr == id_gr)
            .filter(Concert.date_fin_concert <= date_debut_concert)
            .order_by(Concert.date_fin_concert.desc())
            .first()
        )
        prochain_concert = (
            Concert.query
            .filter(Concert.id_gr == id_gr)
            .filter(Concert.date_debut_concert >= date_fin_concert)
            .order_by(Concert.date_debut_concert)
            .first()
        )
        derniere_act = (
            ActiviteAnnexe.query
            .filter(ActiviteAnnexe.id_gr == id_gr)
            .filter(ActiviteAnnexe.date_fin_act_ann <= date_debut_concert)
            .order_by(ActiviteAnnexe.date_fin_act_ann.desc())
            .first()
        )
        prochaine_act = (
            ActiviteAnnexe.query
            .filter(ActiviteAnnexe.id_gr == id_gr)
            .filter(ActiviteAnnexe.date_debut_act_ann >= date_fin_concert)
            .order_by(ActiviteAnnexe.date_debut_act_ann)
            .first()
        )

        if dernier_concert and derniere_act:
            if dernier_concert.date_fin_concert < derniere_act.date_fin_act_ann:
                dernier_concert = derniere_act
        elif derniere_act:
            dernier_concert = derniere_act

        if prochain_concert and prochaine_act:
            if prochain_concert.date_debut_concert > prochaine_act.date_debut_act_ann:
                prochain_concert = prochaine_act
        elif prochaine_act:
            prochain_concert = prochaine_act

        if dernier_concert is not None:
            dernier_trajet = (
                Deplacer.query
                .filter(Deplacer.id_lieu_depart == dernier_concert.id_lieu)
                .filter(Deplacer.id_lieu_arrivee == id_lieu)
                .first()
            )
            if dernier_trajet is None:   
                dernier_trajet = (
                    Deplacer.query
                    .filter(Deplacer.id_lieu_arrivee == dernier_concert.id_lieu)
                    .filter(Deplacer.id_lieu_depart == id_lieu)
                    .first()
                )
            derniere_dispo = date_debut_concert - timedelta(minutes=dernier_trajet.temps_de_trajet) if dernier_trajet is not None else None

        if prochain_concert is not None:
            prochain_trajet = (
                Deplacer.query
                .filter(Deplacer.id_lieu_depart == prochain_concert.id_lieu)
                .filter(Deplacer.id_lieu_arrivee == id_lieu)
                .first()
            )
            if prochain_trajet is None:   
                prochain_trajet = (
                    Deplacer.query
                    .filter(Deplacer.id_lieu_arrivee == prochain_concert.id_lieu)
                    .filter(Deplacer.id_lieu_depart == id_lieu)
                    .first()
                )
            prochaine_dispo = date_fin_concert + timedelta(minutes=prochain_trajet.temps_de_trajet) if prochain_trajet is not None else None

        if dernier_concert is not None and dernier_concert.date_fin_concert >= derniere_dispo or prochain_concert is not None and prochain_concert.date_debut_concert <= prochaine_dispo:
            afficher_popup("Le groupe n'est pas disponible à ce moment.")
            return render_template('ajoutConcert.html', lieu=lieu, groupe=groupe)

        # Vérification si le lieu est disponible pour accueillir le concert
        dernier_concert = (
            Concert.query
            .filter(Concert.id_lieu == id_lieu)
            .filter(Concert.date_fin_concert <= date_debut_concert)
            .order_by(Concert.date_debut_concert.desc())
            .first()
        )
        prochain_concert = (
            Concert.query
            .filter(Concert.id_lieu == id_lieu)
            .filter(Concert.date_debut_concert >= date_fin_concert)
            .order_by(Concert.date_debut_concert)
            .first()
        )

        derniere_dispo = date_debut_concert - timedelta(minutes=dernier_concert.duree_demontage) - timedelta(minutes=duree_montage) if dernier_concert is not None else None
        prochaine_dispo = date_fin_concert + timedelta(minutes=prochain_concert.duree_montage) + timedelta(minutes=duree_demontage) if prochain_concert is not None else None
        if dernier_concert is not None and dernier_concert.date_fin_concert >= derniere_dispo or prochain_concert is not None and prochain_concert.date_debut_concert <= prochaine_dispo:
            afficher_popup("Le lieu n'est pas disponible à ce moment.")
            return render_template('ajoutConcert.html', lieu=lieu, groupe=groupe)

        new_concert = Concert(date_debut_concert=date_debut_concert, date_fin_concert=date_fin_concert, duree_montage=duree_montage, duree_demontage=duree_demontage, id_gr=id_gr, id_lieu=id_lieu)
        db.session.add(new_concert)
        db.session.commit()

        afficher_popup('Concert ajouté.')
        return render_template('ajoutConcert.html', lieu=lieu, groupe=groupe)





@app.route('/voir_prochain', methods=['GET','POST'])
def get_prochain_page():
    concerts = Concert.query.all()
    activities = ActiviteAnnexe.query.all()
    return render_template('voir_prochain.html', concerts=concerts, activities=activities)


@app.context_processor
def utility_processor():
    def get_lieu_by_id(id_lieu):
        lieu = Lieu.query.get(id_lieu)
        return lieu.lieu if lieu else None
    return dict(get_lieu_by_id=get_lieu_by_id)

@app.context_processor
def utility_processor():
    def get_groupe_by_id(id_g):
        groupe = Groupe.query.get(id_g)
        return groupe.nom_gr if groupe else None
    return dict(get_groupe_by_id=get_groupe_by_id)



