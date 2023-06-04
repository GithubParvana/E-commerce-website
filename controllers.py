from flask import render_template, request, redirect, url_for, flash
from app import app
from forms import *
from models import *
from werkzeug.security import generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user



@app.route('/base')
def base_page():
    return render_template('base.html')




@app.route('/product', methods=['GET', 'POST'])  # mehsul sehifesi;
@login_required
def product_page():
    favorites_count = Favorite.query.filter_by(
        user_id=current_user.id).count()
    products = Products.query.all()
    cat = Categories.query.all()
    subcategories = Subcategory.query.all()
    sizes = Sizes.query.all()
    colors = Colors.query.all()
    category = request.args.get('category')
    color = request.args.get('color')
    size = request.args.get('size')
    sub_category = request.args.get('sub_category')
    min_price = request.args.get('min')
    max_price = request.args.get('max')
    
    product_count = Colors.count_color()
    product_count = Sizes.count_size()
    product_count = Categories.count_cat()
    
    name = request.args.get('name')
    # print(name)
    
    if name:
        products = Products.query.filter(Products.name.ilike(f'%{name}%')).all()
        # products = Products.query.filter(Products.name.contains(name)).all()
        # print(products)
    if category:
        products = Categories.query.filter_by(id=category).first().category_
        # print(products)
    if sub_category:
        products = Subcategory.query.filter_by(id=sub_category).first().subcategory_
    if color:
        products = Colors.query.filter_by(id=color).first().colors_
    if size:
        products = Sizes.query.filter_by(id=size).first().sizes_
    if min_price and max_price:
        products = Products.query.filter(Products.price.between(min_price, max_price)).all()
        

    form = NewsletterForm()
    # print(request.form)
    if request.method == 'POST':
        form = NewsletterForm(request.form)
        # print(request.form)
        if form.validate_on_submit():
            newsletter = Newsletter(
                name = form.name.data, 
                email = form.email.data
            )
            newsletter.save()
        redirect(url_for('product_page'))
    return render_template('shop.html', cat = cat, products=products, subcategories = subcategories, form=form, sizes=sizes, colors=colors, product_count=product_count, favorites_count=favorites_count)





# @app.route('/search')
# def search_page():
#     query = request.args.get('name')
#     product = Products.query.filter(Products.name.ilike(f'%{query}%')).all()
#     return render_template('search.html', query=query, product=product)






@app.route('/detail/<int:id>', methods=['GET', 'POST'])
def product_detail(id):
    print(id)
    product=Products.query.all()
    favorites_count = Favorite.query.filter_by(
        user_id=current_user.id).count()
    
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
    return render_template('detail.html', p = p, colors = colors, size = size, p_string = p_string, products=products, form=form, reviews=reviews, favorites_count= favorites_count)





# add favorites from detail page
@app.route('/add_favs/<int:products_id>', methods=['POST', 'GET'])
def add_favorite(products_id):
    product = Products.query.get_or_404(products_id)
    print(product)
    favorite = Favorite(
        products_id=products_id,
        user_id=current_user.id
    )
    if Favorite.query.filter_by(products_id=products_id, user_id=current_user.id).first() is not None:
        flash('Already added, thank you :) ')
    else:
        db.session.add(favorite)
        db.session.commit()   
    
    # redirect('favorites')
    return favorites()
    





# favorites count ucun;
@app.route('/favorites', methods=['GET'])
def favorites():
    favorites_count = Favorite.query.filter_by(user_id=current_user.id).count()
    favorites = Favorite.query.filter_by(user_id=current_user.id).all()
    
    return render_template('favorites.html', favorites=favorites, fav_count=favorites_count)




# favorites silmek ucun id'ye gore;
# products PATH'da daxil etdiyimiz id ile getsin products sehifeye ve o id'li mehsulu sil; 
@app.route('/products/<int:id>', methods=['GET', 'POST'])  # GET ile URL'den ala bilerik id'leri
def delete_product(id):
    
    fav = Favorite.query.filter_by(products_id=id,
                                 user_id=current_user.id).first()

    if fav:
        db.session.delete(fav)
        db.session.commit()
        return favorites()
    return render_template('favorites.html')






# contact
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




# logout

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')





# register

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






# login
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
            # print('User logged in successfully!')
            flash('User logged in successfully!')
            return redirect(url_for('product_page'))
        else:
            flash("User didn't login. Failed :( ")
            return redirect(url_for('login_page')), "Maybe you don't have any account. Dou you want to register?"
    return render_template('login.html', form = form, error = error)



