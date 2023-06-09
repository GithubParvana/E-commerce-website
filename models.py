from extensions import db, login_manager
from app import app
from flask_login import UserMixin, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from flask_security import RoleMixin
from sqlalchemy.schema import UniqueConstraint



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False, unique=True)
    password = db.Column(db.String(255), nullable = False)
    is_superuser = db.Column(db.Boolean, nullable=False)
    # roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users'), lazy='dynamic')


    def __init__(self, name, email, password, is_superuser=False):
        self.name = name
        self.email = email
        self.password = password
        self.is_superuser = is_superuser


    def check_password(self, password):
        return check_password_hash(self.password, password)


    def __repr__(self):
        return self.name


    def save(self):
        db.session.add(self)
        db.session.commit()

        



# class Role(db.Model, RoleMixin):
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(100), nullable = False)







# review form ucun

class Reviews(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    message = db.Column(db.String(255))
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='reviews')


    def __init__(self, message, product_id, user_id):
        self.message = message
        self.product_id = product_id
        self.user_id = user_id


    def __repr__(self):
        return self.message


    def save(self):
        db.session.add(self)
        db.session.commit()

    





class Categories(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable = False)
    category_ = db.relationship('Products', backref = 'categories')


    @classmethod
    def count_cat(cls):
        return cls.query.count()
    

    def __init__(self, name):
        self.name = name
        

    def __repr__(self):
        return self.name

    
    def save(self):
        db.session.add(self)
        db.session.commit()



class Subcategory(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable = False)
    subcategory_ = db.relationship('Products', backref = 'subcategory')
    

    def __init__(self, name): 
        self.name = name    


    def __repr__(self):
        return self.name

    
    def save(self):
        db.session.add(self)
        db.session.commit()





class Colors(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    color = db.Column(db.String(100), nullable = False)
    colors_ = db.relationship('Products', backref = 'colors')


    @classmethod
    def count_color(cls):
        return cls.query.count()


    def __init__(self, color):
        self.color = color


    def __repr__(self):
        return self.color


    def save(self):
        db.session.add(self)
        db.session.commit()





class Sizes(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    size = db.Column(db.String(100), nullable = False)
    sizes_ = db.relationship('Products', backref = 'sizes')


    @classmethod
    def count_size(cls):
        return cls.query.count()
    

    def __init__(self, size):
        self.size = size


    def __repr__(self):
        return self.size


    def save(self):
        db.session.add(self)
        db.session.commit()






class Favorite(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    products_id = db.Column(db.ForeignKey('products.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product = db.relationship('Products', backref=db.backref('favorite', lazy=True))
    __table_args__ = (UniqueConstraint(user_id, products_id), )


    @classmethod
    def count_fave(cls):
        return cls.query.count()
    

    def __init__(self, products_id, user_id):
        self.products_id = products_id,
        self.user_id = user_id
        


    def __repr__(self):
        return self.products_id


    def save(self):
        db.session.add(self)
        db.session.commit()
    




# class Remove(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     favorites_id = db.Column(db.ForeignKey('favorite.id'), nullable = True)
    

    
#     def __init__(self, favorites_id):
#         self.favorites_id = favorites_id
        

#     def __repr__(self):
#         return self.favorites_id


#     def save(self):
#         db.session.delete(self)
#         db.session.commit()




# roles_users = db.Table('roles_users',
#                        db.Column('user_id', db.Integer,
#                        db.ForeignKey('user.id')),
#                        db.Column('role_id', db.Integer,
#                        db.ForeignKey('roles.id'))
# )




class Products(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float())
    sale_price = db.Column(db.Float())
    img_url = db.Column(db.String(255), index=True)
    category_id = db.Column(db.Integer(), db.ForeignKey('categories.id'), nullable=False)
    sizes_id = db.Column(db.Integer(), db.ForeignKey('sizes.id'), nullable=False)
    colors_id = db.Column(db.Integer(), db.ForeignKey('colors.id'), nullable=False)
    subcategory_id = db.Column(db.Integer(), db.ForeignKey('subcategory.id'), nullable=False)
    



    def __init__(self, name, description, price, sale_price, img_url, category_id, sizes_id, colors_id, subcategory_id):
        self.name = name
        self.description = description
        self.price = price
        self.sale_price = sale_price
        self.img_url = img_url
        self.category_id = category_id
        self.sizes_id = sizes_id
        self.colors_id = colors_id
        self.subcategory_id = subcategory_id
        
        


    def __repr__(self):
        return self.name


    def save(self):
        db.session.add(self)
        db.session.commit()







# contacts query contact page ucun

class Contacts(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    subject = db.Column(db.String(100))
    message = db.Column(db.String(255))



    def __init__(self, name, email, subject, message):
        self.name = name
        self.email = email
        self.subject = subject
        self.message = message


    def __repr__(self):
        return self.name


    def save(self):
        db.session.add(self)
        db.session.commit()

    




class Newsletter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)


    def __init__(self, name, email):
        self.name = name
        self.email = email


    def __repr__(self):
        return self.name


    def save(self):
        db.session.add(self)
        db.session.commit()

