from flask import Flask, request, render_template_string
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

# Your Gmail & App Password
FROM = "akibkhan01561@gmail.com"
PWD = "ilnmdmpoyahlypgu"

HTML_FORM = '''
<h2>Email Automation Tool</h2>
<form method="POST">
    Emails (comma separated): <input type="text" name="emails" required><br><br>
    Subject: <input type="text" name="subject" required><br><br>
    Message:<br>
    <textarea name="body" rows="6" cols="50" required></textarea><br><br>
    <input type="submit" value="Send Emails">
</form>
'''

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        emails_input = request.form["emails"]
        subject = request.form["subject"]
        body = request.form["body"]

        emails = [e.strip() for e in emails_input.split(",")]
        results = ""

        for email in emails:
            msg = EmailMessage()
            msg["From"] = FROM
            msg["To"] = email
            msg["Subject"] = subject
            msg.set_content(body)

            try:
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                    server.login(FROM, PWD)
                    server.send_message(msg)
                results += f"✅ Email sent to {email}<br>"
            except Exception as e:
                results += f"❌ Failed for {email}: {e}<br>"

        return results + '<br><a href="/">Back</a>'

    return HTML_FORM

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
