from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import mimetypes
import os

mimetypes.add_type('text/css', '.css')

app = Flask(__name__, template_folder='..', static_folder='..', static_url_path='')

# On utilise la variable d'environnement fournie par Docker Compose
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'mysql://mael:password_mael@db/portfolio_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modèle pour les compétences
class Competence(db.Model):
    __tablename__ = 'competences'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    niveau = db.Column(db.Integer)

@app.route('/')
def index():
    try:
        mes_competences = Competence.query.all()
    except:
        mes_competences = [] # Évite l'erreur si la base n'est pas prête
    return render_template('index.html', competences=mes_competences)

# N'oublie pas d'ajouter les routes ADD et DELETE ici pour la séance 3 !

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)