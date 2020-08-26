from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from account.forms import LoginForm


def log_in(request):
    next_url = request.GET.get('next', reverse('items:dashboard'))
    if request.user.is_authenticated:
        return redirect(next_url)
    form = LoginForm()
    if request.method == 'POST':
        user = authenticate(username=request.POST['email'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect(next_url)
        else:
            messages.error(request, _('Login or Password incorrect. Try again'))
    return render(
        request,
        'account/auth-login.html',
        {
            'title': _('login'),
            'form': form
        }
    )

