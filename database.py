"""
Database implementation using in-memory Python dictionaries.
"""

# 4.1 Users Table
# Stores user credentials and profile info
users = {
    "john": {
        "password": "1234",
        "role": "donor",
        "blood_group": "O+",
        "gender": "Male",
        "state": "California",
        "area": "Los Angeles",
        "last_donation": "2025-11-01"
    },
    "emma": {
        "password": "1234",
        "role": "donor",
        "blood_group": "A-",
        "gender": "Female",
        "state": "New York",
        "area": "Manhattan",
        "last_donation": "2025-12-15"
    },
    "mike": {
        "password": "1234",
        "role": "donor",
        "blood_group": "B+",
        "gender": "Male",
        "state": "California",
        "area": "San Francisco",
        "last_donation": "Never"
    },
    "lisa": {
        "password": "admin",
        "role": "blood_bank"
    },
    "hospital": {
        "password": "pass",
        "role": "hospital"
    }
}

# 4.2 Blood Requests Table
# Stores active blood requests
# A list of dictionaries
blood_requests = [
    {
        "id": 1,
        "blood_group": "AB-",
        "quantity": 2,
        "urgency": "High",
        "requested_by": "Hospital A"
    }
]

# 4.3 Blood Inventory Table
# Stores current stock of blood bags
inventory = {
    "A+": 10,
    "A-": 4,
    "B+": 6,
    "O+": 12,
    "AB-": 1,
    "AB+": 0,
    "O-": 2,
    "B-": 1
}
