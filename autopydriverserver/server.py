#    Source code is modified from and based off of 
#    old/original Appium Python implementation at
#
#    https://github.com/hugs/appium-old
#
#    Licensed to the Apache Software Foundation (ASF) under one
#    or more contributor license agreements.  See the NOTICE file
#    distributed with this work for additional information
#    regarding copyright ownership.  The ASF licenses this file
#    to you under the Apache License, Version 2.0 (the
#    "License"); you may not use this file except in compliance
#    with the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing,
#    software distributed under the License is distributed on an
#    "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#    KIND, either express or implied.  See the License for the
#    specific language governing permissions and limitations
#    under the License.

from bottle import Bottle, request, response, redirect
from bottle import run, static_file
import ConfigParser
import json
import socket
import sys
import platform
import os
import subprocess
import base64
import urllib
import autopy
from time import time
from time import sleep

app = Bottle()

@app.get('/favicon.ico')
def get_favicon():
    return static_file('favicon.ico', root='.')

@app.route('/wd/hub/status', method='GET')
def status():
    status = {'sessionId': app.SESSION_ID if app.started else None,
              'status': 0,
              'value': {'build': {'version': 'AutoPyDriverServer 0.1'}}}
    return status

@app.route('/wd/hub/session', method='POST')
def create_session():
    #process desired capabilities
    request_data = request.body.read()
    dc = json.loads(request_data).get('desiredCapabilities')
    if dc is not None:
        newTolerance = dc.get('imageRecognitionToleranceValue')
        if newTolerance is not None:
            app.tolerance = newTolerance
        newImageFolder = dc.get('defaultImageFolder')
        if newImageFolder is not None:
            app.image_path = newImageFolder
        newConfigFile = dc.get('defaultElementImageMapConfigFile')
        if newConfigFile is not None:
            app.element_locator_map_file = newConfigFile

    #setup session
    app.started = True
    redirect('/wd/hub/session/%s' % app.SESSION_ID)

@app.route('/wd/hub/session/<session_id>', method='GET')
def get_session(session_id=''):
    if sys.platform == "win32":
        if platform.release() == "Vista":
            wd_platform = "VISTA"
        elif platform.release() == "XP": #?
            wd_platform = "XP"
        else:
            wd_platform = "WINDOWS"
    elif sys.platform == "darwin":
        wd_platform = "MAC"
    else: #sys.platform.startswith('linux'):
        wd_platform = "LINUX"

    app_response = {'sessionId': session_id,
                'status': 0,
                'value': {"version":"0.1",
                          "browserName":"AutoPy",
                          "platform":wd_platform,
                          "takesScreenshot":True,
                          "imageRecognitionToleranceValue":app.tolerance,
                          "defaultImageFolder":app.image_path,
                          "defaultElementImageMapConfigFile":app.element_locator_map_file}}
    return app_response

@app.route('/wd/hub/session/<session_id>', method='DELETE')
def delete_session(session_id=''):
    app.started = False
    app_response = {'sessionId': session_id,
                'status': 0,
                'value': {}}
    return app_response

@app.route('/wd/hub/session/<session_id>/execute', method='POST')
def execute_script(session_id=''):
    status = 0
    result = ''
    request_data = request.body.read()
    try:
        script = json.loads(request_data).get('script')
        #args = json.loads(request_data).get('args')
        #script_with_args = [script]
        #script_with_args.extend(args)
        #result = subprocess.check_output(script, stderr=subprocess.STDOUT)
        #result = subprocess.check_output(script_with_args, stderr=subprocess.STDOUT)
        proc_handle = os.popen(script)
        result = proc_handle.read()
        proc_handle.close()
    except:
        response.status = 400
        return {'sessionId': session_id, 'status': 13, 'value': str(sys.exc_info()[0])}

    app_response = {'sessionId': session_id,
        'status': status,
        'value': result}
    return app_response

@app.route('/wd/hub/session/<session_id>/element/<element_id>/click', method='POST')
def element_click(session_id='', element_id=''):
    try:
        _go_to_element(element_id)
        autopy.mouse.click()
    except:
        response.status = 400
        return {'sessionId': session_id, 'status': 13, 'value': str(sys.exc_info()[0])}

    app_response = {'sessionId': session_id,
        'status': 0,
        'value': {}}
    return app_response

@app.route('/wd/hub/session/<session_id>/click', method='POST')
def mouse_click(session_id=''):
    request_data = request.body.read()
    if request_data == None or request_data == '' or request_data == "{}":
        button = 0
    else:
        button = json.loads(request_data).get('button')
    try:
        if button == 1:
            autopy.mouse.click(autopy.mouse.CENTER_BUTTON)
        elif button == 2:
            autopy.mouse.click(autopy.mouse.RIGHT_BUTTON)
        else: #button 1
            autopy.mouse.click()
    except:
        response.status = 400
        return {'sessionId': session_id, 'status': 13, 'value': str(sys.exc_info()[0])}

    app_response = {'sessionId': session_id,
        'status': 0,
        'value': {}}
    return app_response

@app.route('/wd/hub/session/<session_id>/buttonup', method='POST')
def mouse_up(session_id=''):
    request_data = request.body.read()
    if request_data == None or request_data == '' or request_data == "{}":
        button = 0
    else:
        button = json.loads(request_data).get('button')
    try:
        if button == 1:
            autopy.mouse.toggle(False,autopy.mouse.CENTER_BUTTON)
        elif button == 2:
            autopy.mouse.toggle(False,autopy.mouse.RIGHT_BUTTON)
        else: #button 1
            autopy.mouse.toggle(False)
    except:
        response.status = 400
        return {'sessionId': session_id, 'status': 13, 'value': str(sys.exc_info()[0])}

    app_response = {'sessionId': session_id,
        'status': 0,
        'value': {}}
    return app_response

@app.route('/wd/hub/session/<session_id>/buttondown', method='POST')
def mouse_down(session_id=''):
    request_data = request.body.read()
    if request_data == None or request_data == '' or request_data == "{}":
        button = 0
    else:
        button = json.loads(request_data).get('button')
    try:
        if button == 1:
            autopy.mouse.toggle(True,autopy.mouse.CENTER_BUTTON)
        elif button == 2:
            autopy.mouse.toggle(True,autopy.mouse.RIGHT_BUTTON)
        else: #button 1
            autopy.mouse.toggle(True)
    except:
        response.status = 400
        return {'sessionId': session_id, 'status': 13, 'value': str(sys.exc_info()[0])}

    app_response = {'sessionId': session_id,
        'status': 0,
        'value': {}}
    return app_response

@app.route('/wd/hub/session/<session_id>/moveto', method='POST')
def move_to(session_id=''):
    request_data = request.body.read()
    if request_data == None or request_data == '' or request_data == "{}":
        element_id = None
        xoffset = None
        yoffset = None
    else:
        element_id = json.loads(request_data).get('element')
        xoffset = json.loads(request_data).get('xoffset')
        yoffset = json.loads(request_data).get('yoffset')
    try:
        if element_id == None and (xoffset != None or yoffset != None):
            src = autopy.mouse.get_pos()
            autopy.mouse.smooth_move(src[0]+xoffset,src[1]+yoffset)
        else:
            if xoffset != None or yoffset != None:
                path = decode_value_from_wire(element_id)
                elem = autopy.bitmap.Bitmap.open(path)
                pos = autopy.bitmap.capture_screen().find_bitmap(elem,app.tolerance)
                autopy.mouse.smooth_move(pos[0]+xoffset,pos[1]+yoffset)
            else: # just go to center of element
                _go_to_element(element_id)

    except:
        response.status = 400
        return {'sessionId': session_id, 'status': 13, 'value': str(sys.exc_info()[0])}

    app_response = {'sessionId': session_id,
        'status': 0,
        'value': {}}
    return app_response

@app.route('/wd/hub/session/<session_id>/element/<element_id>/value', method='POST')
def set_value(session_id='', element_id=''):
    request_data = request.body.read()
    try:
        value_to_set = json.loads(request_data).get('value')
        value_to_set = ''.join(value_to_set)

        _go_to_element(element_id)
        autopy.mouse.click()
        autopy.key.type_string(value_to_set)
    except:
        response.status = 400
        return {'sessionId': session_id, 'status': 13, 'value': str(sys.exc_info()[0])}

    app_response = {'sessionId': session_id,
        'status': 0,
        'value': {}}
    return app_response

@app.route('/wd/hub/session/<session_id>/element/<element_id>/elements', method='POST')
def element_find_elements(session_id='', element_id=''):
    return _find_element(session_id, element_id, many=True)

@app.route('/wd/hub/session/<session_id>/elements', method='POST')
def find_elements(session_id=''):
    return _find_element(session_id, "root", many=True)

@app.route('/wd/hub/session/<session_id>/element/<element_id>/element', method='POST')
def element_find_element(session_id='', element_id=''):
    return _find_element(session_id, element_id)

@app.route('/wd/hub/session/<session_id>/element', method='POST')
def find_element(session_id=''):
    return _find_element(session_id, "root")

def _go_to_element(element_id):
    path = decode_value_from_wire(element_id)
    elem = autopy.bitmap.Bitmap.open(path)
    pos = autopy.bitmap.capture_screen().find_bitmap(elem,app.tolerance)

    if autopy.mouse.get_pos() != pos:
        autopy.mouse.smooth_move(pos[0]+(elem.width/2),pos[1]+(elem.height/2))

def _find_element(session_id, context, many=False):
    try:
        # TODO: need to support more locator_strategy's
        json_request_data = json.loads(request.body.read())
        locator_strategy = json_request_data.get('using')
        value = json_request_data.get('value')

        if locator_strategy == "id":
            path = app.config.get("Element Mapping",value)
        elif locator_strategy == "name":
            path = os.path.join(app.image_path,value)
        elif locator_strategy == "xpath":
            path = value
        else:
            response.status = 501
            return {'sessionId': session_id, 'status': 32, 'value': 'Unsupported location strategy, use id, name, or XPath only. See docs for details.'}
        elem = autopy.bitmap.Bitmap.open(path)

        if not many:
            if context == "root":
                pos = autopy.bitmap.capture_screen().find_bitmap(elem,app.tolerance)
            else:
                canvas = autopy.bitmap.Bitmap.open(decode_value_from_wire(path))
                pos = canvas.find_bitmap(elem,app.tolerance)

            if pos is None:
                return {'sessionId': session_id, 'status': 7, 'value': 'Element not found'}

            found_elements = {'ELEMENT':encode_value_4_wire(path)}
        else:
            if context == "root":
                if autopy.bitmap.capture_screen().count_of_bitmap(elem,app.tolerance) == 0:
                    found_elements = []
                else:
                    temp_elements = []
                    result = autopy.bitmap.capture_screen().find_every_bitmap(elem,app.tolerance)
                    for pos in result:
                        temp_elements.append({'ELEMENT':encode_value_4_wire(path)})
                    found_elements = temp_elements
            else:
                canvas = autopy.bitmap.Bitmap.open(decode_value_from_wire(path))
                if canvas.count_of_bitmap(elem,app.tolerance) == 0:
                    found_elements = []
                else:
                    temp_elements = []
                    result = canvas.find_every_bitmap(elem,app.tolerance)
                    for pos in result:
                        temp_elements.append({'ELEMENT':encode_value_4_wire(path)})
                    found_elements = temp_elements
            
        return {'sessionId': session_id, 'status': 0, 'value': found_elements}
    except:
        response.status = 400
        return {'sessionId': session_id, 'status': 13, 'value': str(sys.exc_info()[0])}

@app.route('/wd/hub/session/<session_id>/screenshot', method='GET')
def get_screenshot(session_id=''):
    try:
        path = os.path.join(os.path.dirname(os.tempnam()),'autopydriver_screenshot.png')
        autopy.bitmap.capture_screen().save(path)
        with open(path, 'rb') as screenshot:
            encoded_file = base64.b64encode(screenshot.read())
        return {'sessionId': session_id, 'status': 0, 'value': encoded_file}
    except:
        response.status = 400
        return {'sessionId': session_id, 'status': 13, 'value': str(sys.exc_info()[0])}

@app.route('/wd/hub/session/<session_id>/keys', method='POST')
def keys(session_id=''):
    try:
        request_data = request.body.read()
        keys = json.loads(request_data).get('value')[0].encode('utf-8')
        autopy.key.type_string(keys)
        return {'sessionId': session_id, 'status': 0}
    except:
        response.status = 400
        return {'sessionId': session_id, 'status': 13, 'value': str(sys.exc_info()[0])}

@app.route('/wd/hub/session/<session_id>/element/<element_id>/location', method='GET')
def element_location(session_id='', element_id=''):
    try:
        path = decode_value_from_wire(element_id)
        elem = autopy.bitmap.Bitmap.open(path)
        pos = autopy.bitmap.capture_screen().find_bitmap(elem,app.tolerance)
        location = {'x': pos[0], 'y': pos[1]}
        return {'sessionId': session_id, 'status': 0, 'value': location}
    except:
        response.status = 400
        return {'sessionId': session_id, 'status': 13, 'value': str(sys.exc_info()[0])}
    
@app.route('/wd/hub/session/<session_id>/element/<element_id>/size', method='GET')
def element_size(session_id='', element_id=''):
    try:
        path = decode_value_from_wire(element_id)
        elem = autopy.bitmap.Bitmap.open(path)
        size = {'width': elem.width, 'height': elem.height}
        return {'sessionId': session_id, 'status': 0, 'value': size}
    except:
        response.status = 400
        return {'sessionId': session_id, 'status': 13, 'value': str(sys.exc_info()[0])}

@app.route('/wd/hub/session/<session_id>/element/<element_id>/displayed', method='GET')
def element_displayed(session_id='', element_id=''):
    try:
        path = decode_value_from_wire(element_id)
        elem = autopy.bitmap.Bitmap.open(path)
        pos = autopy.bitmap.capture_screen().find_bitmap(elem,app.tolerance)
        displayed = True if pos is not None else False
        return {'sessionId': session_id, 'status': 0, 'value': displayed}
    except:
        response.status = 400
        return {'sessionId': session_id, 'status': 13, 'value': str(sys.exc_info()[0])}

@app.error(404)
def unsupported_command(error):
    response.content_type = 'text/plain'
    return 'Unrecognized command, or AutoPyDriverServer does not support/implement this: %s %s' % (request.method, request.path)

def encode_value_4_wire(value):
    return urllib.pathname2url(base64.b64encode(value))

def decode_value_from_wire(value):
    return base64.b64decode(urllib.url2pathname(value))

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='AutoPyDriverServer - a webdriver-compatible server for use with desktop GUI automation via AutoPy library/tool.')
    #parser.add_argument('-v', dest='verbose', action="store_true", default=False, help='verbose mode')
    parser.add_argument('-a', '--address', type=str, default=None, help='ip address to listen on')
    parser.add_argument('-p', '--port', type=int, default=4723, help='port to listen on')
    parser.add_argument('-t', '--tolerance', type=float, default=0.0, help='define tolerance value for finding elements via images/bitmaps, see docs for details')
    parser.add_argument('-f', '--images_folder', type=str, default=None, help='define image folder containing element locator images for find by name, defaults to image subfolder within the app/server directory')
    parser.add_argument('-c', '--element_image_mapping_file',  type=str, default=None, help='define the element image mapping config file for find by ID, see default sample config file in the app/server directory')

    args = parser.parse_args()
    
    if args.address is None:
        try:
            args.address = socket.gethostbyname(socket.gethostname())
        except:
            args.address = '127.0.0.1'
    
    if args.element_image_mapping_file is not None:
        app.element_locator_map_file = args.element_image_mapping_file
    else:
        app.element_locator_map_file = os.path.join(os.path.curdir,'element_image_map.cfg')
    if args.images_folder is not None:
        app.image_path = args.images_folder
    else:
        app.image_path = os.path.join(os.path.curdir,'images')
    if args.tolerance != 0.0:
        app.tolerance = args.tolerance
    else:
        app.tolerance = 0.0

    app.config = ConfigParser.RawConfigParser()
    app.config.read(app.element_locator_map_file)

    app.SESSION_ID = "%s:%d" % (args.address, args.port)
    app.started = False
    run(app, host=args.address, port=args.port)
