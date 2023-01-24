"""
The main flask app
"""

from auth import auth_blueprint, login_manager
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import current_user

# Create app
app = Flask(__name__)
app.secret_key = "some good secret key"
# ---

# Register folders
app.template_folder = "../templates"
app.static_folder = "../static"
# ---

app.register_blueprint(auth_blueprint)
app.login_manager = login_manager


@app.route("/")
def index():
    if not current_user.is_authenticated:
        return redirect(url_for("login.login"))
    session["title"] = "Bolaget eller nått"
    return render_template("index.html", user=current_user)


if __name__ == "__main__":
    app.run(debug=True)
