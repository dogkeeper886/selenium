from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from time import sleep
import logging

# Loggin
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
driver.implicitly_wait(15)

# Run
logging.info('Run')
driver.get("https://qaalto.ruckuswireless.com")

# login
# user name
driver.find_element_by_id('user_username').send_keys(
    'dog1051@email.com')

# user password
driver.find_element_by_id('user_password').send_keys('password-1')

# login
driver.find_element_by_css_selector(
    'input[type="submit"]').click()

# dashboard
# leftMenuItems = driver.find_elements_by_css_selector('rc-left-menu nav a div')

try:
    logging.info('Try')
    venuesButton = WebDriverWait(driver, 30).until(
        expected_conditions.element_to_be_clickable((By.LINK_TEXT, 'Venues')))
    # venuesButton = driver.find_element_by_link_text('Venues')

    if venuesButton:
        logging.info('Click')
        venuesButton.click()
        sleep(30)
    else:
        logging.info('No venuesButton')

except exceptions.NoSuchElementException:
    logging.warning('NoSuchElementException')

except exceptions.TimeoutException:
    logging.warning('TimeoutException')

except AttributeError:
    logging.warning('AttributeError')

# End task
driver.close()

try:
    driver.quit()
except exceptions.InvalidSessionIdException as err:
    logging.warn(err.msg)
