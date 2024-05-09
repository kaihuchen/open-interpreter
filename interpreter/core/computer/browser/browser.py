import requests
import json

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
# selenium-4.18.1
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import pyautogui

class Browser:
    # This is a class-level global driver instance, for debugging purposes
    driverg = None
    def __init__(self, computer):
        self.computer = computer
        self.driver = None
        self.url = None

    def search(self, query):
        """
        Searches the web for the specified query and returns the results.
        """
        response = requests.get(
            f'{self.computer.api_base.strip("/")}/browser/search',
            params={"query": query},
        )
        return response.json()["result"]

    def _highlight_inputs(self):
        """
        Highlights all input elements by adding a red border around them.
        """
        # inputs = self.driver.find_elements(By.CSS_SELECTOR, "input, textarea, button, select, a[href]")

        # for input_element in inputs:
        #     self.driver.execute_script("arguments[0].style.border='3px solid red'", input_element)

        interactive_elements = self.driver.find_elements(By.CSS_SELECTOR, "input, textarea, button, select, a[href], [onclick], [onchange], [onmouseover], [onmouseout], [onkeydown], [onkeyup], [onkeypress], [tabindex]:not([tabindex='-1'])")
        for element in interactive_elements:
            self.driver.execute_script("arguments[0].style.border='3px solid red'", element)
        return interactive_elements

    # Function to generate a unique CSS selector for an element
    def get_unique_css_selector(self, element):
        path = [] 
        while element.tag_name.lower() != 'html':
            parent = element.find_element(By.XPATH, '..')
            children = [child for child in parent.find_elements(By.XPATH, '*') if child.tag_name == element.tag_name]
            index = children.index(element) + 1
            path.append(f'{element.tag_name}:nth-of-type({index})')
            element = parent
        path.reverse()
        return ' > '.join(path)

    # Function to describe the purpose of an element based on its tag and type
    def describe_element(self, element):
        tag = element.tag_name.lower()
        type_attr = element.get_attribute('type').lower() if element.get_attribute('type') else None
        if tag == 'input' and type_attr == 'text':
            return 'Text Input Field', element.text
        elif tag == 'input' and type_attr == 'button':
            return 'Button Input Field', element.text
        elif tag == 'a':
            return 'Link', element.text
        # Add more descriptions based on the tag and type as necessary
        else:
            return 'Interactive Element', element.text
    
    def save_gui_def(self, interactive_elements, fpath_guidef='_private/guidef.json'):
        
        elements_data = []

        for i, element in enumerate(interactive_elements):
            # Highlight the element
#           self. driver.execute_script("arguments[0].style.border='3px solid red'", element)
            
            # Get the bounding box coordinates
            rect = element.rect
            bounding_box = {
                'x': rect['x'],
                'y': rect['y'],
                'width': rect['width'],
                'height': rect['height']
            }

            center_x = (rect['x'] + rect['width']) / 2
            center_y = (rect['y'] + rect['height']) / 2
            
            # Get a unique CSS selector for the element
            css_selector = self.get_unique_css_selector(element)
            
            # Describe the purpose of the element
            element_type, html_info = self.describe_element(element)
            description = f'#{i+1}: {element_type} : {html_info}'
            # Add element data to the list
            elements_data.append({
                'html_info': description,
                'bounding_box': bounding_box,
                'center': [int(center_x), int(center_y)],
                'css_selector': css_selector
            })

        # Convert the list to a JSON object
#        elements_json = json.dumps(elements_data, indent=4)

#        print(elements_json)

        self.guidef = elements_data
        with open(fpath_guidef, 'w', encoding='utf-8') as f:
            json.dump(self.guidef, f, ensure_ascii=False, indent=4)


    def launch(self, url):
        """
        Launch a web-based GUI for all purposes other than searching
        """

        # for debugging
        url = 'https://www.google.com'

        if url==self.url:
            return

        self.url = url

        if self.driver is None:
            # Setup chrome driver
            self.driver_options = webdriver.ChromeOptions()
            #options.add_argument('--headless')
            self.driver = webdriver.Chrome(options=self.driver_options)
            self.actions = ActionChains(self.driver)

            # For debugging
            Browser.driverg = self.driver

        # Navigate to the url
        self.driver.get(self.url)

        interactive_elements = self._highlight_inputs()
        self.save_gui_def(interactive_elements, fpath_guidef='_private/guidef.json')
 
        # Take a screenshot and save it
        self.driver.save_screenshot('_private/screenshot2.png')

        # Find the search box
#        search_box = self.driver.find_element(By.NAME, 'q')

        # Use action chains to interact with the search box
#        actions = ActionChains(self.driver)
#        actions.move_to_element(search_box)
#        actions.click()
#        actions.send_keys('Hello, World!')
#        actions.perform()

        # Submit the form
#        search_button = self.driver.find_element(By.NAME, 'btnK')
#        search_button.submit()

    def get_focus(self):
        # Bring the browser window to the foreground

        self.driver.switch_to.window(self.driver.current_window_handle)

#        self.driver.execute_script("window.focus();")

#        self.driver.execute_script("alert('Focus the window');")
#        alert = self.driver.switch_to.alert
#        alert.accept()

        # Optional: Maximize the window
#        self.driver.maximize_window()

    def move_to(self, x, y):
        self.get_focus()
        window_rect = self.driver.get_window_rect()
        window_width, window_height, window_x, window_y = window_rect.values()
        offset_y = 190
        pyautogui.moveTo(64 + window_x, 23 + offset_y + window_y)

    def mouse_click(self, target: str):
        #
        pyautogui.click(button="left", clicks=1, interval=0.1)

#
# Clean up
#self.driver.quit()