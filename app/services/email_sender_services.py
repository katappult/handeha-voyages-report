import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


class EmailSender:
    @staticmethod
    def send_email(recipient_email, subject, body, attachment_path):
        msg = MIMEMultipart()
        msg['From'] = "votre_email@gmail.com"
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Pièce jointe
        with open(attachment_path, "rb") as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {attachment_path}")
            msg.attach(part)

        # Envoyer l'e-mail
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login("votre_email@gmail.com", "mot_de_passe")
            server.sendmail(msg['From'], msg['To'], msg.as_string())
