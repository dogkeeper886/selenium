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
driver.set_window_size(width=1920, height=1080)

# Run
logging.info('Run')
driver.get("https://ruckus.cloud")

logging.info('Wait 30 seconds')
sleep(30)

# End
logging.info('End')
driver.quit()
