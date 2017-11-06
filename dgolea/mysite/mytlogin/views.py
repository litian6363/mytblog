import re, hashlib

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from .config import session
from .models import Users


def signin(request):
    return render(request, 'mytlogin/signin.html')


def signup(request):
    return render(request, 'mytlogin/signup.html')


def complete(request):
    message_text = request.POST['message_text']
    return render(request, 'mytlogin/complete.html', message_text)


_re_email = re.compile(r'^(\w)+(\.\w)*\@(\w)+((\.\w{2,3}){1,3})$')
cookie_name = session['cookie_name']


def save_user(request):
    email = request.POST['email']
    password = request.POST['password']
    if not email or not _re_email.match(email):
        return render(request, 'mytlogin/signup.html', {
            'error_message': 'Invalid email.',
        })
    if not password:
        return render(request, 'mytlogin/signup.html', {
            'error_message': 'Invalid password.',
        })
    if Users.objects.filter(email=email):
        return render(request, 'mytlogin/signup.html', {
            'error_message': 'This email has been registered.',
        })
    email_password_key = '%s:%s:%s' % (email, password, session['secret'])
    sha1_password = hashlib.sha1(email_password_key.encode('utf-8')).hexdigest()
    use = Users(email=email, password=sha1_password, create_date=timezone.now())
    use.save()
    re = render(request, 'mytlogin/complete.html', {'massage_text': '注册成功！'})
    re.set_cookie(cookie_name, use[0].email)
    return re


def check_user(request):
    email = request.POST['email']
    password = request.POST['password']
    if not email:
        return render(request, 'mytlogin/signin.html', {
            'error_message': 'Invalid email.',
        })
    if not password:
        return render(request, 'mytlogin/signin.html', {
            'error_message': 'Invalid password.',
        })
    email_password_key = '%s:%s:%s' % (email, password, session['secret'])
    sha1_password = hashlib.sha1(email_password_key.encode('utf-8')).hexdigest()
    use = Users.objects.filter(email=email, password=sha1_password)
    if len(use) == 0 :
        return render(request, 'mytlogin/signin.html', {
            'error_message': 'Eamil or password not exist.',
        })
    re = render(request, 'mytlogin/complete.html', {'massage_text': '登陆成功！'})
    re.set_cookie(cookie_name, use[0].email)
    return re


def logout(request):
    re = render(request, 'mytlogin/complete.html', {'massage_text': '登出成功！'})
    re.delete_cookie(cookie_name)
    return re
