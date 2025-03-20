-- CREATE DATABASE IF NOT EXISTS flask_app_db;
-- USE flask_app_db;

-- CREATE TABLE IF NOT EXISTS users (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     name VARCHAR(100) NOT NULL,
--     email VARCHAR(100) UNIQUE NOT NULL
-- );
CREATE DATABASE IF NOT EXISTS flask_app_db;
USE flask_app_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    branch VARCHAR(50),
    age INT,
    sex ENUM('Male', 'Female', 'Other')
);
