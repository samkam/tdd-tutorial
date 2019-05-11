from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from unittest import skip

class ItemValidationTest(FunctionalTest):
	def test_cannot_add_empty_list_items(self):
		#Edith goes to the homepage and accidentally tries to submit
		#an empty list item she hits enter on the empty input box
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys(Keys.ENTER)
		
		#the home page refreshes, and there is an error message saying
		#that list items cannot be blank
		
		#she tries again with some text for the item, which now works
		
		#she experiments and tries to send a blank item again
		
		#she receives a similar warning
		
		#she can correct it by filling some text in
		self.fail("write me!")
