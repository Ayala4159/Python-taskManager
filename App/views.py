from django.shortcuts import render


def wellcome(request):
    return render(request, 'Wellcome.html')


def sign_in(request):
    return render(request, 'SignIn.html')


def sign_up(request):
    return render(request, 'SignUp.html')
