import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import configparser
import ssl

def send_email(sender_email, sender_password, receiver_email, smtp_server, smtp_port, subject, body, attachment_path, ssl_cert_path):
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with open(attachment_path, 'rb') as file:
            part = MIMEApplication(file.read(), Name=os.path.basename(attachment_path))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
        msg.attach(part)

        context = ssl.create_default_context()
        context.load_verify_locations(ssl_cert_path)

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=context)
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return True
    except smtplib.SMTPConnectError:
        print("Failed to connect to the email server. Please check your network connection.")
    except smtplib.SMTPAuthenticationError:
        print("Authentication failed. Please check your username and password.")
    except smtplib.SMTPException as e:
        print(f"An SMTP error occurred: {e}")
    except Exception as e:
        print(f"General error occurred while sending email: {e}")
    return False

def get_pdfs(directory='data/PDFs'):
    try:
        pdfs = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.pdf')]
        return pdfs
    except Exception as e:
        print(f"Error occurred while retrieving PDFs: {e}")
        return []

def find_email_from_pdf(pdf_path):
    try:
        import PyPDF2
        import re

        reader = PyPDF2.PdfReader(pdf_path)
        text = ''.join(page.extract_text() for page in reader.pages)
        email_pattern = r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)'
        emails_found = re.findall(email_pattern, text)
        emails_found = [email for email in emails_found if email != 'uprava@zgs-ptuj.si']

        if not emails_found:
            with open('data/missing_emails_list.txt', 'a') as f:
                f.write(f'  -{os.path.basename(pdf_path)}\n')

        return emails_found[0] if emails_found else None
    except Exception as e:
        print(f"Error occurred while finding email in PDF: {e}")
        return None

def setup(directory='data/PDFs', txt_file='data/missing_emails_list.txt'):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(txt_file, 'w') as f:
            f.write('List of documents where no email was found (they need to be sent manually):\n')
    except Exception as e:
        print(f"Error occurred during setup: {e}")

def main():
    failed_emails = []  # List to store failed email attempts
    try:
        config = configparser.ConfigParser()
        config.read('config/config.ini', encoding='utf-8')
        smtp_server = config['EmailSettings']['smtp_host']
        smtp_port = int(config['EmailSettings']['smtp_port'])
        subject = config['EmailSettings']['subject']
        body = config['EmailSettings']['body']
        sender_email = config['EmailSettings']['smtp_user']
        sender_password = config['EmailSettings']['smtp_password']
        ssl_cert_path = 'config/cacert-2024-03-11.pem'

        pdfs = get_pdfs()
        setup()
        for pdf in pdfs:
            receiver_email = find_email_from_pdf(pdf)
            if receiver_email:
                if not send_email(sender_email, sender_password, receiver_email, smtp_server, smtp_port, subject, body, pdf, ssl_cert_path):
                    print(f"Failed to send email to {receiver_email}. Please check the recipient's email address and your network connection.")
                    failed_emails.append((receiver_email, pdf))  # Add to list if sending failed
                else:
                    print(f"Email sent to {receiver_email} with attachment {pdf}")

        if failed_emails:
            print("Failed to send emails to the following addresses:")
            for email, pdf in failed_emails:
                print(f"{email} (Attachment: {pdf})")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == '__main__':
    main()

# Author: Oskar Forštnarič
