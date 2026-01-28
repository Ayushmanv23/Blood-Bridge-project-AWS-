from flask import Flask, render_template, request, redirect, url_for, session, flash
import boto3
import uuid
import os
from decimal import Decimal

# ================= AWS CLIENT =================
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

USERS_TABLE = dynamodb.Table('BloodBridgeUsers')
REQUESTS_TABLE = dynamodb.Table('BloodRequests')
INVENTORY_TABLE = dynamodb.Table('BloodInventory')

# ================= FLASK APP =================
app = Flask(__name__)
app.secret_key = os.urandom(24)

# ================= HELPERS =================
def get_user(username):
    res = USERS_TABLE.get_item(Key={'username': username})
    return res.get('Item')

def create_user(user_data):
    USERS_TABLE.put_item(Item=user_data)

def get_all_requests():
    return REQUESTS_TABLE.scan().get('Items', [])

def create_blood_request(data):
    item = {
        'request_id': str(uuid.uuid4()),
        'blood_group': data['blood_group'],
        'quantity': Decimal(str(data['quantity'])),
        'urgency': data['urgency'],
        'requested_by': data['requested_by']
    }
    REQUESTS_TABLE.put_item(Item=item)

def get_inventory():
    res = INVENTORY_TABLE.scan()
    return {item['blood_group']: int(item['quantity']) for item in res.get('Items', [])}

def update_inventory(blood_group, qty):
    INVENTORY_TABLE.update_item(
        Key={'blood_group': blood_group},
        UpdateExpression="SET quantity = if_not_exists(quantity, :z) + :q",
        ExpressionAttributeValues={
            ':q': Decimal(int(qty)),
            ':z': Decimal(0)
        }
    )

# ================= ROUTES =================
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = get_user(request.form['username'])
        if user and user['password'] == request.form['password']:
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('dashboard'))
        flash("Invalid credentials", "error")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if get_user(request.form['username']):
            flash("Username already exists", "error")
            return redirect(url_for('register'))

        user_data = {
            'username': request.form['username'],
            'password': request.form['password'],
            'role': request.form['role']
        }

        if request.form['role'] == 'donor':
            user_data.update({
                'blood_group': request.form.get('blood_group'),
                'state': request.form.get('state'),
                'area': request.form.get('area'),
                'last_donation': "Never"
            })

        create_user(user_data)
        flash("Registration successful", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

# ================= DASHBOARD (FIXED & COMPLETE) =================
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    role = session['role']
    user_data = get_user(username)

    inventory = get_inventory()
    requests_data = get_all_requests()
    search_results = []

    # ✅ HOSPITAL: SEARCH DONORS
    if role == 'hospital' and request.args.get('search'):
        s_state = request.args.get('state', '').lower()
        s_area = request.args.get('area', '').lower()
        s_blood = request.args.get('blood_group', '').lower()

        users = USERS_TABLE.scan().get('Items', [])
        for u in users:
            if u.get('role') == 'donor':
                match = True
                if s_state and s_state not in u.get('state', '').lower():
                    match = False
                if s_area and s_area not in u.get('area', '').lower():
                    match = False
                if s_blood and s_blood != u.get('blood_group', '').lower():
                    match = False
                if match:
                    search_results.append(u)

    return render_template(
        'dashboard.html',
        username=username,
        role=role,
        user_data=user_data,
        inventory=inventory,
        requests=requests_data,
        search_results=search_results
    )

# ================= HOSPITAL: ADD REQUEST =================
@app.route('/add_request', methods=['POST'])
def add_request():
    create_blood_request({
        'blood_group': request.form['blood_group'],
        'quantity': request.form['quantity'],
        'urgency': request.form['urgency'],
        'requested_by': session['username']
    })
    flash("Blood request submitted successfully", "success")
    return redirect(url_for('dashboard'))

# ================= INVENTORY =================
@app.route('/inventory')
def inventory_page():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.args.get('from_donate') == 'true':
        flash(
            "Thank you for your willingness to donate. Our team will contact you shortly.",
            "success"
        )

    return render_template('inventory.html', inventory=get_inventory())

@app.route('/update_inventory', methods=['POST'])
def update_inventory_route():
    update_inventory(
        request.form['blood_group'],
        request.form['quantity_change']
    )
    flash("Inventory updated successfully", "success")
    return redirect(url_for('inventory_page'))

# ================= STATIC PAGES =================
@app.route('/contact', methods=['POST'])
def contact():
    flash("Thank you for contacting us. Our team will get back to you shortly.", "success")
    return redirect(url_for('home'))

@app.route('/blog')
def blog():
    return render_template('blog.html')

# ================= RUN =================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
