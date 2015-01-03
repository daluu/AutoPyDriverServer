from selenium import webdriver
from selenium.webdriver import ActionChains
from os import path
import time

#NOTE: this demo uses images under images subfolder to find by name. 
# Be sure to configure AutoPyDriverServer to use that folder for images by name

# start up both Firefox & AutoPyDriver for demo
browser = webdriver.Firefox()
autopy_driver = webdriver.Remote( command_executor='http://127.0.0.1:4723/wd/hub', desired_capabilities={'browserName':'AutoPy','imageRecognitionToleranceValue':0.0})
print "Desired Capabilities returned by server:\n"
print autopy_driver.desired_capabilities
print ""

# launch browser to Drag & drop page for demo test
browser.get("http://html5demos.com/drag")

if len(browser.find_elements_by_tag_name("li")) != 5:
	print "Drag & drop test page not in correct state for demo test"

time.sleep(5)

src = autopy_driver.find_element_by_name('drag_src_html5.png')
target = autopy_driver.find_element_by_name('drop_target_html5.png')
actions = ActionChains(autopy_driver)
actions.drag_and_drop(src,target).perform()

# check results, drag & drop reduced items by 1 from 5 to 4
result = len(browser.find_elements_by_tag_name('li'))
if result != 4:
    print 'Drag & drop failed. There are %d items when there should be 4.\n' % result
else:
    print 'Drag & drop success.\n'

browser.quit()
autopy_driver.quit()

# Now imagine from this integration demo, you could use AutoPy with browser via
# WebDriver to do stuff like file download, HTTP authentication and other stuff
# like drag item from desktop into browser, that you could not do w/ WebDriver
# alone, or w/ executing shell commands and other external stuff. Now can do all
# with WebDriver APIs against 2+ WebDriver instances.