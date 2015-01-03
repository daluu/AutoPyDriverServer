from selenium import webdriver
from os import path

#NOTE: this demo uses images under images subfolder to find by name. 
# Be sure to configure AutoPyDriverServer to use that folder for images by name

driver = webdriver.Remote( command_executor='http://127.0.0.1:4723/wd/hub', desired_capabilities={'browserName':'AutoPy','imageRecognitionToleranceValue':0.0})
print "Desired Capabilities returned by server:\n"
print driver.desired_capabilities
print ""

# Example opening the "Calculator" app for Windows:
#driver.execute_script("start calc")
# except that it hangs the script until you close calculator
# maybe different on Linux/Mac if you launch as background process but not sure. Try at your own risk.

# so, we assume calculator open with focus and can start testing at this point
# AutoPy has no APIs for handling windows

driver.find_element_by_name('calc_1_btn.png').click()
driver.find_element_by_name('calc_plus_btn.png').click()
driver.find_element_by_name('calc_2_btn.png').click()
equals_btn = driver.find_element_by_name('calc_equals_btn.png')
equals_btn.click()
size = equals_btn.size
loc = equals_btn.location

print "Equals button is %d x %d pixels in size" % (size['width'],size['height'])
print "Equals button is located approximately at (%d,%d) on (main) desktop screen" % (loc['x'],loc['y'])

print "# elements found when try find_elements for an element that can't seem to find: %d" % len(driver.find_elements_by_name('calc_3_result.png'))

# AutoPy may fail below due to problems trying to find the results text field
# may need to tweak AutoPy tolerance values
#if driver.find_element_by_name('calc_3_result.png').is_displayed():
#    print 'Calculated correctly that 1 + 2 = 3\n'
#else:
#    screenshot = path.join(path.curdir,'failed_calculation.png')
#    driver.get_screenshot_as_file(screenshot)
#    print 'Calculation of 1 + 2 is incorrect. See screenshot for actual result: %s.\n' % screenshot

screenshot = path.join(path.curdir,'screenshot_demo.png')
driver.get_screenshot_as_file(screenshot)
print 'See screenshot demo: %s.\n' % screenshot

driver.quit()