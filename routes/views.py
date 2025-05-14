from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import Task
from .forms import TaskForm

# Create your views here.

def task_list(request):
    return render(request, 'tasks.html', {"tasks" : Task.objects.all()} )

def home(request):
    pass


def savenewtask(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
            
    return HttpResponse(form.cleaned_data['date'])

def newtask(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm()
    return render(request, 'newtask.html', {'form': form})

    
