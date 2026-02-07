BRIDGE: CLOUD-BASED BLOOD DONATION & REQUEST MANAGEMENT SYSTEM USING AWS

Project Description:
With the growing demand for timely access to blood during medical emergencies, traditional blood donation and blood request systems often face serious limitations such as lack of centralized data, delayed communication, and inefficient coordination between donors, hospitals, and patients. These issues can result in critical delays during emergencies where every minute is vital. To overcome these challenges, Blood Bridge is developed as a cloud-based blood donation and request management platform that connects donors and recipients through a reliable and scalable system. Blood Bridge is built using Flask as the backend framework and is deployed on AWS EC2 to ensure high availability and scalability. The application uses Amazon DynamoDB as a NoSQL database for fast and efficient storage of user data, donor information, and blood request records. By leveraging cloud infrastructure, Blood Bridge ensures secure data handling, rapid response times, and uninterrupted service during peak usage, making it a dependable solution for emergency healthcare support.
Scenario 1: Efficient Blood Request and Donation Management
In the Blood Bridge system, AWS EC2 provides a robust and scalable infrastructure capable of handling multiple users accessing the platform simultaneously. A user can log in to the application, register either as a blood donor or as a recipient, and update their profile details such as blood group and location. When a recipient raises a blood request, the system stores the request details in DynamoDB and makes them instantly available for matching with eligible donors. Flask manages backend logic such as request validation, session management, and database interactions. 
Scenario 2: Centralized Blood Data Management
Blood Bridge provides a centralized platform where blood availability data is stored and managed efficiently. All donor details, including blood group, contact information, and availability status, are stored securely in DynamoDB. When a blood request is raised, the system retrieves matching donor information based on blood group and location. This centralized data model eliminates the need for manual coordination and reduces dependency on traditional phone-based communication. 
Scenario 3: Easy Access to Blood Availability Information
Blood Bridge offers users a clean and user-friendly interface to search for blood availability across different locations. After logging in, users can filter donors by blood group and city, allowing them to quickly identify potential donors nearby. Flask dynamically fetches relevant data from DynamoDB and renders it on the frontend, ensuring real-time updates without page delays. 

<img width="1920" height="1020" alt="Screenshot 2026-01-28 222224" src="https://github.com/user-attachments/assets/3d642f5a-8463-45d1-ae07-c127c88f30b8" />BLOOD 

AWS Architecture

The architecture of Blood Bridge is designed using a cloud-native approach. The Flask web application is hosted on an AWS EC2 instance, which handles all client requests. DynamoDB acts as the primary database for storing user registrations, donor records, and blood request details. IAM roles are used to securely allow the EC2 instance to interact with DynamoDB without exposing sensitive credentials. 
Entity Relationship (ER) Diagram:
The ER diagram of Blood Bridge consists of the following main entities:
Users, Donors, Blood Requests

<img width="1920" height="1020" alt="Screenshot 2026-01-28 222224" src="https://github.com/user-attachments/assets/f049f7dc-a801-4133-b225-e8d404c2fc7d" />

Relationships define how users can act as donors or recipients and how blood requests are linked.

Pre-requisites:
AWS Account Setup: AWS Account Setup
Understanding IAM: IAM Overview
Amazon EC2 Basics: EC2 Tutorial
DynamoDB Basics: DynamoDB Introduction
Git Version Control: Git Documentation

Project Workflow:
AWS Account Setup and Login
Activity 1.1: Set up an AWS account if not already done.
Activity 1.2: Log in to the AWS Management Console.
DynamoDB Database Creation and Setup
Activity 2.1: Create DynamoDB tables.
Activity 2.2: Configure attributes for users, donors, and blood requests.
Backend Development and Application Setup
Activity 3.1: Develop backend using Flask.
Activity 3.2: Integrate DynamoDB using boto3.
IAM Role Setup
Activity 4.1: Create IAM Role.
Activity 4.2: Attach required policies.
EC2 Instance Setup
Activity 5.1: Launch EC2 instance to host the application.
Deployment on EC2
Activity 6.1: Upload Flask files.
Activity 6.2: Run the Flask application.
Testing and Validation
Activity 7.1: Perform functional testing of all modules.

<img width="1920" height="1020" alt="Screenshot 2026-01-28 232226" src="https://github.com/user-attachments/assets/99aee91f-3dae-4e90-b80c-8d8ba6e8bd28" />

Milestone 1: AWS Account Setup and Login
● Activity 1.1: Create an AWS account and configure billing settings.
 ● Activity 1.2: Log in to the AWS Management Console and verify access to required services.

Accessed AWS account through Troven lab

Milestone 2: DynamoDB Creation and Setup
● Activity 2.1: Navigate to DynamoDB in the AWS Console and create tables.


● Activity 2.2: Create the following tables:
BloodBridge_Users (Partition Key: Email)

BloodBridge_Inventory (Partition Key: Donor_ID)

BloodBridge_Requests (Partition Key: Request_ID)

 
Each table is configured to store structured yet flexible data suitable for real-time access.
 


Confirm validation in troven lab
 
 
Milestone 3: Backend Development and Application Setup
Activity 3.1: Backend Development Using Flask
File Explorer Structure: The project contains folders for templates, static files (CSS, JS), and a main app.py file for backend logic.

Flask App Initialization
Description: Flask is used for routing, session management, and user authentication. Secure password hashing is implemented to protect user credentials. Environment variables are used to manage sensitive configuration details.
DynamoDB Setup
Description: The boto3 library is used to establish a connection with DynamoDB. CRUD operations are implemented for user registration, donor management, and blood request handling. The AWS region is explicitly specified to ensure proper service connectivity.
Routes for Web Pages

Register Route: Collects user registration data, hashes passwords, and stores user details in DynamoDB.


 
Login Route: Verifies user credentials and redirects authenticated users to the dashboard.

<img width="1920" height="1020" alt="Screenshot 2026-01-28 222358" src="https://github.com/user-attachments/assets/94c6e0ba-a669-424d-ac96-e513b1b6e8c6" />

Logout Route: Clears session data securely.

Dashboard Route: Displays donor availability and blood request options.

<img width="1920" height="1020" alt="Screenshot 2026-01-28 232439" src="https://github.com/user-attachments/assets/12c24d6e-7a86-4715-a181-5ce21d43a58b" />

Blood Request Route: Allows recipients to raise blood requests and store them in the database.

Application Entry Point
Description: The Flask application is started using the built-in development server with configured host and port values for testing and deployment.

 

Milestone 4: IAM Role Setup
● Activity 4.1: Create an IAM role for the EC2 instance.

● Activity 4.2: Attach the following policy:
AmazonDynamoDBFullAccess
AmazonEC2FullAccess


 
This ensures secure access to DynamoDB without embedding credentials in the code.
 


 
Milestone 5: EC2 Instance Setup
● Launch an EC2 instance using Amazon Linux 2 or Ubuntu (t2.micro – free tier).


Created new key pair name.
 

 

Instance launched successfully
 
.

Validated the Instance creation. 
 


Now after launching the instance, we connected the IAM role to this.
 

 

After adding the IAM role to instance, connect the instance to the server.
 


Successful connection. 
 



 ● Create and download a key pair for secure access.
 ● Configure security groups to allow HTTP (port 80/5000) and SSH (port 22).
 
Milestone 6: Deployment on EC2
Activity 6.1: Install Required Software
sudo yum update -y
sudo yum install python3 git
sudo pip3 install flask boto3
Activity 6.2: Clone Project from GitHub
git clone https://github.com/Ayushmanv23/Blood-Bridge-project-AWS-.git
cd Blood-Bridge-project-AWS-
sudo flask run --host=0.0.0.0 --port=5000
Verification
Access the application using:
http://<EC2-Public-IP>:5000
 
Milestone 7: Testing and Validation
● Conduct functional testing for the following:
User Registration

 
User Login

Donor Search
 

 
Blood Request Submission

DynamoDB Data Updates
 

Pages Tested:
Index Page
Register Page
Login Page
Dashboard Page
Blood Request Page
DynamoDB Updates:
BloodBridge_Users Table
BloodBridge_Donors Table
BloodBridge_Requests Table
 
 

Update and maintain the inventory.
 


Finally checking all the validating metrics.
 
 
 
 
 
 
 
 
 
 
 
Conclusion:
The Blood Bridge application has been successfully designed, implemented, and deployed using a scalable and reliable cloud-based architecture on Amazon Web Services. By leveraging AWS EC2 for application hosting and Amazon DynamoDB for fast, flexible, and highly available data storage, the platform effectively addresses the critical challenges associated with traditional blood donation and blood request systems. The system ensures that donor and recipient information is stored securely, accessed efficiently, and updated in real time, which is essential during medical emergencies where timely access to blood can save lives. The integration of Flask as the backend framework enables clean routing, secure user authentication, session management, and smooth interaction between the frontend and the cloud database. The modular structure of the application makes it easy to understand, maintain, and extend. DynamoDB’s schema-less design allows the application to scale effortlessly as the number of users, donors, and blood requests increases, without compromising performance or availability.
The responsive and user-friendly interface further improves usability, making it easy for users to navigate the system during critical situations. In conclusion, Blood Bridge stands as a strong demonstration of how cloud computing and web technologies can be applied to solve real-world healthcare challenges. The project highlights the effectiveness of AWS services in building scalable, secure, and impactful applications. With further enhancements such as mobile integration, advanced search filters, and hospital-side dashboards, Blood Bridge has the potential to evolve into a comprehensive digital platform capable of significantly improving emergency blood management and saving lives at scale.
 

