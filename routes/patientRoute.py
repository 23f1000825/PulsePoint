from flask import Blueprint, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from controllers.patientController import create_patient, get_patient_by_user_id, update_patient

patient_bp = Blueprint('patient', __name__)

# ------------------- Create Patient Profile -------------------
@patient_bp.route('/patient/create', methods=['POST'])
@login_required
def create_patient_profile():
    if current_user.role != 'patient':
        return jsonify({"error": "Unauthorized access"}), 403

    data = request.get_json() or request.form
    required_fields = ['name', 'age', 'gender', 'contact', 'address']

    # Missing fields check
    missing = [field for field in required_fields if not data.get(field)]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    result = create_patient(
        user_id=current_user.id,
        name=data.get('name'),
        age=data.get('age'),
        gender=data.get('gender'),
        contact=data.get('contact'),
        address=data.get('address')
    )

    if not result['success']:
        return jsonify({"error": result['message']}), 400

    # Success
    patient = result['patient']
    return jsonify({
        "message": "Patient profile created successfully!",
        "patient": {
            "id": patient.id,
            "name": patient.name,
            "age": patient.age,
            "gender": patient.gender,
            "contact": patient.contact,
            "address": patient.address
        }
    }), 201


# ------------------- Get Patient Dashboard -------------------
@patient_bp.route('/patient/dashboard', methods=['GET'])
@login_required
def dashboard():
    if current_user.role != 'patient':
        return jsonify({"error": "Unauthorized access"}), 403

    result = get_patient_by_user_id(current_user.id)
    if not result['success']:
        return jsonify({"error": result['message']}), 404

    patient = result['patient']
    return jsonify({
        "message": f"Welcome {patient.name}!",
        "patient": {
            "id": patient.id,
            "name": patient.name,
            "age": patient.age,
            "gender": patient.gender,
            "contact": patient.contact,
            "address": patient.address
        }
    }), 200


# ------------------- Update Patient Info -------------------
@patient_bp.route('/patient/update', methods=['PUT'])
@login_required
def update_patient_info():
    if current_user.role != 'patient':
        return jsonify({"error": "Unauthorized access"}), 403

    data = request.get_json() or request.form
    if not data:
        return jsonify({"error": "No data provided"}), 400

    result = update_patient(current_user.id, data)
    if not result['success']:
        return jsonify({"error": result['message']}), 400

    patient = result['patient']
    return jsonify({
        "message": "Profile updated successfully!",
        "patient": {
            "id": patient.id,
            "name": patient.name,
            "age": patient.age,
            "gender": patient.gender,
            "contact": patient.contact,
            "address": patient.address
        }
    }), 200