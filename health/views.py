import json
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Feedback, Profile, Doctor, Questions, Symptoms, Disease
from .data import symptoms_list
import infermedica_api
# Create your views here.

def home(request):
	return render(request, 'home.html')


def signup(request):
	if request.method == 'POST':
		if request.POST['pass1'] == request.POST['pass2'] and len(request.POST['pass1']) > 8 :
			try:
				user = User.objects.get(username=request.POST['uname'])
				context = {
					'error': 'Username already taken.'
				}
				return render(request, 'signup.html', context)
			except User.DoesNotExist:
				user = User.objects.create_user(username=request.POST['uname'], password=request.POST['pass1'])
				auth.login(request, user)
				return redirect('login')
		else:
			context = {
				'error': 'Password must match or Length of Password must be greater than 8.'
			}
			return render(request, 'signup.html', context)
	else:
		return render(request, 'signup.html')


def login(request):
	if request.method == 'POST':
		user = auth.authenticate(username=request.POST['uname'], password=request.POST['pass1'])
		if user is not None:
			auth.login(request,user)
			# question = Questions.objects.filter(user_id=request.user.id)
			profile = Profile.objects.filter(user_id=request.user.id)
			if profile:
				return redirect('index')
			else:
				return redirect('add_profile')
		else:
			context = {
				'error': 'Username or password is incorrect.'
			}
			return render(request, 'login.html', context)
	else:
		return render(request, 'login.html')


def logout(request):
	if request.method == 'POST':
		auth.logout(request)
		return redirect('home')


def index(request):
	profile = Profile.objects.filter(user_id = request.user.id)
	context = {
		'profile': profile
	}
	return render(request, 'index.html', context)


def feedback(request):
	if request.method == 'POST':
		feed = request.POST['feed']
		if feed != '':
			feedback = Feedback(feedback = feed, user_id = request.user.id)
			feedback.save()
			return redirect('index')
		else:
			context = {
				'error': "Feedback can't be blank."
			}
			return render(request, 'feedback.html', context)
	return render(request, 'feedback.html')



def add_profile(request):
	if request.method == 'POST':
		profile = Profile(fname = request.POST['fname'], lname = request.POST['lname'],
						  age = request.POST['age'],  contact = request.POST['contact'], gender = request.POST['gender'].capitalize(),
						  email = request.POST['email'], street = request.POST['street'], city = request.POST['city'],
						  state = request.POST['state'], pincode = request.POST['pin'],user_id = request.user.id)
		profile.save()
		return redirect('question')
	return render(request, 'add_profile.html')


def see_profile(request):
	profile = Profile.objects.filter(user_id = request.user.id)
	context = {
		'profile': profile
	}
	return render(request, 'see_profile.html', context)


def doctor(request):
	query = Doctor.objects.all()

	if 'name' in request.GET:
		name = request.GET['name']
		if name:
			query = query.filter(name__icontains=name)

	if 'category' in request.GET:
		category = request.GET['category']
		if category:
			query = query.filter(category__icontains=category)

	if 'address' in request.GET:
		address = request.GET['address']
		if address:
			query = query.filter(address__icontains=address)

	return render(request, 'doctor.html', {'query': query})


def question(request):
	gender = Profile.objects.filter(user_id=request.user.id).filter(gender='Female')
	person = Profile.objects.get(user_id=request.user.id)
	print(person.fname)
	if request.method == 'POST':
		questions = Questions(pregnant = request.POST['pregnant'], weight = request.POST['weight'],
						  cigarettes = request.POST['cig'], injured = request.POST['inj'],
						  cholestrol = request.POST['ch'], hypertension = request.POST['hyp'],
						  user_id = request.user.id)
		questions.save()
		return redirect('index')
	context = {
		'gender': gender,
		'person': person,
	}
	return render(request, 'question.html', context)


def api_function(array):
	api = infermedica_api.configure(app_id='', app_key='') # Your app_id and app_key (from infermedica)
	request = infermedica_api.Diagnosis(sex='male', age=35)
	for i in array:
		request.add_symptom(i, 'present')
	request = api.diagnosis(request)

	result = request.conditions[0]['name']
	return result


def check_disease(request):
	pro = Profile.objects.get(user_id = request.user.id)
	# symptoms_from_database = Symptoms.objects.all()
	result = ''
	symptoms_names = []
	if request.method == 'POST':
		symptoms_ids = request.POST.getlist('disease')
		result = api_function(symptoms_ids)
		print(result)
		print(symptoms_ids)
		symptoms_names = []
		for id in symptoms_ids:
			if id in symptoms_list:
				symptom_name = symptoms_list[id]
				symptoms_names.append(symptom_name)
		print(symptoms_names)
		disease = Disease(ids_of_selected_symptoms=symptoms_ids, name_of_selected_symptoms=symptoms_names,
						  result_of_predicted_disease=result, user_id = request.user.id)
		disease.save()
	context = {
		'result': result,
		'user': pro,
		'symptoms': symptoms_names
	}
	return render(request, 'check_disease.html', context)
