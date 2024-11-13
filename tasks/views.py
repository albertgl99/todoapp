from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.http import JsonResponse

def task_list(request):
    tasks = Task.objects.all()  # Obtenim totes les tasques per defecte

    # Si es clica el cercle per completar i esborrar la tasca
    if request.method == 'POST' and 'complete_task_id' in request.POST:
        task_id = request.POST.get('complete_task_id')
        task = get_object_or_404(Task, id=task_id)
        task.completed = True  # Marca com a completada
        task.save()
        task.delete()  # Esborra la tasca immediatament després de marcar-la com a completada
        return redirect('task_list')

    return render(request, 'tasks/task_list.html', {'tasks': tasks})

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

