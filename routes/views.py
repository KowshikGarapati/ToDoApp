from django.shortcuts import render , redirect, get_object_or_404 
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

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')  # Replace with your list view name
    else:
        form = TaskForm(instance=task)
    return render(request, 'edit_task.html', {'form': form})


# views.py
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('task_list')
    #return render(request, 'confirm_delete.html', {'task': task})
