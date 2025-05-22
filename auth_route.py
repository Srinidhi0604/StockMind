from flask import Flask,Blueprint, render_template, redirect, url_for, request, session
from database_model import db
from database_model import User
import authenticator

auth_bp = Blueprint('auth', __name__, url_prefix='/account')

# Authentication Routes
@auth_bp.route("/login", methods = ['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    if(not email or not password):
        return render_template("access-account.html", error = "Invalid Information, Please try again")
    user = User.query.filter_by(email = email).first()
    if(user and user.check_password(password)):
        username = user.username
        session["username"] = username
        return redirect(url_for("home"))
    else:
        return render_template("access-account.html", error = "Invalid Information")
        
@auth_bp.route("/register", methods = ['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    if(not username or not email or not password):
        return render_template("access-account.html", error = "Invalid Information, Please try again")
    user = User.query.filter_by(email = email).first()
    if user:
        return render_template("access-account.html", error="Account Already Exist")
    else:
        new_user = User(username = username, email = email)
        new_user.set_passsword(password)
        session['username'] = username
        session['password'] = new_user.get_passw_hash()
        session['email'] = email
        return redirect(url_for('auth.authenticate'))
    
@auth_bp.route('/api/authenticate')
def authenticate():
    username = session['username']
    email = session['email']
    try:
        otp =  authenticator.generateOTP(username=username, usermail=email)
        session["otp"] = otp
    except:
        return render_template("access-account.html", error = "Invalid email address")
    return render_template("access-account.html", otp = True)

@auth_bp.route('/api/verify', methods = ['POST'])
def verify():
    inp = request.form['userOTP']
    username = session["username"]
    password= session["password"]
    email = session["email"]
    otp = session["otp"]
    session.pop("password",None)
    session.pop("email",None)
    session.pop("otp",None)
    authSuccess = authenticator.verifyOTP(otp, inp)
    if(authSuccess):
        newUser = User(username = username , email = email, password_hash = password)
        #registering the user in database
        db.session.add(newUser)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        session.pop("username",None)
        return render_template("FRONT.html", error = "❌ Invalid OTP")
    
@auth_bp.route('/logout')
def logout():
    session.pop("username", None)
    return redirect(url_for('home'))

@auth_bp.route('/access-account')
def accessAccount():
    return render_template("access-account.html")
