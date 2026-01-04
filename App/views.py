from django.shortcuts import render, redirect
from .forms import SignUpForm, SignInForm, AddTeamForm, JoinTeamForm
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction
from .models import Team


def wellcome(request):
    return render(request, 'Wellcome.html')


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user_data = form.cleaned_data
            request.session['temp_user_data'] = user_data
            if user_data['role'] == 'Manager':
                return redirect('create_team')
            return redirect('select_team')
    else:
        form = SignUpForm()
    return render(request, 'User/SignUp.html', {'form': form})


def sign_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("wellcome")
    else:
        form = AuthenticationForm()
    return render(request, 'User/SignIn.html', {'form': form})


def create_team(request):
    User = get_user_model()
    user_data = request.session.get('temp_user_data')
    if not user_data:
        return redirect('sign_up')
    if request.method == 'POST':
        form = AddTeamForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    team_name_val = form.cleaned_data['team_name']
                    if Team.objects.filter(team_name=team_name_val).exists():
                        form.add_error('team_name', 'This team name already exists')
                    else:
                        new_team = Team.objects.create(team_name=team_name_val)
                        user = User.objects.create_user(
                            username=user_data['email'],
                            email=user_data['email'],
                            password=user_data['password'],
                            first_name=user_data['first_name'],
                            last_name=user_data['last_name'],
                            role=user_data['role'],
                            team=new_team
                        )
                        del request.session['temp_user_data']
                        login(request, user)
                        return redirect('wellcome')
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = AddTeamForm()
    return render(request, 'Team/CreateTeam.html', {'form': form})


def select_team(request):
    User = get_user_model()
    # 1. שליפת הנתונים מהסשן כבר בהתחלה
    user_data = request.session.get('temp_user_data')

    # 2. הגנה: אם המשתמש הגיע לדף בלי לעבור ב-Sign Up
    if not user_data:
        return redirect('sign_up')

    if request.method == 'POST':
        form = JoinTeamForm(request.POST)
        if form.is_valid():
            try:
                selected_team = form.cleaned_data['team']
                with transaction.atomic():
                    if User.objects.filter(email=user_data['email']).exists():
                        form.add_error(None, "משתמש עם אימייל זה כבר נרשם במערכת")
                        return render(request, 'Team/SelectTeam.html', {'form': form})
                    user = User.objects.create_user(
                        username=user_data['email'],
                        email=user_data['email'],
                        password=user_data['password'],
                        first_name=user_data.get('first_name', ''),
                        last_name=user_data.get('last_name', ''),
                        role=user_data.get('role'),
                        team=selected_team
                    )
                    request.session.pop('temp_user_data', None)
                    login(request, user)

                    return redirect('wellcome')

            except Exception as e:
                form.add_error(None, f"An error occurred during the registration process: {str(e)}")
    else:
        form = JoinTeamForm()

    return render(request, 'Team/SelectTeam.html', {'form': form})


def add_task():
    return None


def get_tasks():
    return None