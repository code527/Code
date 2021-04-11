#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading
import urllib
import urllib2
import redis
import logging
import re
import uuid
import json
import time
import datetime
import io
import os
import Queue
from crypto import random 
from crypto.PublicKey import RSA
from crypto.Cipher import PKCS1_v1_5 as Cipher_pkcsl_v1_5
from crypto.Cipher import _DES3
import base64
import hashlib
import hmac
from hashlib import md5
 
reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s|%(thread)d|%(filename)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='uniqueLogin.log',
                    filemode='a')
def PrintLog(msg,ln=0):
	logging.warning(str(ln) + "|" + str(msg))
	print(str(ln) + "|" + str(msg))
	
expireTime = 7*86400
pool = None
ssoGetTokenUrl = ""
ssoGetInfoUrl = ""
getCrmInfoUrl = ""
deskey = "zheshisuibianzhaodeyiduanshuju"
descbc = "huohuaim"

condiation = "QA"
#condiation = "SIM"
#condiation = "ONLINE"

if (condiation == "QA"):
	ssoGetTokenUrl = "http://sso.qa.huohua.cn/oauth/token?"
	ssoGetInfoUrl = "http://sso.qa.huohua.cn/authentication/user?access_token="
	getCrmInfoUrl = "http://employee.qa.huohua.cn/im/info"
	pool = redis.ConnectionPool(host="redis.qa.huohua.cn", port=6379, db=15, password="AcUVeRb8lN", decode_responses=False)
elif (condiation == "SIM"):
	ssoGetTokenUrl = "http://sso.sim.huohua.cn/oauth/token?"
	ssoGetInfoUrl = "http://sso.sim.huohua.cn/authentication/user?access_token="
	getCrmInfoUrl = "http://employee.sim.huohua.cn/im/info"
	pool = redis.ConnectionPool(host="redis.sim.huohua.cn", port=6379, db=13, password="AcUVeRb8lN", decode_responses=False)
else:
	ssoGetTokenUrl = "http://sso.huohua.cn/oauth/token?"
	ssoGetInfoUrl = "http://sso.huohua.cn/authentication/user?access_token="
	getCrmInfoUrl = "http://employee.s.huohua.cn/im/info"
	pool = redis.ConnectionPool(host="imredis.qc.huohua.cn", port=6379, db=0, password="QN!GODRt", decode_responses=False)

def formatResp(msg,dat,code):
	suc = False
	if (int(code) == 0):
		suc = True
	return (json.dumps({"code":code,"success":suc, "message":msg,"data":dat}))
	
class UriParam:
	def __init__(self, uri):
		try:
			self.dict = {}
			params = uri.split('&')
			if (len(params) > 0):
				for item in params:
					kv = item.split('=')
					if (len(kv) < 2):
						self.dict[kv] = ''
					else:
						self.dict[kv[0]] = kv[1]
		except Exception, e:
			print e
	def Len(self):
		return len(self.dict)
	def Get(self, key, bUrlDecode = True):
		if (bUrlDecode == True):
			return urllib.unquote(self.dict.get(key, ''))
		return self.dict.get(key, '')

def Des3Decode(text):
	key = md5(deskey).hexdigest()[8:]
	cryptor = _DES3.new(key, _DES3.MODE_CBC, descbc)
	return cryptor.decrypt(base64.standard_b64decode(text))
def Des3Encode(text):
	key = md5(deskey).hexdigest()[8:]
	cryptor = _DES3.new(key, _DES3.MODE_CBC, descbc)
	return base64.standard_b64encode(cryptor.encrypt(text+"|"*(8-(len(text)%8))))
#mw=Des3Encode("thisisatest")
#print mw
#print Des3Decode(mw)


def createRSA():
	#伪随机数生成器 
	random_generator = Random.new().read 
	# rsa算法生成实例 
	key = RSA.generate(1024, random_generator) 
	#key = RSA.generate(1024)
	pub = key.publickey().exportKey()
	#PrintLog(pub, sys._getframe().f_lineno)
	pri = key.exportKey()
	#PrintLog(pri, sys._getframe().f_lineno)
	return (pub,pri)
	
def GetTokenFromSSO(getTokenUrl):
	try:
		PrintLog(getTokenUrl, sys._getframe().f_lineno)
		request = urllib2.Request(getTokenUrl)
		request = urllib2.Request(getTokenUrl, data="", headers = {'Authorization':'Basic aW06aW0='})
		response = urllib2.urlopen(request)
		retCode = response.getcode()
		retText = response.read()
		response.close()
		PrintLog(retCode, sys._getframe().f_lineno)
		PrintLog(retText, sys._getframe().f_lineno)
		if (retCode == 200):
			res = json.loads(retText)
			userToken = res["access_token"]
			if (userToken != ""):
				return userToken
	except (urllib2.URLError,urllib2.HTTPError),e:
		PrintLog(e.reason, sys._getframe().f_lineno)
	except Exception, e:
		PrintLog(e, sys._getframe().f_lineno)
	return ""
	
def GetTokenFromSSOByCode(userCode,redirectUrl):
	getTokenUrl = ssoGetTokenUrl + "grant_type=authorization_code&code=" +  str(userCode) + "&redirect_uri=" + redirectUrl
	return GetTokenFromSSO(getTokenUrl)

def GetTokenFromSSOByPwd(useremail,passwd):
	getTokenUrl = ssoGetTokenUrl + "grant_type=password&username=" +  str(useremail) + "&password=" + passwd
	return GetTokenFromSSO(getTokenUrl)

def GetUserInfoFromSSO(userToken):
	try:
		getInfoUrl = ssoGetInfoUrl + userToken
		PrintLog(getInfoUrl, sys._getframe().f_lineno)
		request = urllib2.Request(getInfoUrl)
		request.add_header('Authorization', 'Basic aW06aW0=')
		response = urllib2.urlopen(request)
		retCode = response.getcode()
		retText = response.read()
		response.close()
		PrintLog(retCode, sys._getframe().f_lineno)
		PrintLog(retText, sys._getframe().f_lineno)
		if (retCode == 200):
			return retText
	except (urllib2.URLError,urllib2.HTTPError),e:
		PrintLog(e.reason, sys._getframe().f_lineno)
	except Exception, e:
		PrintLog(e, sys._getframe().f_lineno)
	return ""
	
def GetUserInfoByEmailAndPasswd(mail,passwd):
	try:
		getInfoUrl = getCrmInfoUrl
		PrintLog(getInfoUrl, sys._getframe().f_lineno)
		request = urllib2.Request(getInfoUrl, data=json.dumps({"username":mail, "password":passwd}))
		request.add_header('Content-Type', 'application/json')
		response = urllib2.urlopen(request)
		retCode = response.getcode()
		retText = response.read()
		response.close()
		PrintLog(retCode, sys._getframe().f_lineno)
		PrintLog(retText, sys._getframe().f_lineno)
		if (retCode == 200):
			jsn = json.loads(retText)
			if (jsn.has_key("code") and int(jsn["code"]) == 0):
				if (jsn.has_key("userModel")):
					return json.dumps(jsn["userModel"])
	except (urllib2.URLError,urllib2.HTTPError),e:
		PrintLog(str(e), sys._getframe().f_lineno)
		PrintLog(e.reason, sys._getframe().f_lineno)
	except Exception, e:
		PrintLog(e, sys._getframe().f_lineno)
	return ""

def GetImid(crmid):
	return int(crmid)*256+2
	
def AuthApp(crmId,devId,appId,appToken):
	PrintLog("AuthApp: " + str((crmId,devId,appId,appToken)), sys._getframe().f_lineno)
	imid = GetImid(crmId)
	rkey = "imTokenOfUser:"+str(imid)+"."+str(devId)
	redisConn = redis.Redis(connection_pool=pool)
	priKey = redisConn.get(rkey)
	if (priKey is None):
		return False
	priKey = base64.b64decode(priKey)
	try:
		rsakey = RSA.importKey(priKey)
		cipher = Cipher_pkcsl_v1_5.new(rsakey)
		info = cipher.decrypt(base64.b64decode(appToken), None)
		PrintLog(info, sys._getframe().f_lineno)
		info = info.split("|")
		if (info[1] == crmId and info[2] == devId and info[5] == appId):
			devType = info[3]
			appType = info[4]
			currTime = int(time.mktime(datetime.datetime.now().timetuple()))
			loginKey = "uniqueLogin:" + str(crmId) + "." + str(devType) + "." + str(appType) + "." + str(devId)
			loginTime = redisConn.get(loginKey)
			if (loginTime is None or int(loginTime)+expireTime < currTime):
				PrintLog("AuthApp, token expire !", sys._getframe().f_lineno)
				return False
			return True
		PrintLog("decrypt info error", sys._getframe().f_lineno)
	except Exception, e:
		PrintLog(str(e), sys._getframe().f_lineno)
	return False
	
def Logout(crmId,devId,session):
	imid = GetImid(crmId)
	rkey = "imTokenOfUser:"+str(imid)+"."+str(devId)
	redisConn = redis.Redis(connection_pool=pool)
	priKey = redisConn.get(rkey)
	if (priKey is None):
		return False
	priKey = base64.b64decode(priKey)
	try:
		rsakey = RSA.importKey(priKey)
		cipher = Cipher_pkcsl_v1_5.new(rsakey)
		info = cipher.decrypt(base64.b64decode(session),None)
		PrintLog(info, sys._getframe().f_lineno)
		info = info.split("|")
		if (info[1] == crmId and info[2] == devId and info[5] == "im"):
			devType = info[3]
			appType = info[4]
			loginKey = "uniqueLogin:" + str(crmId) + "." + str(devType) + "." + str(appType) + "." + str(devId)
			redisConn.delete(loginKey)
			return True
	except Exception, e:
		PrintLog(str(e), sys._getframe().f_lineno)
	return False
		
def GetDdToken():
	try:
		getTokenUrl = "https://oapi.dingtalk.com/gettoken?appkey=dingv9w2quozitlexnyl&appsecret=PBJVMWH50BanTKP8CGsnXBEIdwZTk5BYD19BUjjPxFotmZ2fh6ZfJRREqoRySuMa"
		request = urllib2.Request(getTokenUrl)
		response = urllib2.urlopen(request)
		retCode = response.getcode()
		retText = response.read()
		response.close()
		PrintLog(retCode, sys._getframe().f_lineno)
		PrintLog(retText, sys._getframe().f_lineno)
		if (retCode == 200):
			res = json.loads(retText)
			errcode = res["errcode"]
			if (errcode == 0):
				return res["access_token"]
	except (urllib2.URLError,urllib2.HTTPError),e:
		PrintLog(e.code, sys._getframe().f_lineno)
		PrintLog(e.reason)
	except Exception, e:
		PrintLog(e, sys._getframe().f_lineno)
	return ""

def GetDdUserId(unionid):
	try:
		accessToken = GetDdToken()
		getUrl = "https://oapi.dingtalk.com/user/getUseridByUnionid?access_token=" + accessToken + "&unionid=" + unionid
		request = urllib2.Request(getUrl)
		response = urllib2.urlopen(request)
		retCode = response.getcode()
		retText = response.read()
		response.close()
		PrintLog(retCode, sys._getframe().f_lineno)
		PrintLog(retText, sys._getframe().f_lineno)
		if (retCode == 200):
			res = json.loads(retText)
			errcode = res["errcode"]
			if (errcode == 0):
				return res["userid"]
	except (urllib2.URLError,urllib2.HTTPError),e:
		PrintLog(e.code, sys._getframe().f_lineno)
		PrintLog(e.reason)
	except Exception, e:
		PrintLog(e, sys._getframe().f_lineno)
	return ""

def GetUnionidFromDD(tmpcode):
	tm = int(time.time()*1000)
	sec = "ULYjcaAksAi7x7Gu0O4fP98tpaGzm9DXAldRsNToi7C9W_HfmzL4LmIB2O3fPqbe"
	signature = base64.b64encode(hmac.new(sec, str(tm), digestmod=hashlib.sha256).digest())
	PrintLog(signature, sys._getframe().f_lineno)
	try:
		ddUrl = "https://oapi.dingtalk.com/sns/getuserinfo_bycode?signature=" + urllib.quote(signature) + "&timestamp=" + str(tm) + "&accessKey=dingoa8nbvgtpctt2edzph"
		PrintLog(ddUrl, sys._getframe().f_lineno)
		request = urllib2.Request(ddUrl, data=json.dumps({"tmp_auth_code":tmpcode}))
		request.add_header('Content-Type', 'application/json')
		response = urllib2.urlopen(request)
		retCode = response.getcode()
		retText = response.read()
		response.close()
		PrintLog(retCode, sys._getframe().f_lineno)
		PrintLog(retText, sys._getframe().f_lineno)
		if (retCode == 200):
			jsn = json.loads(retText)
			if (jsn.has_key("errcode") and int(jsn["errcode"]) == 0):
				if (jsn.has_key("user_info")):
					if (jsn["user_info"].has_key("unionid")):
						return jsn["user_info"]["unionid"]
	except (urllib2.URLError,urllib2.HTTPError),e:
		PrintLog(str(e), sys._getframe().f_lineno)
		PrintLog(e.reason, sys._getframe().f_lineno)
	except Exception, e:
		PrintLog(e, sys._getframe().f_lineno)
	return ""

#unionid = GetUnionidFromDD("6520551e2e8b386a91d60708366bd633")
#GetDdUserId(unionid)
	
class Handler(BaseHTTPRequestHandler):
	
	def do_OPTIONS(self):

		self.send_response(200)
		##self.send_header('Access-Control-Allow-Origin', '*');
		#self.send_header('Access-Control-Allow-Methods', 'GET,POST,OPTIONS');
		#self.send_header('Access-Control-Allow-Headers', 'user-token,DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range');
		#self.send_header('Access-Control-Max-Age', '1728000');
		self.send_header('Content-Type', 'application/json; charset=utf-8');
		self.send_header('Content-Length', '0');
		self.end_headers()
	
	def Response(self,resp,ct,ll=0):
		self.send_response(200)
		##self.send_header('Access-Control-Allow-Origin', '*');
		#self.send_header('Access-Control-Allow-Methods', 'GET,POST,OPTIONS');
		#self.send_header('Access-Control-Allow-Headers', 'user-token,DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range');
		#self.send_header('Access-Control-Expose-Headers', 'Content-Length,Content-Range');
		self.send_header('Content-type', ct)
		if (ll == 0):
			ll = len(resp.encode('utf-8'))
		self.send_header("Content-Length", ll)
		self.end_headers()
		PrintLog("response: "+resp, sys._getframe().f_lineno)
		self.wfile.write(resp)

	def do_GET(self):
		try:
			query = urllib.splitquery(self.path)
			self.process(query, query[1])
		except Exception, e:
			PrintLog(str(e), sys._getframe().f_lineno)
			self.Response(formatResp("fail",str(e), 110), 'application/json; charset=utf-8')
	
	def do_POST(self):
		try:
			query = urllib.splitquery(self.path)
			body = self.rfile.read(int(self.headers['content-length']))
			self.process(query, body)	
		except Exception, e:
			PrintLog(str(e), sys._getframe().f_lineno)
			self.Response(formatResp("fail",str(e), 110), 'application/json; charset=utf-8')

	def process(self, query, data):
		tmp1 = self.path
		mm = ''
		pos = tmp1.find("pwd")
		if (pos > 0):
			mm = Des3Encode(tmp1[pos:])
			tmp1 = tmp1[0:pos] + mm
		tmp2 = data
		pos = tmp2.find("pwd")
		if (pos > 0):
			tmp2 = data[0:pos]+mm
		PrintLog(tmp1 + "\nparameters:" + str(tmp2), sys._getframe().f_lineno)
		#PrintLog(self.headers,  sys._getframe().f_lineno)
		if (query[0] != "/auth" and query[0] != "/verify" and query[0] != "/logout" and query[0] != "/ddauth"):
			self.Response(formatResp("fail","not support!", 111), 'application/json; charset=utf-8')
			return ""
			
		params = UriParam(query[1])
		if (params.Len() == 0):
			self.Response(formatResp("fail","parameters error", 112), 'application/json; charset=utf-8')
			return ""
		if (query[0] == "/verify"):
			crmId   = params.Get("userId")
			appId    = params.Get("appId")
			devId    = params.Get("devId")
			appToken = self.headers["user-token"]
			PrintLog(appToken, sys._getframe().f_lineno)
			if (AuthApp(crmId,devId,appId,appToken)):
				self.Response(formatResp("","ok", 0), 'application/json; charset=utf-8')
			else:
				self.Response(formatResp("fail","can't tell you", 401), 'application/json; charset=utf-8')
		elif (query[0] == "/ddauth"):
			tmpcode = params.Get("tmpcode")
			unionid = GetUnionidFromDD(tmpcode)
			useremail = GetDdUserId(unionid)
			resp = {"email":useremail}
			self.Response(formatResp("",resp, 0), 'application/json; charset=utf-8')
		elif (query[0] == "/logout"):
			crmId   = params.Get("userId")
			devId    = params.Get("devId")
			session = self.headers['user-token']
			if (Logout(crmId,devId,session)):
				self.Response(formatResp("","ok", 0), 'application/json; charset=utf-8')
			else:
				self.Response(formatResp("fail","logout fail", 401), 'application/json; charset=utf-8')
		else:
			devId    = params.Get("devId")
			devType  = params.Get("devType")
			appType  = params.Get("appType")
			userEmail  = params.Get("mail")
			userToken = ""
			if (userEmail != ""):
				userPasswd = params.Get("pwd",False)
				PrintLog(userPasswd, sys._getframe().f_lineno)
				###userPasswd = Des3Decode(userEmail, userPasswd)
				#userInfo = GetUserInfoByEmailAndPasswd(userEmail, userPasswd)
				#self.ReturnInfo(userInfo, devId, devType, appType)
				userToken = GetTokenFromSSOByPwd(userEmail, userPasswd)
			else:
				userCode = params.Get("code")
				redirect = params.Get("srcUrl")
				userToken = GetTokenFromSSOByCode(userCode, redirect)
			if (userToken == ""):
				self.Response(formatResp("fail","sso auth fail", 113), 'application/json; charset=utf-8')
			else:
				userInfo = GetUserInfoFromSSO(userToken)
				self.ReturnInfo(userInfo, devId, devType, appType, userToken)
					
	def ReturnInfo(self, userInfo, devId, devType, appType, ssoToken):
		if (userInfo == ""):
			self.Response(formatResp("fail","sso auth fail", 114), 'application/json; charset=utf-8')
		else:
			info = json.loads(userInfo)
			if (not info.has_key("id")):
				self.Response(formatResp("fail","sso server error", 115), 'application/json; charset=utf-8')
			else:
				currTime = str(int(time.mktime(datetime.datetime.now().timetuple())))
				crmId = info["id"]
				imId = str(GetImid(crmId))
				redisConn = redis.Redis(connection_pool=pool)
				# save login time to redis
				loginKey = "uniqueLogin:" + str(crmId) + "." + str(devType) + "." + str(appType) + "." + str(devId)
				redisConn.setex(loginKey,expireTime,currTime)
				
				# read or generate rsa public key
				rkey = "imPUBTokenOfUser:"+str(imId)+"."+str(devId)
				PrintLog(rkey, sys._getframe().f_lineno)
				#pubKey = redisConn.get(rkey)
				#PrintLog("---" + str(pubKey) + "+++")
				if True: #(pubKey is None):
					(publicKey,pri) = createRSA()
					redisConn.setex("imPUBTokenOfUser:" + str(imId) + "." + devId, expireTime, base64.b64encode(bytes(publicKey)))
					redisConn.setex("imTokenOfUser:" + str(imId) + "." + devId, expireTime, base64.b64encode(bytes(pri)))

					pubKey = publicKey[27:-25].replace("\n","")
					#publicKey = "-----BEGIN PUBLIC KEY-----\n"+pubKey+"\n-----END PUBLIC KEY-----\n"
					rsakey = RSA.importKey(publicKey)
					cipher = Cipher_pkcsl_v1_5.new(rsakey)
					
					msg = currTime 
					msg += "|" + str(crmId) + "|" + str(devId) + "|" + str(devType) + "|" + str(appType)
					session = base64.b64encode(cipher.encrypt(bytes(msg+"|im")))				
					appId = ["CRM0100","CRM0101"];appToken = []
					for aid in appId:
						msgT = msg + "|" + str(aid)
						ak = base64.b64encode(cipher.encrypt(bytes(msgT)))
						appToken.append({"appid":aid,"token":ak})
					
					resp = {"uid":crmId,"name":info["name"],"session":session,"imid":imId,"secKey":pubKey,"appToken":appToken,"stk":ssoToken}
					self.Response(formatResp("",resp, 0), 'application/json; charset=utf-8')

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

                                                               
if __name__ == '__main__':
	port = 8182
	if(len(sys.argv) > 1):
		port = int(sys.argv[1])
	server = ThreadedHTTPServer(('', port), Handler)
	#print 'starting server, use <Ctrl-C> to stop'
	server.serve_forever()
    
