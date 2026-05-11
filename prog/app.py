from flask import Flask, render_template, request, redirect, url_for, session
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import mimetypes
import os

mimetypes.add_type('text/css', '.css')

app = Flask(__name__, template_folder='..', static_folder='..', static_url_path='')
app.secret_key = os.environ.get('SECRET_KEY', 'LeclercAzure_changeme_en_prod')

# --- CONFIGURATION DU PROFIL ---
app.config['USER_PROFILE'] = {
    'nom': 'Maël Massin',
    'titre': 'Étudiant en BUT R&T',
    'etablissement': 'IUT de Béthune',
    'description': 'Passionné par les technologies réseaux et le développement.'
}

# Configuration BDD
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'mysql://mael:password_mael@db_final/portfolio_db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- MODÈLES ---

class Semestre(db.Model):
    __tablename__ = 'semestres'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50))
    code = db.Column(db.String(10))
    blocs = db.relationship('Bloc', backref='semestre')

class Bloc(db.Model):
    __tablename__ = 'blocs'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    code = db.Column(db.String(20))
    semestre_id = db.Column(db.Integer, db.ForeignKey('semestres.id'))
    competences = db.relationship('Competence', backref='bloc')

class Competence(db.Model):
    __tablename__ = 'competences'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20))
    nom = db.Column(db.String(255))
    fait = db.Column(db.Text)
    pourquoi = db.Column(db.Text)
    comment = db.Column(db.Text)
    difficultes = db.Column(db.Text)
    appris = db.Column(db.Text)
    autrement = db.Column(db.Text)
    niveau = db.Column(db.String(50))
    bloc_id = db.Column(db.Integer, db.ForeignKey('blocs.id'))

# Niveaux autorisés (évite les injections via le champ niveau)
NIVEAUX_VALIDES = ['non acquis', 'en cours d\'acquisition', 'presque acquis', 'acquis', 'expert']

# --- ROUTES ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        # On récupère les données du formulaire
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Test simple (à améliorer plus tard si besoin)
        if username == 'admin' and password == 'LeclercAzure':
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            error = 'Identifiants invalides. Veuillez réessayer.'
            
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/')
def index():
    mon_profil = app.config.get('USER_PROFILE')
    mes_competences = Competence.query.all()
    mes_blocs = Bloc.query.all()          # ← C'était le bug : blocs manquait
    mes_semestres = Semestre.query.all()
    return render_template(
        'index.html',
        profile=mon_profil,
        competences=mes_competences,
        blocs=mes_blocs,
        semestres=mes_semestres
    )

@app.route('/add', methods=['POST'])
def add_competence():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    nom    = request.form.get('nom_competence', '').strip()
    niveau = request.form.get('niveau_competence', '').strip().lower()
    bloc_id = request.form.get('bloc_id', '').strip()

    # Validation des entrées
    if not nom or not niveau or not bloc_id:
        return redirect(url_for('index'))

    if niveau not in NIVEAUX_VALIDES:
        return "Niveau invalide", 400

    try:
        bloc_id_int = int(bloc_id)
    except ValueError:
        return "Bloc invalide", 400

    # SQLAlchemy utilise des requêtes paramétrées → protection injection SQL native
    nouvelle_comp = Competence(
        nom=nom,
        niveau=niveau,
        bloc_id=bloc_id_int,
        code="AC-NOUVEAU"
    )
    db.session.add(nouvelle_comp)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_competence(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    comp = Competence.query.get_or_404(id)
    db.session.delete(comp)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/competence/<int:id>')
def details_competence(id):
    comp = Competence.query.get_or_404(id)
    return render_template('details_ac.html', ac=comp, profile=app.config.get('USER_PROFILE'))

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)  # debug=False en prod