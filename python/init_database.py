"""
Simple database initialization script
Run with: docker-compose exec web python init_database.py
"""
import sys
import os

# Add app to path
sys.path.insert(0, '/app')

try:
    from app_production import create_app
    from core.extensions import db
    from models import User
    from werkzeug.security import generate_password_hash
    
    print("Initializing database...")
    
    app = create_app()
    
    with app.app_context():
        # Create tables
        db.create_all()
        print("✅ Database tables created!")
        
        # Check if admin exists
        admin = User.query.filter_by(email='admin@sentiment.ai').first()
        
        if not admin:
            # Create admin user
            admin = User(
                email='admin@sentiment.ai',
                name='Admin User',
                password_hash=generate_password_hash('Admin123!'),
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created!")
            print("   Email: admin@sentiment.ai")
            print("   Password: Admin123!")
        else:
            print("✅ Admin user already exists")
        
        # Create demo user
        demo = User.query.filter_by(email='demo@sentiment.ai').first()
        if not demo:
            demo = User(
                email='demo@sentiment.ai',
                name='Demo User',
                password_hash=generate_password_hash('Demo123!')
            )
            db.session.add(demo)
            db.session.commit()
            print("✅ Demo user created!")
            print("   Email: demo@sentiment.ai")
            print("   Password: Demo123!")
        
        print("\n✅ Database initialization complete!")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
