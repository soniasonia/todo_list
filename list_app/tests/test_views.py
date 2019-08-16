from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.utils.html import escape
from django.template.loader import render_to_string

from list_app.views import home_page
from list_app.models import Item, List
from list_app.forms import ItemForm, ExistingListItemForm,\
    EMPTY_LIST_ERROR, DUPLICATE_ERROR


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
    # To można potem usunąć bo jest pokryte przez nastepny test

    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/{:d}/'.format(list_.id))
        self.assertTemplateUsed(response, 'list.html')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/{}/'.format(correct_list.id))
        self.assertEqual(response.context['list'], correct_list)

        # nie ma na liscie strona 235, chyba do forms
    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/{:d}/'.format(list_.id), )
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    def test_displays_items_only_for_this_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='banana', list=correct_list)
        Item.objects.create(text='orange', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='wrong banana', list=other_list)
        Item.objects.create(text='wrong orange', list=other_list)
        # self.client.get() - Django specific function that returns response to html request
        response = self.client.get('/lists/{:d}/'.format(correct_list.id))
        self.assertContains(response, 'banana')
        self.assertContains(response, 'orange')

    def test_can_save_a_POST_to_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        self.client.post('/lists/{}/'.format(correct_list.id), data={'text': 'Nowy element listy'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'Nowy element listy')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        list_ = List.objects.create()
        response = self.client.post('/lists/{:d}/'.format(list_.id), data={'text': 'Nowy element listy'})
        self.assertRedirects(response, '/lists/{:d}/'.format(list_.id))

    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post('/lists/{:d}/'.format(list_.id),
                                    data={'text': ''})

    def test_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')

    def test_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)

    def test_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_LIST_ERROR))

    def test_duplicate_item_validation_errors_ends_up_on_list_page(self):
        list_ = List.objects.create()
        Item.objects.create(text='kotek', list=list_)
        response = self.client.post('/lists/{:d}/'.format(list_.id),
                                    data={'text': 'kotek'})
        expected_error = escape(DUPLICATE_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(Item.objects.all().count(), 1)

class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        correct_list = List.objects.create()
        self.client.post('/lists/new', data={'text': 'Nowy element listy'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'Nowy element listy')

    def test_redirects_to_list_view(self):
        # request = HttpRequest()
        # request.method = 'POST'
        # request.POST['item_text'] = 'Nowy element listy'
        # response = home_page(request)
        response = self.client.post('/lists/new', data={'text': 'Nowy element listy'})
        # Django client generates with "client.post" response to HttpRequest (method POST)

        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/{:d}/'.format(new_list.id))

    def test_show_correct_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.post('/lists/{}/'.format(correct_list.id),
                                    data={'text': 'Nowy element listy'})
        self.assertRedirects(response, '/lists/{:d}/'.format(correct_list.id))

    def test_invalid_input_nothing_saved_to_db(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(Item.objects.count(), 0)

    def test_invalid_input_renders_home_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertContains(response, escape(EMPTY_LIST_ERROR))

    def test_invalid_input_passes_form_to_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)

