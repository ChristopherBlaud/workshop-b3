import sqlite3

# Fonction de connexion à la base de données SQLite
def get_db_connection():
    conn = sqlite3.connect('CampusConnect.db')
    conn.row_factory = sqlite3.Row
    return conn

# Ajout des codes d'identification dans la base de données
codes = ['CODE123', 'CODE456', 'CODE789']

# Connexion à la base de données
conn = get_db_connection()

# Ajout des codes d'identification à la table 'identification_codes'
for code in codes:
    conn.execute('INSERT INTO identification_codes (code) VALUES (?)', (code,))

# Sauvegarde des changements et fermeture de la connexion
conn.commit()
conn.close()
