from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import mimetypes
import os

mimetypes.add_type('text/css', '.css')

app = Flask(__name__, template_folder='..', static_folder='..', static_url_path='')

# Configuration via variable d'environnement (Docker)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'mysql://mael:password_mael@db/portfolio_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modèle pour les compétences
class Competence(db.Model):
    __tablename__ = 'competences'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    niveau = db.Column(db.Integer)

# --- ROUTES ---

@app.route('/')
def index():
    try:
        # Correction : on utilise la même variable partout (mes_competences)
        mes_competences = Competence.query.all()
    except Exception as e:
        print(f"Erreur BDD : {e}")
        mes_competences = []
    
    return render_template('index.html', competences=mes_competences)

@app.route('/add', methods=['POST'])
def add_competence():
    nom = request.form.get('nom_competence')
    niveau = request.form.get('niveau_competence')

    if nom and niveau:
        nouvelle_comp = Competence(nom=nom, niveau=int(niveau))
        db.session.add(nouvelle_comp)
        db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_competence(id):
    comp_a_supprimer = Competence.query.get_or_404(id)
    db.session.delete(comp_a_supprimer)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)