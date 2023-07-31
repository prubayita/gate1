from django.db import models

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

    def __str__(self):
        return f"{self.first_name} {self.surname}"

class Card(models.Model):
    name= models.CharField(max_length=50)
    number = models.IntegerField(max_length=50)

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
    card = models.OneToOneField(Card, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.visitor} - Time In: {self.time_in} - Time Out: {self.time_out}"
