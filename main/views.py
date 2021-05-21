from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Todo
from .forms import TodoForm


# Create your views here.
def homepage(request):
    todos = Todo.objects.all()
    return render(request, 'main/mytodos.html', {'todos': todos})

def todo_list(request):
    todos = Todo.objects.all()
    return render(request, 'main/todo_list.html', {'todos': todos})

def todo_detail(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    return render(request, 'main/todo_detail.html', {'todo': todo})

def todo_new(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.author = request.user
            todo.published_date = timezone.now()
            todo.save()
            return redirect('todo_detail', pk=todo.pk)
    else:
        form = TodoForm()
    return render(request, 'main/todo_edit.html', {'form': form})

def todo_edit(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == "POST":
        form = TodoForm(request.POST, request.FILES, instance=todo)
    
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.created_date = timezone.now()
            todo.save()
            return redirect('todo_detail', pk=todo.pk)
    else:
        form = TodoForm(instance=todo)
    return render(request, 'main/todo_edit.html', {'form': form})
