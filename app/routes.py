from app import app,db
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Order
from app.forms import LoginForm, RegistrationForm
from flask import render_template, flash, redirect, request, url_for
from werkzeug.urls import url_parse
from werkzeug.datastructures import ImmutableMultiDict
from datetime import datetime
import sys

@app.route('/')

@app.route('/index')
@login_required
def index():
    isAdmin = current_user.username
    if isAdmin == 'admin':
        admin = {'username': isAdmin}
        return render_template('indexadmin.html', admin=admin)
    prevOrders = Order.query.filter_by(user_id=current_user.id).all()
    if prevOrders is None:
        prevOrders = 'No results'
    return render_template('index.html', prevOrders=prevOrders)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/buildpizza', methods=['GET', 'POST'])
def buildpizza():
    if request.method =='POST':
        pizzaorder = request.get_json()
        o_pepp = ''
        o_mush = ''
        o_green = ''
        o_sauce = ''
        o_crust = ''
        total = 10
        if 'pepperonni' in pizzaorder:
            o_pepp = pizzaorder['pepperonni']
            total = total + int(o_pepp)
        if 'mushrooms' in pizzaorder:
            o_mush = pizzaorder['mushrooms']
            total = total + int(o_mush)
        if 'greenpeppers' in pizzaorder:
            o_green = pizzaorder['greenpeppers']
            total = total + int(o_green)
        if 'sauce' in pizzaorder:
            o_sauce = pizzaorder['sauce']
            total = total + int(o_sauce)
        if 'crust' in pizzaorder:
            o_crust = pizzaorder['crust']
            total = total + int(o_crust)
        now = datetime.utcnow()
        order = Order(user_id=current_user.id, pepperonni=o_pepp, mushrooms=o_mush, peppers=o_green, sauce=o_sauce, crust=o_crust, ordertime=now, order_total=total)
        db.session.add(order)
        db.session.commit()

        print('order added successfully!', file=sys.stderr)
        return redirect(url_for('buildpizza'))
    return render_template('buildpizza.html', user=current_user)

@app.route('/viewallorders')
def viewallorders():
    prevOrders = Order.query.all()
    if prevOrders is None:
        prevOrders = {'Results': 'Nothing ordered yet'}
    return render_template('viewallorders.html', orders=prevOrders)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page=url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash ('Congratulations, you are now a Four Seniors Pizza Customer!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)
