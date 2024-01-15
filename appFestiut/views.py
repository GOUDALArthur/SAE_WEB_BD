
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
from datetime import timedelta



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





@app.route('/favorites', methods=['GET'])
@login_required
def get_favorites():
    favorite_groups = FavoriserGroupe.query.filter_by(id_fest=current_user.id_fest).all()
    favorite_groups = [(Groupe.query.get(favorite.id_gr), 'group') for favorite in favorite_groups]

    favorite_styles = FavoriserStyle.query.filter_by(id_fest=current_user.id_fest).all()
    favorite_styles = [(StyleMusique.query.get(favorite.id_style), 'style') for favorite in favorite_styles]

    favorite_artists = FavoriserArtiste.query.filter_by(id_fest=current_user.id_fest).all()
    favorite_artists = [(Artiste.query.get(favorite.id_art), 'artist') for favorite in favorite_artists]

    favorites = favorite_groups + favorite_styles + favorite_artists

    return render_template('favori.html', favorites=favorites)


