from django.shortcuts import render, redirect, get_object_or_404
from .models import Target
from .forms import TargetForm

def index(request):
    return render(request, 'base.html')

# Target CRUD
def target_list(request):
    targets = Target.objects.all()
    return render(request, 'target/target_list.html', {'targets': targets})

def target_create(request):
    if request.method == 'POST':
        form = TargetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('target:target_list')
    else:
        form = TargetForm()
    return render(request, 'target/target_form.html', {'form': form})

def target_update(request, pk):
    target = get_object_or_404(Target, pk=pk)
    if request.method == 'POST':
        form = TargetForm(request.POST, instance=target)
        if form.is_valid():
            form.save()
            return redirect('target:target_list')
    else:
        form = TargetForm(instance=target)
    return render(request, 'target/target_form.html', {'form': form})

def target_delete(request, pk):
    target = get_object_or_404(Target, pk=pk)
    if request.method == 'POST':
        target.delete()
        return redirect('target:target_list')
    return render(request, 'target/target_confirm_delete.html', {'target': target})
