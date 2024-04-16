from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm,UserChangeForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm, ProfileForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, 'home.html')

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    
    return render(request, 'tasks_folder/tasks.html', {
        'tasks':tasks, 'title':'Tasks to do'
    })

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks_folder/tasks.html', {'tasks':tasks, 'title':'Tasks completed'})

@login_required
def task_details(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'GET':
        formm = TaskForm(instance=task)
        return render(request, 'tasks_folder/task_details.html', {
            'task':task, 'formm':formm})
    else:
        try:
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'tasks_folder/task_details.html', {
            'task':task, 'formm':formm, 'error':'Error Updating task'})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

def create_task(request):
    if request.method == 'GET':
        return render(request, 'tasks_folder/create_task.html', {
        'form': TaskForm
    })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except:
            if request.user.is_authenticated:
                return render(request, 'tasks_folder/create_task.html', {
                'form': TaskForm, 'error': 'Please provide valid data'})
                
            else:
                return render(request, 'tasks_folder/create_task.html', {
                'form': TaskForm, 'error': 'Please login / signup'})

def signup(request):

    if request.method == 'GET':
        return render(request, 'user/signup.html', {
            'form': UserCreationForm})

    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'user/signup.html', {
                    'form': UserCreationForm,
                    'message': 'User already exists'})
            except ValueError:
                return render(request, 'user/signup.html', {
                    'form': UserCreationForm,
                    'message': 'Please provide valid data'})

        return render(request, 'user/signup.html', {
            'form': UserCreationForm,
            'message': "Passwords don't match"})

@login_required          
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'user/signin.html', {
            'form':AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'user/signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('tasks')

@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        user_form = UserChangeForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            new_username = user_form.cleaned_data.get('username')
            if User.objects.filter(username=new_username).exclude(pk=user.pk).exists():
                messages.error(request, "Username already exists.")
                return redirect('profile')
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        user_form = UserChangeForm(instance=user)
        profile_form = ProfileForm(instance=user.profile)
    return render(request, 'user/profile.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            confirm_password = form.cleaned_data.get('confirm_password')
            current_password = form.cleaned_data.get('current_password')
            
            # Check if new passwords match
            if password and confirm_password and password != confirm_password:
                messages.error(request, "New passwords do not match.")
                return redirect('update_profile')

            # Check if current password is correct
            if current_password and not user.check_password(current_password):
                messages.error(request, "Current password is incorrect.")
                return redirect('update_profile')

            # Change password if new one provided
            if password:
                user.set_password(password)
                user.save()
                messages.success(request, "Password changed successfully.")
                return redirect('home')

            # Save other user fields
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('home')
    else:
        form = UserChangeForm(instance=user)
    return render(request, 'user/update_profile.html', {'form': form})


@login_required
def profile_details(request):
    user = request.user
    return render(request, 'user/profile_details.html', {'user': user})
