import mysql.connector

cnx = mysql.connector.connect(host='localhost', user='root', passwd='Bcawala@123')
cnx.autocommit = True
cur = cnx.cursor()
cur.execute('CREATE DATABASE IF NOT EXISTS user_db')
cur.execute('USE user_db')
cur.execute(
    '''CREATE TABLE IF NOT EXISTS visitors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ip_address VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )'''
)
cur.execute(
    '''CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255),
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255)
    )'''
)
cur.execute(
    '''CREATE TABLE IF NOT EXISTS admin_credentials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255),
    Gender VARCHAR(50),
    Country VARCHAR(100),
    Address TEXT,
    Phone VARCHAR(50),
    email VARCHAR(255),
    password VARCHAR(255)
    )'''
)
cur.execute(
    '''CREATE TABLE IF NOT EXISTS comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )'''
)
cur.execute(
    '''CREATE TABLE IF NOT EXISTS likes_dislikes (
    id INT PRIMARY KEY,
    likes INT DEFAULT 0,
    dislikes INT DEFAULT 0
    )'''
)
cur.execute(
    '''CREATE TABLE IF NOT EXISTS test_report (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    MDVP_Fo_Hz FLOAT,
    MDVP_Fhi_Hz FLOAT,
    MDVP_Flo_Hz FLOAT,
    MDVP_Jitter_percent FLOAT,
    MDVP_Shimmer FLOAT,
    NHR FLOAT,
    RPDE FLOAT,
    DFA FLOAT,
    spread1 FLOAT,
    spread2 FLOAT,
    D2 FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )'''
)
cur.execute(
    'INSERT INTO likes_dislikes (id, likes, dislikes) VALUES (1, 0, 0) ON DUPLICATE KEY UPDATE likes=likes, dislikes=dislikes'
)
cur.close()
cnx.close()
print('Database and tables created successfully')
