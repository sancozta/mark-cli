# desc: Captura screenshot de uma URL via Chrome/Selenium
import sys
import time

from selenium import webdriver

if len(sys.argv) != 2:
    print('Usage: python get_screen.py <url>')
    print('Example: python get_screen.py https://example.com')
    sys.exit(1)

url = sys.argv[1]

def capture_screenshot(target_url, save_path):
    driver = webdriver.Chrome()
    driver.get(target_url)
    time.sleep(10)
    driver.save_screenshot(save_path)
    driver.quit()

capture_screenshot(url, 'screenshot.png')