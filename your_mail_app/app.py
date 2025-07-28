import os
import sqlite3
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, redirect, url_for, jsonify, session

# Initialize Flask App
app = Flask(__name__)
# A strong secret key is crucial for production. For this demo, a simple one is used.
app.secret_key = os.urandom(24)

# --- Database Setup ---
DATABASE = 'email_app.db'

def init_db():
    """Initializes the SQLite database with necessary tables."""
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        # Create users table to store email configurations
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                email TEXT NOT NULL UNIQUE,
                smtp_server TEXT NOT NULL,
                smtp_port INTEGER NOT NULL,
                imap_server TEXT NOT NULL,
                imap_port INTEGER NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        # Create sent_emails table to log sent emails
        c.execute('''
            CREATE TABLE IF NOT EXISTS sent_emails (
                id INTEGER PRIMARY KEY,
                user_email TEXT NOT NULL,
                to_email TEXT NOT NULL,
                subject TEXT,
                body TEXT,
                sent_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

# Ensure database is initialized when the app starts
with app.app_context():
    init_db()

# --- Email Service Functions ---

def send_email_service(from_email, to_email, subject, body, smtp_server, smtp_port, password):
    """Sends an email using SMTP."""
    try:
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Using SMTP_SSL for port 465 (secure) or SMTP for other ports with starttls
        if smtp_port == 465:
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        else:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls() # Secure the connection if not using SSL directly

        with server:
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())
        return True, "Email sent successfully!"
    except Exception as e:
        return False, f"Failed to send email: {e}"

def get_emails_service(email_address, password, imap_server, imap_port):
    """Fetches emails using IMAP."""
    emails = []
    try:
        with imaplib.IMAP4_SSL(imap_server, imap_port) as mail: # IMAP_SSL for secure connection
            mail.login(email_address, password)
            mail.select('inbox')
            status, email_ids = mail.search(None, 'ALL')
            
            # Fetch the latest 10 emails for efficiency
            latest_email_ids = email_ids[0].split()[-10:] 

            for e_id in reversed(latest_email_ids): # Display newer emails first
                status, msg_data = mail.fetch(e_id, '(RFC822)')
                if status == 'OK':
                    for response_part in msg_data:
                        if isinstance(response_part, tuple):
                            msg = email.message_from_bytes(response_part[1])
                            
                            # Decode subject
                            subject, encoding = email.header.decode_header(msg['Subject'])[0]
                            if isinstance(subject, bytes):
                                subject = subject.decode(encoding if encoding else 'utf-8', errors='ignore')
                            
                            # Decode 'From' field
                            from_field, encoding = email.header.decode_header(msg['From'])[0]
                            if isinstance(from_field, bytes):
                                from_field = from_field.decode(encoding if encoding else 'utf-8', errors='ignore')

                            body = ""
                            if msg.is_multipart():
                                for part in msg.walk():
                                    ctype = part.get_content_type()
                                    cdisposition = str(part.get('Content-Disposition'))

                                    # Try to get plain text part
                                    if ctype == 'text/plain' and 'attachment' not in cdisposition:
                                        try:
                                            body = part.get_payload(decode=True).decode('utf-8')
                                        except UnicodeDecodeError:
                                            body = part.get_payload(decode=True).decode('latin-1', errors='ignore')
                                        break
                            else:
                                try:
                                    body = msg.get_payload(decode=True).decode('utf-8')
                                except UnicodeDecodeError:
                                    body = msg.get_payload(decode=True).decode('latin-1', errors='ignore')

                            emails.append({
                                'from': from_field,
                                'subject': subject,
                                'body': body,
                                'date': msg['Date']
                            })
    except Exception as e:
        print(f"Error fetching emails: {e}")
        return [], f"Failed to fetch emails: {e}"
    return emails, None

# --- Flask Routes ---

@app.route('/')
def index():
    """Renders the configuration/login page if not configured, otherwise redirects to mail."""
    user_email = session.get('user_email')
    if user_email:
        # If user is already logged in, redirect to mail page
        return redirect(url_for('mail_app'))
    
    # Render configuration page
    return render_template('config.html')

@app.route('/save_config', methods=['POST'])
def save_config():
    """Saves user's email configuration to the database and logs them in."""
    email_address = request.form['email'] # Renamed variable to avoid conflict with 'email' module
    smtp_server = request.form['smtp_server']
    smtp_port = int(request.form['smtp_port'])
    imap_server = request.form['imap_server']
    imap_port = int(request.form['imap_port'])
    password = request.form['password'] # For demo, storing plaintext. In production, hash and encrypt!

    # Validate inputs (simple check)
    if not all([email_address, smtp_server, smtp_port, imap_server, imap_port, password]):
        return render_template('config.html', error="All fields are required!")

    try:
        with sqlite3.connect(DATABASE) as conn:
            c = conn.cursor()
            # Check if user already exists
            c.execute('SELECT id FROM users WHERE email = ?', (email_address,))
            existing_user = c.fetchone()

            if existing_user:
                # Update existing user config
                c.execute('''
                    UPDATE users SET smtp_server=?, smtp_port=?, imap_server=?, imap_port=?, password=?
                    WHERE email=?
                ''', (smtp_server, smtp_port, imap_server, imap_port, password, email_address))
            else:
                # Insert new user config
                c.execute('''
                    INSERT INTO users (email, smtp_server, smtp_port, imap_server, imap_port, password)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (email_address, smtp_server, smtp_port, imap_server, imap_port, password))
            conn.commit()
        
        # Set session for the logged-in user
        session['user_email'] = email_address
        return redirect(url_for('mail_app'))

    except sqlite3.IntegrityError:
        return render_template('config.html', error="Email already registered. Please login or update.")
    except Exception as e:
        return render_template('config.html', error=f"Error saving configuration: {e}")

@app.route('/logout')
def logout():
    """Logs out the user by clearing the session."""
    session.pop('user_email', None)
    return redirect(url_for('index'))

@app.route('/mail')
def mail_app():
    """Renders the main mail application page if the user is logged in."""
    user_email = session.get('user_email')
    if not user_email:
        return redirect(url_for('index')) # Redirect to config if not logged in

    user_config = get_user_config(user_email)
    if not user_config:
        # Should not happen if session is set correctly, but as a fallback
        session.pop('user_email', None)
        return redirect(url_for('index', error="User configuration not found."))

    # Initial fetch of emails for display
    emails, error = get_emails_service(user_config['email'], user_config['password'],
                                       user_config['imap_server'], user_config['imap_port'])
    
    # Fetch sent emails from local DB
    sent_emails = []
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute('SELECT to_email, subject, body, sent_date FROM sent_emails WHERE user_email = ? ORDER BY sent_date DESC LIMIT 5', (user_email,))
        sent_emails = [{'to_email': row[0], 'subject': row[1], 'body': row[2], 'sent_date': row[3]} for row in c.fetchall()]


    return render_template('index.html', user_email=user_email, emails=emails, sent_emails=sent_emails, fetch_error=error)

@app.route('/send_email', methods=['POST'])
def send_email():
    """Handles sending an email."""
    user_email = session.get('user_email')
    if not user_email:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401

    user_config = get_user_config(user_email)
    if not user_config:
        return jsonify({'success': False, 'message': 'User config not found'}), 500

    to_email = request.form['to_email']
    subject = request.form['subject']
    body = request.form['body']

    success, message = send_email_service(user_config['email'], to_email, subject, body,
                                        user_config['smtp_server'], user_config['smtp_port'],
                                        user_config['password'])
    if success:
        # Log sent email to local DB
        try:
            with sqlite3.connect(DATABASE) as conn:
                c = conn.cursor()
                c.execute('''
                    INSERT INTO sent_emails (user_email, to_email, subject, body)
                    VALUES (?, ?, ?, ?)
                ''', (user_email, to_email, subject, body))
                conn.commit()
        except Exception as db_e:
            print(f"Error logging sent email to DB: {db_e}")
            message += " (Note: Failed to log email locally)"

    return jsonify({'success': success, 'message': message})

@app.route('/get_emails_ajax')
def get_emails_ajax():
    """AJAX endpoint to fetch new emails."""
    user_email = session.get('user_email')
    if not user_email:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    user_config = get_user_config(user_email)
    if not user_config:
        return jsonify({'success': False, 'message': 'User config not found'}), 500

    emails, error = get_emails_service(user_config['email'], user_config['password'],
                                       user_config['imap_server'], user_config['imap_port'])
    
    if error:
        return jsonify({'success': False, 'message': error}), 500

    return jsonify({'success': True, 'emails': emails})

def get_user_config(email_address):
    """Helper function to retrieve user configuration from the database."""
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute('SELECT email, smtp_server, smtp_port, imap_server, imap_port, password FROM users WHERE email = ?', (email_address,))
        row = c.fetchone()
        if row:
            return {
                'email': row[0],
                'smtp_server': row[1],
                'smtp_port': row[2],
                'imap_server': row[3],
                'imap_port': row[4],
                'password': row[5]
            }
        return None

if __name__ == '__main__':
    # Flask runs on localhost, which will open in a browser tab (separate window).
    # Changed port to 5001 to avoid potential conflicts with port 5000.
    app.run(debug=True, port=5001)
