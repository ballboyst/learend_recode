-- データベースの作成
CREATE DATABASE IF NOT EXISTS todo_db;

-- ユーザーの作成
CREATE USER IF NOT EXISTS 'admin'@'%' IDENTIFIED BY 'admin';

-- 権限の付与
GRANT ALL PRIVILEGES ON todo_db.* TO 'admin'@'%';


USE todo_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description text ,
    done bool
    FOREIGN KEY(uid) REFERENCES users(id)
);

