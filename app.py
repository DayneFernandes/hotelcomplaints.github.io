
from flask import Flask, render_template, request, redirect
import mysql.connector
from flask import render_template, render_template_string
from datetime import datetime,date


app = Flask(__name__)

# MySQL database configuration
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'dayneD199931#',
    'database': 'hotel_complaints1'
}



# Create MySQL connection
cnx = mysql.connector.connect(**db_config)


# Create a cursor to execute SQL queries
cursor = cnx.cursor()

# SQL query to create the complaints table
# Drop the existing complaints table
drop_table_query = '''
DROP TABLE IF EXISTS complaints
'''
cursor.execute(drop_table_query)



# Create the new complaints table
complaints_table_query = '''
CREATE TABLE IF NOT EXISTS complaints (
    id INT AUTO_INCREMENT PRIMARY KEY,
    guest_name VARCHAR(255) NOT NULL,
    room_number VARCHAR(10) NOT NULL,
    phone_number VARCHAR(15) NOT NULL,
    category VARCHAR(255) NOT NULL,
    comment TEXT NOT NULL,
    staff_name VARCHAR(255),
    status VARCHAR(20) DEFAULT 'Pending',
    staff_comment TEXT,
    complaint_timing TIME,
    complaint_date DATE
)
'''
cursor.execute(complaints_table_query)



# SQL query to create the users table
users_table_query = '''
CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
)
'''
cursor.execute(users_table_query)

# Commit the changes and close the cursor
cnx.commit()
cursor.close()


@app.route('/')
def index():
    return """
    <html>
    <head>
        <title>Summerville Beach Resort Guest Portal</title>
        <style>
            body {
                background-color: #f7f7f7;
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
            }

            .container {
                width: 80%;
                margin: 0 auto;
                padding: 50px 0;
                text-align: center;
            }

            h1 {
                font-family: 'Helvetica Neue', Arial, sans-serif;
                font-size: 36px;
                color: #333;
                margin-bottom: 20px;
            }

            p {
                font-size: 18px;
                margin-bottom: 10px;
            }

            a {
                display: inline-block;
                padding: 12px 20px;
                background-color: #007bff;
                color: #fff;
                text-decoration: none;
                border-radius: 4px;
                font-size: 16px;
                transition: background-color 0.3s ease;
            }

            a:hover {
                background-color: #0056b3;
            }

            .logo {
                margin-bottom: 30px;
            }

            .message {
                font-size: 20px;
                color: #666;
                margin-bottom: 30px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <img class="logo" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTUCRhC1D93TwUbeNPTnS-HLSmY0TBRtaGIE3ANZXBD-Q&s" alt="Summerville Beach Resort Logo">
            <h1>Welcome to Summerville Beach Resort Guest Portal</h1>
            <p class="message">We value your stay and are committed to providing exceptional service.</p>
            <p>Kindly choose an option below:</p>
            <p><a href="/submit-complaint">Lodge a Complaint</a></p>
            <p><a href="/complaints">Staff Login</a></p>
        </div>
    </body>
    </html>
    """


@app.route('/submit-complaint', methods=['GET', 'POST'])
def submit_complaint():
    if request.method == 'POST':
        guest_name = request.form['guest_name']
        room_number = request.form['room_number']
        phone_number = request.form['phone_number']
        category = request.form['category']
        comment = request.form['comment']
        complaint_time = datetime.now().time().strftime('%H:%M:%S')
        
        today = date.today()
        
        # Insert the complaint into the database
        cursor = cnx.cursor()
        insert_query = '''
        INSERT INTO complaints (guest_name, room_number, phone_number, category, comment,complaint_date)
        VALUES (%s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(insert_query, (guest_name, room_number, phone_number, category, comment,today))
        cnx.commit()
        cursor.close()
    
    
        
    
        return """
        <html>
            <head>
                <title>Thank You</title>
            </head>
            <body style="background-color: #f2f2f2; text-align: center;">
                <h1 style="color: #333;">Thank You for Submitting Your Complaint</h1>
            </body>
        </html>
        """
    
    return """
    <html>
        <head>
            <title>Submit Complaint</title>
        </head>
        <body style="background-color: #f2f2f2; text-align: center;">
            <h1 style="color: #333;">Submit a Complaint</h1>
            <form method="POST" action="/submit-complaint">
                <label for="guest_name">Guest Name:</label><br>
                <input type="text" id="guest_name" name="guest_name" required><br><br>
                <label for="room_number">Room Number:</label><br>
                <input type="text" id="room_number" name="room_number" required><br><br>
                <label for="phone_number">Phone Number:</label><br>
                <input type="text" id="phone_number" name="phone_number" required><br><br>
                <label for="category">Category:</label><br>
                <select id="category" name="category" required>
                    <option value="TV">TV</option>
                    <option value="Fridge">Fridge</option>
                    <option value="Fan">Fan</option>
                    <option value="Lights">Lights</option>
                    <option value="Cleaning">Cleaning</option>
                    <option value="Internet">Internet</option>
                    <option value="AC">AC</option>
                    <option value="Bed">Bed</option>
                    <option value="Others">Others</option>
                </select><br><br>
                <label for="comment">Comment:</label><br>
                <textarea id="comment" name="comment" rows="4" cols="50" required></textarea><br><br>
                <input type="submit" value="Submit">
            </form>
        </body>
    </html>
    """

import io
import xlsxwriter




# Complaints route
@app.route('/complaints', methods=['GET', 'POST'])
def complaints():
    if request.method == 'POST':
        # Check if the username and password are valid
        username = request.form['username']
        password = request.form['password']
        
        # Perform the necessary validation/authentication logic here
        if not is_valid_staff(username, password):
            return "Invalid staff login"
        # If the username and password are valid, proceed to display the complaints table
        cursor = cnx.cursor()
        select_query = '''
        SELECT * FROM complaints
        '''
        cursor.execute(select_query)
        complaints = cursor.fetchall()
        cursor.close()

        # Generate the HTML table dynamically
        table_content = ''
        for complaint in complaints:
            table_content += f'''
                <tr>
                    <td>{complaint[1]}</td>
                    <td>{complaint[2]}</td>
                    <td>{complaint[3]}</td>
                    <td>{complaint[4]}</td>
                    <td>{complaint[5]}</td>
                    <td>{complaint[9]}</td>
                    <td>{complaint[10]}</td>
                    <td>
                        <form method="POST" action="/update-complaint">
                            <input type="hidden" name="complaint_id" value="{complaint[0]}">
                            <input type="text" name="staff_name" value="{complaint[6]}">
                    </td>
                    <td>
                            <input type="text" name="staff_comment" value="{complaint[8]}">
                    </td>
                    <td>
                            <select name="status">
                                <option value="Pending" {'selected' if complaint[7] == 'Pending' else ''}>Pending</option>
                                <option value="In Progress" {'selected' if complaint[7] == 'In Progress' else ''}>In Progress</option>
                                <option value="Completed" {'selected' if complaint[7] == 'Completed' else ''}>Completed</option>
                            </select>
                    </td>
                    <td>
                            <input type="submit" value="Update">
                        </form>
                    </td>
                </tr>
            '''

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Complaints</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #eef5f9;
                }}
                h1 {{
                    text-align: center;
                    color: #112d4e;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin-top: 20px;
                    background-color: #fff;
                }}
                th, td {{
                    padding: 10px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                th {{
                    background-color: #f9a828;
                    color: #fff;
                }}
                tr:hover {{
                    background-color: #f2f2f2;
                }}
                form {{
                    display: inline-block;
                }}
                select {{
                    width: 100%;
                    padding: 8px;
                    border-radius: 3px;
                    border: 1px solid #ccc;
                }}
                input[type="text"], select, input[type="submit"] {{
                    width: 100%;
                    padding: 8px;
                    border-radius: 3px;
                    border: 1px solid #ccc;
                }}
                input[type="submit"] {{
                    background-color: #f9a828;
                    color: #fff;
                    font-weight: bold;
                    cursor: pointer;
                }}
                input[type="submit"]:hover {{
                    background-color: #d18e17;
                }}
            </style>
        </head>
        <body>
            <h1>Complaints</h1>
            <table>
                <tr>
                    <th>Guest Name</th>
                    <th>Category</th>
                    <th>Room Number</th>
                    <th>Phone Number</th>
                    <th>Comments</th>
                    <th>Time</th>
                    <th>Date</th>
                    <th>Staff Name</th>
                    <th>Staff Comment</th>
                    <th>Status</th>
                    <th>Action</th>
                </tr>
                {table_content}
            </table>
            <br>
            <form action="/export-complaints" method="POST">
                <input type="submit" value="Export to Excel">
            </form>
        </body>
        </html>
        """
        
        return html_content
    
    # If it's a GET request, display the login form
    login_form = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Staff Login</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #eef5f9;
            }}
            h1 {{
                text-align: center;
                color: #112d4e;
                margin-top: 100px;
            }}
            form {{
                width: 300px;
                margin: 0 auto;
                margin-top: 20px;
                padding: 20px;
                background-color: #fff;
                border-radius: 5px;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            }}
            label {{
                display: block;
                margin-bottom: 10px;
                color: #112d4e;
                font-weight: bold;
            }}
            input[type="text"], input[type="password"] {{
                width: 100%;
                padding: 8px;
                border-radius: 3px;
                border: 1px solid #ccc;
            }}
            input[type="submit"] {{
                width: 100%;
                padding: 10px;
                background-color: #f9a828;
                border: none;
                color: #fff;
                font-weight: bold;
                cursor: pointer;
                border-radius: 3px;
            }}
            input[type="submit"]:hover {{
                background-color: #d18e17;
            }}
        </style>
    </head>
    <body>
        <h1>Staff Login</h1>
        <form action="/complaints" method="POST">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required><br><br>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required><br><br>
            <input type="submit" value="Login">
        </form>
    </body>
    </html>
    """
    
    return login_form


# Update complaint route
@app.route('/update-complaint', methods=['POST'])
def update_complaint():
    complaint_id = request.form['complaint_id']
    staff_name = request.form['staff_name']
    staff_comment = request.form['staff_comment']
    status = request.form['status']
    
    # Update the complaint with staff information
    cursor = cnx.cursor()
    complaints_update_query = '''
    UPDATE complaints SET staff_name = %s, status = %s, staff_comment = %s WHERE id = %s
    '''
    cursor.execute(complaints_update_query, (staff_name, status, staff_comment, complaint_id))
    cnx.commit()
    cursor.close()
    
    return redirect('/complaints')



































































@app.route('/complaints', methods=['GET', 'POST'])
def complaints():
    if request.method == 'POST':
        # Check if the username and password are valid
        username = request.form['username']
        password = request.form['password']
        
        # Perform the necessary validation/authentication logic here
        # You can check if the username and password match a staff member in your database
        
        # Assuming the staff member is authenticated, proceed to display the complaints table
        cursor = cnx.cursor()
        select_query = '''
        SELECT * FROM complaints
        '''
        cursor.execute(select_query)
        complaints = cursor.fetchall()
        cursor.close()

        # Sort complaints by status (Pending complaints first)
        complaints = sorted(complaints, key=lambda x: x[7] != 'Complete')

        # Generate the HTML table dynamically
        table_content = ''
        for complaint in complaints:
            table_content += f'''
                <tr>
                    <td>{complaint[1]}</td>
                    <td>{complaint[2]}</td>
                    <td>{complaint[3]}</td>
                    <td>{complaint[4]}</td>
                    <td>{complaint[5]}</td>
                    <td>{complaint[6]}</td>
                    <td>{complaint[7]}</td>
                    <td>{complaint[8]}</td>
                    <td>{complaint[9]}</td>
                    <td>{complaint[10]}</td>
                    <td>
                        <form method="POST" action="/update-complaint">
                            <input type="hidden" name="complaint_id" value="{complaint[0]}">
                            <input type="hidden" name="status" value="{complaint[7]}">
                            <input type="hidden" name="staff_name" value="{complaint[6]}">
                            <input type="hidden" name="staff_comment" value="{complaint[8]}">
                            <input type="submit" value="Update">
                        </form>
                        
                    </td>
                </tr>
            '''

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Complaints</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #eef5f9;
                }}
                h1 {{
                    text-align: center;
                    color: #112d4e;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin-top: 20px;
                    background-color: #fff;
                }}
                th, td {{
                    padding: 10px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                th {{
                    background-color: #f9a828;
                    color: #fff;
                }}
                tr:hover {{
                    background-color: #f2f2f2;
                }}
                form {{
                    display: inline-block;
                }}
                input[type="submit"] {{
                    padding: 5px 10px;
                    background-color: #f9a828;
                    border: none;
                    color: #fff;
                    font-weight: bold;
                    cursor: pointer;
                    border-radius: 3px;
                }}
                input[type="submit"]:hover {{
                    background-color: #d18e17;
                }}
                input[type="submit"][disabled] {{
                    background-color: #ccc;
                    cursor: not-allowed;
                }}
            </style>
        </head>
        <body>
            <h1>Complaints</h1>
            <table>
                <tr>
                    <th>Guest Name</th>
                    <th>Category</th>
                    <th>Room Number</th>
                    <th>Phone Number</th>
                    <th>Comments</th>
                    <th>Staff Name</th>
                    <th>Status</th>
                    <th>Staff Comment</th>
                    <th>Actions</th>
                </tr>
                {table_content}
            </table>
            <br>
            <form action="/export-complaints" method="POST">
                <input type="submit" value="Export to Excel">
            </form>
        </body>
        </html>
        """
        
        return html_content
    
    # If it's a GET request, display the login form
    login_form = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Staff Login</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #eef5f9;
            }}
            h1 {{
                text-align: center;
                color: #112d4e;
                margin-top: 100px;
            }}
            form {{
                width: 300px;
                margin: 0 auto;
                margin-top: 20px;
                padding: 20px;
                background-color: #fff;
                border-radius: 5px;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            }}
            label {{
                display: block;
                margin-bottom: 10px;
                color: #112d4e;
                font-weight: bold;
            }}
            input[type="text"], input[type="password"] {{
                width: 100%;
                padding: 8px;
                border-radius: 3px;
                border: 1px solid #ccc;
            }}
            input[type="submit"] {{
                width: 100%;
                padding: 10px;
                background-color: #f9a828;
                border: none;
                color: #fff;
                font-weight: bold;
                cursor: pointer;
                border-radius: 3px;
            }}
            input[type="submit"]:hover {{
                background-color: #d18e17;
            }}
        </style>
    </head>
    <body>
        <h1>Staff Login</h1>
        <form action="/complaints" method="POST">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required><br><br>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required><br><br>
            <input type="submit" value="Login">
        </form>
    </body>
    </html>
    """
    
    return login_form




































@app.route('/complaints', methods=['GET', 'POST'])
def complaints():
    if request.method == 'POST':
        # Check if the username and password are valid
        username = request.form['username']
        password = request.form['password']
        
        # Perform the necessary validation/authentication logic here
        
        # If the username and password are valid, proceed to display the complaints table
        cursor = cnx.cursor()
        select_query = '''
        SELECT * FROM complaints
        '''
        cursor.execute(select_query)
        complaints = cursor.fetchall()
        cursor.close()

        # Generate the HTML table dynamically
        table_content = ''
        for complaint in complaints:
            table_content += f'''
                <tr>
                    <td>{complaint[1]}</td>
                    <td>{complaint[2]}</td>
                    <td>{complaint[3]}</td>
                    <td>{complaint[4]}</td>
                    <td>{complaint[5]}</td>
                    <td>{complaint[6]}</td>
                    <td>{complaint[7]}</td>
                    <td>{complaint[8]}</td>
                    <td>{complaint[9]}</td>
                    <td>{complaint[10]}</td>
                </tr>
            '''

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Complaints</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #eef5f9;
                }}
                h1 {{
                    text-align: center;
                    color: #112d4e;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin-top: 20px;
                    background-color: #fff;
                }}
                th, td {{
                    padding: 10px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                th {{
                    background-color: #f9a828;
                    color: #fff;
                }}
                tr:hover {{
                    background-color: #f2f2f2;
                }}
                form {{
                    width: 300px;
                    margin: 0 auto;
                    margin-top: 100px;
                    padding: 20px;
                    background-color: #fff;
                    border-radius: 5px;
                    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                }}
                label {{
                    display: block;
                    margin-bottom: 10px;
                    color: #112d4e;
                    font-weight: bold;
                }}
                input[type="text"], input[type="password"] {{
                    width: 100%;
                    padding: 8px;
                    border-radius: 3px;
                    border: 1px solid #ccc;
                }}
                input[type="submit"] {{
                    width: 100%;
                    padding: 10px;
                    background-color: #f9a828;
                    border: none;
                    color: #fff;
                    font-weight: bold;
                    cursor: pointer;
                    border-radius: 3px;
                }}
                input[type="submit"]:hover {{
                    background-color: #d18e17;
                }}
            </style>
        </head>
        <body>
            <h1>Complaints</h1>
            <table>
                <tr>
                    <th>Guest Name</th>
                    <th>Category</th>
                    <th>Room Number</th>
                    <th>Phone Number</th>
                    <th>Comments</th>
                    <th>Guest Name1</th>
                    <th>Category1</th>
                    <th>Room Number1</th>
                    <th>Phone Number1</th>
                    <th>Comments1</th>
                </tr>
                {table_content}
            </table>
            <br>
            <form action="/export-complaints" method="POST">
                <input type="submit" value="Export to Excel">
            </form>
        </body>
        </html>
        """
        
        return html_content
    
    # If it's a GET request, display the login form
    login_form = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Staff Login</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #eef5f9;
            }}
            h1 {{
                text-align: center;
                color: #112d4e;
                margin-top: 100px;
            }}
            form {{
                width: 300px;
                margin: 0 auto;
                margin-top: 20px;
                padding: 20px;
                background-color: #fff;
                border-radius: 5px;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            }}
            label {{
                display: block;
                margin-bottom: 10px;
                color: #112d4e;
                font-weight: bold;
            }}
            input[type="text"], input[type="password"] {{
                width: 100%;
                padding: 8px;
                border-radius: 3px;
                border: 1px solid #ccc;
            }}
            input[type="submit"] {{
                width: 100%;
                padding: 10px;
                background-color: #f9a828;
                border: none;
                color: #fff;
                font-weight: bold;
                cursor: pointer;
                border-radius: 3px;
            }}
            input[type="submit"]:hover {{
                background-color: #d18e17;
            }}
        </style>
    </head>
    <body>
        <h1>Staff Login</h1>
        <form action="/complaints" method="POST">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required><br><br>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required><br><br>
            <input type="submit" value="Login">
        </form>
    </body>
    </html>
    """
    
    return login_form








































@app.route('/complaints', methods=['GET', 'POST'])
def complaints():
    if request.method == 'POST':
        
        username = request.form['username']
        password = request.form['password']
        
        if not is_valid_staff(username, password):
            return "Invalid staff login"
        
        staff_name = request.form['staff_name']
        status = request.form['status']
        staff_comment = request.form['staff_comment']
        complaint_id = request.form['complaint_id']
    
        # Update the complaint with staff information
        cursor = cnx.cursor()
        complaints_update_query = '''
        UPDATE complaints SET staff_name = %s, status = %s, staff_comment = %s WHERE id = %s
        '''
        cursor.execute(complaints_update_query, (staff_name, status, staff_comment, complaint_id))
        cnx.commit()
        cursor.close()
    
        return redirect('/complaints')
    
    # Fetch the complaints from the database
    cursor = cnx.cursor()
    select_query = '''
    SELECT * FROM complaints ORDER BY (status = 'Pending') DESC
    '''
    cursor.execute(select_query)
    complaints = cursor.fetchall()
    cursor.close()
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Complaints</title>
        <style>
            table {
                border-collapse: collapse;
                width: 100%;
                font-family: Arial, sans-serif;
            }
            th, td {
                padding: 8px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }
            th {
                background-color: #f2f2f2;
            }
            .update-form {
                display: inline-block;
            }
            .update-form input {
                margin-right: 10px;
            }
        </style>
    </head>
    <body>
        <h1>Complaints</h1>
        <table>
            <tr>
                <th>Guest Name</th>
                <th>Category</th>
                <th>Room Number</th>
                <th>Phone Number</th>
                <th>Comments</th>
                <th>Status</th>
                <th>Staff Name</th>
                <th>Staff Comment</th>
                <th>Complaint Date</th>
                <th>Complaint Time</th>
                <th>Action</th>
            </tr>
    """

    for complaint in complaints:
        complaint_id = complaint[0]
        guest_name = complaint[1]
        category = complaint[4]
        room_number = complaint[2]
        phone_number = complaint[3]
        comment = complaint[5]
        status = complaint[7]
        staff_name = complaint[6]
        staff_comment = complaint[8]
        complaint_date = complaint[10]
        complaint_time = complaint[9]

        html_content += f"""
            <tr>
                <td>{guest_name}</td>
                <td>{category}</td>
                <td>{room_number}</td>
                <td>{phone_number}</td>
                <td>{comment}</td>
                <td>{status}</td>
                <td>{staff_name}</td>
                <td>{staff_comment}</td>
                <td>{complaint_date}</td>
                <td>{complaint_time}</td>
                <td>
                    <form class="update-form" method="POST">
                        <input type="hidden" name="complaint_id" value="{complaint_id}">
                        <input type="text" name="staff_name" placeholder="Staff Name">
                        <select name="status">
                            <option value="Pending">Pending</option>
                            <option value="Complete">Complete</option>
                        </select>
                        <input type="text" name="staff_comment" placeholder="Staff Comment">
                        <input type="submit" value="Update">
                    </form>
                    <p><a href="/export-complaints">Excel-Download</a></p>
                </td>
            </tr>
        """

    html_content += """
        </table>
    </body>
    </html>
    """

    return render_template_string(html_content)



from flask import send_file


import pandas as pd
from flask import make_response
import io
import xlsxwriter


@app.route('/export-complaints', methods=['POST'])
def export_complaints():
    cursor = cnx.cursor()
    select_query = '''
    SELECT * FROM complaints
    '''
    cursor.execute(select_query)
    complaints = cursor.fetchall()
    cursor.close()

    # Create an in-memory file-like object
    output = io.BytesIO()

    # Create a new workbook and add a worksheet
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    # Write the column headers
    headers = ['Guest Name', 'Room Number', 'Phone Number', 'Category','Comment', 'Staff_Name','Status','Staff_Comment','Complaint_Time','Complaint_Date']
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)

    
            
    # Write the complaint data
    for row, complaint in enumerate(complaints):
        for col, field in enumerate(complaint[1:]):
            # Handle date formatting for Complaint_Date column
            if headers[col] == 'Complaint_Date':
                field = field.strftime('%d-%m-%Y')

            worksheet.write(row + 1, col, field)

    # Close the workbook
    workbook.close()

    # Set the appropriate headers for Excel file download
    output.seek(0)
    return send_file(output, attachment_filename='complaints.xlsx', as_attachment=True)

from flask import send_file

def is_valid_staff(username, password):
    valid_combinations = {
        'Pundalik': 'Pundalik@Summerville',
        'Dayne': 'Dayne@Summerville',
        'Staff': 'Stafflogin123'
    }
    
    if username in valid_combinations and password == valid_combinations[username]:
        return True
    
    return False



if __name__ == '__main__':
    app.run()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
