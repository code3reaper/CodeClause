CodeClause Internship Projects 🚀
Welcome to my CodeClause Internship Projects repository! This collection showcases a series of web development applications built as part of my internship, demonstrating proficiency in Python (Flask), front-end technologies (HTML, CSS with Tailwind CSS), and JavaScript.

Each project is designed to be functional, user-friendly, and provides practical experience with common web development patterns.

📋 Table of Contents
Stylish Calculator App 🔢

Real-Time Mail Application 📧📬

URL Shortener 🔗✨

Technologies Used 🛠️

Setup and Installation ⚙️⬇️

Usage ▶️

Screenshots 📸

Contributing 🤝

License 📄

Contact ✉️

1. Stylish Calculator App ➕➖✖️➗🔢
A modern and interactive web-based calculator that handles basic arithmetic operations. Designed for a clean user experience with a responsive layout.

✨ Features:
✅ Basic Operations: Addition, subtraction, multiplication, and division.

💡 Real-time Display: Shows both the current input/result and the ongoing operation history.

🗑️ Clear & Delete: Buttons for clearing the entire input or deleting the last character.

⌨️ Keyboard Support: Fully functional with keyboard input.

📱 Responsive Design: Adapts seamlessly to different screen sizes.

💻 Technologies:
🐍 Backend: Python (Flask)

🌐 Frontend: HTML, JavaScript

🎨 Styling: Tailwind CSS

2. Real-Time Mail Application 📧📬
A simple web-based email client allowing users to configure their email settings (SMTP/IMAP), send new emails, and view incoming messages from their inbox. It also logs sent emails locally.

✨ Features:
⚙️ Email Configuration: Set up SMTP and IMAP server details, email address, and password.

✍️ Send Emails: Compose and send emails with recipients, subjects, and body content.

📥 Inbox Viewing: Fetches and displays the latest emails from your inbox.

📤 Sent Emails Log: Maintains a local log of emails you've sent.

↩️ Reply Functionality: Quickly populate the compose form to reply to received or sent emails.

🔄 Dynamic Inbox Refresh: Refresh your inbox with a click.

⚠️ Important Security Note:
For demonstration purposes, this application stores email passwords directly in a local SQLite database. In a real-world production environment, passwords must ALWAYS be securely hashed and encrypted. Using app-specific passwords from your email provider (e.g., Gmail App Passwords) is highly recommended for added security, even for testing.

💻 Technologies:
🐍 Backend: Python (Flask, smtplib, imaplib, email modules)

🗄️ Database: SQLite3 (for user configurations and sent email logs)

🌐 Frontend: HTML, JavaScript

🎨 Styling: Tailwind CSS

3. URL Shortener 🔗✨
A lightweight web service that transforms long, unwieldy URLs into concise, easy-to-share short links.

✨ Features:
✂️ URL Shortening: Generates a unique short code for any given long URL.

➡️ Redirection: Short URLs redirect seamlessly to their original long counterparts.

📋 Copy to Clipboard: Convenient button to copy the generated short URL.

🚫 Error Handling: Displays a user-friendly error page for invalid or non-existent short URLs.

⚠️ Important Data Storage Note:
For simplicity, this demo uses an in-memory dictionary (url_mappings) to store URL mappings. This means all shortened URLs will be lost when the Flask server is restarted. For a production application, you would need a persistent database (e.g., SQLite, PostgreSQL, MongoDB) to store the URL mappings permanently.

💻 Technologies:
🐍 Backend: Python (Flask, secrets module for unique code generation)

🌐 Frontend: HTML, JavaScript

🎨 Styling: Tailwind CSS

4. Technologies Used 🛠️
This repository leverages the following core technologies:

🐍 Python 3.x: The primary programming language.

🍾 Flask: A lightweight Python web framework.

📄 HTML5: For structuring web content.

🌈 CSS3: For styling, primarily using Tailwind CSS for utility-first styling.

⚙️ JavaScript: For interactive front-end functionality.

🗃️ SQLite3: A lightweight, file-based database (used by the Mail Application).

5. Setup and Installation ⚙️⬇️
To get these projects up and running on your local machine, follow these steps:

Clone the Repository:

git clone https://github.com/code3reaper/CodeClause.git
cd CodeClause

Install Python Dependencies:
Each project requires Flask. It's recommended to set up a virtual environment.

# Create a virtual environment
python -m venv venv
# Activate the virtual environment
# On Windows:
# venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

# Install Flask
pip install Flask

Note: The Mail Application also implicitly uses built-in Python modules like smtplib, imaplib, and sqlite3, which do not require separate pip installations.

6. Usage ▶️
Navigate into the respective project directory and run the app.py file.

1. Stylish Calculator App
Navigate:

cd Calculator

Run:

python app.py

Access: Open your web browser and go to http://127.0.0.1:5000/

2. Real-Time Mail Application
Navigate:

cd Mail_application

Run:

python app.py

Access: Open your web browser and go to http://127.0.0.1:5001/

First Use: You will be redirected to a configuration page where you'll enter your email details.

3. URL Shortener
Navigate:

cd "URL Shortener" # Use quotes because of the space in the folder name

Run:

python app.py

Access: Open your web browser and go to http://127.0.0.1:5000/

Note: If the Calculator App is running, it will conflict with this port (5000). Please stop one before running the other, or modify the port in one of the app.py files (e.g., app.run(debug=True, port=5002)).

7. Screenshots 📸
(To make your README truly shine, consider adding screenshots of each application here! You can upload them to your repository (e.g., in an assets/ folder) and then link them here.)

Example Placeholder:

Calculator App

Mail Application (Inbox)

URL Shortener







8. Contributing 🤝
Contributions are welcome! If you have suggestions for improvements or bug fixes, feel free to open an issue or submit a pull request.

9. License 📄
This project is licensed under the MIT License - see the LICENSE file for details (if you plan to add one). Otherwise, you can state:

This project is open-source.

10. Contact ✉️
GitHub: code3reaper 🐙

(Optional: Add your LinkedIn, personal website, or email here)

Feel free to connect or reach out with any questions!
