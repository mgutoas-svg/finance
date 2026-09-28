-- Create tables for Financial Management System

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    recovery_email VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Categories table
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_custom BOOLEAN DEFAULT FALSE,
    ideal_percentage FLOAT DEFAULT 0,
    alert_percentage FLOAT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Transactions table
CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    description VARCHAR(255) NOT NULL,
    amount FLOAT NOT NULL,
    transaction_date TIMESTAMP NOT NULL,
    transaction_type VARCHAR(10) NOT NULL,
    source VARCHAR(100),
    source_file_id INTEGER,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- File uploads table
CREATE TABLE IF NOT EXISTS file_uploads (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(10) NOT NULL,
    status VARCHAR(20) DEFAULT 'processing',
    records_imported INTEGER DEFAULT 0,
    error_message TEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Goals table
CREATE TABLE IF NOT EXISTS goals (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    target_amount FLOAT NOT NULL,
    current_amount FLOAT DEFAULT 0,
    frequency VARCHAR(20) NOT NULL,
    due_date TIMESTAMP,
    category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Audit logs table
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    resource_id INTEGER,
    old_values TEXT,
    new_values TEXT,
    ip_address VARCHAR(50),
    user_agent VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON transactions(user_id);
CREATE INDEX IF NOT EXISTS idx_transactions_category_id ON transactions(category_id);
CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(transaction_date);
CREATE INDEX IF NOT EXISTS idx_categories_user_id ON categories(user_id);
CREATE INDEX IF NOT EXISTS idx_goals_user_id ON goals(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON audit_logs(created_at);

-- Insert default categories for first user
INSERT INTO categories (user_id, name, ideal_percentage, alert_percentage, is_custom)
SELECT 1, 'Alimentação', 15, 18, FALSE
WHERE NOT EXISTS (SELECT 1 FROM categories WHERE user_id = 1 AND name = 'Alimentação');

INSERT INTO categories (user_id, name, ideal_percentage, alert_percentage, is_custom)
SELECT 1, 'Transporte', 15, 18, FALSE
WHERE NOT EXISTS (SELECT 1 FROM categories WHERE user_id = 1 AND name = 'Transporte');

INSERT INTO categories (user_id, name, ideal_percentage, alert_percentage, is_custom)
SELECT 1, 'Saúde', 5, 6, FALSE
WHERE NOT EXISTS (SELECT 1 FROM categories WHERE user_id = 1 AND name = 'Saúde');

INSERT INTO categories (user_id, name, ideal_percentage, alert_percentage, is_custom)
SELECT 1, 'Educação', 10, 12, FALSE
WHERE NOT EXISTS (SELECT 1 FROM categories WHERE user_id = 1 AND name = 'Educação');

INSERT INTO categories (user_id, name, ideal_percentage, alert_percentage, is_custom)
SELECT 1, 'Lazer', 10, 12, FALSE
WHERE NOT EXISTS (SELECT 1 FROM categories WHERE user_id = 1 AND name = 'Lazer');

INSERT INTO categories (user_id, name, ideal_percentage, alert_percentage, is_custom)
SELECT 1, 'Compras', 10, 12, FALSE
WHERE NOT EXISTS (SELECT 1 FROM categories WHERE user_id = 1 AND name = 'Compras');

INSERT INTO categories (user_id, name, ideal_percentage, alert_percentage, is_custom)
SELECT 1, 'Utilities', 10, 12, FALSE
WHERE NOT EXISTS (SELECT 1 FROM categories WHERE user_id = 1 AND name = 'Utilities');

INSERT INTO categories (user_id, name, ideal_percentage, alert_percentage, is_custom)
SELECT 1, 'Seguros', 5, 6, FALSE
WHERE NOT EXISTS (SELECT 1 FROM categories WHERE user_id = 1 AND name = 'Seguros');

INSERT INTO categories (user_id, name, ideal_percentage, alert_percentage, is_custom)
SELECT 1, 'Investimentos', 10, 12, FALSE
WHERE NOT EXISTS (SELECT 1 FROM categories WHERE user_id = 1 AND name = 'Investimentos');

INSERT INTO categories (user_id, name, ideal_percentage, alert_percentage, is_custom)
SELECT 1, 'Outros', 0, 0, FALSE
WHERE NOT EXISTS (SELECT 1 FROM categories WHERE user_id = 1 AND name = 'Outros');
