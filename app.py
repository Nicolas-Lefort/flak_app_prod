from models import db, Articles, Users
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import Flask
from config import config

CONFIG = 'dev'

app = Flask(__name__)

app.config['FLASK_ADMIN_SWATCH'] = 'united'
admin = Admin(app, name='Arnika', template_mode='bootstrap3')
admin.add_view(ModelView(Users, db.session))
admin.add_view(ModelView(Articles, db.session))

app.config.from_object(config.get(CONFIG or 'default'))

db.init_app(app)

from routes import *

if __name__ == "__main__":
    app.secret_key = "secret123"
    app.run(debug=True)


