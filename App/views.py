from django.shortcuts import render
from .forms import SignUpForm


def wellcome(request):
    return render(request, 'Wellcome.html')


def sign_in(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = SignUpForm()
    return render(request, 'SignIn.html', {'form': form})


def sign_up(request):
    return render(request, 'SignUp.html')
