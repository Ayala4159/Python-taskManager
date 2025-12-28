from django.shortcuts import render, redirect
from .forms import SignUpForm, SignInForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm


def wellcome(request):
    return render(request, 'Wellcome.html')


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.username = form.cleaned_data['email']
            user.save()
            return redirect("wellcome")
    else:
        form = SignUpForm()
    return render(request, 'SignUp.html', {'form': form})


def sign_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            print("Success1 - המשתמש אומת ומתבצע ניתוב")
            return redirect("wellcome")
        else:
            print("שגיאה: פרטי התחברות לא נכונים")
            print(form.errors)
    else:
        form = AuthenticationForm()

    return render(request, 'SignIn.html', {'form': form})