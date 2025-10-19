from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(100),unique=True,nullable=False)
    password_hash=db.Column(db.String(200),nullable=False)
    role=db.Column(db.String(20),nullable=False) #admin,doctor,patient

    #relationships
    patient=db.relationship('Patient',backref='user',uselist=False)
    doctor=db.relationship('Doctor',backref='user',uselist=False)

    #password hashing
    def set_password(self,password):
        self.password_hash=generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    
class Patient(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    name= db.Column(db.String(100, nullable=False))
    age=db.Column(db.Integer)
    gender=db.Column(db.String(10))
    contact=db.Column(db.String(20))
    address=db.Column(db.String(200))

    appointments= db.relationship('Appointment', backref='patient',lazy=True)

class Doctor(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    name=db.Column(db.String(100),nullable=False)
    specialization=db.Column(db.String(100),nullable=False)
    contact=db.Column(db.String(20))
    availability=db.Column(db.String(200))
    department_id=db.Column(db.Integer,db.ForeignKey('department.id'))

    appointments=db.relationship('Appointment', backref='doctor',lazy=True)

class Department(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100),nullable=True)
    description=db.Column(db.Text)

    doctors=db.relationship('Doctor', backref='department', lazy=True)

class Appointment(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    patient_id=db.Column(db.Integer,db.ForeignKey('patient.id',nullable=True))
    doctor_id=db.Column(db.Integer,db.ForeignKey('doctor.id'),nullable=True)
    date=db.Column(db.Date, nullable=True)
    time=db.Column(db.Time, nullable=True)
    status=db.Column(db.String(20),default='Booked')

    treatment=db.relationship('Treatement',backref='appointment',uselight=False)

class Treatment(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    appointment_id=db.Column(db.Integer,db.ForeignKey('appointment.id'),nullable=False)
    diagnosis=db.Column(db.Text)
    prescription=db.Column(db.Text)
    notes=db.Column(db.Text)

    