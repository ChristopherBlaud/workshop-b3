from app import app, db, IdentificationCode

# Créer la base de données et les tables
with app.app_context():
    db.create_all()

    # Ajouter des codes d'identification
    codes = ['CODE123', '456', 'CODE789']  # Remplace par tes propres codes
    for code in codes:
        new_code = IdentificationCode(code=code)
        db.session.add(new_code)

    db.session.commit()
    print("Codes d'identification ajoutés avec succès !")