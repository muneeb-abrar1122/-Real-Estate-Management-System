# UnionEstate - Real Estate Management System

A complete Flask-based real estate management application with user authentication, client management, and a secure admin panel.

---

## 🌟 Features

### Main Application
- ✅ **User Authentication** - Secure login and registration system
- ✅ **Client Management** - Full CRUD operations (Create, Read, Update, Delete)
- ✅ **Advanced Search & Filtering** - Search by name, society, block, date range
- ✅ **Data Export/Import** - Backup and restore data in JSON format
- ✅ **Password Visibility Toggle** - Eye icon to show/hide passwords
- ✅ **Mobile Responsive** - Works perfectly on all devices

### Admin Panel
- ✅ **Secure Admin Access** - Password required on every access
- ✅ **User Management** - Create, edit, and delete users
- ✅ **Client Management** - Manage all clients from admin panel
- ✅ **Admin Password Change** - Change admin password anytime
- ✅ **Dashboard Statistics** - View total users, clients, and recent activity
- ✅ **Separate Authentication** - Independent from user login

---

## 🔐 Default Credentials

### Main Application Login
```
Username: union
Password: union1234
```

### Admin Panel Access
```
Admin Password: admin123
```

> **Note:** Admin panel requires password on **every access** for maximum security.

---

## 📦 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python app.py
```

### Step 3: Access the Application
Open your browser and navigate to:
```
http://localhost:5000
```

---

## 📖 User Guide

### 1. Login to Main Application

1. Open `http://localhost:5000` in your browser
2. Enter credentials:
   - Username: `union`
   - Password: `union1234`
3. Click the **eye icon** (👁) to show/hide password
4. Click **Sign In**

### 2. Register New User

1. On the login page, click **Register**
2. Fill in:
   - Username (unique)
   - Email address
   - Password (use eye icon to verify)
3. Click **Register**
4. You'll be redirected to login page

### 3. Managing Clients

#### Add New Client
1. After login, you'll see the dashboard
2. Fill in the **Add / Register Client** form:
   - Client name
   - Contact number
   - Society name
   - Plot number
   - Block (A-Z)
   - Price
   - Size
   - Date
   - Description (optional)
3. Click **Save Client**

#### Edit Client
1. Find the client in the list
2. Click **Edit** button
3. Modify the fields
4. Click **Save**

#### Delete Client
1. Click **Delete** button on any client
2. Confirm the deletion in the popup
3. Client will be removed

### 4. Search & Filter

#### Search by Text
- Use the search box at the top
- Type any text (name, society, plot number, etc.)
- Results update automatically

#### Filter by Block
1. Click the **menu icon** (☰) to open sidebar
2. Click **Blocks** to expand
3. Select any block (A-Z) or **All**

#### Filter by Date
1. Use the date filters above the client list
2. Select **From** date and/or **To** date
3. Results will filter automatically

### 5. Export/Import Data

#### Export Data
1. Open sidebar (menu icon)
2. Under **Data Tools**, click **Export**
3. JSON file will download automatically

#### Import Data
1. Open sidebar
2. Under **Data Tools**, click **Import**
3. Select a JSON file
4. Confirm the import
5. All data will be replaced

### 6. Access Admin Panel

1. Click **🏢 Admin Panel** in the sidebar
2. Enter admin password: `admin123`
3. Click eye icon to verify password
4. Click **Access Admin Panel**

> **Important:** Password is required **every time** you access the admin panel for security.

### 7. Admin Panel - User Management

#### View All Users
1. In admin panel, click **Users** in navigation
2. See list of all users with IDs and creation dates

#### Create New User
1. Click **+ Create User**
2. Fill in:
   - Username (must be unique)
   - Email
   - Password (use eye icon)
3. Click **Create**

#### Edit User
1. Click **Edit** next to any user
2. Modify username, email, or password
3. Leave password blank to keep current password
4. Click **Update**

#### Delete User
1. Click **Delete** next to any user
2. Confirm deletion
3. User will be removed

### 8. Admin Panel - Client Management

Works exactly like main app client management, but from admin panel.

1. Click **Clients** in admin navigation
2. Use **+ Create Client** to add new
3. Edit or delete any client
4. All changes sync with main app

### 9. Change Admin Password

1. In admin panel, click **Settings**
2. Enter:
   - Current Password (use eye icon)
   - New Password (minimum 6 characters)
   - Confirm New Password
3. All three fields have eye icons to verify
4. Click **Change Password**
5. Use new password for next admin access

### 10. Logout

#### Logout from Main App
- Click **Logout** in sidebar
- You'll be redirected to login page
- All sessions cleared

#### Logout from Admin Panel
- Click **Logout Admin** in navigation
- Admin session cleared
- User session remains active

---

## 💾 Data Storage

All data is stored in JSON files for easy backup and portability:

```
data/
├── users.json          # User accounts with IDs and timestamps
├── clients.json        # Client records with all details
└── admin_config.json   # Admin password (encrypted storage)
```

### Benefits of JSON Storage
- ✅ No database setup required
- ✅ Data persists across server restarts
- ✅ Easy to backup (just copy the `data/` folder)
- ✅ Portable across different deployments
- ✅ Human-readable format

---

## 🔑 Password Visibility Feature

Every password field includes an **eye icon** (👁) for convenience:

- **Click once** → Password becomes visible
- **Click again** → Password is hidden

Available on:
- Login page
- Registration page
- Admin login page
- Admin settings (all 3 password fields)
- User create/edit forms

---

## 🛡️ Security Features

1. **Separate Admin Authentication** - Admin panel has its own password system
2. **Password Required Every Time** - Admin panel requires password on each access
3. **Session Management** - Secure session handling for user login
4. **CSRF Protection** - Cross-Site Request Forgery protection enabled
5. **Password Visibility Control** - Users can verify passwords before submission

---

## 📱 Mobile Friendly

The application is fully responsive and mobile-optimized:

- ✅ Touch-friendly buttons (minimum 44px)
- ✅ Responsive grid layouts
- ✅ Mobile-optimized forms
- ✅ Sidebar navigation for small screens
- ✅ Works on phones, tablets, and desktops

---

## 🛠️ Technical Stack

### Backend
- **Framework:** Flask (Python)
- **Authentication:** Flask-Login
- **Session Management:** Flask sessions
- **CSRF Protection:** Flask-WTF

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Custom responsive design
- **JavaScript** - Vanilla JS for interactivity
- **SweetAlert2** - Beautiful alerts and confirmations

### Data Storage
- **JSON Files** - Simple, portable data storage

---

## 📂 Project Structure

```
UnionEstate/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── data/                       # Data storage
│   ├── users.json             # User accounts
│   ├── clients.json           # Client records
│   └── admin_config.json      # Admin configuration
├── templates/                  # HTML templates
│   ├── login.html             # User login page
│   ├── register.html          # User registration
│   ├── index.html             # Main dashboard
│   └── admin/                 # Admin panel templates
│       ├── admin_login.html   # Admin login
│       ├── dashboard.html     # Admin dashboard
│       ├── users.html         # User management
│       ├── user_form.html     # User create/edit
│       ├── clients.html       # Client management
│       ├── client_form.html   # Client create/edit
│       └── settings.html      # Admin settings
└── static/                     # Static assets
    ├── css/
    │   └── style.css          # Application styles
    └── js/
        └── app.js             # Client-side logic
```

---

## 🚀 Quick Start Guide

### For First-Time Users

1. **Install Python** (if not already installed)
   - Download from [python.org](https://www.python.org/)
   - Version 3.7 or higher required

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   python app.py
   ```

4. **Open in Browser**
   ```
   http://localhost:5000
   ```

5. **Login**
   - Username: `union`
   - Password: `union1234`

6. **Start Using!**
   - Add clients
   - Search and filter
   - Access admin panel
   - Manage users

---

## ⚙️ Configuration

### Change Admin Password
1. Login to admin panel
2. Go to Settings
3. Change password
4. New password saved in `data/admin_config.json`

### Add More Users
1. Use registration page, or
2. Use admin panel user management

### Backup Data
Simply copy the entire `data/` folder to backup all:
- User accounts
- Client records
- Admin configuration

---

## 🔧 Troubleshooting

### Application Won't Start
```bash
# Check if port 5000 is already in use
# Stop other Flask apps or change port in app.py
```

### Can't Login
- Verify credentials: `union` / `union1234`
- Check `data/users.json` file exists
- Try registering a new user

### Admin Panel Not Working
- Verify admin password: `admin123`
- Check `data/admin_config.json` exists
- Password required on **every** access

### Data Not Saving
- Check `data/` folder permissions
- Ensure JSON files are not corrupted
- Check console for error messages

---

## 📊 Features Summary

| Feature | Status | Description |
|---------|--------|-------------|
| User Login | ✅ | Secure authentication system |
| User Registration | ✅ | Self-service account creation |
| Client CRUD | ✅ | Full create, read, update, delete |
| Search & Filter | ✅ | Advanced filtering options |
| Export/Import | ✅ | Data backup and restore |
| Admin Panel | ✅ | Separate admin interface |
| User Management | ✅ | Admin can manage users |
| Password Toggle | ✅ | Show/hide password feature |
| Mobile Friendly | ✅ | Responsive design |
| Data Persistence | ✅ | JSON file storage |
| Secure Access | ✅ | Password required every time |

---

## 📝 Important Notes

### Security
- This is a **development version**
- For production use:
  - Use environment variables for passwords
  - Enable HTTPS
  - Use a proper database
  - Implement password hashing
  - Add rate limiting

### Data Backup
- Regularly backup the `data/` folder
- Use the export feature for quick backups
- Keep backups in a safe location

### Admin Access
- Admin password is required **every time**
- This is by design for maximum security
- Change default password after first use

---

## 🆘 Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Verify all dependencies are installed
3. Check the console for error messages
4. Ensure data files are not corrupted
5. Try restarting the application

---

## 📄 License

This project is created for UnionEstate real estate management.

---

## 🎯 Version Information

**Current Version:** 1.0.0
**Last Updated:** December 2025

### Recent Updates
- ✅ Complete CRUD operations for users and clients
- ✅ Password visibility toggle on all password fields
- ✅ Admin panel with secure access
- ✅ Enhanced security with password required every time
- ✅ Mobile-responsive design
- ✅ Export/Import functionality

---

**Made with ❤️ for UnionEstate**

For any questions or support, please refer to this documentation.
