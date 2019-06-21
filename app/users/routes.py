from bcrypt import checkpw, gensalt, hashpw
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app import db
from app import logger
from app.models import User
from app.users import blueprint
from app.users.forms import (LoginForm,
                             RegistrationForm,
                             RequestResetForm,
                             ResetPasswordForm,
                             UpdateAccountForm)
from app.users.utils import send_reset_email


@blueprint.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home_blueprint.home'))
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = hashpw(password.encode('utf8'), gensalt())
        user = User(username=username, email=email, password=hashed_password)

        if User.is_user_name_taken(username):
            flash('Username is already in use.', 'danger')
            return render_template('register.html',
                                   title='Register',
                                   form=form)
        if User.is_email_taken(email):
            flash('Email is already in use.', 'danger')
            return render_template('register.html',
                                   title='Register',
                                   form=form)

        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            logger.debug("ERROR: Adding user {}.".format(user))
            logger.debug("ERROR {}.".format(e))
        else:
            flash('Your account has been created!', 'success')
            logger.debug("Created user {} in Database.".format(user))
            return redirect(url_for('users_blueprint.login'))

    return render_template('register.html', title='Register', form=form)


@blueprint.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home_blueprint.home'))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and checkpw(password.encode('utf8'), user.password):
            login_user(user)
            logger.debug("Logging in {}.".format(user))
            return redirect(url_for('home_blueprint.home'))
        else:
            return render_template('403.html')
    return render_template('login.html', title='Login', form=form)


@blueprint.route("/logout", methods=['GET', 'POST'])
def logout():
    logger.debug("Logging out {}.".format(current_user))
    logout_user()
    return redirect(url_for('users_blueprint.login'))


@blueprint.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.company = form.company.data

        try:
            db.session.commit()
        except Exception as e:
            logger.debug("Error: {} Account Info Update ".format(current_user))
            logger.debug("ERROR {}.".format(e))
        else:
            flash('Your account has been updated!', 'success')
            logger.debug("Updated account: {}.".format(current_user))
            return redirect(url_for('users_blueprint.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.company.data = current_user.company
    return render_template('account.html', form=form)


@blueprint.route("/reset_request", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home_blueprint.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Email sent with instructions to reset your password.', 'info')
        return redirect(url_for('users_blueprint.login'))
    return render_template('reset_request.html', form=form)


@blueprint.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home_blueprint.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token!', 'warning')
        return redirect(url_for('users_blueprint.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        password = request.form['password']
        hashed_password = hashpw(password.encode('utf8'), gensalt())
        user.password = hashed_password

        try:
            db.session.commit()
        except Exception as e:
            logger.debug("Attempted to update password for {}.".format(user))
            logger.debug("ERROR {}.".format(e))
        else:
            flash('Your password has been updated!', 'success')
            logger.debug("Updated password for user {}.".format(user))
            return redirect(url_for('users_blueprint.login'))

    return render_template('reset_token.html',
                           title='Reset Password',
                           form=form)
