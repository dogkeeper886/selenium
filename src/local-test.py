from selenium import webdriver
from time import sleep
import logging

# Loggin
logging.basicConfig(level=logging.DEBUG)

# Setup capabilities
logging.info('Set capabilities')
capabilities = webdriver.DesiredCapabilities.EDGE
logging.debug(capabilities)

# Start
logging.info('Start')
driver = webdriver.Remote(
    command_executor='http://192.168.2.46:32019/wd/hub',
    desired_capabilities=capabilities
)

# Browser setting
driver.set_window_size(width=1366, height=768)
driver.delete_all_cookies()
driver.implicitly_wait(15)

# Run
logging.info('Run')
driver.get("https://devalto.ruckuswireless.com")

# login
# user name
driver.find_element_by_id('user_username').send_keys(
    'dog1051@email.com')

# user password
driver.find_element_by_id('user_password').send_keys('password-1')

# login
driver.find_element_by_css_selector(
    'input[type="submit"]').click()
logging.info('Sleep')
sleep(15)

# dashboard
try:
    logging.info('Try')
    driver.find_element_by_link_text('Venues')
except:
    logging.info('Except')
    driver.refresh()
finally:
    logging.info('Finally')
    for data in driver.get_log('browser'):
        logging.info(data)
    driver.quit()
