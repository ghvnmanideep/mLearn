from flask import Flask, render_template, request, redirect, session, flash
from pymongo import MongoClient
from datetime import datetime
from flask_mail import Mail, Message
import re

# MongoDB connection URI
mongouri = "mongodb+srv://manideep:11112006@manideep.wvzfqun.mongodb.net/?retryWrites=true&w=majority&appName=manideep"
client = MongoClient(mongouri)
print("Server is connected to the database")

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = '22f01a0545@gmail.com'
app.config['MAIL_PASSWORD'] = 'duqd cjoc grrn mwgu'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
db = client['sacet']
app.secret_key = "manideep11"

@app.route('/')
def start():
    return render_template('getstarted.html')

@app.route('/home')
def home1():
    if "username" not in session:
        return redirect("/")
    return render_template('home.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['uname']
        password = request.form['pwd']
        created_at = datetime.now()
        if not password_correct(password):
            return render_template('signup.html', err="Password must be at least 8 characters long and contain one special character.")
        data = {"username": username, "email": email, "password": password, "created_at": created_at}
        collection = db['signup']
        k = collection.find_one({"username": username, "email": email})
        
        if k is not None:
            return render_template('signup.html', err="Account exists")
        
        else:
            collection.insert_one(data)
            msg = Message("WELCOME TO M-LEARN", sender='22f01a0545@gmail.com', recipients=[email])
            msg.body = f'''Subject: Welcome to mLearn – Your Learning Journey Begins!
Dear {username},
Congratulations and welcome to mLearn!

We are thrilled to have you join our vibrant community of learners. You are now part of a platform dedicated to empowering individuals like you to achieve their educational goals and unlock new opportunities.

Here’s what you can expect as you embark on your learning journey with us:

🌟 Personalized Learning Experience: Explore a wide range of courses tailored to your interests and career aspirations. Our platform adapts to your learning style, ensuring you get the most out of your experience.

📚 Expert Instructors: Learn from industry professionals and experienced educators who are passionate about sharing their knowledge and helping you succeed.

💬 Community Support: Connect with fellow learners, share insights, and collaborate on projects. Our community is here to support you every step of the way.

🎓 Track Your Progress: Keep an eye on your achievements and milestones as you complete courses and gain new skills.

To get started, simply log in to your account at [mLearn website link] and explore the courses available to you. If you have any questions or need assistance, our support team is just an email away.

Once again, welcome to mLearn! We can’t wait to see all the amazing things you will accomplish.

Happy learning!

Best regards,

The mLearn Team'''
            mail.send(msg)
            print("Email sent successfully")
            return redirect('/login')
    return render_template('signup.html')
def password_correct(password):
    if len(password) < 8:
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):  # Check for special characters
        return False
    return True

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('uname')  
        password = request.form.get('pwd')
        if not username or not password:  
            return render_template('login.html', err="Please enter both username and password.")
        collection = db['signup']
        k = collection.find_one({"username": username, "password": password})
        if k is None:
            return render_template('signup.html', err="Account not found.")
        else:
            collections = db['login']
            login_time = datetime.now()
            user_data = {"username": username, "login_time": login_time}
            collections.insert_one(user_data)
            session['username'] = username
            return redirect('/home')
    return render_template('login.html')

@app.route('/contactus',methods=['GET','POST'])
def contactus():
    if request.method=='POST':
        redirect('/contactus.html')
    return render_template('contactus.html')
@app.route('/support')
def supportus(): 
    return render_template('supportus.html')
@app.route('/internships')
def internships():
    return render_template('internships.html')
@app.route('/courses')
def courses():
    return render_template('courses.html')
@app.route('/logoff')
def logout():
        session.pop("username", None)
        return redirect('/')
@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')
@app.route('/contacting', methods=['POST'])
def contacting():
    name = request.form.get('name') 
    email = request.form.get('email')
    message = request.form.get('message') 

    # Store contact message
    data = {"name": name, "email": email, "message": message}
    with open('contact_messages.txt', 'a') as file:
        file.write(f"Name: {name}\nEmail: {email}\nMessage: {message}\n\n")

    # Send Thank You Email
    msg = Message('Thanks for contacting mLearn', sender='22f01a0545@gmail.com', recipients=[email])
    msg.body = f'''Dear {name},

Thank you for reaching out to mLearn! We appreciate your message and will respond within 24-48 hours.

Here’s a summary of your message:

Name: {name}
Email: {email}
Message: {message} 

Best regards,
The mLearn Team
'''
    mail.send(msg)

    return render_template('contactus.html', msg="Your message has been sent successfully!")
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=8000)