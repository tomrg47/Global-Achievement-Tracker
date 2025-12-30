from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app import db
from steam_openid import SteamOpenID
import os
import requests

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

@auth_bp.route("/login/steam")
def steam_login():
    realm = request.url_root
    return_to = url_for("auth.steam_callback", _external=True)
    steam = SteamOpenID(realm, return_to)
    return redirect(steam.get_redirect_url())

@auth_bp.route("/login/steam/callback")
def steam_callback():
    realm = request.url_root
    return_to = url_for("auth.steam_callback", _external=True)
    steam = SteamOpenID(realm, return_to)
    steam_id = steam.validate_results(request.args)
    
    if not steam_id:
        flash("Steam login failed", "error")
        return redirect(url_for("auth.login"))
        
    user = User.query.filter_by(steam_id=steam_id).first()
    
    if user:
        login_user(user)
        flash(f"Welcome back, {user.username}!", "success")
        return redirect(url_for("home.home"))
    
    # New user - fetch details and redirect to complete profile
    username = f"Steam_{steam_id}"
    api_key = os.getenv("STEAM_API_KEY")
    if api_key:
        try:
            response = requests.get(f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={steam_id}")
            data = response.json()
            players = data.get("response", {}).get("players", [])
            if players:
                username = players[0].get("personaname", username)
        except Exception as e:
            print(f"Failed to fetch Steam profile: {e}")
            
    session['steam_id'] = steam_id
    session['steam_username'] = username
    return redirect(url_for("auth.complete_profile"))

@auth_bp.route("/complete-profile", methods=["GET", "POST"])
def complete_profile():
    steam_id = session.get('steam_id')
    if not steam_id:
        return redirect(url_for("auth.login"))
        
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        
        if password and password != confirm_password:
            flash("Passwords do not match", "error")
            return render_template("complete_profile.html", username=username)
            
        if User.query.filter_by(username=username).first():
            flash("Username already exists", "error")
            return render_template("complete_profile.html", username=username)
            
        if email and User.query.filter_by(email=email).first():
            flash("Email already exists", "error")
            return render_template("complete_profile.html", username=username)
            
        new_user = User(username=username, email=email, steam_id=steam_id)
        if password:
            new_user.set_password(password)
            
        db.session.add(new_user)
        db.session.commit()
        
        session.pop('steam_id', None)
        session.pop('steam_username', None)
        
        login_user(new_user)
        flash(f"Account created! Welcome, {username}", "success")
        return redirect(url_for("home.home"))
        
    return render_template("complete_profile.html", username=session.get('steam_username'))

@auth_bp.route("/account")
@login_required
def account():
    return render_template("account.html")