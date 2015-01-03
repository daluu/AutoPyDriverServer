from selenium import webdriver
from selenium.webdriver import ActionChains
from os import path

#NOTE: this demo uses images under images subfolder to find by name. 
# Be sure to configure AutoPyDriverServer to use that folder for images by name

driver = webdriver.Remote( command_executor='http://127.0.0.1:4723/wd/hub', desired_capabilities={'browserName':'AutoPy','imageRecognitionToleranceValue':0.0})
print "Desired Capabilities returned by server:\n"
print driver.desired_capabilities
print ""

# Example opening the test drag & drop webpage for Windows:
#driver.execute_script("start http://html5demos.com/drag")
# or
#driver.execute_script("start http://jqueryui.com/resources/demos/droppable/default.html")
# except that it hangs the script until you close calculator
# maybe different on Linux/Mac if you launch as background process but not sure. Try at your own risk.

# so, we assume the test webpage is open, in default state, & w/ focus so can start testing at this point
# AutoPy has no APIs for handling windows

# example for http://html5demos.com/drag
src = driver.find_element_by_name('drag_src_html5.png')
target = driver.find_element_by_name('drop_target_html5.png')
actions = ActionChains(driver)
actions.drag_and_drop(src,target).perform()

# or http://jqueryui.com/resources/demos/droppable/default.html
#src = driver.find_element_by_name('drag_src.png')
#target = driver.find_element_by_name('drop_target.png')
#actions = ActionChains(driver)
#actions.drag_and_drop(src,target).perform()

# result check for http://html5demos.com/drag
if len(driver.find_elements_by_name('drag_src_html5.png')) == 0: # as drag src disappeared into drop target
# or http://jqueryui.com/resources/demos/droppable/default.html
#if driver.find_element_by_name('dnd_result.png').is_displayed():
    print 'Drag & drop succeeded.\n'
else:
    screenshot = path.join(path.curdir,'failed_drag_and_drop.png')
    driver.get_screenshot_as_file(screenshot)
    print 'Drag & drop failed. See screenshot for actual result: %s.\n' % screenshot

# AutoPy may fail below due to problems trying to find the drag & drop result,
# may need to tweak AutoPy tolerance values. Also actual drag & drop operation
# may not be perfect in placement location each time, so actual result may not
# match the saved result image

driver.quit()