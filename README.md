AutoPyDriverServer
=========

AutoPyDriverServer is a (test) automation tool via image recognition that provides a Selenium WebDriver API via the webdriver JSON  wire protocol to drive to the [AutoPy](https://github.com/msanders/autopy) tool/library running as a server. It is adapted from the [old Appium server Python implementation](https://github.com/hugs/appium-old).

AutoPyDriverServer uses the [Bottle micro web-framework](http://www.bottlepy.org), and has the goal of working with all off the shelf Selenium client libraries.

There are two benefits to testing with AutoPyDriverServer:

1: With AutoPyDriverServer, you are able to write your test in your choice of programming language, using the Selenium WebDriver API and language-specific client libraries. If you only used AutoPy, you would be required to write tests in Python, or interface to some Python code to call AutoPy.

2: AutoPyDriverServer uses the AutoPy library for Python, which provides cross-plaform support for some image recognition capability and mouse, keyboard manipulation. If you already use AutoPy, this will be a nice benefit.

Quick Start
-----------

To get started, clone the repo:<br />
`git clone git://github.com/hugs/appium`

Next, change into the 'autopydriverserver' directory, and install dependencies:<br />
`pip install -r linux_mac_requirements.txt`<br />
or<br />
`pip install -r windows_requirements.txt`

For Windows, you may wish to manually install AutoPy module (dependency), which is not in the requirements file for Windows (above), as suggested by AutoPy author. Get the binary installer at https://pypi.python.org/pypi/autopy/

To launch a webdriver-compatible server, run:<br />
`python server.py` <br />

For additional parameter info, append the `--help` parameter

Example WebDriver test usage against this server tool can be found in `sample-code` folder. To run the test, startup the server (with customized parameters as needed) and review the example files' code before executing those scripts. Examples use Python WebDriver binding, but any language binding will do.

NOTES/Caveats
-------------

AutoPyDriverServer is simply a WebDriver server interface to AutoPy. Issues you experience may usually be the result of an issue with AutoPy rather than AutoPyDriverServer itself. If you are experienced with Python, it would be wise to test your issue/scenario using native Python AutoPy API to confirm whether the issue is with AutoPy or AutoPyDriverServer. The source code of AutoPyDriverServer will point you to the appropriate AutoPy API or see the [AutoPy Python API specifics for debugging](https://github.com/daluu/AutoPyDriverServer/wiki/AutoPy-Python-API-specifics-for-debugging).

WebDriver API/command support and mapping to AutoPy API
-------------------------------------------------------

See [WebDriver API command support and mapping to AutoPy API](https://github.com/daluu/AutoPyDriverServer/wiki/WebDriver-API-command-support-and-mapping-to-AutoPy-API)

Contributing
------------

Fork the project, make a change, and send a pull request!

Or as a user, try it out, provide your feedback, submit bugs/enhancement requests.
