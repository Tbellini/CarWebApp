from django.db import models
import hashlib
from django import forms
from passlib.hash import sha256_crypt
from django.core.validators import MinLengthValidator
from datetime import date
from django.contrib.auth.models import User

# Create your models here.

class Car(models.Model):
    name=models.CharField(max_length=200) #nome veicolo
    model=models.CharField(max_length=200) #modello
    licenseplate=models.CharField(max_length=200) #targa
    doors=models.CharField(max_length=200) #portiere
    seats=models.CharField(max_length=200) #posti a sedere

    def __str__(self):
        return self.model

class CarBooked(models.Model):
    frombooked = models.DateField(verbose_name=u"Da",default=date.today)
    tobooked = models.DateField(verbose_name=u"a",default=date.today)
    place = models.CharField(verbose_name=u"Dove?", max_length=30)
    note = models.TextField(default=None)

    username = models.ManyToManyField(User)
    model = models.ForeignKey(Car,on_delete=models.CASCADE)

    def valuta(self, datainit,datafine):

        import datetime
        if self.frombooked <= datainit <= self.tobooked:
            print(datainit)
            return "In mezzo"
        else:
            print(datainit)
            return "fuori"
