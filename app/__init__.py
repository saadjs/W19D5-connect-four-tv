import os
from flask import Flask, render_template, request, session
from flask_cors import CORS
from flask_migrate import Migrate
#from flask_wtf.csrf import CSRFProtect, generate_csrf

from .models import db
from .api.game_routes import game_routes

from .config import Config
from dotenv import load_dotenv
load_dotenv()
print(os.environ.get('DATABASE_URL'))

app = Flask(__name__)

app.config.from_object(Config)
app.register_blueprint(game_routes, url_prefix='/api/games')
db.init_app(app)
Migrate(app, db)

# Application Security
CORS(app)


'''@app.after_request
def inject_csrf_token(response):
    response.set_cookie('csrf_token',
                        generate_csrf(),
                        secure=True if os.environ.get(
                            'FLASK_ENV') == 'production' else False,
                        samesite='Strict' if os.environ.get(
                            'FLASK_ENV') == 'production' else None,
                        httponly=True)
    return response'''


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def react_root(path):
    print("path", path)
    if path == 'favicon.ico':
        return app.send_static_file('favicon.ico')
    return app.send_static_file('index.html')
