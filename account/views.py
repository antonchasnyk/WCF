from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.urls import reverse, reverse_lazy

from account.forms import LoginForm, ProfileForm, UserForm


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
            messages.error(request, _('Login or Password incorrect'))

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
@transaction.atomic
def profile_detail(request, user_id=-1):
    if user_id == -1:
        user_id = request.user.pk
    user = get_object_or_404(User, pk=user_id)
    ami = False
    user_form = None
    profile_form = None
    if request.user == user:
        ami = True
        if request.method == 'POST':
            user_form = UserForm(request.POST, instance=request.user)
            profile_form = ProfileForm(request.POST, instance=request.user.profile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                return redirect("account:profile_detail")
            else:
                messages.error(request, _('Input incorrect'), extra_tags='alert-danger')
        else:
            user_form = UserForm(instance=request.user)
            profile_form = ProfileForm(instance=request.user.profile)
    return render(
        request,
        'account/profile.html',
        {'user_profile': user,
         'ami': ami,
         'user_form': user_form,
         'profile_form': profile_form,
         }
    )


@login_required(login_url=reverse_lazy('account:login'))
def team(request):
    user_list = User.objects.all().prefetch_related('profile')
    return render(
        request,
        'account/team.html',
        {'team': user_list}
    )


@login_required(login_url=reverse_lazy('account:login'))
def upload_user_avatar(request):
    if request.method == 'POST':
        if request.FILES:
            try:
                uploaded = request.FILES['avatar']
                if uploaded.size > 100000:
                    return HttpResponseNotAllowed(_('avatar to large'))
                request.user.profile.avatar.save(request.user.username+'.png', uploaded.file)
            except KeyError:
                return HttpResponseNotAllowed('Image file corrupted')
    return HttpResponse('')
