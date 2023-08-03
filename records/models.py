from django.db import models
from django.contrib.auth.models import User

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
    # visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, to_field='id_passport_nbr')
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

    def __str__(self):
        return f"{self.visitor} - Time In: {self.time_in} - Time Out: {self.time_out}"

class Log(models.Model):
    action_choices = [
        ('APPROVE', 'Approved Visitor'),
        ('CHECKOUT', 'Check Out Visitor'),
        ('DECLINE', 'Declined Visitor'),
        # Add more action choices as needed
    ]
    action = models.CharField(max_length=20, choices=action_choices)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    visitor_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.action} - {self.user} - {self.timestamp}"

       
