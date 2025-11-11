"""
Script to manually add users to the database
"""
from app_simple import app, db, User
from werkzeug.security import generate_password_hash

def add_user(username, password):
    """Add a new user to the database"""
    with app.app_context():
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print(f"❌ User '{username}' already exists!")
            return False
        
        # Create new user
        new_user = User(
            username=username,
            password_hash=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()
        
        print(f"✅ User '{username}' created successfully!")
        return True

def list_users():
    """List all users in the database"""
    with app.app_context():
        users = User.query.all()
        if not users:
            print("No users found in database.")
            return
        
        print("\n📋 Current Users:")
        print("-" * 50)
        for user in users:
            print(f"  • {user.username} (ID: {user.id}) - Created: {user.created_at.strftime('%Y-%m-%d %H:%M')}")
        print("-" * 50)

def delete_user(username):
    """Delete a user from the database"""
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if not user:
            print(f"❌ User '{username}' not found!")
            return False
        
        db.session.delete(user)
        db.session.commit()
        print(f"✅ User '{username}' deleted successfully!")
        return True

if __name__ == '__main__':
    print("\n" + "="*50)
    print("     USER MANAGEMENT TOOL")
    print("="*50 + "\n")
    
    while True:
        print("\nOptions:")
        print("1. Add new user")
        print("2. List all users")
        print("3. Delete user")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            print("\n--- Add New User ---")
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            
            if username and password:
                add_user(username, password)
            else:
                print("❌ Username and password cannot be empty!")
        
        elif choice == '2':
            list_users()
        
        elif choice == '3':
            print("\n--- Delete User ---")
            username = input("Enter username to delete: ").strip()
            if username:
                confirm = input(f"Are you sure you want to delete '{username}'? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    delete_user(username)
                else:
                    print("Deletion cancelled.")
            else:
                print("❌ Username cannot be empty!")
        
        elif choice == '4':
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice! Please enter 1-4.")
