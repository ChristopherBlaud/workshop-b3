from flask import Flask, jsonify, render_template, request, redirect, url_for,  flash, session
import sqlite3


# Initialisation de l'application Flask
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Nécessaire pour les sessions et les flash messages

# Fonction de connexion à la base de données SQLite
def get_db_connection():
    conn = sqlite3.connect('CampusConnect.db')
    conn.row_factory = sqlite3.Row
    return conn


# Code utilisé pour créer la base de données et les tables
# Utilise ces lignes pour créer la base de données et les tables lors de la première exécution :
# Connexion à la base de données

conn = sqlite3.connect('CampusConnect.db')
# Creation de la table user_activity

conn.execute('''
    CREATE TABLE IF NOT EXISTS user_activity (
        user_id INTEGER,
        activity_id INTEGER,
        PRIMARY KEY (user_id, activity_id),
        FOREIGN KEY  (user_id) REFERENCES users(id),
        FOREIGN KEY (activity_id) REFERENCES activity(id)
   ); 
''')

#Création du modèle d'actité "Activity"
conn.execute('''
    CREATE TABLE IF NOT EXISTS activity (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT UNIQUE NOT NULL,
        type TEXT NOT NULL,
        description TEXT UNIQUE NOT NULL
    );
''')

# Création de la table 'users'
conn.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        firstname TEXT NOT NULL,
        lastname TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        identification_code TEXT NOT NULL,
        campus_location TEXT NOT NULL,
        Admin INTEGER 
    );
''')

# Création de la table 'identification_codes'
conn.execute('''
    CREATE TABLE IF NOT EXISTS identification_codes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE NOT NULL
    );
''')

# Sauvegarde des modifications et fermeture de la connexion
conn.commit()
conn.close()


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        identification_code = request.form['auth-code']
        campus = request.form['campus']  

        # Connexion a la base de donnée
        conn = get_db_connection()

        # Vérification du code d'authentification
        existing_code = conn.execute('SELECT * FROM identification_codes WHERE code = ?', (identification_code,)).fetchone()
        if not existing_code:
            flash('Code d\'authentification invalide.')
            return redirect(url_for('register'))

        # Vérification de l'existence de l'email
        existing_user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        if existing_user:
            flash('Cet email est déjà utilisé. Veuillez en choisir un autre.')
            return redirect(url_for('register'))

        # Ajout de l'utilisateur à la base de données
        conn.execute('INSERT INTO users (firstname, lastname, email, password, identification_code, campus_location) VALUES (?, ?, ?, ?, ?, ?)',
                     (firstname, lastname, email, password, identification_code, campus))
        conn.commit()
        conn.close()

        flash('Inscription réussie ! Vous pouvez maintenant vous connecter.')
        return redirect(url_for('login'))

    return render_template('register.html')  # Affiche la page d'inscription


# Logique pour le login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Connexion à la base de données
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password)).fetchone()
        conn.close()
        
        if user:
            # Stocker les informations de l'utilisateur dans la session, y compris s'il est admin
            session['user'] = {
                'firstname': user['firstname'], 
                'lastname': user['lastname'],
                'is_admin': bool(user['Admin'])  # Convertir l'Admin en booléen
            }
            return redirect(url_for('dashboard'))  # Rediriger vers le tableau de bord
        else:
            flash('Email ou mot de passe incorrect.')
            return redirect(url_for('login'))

    return render_template('login.html')  # Affiche la page de login



# Logique pour le dashboard 
@app.route('/dashboard')
def dashboard():
    # Vérification que l'utilisateur est connecté
    if 'user' not in session:
        return redirect(url_for('login'))

    # Connexion à la base de données
    conn = get_db_connection()
    
    # Récupération des activités depuis la base de données
    activities = conn.execute('SELECT * FROM activity').fetchall()
    print(activities)

    # Récupération de l'utilisateur connecté
    user = session['user']
    
    # Vérification si l'utilisateur est admin
    is_admin = user['is_admin']

    conn.close()

    # Envoie des informations de l'utilisateur et des activités au template
    return render_template('dashboard.html', user=user, activities=activities, is_admin=is_admin)

@app.route('/add_activity', methods=['POST'])
def add_activity():
    nom = request.form['title']
    type_activite = request.form['category']
    description = request.form['description']

    # Insérer l'activité dans la base de données SQLite
    conn = sqlite3.connect('CampusConnect.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO activity (nom, type, description) VALUES (?, ?, ?)", (nom, type_activite, description))
    conn.commit()
    conn.close()

    return redirect(url_for('dashboard'))  # Redirige vers le dashboard après ajout

@app.route('/dashboard/activity/<int:activity_id>', methods=['GET'])
def show_activity(activity_id):
    # Récupérer l'activité depuis la base de données
    conn = sqlite3.connect('CampusConnect.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM activity WHERE id = ?", (activity_id,))
    activity = cursor.fetchone()
    conn.close()

    if activity:
        # Convertir les informations de l'activité en JSON
        activity_data = {
            "id": activity[0],
            "nom": activity[1],
            "type": activity[2],
            "description": activity[3]
        }
        return jsonify(activity_data)  # Renvoyer les données en JSON
    else:
        return jsonify({"error": "Activity not found"}), 404




# Logique pour la déconnexion
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Déconnexion réussie.')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)