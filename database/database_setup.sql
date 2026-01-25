-- MoMo SMS Transaction Database Setup
-- Database schema for mobile money transaction processing

DROP DATABASE IF EXISTS momo_sms_db;
CREATE DATABASE momo_sms_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE momo_sms_db;

-- Users Table
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    phone_number VARCHAR(15) NOT NULL UNIQUE COMMENT 'User phone number',
    full_name VARCHAR(100) COMMENT 'Full name',
    email VARCHAR(100) COMMENT 'Email address',
    registration_date DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Registration date',
    account_status ENUM('active', 'suspended', 'closed') DEFAULT 'active' COMMENT 'Account status',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_phone (phone_number),
    INDEX idx_status (account_status)
) ENGINE=InnoDB COMMENT='Customer information';

-- Transaction_Categories Table
CREATE TABLE Transaction_Categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL UNIQUE COMMENT 'Category name',
    description TEXT COMMENT 'Category description',
    is_active BOOLEAN DEFAULT TRUE COMMENT 'Active status',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_name (category_name)
) ENGINE=InnoDB COMMENT='Transaction type classifications';

-- Transactions Table
CREATE TABLE Transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    reference VARCHAR(50) NOT NULL UNIQUE COMMENT 'Transaction reference',
    sender_id INT NOT NULL COMMENT 'Sender user ID',
    receiver_id INT NOT NULL COMMENT 'Receiver user ID',
    category_id INT NOT NULL COMMENT 'Transaction category',
    amount DECIMAL(15, 2) NOT NULL COMMENT 'Transaction amount',
    currency VARCHAR(3) DEFAULT 'SZL' COMMENT 'Currency code',
    status ENUM('pending', 'completed', 'failed', 'reversed') DEFAULT 'pending' COMMENT 'Transaction status',
    transaction_date DATETIME NOT NULL COMMENT 'Transaction date',
    description TEXT COMMENT 'Transaction description',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_sender FOREIGN KEY (sender_id) 
        REFERENCES Users(user_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_receiver FOREIGN KEY (receiver_id) 
        REFERENCES Users(user_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_category FOREIGN KEY (category_id) 
        REFERENCES Transaction_Categories(category_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    
    CONSTRAINT chk_amount CHECK (amount > 0),
    
    INDEX idx_sender (sender_id),
    INDEX idx_receiver (receiver_id),
    INDEX idx_date (transaction_date),
    INDEX idx_status (status)
) ENGINE=InnoDB COMMENT='Transaction records';

-- System_Logs Table
CREATE TABLE System_Logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    log_level ENUM('INFO', 'WARNING', 'ERROR', 'CRITICAL') NOT NULL COMMENT 'Log severity',
    log_message TEXT NOT NULL COMMENT 'Log message',
    event_type VARCHAR(50) COMMENT 'Event type',
    source_module VARCHAR(100) COMMENT 'Source module',
    error_code VARCHAR(20) COMMENT 'Error code',
    stack_trace TEXT COMMENT 'Stack trace',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Log timestamp',
    
    INDEX idx_level (log_level),
    INDEX idx_event (event_type),
    INDEX idx_created (created_at)
) ENGINE=InnoDB COMMENT='System activity logs';

-- User_Logs Junction Table (M:N Relationship)
CREATE TABLE User_Logs (
    user_log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL COMMENT 'User ID',
    log_id INT NOT NULL COMMENT 'Log ID',
    user_action VARCHAR(100) COMMENT 'User action',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_user FOREIGN KEY (user_id) 
        REFERENCES Users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_log FOREIGN KEY (log_id) 
        REFERENCES System_Logs(log_id) ON DELETE CASCADE ON UPDATE CASCADE,
    
    UNIQUE KEY uk_user_log (user_id, log_id),
    
    INDEX idx_user (user_id),
    INDEX idx_log (log_id)
) ENGINE=InnoDB COMMENT='User-Log mapping (M:N)';

-- Insert Categories
INSERT INTO Transaction_Categories (category_name, description) VALUES
('SEND', 'Send money to another user'),
('RECEIVE', 'Receive money from another user'),
('DEPOSIT', 'Deposit money into account'),
('WITHDRAW', 'Withdraw money from account'),
('PAYMENT', 'Payment for goods or services');

-- Insert Users
INSERT INTO Users (phone_number, full_name, email, account_status) VALUES
('0791234567', 'John Doe', 'john.doe@example.com', 'active'),
('0797654321', 'Jane Smith', 'jane.smith@example.com', 'active'),
('0798888888', 'Alice Johnson', 'alice.j@example.com', 'active'),
('0795555555', 'Bob Williams', 'bob.w@example.com', 'active'),
('0796666666', 'Charlie Brown', 'charlie.b@example.com', 'active'),
('0793333333', 'Diana Prince', 'diana.p@example.com', 'active'),
('BANK', 'Bank System', 'support@bank.com', 'active');

-- Insert Transactions
INSERT INTO Transactions (reference, sender_id, receiver_id, category_id, amount, status, transaction_date, description) VALUES
('TXN000001', 1, 2, 1, 5000.00, 'completed', '2024-01-15 10:30:00', 'Monthly allowance'),
('TXN000002', 2, 1, 2, 3500.00, 'completed', '2024-01-15 11:45:00', 'Payment received'),
('TXN000003', 1, 7, 3, 10000.00, 'completed', '2024-01-15 14:20:00', 'Salary deposit'),
('TXN000004', 1, 3, 5, 1500.00, 'completed', '2024-01-16 16:30:00', 'Shopping payment'),
('TXN000005', 1, 3, 1, 8000.00, 'completed', '2024-01-17 08:00:00', 'Loan repayment'),
('TXN000006', 4, 1, 2, 4200.00, 'completed', '2024-01-17 12:30:00', 'Service payment'),
('TXN000007', 5, 6, 1, 2500.00, 'completed', '2024-01-18 09:00:00', 'Transfer');

-- Insert System Logs
INSERT INTO System_Logs (log_level, log_message, event_type, source_module) VALUES
('INFO', 'ETL process started', 'ETL', 'etl.run'),
('INFO', 'Database connection established', 'DATABASE', 'api.db'),
('WARNING', 'High transaction volume', 'MONITORING', 'system.monitor'),
('ERROR', 'XML parse failed', 'ETL', 'etl.parse_xml'),
('INFO', 'API server started', 'API', 'api.rest_server'),
('CRITICAL', 'Database connection lost', 'DATABASE', 'api.db'),
('INFO', 'Backup completed', 'BACKUP', 'system.backup');

-- Insert User-Log Mappings
INSERT INTO User_Logs (user_id, log_id, user_action) VALUES
(1, 1, 'Initiated ETL'),
(1, 4, 'Parse failed'),
(2, 3, 'Multiple transactions'),
(1, 6, 'Connection lost'),
(3, 5, 'API request'),
(4, 7, 'Backup included');

-- CRUD Operations

-- CREATE
INSERT INTO Transactions (reference, sender_id, receiver_id, category_id, amount, status, transaction_date, description)
VALUES ('TXN000008', 2, 3, 1, 1200.00, 'completed', NOW(), 'Test transaction');

-- READ
SELECT t.transaction_id, t.reference, u1.full_name AS sender, u2.full_name AS receiver, 
       tc.category_name, t.amount, t.status
FROM Transactions t
JOIN Users u1 ON t.sender_id = u1.user_id
JOIN Users u2 ON t.receiver_id = u2.user_id
JOIN Transaction_Categories tc ON t.category_id = tc.category_id
WHERE t.reference = 'TXN000008';

-- UPDATE
UPDATE Transactions 
SET status = 'completed', description = 'Updated test'
WHERE reference = 'TXN000008';

-- DELETE
DELETE FROM Transactions WHERE reference = 'TXN000008';

-- Sample Queries

-- Query 1: User transactions
SELECT t.reference, u_sender.full_name AS sender, u_receiver.full_name AS receiver,
       tc.category_name, t.amount, t.status, t.transaction_date
FROM Transactions t
JOIN Users u_sender ON t.sender_id = u_sender.user_id
JOIN Users u_receiver ON t.receiver_id = u_receiver.user_id
JOIN Transaction_Categories tc ON t.category_id = tc.category_id
WHERE u_sender.phone_number = '0791234567'
ORDER BY t.transaction_date DESC;

-- Query 2: Category totals
SELECT tc.category_name, COUNT(*) AS count, SUM(t.amount) AS total, AVG(t.amount) AS average
FROM Transactions t
JOIN Transaction_Categories tc ON t.category_id = tc.category_id
GROUP BY tc.category_name
ORDER BY total DESC;

-- Query 3: System errors with users
SELECT sl.log_level, sl.log_message, sl.created_at,
       GROUP_CONCAT(u.full_name SEPARATOR ', ') AS affected_users
FROM System_Logs sl
LEFT JOIN User_Logs ul ON sl.log_id = ul.log_id
LEFT JOIN Users u ON ul.user_id = u.user_id
WHERE sl.log_level IN ('ERROR', 'CRITICAL')
GROUP BY sl.log_id
ORDER BY sl.created_at DESC;

-- Security Rules

-- Trigger: Log inserts
DELIMITER //
CREATE TRIGGER trg_log_insert
AFTER INSERT ON Transactions
FOR EACH ROW
BEGIN
    INSERT INTO System_Logs (log_level, log_message, event_type, source_module)
    VALUES ('INFO', CONCAT('Transaction ', NEW.reference, ' created'), 'TRANSACTION', 'trigger');
END//
DELIMITER ;

-- Trigger: Prevent deletion of completed transactions
DELIMITER //
CREATE TRIGGER trg_prevent_delete
BEFORE DELETE ON Transactions
FOR EACH ROW
BEGIN
    IF OLD.status = 'completed' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot delete completed transactions';
    END IF;
END//
DELIMITER ;

-- View: Active users
CREATE VIEW vw_active_users AS
SELECT u.user_id, u.phone_number, u.full_name, u.account_status,
       COUNT(DISTINCT t.transaction_id) AS total_transactions,
       COALESCE(SUM(CASE WHEN t.sender_id = u.user_id THEN t.amount ELSE 0 END), 0) AS total_sent,
       COALESCE(SUM(CASE WHEN t.receiver_id = u.user_id THEN t.amount ELSE 0 END), 0) AS total_received
FROM Users u
LEFT JOIN Transactions t ON u.user_id = t.sender_id OR u.user_id = t.receiver_id
WHERE u.account_status = 'active'
GROUP BY u.user_id;

-- Verification
SHOW TABLES;
SELECT * FROM vw_active_users;
