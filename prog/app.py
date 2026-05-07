from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import mimetypes

mimetypes.add_type('text/css', '.css')

app = Flask(__name__, template_folder='..', static_folder='..', static_url_path='')

# Configuration de la connexion (User:Password@Host/DBname)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://mael:password_mael@db/portfolio_db'
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
    # On récupère toutes les compétences en base de données
    mes_competences = Competence.query.all()
    return render_template('index.html', competences=mes_competences)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)