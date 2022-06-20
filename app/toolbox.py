#! /usr/bin/env python3
# -*- coding : utf-8 -*-

import re

license_BSD = """Copyright 2019-2022 Fabre Vincent <peigne.plume@gmail.com>

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."""


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
