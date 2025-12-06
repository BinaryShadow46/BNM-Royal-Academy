-- BNM ROYAL ACADEMY Database Schema

CREATE DATABASE IF NOT EXISTS bnm_royal_academy;
USE bnm_royal_academy;

-- Users Table
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'teacher', 'student', 'parent', 'staff') NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL
);

-- Students Table
CREATE TABLE students (
    student_id VARCHAR(20) PRIMARY KEY,
    user_id INT UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender ENUM('Male', 'Female', 'Other'),
    address TEXT,
    parent_name VARCHAR(100),
    parent_phone VARCHAR(15),
    parent_email VARCHAR(100),
    admission_date DATE NOT NULL,
    grade VARCHAR(10),
    section VARCHAR(10),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Teachers Table
CREATE TABLE teachers (
    teacher_id VARCHAR(20) PRIMARY KEY,
    user_id INT UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    qualification VARCHAR(100),
    specialization VARCHAR(100),
    joining_date DATE,
    phone VARCHAR(15),
    email VARCHAR(100) UNIQUE,
    department VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Courses/Subjects Table
CREATE TABLE courses (
    course_id VARCHAR(20) PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    description TEXT,
    grade VARCHAR(10),
    teacher_id VARCHAR(20),
    credits INT DEFAULT 1,
    academic_year YEAR,
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
);

-- Attendance Table
CREATE TABLE attendance (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id VARCHAR(20),
    date DATE NOT NULL,
    status ENUM('Present', 'Absent', 'Late', 'Excused') NOT NULL,
    course_id VARCHAR(20),
    recorded_by VARCHAR(20),
    notes TEXT,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- Grades/Marks Table
CREATE TABLE grades (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id VARCHAR(20),
    course_id VARCHAR(20),
    exam_type VARCHAR(50),
    marks_obtained DECIMAL(5,2),
    total_marks DECIMAL(5,2),
    percentage DECIMAL(5,2),
    grade CHAR(2),
    exam_date DATE,
    recorded_by VARCHAR(20),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- Timetable Table
CREATE TABLE timetable (
    id INT PRIMARY KEY AUTO_INCREMENT,
    grade VARCHAR(10),
    section VARCHAR(10),
    day_of_week ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'),
    period INT,
    course_id VARCHAR(20),
    teacher_id VARCHAR(20),
    classroom VARCHAR(20),
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
);

-- Fees Table
CREATE TABLE fees (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id VARCHAR(20),
    fee_type VARCHAR(50),
    amount DECIMAL(10,2),
    due_date DATE,
    paid_amount DECIMAL(10,2) DEFAULT 0,
    payment_date DATE,
    status ENUM('Paid', 'Pending', 'Partial') DEFAULT 'Pending',
    payment_method VARCHAR(50),
    transaction_id VARCHAR(100),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);
