from flask import render_template
from appFestiut import app
from flask_login import login_user , current_user, logout_user, login_required

@app.route("/")
def home():
    return render_template(
        "home.html"
    )