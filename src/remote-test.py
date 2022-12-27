from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from time import sleep
import logging
import sys


def driverDecorator(func):
    def wrapper(*args, **kwargs):
        try:
            logging.info(func.__name__)
            func(*args, **kwargs)

        except exceptions.NoSuchElementException:
            logging.warning('Except %s: NoSuchElementException', func.__name__)
            endTask()
            sys.exit()

        except exceptions.TimeoutException:
            logging.warning('Except %s: TimeoutException', func.__name__)
            endTask()
            sys.exit()

        except exceptions.InvalidSessionIdException as err:
            logging.warning('Except %s: %s', func.__name__, err.msg)

        finally:
            sleep(5)

    return wrapper


@driverDecorator
def login(login_url, user_name, user_password):
    driver.get(login_url)

    # User name
    driver.find_element_by_id('user_username').send_keys(user_name)

    # User password
    driver.find_element_by_id('user_password').send_keys(user_password)

    # Submit
    driver.find_element_by_css_selector('input[type="submit"]').click()


@driverDecorator
def endTask():
    driver.close()
    driver.quit()


@driverDecorator
def leftMenu(itemName):
    menuButton = WebDriverWait(driver, 10).until(
        expected_conditions.element_to_be_clickable((By.LINK_TEXT, itemName))
    )
    menuButton.click()


def textElementFinder(elementText, css):
    elementList = driver.find_elements_by_css_selector(css)
    for element in elementList:
        if element.text == elementText:
            return element
    else:
        logging.info('No element match %s', elementText)


@driverDecorator
def venue(venueName):
    venueTextElement = textElementFinder(venueName, 'span')
    venueTextElement.click()

@driverDecorator
def settings(buttonName):
    dropdownButton = textElementFinder('Settings', 'span')
    dropdownButton.click()
    button = textElementFinder(buttonName, 'span')
    button.click()


if __name__ == '__main__':
    # Logging
    logging.basicConfig(level=logging.INFO)

    # Start
    logging.info('Start')
    driver = webdriver.Remote(
        command_executor='http://192.168.2.46:31623/wd/hub',
        desired_capabilities=webdriver.DesiredCapabilities.FIREFOX
    )

    # Browser setting
    driver.set_window_size(width=1920, height=1080)
    driver.delete_all_cookies()
    driver.implicitly_wait(10)

    # Log in
    login(
        'https://qaalto.ruckuswireless.com',
        'dog1051@email.com',
        'password-1'
    )

    # Go to Venues
    leftMenu('Venues')
    venue('My-Venue')
    #settings('Wi-Fi Settings')
    settings('Switch Settings')
    
    # Test
    sleep(30)

    # End task
    endTask()
