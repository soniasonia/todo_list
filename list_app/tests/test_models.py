from django.test import TestCase
from django.core.exceptions import ValidationError
from list_app.models import Item, List
from unittest import skip


class ItemModelTest(TestCase):

    @skip
    def test_saving_and_retrieving_items(self):
        correct_list = List.objects.create()
        first_item = Item()
        first_item.text = 'Absolutnie pierwszy element listy'
        first_item.list = correct_list
        first_item.save()
        second_item = Item()
        second_item.text = 'Drugi element listy'
        second_item.list = correct_list
        second_item.save()
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        first_item_saved = saved_items[0]
        second_item_saved = saved_items[1]
        self.assertEqual(first_item_saved.text, 'Absolutnie pierwszy element listy')
        self.assertEqual(second_item_saved.text, 'Drugi element listy')

    # nowa wersja tamtej metody
    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_item_is_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(text='Kupić żwirek dla kota', list=list_)
        with self.assertRaises(ValidationError):
            item = Item(text='Kupić żwirek dla kota', list=list_)
            item.full_clean()

    def test_can_save_tem_to_different_list(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(text='Kupić żwirek dla kota', list=list1)
        item = Item(text='Kupić żwirek dla kota', list=list2)
        item.full_clean()

    def test_order_of_list(self):
        list_ = List.objects.create()
        i1 = Item.objects.create(text='banana', list=list_)
        i2 = Item.objects.create(text='orange', list=list_)
        i3 = Item.objects.create(text='apple', list=list_)
        self.assertEqual(list(Item.objects.all()), [i1, i2, i3])

class ListModelTest(TestCase):

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), '/lists/{:d}/'.format(list_.id))


