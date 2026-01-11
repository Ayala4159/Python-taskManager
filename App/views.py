from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.defaults import bad_request

from .forms import SignUpForm, AddTeamForm, JoinTeamForm, AddTaskForm
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction
from .models import Team, Task, User


def welcome(request):
    if request.user.is_authenticated:
        return redirect('get_tasks')
    return render(request, 'Welcome.html')


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('get_tasks')
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
    if request.user.is_authenticated:
        return redirect('get_tasks')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("get_tasks")
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
                        return redirect('get_tasks')
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = AddTeamForm()
    return render(request, 'Team/CreateTeam.html', {'form': form})


def select_team(request):
    User = get_user_model()
    user_data = request.session.get('temp_user_data')
    teams = Team.objects.all()
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

                    return redirect('get_tasks')

            except Exception as e:
                form.add_error(None, f"An error occurred during the registration process: {str(e)}")
    else:
        form = JoinTeamForm()
    context = {'form': form, 'teams': teams}
    return render(request, 'Team/SelectTeam.html', context)



@login_required
def add_task(request):
    if request.user.role != 'Manager':
        raise PermissionDenied
    if request.method == 'POST':
        form = AddTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.status="NEW_TASK"
            task.team = request.user.team
            task.save()
            return redirect('get_tasks')
    else:
        form = AddTaskForm()
    return render(request, 'Task/AddTask.html', {'form': form})

@login_required()
def get_tasks(request):
    tasks = Task.objects.filter(team=request.user.team)
    team= request.user.team
    users= User.objects.filter(team=team)
    status_filter = request.GET.get('status')
    query = request.GET.get('q')
    if query:
        tasks = Task.objects.filter(
            Q(owner__first_name__icontains=query) |
            Q(owner__last_name__icontains=query)
        )
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    context = {'tasks': tasks, 'team': team, 'users': users}
    now = timezone.now().date()
    for task in tasks:
        if task.end_date < now and task.status != 'EXPIRED' and task.status != 'DONE':
            task.status = 'EXPIRED'
            task.save()
    return render(request, 'Task/GetTasks.html', context)

@login_required
def delete_task(request, task_id):
    if request.user.role != 'Manager':
        raise PermissionDenied
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id, team=request.user.team)
        task.delete()
        return redirect('get_tasks')
    return bad_request()


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, team=request.user.team)
    
    if request.user.role != 'Manager':
        raise PermissionDenied("רק מנהלים יכולים לערוך משימות")

    if not task.status=="NEW":
        raise PermissionDenied("לא ניתן לערוך משימה שהושלמה")


    if request.method == 'POST':
        form = AddTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('get_tasks')
    else:
        form = AddTaskForm(instance=task)
    context = {
        'form': form,
        'task': task
    }
    return render(request,  'Task/AddTask.html', context)

@login_required
def update_owner(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id, team=request.user.team)
        new_owner_id = request.POST.get('user_id')
        
        if request.user.role == 'Manager':
            if not task.owner and new_owner_id:
                new_owner = get_object_or_404(User, id=new_owner_id)
                task.owner = new_owner
                task.status = "ON_PROCESS"
                task.save()
        else:
            if not task.owner and task.status != 'EXPIRED' and int(new_owner_id) == request.user.id:
                task.owner = request.user
                task.status = "ON_PROCESS"
                task.save()
        
        return redirect('get_tasks')
    return redirect('get_tasks')

@login_required
def update_status(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id, team=request.user.team)
        
        if task.owner and task.owner.id == request.user.id and task.status != 'DONE':
            task.status = "DONE"
            task.save()
        
        return redirect('get_tasks')
    return redirect('get_tasks')

@login_required
def logout_view(request):
    logout(request)
    return redirect('welcome')