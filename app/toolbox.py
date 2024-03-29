#! /usr/bin/env python3
# -*- coding : utf-8 -*-

import time

import re
import os
import json
import requests
import signal
from contextlib import contextmanager

from config import DEBUG, NVPN_URL

license_BSD = """Copyright 2019-2023 Fabre Vincent <peigne.plume@gmail.com>

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."""


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
data_file = os.path.join(BASE_DIR, "data.json")


def record_data(data):
    with open(data_file, 'w') as file:
        json.dump(data, file)


def load_data():
    with open(data_file, 'r') as file:
        data = json.load(file)
    return data


TIMEOUT = load_data()['timeout']


def debug_print(text):
    if DEBUG:
        print(text)


@contextmanager
def timeout(timer):
    def raise_timeout(signum, frame):
        raise TimeoutError
    # Register a function to raise a TimeoutError on the signal.
    signal.signal(signal.SIGALRM, raise_timeout)
    # Schedule the signal to be sent after ``time``.
    signal.alarm(int(timer))

    try:
        yield
    except TimeoutError:
        pass
    finally:
        # Unregister the signal so it won't be triggered
        # if the timeout is not reached.
        signal.signal(signal.SIGALRM, signal.SIG_IGN)


def get_countries():
    """Get contries and cities from NordVPN's API"""

    TIMEOUT = load_data()['timeout']
    payload = {}
    headers = {}

    timed_out = True
    with timeout(TIMEOUT):
        # time.sleep(5)
        response = requests.request("GET", NVPN_URL, headers=headers, data=payload)
        datas = json.loads(response.text)
        timed_out = False

    if timed_out:
        os.system("notify-send 'Nord Manager' 'Connection timed out, check your internet connection and try again'")
        return []

    countries = []
    for elem in datas:
        country = {}
        country['name'] = elem['name']
        country['cities'] = []

        for city in elem['cities']:
            country['cities'].append(city['name'])

        countries.append(country)
    return countries


def tri(text):
    list_out = []
    for line in text:
        line = line.strip()
        line = line.strip("-")
        print("==", line)
        if "," in line:
            cutting = line.split(", ")
        else:
            cutting = line.split("\t")
        for c in cutting:
            list_out.append(c)

    return list_out


def reg(text):
    liste = tri(text)
    liste2 = []
    for line in liste:
        m = re.match('(^[a-zA-Z])', line)
        if m is not None and "-" not in line:
            line = line.strip().strip("\n")
            liste2.append(line)
    liste2.sort()
    return liste2


def menu_builder(text):
    for i in reg(text):
        print(i)


def connection(place):
    TIMEOUT = load_data()['timeout']
    command = "nordvpn c {}".format(place.lower())
    timed_out = True
    with timeout(TIMEOUT):
        shortcut_connection(command)
        timed_out = False
    if timed_out:
        os.system("notify-send 'Nord Manager' 'Connection timed out, check your internet connection and try again'")


def shortcut_connection(command):
    """Opens the login page in web browser if not logged in with nordvpn"""
    debug_print("command sent...")
    # time.sleep(6)
    answer = os.popen(command).readlines()
    debug_print(answer)
    data = load_data()
    for text in answer:
        if data['not_logged_in'] in text:
            os.system("notify-send  'Nord Manager' 'You are not logged in'")
            answer = [text for text in os.popen("nordvpn login").readlines() if "browser" in text.lower()]
            url = answer[0].split(" ")[-1]
            os.system(f"xdg-open '{url}'")
