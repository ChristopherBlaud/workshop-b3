from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from email.mime.text import MIMEText

# Initialisation de l'application Flask
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Nécessaire pour les sessions et les flash messages

# Configuration de SQLAlchemy pour utiliser SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de SQLAlchemy
db = SQLAlchemy(app)


class IdentificationCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'<IdentificationCode {self.code}>'
    
# Modèle pour la table "User"
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)  # Assure-toi que cette ligne est là
    email = db.Column(db.String(120), unique=True, nullable=False)
    identification_code = db.Column(db.String(50), nullable=False)


# Crée la base de données et la table si elles n'existent pas encore
with app.app_context():
    db.create_all()


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        identification_code = request.form['auth-code']  # Correction ici

        # Vérifier si le code d'authentification existe
        existing_code = IdentificationCode.query.filter_by(code=identification_code).first()
        if not existing_code:
            flash('Code d\'authentification invalide.')
            return redirect(url_for('register'))

        # Vérifier si l'email est déjà utilisé
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Cet email est déjà utilisé. Veuillez en choisir un autre.')
            return redirect(url_for('register'))

        # Créer un nouvel utilisateur et l'ajouter à la base de données
        new_user = User(firstname=firstname, lastname=lastname, password=password, email=email, identification_code=identification_code)
        db.session.add(new_user)
        db.session.commit()

        flash('Inscription réussie ! Vous pouvez maintenant vous connecter.')
        return redirect(url_for('register'))

    return render_template('register.html')  # Affiche la page d'inscription



@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Rechercher l'utilisateur dans la base de données par email
        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            session['user'] = {'firstname': user.firstname, 'lastname': user.lastname, 'email': user.email}
            flash(f'Connexion réussie, bienvenue {user.firstname} {user.lastname}!')
            return redirect(url_for('dashboard'))
        else:
            flash('Email ou mot de passe incorrect.')
            return redirect(url_for('login'))

    return render_template('login.html')

# Route de la page d'accueil une fois connecté
@app.route('/dashboard')
def dashboard():
    # Vérifier si l'utilisateur est connecté
    if 'user' in session:
        user = session['user']
        return render_template('dashboard.html', user=user)
    else:
        flash('Veuillez vous connecter pour accéder à cette page.')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Déconnexion réussie.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=False)