from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory
from .models import Collection
from .forms import CollectionForm


def index(request):
    return redirect('collection_list')


def collection_list(request):
    collections = Collection.objects.all()
    return render(request, 'collection/collection_list.html', {'collections': collections})


def collection_create(request):
    if request.method == 'POST':
        form = CollectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('collection_list')
    else:
        form = CollectionForm()
    return render(request, 'collection/collection_form.html', {'form': form})


def collection_update(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    if request.method == 'POST':
        form = CollectionForm(request.POST, instance=collection)
        if form.is_valid():
            form.save()
            return redirect('collection_list')
    else:
        form = CollectionForm(instance=collection)
    return render(request, 'collection/collection_form.html', {'form': form})


def collection_delete(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    if request.method == 'POST':
        collection.delete()
        return redirect('collection_list')
    return render(request, 'collection/collection_confirm_delete.html', {'collection': collection})
