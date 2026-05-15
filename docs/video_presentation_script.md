# Video Presentation Script: CCCS 105 Final Project
**Duration**: 10-15 Minutes
**Project**: Student To-Do List Application (with Pomodoro & Analytics)

---

## 1. Introduction (0:00 - 2:00)
**[Action: Show the Landing Page / Login Screen]**
*   "Hello everyone! We are [Team Names], and today we’re excited to present our Final Project for Information Management 1: A Python-based Database Application."
*   "Our project is a specialized To-Do List application designed for students. We built this to solve the common problem of academic burnout by combining task management with the Pomodoro technique and data analytics."
*   "Our tech stack includes **Python 3**, **Flask** for the web framework, and **MySQL** via XAMPP for our relational database management."

## 2. Demonstration of Features (2:00 - 7:00)
**[Action: Show Google/Facebook Login]**
*   "Security is a priority, so we implemented User Authentication. Beyond standard login, we integrated **Google and Facebook OAuth**. This allows users to sign in securely using their existing accounts."

**[Action: Show the Dashboard / Task List]**
*   "Once logged in, you see our main Dashboard. This is a live view of our `task` and `category` tables. We have implemented full **CRUD operations** here."
*   "I can **Create** a new task, assign it a **Category** like 'Math' or 'Science', and set a **Priority**. You’ll notice the icons change automatically based on the subject name—that’s our custom logic at work."
*   "We can **Update** tasks by clicking them, and **Delete** them with a single click. Every change is instantly synced to our MySQL database."

**[Action: Show the Focus Button / Pomodoro]**
*   "One unique feature is our **Focus Mode**. By clicking the tomato icon, users can start a Pomodoro timer. This tracks study sessions directly in the `pomodoro` table, which we later use for analytics."

**[Action: Show Export Button]**
*   "Finally, for the **Data Export** requirement, we added a CSV export feature. This generates a report of all tasks, including subtask completion percentages, which is perfect for students who want to track their progress offline."

## 3. Database Design (7:00 - 9:00)
**[Action: Show docs/diagrams/erd.png]**
*   "Our database follows a normalized relational structure. We have 5 main tables: `User`, `Task`, `Category`, `Subtask`, and `Pomodoro`."
*   "We enforced **Referential Integrity** using Foreign Keys. For example, if a user deletes their account, all their tasks and pomodoro sessions are automatically cleaned up via `ON DELETE CASCADE`."
*   "We also ensured our `password_hash` column is **255 characters long**. This is a critical design choice to support modern, high-security hashing algorithms like `scrypt`."

## 4. Challenges Faced (9:00 - 12:00)
**[Action: Show some code in src/auth/__init__.py]**
*   "One major challenge was handling **OAuth edge cases**. We found that some Facebook accounts don't provide an email address. We overcame this by implementing a fallback system that generates a unique internal email, ensuring the user can still log in without crashing the system."
*   "Another challenge was a **Database Truncation bug**. Initially, our password hashes were being cut off at 128 characters, causing login failures. We diagnosed this by analyzing the database logs and fixed it by altering the MySQL table schema to 255 characters."

## 5. Conclusion & Future Improvements (12:00 - 15:00)
*   "In conclusion, we’ve built a fully functional CRUD application that meets all project requirements, including secure authentication and data export."
*   "For future improvements, we'd like to implement **Push Notifications** and a **Mobile App** version to help students stay on track even when they're away from their computers."
*   "Thank you for your time!"

---

### **Speaker Notes:**
*   **Speak slowly and clearly.**
*   **Make sure XAMPP is running** before you start!
*   **Show the database in phpMyAdmin** during the "Database Design" section to prove you have 50+ records!
