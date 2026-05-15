import os
from werkzeug.security import generate_password_hash
from faker import Faker
import random
from datetime import datetime, timedelta

def generate_schema():
    print("Generating schema.sql...")
    schema = """
CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(128),
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
"""
    with open('database/schema.sql', 'w', encoding='utf-8') as f:
        f.write(schema)

def generate_data():
    print("Generating initial_data.sql...")
    fake = Faker()
    
    with open('database/initial_data.sql', 'w', encoding='utf-8') as f:
        f.write("USE CCCS105;\n\n")
        
        # Generate 50 Users
        f.write("-- Users\n")
        user_ids = list(range(1, 51))
        for i in user_ids:
            username = fake.user_name() + str(i)
            email = fake.email()
            password_hash = generate_password_hash('password123')
            f.write(f"INSERT INTO user (id, username, email, password_hash, created_at) VALUES ({i}, '{username}', '{email}', '{password_hash}', NOW());\n")
            
        f.write("\n-- Categories\n")
        # Generate 50 Categories (assigned to random users)
        category_ids = list(range(1, 51))
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f1c40f', '#9b59b6']
        for i in category_ids:
            name = fake.word().capitalize()
            color = random.choice(colors)
            user_id = random.choice(user_ids)
            f.write(f"INSERT INTO category (id, name, color, icon, user_id, created_at) VALUES ({i}, '{name}', '{color}', '📁', {user_id}, NOW());\n")
            
        f.write("\n-- Tasks\n")
        # Generate 50 Tasks
        task_ids = list(range(1, 51))
        for i in task_ids:
            title = fake.sentence(nb_words=4).replace("'", "''")
            desc = fake.sentence(nb_words=10).replace("'", "''")
            priority = random.choice(['Low', 'Medium', 'High'])
            is_completed = random.choice([0, 1])
            user_id = random.choice(user_ids)
            category_id = random.choice(category_ids)
            f.write(f"INSERT INTO task (id, title, description, priority, is_completed, user_id, category_id, created_at) VALUES ({i}, '{title}', '{desc}', '{priority}', {is_completed}, {user_id}, {category_id}, NOW());\n")
            
        f.write("\n-- Subtasks\n")
        # Generate 50 Subtasks
        subtask_ids = list(range(1, 51))
        for i in subtask_ids:
            title = fake.sentence(nb_words=3).replace("'", "''")
            is_completed = random.choice([0, 1])
            task_id = random.choice(task_ids)
            f.write(f"INSERT INTO subtask (id, title, is_completed, task_id, created_at) VALUES ({i}, '{title}', {is_completed}, {task_id}, NOW());\n")
            
        f.write("\n-- Pomodoros\n")
        # Generate 50 Pomodoros
        pomodoro_ids = list(range(1, 51))
        for i in pomodoro_ids:
            duration = random.choice([25, 50])
            user_id = random.choice(user_ids)
            task_id = random.choice(task_ids)
            f.write(f"INSERT INTO pomodoro (id, duration, user_id, task_id, completed_at) VALUES ({i}, {duration}, {user_id}, {task_id}, NOW());\n")

if __name__ == '__main__':
    generate_schema()
    generate_data()
    print("Database files generated successfully in database/")
