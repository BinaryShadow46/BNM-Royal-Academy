import os
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__, 
                static_folder='../static' if os.path.exists('../static') else None,
                template_folder='templates')
    
    # Configuration
    if os.environ.get('VERCEL'):
        # Vercel environment
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'vercel-secret-key')
        database_url = os.environ.get('DATABASE_URL')
        if database_url and database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///:memory:'
    else:
        # Local development
        from config import Config
        app.config.from_object(Config)
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    CORS(app)
    db.init_app(app)
    login_manager.init_app(app)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.students import students_bp
    from app.routes.teachers import teachers_bp
    from app.routes.admin import admin_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(students_bp, url_prefix='/api/students')
    app.register_blueprint(teachers_bp, url_prefix='/api/teachers')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    
    # Serve static files
    @app.route('/')
    def index():
        return send_from_directory(app.template_folder, 'index.html') if os.path.exists(os.path.join(app.template_folder, 'index.html')) else "BNM Royal Academy SMS API"
    
    @app.route('/<path:path>')
    def serve_static(path):
        if os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        return "Not Found", 404
    
    return app
