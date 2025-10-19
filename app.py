import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Ensure the instance folder exists (for hospital.db)
os.makedirs("instance", exist_ok=True)

app = Flask(__name__)

# App configuration
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # 'admin', 'customer', or 'professional'
    approve = db.Column(db.Boolean, default=False)
    blocked = db.Column(db.Boolean, default=False)

@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, role='admin').first()
        if user and check_password_hash(user.password, password):
            session['adminuserid'] = user.id
            session['role'] = user.role
            flash('Admin login successful!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid Credentials', 'danger')
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter(User.username == username, User.role.in_(['customer', 'professional'])).first()
        if user and check_password_hash(user.password, password):
            session['userid'] = user.id
            session['role'] = user.role
            if user.role == 'customer':
                if not user.approve:
                    flash('Your account is not approved yet! Please wait for the admin to approve.', 'danger')
                    return redirect(url_for('login'))
                if user.blocked:
                    flash('Your account is blocked! Please contact the admin.', 'danger')
                    return redirect(url_for('login'))
                flash('Patient login successful!', 'success')
                return redirect(url_for('dashboard'))
            elif user.role == 'professional':
                if not user.approve:
                    flash('Your account is not approved yet! Please wait for the admin to approve.', 'danger')
                    return redirect(url_for('login'))
                if user.blocked:
                    flash('Your account is blocked! Please contact the admin.', 'danger')
                    return redirect(url_for('login'))
                flash('Doctor login successful!', 'success')
                return redirect(url_for('dashboard'))
        flash('Invalid Credentials', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']  # admin, customer, professional
        # For testing, set approve=True for admin and doctor to make login easier
        approve = True if role == 'admin' or role == 'professional' else False
        hashed_password = generate_password_hash(password)
        user = User(username=username, password=hashed_password, role=role, approve=approve)
        db.session.add(user)
        db.session.commit()
        flash(f'Registered {role} successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensures tables are created
    app.run(debug=True)

