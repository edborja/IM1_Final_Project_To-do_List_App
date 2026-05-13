# 🚀 CCCS105 Project: Final Completion Checklist

This list outlines the remaining tasks needed to fulfill the project requirements for the **Python Based Database Application**.

## 1. Documentation & Diagrams (High Priority)
The rubric allocates **20 points** to Database Design and **15 points** to Documentation.
- [ ] **Generate ERD Image:** Copy the Mermaid code from `README.md`, paste it into [Mermaid Live Editor](https://mermaid.live/), and save the PNG as `docs/diagrams/erd.png`.
- [ ] **Generate Relational Model Image:** Do the same for the Relational Model code and save as `docs/diagrams/rm.png`.
- [ ] **Update Team Table:** Open `README.md` and replace the `[INSERT NAME]` placeholders with the actual names and roles of the 3 group members.
- [ ] **Video Presentation:** Record a 10-15 minute walkthrough of the app and database design.
- [ ] **Add Video Link:** Paste the link to your video (YouTube/Google Drive) into the designated section at the bottom of `README.md`.

## 2. Technical Setup (For Teammates)
Every group member needs to do this to run the app locally:
- [ ] **XAMPP:** Start Apache and MySQL.
- [ ] **Database:** Create a database named `CCCS105` in phpMyAdmin.
- [ ] **Import SQL:** Import `database/schema.sql` first, then `database/initial_data.sql`.
- [ ] **SSL Certificates:** Run the `mkcert` commands (or use the provided `.pem` files) to ensure the app runs on `https://127.0.0.1:5000`.
- [ ] **Email Setup:** Each member should create a Google App Password and put it in their local `.env` to test the "Forgot Password" feature.

## 3. Code & Features (Optional "Bonus" Tasks)
To ensure an "Exemplary" grade in the **Application Functionality (25 pts)** category:
- [ ] **Data Export:** Add a feature to download tasks as a CSV file (Requirement: *"Users will be able to export query results"*).
- [ ] **Verification:** Double-check that all CRUD operations (Create, Read, Update, Delete) work without any console errors.

## 4. Final Submission Security
- [ ] **Protect Secrets:** Ensure the `.env` file is **NOT** committed to GitHub. The `.gitignore` is already set up to prevent this, but double-check before the final push!

---
**Status Note:** The database currently has the required **50 records per table** included in the `initial_data.sql` file.
