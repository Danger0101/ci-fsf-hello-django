from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from .models import Item
from .forms import ItemForm


# Create your views here.
def get_todo_list(request):
    """
    Retrieve the list of todo items and render them in the todo_list.html template.

    Args:
        request: The HTTP request object.

    Returns:
        A rendered HTML response containing the todo items.
    """
    items = Item.objects.all()
    context = {
        'items': items
    }
    return render(request, 'todo/todo_list.html', context)


def add_item(request):
    """
    View function to handle adding an item to the todo list.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.

    """
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid (): # if the form is valid, save it
            form.save()
        return redirect('get_todo_list')
    form = ItemForm()
    context = {
        'form': form
    }
    return render(request, 'todo/add_item.html', context)



def edit_item(request, item_id):
    """
    Edit an item with the given item_id.

    Args:
        request (HttpRequest): The HTTP request object.
        item_id (int): The ID of the item to be edited.

    Returns:
        HttpResponse: The HTTP response object.

    Raises:
        Http404: If the item with the given item_id does not exist.
    """
    item = get_object_or_404(Item, id=item_id)
    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
        return redirect('get_todo_list')
    form = ItemForm(instance=item)
    context = {
        'form': form
    }
    return render(request, 'todo/edit_item.html', context)



def toggle_item(request, item_id):
    """
    Toggle the status of an item.

    Args:
        request (HttpRequest): The HTTP request object.
        item_id (int): The ID of the item to toggle.

    Returns:
        HttpResponseRedirect: A redirect to the 'get_todo_list' view.
    """
    if request.method == "POST":
        item = get_object_or_404(Item, id=item_id)
        item.done = not item.done
        item.save()
        return redirect('get_todo_list')
    return HttpResponseBadRequest("Bad Request")

def delete_item(request, item_id):
    """
    Delete an item from the todo list.

    Args:
        request (HttpRequest): The HTTP request object.
        item_id (int): The ID of the item to be deleted.

    Returns:
        HttpResponseRedirect: Redirects to the 'get_todo_list' view.
    """
    if request.method == "POST":
        item = get_object_or_404(Item, id=item_id)
        item.delete()
        return redirect('get_todo_list')
    return HttpResponseBadRequest("Bad Request")

