from flask import render_template, url_for, flash, redirect, request
from app import app, db
from app.forms import RegistrationForm, LoginForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import SMTPSettingsForm
from app.models import SMTPSettings
from app.forms import EmailForm
from app.models import SentEmail
import smtplib

@app.route("/compose", methods=['GET', 'POST'])
@login_required
def compose():
    form = EmailForm()
    if form.validate_on_submit():
        settings = SMTPSettings.query.filter_by(owner=current_user).first()
        if not settings:
            flash('Please configure your SMTP settings first', 'warning')
            return redirect(url_for('smtp_config'))
        
        # Sending email logic
        try:
            with smtplib.SMTP(settings.smtp_server, settings.smtp_port) as server:
                server.login(settings.smtp_username, settings.smtp_password)
                message = f"Subject: {form.subject.data}\n\n{form.body.data}"
                server.sendmail(settings.smtp_username, form.recipient.data, message)
            
            sent_email = SentEmail(
                subject=form.subject.data,
                body=form.body.data,
                recipient=form.recipient.data,
                user_id=current_user.id
            )
            db.session.add(sent_email)
            db.session.commit()
            flash('Email sent successfully!', 'success')
            return redirect(url_for('sent_emails'))
        except Exception as e:
            flash(f'Failed to send email: {str(e)}', 'danger')
        
    return render_template('compose.html', title='Compose Email', form=form)

@app.route("/smtp_config", methods=['GET', 'POST'])
@login_required
def smtp_config():
    form = SMTPSettingsForm()
    if form.validate_on_submit():
        settings = SMTPSettings(
            smtp_server=form.smtp_server.data,
            smtp_port=form.smtp_port.data,
            smtp_username=form.smtp_username.data,
            smtp_password=form.smtp_password.data,
            owner=current_user
        )
        db.session.add(settings)
        db.session.commit()
        flash('SMTP settings have been saved!', 'success')
        return redirect(url_for('home'))
    return render_template('smtp_config.html', title='SMTP Configuration', form=form)

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/sent_emails")
@login_required
def sent_emails():
    emails = SentEmail.query.filter_by(user_id=current_user.id).all()
    return render_template('sent_emails.html', emails=emails)
