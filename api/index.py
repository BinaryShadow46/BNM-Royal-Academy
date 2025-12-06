import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, jsonify, request
import mysql.connector.pooling
import json

# Initialize Flask app
app = Flask(__name__)

# Database connection pool
db_pool = None

def init_db_pool():
    """Initialize database connection pool"""
    global db_pool
    
    if os.environ.get('VERCEL'):
        # Vercel environment - Use environment variables
        db_config = {
            'host': os.environ.get('MYSQL_HOST', 'localhost'),
            'user': os.environ.get('MYSQL_USER', 'root'),
            'password': os.environ.get('MYSQL_PASSWORD', ''),
            'database': os.environ.get('MYSQL_DATABASE', 'bnm_royal_academy'),
            'port': int(os.environ.get('MYSQL_PORT', 3306)),
            'pool_name': 'bnm_pool',
            'pool_size': 5
        }
    else:
        # Local development
        db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'password',
            'database': 'bnm_royal_academy',
            'pool_name': 'bnm_pool',
            'pool_size': 5
        }
    
    try:
        db_pool = mysql.connector.pooling.MySQLConnectionPool(**db_config)
        print("Database pool initialized successfully")
        return True
    except Exception as e:
        print(f"Database pool initialization failed: {e}")
        return False

# Initialize database pool on startup
init_db_pool()

@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        "message": "Welcome to BNM Royal Academy School Management System",
        "status": "online",
        "version": "1.0.0",
        "endpoints": [
            "/api/health",
            "/api/students",
            "/api/teachers",
            "/api/courses"
        ]
    })

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    try:
        if db_pool:
            conn = db_pool.get_connection()
            conn.close()
            db_status = "connected"
        else:
            db_status = "disconnected"
        
        return jsonify({
            "status": "healthy",
            "database": db_status,
            "timestamp": os.environ.get('VERCEL', 'local')
        })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500

@app.route('/api/students', methods=['GET'])
def get_students():
    """Get all students"""
    try:
        if not db_pool:
            init_db_pool()
        
        conn = db_pool.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Create students table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id VARCHAR(20) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                grade VARCHAR(10),
                section VARCHAR(10),
                email VARCHAR(100),
                phone VARCHAR(15),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insert sample data if table is empty
        cursor.execute("SELECT COUNT(*) as count FROM students")
        result = cursor.fetchone()
        
        if result['count'] == 0:
            sample_students = [
                ('BNM2024001', 'Rohan Sharma', '10', 'A', 'rohan@bnm.edu', '9876543210'),
                ('BNM2024002', 'Priya Patel', '10', 'B', 'priya@bnm.edu', '9876543211'),
                ('BNM2024003', 'Amit Kumar', '9', 'A', 'amit@bnm.edu', '9876543212')
            ]
            
            cursor.executemany('''
                INSERT INTO students (id, name, grade, section, email, phone)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', sample_students)
            conn.commit()
        
        # Fetch all students
        cursor.execute("SELECT * FROM students ORDER BY id")
        students = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            "success": True,
            "count": len(students),
            "students": students
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/students', methods=['POST'])
def add_student():
    """Add a new student"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        required_fields = ['id', 'name', 'grade']
        for field in required_fields:
            if field not in data:
                return jsonify({"success": False, "error": f"Missing required field: {field}"}), 400
        
        if not db_pool:
            init_db_pool()
        
        conn = db_pool.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO students (id, name, grade, section, email, phone)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (
            data['id'],
            data['name'],
            data['grade'],
            data.get('section', 'A'),
            data.get('email', ''),
            data.get('phone', '')
        ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            "success": True,
            "message": "Student added successfully",
            "student_id": data['id']
        }), 201
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/teachers', methods=['GET'])
def get_teachers():
    """Get all teachers"""
    try:
        # Mock data for teachers
        teachers = [
            {
                "id": "TCH001",
                "name": "Dr. Sharma",
                "subject": "Mathematics",
                "email": "sharma@bnm.edu",
                "phone": "9876543201"
            },
            {
                "id": "TCH002",
                "name": "Ms. Patel",
                "subject": "Science",
                "email": "patel@bnm.edu",
                "phone": "9876543202"
            }
        ]
        
        return jsonify({
            "success": True,
            "count": len(teachers),
            "teachers": teachers
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/courses', methods=['GET'])
def get_courses():
    """Get all courses"""
    try:
        courses = [
            {"id": "MATH101", "name": "Mathematics", "grade": "10", "teacher": "Dr. Sharma"},
            {"id": "SCI101", "name": "Science", "grade": "10", "teacher": "Ms. Patel"},
            {"id": "ENG101", "name": "English", "grade": "10", "teacher": "Mr. Verma"}
        ]
        
        return jsonify({
            "success": True,
            "count": len(courses),
            "courses": courses
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/attendance', methods=['POST'])
def mark_attendance():
    """Mark attendance"""
    try:
        data = request.get_json()
        
        # Simulate attendance marking
        return jsonify({
            "success": True,
            "message": "Attendance marked successfully",
            "date": data.get('date'),
            "students": len(data.get('students', []))
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "error": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"success": False, "error": "Internal server error"}), 500

# This is IMPORTANT for Vercel
# Vercel looks for 'app' by default, but we need to expose it as 'application'
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
else:
    # For Vercel serverless
    application = app
