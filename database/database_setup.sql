-- database/database_setup.sql
-- MySQL 8+ script for Momo-SMS DB implementation (matches ERD: Users, Channels, Transactions, Transaction_Categories, Assignments, System_Logs)
-- Usage: mysql -u <user> -p < database_setup.sql

CREATE DATABASE IF NOT EXISTS momo_sms CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE momo_sms;

-- USERS
CREATE TABLE IF NOT EXISTS users (
  user_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'PK: user identifier',
  name VARCHAR(200) NOT NULL COMMENT 'Full name',
  phone VARCHAR(32) NOT NULL UNIQUE COMMENT 'E.164 or normalized local format',
  email VARCHAR(200) DEFAULT NULL COMMENT 'Email (optional)',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Record creation timestamp',
  INDEX idx_users_phone (phone)
) ENGINE=InnoDB;

-- CHANNELS (represents source channel e.g., SMS, USSD, Merchant)
CREATE TABLE IF NOT EXISTS channels (
  channel_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'PK: channel identifier',
  channel_name VARCHAR(120) NOT NULL COMMENT 'Channel name (e.g., MoMo SMS, USSD, Merchant)',
  description VARCHAR(255) DEFAULT NULL COMMENT 'Optional description',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_channel_name (channel_name)
) ENGINE=InnoDB;

-- TRANSACTION CATEGORIES (lookup)
CREATE TABLE IF NOT EXISTS transaction_categories (
  category_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'PK: transaction category',
  category_name VARCHAR(100) NOT NULL COMMENT 'Display name (e.g., merchant, airtime)',
  code VARCHAR(64) NOT NULL UNIQUE COMMENT 'Short code for programmatic use',
  description VARCHAR(255) DEFAULT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_category_code (code)
) ENGINE=InnoDB;

-- TRANSACTIONS (core)
CREATE TABLE IF NOT EXISTS transactions (
  transaction_id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT 'PK: transaction id',
  momo_txn_id VARCHAR(128) UNIQUE COMMENT 'Original MoMo transaction id if present',
  sender_user_id INT DEFAULT NULL COMMENT 'FK -> users.user_id (sender)',
  receiver_user_id INT DEFAULT NULL COMMENT 'FK -> users.user_id (receiver)',
  channel_id INT DEFAULT NULL COMMENT 'FK -> channels.channel_id',
  amount_cents BIGINT NOT NULL COMMENT 'Amount stored as integer cents (no floats)',
  currency CHAR(3) DEFAULT 'KES' COMMENT 'Currency code (ISO 4217)',
  transaction_date DATETIME NOT NULL COMMENT 'When transaction occurred',
  narration VARCHAR(500) DEFAULT NULL COMMENT 'Transaction narration/text',
  balance_cents BIGINT DEFAULT NULL COMMENT 'Balance after txn (if present)',
  status ENUM('PENDING','SUCCESS','FAILED') DEFAULT 'SUCCESS' COMMENT 'Transaction status',
  raw_xml TEXT DEFAULT NULL COMMENT 'Original raw XML snippet',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  -- FK constraints
  CONSTRAINT fk_txn_sender FOREIGN KEY (sender_user_id) REFERENCES users(user_id)
    ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT fk_txn_receiver FOREIGN KEY (receiver_user_id) REFERENCES users(user_id)
    ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT fk_txn_channel FOREIGN KEY (channel_id) REFERENCES channels(channel_id)
    ON DELETE SET NULL ON UPDATE CASCADE,
  CHECK (amount_cents > 0),
  INDEX idx_txn_date (transaction_date),
  INDEX idx_sender (sender_user_id),
  INDEX idx_receiver (receiver_user_id),
  INDEX idx_channel (channel_id)
) ENGINE=InnoDB;

-- ASSIGNMENTS (junction table linking transactions <-> categories)
CREATE TABLE IF NOT EXISTS assignments (
  assignment_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'PK: assignment id',
  transaction_id BIGINT NOT NULL COMMENT 'FK -> transactions.transaction_id',
  category_id INT NOT NULL COMMENT 'FK -> transaction_categories.category_id',
  tagged_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'When category was assigned',
  CONSTRAINT uq_assignment UNIQUE (transaction_id, category_id),
  CONSTRAINT fk_assign_txn FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_assign_cat FOREIGN KEY (category_id) REFERENCES transaction_categories(category_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  INDEX idx_assign_txn (transaction_id),
  INDEX idx_assign_cat (category_id)
) ENGINE=InnoDB;

-- SYSTEM LOGS (ETL / processing logs)
CREATE TABLE IF NOT EXISTS system_logs (
  log_id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT 'PK: log identifier',
  transaction_id BIGINT DEFAULT NULL COMMENT 'Optional FK -> transactions.transaction_id',
  log_level ENUM('DEBUG','INFO','WARN','ERROR') DEFAULT 'INFO' COMMENT 'Severity level',
  message TEXT NOT NULL COMMENT 'Log message',
  log_date DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Log timestamp',
  CONSTRAINT fk_logs_txn FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
    ON DELETE SET NULL ON UPDATE CASCADE,
  INDEX idx_logs_txn (transaction_id),
  INDEX idx_logs_level (log_level)
) ENGINE=InnoDB;

-- ========== SAMPLE DATA (5+ records per main table) ==========

-- USERS (5)
INSERT INTO users (name, phone, email) VALUES
('Amina Mwangi', '+254712345001', 'amina@example.com'),
('Juma Odhiambo', '+254712345002', 'juma@example.com'),
('Grace Wanjiru', '+254712345003', 'grace@example.com'),
('Peter Kimani', '+254712345004', 'peter@example.com'),
('Lilian Njoroge', '+254712345005', 'lilian@example.com');

-- CHANNELS (5)
INSERT INTO channels (channel_name, description) VALUES
('MoMo SMS', 'Mobile money SMS ingestion channel'),
('USSD', 'USSD-based channel'),
('Merchant API', 'Merchant payments via API'),
('Voucher', 'Voucher top-up channel'),
('Agent Till', 'Agent till transactions');

-- TRANSACTION CATEGORIES (5)
INSERT INTO transaction_categories (category_name, code, description) VALUES
('Airtime Topup', 'airtime', 'Airtime purchase or transfer'),
('Merchant Payment', 'merchant', 'Payment to merchant'),
('Person-to-Person', 'p2p', 'Person to person transfer'),
('Bill Payment', 'bill', 'Utility or biller payment'),
('Refund', 'refund', 'Refunds or reversals');

-- TRANSACTIONS (5) -- ensure sender/receiver exist (IDs 1..5)
INSERT INTO transactions (momo_txn_id, sender_user_id, receiver_user_id, channel_id, amount_cents, currency, transaction_date, narration, balance_cents, status, raw_xml)
VALUES
('momo-0001', 1, 3, 1, 25000, 'KES', '2025-09-14 10:15:00', 'Payment for groceries', 150000, 'SUCCESS', '<xml>txn1</xml>'),
('momo-0002', 2, 4, 3, 500000, 'KES', '2025-09-14 11:00:00', 'Merchant payment - cafe', 70000, 'SUCCESS', '<xml>txn2</xml>'),
('momo-0003', 3, 2, 1, 10000, 'KES', '2025-09-13 09:05:00', 'Airtime topup', 90000, 'SUCCESS', '<xml>txn3</xml>'),
('momo-0004', 4, 1, 2, 75000, 'KES', '2025-09-12 16:20:00', 'Bill payment - water', 250000, 'SUCCESS', '<xml>txn4</xml>'),
('momo-0005', 5, 2, 5, 120000, 'KES', '2025-09-11 08:45:00', 'Transfer to Juma', 180000, 'SUCCESS', '<xml>txn5</xml>');

-- ASSIGNMENTS (map txns -> categories) (5)
INSERT INTO assignments (transaction_id, category_id) VALUES
(1, 2), -- txn1 -> merchant
(1, 5), -- txn1 -> refund (example multi-tag)
(2, 2),
(3, 1),
(4, 4);

-- SYSTEM LOGS (5)
INSERT INTO system_logs (transaction_id, log_level, message) VALUES
(1,'INFO','Parsed successfully'),
(2,'INFO','Parsed successfully'),
(3,'WARN','Missing optional field: balance'),
(NULL,'ERROR','Dead_letter: unparsed snippet saved'),
(5,'INFO','Categorized as p2p');

-- Script end
