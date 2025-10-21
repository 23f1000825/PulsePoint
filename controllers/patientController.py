from models import db, Patient

def create_patient(user_id, name, age, gender, contact, address):
    """
    Create a new patient record linked to a user.
    """
    if not all([user_id, name, contact, address]):
        return {"success": False, "message": "Missing required fields"}

    # Check if already exists
    existing = Patient.query.filter_by(user_id=user_id).first()
    if existing:
        return {"success": False, "message": "Patient profile already exists"}

    # Age validation
    if age is not None:
        try:
            age = int(age)
            if age < 0 or age > 120:
                return {"success": False, "message": "Age must be between 0 and 120"}
        except ValueError:
            return {"success": False, "message": "Invalid age format"}

    # Gender validation
    if gender and gender.lower() not in ['male', 'female', 'other']:
        return {"success": False, "message": "Gender must be 'Male', 'Female', or 'Other'"}

    # Contact validation
    if not contact.isdigit() or len(contact) < 8 or len(contact) > 15:
        return {"success": False, "message": "Invalid contact number"}

    patient = Patient(
        user_id=user_id,
        name=name.strip(),
        age=age,
        gender=gender.strip().capitalize() if gender else None,
        contact=contact.strip(),
        address=address.strip()
    )

    db.session.add(patient)
    db.session.commit()

    return {"success": True, "patient": patient}


def get_patient_by_user_id(user_id):
    patient = Patient.query.filter_by(user_id=user_id).first()
    if not patient:
        return {"success": False, "message": "Patient not found"}
    return {"success": True, "patient": patient}


def update_patient(user_id, data):
    patient = Patient.query.filter_by(user_id=user_id).first()
    if not patient:
        return {"success": False, "message": "Patient not found"}

    name = data.get('name')
    age = data.get('age')
    gender = data.get('gender')
    contact = data.get('contact')
    address = data.get('address')

    # Field-wise validation
    if age:
        try:
            age = int(age)
            if age < 0 or age > 120:
                return {"success": False, "message": "Age must be between 0 and 120"}
        except ValueError:
            return {"success": False, "message": "Invalid age format"}

    if gender and gender.lower() not in ['male', 'female', 'other']:
        return {"success": False, "message": "Gender must be 'Male', 'Female', or 'Other'"}

    if contact:
        if not contact.isdigit() or len(contact) < 8 or len(contact) > 15:
            return {"success": False, "message": "Invalid contact number"}

    # Apply updates
    if name: patient.name = name.strip()
    if age: patient.age = age
    if gender: patient.gender = gender.strip().capitalize()
    if contact: patient.contact = contact.strip()
    if address: patient.address = address.strip()

    db.session.commit()
    return {"success": True, "patient": patient}