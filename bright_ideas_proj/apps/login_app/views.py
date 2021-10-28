from django.shortcuts import render, redirect
from django.contrib import messages
from .models import * 
import bcrypt

def index(request):
    request.session.flush()
    context = {

    }
    return render(request, 'index.html', context)


def success(request):
    if 'user_id' not in request.session:
        messages.error(request, "Please log in.")
        return redirect('/')

    context = {
        'this_user' : User.objects.get(id = request.session['user_id'])
    }
    return render(request, 'success.html', context)


def register(request):
    if request.method != 'POST':
        return redirect('/')
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt(14)).decode()

        #create a new user in the database
    new_user = User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = hashed_pw,
    )
    # store the user's id in the request.session
    request.session['user_id'] = new_user.id
    return redirect('/success')


def login(request):
    if request.method != 'POST':
        return redirect('/')
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    # find the user that is logging in
    this_user = User.objects.filter(email = request.POST['email'])[0]
    # put the user id in the request.session
    request.session['user_id'] = this_user.id
    messages.success(request, "Congrats on logging in.")
    return redirect('/success')


def logout(request):
    request.session.flush()
    return redirect('/')