from flask import render_template, request, redirect, url_for, flash
from app import app
from forms import *
from models import *
from werkzeug.security import generate_password_hash
from flask_login import login_user, login_required, logout_user ,current_user



@app.route('/base')
def base_page():
    categories_ = Categories.query.all()
    
    return render_template('base.html', categories_ = categories_)




@app.route('/product', methods=['GET', 'POST'])  # mehsul sehifesi;
@login_required
def product_page():
    products = Products.query.all()
    pro = Products.query.all()
    cat = Categories.query.all()
    name = request.args.get('name')
    print(name)
    
    if name:
        products = Products.query.filter(Products.name.contains(name)).all()
        print(products)
    return render_template('shop.html', pro = pro, cat = cat, products=products)




@app.route('/detail/<int:id>', methods=['GET', 'POST'])
def product_detail(id):
    print(id)
    h = Products.query.all()
    p = Products.query.first()
    colors = Colors.query.all()
    size = Sizes.query.all()
    p_string = Products.query.filter_by(id=id).first()
    form = ReviewForm(formdata=None)
    print('form post olundu')
    if request.method == 'POST':
        form = ReviewForm(request.form)
        print(request.form)
        if form.validate_on_submit():
            print('validate olunub')
            review = Reviews(
                message = form.message.data,
                product_id = id,
                user_id = current_user.id
            )
            review.save()
        form = ReviewForm(formdata=None)    
    reviews=Reviews.query.filter_by(product_id=id).all()
    products = Products.query.filter_by(id=id).first()
    return render_template('detail.html', p = p, h=h, colors = colors, size = size, p_string = p_string, products=products, form=form, reviews=reviews)




@app.route('/favorite')
def fav():
    return render_template('favorites.html')



@app.route('/contact', methods=['GET', 'POST'])
def contact_page():
    form = ContactsForm()
    print('post!!!!!!!!')
    print(request.form)
    if request.method == 'POST':
        print('sent')
        form = ContactsForm(request.form)
        print(request.form)
        if form.validate_on_submit():
            print('valid')
            contacts = Contacts(
                name = form.name.data, 
                email = form.email.data, 
                subject = form.subject.data, 
                message = form.message.data
                )
            contacts.save()
        return redirect(url_for('product_page'))
    return render_template('contact.html', form = form)






@app.route('/logout')
def logout():
    logout_user()
    return redirect('login_page')





@app.route('/register', methods = ['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.form)
        if form.validate_on_submit():
            user = User(
                name = form.name.data,
                email = form.email.data,
                password = generate_password_hash(form.password.data)
            )
            user.save()
        return redirect(url_for('login_page'))
    return render_template('register.html', form = form)




@app.route('/login', methods=['GET', 'POST'])
def login_page():
    error = None
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.form)
        print('valid')
        user = User.query.filter_by(email = form.email.data).first()
        print(user)
        if user and user.check_password(form.password.data):
            login_user(user)
            print('User logged in successfully!')
            flash('User logged in successfully!')
            return redirect(url_for('product_page'))
        else:
            flash("User didn't login. Failed :( ")
            return redirect(url_for('login_page')), "Maybe you don't have any account. Dou you want to register?"
    return render_template('login.html', form = form, error = error)







