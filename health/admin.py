from django.contrib import admin
from .models import Doctor,Feedback, Profile, Questions, Symptoms, Disease
# Register your models here.
admin.site.register(Doctor)
admin.site.register(Feedback)
admin.site.register(Profile)
admin.site.register(Questions)
admin.site.register(Symptoms)
admin.site.register(Disease)
