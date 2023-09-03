from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail

# Create your views here.

def index(request) :
    btn_list = []
    if request.user.is_authenticated :
        btn_list = [
            ("déconnexion"    ,"account:logout"         , ()),
            ("mon compte", "account:detail", ())
            ]
    else :
        btn_list = [("login", "account:login", ())]
    return render(request, 'welcome/index.html', {"buttons": btn_list})