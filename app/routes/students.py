from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models.student import Student, User
from app.models.attendance import Attendance
from app.models.grades import Grade
import uuid
from datetime import datetime

students_bp = Blueprint('students', __name__)

@students_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'student':
        flash('Access denied!', 'danger')
        return redirect(url_for('auth.login'))
    
    student = Student.query.filter_by(user_id=current_user.id).first()
    return render_template('students/dashboard.html', student=student)

@students_bp.route('/api/students', methods=['GET'])
@login_required
def get_students():
    if current_user.role not in ['admin', 'teacher']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    students = Student.query.all()
    return jsonify([student.to_dict() for student in students])

@students_bp.route('/api/students', methods=['POST'])
@login_required
def add_student():
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    # Generate student ID
    student_id = f"BNM{datetime.now().year}{str(uuid.uuid4().int)[:6]}"
    
    # Create user account
    user = User(
        username=data['username'],
        email=data['email'],
        role='student'
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.flush()  # Get user id
    
    # Create student record
    student = Student(
        student_id=student_id,
        user_id=user.id,
        first_name=data['first_name'],
        last_name=data['last_name'],
        date_of_birth=datetime.strptime(data['dob'], '%Y-%m-%d'),
        gender=data['gender'],
        grade=data['grade'],
        section=data['section'],
        admission_date=datetime.now().date(),
        parent_name=data.get('parent_name'),
        parent_phone=data.get('parent_phone'),
        parent_email=data.get('parent_email')
    )
    
    db.session.add(student)
    db.session.commit()
    
    return jsonify({'message': 'Student added successfully', 'student_id': student_id}), 201

@students_bp.route('/api/students/<student_id>/attendance')
@login_required
def get_student_attendance(student_id):
    if current_user.role != 'admin' and \
       (current_user.role == 'student' and not current_user.student.student_id == student_id):
        return jsonify({'error': 'Unauthorized'}), 403
    
    attendances = Attendance.query.filter_by(student_id=student_id).all()
    return jsonify([att.to_dict() for att in attendances])

@students_bp.route('/api/students/<student_id>/grades')
@login_required
def get_student_grades(student_id):
    if current_user.role != 'admin' and \
       (current_user.role == 'student' and not current_user.student.student_id == student_id):
        return jsonify({'error': 'Unauthorized'}), 403
    
    grades = Grade.query.filter_by(student_id=student_id).all()
    return jsonify([grade.to_dict() for grade in grades])
