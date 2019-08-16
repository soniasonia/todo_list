from django.test import TestCase
from list_app.forms import ItemForm, ExistingListItemForm,\
    EMPTY_LIST_ERROR, DUPLICATE_ERROR
from list_app.models import Item, List

class ItemFormTest(TestCase):
    def test_form_renders_item_text_input(self):
        form = ItemForm()
        self.assertIn('placeholder="Wpisz rzecz do zrobienia"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_LIST_ERROR])

    def test_save_handles_saving_to_list(self):
        list_ = List.objects.create()
        form = ItemForm(data={'text': 'banana'})
        new_item = form.save(for_list=list_)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, 'banana')
        self.assertEqual(new_item.list, list_)


class ExistingListItemFormTest(TestCase):
    def test_form_renders_item_text_input(self):
        form = ItemForm()
        self.assertIn('placeholder="Wpisz rzecz do zrobienia"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_LIST_ERROR])

    def test_validation_for_duplicates(self):
        list_ = List.objects.create()
        Item.objects.create(text="kotek", list=list_)
        form = ExistingListItemForm(for_list=list_, data={'text': 'kotek'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ERROR])

