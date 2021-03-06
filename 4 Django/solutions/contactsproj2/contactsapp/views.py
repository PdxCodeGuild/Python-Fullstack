from django.shortcuts import render, reverse, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import ContactForm
from .models import Contact
import requests

from django.conf import settings


# from django.contrib.auth import login as login_user
import django.contrib.auth

def index(request):
    return render(request, 'contactsapp/index.html')

def register(request):

    if request.method == 'POST': # receiving form submission

        # recaptcha
        recaptcha_data = {
            'response': request.POST['g-recaptcha-response'],
            'secret': settings.RECAPTCHA_SECRET_KEY
        }
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=recaptcha_data)

        if (response.json()['success'] == False):
            message = 'invalid_recaptcha'
            return render(request, 'contactsapp/register.html', {'message': message})
        
        # get data out of form submission
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        retype_password = request.POST['retype_password']

        if password != retype_password:
            message = 'passwords_dont_match'
            return render(request, 'contactsapp/register.html', {'message': message})

        # if a user doesn't exist with that username
        if User.objects.filter(username=username).exists():
            message = 'user_already_exists'
            return render(request, 'contactsapp/register.html', {'message': message})

             
        # create the user
        user = User.objects.create_user(username, email, password)
        # log the user in (sets a cookie)
        django.contrib.auth.login(request, user)
        # redirect to the home page
        return HttpResponseRedirect(reverse('contactsapp:home'))
            
    return render(request, 'contactsapp/register.html', {'recaptcha_public_key': settings.RECAPTCHA_PUBLIC_KEY})


def login(request):
    message = ''
    if request.method == 'POST':
        print(request.GET)
        username = request.POST['username']
        password = request.POST['password']
        user = django.contrib.auth.authenticate(request, username=username, password=password)
        if user is None:
            message = 'not_found'
        else:
            # log the user in (sets a cookie)
            django.contrib.auth.login(request, user)
            next = request.GET.get('next', reverse('contactsapp:home'))
            # redirect to the next page
            return HttpResponseRedirect(next)
    return render(request, 'contactsapp/login.html', {'message': message})

def logout(request):
    django.contrib.auth.logout(request)
    return HttpResponseRedirect(reverse('contactsapp:login'))

@login_required
def home(request):
    # contacts = Contact.objects.filter(user=request.user)
    # contacts = Contact.objects.filter(user_id=request.user.id)
    contacts = request.user.contacts.all()
    context = {
        'contacts': contacts
    }
    return render(request, 'contactsapp/home.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.instance)

            # form.save()
            # return HttpResponseRedirect(reverse('contactsapp:home'))

            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            return HttpResponseRedirect(reverse('contactsapp:home'))
    else:
        form = ContactForm()
    context = {
        'form': form
    }
    return render(request, 'contactsapp/create.html', context)

@login_required
def edit(request, contact_id):
    # contact = request.user.contacts.get(id=contact_id)
    # contact = get_object_or_404(request.user.contacts, id=contact_id)
    contact = get_object_or_404(Contact, id=contact_id, user=request.user)
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=contact)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('contactsapp:home'))
    else:
        form = ContactForm(instance=contact)
    context = {
        'form': form
    }
    return render(request, 'contactsapp/edit.html', context)