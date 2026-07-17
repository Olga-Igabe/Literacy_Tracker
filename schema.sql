CREATE DATABASE IF NOT EXISTS community_tracker;
USE community_tracker;

-- 1. Members Table
CREATE TABLE IF NOT EXISTS members (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    contact VARCHAR(100),
    age_group ENUM('Child', 'Youth', 'Adult') NOT NULL,
    guardian_name VARCHAR(255) DEFAULT NULL,
    guardian_contact VARCHAR(100) DEFAULT NULL
);

-- 2. Member Progress / Skills Table
CREATE TABLE IF NOT EXISTS member_progress (
    progress_id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT,
    skill_name VARCHAR(255) NOT NULL,
    status ENUM('Not Started', 'In Progress', 'Completed') DEFAULT 'Not Started',
    FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE,
    UNIQUE KEY unique_member_skill (member_id, skill_name)
);

-- 3. Devices Table
CREATE TABLE IF NOT EXISTS devices (
    device_id INT AUTO_INCREMENT PRIMARY KEY,
    device_name VARCHAR(255) NOT NULL,
    type VARCHAR(100) NOT NULL, -- e.g., laptop, tablet, router
    device_condition VARCHAR(100) NOT NULL,
    status ENUM('Available', 'On Loan') DEFAULT 'Available'
);

-- 4. Loans Table
CREATE TABLE IF NOT EXISTS loans (
    loan_id INT AUTO_INCREMENT PRIMARY KEY,
    device_id INT,
    member_id INT,
    date_borrowed DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE DEFAULT NULL,s
    guardian_name VARCHAR(255) DEFAULT NULL,
    guardian_contact VARCHAR(100) DEFAULT NULL,
    FOREIGN KEY (device_id) REFERENCES devices(device_id),
    FOREIGN KEY (member_id) REFERENCES members(member_id)
);

-- 5. Workshops Table
CREATE TABLE IF NOT EXISTS workshops (
    workshop_id INT AUTO_INCREMENT PRIMARY KEY,
    workshop_name VARCHAR(255) NOT NULL,
    workshop_date DATE NOT NULL,
    topic VARCHAR(255) NOT NULL
);

-- 6. Workshop Attendance Table
CREATE TABLE IF NOT EXISTS workshop_attendance (
    attendance_id INT AUTO_INCREMENT PRIMARY KEY,
    workshop_id INT,
    member_id INT,
    FOREIGN KEY (workshop_id) REFERENCES workshops(workshop_id) ON DELETE CASCADE,
    FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE
);
