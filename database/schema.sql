
CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE category (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    color VARCHAR(7) DEFAULT '#3498db',
    icon VARCHAR(20) DEFAULT '📚',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

CREATE TABLE task (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(140) NOT NULL,
    description TEXT,
    notes TEXT,
    link VARCHAR(500),
    priority VARCHAR(20) DEFAULT 'Medium',
    due_date DATETIME,
    is_completed BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_recurring BOOLEAN DEFAULT 0,
    recurrence_pattern VARCHAR(20),
    recurrence_end DATETIME,
    user_id INT NOT NULL,
    category_id INT,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES category(id)
);

CREATE TABLE subtask (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(140) NOT NULL,
    is_completed BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    task_id INT NOT NULL,
    FOREIGN KEY (task_id) REFERENCES task(id) ON DELETE CASCADE
);

CREATE TABLE pomodoro (
    id INT AUTO_INCREMENT PRIMARY KEY,
    duration INT DEFAULT 25,
    completed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    was_completed BOOLEAN DEFAULT 1,
    user_id INT NOT NULL,
    task_id INT,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (task_id) REFERENCES task(id) ON DELETE CASCADE
);
