from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
from concurrent.futures import ThreadPoolExecutor, as_completed

import random
from comments import comments
from hashtags import hashtags
from accounts import accounts




# CLASS_NAME
# CSS_SELECTOR
# ID
# LINK_TEXT
# NAME
# PARTIAL_LINK_TEXT
# TAG_NAME
# XPATH


class Bot():

    links = []
    comments = comments
    hashtags = hashtags
    MAX_ATTEMPTS = 5

    def __init__(self):
        self = self

    def find_elem_and_action(self, value, sendKeys, keysText, click, isAnAction = False):
        # Check if a value is provided
        if value is None:
            print("No value provided")

        # Try to find the element and perform the action
        try:
            user_input = self.driver.find_element(by=By.XPATH, value=value)
            if(user_input):
                if(sendKeys):
                    user_input.send_keys(keysText) # Send keys to the element
                if(click):
                    user_input.click() # Click the element
            if(isAnAction):
                sleep(random.randint(25, 35)) # Sleep for random time if it's an action
            else:
                sleep(random.randint(5, 10)) # Sleep for random time
        except:
            print('Element not found')


    def go_home(self):
        self.driver.get('https://instagram.com/') # Navigate to Instagram home page
        sleep(2) # Wait for the page to load

    def login(self, usText, psText):
        options = Options()
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.75 Safari/537.36")
        options.add_argument('--headless') # Start the browser in headless mode
        PATH = "C:\Program Files (x86)\chromedriver.exe"
        # Note that the path of the chrome driver may need to be updated to match the location of the chrome driver on your computer.
        driver_service = Service(executable_path=PATH)
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(service=driver_service,options=options)

        self.go_home() # Go to Instagram home page
        sleep(5) # Wait for the page to load
        print('loging in...')

        self.find_elem_and_action('//input[@name="username"]', True, usText, False) # Enter username
        print('username entered')
        self.find_elem_and_action('//input[@name="password"]', True, psText, False) # Enter password
        print('password entered')
        self.find_elem_and_action('//button[@type="submit"]', False, '', True) # Click the login button

        self.find_elem_and_action('//button[text()="Save Info"]', False, '', True) # Click the "Save Info" button
        self.find_elem_and_action('//button[text()="Not Now"]', False, '', True) # Click the "Not Now" button


    def search(self, value):
        print(f'searching {value}...')
        # Click on the search bar
        self.find_elem_and_action('//div/div/div/div[1]/div/div/div/div[1]/div[1]/div[1]/div/div/div[1]/div/div[2]/div[2]/div/a', False, '', True)
        # Send the search value to the search bar
        self.find_elem_and_action('//input[@placeholder="Search"]', True, value, False)

    def is_logged_in(self):
        try:
            self.driver.find_element(by=By.XPATH, value='//div/div/div/div[1]/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[1]')
            print('logged in!')
            return True
        except:
            return False


    def like_by_hashtag(self, hashtag):
        #search for the hashtag in the search bar
        self.search('#'+hashtag)
        #click on the hashtag
        self.find_elem_and_action(f'//a[@href="/explore/tags/{hashtag}/"]', False, '', True)

        #find all the links in the hashtag page
        links = self.driver.find_elements(By.CSS_SELECTOR, "main article h2:nth-child(2) ~ div a")

        #filter the links that have /p/ in the link
        def condition(link):
            return '.com/p/' in link.get_attribute('href')

        #if there are links filter them, if not make the variable an empty list
        valid_links = list(filter(condition, links)) if links else []

        #if there are links in the filtered links then the number of links to like is 5, if not the number is 0
        num = 4 if valid_links else 0

        for i in range(num):
            link = valid_links[i].get_attribute('href')
            #if the link is not already in the links list then add it
            if link not in self.links:
                self.links.append(link)

        for link in self.links:
            #go to the link
            self.driver.get(link)
            sleep(random.randint(5, 7))

            #like the post
            print('liked! ', link)
            self.find_elem_and_action('//main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button', False, '', True, True)

        #clear the links list
        self.links.clear()


    def comment_and_like_by_hashtag(self, hashtag):
        self.search('#'+hashtag) # search for the provided hashtag
        self.find_elem_and_action(f'//a[@href="/explore/tags/{hashtag}/"]', False, '', True) # Click on the hashtag link

        links = self.driver.find_elements(By.CSS_SELECTOR, "main article h2:nth-child(2) ~ div a")

        def condition(link):
            return '.com/p/' in link.get_attribute('href') # check if the link is a post link

        valid_links = list(filter(condition, links)) if links else []

        num = 3 if valid_links else 0

        for i in range(num):
            link = valid_links[i].get_attribute('href')
            if link not in self.links:
                self.links.append(link)

        for link in self.links:
            self.driver.get(link) # visit the post link
            sleep(random.randint(5, 7))

            # like
            print('liked! ', link)
            self.find_elem_and_action('//main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button', False, '', True, True)

            # comment
            print('commented: ', link)
            self.find_elem_and_action('//main/div[1]/div[1]/article/div/div[3]/div/div/section[1]/span[2]/button', False, '', True, False)
            self.find_elem_and_action('//textarea[@placeholder="Add a comment…"]', False, '', True, False)
            self.find_elem_and_action('//textarea[@placeholder="Add a comment…"]', True, random.choice(self.comments), False)
            self.find_elem_and_action('//div[text()="Post"]', False, '', True)

        #clear the links list
        self.links.clear()


    def commands(self):
        attempts = 0
        while True:
            try:
                # like a post by a random hashtag
                self.like_by_hashtag(random.choice(self.hashtags))
                # navigate back to home page
                self.go_home()
                # comment and like a post by a random hashtag
                self.comment_and_like_by_hashtag(random.choice(self.hashtags))
                # navigate back to home page
                self.go_home()
                break
            except Exception:
                # check if the number of attempts has been reached before retrying.
                attempts += 1
                print('Something went wrong: trying again. Attempt #  ' + attempts)
                if attempts >= self.MAX_ATTEMPTS:
                    raise

def run_bots(user_name, password):
    print('username entered: ', user_name)

    bot = Bot()
    bot.login(user_name, password)
    if not bot.is_logged_in():
            print('User is not logged in')
    else:
        print('running...')
        bot.commands()


def main():
    wait_times = [60,45,50,60,55,60]
    while True:
        # create a list of functions using a list comprehension
        function_list = [run_bots(acc['username'], acc['password']) for acc in accounts]
        with ThreadPoolExecutor() as executor:
            # submit all the functions in the function_list to the thread pool executor
            executor.map(lambda function: function(), function_list)
            print('sleeping... zzzz')
            sleep(30 * random.choice(wait_times))

if __name__ == '__main__':
    main()
