from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home.home"))
    return render_template("login.html")

@auth_bp.route("/signup", methods=["GET"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("home.home"))
    return render_template("signup.html")


@auth_bp.route("/api/auth/signup", methods=["POST"])
def api_signup():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    
    if password != confirm_password:
        flash("Passwords do not match", "error")
        return redirect(url_for("auth.signup"))
    
    user = User.query.filter_by(username=username).first()
    if user:
        flash("Username already exists", "error")
        return redirect(url_for("auth.signup"))
        
    email_user = User.query.filter_by(email=email).first()
    if email_user:
        flash("Email already exists", "error")
        return redirect(url_for("auth.signup"))
        
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    
    db.session.add(new_user)
    db.session.commit()
    
    login_user(new_user)
        
    flash(f"Account created! Welcome, {username}", "success")
    return redirect(url_for("home.home"))

@auth_bp.route("/api/auth/login", methods=["POST"])
def api_login():
    username = request.form.get("username")
    password = request.form.get("password")
    
    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        login_user(user)
        flash(f"Welcome back, {username}!", "success")
        return redirect(url_for("home.home"))
    else:
        flash("Invalid username or password", "error")
        return redirect(url_for("auth.login"))

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))

@auth_bp.route("/account")
@login_required
def account():
    return render_template("account.html")