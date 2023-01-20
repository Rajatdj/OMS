from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib
from django.conf import settings
from django.contrib.auth.models import User
import csv
from inventory.models import Inventory
from core_app.models import Token
from barcode import EAN13

def send_stock_update_email():
    try:
        users = User.objects.all()
        
        for user in users:
            if user.is_superuser:
                pass
            else:
                message = MIMEMultipart()
                message['From'] = 'Techmaadhyam'
                message['To'] =  user.email
                message['Subject'] = 'Stock Update'
                html = f"""
                <html>
                    <body>
                    <h3>
                        Hi {user.first_name}, 
                    </h3>
                    </body>
                </html>
                """
                filname = "{}.csv".format(settings.MEDIA_ROOT)
                stock_details = Inventory.objects.filter(user=user)
                header = ['SKU', 'Item Name', 'Price', 'Tax','Type','Unit', 'Category', 'HSN Code', 'Stock']
                with open('inventory.csv', 'w', encoding='UTF8') as f:
                    writer = csv.writer(f)
                    writer.writerow(header)
                    for item in stock_details:
                        writer.writerow([item.sku, item.item_name, item.price, item.tax, item.type, item.unit_of_measurement, item.item_category, item.hsn_code, item.stock])
                FILE_NAME = 'inventory.csv'
                message.attach(MIMEText(html, 'html'))
                with open('inventory.csv','rb') as file:
                    message.attach(MIMEApplication(file.read(), Name=FILE_NAME))
                with smtplib.SMTP(host=settings.EMAIL_HOST, port=settings.EMAIL_PORT) as smtp:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.login(user=settings.EMAIL_HOST_USER, password=settings.EMAIL_HOST_PASSWORD)
                    smtp.send_message(message)
                
    except Exception as error:
        pass
        print(str(error))


def send_password_reset_email(*args):
    try:
        token = args[0]
        user_detail = Token.objects.get(token=args[0])
        if user_detail.user_id:
            users =  user_detail.user_id
            if users.is_superuser:
                pass
            else:
                message = MIMEMultipart()
                message['From'] = 'Techmaadhyam'
                message['To'] =  users.email
                message['Subject'] = 'Techmaadhyam: Reset Password'
                html = f"""
                                    <html>
                                        <body>
                                        <h3>
                                            Hi {users.first_name}, 
                                            <p>Click on the below link to reset your password:</p>
                                            <a href="http://127.0.0.1:8000/reset-password/{user_detail.token}"> Reset Password </a>
                                        </h3>
                                        </body>
                                    </html>
                                    """
                message.attach(MIMEText(html, 'html'))
                with smtplib.SMTP(host=settings.EMAIL_HOST, port=settings.EMAIL_PORT) as smtp:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.login(user=settings.EMAIL_HOST_USER, password=settings.EMAIL_HOST_PASSWORD)
                    smtp.send_message(message)
    except Exception as error:
        pass
        print(str(error))


def generate_barcode(number):
    path = 'media/barcode/' + number + '.png'
    my_code = EAN13(number)
    my_code.save(path)
    return 'barcode/' + number + '.png'