from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import mimetypes
import os

mimetypes.add_type('text/css', '.css')

app = Flask(__name__, template_folder='..', static_folder='..', static_url_path='')
app.secret_key = 'LeclercAzure'

# --- CONFIGURATION DU PROFIL (La clé manquante était ici !) ---
app.config['USER_PROFILE'] = {
    'nom': 'Maël Massin',
    'titre': 'Étudiant en BUT R&T',
    'etablissement': 'IUT de Béthune',
    'description': 'Passionné par les technologies réseaux et le développement.'
}

# Configuration BDD
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'mysql://mael:password_mael@db/portfolio_db')
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

# --- ROUTES ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'LeclercAzure':
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return "Identifiants incorrects", 401
            
    # Un petit formulaire propre pour le login
    return '''
        <body style="background:#1a1a1a; color:white; font-family:sans-serif; display:flex; justify-content:center; align-items:center; height:100vh;">
            <form method="post" style="background:#2a2a2a; padding:20px; border-radius:10px; box-shadow: 0 4px 15px rgba(0,0,0,0.5);">
                <h2 style="margin-top:0;">Connexion Admin</h2>
                <input type="text" name="username" placeholder="Utilisateur" style="display:block; width:100%; margin-bottom:10px; padding:10px; border-radius:5px; border:none;">
                <input type="password" name="password" placeholder="Mot de passe" style="display:block; width:100%; margin-bottom:20px; padding:10px; border-radius:5px; border:none;">
                <button type="submit" style="width:100%; padding:10px; border-radius:5px; border:none; background:#ff4d4d; color:white; cursor:pointer;">Se connecter</button>
            </form>
        </body>
    '''

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/')
def index():
    mon_profil = app.config.get('USER_PROFILE')
    mes_competences = Competence.query.all()
    mes_semestres = Semestre.query.all()
    return render_template('index.html', profile=mon_profil, competences=mes_competences, semestres=mes_semestres)

@app.route('/add', methods=['POST'])
def add_competence():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    nom = request.form.get('nom_competence')
    niveau = request.form.get('niveau_competence')
    if nom and niveau:
        nouvelle_comp = Competence(nom=nom, niveau=niveau)
        db.session.add(nouvelle_comp)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_competence(id):
    # SÉCURITÉ : On vérifie si on est connecté avant de supprimer
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    comp_a_supprimer = Competence.query.get_or_404(id)
    db.session.delete(comp_a_supprimer)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/competence/<int:id>')
def details_competence(id):
    comp = Competence.query.get_or_404(id)
    # On renvoie aussi le profil pour le header de la page de détails
    return render_template('details_ac.html', ac=comp, profile=app.config.get('USER_PROFILE'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)