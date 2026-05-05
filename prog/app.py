from flask import Flask, render_template
from config import USER_INFO

app = Flask(__name__, template_folder='..', static_folder='..')

@app.route('/')
def index():
    # C'est ici que la magie opère : on envoie tes infos au HTML
    return render_template('index.html', info=USER_INFO)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)