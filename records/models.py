from django.db import models
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
import qrcode  
import requests
from qrcode import QRCode, constants
from PIL import Image, ImageOps
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.conf import settings
import os
# Create your models here.
class WaitingList(models.Model):
    id_passport_nbr = models.CharField(max_length=100, primary_key=True)
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    country_of_origin = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=200)
    mobile_phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.surname}"
    
    
class Visitor(models.Model):
    id_passport_nbr = models.CharField(max_length=100, primary_key=True)
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    country_of_origin = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=200)
    mobile_phone = models.CharField(max_length=20)
    user_saved = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='saved_visitors', null=True)
    user_checked_in = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='checked_in_visitors', null=True)
    def __str__(self):
        return f"{self.first_name} {self.surname}"

class Card(models.Model):
    name= models.CharField(max_length=50)
    number = models.CharField(max_length=50)

    def __str__(self):
        return self.number


class Movement(models.Model):
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, to_field='id_passport_nbr', related_name='movements')
    purpose = models.CharField(max_length=200)
    time_in = models.DateTimeField()
    time_out = models.DateTimeField(blank=True, null=True)
    devices = models.CharField(max_length=200, blank=True)
    comment = models.TextField(blank=True)
    card = models.ForeignKey(Card, on_delete=models.SET_NULL, blank=True, null=True)
    user_checked_in = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='checked_in_movements', null=True)
    user_checked_out = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='checked_out_movements', null=True)
    email_recipient_user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='email_recipient_movements', null=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def __str__(self):
        return f"{self.visitor} - Time In: {self.time_in} - Time Out: {self.time_out}"
    #goes in action after assigning/scanning the card to visitor
    def generate_qr_code(self):
        qr_data = f"{self.visitor.id_passport_nbr}" 
        logo_url = "https://bsc.rw/wp-content/uploads/2023/01/BSC-High-res.-vector-logo-01@2x-1-160x69.png"
        logo_response = requests.get(logo_url)
        logo = Image.open(BytesIO(logo_response.content))
        
        # taking base width
        basewidth = 100
        
        # adjust image size
        wpercent = (basewidth/float(logo.size[0]))
        hsize = int((float(logo.size[1])*float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
        QRcode = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H
        )
        
        
        # adding URL or text to QRcode
        QRcode.add_data(qr_data)
        
        # generating QR code
        QRcode.make()
        buffer = BytesIO()
        # taking color name from user
        QRcolor = 'Red'
        
        # adding color to QR code
        qr_img = QRcode.make_image(
            fill_color=QRcolor, back_color="white").convert('RGB')
        
        # set size of QR code
        pos = ((qr_img.size[0] - logo.size[0]) // 2,
            (qr_img.size[1] - logo.size[1]) // 2)
        qr_img.paste(logo, pos)
        # Save the QR code image to a temporary file
        img_temp = NamedTemporaryFile(delete=True, suffix='.png')
        qr_img.save(img_temp, format="PNG")
        img_temp.flush()

        # Save the QR code image to the Movement model with the visitor's ID as the filename
        qr_code_filename = f"{self.visitor.id_passport_nbr}.png"
        self.qr_code.save(qr_code_filename, File(img_temp), save=True)

        # Close the buffer
        buffer.close()

        return self.qr_code
        #delete qr when user checks out
    def delete_qr_codes(self):
        # Get the visitor ID of the current movement
        visitor_id = self.visitor.id_passport_nbr

        # Get the directory path where QR code files are stored
        qr_codes_dir = os.path.join(settings.MEDIA_ROOT, 'qr_codes')

        # List all the files in the QR codes directory
        qr_code_files = os.listdir(qr_codes_dir)

        # Iterate through the files and delete the ones that contain the visitor ID
        for file_name in qr_code_files:
            if visitor_id in file_name:
                file_path = os.path.join(qr_codes_dir, file_name)
                try:
                    os.remove(file_path)
                except Exception as e:
                    # Handle any errors that might occur while deleting the files
                    print(f"Error deleting file: {e}")
    def save(self, *args, **kwargs):
        # Check if the movement is being saved and has a time_out value (i.e., the visitor is checking out)
        if self.pk and self.time_out:
            # Delete the QR codes associated with the visitor
            self.delete_qr_codes()

        # Call the original save method to save the movement instance
        super().save(*args, **kwargs)
class Log(models.Model):
    action_choices = [
        ('APPROVE', 'Approved Visitor'),
        ('CHECKOUT', 'Check Out Visitor'),
        ('DECLINE', 'Declined Visitor'),
        ('RECORD', 'Recorded a Visitor')
        # Add more action choices as needed
    ]
    action = models.CharField(max_length=20, choices=action_choices)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    visitor_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.action} - {self.user} - {self.timestamp}"

