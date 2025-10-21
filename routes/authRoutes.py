from flask import Blueprint, request, jsonify, redirect, url_for, render_template, flash
from controllers.authController import register_user, authenticate_user
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json() or request.form
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not all([email, password, role]):
        return jsonify({"error": "Missing required fields"}), 400

    user = register_user(email, password, role)
    if not user:
        return jsonify({"error": "Registration failed"}), 400

    return jsonify({"message:" , " User registered successfully!"}), 201


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json() or request.form
    email = data.get('email')
    password = data.get('password')

    user = authenticate_user(email, password)
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    login_user(user)
    return jsonify({"message": "Login successful!", "user": {"email": user.email, "role": user.role}}), 200


@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully!"}), 200
