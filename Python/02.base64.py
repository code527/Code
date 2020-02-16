#!/usr/bin/env python
# coding=utf-8

import base64
import pyperclip

path = raw_input('input image path:\n')
f = open(path,'rb') #二进制方式打开图文件
ls_f = base64.b64encode(f.read()) #读取文件内容，转换为base64编码
f.close()
pyperclip.copy(ls_f)
