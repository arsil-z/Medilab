from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Feedback(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	feedback = models.TextField()

	def __str__(self):
		return self.user.username

class Profile(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	fname = models.CharField(max_length=20)
	lname = models.CharField(max_length=20)
	age = models.IntegerField()
	contact = models.IntegerField()
	gender = models.CharField(max_length=10)
	email = models.CharField(max_length=50)
	street = models.CharField(max_length=200)
	city = models.CharField(max_length=200)
	state = models.CharField(max_length=200)
	pincode = models.IntegerField()

	def __str__(self):
		return self.fname


class Doctor(models.Model):
	name = models.CharField(max_length=50)
	category = models.CharField(max_length=200)
	contact = models.IntegerField()
	address = models.TextField()

	def __str__(self):
		return self.name


class Questions(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	pregnant = models.CharField(max_length=50, blank=True)
	weight = models.CharField(max_length=50)
	cigarettes = models.CharField(max_length=50)
	injured = models.CharField(max_length=50)
	cholestrol = models.CharField(max_length=50)
	hypertension = models.CharField(max_length=50)

	def __str__(self):
		return self.user.username


class Symptoms(models.Model):
	symptom_id = models.CharField(max_length=15)
	symptom_name = models.CharField(max_length=200)

	def __str__(self):
		return self.symptom_name

class Disease(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	ids_of_selected_symptoms = ArrayField(ArrayField(models.CharField(max_length=100)))
	name_of_selected_symptoms = ArrayField(ArrayField(models.CharField(max_length=500)))
	result_of_predicted_disease = models.CharField(max_length=100)

	def __str__(self):
		return self.user.username
