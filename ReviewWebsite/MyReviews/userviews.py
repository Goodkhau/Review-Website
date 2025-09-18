from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .userform import RegistrationForm
from .tokens import account_activation_token
from .models import User

def profilepage(request, pk):
    user = User.objects.get(id=pk)
    reviews = user.review_set.all()
    context = {'reviews': reviews}
    return render(request, 'MyReviews/userprofile.html', context)

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home-page')

    if not request.POST:
        context = {}
        return render(request, 'MyReviews/loginpage.html', context)
    
    username = request.POST["username"]
    password = request.POST["password"]

    try:
        user = User.objects.get(username=username)
    except:
        messages.error(request, 'User does not exist')
    
    user = authenticate(username=username, password=password)

    if user is None:
        messages.error(request, 'Username or Password does not exist.')
    
    login(request, user)
    return redirect('home-page')

def logoutrequest(request):
    if not request.user.is_authenticated:
        return redirect('login-page')
    
    logout(request)
    return redirect('home-page')

def registerpage(request):
    form = RegistrationForm

    if not request.POST:
        context = {'form': form}
        return render(request, 'MyReviews/registerpage.html', context)
    
    form = RegistrationForm(request.POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(request)
        mail_subject = "Activate your account."
        message = render_to_string('MyReviews/activateaccount.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage (
            mail_subject, message, to=[to_email]
        )
        email.send()
        return HttpResponse('Your account activation link has been sent.\nYou can close this tab.')
    else:
        message = "Form was invalid"
        context = {'message': message, 'form': form}
        return render(request, 'MyReviews/registerpage.html', context)
    
def activate(request, uidb64, token):
    try:
        uid = int(force_str(urlsafe_base64_decode(uidb64)))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is None:
        return HttpResponse('User does not exist!')

    if account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home-page')
    else:
        return HttpResponse('Token is invalid!')
    