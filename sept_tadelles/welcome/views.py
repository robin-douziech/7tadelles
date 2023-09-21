from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail

from account.views import helpers

# Create your views here.

def index(request) :

    current_view = ['welcome:index', []]
    real_view = True

    btn_list = []
    if request.user.is_authenticated :
        btn_list = [
            ("déconnexion", "account:logout", "", ()),
            ("mon compte", "account:detail", f"?id={request.user.id}", ())
        ]
    else :
        btn_list = [("connexion", "account:login", "", ())]

    helpers.register_view(request, current_view, real_view)
    return render(request, 'welcome/index.html', {"buttons": btn_list})