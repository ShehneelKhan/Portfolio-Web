import csv
from flask import Flask, render_template, url_for, request, redirect
from flask_mail import Mail, Message
import smtplib
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException





app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'yourId@gmail.com'
app.config['MAIL_PASSWORD'] = '*****'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


mail = Mail(app)



@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


# def write_to_file(data):
#     with open('database.txt', mode='a') as database:
#         email = data['email']
#         subject = data['subject']
#         message = data['message']
#         file = database.write(f'\n{email},{subject},{message}')

@app.route('/contact/')
def contact(data): 
    return render_template('contact.html')

    with open('database.csv', 'a', newline='') as csvfile:
        email = data['email']
        subject = data['subject']
        message = data['message']
        writer = csv.writer(csvfile)
        writer.writerow([email, subject, message])


        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = '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'

        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
        subject = "from the Python SDK!"
        sender = {"name":"Sendinblue","email":"contact@sendinblue.com"}
        replyTo = {"name":"Sendinblue","email":"contact@sendinblue.com"}
        html_content = "<html><body><h1>This is my first transactional email </h1></body></html>"
        to = [{"email":"example@example.com","name":"Jane Doe"}]
        params = {"parameter":"My param value","subject":"New Subject"}
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to="shehneelkhan92gmail.com", html_content=html_content, sender=email, subject=subject)
    
        try:
            api_response = api_instance.send_transac_email(send_smtp_email)
            print("MUHIB CHEETA: ", api_response)
        except ApiException as e:
            print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)


@app.route('/submit_form', methods=['GET', 'POST'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        write_to_csv(data)
        return redirect('/thankyou.html')
    else:
        return 'Something went wrong!'
