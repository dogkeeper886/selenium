from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from time import sleep
import logging
import sys
from dotenv import load_dotenv
from os import getenv


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
    dropdownButton = textElementFinder('Settings', 'div.button-wrapper span')
    dropdownButton.click()
    button = textElementFinder(buttonName, 'button span')
    button.click()


@driverDecorator
def channel(channelNumber):
    channelButton = textElementFinder(str(channelNumber), 'span.channel-text')
    channelButton.click()


@driverDecorator
def saveRadio():
    saveButton = textElementFinder(
        'Save Radio & Airtime Management', 'span.p-button-label'
    )
    saveButton.click()
    toastMessage()



@driverDecorator
def toastMessage():
    summaryMessage = WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located(
            (By.CSS_SELECTOR, 'div.summary-area span.leading-text-style')
        )
    )
    logging.info(summaryMessage.text)
    toastMessage = WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'div.toast-style div')
        )
    )
    for message in toastMessage:
        logging.info(message.text)


@driverDecorator
def closeDialogue():
    closeButton = textElementFinder(
        'Close', 'button.p-button span.p-button-label'
    )
    closeButton.click()


@driverDecorator
def tab(tabName):
    tabTitle = textElementFinder(tabName, 'div.tab-title-div')
    tabTitle.click()


@driverDecorator
def tableReader():
    rowGroup = driver.find_element_by_css_selector(
        'div.ag-center-cols-container')
    rowRawData = rowGroup.find_elements_by_css_selector('div[role="row"]')
    for row in rowRawData:
        nameColumn = row.find_element_by_css_selector('div[col-id="name"]')
        nameText = nameColumn.find_element_by_css_selector('span.icon-text')
        statusColumn = row.find_element_by_css_selector(
            'div[col-id="deviceStatus"]'
        )
        statusText = statusColumn.find_element_by_css_selector(
            'span.icon-text'
        )

        logging.info('%s %s', nameText.text, statusText.text)


if __name__ == '__main__':
    # Read .env file
    load_dotenv()

    # Logging
    logging.basicConfig(level=logging.INFO)

    # Start
    logging.info('Start')
    driver = webdriver.Remote(
        command_executor=getenv('WEBDRIVER_URL'),
        desired_capabilities=webdriver.DesiredCapabilities.FIREFOX
    )

    # Browser setting
    driver.set_window_size(width=1920, height=1080)
    driver.delete_all_cookies()
    driver.implicitly_wait(15)

    # Log in
    login(
        getenv('LOGIN_URL'),
        getenv('LOGIN_USERNAME'),
        getenv('LOGIN_PASSWORD')
    )

    # Wi-Fi
    leftMenu('Venues')
    venue('My-Venue')
    settings('Wi-Fi Settings')
    channel(6)
    saveRadio()
    closeDialogue()
    tab('Networking Devices')
    tableReader()

    # Switch
    # settings('Switch Settings')

    # Test
    sleep(30)

    # End task
    endTask()
