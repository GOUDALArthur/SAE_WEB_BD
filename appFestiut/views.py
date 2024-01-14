from flask import redirect, render_template, request, url_for
from . import *
from flask_login import login_user , current_user, logout_user, login_required
from wtforms import EmailField, StringField, HiddenField, PasswordField, DateField,SelectField,SelectMultipleField,TextAreaField
from wtforms.validators import InputRequired, Email, Length, EqualTo, ValidationError
from flask_wtf import FlaskForm
from hashlib import sha256
from .models import *
from flask import request

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

        # Créer un nouveau billet
        billet = Billet(duree_val_bil=jours, id_proprietaire=id_proprietaire)

        # Ajouter le billet à la base de données
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

