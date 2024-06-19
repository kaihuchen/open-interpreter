import requests
import json
import re
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
# selenium-4.18.1
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup as bs
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
    
    def save_gui_def(self, interactive_elements, fpath_guidef='open-interpreter/_private/guidef.json'):

        elements_data = []

        for i, element in enumerate(interactive_elements):
            # Highlight the element
            self.driver.execute_script("arguments[0].style.border='3px solid red'", element)
            
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
        elements_json = json.dumps(elements_data, indent=4)

        print(elements_json)

        self.guidef = elements_data
        with open(fpath_guidef, 'w', encoding='utf-8') as f:
            json.dump(self.guidef, f, ensure_ascii=False, indent=4)

    def attach_to_existing_session(executor_url, session_id): # returns a driver object that is now appended to an existing browser window / session.
        original_execute = WebDriver.execute
        def new_command_execute(self, command, params=None):
            if command == "newSession":
                # Mock the response
                return {'success': 0, 'value': None, 'sessionId': session_id}
            else:
                return original_execute(self, command, params)
        # Patch the function before creating the driver object
        WebDriver.execute = new_command_execute
        driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
        driver.session_id = session_id
        # Replace the patched function with original function
        WebDriver.execute = original_execute
        return driver
        # bro = attach_to_existing_session('http://127.0.0.1:64092', '8de24f3bfbec01ba0d82a7946df1d1c3')
        # bro.get('http://bing.com/')

    def launch(self, url):
        """
        Launch a web-based GUI for all purposes other than searching
        """

        # for debugging
        # url = 'https://www.amazon.com'

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

            # TRYING TO OPEN IN EXISTING BROWSER WINDOW =================================


        # Navigate to the url
        self.driver.get(self.url)

        # soup = bs(self.driver.page_source)
        # for link in soup.find_all('a'):
        #     if link.get('href', None)

        # self.driver.maximize_window
        
        # currentHandle = self.driver.current_window_handle
        
        # # Searching Iphone 14 
        # self.driver.find_element(By.ID, "twotabsearchtextbox").send_keys("iPhone 14", Keys.ENTER)
        
        # # Clicking on search button
        # self.driver.find_element(By.XPATH, "//input[@type=’submit’]").click()
        # itemToSelect = self.driver.find_element(By.XPATH, "//span[text()=’Apple iPhone 14 128GB (Product) RED’]/../..").get_attribute("href")
        
        # # opening the new tab
        # self.driver.execute_script("window.open()")
        
        # handles = self.driver.window_handles
        # for s in handles:
        #     if (s != currentHandle):
        #         # switch to current tba
        #         self.driver.switch_to.window(s)
        #         self.driver.get("http://google.com")


        interactive_elements = self._highlight_inputs()
        self.save_gui_def(interactive_elements, fpath_guidef='_private/guidef.json')
 
        # Take a screenshot and save it
        self.driver.save_screenshot('_private/screenshot2.png')

        # Find the search box
        # search_box = self.driver.find_element(By.NAME, 'q')
        # search_box = self.driver.find_element(By.CSS_SELECTOR, "textarea")
        # WebDriverWait(self.driver,10000).until(expected_conditions.visibility_of_element_located((By.TAG_NAME,'body'))) 
        hiddenText = "Google apps"
        self.driver.find_element(By.XPATH, f"//a[contains(@aria-label,'{hiddenText}')]").click()

        # self.driver.find_element(By.XPATH, f"//*[text()[contains(.,'Images')]]").click()

        # TESTING
        # if (search_box.is_displayed()):
        #     search_box.click()
        #     search_box.clear()
        #     search_box.send_keys("Selenium webdrivers!")
        #     search_box.send_keys(Keys.RETURN)
        # else:
        #     print("SEARCH BOX NOT FOUND")
        # self.driver.manage().timeouts().implicitlyWait(30)
        # wait = WebDriverWait(self.driver, 20)
        # wait.until(expected_conditions.presence_of_element_located(By.className("sbtc")))

        # ((JavascriptExecutor) webDriver).executeScript("window.focus();");
        # ((JavascriptExecutor))
        # Use action chains to interact with the search box
        # actions = ActionChains(self.driver)
        # actions.move_to_element(search_box)
        # actions.click()
        # actions.send_keys('Hello, World!')
        # actions.perform()

    #     Submit the form
        # search_button = self.driver.find_element(By.NAME, 'btnK')
        # search_button.click()


    def open_tab_in_current_window(self, nameOfTabTask, newQueryURL):
        if not self.driver._check_if_window_handle_is_current:
            self.driver.switch_to.window(self.driver.current_window_handle)
        self.driver.execute_script(f"window.open('about:blank', {nameOfTabTask});")
        self.driver.switch_to.window(nameOfTabTask)
        self.driver.get(newQueryURL)

    def get_focus(self):
        # Bring the browser window to the foreground

        self.driver.switch_to.window(self.driver.current_window_handle)

        self.driver.execute_script("window.focus();")

        self.driver.execute_script("alert('Focus the window');")
        alert = self.driver.switch_to.alert
        alert.accept()

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
        self.driver.find_element(By.XPATH, f"//*[text()[contains(.,'{target}')]]").click()
        pyautogui.click(button="left", clicks=1, interval=0.1)

    def mouse_click_text(self, text):
        self.driver.find_element(By.XPATH, f"//*[text()[contains(.,'{text}')]]").click()


    # def mouse_click_text_in_element(self, text, element_type):
    #     self.driver.find_element(By.XPATH, f"//{element_type}[contains( text(), '{text}')]" )

    def mouse_click_element(self, jsonObject): 
        css_selector_text = jsonObject["css_selector"]
        # self.driver.find_element(By.CSS_SELECTOR, css_selector_text).click()
        try:
            # attempt to use the pre-generated CSS-selector (works only if literally correct)
            self.driver.find_element(By.CSS_SELECTOR, css_selector_text)
        except:
            # try to parse text found from the element, if any
            html_info_text = jsonObject["html_info"]
            pattern = r"#\d+:.+:(.+)"
            match = re.search(pattern, html_info_text)
            if match:
                extracted_text = match.group(1)
            if extracted_text:
                self.mouse_click_text(extracted_text)
            else:
                self.driver.get("musinsa.com")
            
    def mouse_click_accessible_text(self, text):
        self.driver.find_element(By.XPATH, f"/a[contains(@aria-label,'{text}')]").click()

    def mouse_click_by_xpath(self, xpath):
        self.driver.find_element(By.XPATH, f"{xpath}").click()




        

#
# Clean up
#self.driver.quit()