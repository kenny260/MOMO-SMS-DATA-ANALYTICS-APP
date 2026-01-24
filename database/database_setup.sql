-- =====================================================
-- MoMo SMS Database Setup
-- =====================================================

-- Drop and recreate database
DROP DATABASE IF EXISTS momo_sms_db;
CREATE DATABASE momo_sms_db;
USE momo_sms_db;

-- ======================
-- USERS / CUSTOMERS
-- ======================
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique user identifier',
    full_name VARCHAR(100) NOT NULL COMMENT 'Customer full name',
    phone_number VARCHAR(20) NOT NULL UNIQUE COMMENT 'Registered mobile number',
    email VARCHAR(100) UNIQUE COMMENT 'Optional email address',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Account creation timestamp'
) ENGINE=InnoDB;

CREATE INDEX idx_users_phone ON users(phone_number);

-- ======================
-- TRANSACTION CATEGORIES
-- ======================
CREATE TABLE transaction_categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Category identifier',
    category_name VARCHAR(50) NOT NULL UNIQUE COMMENT 'Transaction type name',
    description VARCHAR(255) COMMENT 'Category description'
) ENGINE=InnoDB;

-- ======================
-- TRANSACTIONS
-- ======================
CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Transaction identifier',
    sender_id INT NOT NULL COMMENT 'FK to users (sender)',
    receiver_id INT NOT NULL COMMENT 'FK to users (receiver)',
    category_id INT NOT NULL COMMENT 'FK to transaction category',
    amount DECIMAL(10,2) NOT NULL COMMENT 'Transaction amount',
    currency CHAR(3) NOT NULL DEFAULT 'RWF' COMMENT 'Transaction currency',
    status VARCHAR(20) NOT NULL COMMENT 'Transaction status',
    transaction_date DATETIME NOT NULL COMMENT 'Date of transaction',
    reference_code VARCHAR(50) NOT NULL UNIQUE COMMENT 'Unique transaction reference',

    CONSTRAINT fk_sender FOREIGN KEY (sender_id) REFERENCES users(user_id),
    CONSTRAINT fk_receiver FOREIGN KEY (receiver_id) REFERENCES users(user_id),
    CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES transaction_categories(category_id),

    CONSTRAINT chk_amount CHECK (amount > 0),
    CONSTRAINT chk_status CHECK (status IN ('SUCCESS', 'FAILED', 'PENDING'))
) ENGINE=InnoDB;

CREATE INDEX idx_transactions_date ON transactions(transaction_date);
CREATE INDEX idx_transactions_sender ON transactions(sender_id);

-- ======================
-- SYSTEM LOGS
-- ======================
CREATE TABLE system_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Log entry identifier',
    transaction_id INT COMMENT 'Related transaction (optional)',
    log_level VARCHAR(20) NOT NULL COMMENT 'INFO, WARNING, ERROR',
    message TEXT NOT NULL COMMENT 'Log message details',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Log timestamp',

    CONSTRAINT fk_log_transaction FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id),
    CONSTRAINT chk_log_level CHECK (log_level IN ('INFO', 'WARNING', 'ERROR'))
) ENGINE=InnoDB;

-- ======================
-- SAMPLE DATA INSERTION
-- ======================

-- Users
INSERT INTO users (full_name, phone_number, email) VALUES
('Alice Mukamana', '250788111111', 'alice@example.com'),
('Bob Nkurunziza', '250788222222', 'bob@example.com'),
('Charles Uwimana', '250788333333', NULL),
('Diane Uwamahoro', '250788444444', 'diane@example.com'),
('Eric Habimana', '250788555555', NULL);

-- Categories
INSERT INTO transaction_categories (category_name, description) VALUES
('P2P Transfer', 'Peer to peer transfer'),
('Merchant Payment', 'Payment to merchant'),
('Airtime Purchase', 'Mobile airtime top-up'),
('Bill Payment', 'Utility bill payment'),
('Bank Transfer', 'Transfer to bank account');

-- Transactions
INSERT INTO transactions (sender_id, receiver_id, category_id, amount, status, transaction_date, reference_code) VALUES
(1, 2, 1, 5000.00, 'SUCCESS', '2026-01-10 10:15:00', 'TXN001'),
(2, 3, 1, 12000.00, 'SUCCESS', '2026-01-11 11:30:00', 'TXN002'),
(3, 4, 2, 8000.00, 'FAILED', '2026-01-12 09:45:00', 'TXN003'),
(4, 5, 3, 1500.00, 'SUCCESS', '2026-01-13 14:00:00', 'TXN004'),
(5, 1, 4, 20000.00, 'PENDING', '2026-01-14 16:20:00', 'TXN005');

-- System Logs
INSERT INTO system_logs (transaction_id, log_level, message) VALUES
(1, 'INFO', 'Transaction processed successfully'),
(2, 'INFO', 'Transaction completed'),
(3, 'ERROR', 'Insufficient balance'),
(4, 'INFO', 'Airtime purchase successful'),
(5, 'WARNING', 'Transaction pending confirmation');

-- ======================
-- CRUD TEST QUERIES (for screenshots)
-- ======================

-- READ
SELECT * FROM transactions;

-- UPDATE
UPDATE transactions SET status = 'SUCCESS' WHERE transaction_id = 5;

-- DELETE
DELETE FROM system_logs WHERE log_id = 5;

-- INSERT
INSERT INTO system_logs (transaction_id, log_level, message)
VALUES (1, 'INFO', 'Audit log inserted manually');
