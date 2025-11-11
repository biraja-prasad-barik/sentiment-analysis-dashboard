# 🚀 How to Run with Login

## Quick Start

### Step 1: Run the Application

```bash
python app_simple.py
```

This will:
- ✅ Create the database
- ✅ Create a default admin user
- ✅ Start the server on http://localhost:5000

### Step 2: Open Browser

Open: **http://localhost:5000**

You'll see the login page!

### Step 3: Login

**Default Credentials:**
- **Username:** `admin`
- **Password:** `admin123`

---

## 📝 Managing Users

### Add New Users Manually

Run the user management tool:

```bash
python add_user.py
```

This interactive tool lets you:
1. ✅ Add new users
2. ✅ List all users
3. ✅ Delete users

**Example:**
```
Options:
1. Add new user
2. List all users
3. Delete user
4. Exit

Enter your choice (1-4): 1

--- Add New User ---
Enter username: john
Enter password: john123
✅ User 'john' created successfully!
```

---

## 🔐 Login Flow

1. Open http://localhost:5000
2. You'll see the login page
3. Enter username and password
4. Click "Login"
5. You'll be redirected to the dashboard
6. Now you can use all features!

---

## 📊 Features After Login

Once logged in, you can:
- ✅ Analyze text sentiment
- ✅ Scrape reviews from websites
- ✅ View analytics dashboard
- ✅ See all reviews

---

## 🔧 Troubleshooting

### "Module not found"
```bash
pip install flask flask-cors flask-sqlalchemy werkzeug
```

### "Port already in use"
Change the port in `app_simple.py`:
```python
app.run(debug=True, port=8000)  # Change 5000 to 8000
```

### "Can't login"
Make sure the default user was created. Check the console output when starting the app.

---

## 🎯 Quick Commands

```bash
# Start the app
python app_simple.py

# Add users manually
python add_user.py

# Stop the app
Press Ctrl+C
```

---

## 💡 Tips

1. **Change default password** - Use `add_user.py` to create a new admin with a strong password
2. **Multiple users** - You can create as many users as you want
3. **Logout** - Go to http://localhost:5000/logout to logout

---

**That's it! You're ready to go! 🎉**
