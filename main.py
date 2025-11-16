import os

from flask import Flask, render_template, request, redirect, flash, abort, send_file
from werkzeug.utils import safe_join
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ✅ Your project data (you can add more later)
projects_data = {
    "MindCare-AI-Platform": {
        "title": "MindCare AI Platform",
        "image": "mindcare-ai-platform.jpg",
        "description": "An AI-powered mental health web app with therapist booking, chat integration, and daily mood tracking. Built with Flask, FastAPI, SQL, and JWT authentication for secure access.",
        "tools": ["Python", "Flask", "FastAPI", "SQLAlchemy", "JWT Auth", "React (frontend)"],
        "outcome": "Delivered an interactive AI-assisted therapy experience that improved client engagement and reduced manual therapist workload."
    },
    "Retail-Distribution-System": {
        "title": "Retail & Distribution Management System",
        "image": "retail-inventory-system.jpg",
        "description": "A Microsoft Access-based business information system managing inventory, sales, and employee data with secure role-based access control.",
        "tools": ["Access", "VBA", "SQL", "Microsoft Office Integration"],
        "outcome": "Automated inventory control, reduced data entry errors, and improved operational efficiency for retail management."
    },
    "Electric-Wire-Database": {
        "title": "Electric Wire Company Database",
        "image": "factory-data-system.jpg",
        "description": "A custom SQL-based database for a multi-branch wire manufacturing company. Tracks production, imports, sales, and quality assurance records.",
        "tools": ["SQLite", "Python", "Database Design", "Data Analysis"],
        "outcome": "Enabled real-time monitoring and data-driven decision-making across production units and distribution centers."
    },
    "AI-Chat-Integration": {
        "title": "AI Chat Integration",
        "image": "ai-chat-interface.jpg",
        "description": "A GPT-powered conversational AI system integrated into the MindCare platform to simulate therapist-client interactions and provide real-time mental health assistance.",
        "tools": ["OpenAI API", "FastAPI", "Flask", "WebSocket", "HTML/CSS"],
        "outcome": "Enhanced patient support availability by 40% through on-demand intelligent chat assistance."
    },
    "Gymshark-Digital-Strategy": {
        "title": "Gymshark Digital Marketing Strategy",
        "image": "digital-marketing-dashboard.jpg",
        "description": "A full-scale digital marketing plan including AI-based email personalization, SEO optimization, and interactive community engagement strategy.",
        "tools": ["Data Analytics", "SEO", "Email Automation", "Tableau", "Python"],
        "outcome": "Increased customer engagement and loyalty through personalized AI-powered marketing insights."
    },
    "Media-Trust-Analytics": {
        "title": "Media Trust Data Analytics",
        "image": "data-visualization-dashboard.jpg",
        "description": "A data analysis project exploring misinformation and media trust using Python, SQL, and Tableau visualization dashboards.",
        "tools": ["Python", "Pandas", "SQL", "Tableau", "Data Visualization"],
        "outcome": "Provided actionable insights into audience behavior and improved communication strategies."
    },
}



app = Flask(__name__)
app.secret_key = "yoursecretkey"


@app.context_processor
def inject_year():
    """Inject current year into all templates."""
    return {"current_year": datetime.datetime.now().year}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/services")
def services():
    return render_template("services.html")


@app.route("/projects")
def projects():
    return render_template("projects.html", projects=projects_data)


@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route('/send_email', methods=['POST'])
def send_email():
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']

    sender_email = email
    receiver_email = "enyionyinyegrace11@gmail.com"
    password = "gtrd dilz rzap zcbc"

    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = f"New Contact Form Message: {subject}"

        body = f"""
        Name: {name}
        Email: {email}
        Message:
        {message}
        """
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()

        flash("✅ Your message has been sent successfully!", "success")
        return redirect('/contact')

    except Exception as e:
        print(e)
        flash("❌ There was an error sending your message. Please try again.", "danger")
        return redirect('/contact')

@app.route("/project_view/<project_name>")
def project_view(project_name):
    project = projects_data.get(project_name)
    if not project:
        abort (404)
    return render_template("post.html", project=project)

@app.route('/amazon_analysis')
def amazon_analysis():
    return render_template("amazon_analysis.html")

@app.route("/devistar_project")
def devistar_project():
    return render_template("devistar_project.html")

UPLOAD_FOLDER = 'uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # ✅ Register in Flask config

@app.route('/download/<filename>')
def download(filename):
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Ensure the file exists before sending
        if not os.path.isfile(file_path):
            abort(404)

        # Send the file as an attachment
        return send_file(file_path, as_attachment=True)

    except Exception as e:
        print(f"Error while sending file: {e}")
        abort(500)

@app.route('/ecommerce-analysis')
def ecommerce_analysis():
    return render_template('ecommerce_analysis.html')

@app.route('/company-analysis')
def company_analysis():
    return render_template('customer_analytics.html')

if __name__ == "__main__":
    app.run(debug=True)
