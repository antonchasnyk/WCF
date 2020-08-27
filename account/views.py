from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.urls import reverse, reverse_lazy

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


def log_out(request):
    logout(request)
    return redirect(reverse('account:login'))


@login_required(login_url=reverse_lazy('account:login'))
def profile_detail(request):
    return render(
        request,
        'account/profile.html'
    )

