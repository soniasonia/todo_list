from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from .models import Item, List
from .forms import ItemForm, ExistingListItemForm, \
    EMPTY_LIST_ERROR


def home_page(request):
    if request.method == 'POST':
        new_item_text = request.POST['text']
        Item.objects.create(text=new_item_text)
        return redirect('/lists/new')
    return render(request, 'home.html', {'form': ItemForm()})

    # Django automatycznie suka katalogów o nazwie templates
    # Funkcja render zwraca obiekt HttpResponse w oparciu o znaleziony szablon html
    # Django nie może jednak znaleźć szablonu, dopóki nie uzupełnimy listy INSTALLED_APPS w setting.py

# Widok pobiera info z żądania użytkownika, łączy z własną logiką lub info pobranymi z adresu URL
# przekazuje do formularza sieciowego w celu weryfikacji zapisu i przekierowouje lub renderuje szablon


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, 'list.html', {
        'list': list_, 'form': form})


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {"form": form})

    # Funkcja redirect obiera obiekt i automatycznie używa funkcji get_absolute_url
