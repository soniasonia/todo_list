from django import forms
from django.core.exceptions import ValidationError
from .models import Item, List

EMPTY_LIST_ERROR = "Element listy nie może być pusty"
DUPLICATE_ERROR = "Element jest już na liście"

class ItemForm(forms.models.ModelForm):
    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
            'placeholder': 'Wpisz rzecz do zrobienia',
            'class':'form-control input-lg'
            }),
        }
        error_messages = {
            'text': {'required': EMPTY_LIST_ERROR}
        }

    def save(self, for_list):
        self.instance.list = for_list
        return super().save()
    # atrybut instance przedstawia tworzony lub modyfikowany obiekt bazy danych

# Pierwszy formularz jest dodany dużo później niż pierwsza wersja
# działającej aplikacji


class ItemForm(forms.models.ModelForm):
    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
            'placeholder': 'Wpisz rzecz do zrobienia',
            'class':'form-control input-lg'
            }),
        }
        error_messages = {
            'text': {'required': EMPTY_LIST_ERROR}
        }

    def save(self, for_list):
        self.instance.list = for_list
        return super().save()


# Formularz z niestandardowym konstruktorem (nadpisanie funkcji init)
# tak że argument to_list jest wymagany
class ExistingListItemForm(ItemForm):
    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def save(self):
        return forms.models.ModelForm.save(self)

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ERROR]}
            self._update_errors(e)
