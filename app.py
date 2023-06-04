from flask import Flask, render_template, flash


app = Flask(__name__)


# mysql database ile connection qurmaq ucun;
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123@127.0.0.1:3306/project_end'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'project'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'


# Add administrative views here



from extensions import *
from controllers import *
from models import *

admin.add_view(ModelView(Products, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Contacts, db.session))
admin.add_view(ModelView(Categories, db.session))
admin.add_view(ModelView(Subcategory, db.session))
admin.add_view(ModelView(Reviews, db.session))





if __name__ == '__main__':
    app.init_app(db)
    app.init_app(migrate)
    
