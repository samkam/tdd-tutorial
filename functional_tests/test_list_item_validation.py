from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from unittest import skip

class ItemValidationTest(FunctionalTest):
	def test_cannot_add_empty_list_items(self):
		#Edith goes to the homepage and accidentally tries to submit
		#an empty list item she hits enter on the empty input box
		self.browser.get(self.live_server_url)
		inputbox = self.get_item_input_box()
		inputbox.send_keys(Keys.ENTER)
		
		#the home page refreshes, and there is an error message saying
		#that list items cannot be blank
		self.wait_for( lambda: self.browser.find_element_by_css_selector(
			'#id_text:invalid'
		))
		#she tries again with some text for the item, which now works
		self.get_item_input_box().send_keys('Buy milk')
		self.wait_for( lambda: self.browser.find_element_by_css_selector(
			'#id_text:valid'
		))
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')

		#she experiments and tries to send a blank item again
		self.get_item_input_box().send_keys(Keys.ENTER)

		#she receives a similar warning
		self.wait_for( lambda: self.browser.find_element_by_css_selector(
			'#id_text:invalid'
		))
		#she can correct it by filling some text in
		self.get_item_input_box().send_keys('Make tea')
		self.wait_for( lambda: self.browser.find_element_by_css_selector(
			'#id_text:valid'
		))
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')
		self.wait_for_row_in_list_table('2: Make tea')
