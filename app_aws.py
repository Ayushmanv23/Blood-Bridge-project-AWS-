from flask import Flask, render_template, request, redirect, url_for, session, flash
import boto3
import uuid
import os

# ================= AWS CLIENTS =================
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
sns = boto3.client('sns', region_name='us-east-1')

USERS_TABLE = dynamodb.Table('BloodBridgeUsers')
REQUESTS_TABLE = dynamodb.Table('BloodRequests')
INVENTORY_TABLE = dynamodb.Table('BloodInventory')

SNS_TOPIC_ARN = "arn:aws:sns:ap-south-1:XXXXXXXXXXXX:BloodBridgeAlerts"
# ↑ replace ACCOUNT ID only (region auto from EC2)

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
    data['request_id'] = str(uuid.uuid4())
    REQUESTS_TABLE.put_item(Item=data)

    # SNS Notification
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject="🚨 New Blood Request",
        Message=f"""
New Blood Request Raised!

Blood Group: {data['blood_group']}
Quantity: {data['quantity']}
Urgency: {data['urgency']}
Hospital: {data['requested_by']}
"""
    )

def get_inventory():
    res = INVENTORY_TABLE.scan()
    return {item['blood_group']: int(item['quantity']) for item in res.get('Items', [])}

def update_inventory(blood_group, qty):
    INVENTORY_TABLE.update_item(
        Key={'blood_group': blood_group},
        UpdateExpression="SET quantity = if_not_exists(quantity, :z) + :q",
        ExpressionAttributeValues={
            ':q': qty,
            ':z': 0
        }
    )

# ================= ROUTES =================
@app.route('/')
def home():
    return render_template('index.html')

# ---------- LOGIN ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user(username)
        if user and user['password'] == password:
            session['username'] = username
            session['role'] = user['role']
            return redirect(url_for('dashboard'))

        flash('Invalid username or password', 'error')

    return render_template('login.html')

# ---------- LOGOUT ----------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ---------- REGISTER ----------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        if get_user(username):
            flash('Username already exists', 'error')
            return redirect(url_for('register'))

        user_data = {
            'username': username,
            'password': password,
            'role': role
        }

        if role == 'donor':
            user_data.update({
                'blood_group': request.form.get('blood_group'),
                'gender': request.form.get('gender'),
                'state': request.form.get('state'),
                'area': request.form.get('area'),
                'last_donation': "Never"
            })

        create_user(user_data)
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# ---------- DASHBOARD ----------
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

    if request.args.get('search'):
        s_state = request.args.get('state', '').lower()
        s_area = request.args.get('area', '').lower()
        s_blood = request.args.get('blood_group', '').lower()

        users = USERS_TABLE.scan().get('Items', [])
        for u in users:
            if u['role'] == 'donor':
                match = True
                if s_state and s_state not in u.get('state', '').lower(): match = False
                if s_area and s_area not in u.get('area', '').lower(): match = False
                if s_blood and s_blood != u.get('blood_group', '').lower(): match = False
                if match:
                    search_results.append(u)

    return render_template(
        'dashboard.html',
        username=username,
        role=role,
        inventory=inventory,
        requests=requests_data,
        user_data=user_data,
        search_results=search_results
    )

# ---------- ADD REQUEST ----------
@app.route('/add_request', methods=['POST'])
def add_request():
    if 'username' not in session or session['role'] != 'hospital':
        return redirect(url_for('dashboard'))

    create_blood_request({
        'blood_group': request.form['blood_group'],
        'quantity': int(request.form['quantity']),
        'urgency': request.form['urgency'],
        'requested_by': session['username']
    })

    flash('Blood request submitted & notifications sent!', 'success')
    return redirect(url_for('dashboard'))

# ---------- UPDATE INVENTORY ----------
@app.route('/update_inventory', methods=['POST'])
def update_inventory_route():
    if 'username' not in session or session['role'] != 'blood_bank':
        return redirect(url_for('dashboard'))

    blood_group = request.form['blood_group']
    qty = int(request.form['quantity_change'])

    update_inventory(blood_group, qty)
    flash(f'Inventory updated for {blood_group}', 'success')
    return redirect(url_for('dashboard'))

# ---------- INVENTORY PAGE ----------
@app.route('/inventory')
def inventory_page():
    if 'username' not in session or session['role'] != 'blood_bank':
        return redirect(url_for('dashboard'))

    return render_template('inventory.html', inventory=get_inventory())

# ---------- BLOG ----------
@app.route('/blog')
def blog():
    return render_template('blog.html')

# ---------- CONTACT ----------
@app.route('/contact', methods=['POST'])
def contact():
    flash('Thank you for contacting us! We will get back to you shortly.', 'success')
    return redirect(url_for('home'))

# ================= RUN =================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
