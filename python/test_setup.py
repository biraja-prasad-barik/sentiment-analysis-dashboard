"""
Test script to verify if the application will run successfully
"""
import sys
import os

def test_imports():
    """Test if all required packages are installed"""
    print("\n" + "="*60)
    print("TESTING PACKAGE IMPORTS")
    print("="*60 + "\n")
    
    required_packages = {
        'flask': 'Flask',
        'flask_cors': 'Flask-CORS',
        'flask_sqlalchemy': 'Flask-SQLAlchemy',
        'werkzeug.security': 'Werkzeug',
        'transformers': 'Transformers (for ML)',
        'torch': 'PyTorch (for ML)',
        'selenium': 'Selenium (for scraping)',
        'bs4': 'BeautifulSoup4 (for scraping)',
    }
    
    missing = []
    installed = []
    
    for package, name in required_packages.items():
        try:
            __import__(package)
            print(f"✅ {name:30} - Installed")
            installed.append(name)
        except ImportError:
            print(f"❌ {name:30} - NOT installed")
            missing.append(name)
    
    return missing, installed

def test_files():
    """Test if all required files exist"""
    print("\n" + "="*60)
    print("TESTING FILE STRUCTURE")
    print("="*60 + "\n")
    
    required_files = [
        'app_simple.py',
        'add_user.py',
        'templates/login.html',
        'templates/index.html',
        'models/sentiment_model.py',
        'services/review_scraper.py',
        'static/css/style.css',
        'static/js/app.js',
    ]
    
    missing = []
    found = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file:40} - Found")
            found.append(file)
        else:
            print(f"❌ {file:40} - MISSING")
            missing.append(file)
    
    return missing, found

def test_syntax():
    """Test Python syntax of main files"""
    print("\n" + "="*60)
    print("TESTING PYTHON SYNTAX")
    print("="*60 + "\n")
    
    files_to_test = [
        'app_simple.py',
        'add_user.py',
    ]
    
    errors = []
    
    for file in files_to_test:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                compile(f.read(), file, 'exec')
            print(f"✅ {file:40} - Syntax OK")
        except SyntaxError as e:
            print(f"❌ {file:40} - Syntax Error: {e}")
            errors.append(file)
    
    return errors

def test_app_import():
    """Test if app can be imported"""
    print("\n" + "="*60)
    print("TESTING APP IMPORT")
    print("="*60 + "\n")
    
    try:
        # Try importing the simple app
        sys.path.insert(0, os.getcwd())
        from app_simple import app, db, User
        print("✅ app_simple.py can be imported successfully")
        print(f"✅ Flask app created: {app}")
        print(f"✅ Database initialized: {db}")
        print(f"✅ User model available: {User}")
        return True
    except Exception as e:
        print(f"❌ Cannot import app_simple.py: {e}")
        return False

def generate_report(missing_packages, missing_files, syntax_errors, app_import_ok):
    """Generate final report"""
    print("\n" + "="*60)
    print("FINAL REPORT")
    print("="*60 + "\n")
    
    all_ok = True
    
    # Check packages
    if missing_packages:
        all_ok = False
        print("❌ MISSING PACKAGES:")
        for pkg in missing_packages:
            print(f"   - {pkg}")
        print("\n   Install with:")
        print("   pip install flask flask-cors flask-sqlalchemy werkzeug")
        print("   pip install transformers torch selenium beautifulsoup4")
    else:
        print("✅ All required packages installed")
    
    # Check files
    if missing_files:
        all_ok = False
        print("\n❌ MISSING FILES:")
        for file in missing_files:
            print(f"   - {file}")
    else:
        print("✅ All required files present")
    
    # Check syntax
    if syntax_errors:
        all_ok = False
        print("\n❌ SYNTAX ERRORS IN:")
        for file in syntax_errors:
            print(f"   - {file}")
    else:
        print("✅ No syntax errors found")
    
    # Check app import
    if not app_import_ok:
        all_ok = False
        print("\n❌ Cannot import application")
    else:
        print("✅ Application can be imported")
    
    # Final verdict
    print("\n" + "="*60)
    if all_ok:
        print("🎉 SUCCESS! Your application is ready to run!")
        print("="*60)
        print("\nRun with:")
        print("   python app_simple.py")
        print("\nThen open: http://localhost:5000")
        print("Login: admin / admin123")
    else:
        print("⚠️  ISSUES FOUND - Please fix the above issues")
        print("="*60)
        if missing_packages:
            print("\nQuick fix:")
            print("   pip install flask flask-cors flask-sqlalchemy werkzeug")
    
    return all_ok

if __name__ == '__main__':
    print("\n" + "="*60)
    print("SENTIMENT ANALYSIS APP - SETUP VERIFICATION")
    print("="*60)
    
    # Run tests
    missing_packages, installed_packages = test_imports()
    missing_files, found_files = test_files()
    syntax_errors = test_syntax()
    app_import_ok = test_app_import()
    
    # Generate report
    success = generate_report(missing_packages, missing_files, syntax_errors, app_import_ok)
    
    # Exit code
    sys.exit(0 if success else 1)
