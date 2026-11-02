import os
import numpy as np
from flask import Flask, render_template, request, redirect, session, jsonify, Blueprint, send_file
import mysql.connector
import pycountry
import sklearn.metrics._dist_metrics as _dist_metrics
from werkzeug.utils import secure_filename

from feature_extraction import allowed_file, extract_voice_features
from model_utils import load_model_and_scaler, predict_from_features

knn = Blueprint('knn', __name__)

# Compatibility alias for older pickled sklearn KNN models
if not hasattr(_dist_metrics, 'EuclideanDistance'):
    _dist_metrics.EuclideanDistance = _dist_metrics.EuclideanDistance64

app = Flask(__name__)
app.secret_key = '\xb6skT\xf9\xe1\x98\xef\xd5\xb1q\xbb\xc9^\xac\x19:S\xde\r\\\xdc$L'
model, scaler = load_model_and_scaler()
print(f"[STARTUP] Scaler expects {scaler.n_features_in_} features")
print(f"[STARTUP] Model expects {model.n_features_in_} features")

# MySQL Configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Bcawala@123",
    database="user_db"
)
cursor = db.cursor()

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # limit uploads to 16 MB

# Define a route to handle tracking of user IP addresses
@app.route('/')
def track_ip():
    # Get the visitor's IP address
    ip_address = request.remote_addr
    
    # Insert the IP address into the database
    cursor.execute("INSERT INTO visitors (ip_address) VALUES (%s)", (ip_address,))
    db.commit()
    
    # Return a response
    return render_template('login.html')

# Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()
        if user:
            session['username'] = user[1]  # Assuming username is the second column
            return redirect('/dashboard')
        else:
            return "Invalid email or password. <a href='/login'>Try again</a>"
    return render_template('login.html')

@app.route('/adminlogin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor.execute("SELECT * FROM admin_credentials WHERE email=%s AND password=%s", (email, password))
        admin = cursor.fetchone()
        if admin:
            session['admin'] = True
            track_ip()  # Track admin IP address
            return redirect('/admindashboard')
        else:
            return "Invalid email or password. <a href='/adminlogin'>Try again</a>"
    return render_template('adminlogin.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        db.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('index.html', username=session['username'], prediction_text=None, error=None)
    return redirect('/login')

@app.route('/admindashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect('/adminlogin')  # Redirect if not logged in as admin

    # Execute SQL query to count rows
    cursor.execute("SELECT COUNT(*) FROM visitors")
    result = cursor.fetchone()
    row_count = result[0] if result else 0

    # Execute SQL query to count comments
    cursor.execute("SELECT COUNT(*) FROM comments")
    comment_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM test_report")
    tested = cursor.fetchone()[0]

    # Fetch user details from the database
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    return render_template('admindashboard.html', row_count=row_count, comment_count=comment_count, tested=tested, users=users)

@app.route('/report')
def report():
    try:
        # Execute the SQL query to fetch data from users and test_report tables
        cursor.execute("""
            SELECT users.id, users.username, test_report.MDVP_Fo_Hz, test_report.MDVP_Fhi_Hz, 
                   test_report.MDVP_Flo_Hz, test_report.MDVP_Jitter_percent, test_report.MDVP_Shimmer, 
                   test_report.NHR, test_report.RPDE, test_report.DFA, test_report.spread1, 
                   test_report.spread2, test_report.D2
            FROM users
            JOIN test_report ON users.id = test_report.id;
        """)
        
        # Fetch all rows returned by the query
        data = cursor.fetchall()
        print("Fetched data:", data)  # Print fetched data for debugging
        
        # Render the template with the fetched data
        return render_template('report.html', data=data)
    except Exception as e:
        return 'Error: ' + str(e)

# Route to handle like button click
@app.route('/like', methods=['POST'])
def like():
    try:
        # Execute SQL query to update like count in the database
        cursor.execute("UPDATE likes_dislikes SET likes = likes + 1 WHERE id = 1")
        db.commit()
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}


# Route to handle dislike button click
@app.route('/dislike', methods=['POST'])
def dislike():
    try:
        # Execute SQL query to update dislike count in the database
        cursor.execute("UPDATE likes_dislikes SET dislikes = dislikes + 1 WHERE id = 1")
        db.commit()
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}
    
# Route to handle form submission
@app.route('/submit_comment', methods=['POST'])
def submit_comment():
    if request.method == 'POST':
        # Get comment data from the form
        comment = request.form['comment']

        # Store comment data in the database
        cursor.execute("INSERT INTO comments (comment) VALUES (%s)", (comment,))
        db.commit()

        return render_template('download.html')
    
# Function to insert data into MySQL database
def insert_data(name, email):
    try:
        conn = mysql.connector.connect
        cursor = conn.cursor()
        query = "INSERT INTO users (name, email) VALUES (%s, %s)"
        cursor.execute(query, (name, email))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        return False
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

PDF_FOLDER = r"C:\Users\Dipen Rana\Documents\project\testD\pdfs"
@app.route('/download', methods=['GET', 'POST'])
def download():
    if request.method == 'POST':
        username = request.form['username']
        pdf_file = os.path.join(PDF_FOLDER, f'{username}.pdf')
        if os.path.exists(pdf_file):
            return send_file(pdf_file, as_attachment=True)
        else:
            return 'PDF not found for this username.'
    return render_template('download.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        if insert_data(name, email):
            return "Data submitted successfully!"
        else:
            return "An error occurred while submitting data."

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('admin', None)
    return redirect('/login')

def insert_data(data):
    try:
        # Execute SQL query to insert data
        query = "INSERT INTO test_report (MDVP_Fo_Hz, MDVP_Fhi_Hz, MDVP_Flo_Hz, MDVP_Jitter_percent, MDVP_Shimmer, NHR, RPDE, DFA, spread1, spread2, D2) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, data)

        # Commit changes
        db.commit()

        return True
    except mysql.connector.Error as err:
        print("MySQL Error:", err)  # Print error message
        return False
    
@app.route('/edit_admin')
def edit_admin():
    # Fetch admin details from database
    cursor.execute("SELECT * FROM admin_credentials WHERE id = 1")
    admin_details = cursor.fetchone()
    
    # Fetch all available countries
    countries = [country.name for country in pycountry.countries]
    
    return render_template('edit_admin.html', admin_details=admin_details, countries=countries)


@app.route('/save_admin_details', methods=['POST'])
def save_admin_details():
    name = request.form['name']
    gender = request.form['gender']
    country = request.form['country']
    address = request.form['address']
    phone = request.form['phone']
    
    # Update admin details in the database
    cursor.execute("UPDATE admin_credentials SET Name = %s, Gender = %s, Country = %s, Address = %s, Phone = %s WHERE id = 1",
                   (name, gender, country, address, phone))
    db.commit()
    
    return 'Admin details updated successfully!'


@app.route('/predict', methods=['POST'])
def predict():
    error = None
    prediction_text = None
    if 'audio_file' not in request.files:
        error = 'No file part in the request.'
        return render_template('index.html', prediction_text=None, error=error)

    audio_file = request.files['audio_file']
    if audio_file.filename == '':
        error = 'No WAV file selected.'
        return render_template('index.html', prediction_text=None, error=error)

    if not allowed_file(audio_file.filename):
        error = 'Invalid file type. Please upload a .wav file.'
        return render_template('index.html', prediction_text=None, error=error)

    filename = secure_filename(audio_file.filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    audio_file.save(save_path)

    try:
        feature_dict = extract_voice_features(save_path)
        model, scaler = load_model_and_scaler()
        prediction = predict_from_features(model, scaler, feature_dict)
        prediction_text = 'Parkinson\'s Disease Detected' if prediction == 1 else 'Parkinson\'s Disease Not Detected'
    except Exception as exc:
        error = f'Error processing file: {exc}'
    finally:
        if os.path.exists(save_path):
            try:
                os.remove(save_path)
            except OSError:
                pass

    return render_template('index.html', prediction_text=prediction_text, error=error)

if __name__ == '__main__':
    app.run(debug=True)
