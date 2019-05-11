from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from lists.views import home_page
from lists.models import Item, List
from django.utils.html import escape
from lists.forms import ItemForm
class HomePageTest(TestCase):
	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func,home_page)
	def test_home_page_returns_correct_html(self):
		response = self.client.get('')
		self.assertTemplateUsed(response, 'home.html')
	
	def test_home_page_uses_item_form(self):
		response = self.client.get('')
		self.assertIsInstance(response.context['form'],ItemForm)


class ListViewTest(TestCase):

	def test_uses_list_template(self):
		list_ = List.objects.create()
		response = self.client.get(f'/lists/{list_.id}')
		self.assertTemplateUsed(response, 'list.html')
	def test_displays_only_items_for_that_list(self):
		list_ = List.objects.create()
		Item.objects.create(text="itemey 1", list=list_)
		Item.objects.create(text="itemey 2", list=list_)
		
		other_list = List.objects.create()
		Item.objects.create(text="other itemey 1", list=other_list)
		Item.objects.create(text="other itemey 2", list=other_list)
		
		response = self.client.get(f'/lists/{list_.id}')
		self.assertContains(response,'itemey 1')
		self.assertContains(response,'itemey 2')
		self.assertNotContains(response,'other itemey 1')
		self.assertNotContains(response,'other itemey 2')
	def test_can_save_a_POST_request(self):
		response = self.client.post('/lists/new', data={'item_text': 'A new list item'})		
		self.assertEqual(Item.objects.count(),1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, "A new list item")
	
	def test_redirects_after_POST(self):
		#status code is for redirect
		response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
		new_list = List.objects.first()
		self.assertRedirects(response,f'/lists/{new_list.id}')
	
	def test_passes_correct_list_to_template(self):
		correct_list = List.objects.create()
		wrong_list = List.objects.create()
		response = self.client.get(f'/lists/{correct_list.id}')
		self.assertEqual(response.context['list'],correct_list)
	
	def test_validation_errors_are_sent_back_to_home_page_template(self):
		response = self.client.post('/lists/new', data={'item_text':''})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'home.html')
		expected_error = escape("You can't have an empty list item")
		self.assertContains(response, expected_error)
		
	def test_validation_errors_are_sent_back_to_list_page(self):
		list_ = List.objects.create()
		
		response = self.client.post(f'/lists/{list_.id}', data={'item_text':''})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'list.html')
		expected_error = escape("You can't have an empty list item")
		self.assertContains(response, expected_error)	
	
	def test_invalid_items_arent_saved(self):
		self.client.post('/lists/new', data={'item_text': ''})
		self.assertEqual(Item.objects.count(),0)
		self.assertEqual(List.objects.count(),0)
	
	def test_can_save_a_POST_to_existing_list(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		response = self.client.post(f'/lists/{correct_list.id}',
			data={'item_text': "a new item for existing list"}
		)
		
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		
		self.assertEqual(new_item.text, 'a new item for existing list')
		self.assertEqual(new_item.list, correct_list)

	def test_POST_redirects_to_list_view(self):
		list_ = List.objects.create()
		other_list = List.objects.create()
		response = self.client.post(f'/lists/{list_.id}',
			data={'item_text': "a new list item"}
		)
		self.assertRedirects(response, f'/lists/{list_.id}')
		
	#def test_invalid_items_arent_saved_on_existing_list
		
