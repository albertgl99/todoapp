from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.http import JsonResponse

def task_list(request):
    # Processa només les peticions AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET.get('q', '').strip()
        tasks = Task.objects.filter(title__icontains=query) if query else Task.objects.all()
        tasks_data = [{'id': task.id, 'title': task.title, 'completed': task.completed} for task in tasks]
        incomplete_tasks_count = tasks.filter(completed=False).count()
        return JsonResponse({'tasks': tasks_data})

    # Processa la pàgina principal si no és AJAX
    tasks = Task.objects.all()
    incomplete_tasks_count = tasks.filter(completed=False).count()
    
    if request.method == 'POST' and 'complete_task_id' in request.POST:
        task_id = request.POST.get('complete_task_id')
        task = get_object_or_404(Task, id=task_id)
        task.completed = True
        task.save()
        task.delete()
        return redirect('task_list')

    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'incomplete_tasks_count': incomplete_tasks_count,
        })

def add_task(request):
    if request.method == 'POST':
        title = request.POST['title']
        Task.objects.create(title=title)
        return redirect('task_list')
    return render(request, 'tasks/add_task.html')

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.title = request.POST['title']
        task.completed = 'completed' in request.POST  # Marcar com a completada si el checkbox està seleccionat
        task.save()
        return redirect('task_list')
    return render(request, 'tasks/edit_task.html', {'task': task})



