from django.shortcuts import render

# Create your views here.
# tasks/views.py
from django.shortcuts import render, redirect
from .models import Project, Task
from .forms import ProjectForm, TaskForm

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'tasks/project_list.html', {'projects': projects})

def task_list(request, project_id):
    project = Project.objects.get(id=project_id)
    tasks = Task.objects.filter(project=project)
    return render(request, 'tasks/task_list.html', {'project': project, 'tasks': tasks})

def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'tasks/create_project.html', {'form': form})

def create_task(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('task_list', project_id=project_id)
    else:
        form = TaskForm(initial={'project': project})
    return render(request, 'tasks/create_task.html', {'form': form, 'project': project})

