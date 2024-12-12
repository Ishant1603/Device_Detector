from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from plyer import notification
#Mail Sendigfunction
def send_email(new_devices):
    sender_email = "sender_email"
    receiver_email = "recipient_email"
    password = ""

    msg = MIMEMultipart()
    msg['from'] = sender_email
    msg['to'] = receiver_email
    msg['subject'] = 'New Devices Connected to the Network'

    body = "New devices connected to the network:\n\n"
    for device in new_devices:
        body += f"IP: {device['ip']}, MAC: {device['mac']}, Hostname: {device['hostname']}\n"


    msg.attach(MIMEText(body,'plain'))


    try: 
        with smtplib.SMTP_SSL('smtp.gmail.com',465) as server:
            server.login(sender_email,password)
            text = msg.as_string()
            server.sendmail(sender_email,receiver_email,text)
        print("Email sent Successfully")

    except Exception as e:
        print(f"Error sending email: {e}") 

def send_notification(new_devices):
    devices_str = '\n'.join([f"IP: {device['ip']}, MAC: {device['mac']},Hostname: {device['hostname']}" for device in new_devices])
    notification.notify (
        title="New Devices Connected",
        message=f"New Devices:\n{devices_str}",
        timeout=10 )       
