from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import mysql
import time
from decimal import Decimal



main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")


@main.route("/dashboard")
def dashboard():
    # Select data from user_profile and user_activity that match user_id
    cursor = mysql.connection.cursor()

    id = str(session['user_id'])

    cursor.execute("SELECT * FROM user_profile WHERE user_id=%s", (id))
    profile_response = cursor.fetchone()
    profile_id, p_user_id, first_name, last_name, bio, avatar_url = profile_response

    profile_data = {
        "firstname" : first_name,
        "lastname" : last_name
    }

    cursor.execute("SELECT * FROM user_activity WHERE user_id=%s", (id))
    activity_response = cursor.fetchall()

    account_totals = {
        'checking': 0,
        'savings': 0,
    }
    activity_data = []
    
    balance = Decimal('0.00')
    balance_data = []
    for response in activity_response:
        activity_id, a_user_id, amount, details, transaction_type, date_created, account = response
        activity_data.append({
            'amount': amount,
            'details': details,
            'type': transaction_type,
            'date_created': date_created,
            'account': account
        })

        if account.lower() == 'checking':
            account_totals['checking'] = account_totals['checking'] + amount
        elif account.lower() == 'savings':
            account_totals['savings'] = account_totals['savings'] + amount

        balance += Decimal(amount)
        balance_data.append({
            'day': date_created.strftime('%Y-%m-%d'),
            'balance': float(balance)
        })

    activity_data.reverse()
    
    return render_template("dashboard.html", profile_data=profile_data, activity_data=activity_data, totals=account_totals, balance_data=balance_data)


@main.route("/not_found")
def not_found():
    return render_template("404_not_found.html")



auth = Blueprint("auth", __name__)

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
            flash("User already exists. Please login.", "duplicate")

    return render_template("signup.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        cursor = mysql.connection.cursor()

        try:
            cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
            user = cursor.fetchone()
            if user:
                flash("User authenticated successfully", "success")
                session['user_id'] = user[0]
                session['username'] = user[1]
                return redirect(url_for("main.dashboard"))
            else:
                flash("Username or password invalid", "failed")
        except Exception as e:
                flash(f"Authentication Error: {e}", "error")
        finally:
            cursor.close()
            
    return render_template("login.html")


@auth.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    flash("You have been logged out", "info")
    return redirect(url_for("main.index"))
