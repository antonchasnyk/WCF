from django.shortcuts import render

# Create your views here.


def error_404(request, *args, **kwargs):
    data = {}
    return render(request, 'errors-404.html', data)


def error_403(request, *args, **kwargs):
    data = {}
    return render(request, 'errors-403.html', data)


def error_500(request, *args, **kwargs):
    data = {}
    return render(request, 'errors-500.html', data)


def error_503(request, *args, **kwargs):
    data = {}
    return render(request, 'errors-503.html', data)
