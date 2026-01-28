from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import users, blood_requests, inventory
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# --- Routes ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username]['password'] == password:
            session['username'] = username
            session['role'] = users[username]['role']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        
        if username in users:
            flash('Username already exists', 'error')
        else:
            # Create new user
            users[username] = {
                "password": password,
                "role": role
            }
            # Initialize additional fields if needed
            if role == 'donor':
                users[username]['blood_group'] = request.form.get('blood_group', 'unknown')
                users[username]['gender'] = request.form.get('gender', 'unknown')
                users[username]['state'] = request.form.get('state', 'unknown')
                users[username]['area'] = request.form.get('area', 'unknown')
                users[username]['last_donation'] = "Never"
                
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
            
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    role = session['role']
    user_data = users[username]
    
    search_results = []
    if request.args.get('search'):
        s_state = request.args.get('state', '').lower()
        s_area = request.args.get('area', '').lower()
        s_blood = request.args.get('blood_group', '').lower()
        
        for u, data in users.items():
            if data['role'] == 'donor':
                # Simple match logic
                match = True
                if s_state and s_state not in data.get('state', '').lower(): match = False
                if s_area and s_area not in data.get('area', '').lower(): match = False
                if s_blood and s_blood != data.get('blood_group', '').lower(): match = False
                
                if match:
                    # Add username to display
                    data_copy = data.copy()
                    data_copy['username'] = u
                    search_results.append(data_copy)

    return render_template('dashboard.html', 
                           username=username, 
                           role=role, 
                           inventory=inventory, 
                           requests=blood_requests,
                           user_data=user_data,
                           search_results=search_results)

@app.route('/add_request', methods=['POST'])
def add_request():
    if 'username' not in session or session['role'] != 'hospital':
        return redirect(url_for('dashboard'))
        
    blood_group = request.form['blood_group']
    quantity = int(request.form['quantity'])
    urgency = request.form['urgency']
    
    new_request = {
        "id": len(blood_requests) + 1,
        "blood_group": blood_group,
        "quantity": quantity,
        "urgency": urgency,
        "requested_by": session['username']
    }
    blood_requests.append(new_request)
    flash('Blood request submitted successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/update_inventory', methods=['POST'])
def update_inventory():
    if 'username' not in session or session['role'] != 'blood_bank':
        return redirect(url_for('dashboard'))
    
    # We expect form data like "A+" : "val", "B+" : "val"
    # Or a simplified interface. Let's assume the inventory.html sends specific updates or we use this route to handle a form for a specific item.
    # For simplicity, let's assume the dashboard offers a way to update specifically.
    # Let's support updating a single item for now or bulk.
    
    # Check if this is a bulk update or specific item
    blood_group = request.form.get('blood_group')
    quantity_change = request.form.get('quantity_change')
    
    if blood_group and quantity_change:
        if blood_group in inventory:
            inventory[blood_group] = max(0, inventory[blood_group] + int(quantity_change))
            flash(f'Inventory updated for {blood_group}', 'success')
        else:
            flash('Invalid blood group', 'error')
            
    return redirect(url_for('dashboard'))

@app.route('/inventory', methods=['GET'])
def inventory_page():
    if 'username' not in session or session['role'] != 'blood_bank':
        return redirect(url_for('dashboard'))
    return render_template('inventory.html', inventory=inventory)

@app.route('/contact', methods=['POST'])
def contact():
    # In a real app, this would send an email via AWS SES or SMTP
    flash('Thank you for contacting us! We will get back to you shortly.', 'success')
    return redirect(url_for('home'))

@app.route('/blog')
def blog():
    return render_template('blog.html')


if __name__ == '__main__':
    app.run(debug=True)
