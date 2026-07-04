-- Create Database
CREATE DATABASE vehicle_db;
USE vehicle_db;

-- Admin Table
CREATE TABLE admin (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50),
    password VARCHAR(50)
);

INSERT INTO admin (username, password)
VALUES ('admin', 'admin123');

-- Owner Table
CREATE TABLE owner (
    owner_id INT PRIMARY KEY AUTO_INCREMENT,
    owner_name VARCHAR(100),
    phone VARCHAR(20) UNIQUE,
    address VARCHAR(200)
);

-- Vehicle Table
CREATE TABLE vehicle (
    vehicle_id INT PRIMARY KEY AUTO_INCREMENT,
    vehicle_no VARCHAR(20) UNIQUE,
    owner_id INT,
    vehicle_type VARCHAR(50),
    model VARCHAR(100),
    reg_date DATE,
    FOREIGN KEY (owner_id) REFERENCES owner(owner_id)
);

-- Sample Data
INSERT INTO owner (owner_name, phone, address) VALUES
('Ravi Kumar', '9876543210', 'Chennai'),
('Arun Kumar', '9123456780', 'Coimbatore'),
('Suresh Babu', '9988776655', 'Madurai'),
('Karthik', '9012345678', 'Salem'),
('Vignesh', '9345678901', 'Trichy'),
('Dinesh', '9871234560', 'Erode'),
('Prakash', '9786543210', 'Tirunelveli'),
('Manoj', '9654321780', 'Vellore'),
('Ajith', '9123987654', 'Thanjavur'),
('Surya', '9876541230', 'Kanchipuram'),
('Rajesh', '9988123456', 'Chengalpattu'),
('Deepak', '9345612780', 'Nagapattinam'),
('Naveen', '9876501234', 'Cuddalore'),
('Harish', '9789012345', 'Dharmapuri'),
('Gokul', '9654781230', 'Krishnagiri'),
('Vinoth', '9123678901', 'Karur'),
('Bala', '9876123450', 'Dindigul'),
('Ramesh', '9345126789', 'Perambalur'),
('Kiran', '9987012345', 'Pudukkottai'),
('Sathish', '9123456700', 'Thoothukudi');