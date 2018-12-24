#! /usr/bin/pytdon
# -*- coding:utf-8 -*- 

'''
cppcloud的webclient，为中心端间接的restful API和可视化展示/操作界面
'''

from flask import Flask,request,redirect, url_for,render_template
import json
import re
import datetime
import time
import os
import sys
sys.path.append("../")
from client_py.tcpclient import TcpClient
from client_py.cliconfig import config
from client_py.const import *

gweb_cli = None
# http server
app = Flask(__name__)

@app.route('/test')
def test():
    cmd = request.args.get("cmd")
    resp = gweb_cli.request(CMD_TESTING_REQ, {
        "cmd": cmd, "toSvr": 990})
    return resp

@app.route('/confname')
def confname():
    return gweb_cli.request(CMD_GETCFGNAME_REQ, {})

@app.route('/getconf')
def qconf():
    return gweb_cli.request(CMD_GETCONFIG_REQ, {
        "file_pattern": request.args.get("file_pattern"),
        "key_pattern": request.args.get("key_pattern"),
        "gt_mtime": int(request.args.get("gt_mtime", 0)),
        "incbase": int(request.args.get("incbase", 0))
    })

@app.route('/bookchange')
def bookchange():
    rsp = gweb_cli.request(CMD_BOOKCFGCHANGE_REQ, {
        "file_pattern": request.args.get("file_pattern"),
        "incbase": int(request.args.get("incbase", 0))
    })
    print("bookchange resp:"+rsp)
    return rsp

@app.route('/setconf', methods=['POST'])
def setconf():
    data = request.get_data()
    #print(type(data))
    print(request.json)
    return gweb_cli.request(CMD_SETCONFIG_REQ, request.json)

@app.route('/svrall')
def svrall():
    rsp = gweb_cli.request(CMD_SVRSHOW_REQ, {
        "regname": request.args.get("regname", "")
    })
    return rsp

@app.route('/qsvr') # 服务发现
def qsvr():
    rsp = gweb_cli.request(CMD_SVRSEARCH_REQ, {
        "regname": request.args.get("regname", ""),
        "idc": int(request.args.get("idc", 0)),
        "rack": int(request.args.get("rack", 0)),
        "bookchange": int(request.args.get("bookchange", 0))
    })
    return rsp

@app.route('/regsvr', methods=['POST'])
def regsvr():
    return gweb_cli.request(CMD_SVRREGISTER_REQ, request.json)

# svrid=0时获取所有
@app.route('/clidata/<int:svrid>')
def clidata(svrid):
    key = request.args.get('key', '')
    return gweb_cli.request(CMD_GETCLI_REQ, { "key": key, "svrid": svrid })

@app.route('/notify/<string:cmd>')
def command(cmd):
    intKey = ('prvdid', 'svrid', 'weight', 'enable')
   
    reqobj = dict(request.args.items())
    reqobj["notify"] = cmd

    for key in intKey:
        if key in reqobj:
            reqobj[key] = int(reqobj[key])

    if 'closelink' == cmd:
        pass
    else:
        reqobj['to'] = int(reqobj['svrid'])
        del reqobj['svrid']
    

    #if 'shellcmd' == cmd:
    #    reqobj['cmdid'] = request.args.get('cmdid')

    return gweb_cli.request(CMD_EVNOTIFY_REQ, reqobj)

def onNotifyMsg(cmdid, seqid, msg):
    print(msg)

@app.route('/runlog/<int:svrid>')
def runlog(svrid):
    return gweb_cli.request(CMD_APPRUNLOG_REQ, {"to": svrid, "type": 1})

def onRunLogReq(cmdid, seqid, msg):
    print(msg)
    dictmsg = json.loads(msg);
    gweb_cli.post_msg(CMD_APPRUNLOG_RSP, seqid, 
        {"log": 1234, "to": dictmsg["from"]})

if __name__ == '__main__':
    gweb_cli = TcpClient(
        ('vpc2', 4800),
        clitype = 20,
        svrid = 990,
        aliasname="tag1",
        svrname = "Web-Ctrl",
        desc = "CppCloud-Web-Serv"
    )

    gweb_cli.setCmdHandle(CMD_EVNOTIFY_REQ, onNotifyMsg);
    gweb_cli.setCmdHandle(CMD_APPRUNLOG_REQ, onRunLogReq);

    if gweb_cli.start():
        #app.debug = True
        host = config.get('http_host', '0.0.0.0')
        port = config.get('http_port', 80)

        app.response_class.default_mimetype = 'application/json; charset=utf-8'
        app.run(host=host,port=port) # , threaded=True

        gweb_cli.shutdown()
