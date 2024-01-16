from flask import redirect, render_template, request, url_for
from appFestiut import app
from flask_login import login_user , current_user, logout_user, login_required
from wtforms import EmailField, StringField, HiddenField, PasswordField, DateField,SelectField,SelectMultipleField,TextAreaField
from wtforms.validators import InputRequired, Email, Length, EqualTo, ValidationError
from flask_wtf import FlaskForm

@app.route("/")
def home():
    return render_template("home.html")

class LoginForm(FlaskForm):
    mail = StringField("Email",validators=[InputRequired()])
    password = PasswordField("Password",validators=[InputRequired()])
    next = HiddenField()

@app.route("/login/", methods=("GET", "POST",))
def login():
    """Affiche la page de login
    """
    f = LoginForm()
    if not f.is_submitted():
        f.next.data = request.args.get("next")
    return render_template("login.html",form=f)



@app.route("/billet/", methods=("GET", "POST",))
def acheter():
    """Affiche la page de login
    """
    return render_template("billet.html")


@app.route('/acheter_billet', methods=['POST'])
def acheter_billet():
    ticket_type = request.form.get('ticket_type')
    return redirect(url_for('confirmation_billet'))

@app.route('/confirmation_billet', methods=['GET', 'POST'])
def confirmation_billet():
    return render_template('confirmation_billet.html')

@app.route('/confirmation_billet', methods=['GET', 'POST'])
def payer_billet():
    return render_template("home.html")