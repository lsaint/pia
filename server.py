# -*- coding: utf-8 -*-

import json, time
from datetime import datetime, timedelta, date

from gevent.server import StreamServer

from session import *

DELIMITER = "\n"
BILLBOARD_NUM = 10



g_uid2name = {}

def cacheName():
    global g_uid2name
    ret = session.query(Uname)
    for q in ret:
        g_uid2name[q.uid] = q.name
cacheName()



def accept(socket, address):
    print 'New connection from %s:%s' % address
    buf = ""
    while True:
        buf =  "%s%s" % (buf, socket.recv(1024))
        if not buf:
            break
        if DELIMITER not in buf:
            continue
        la = buf.rindex(DELIMITER)
        buf, lines = buf[la+1:], buf[:la]
        lt = lines.splitlines()
        for line in lt:
            jn = json.loads(line)
            if type(jn) == dict:
                dispatch(jn, socket)


def dispatch(jn, socket):
    print "req", jn
    kwargs = jn["params"][0]
    method = eval(jn["method"])
    reply, err = method(**kwargs)
    jn = {"result":reply, "error":err, "id":jn["id"]}
    print "reply", jn
    socket.send(json.dumps(jn))



def setLogoutTime(**kwargs):
    print "setLogoutTime"
    uid = kwargs["Uid"]
    now = datetime.now()
    ret = session.query(Ltime).filter_by(uid=uid).first()
    if ret:
        ret.logout_time = now
    else:
        t = Ltime(uid, None, now)
        session.add(t)
    session.commit()
    return {"Time":now.ctime()}, None


def setLoginTime(**kwargs):
    print "setLoginTime"
    uid = kwargs["Uid"]
    now = datetime.now()
    ret = session.query(Ltime).filter_by(uid=uid).first()
    if ret:
        ret.login_time = now
    else:
        t = Ltime(uid, now, None)
        session.add(t)
    session.commit()
    return {"Time":now.ctime()}, None


def getLogTime(**kwargs):
    print "getLogTime"
    uid = kwargs["Uid"]
    ret = session.query(Ltime).filter_by(uid=uid).first()
    if ret:
        intime = "" if not ret.login_time else ret.login_time.ctime()
        outime = "" if not ret.logout_time else ret.logout_time.ctime()
    else:
        intime = ""
        outime = ""
    return {"Logintime":intime, "Logouttime":outime}, None


def modifyBalance(bank, **kwargs):
    uid = kwargs["Uid"]
    n = kwargs["Num"]
    ret = session.query(bank).filter_by(uid=uid).first()
    if ret:
        if n < 0 and ret.balance < -n:
            return {"Balance":ret.balance}, "not enough balance"
        ret.balance += n
        if ret.balance < 0:
            ret.balance = 0
    else:
        if n < 0:
            return {"Balance":0}, "not enough balance"
        ret = bank(uid, 0)
        if n > 0:
            ret.balance = n
        session.add(ret)

    session.commit()
    return {"Balance":ret.balance}, None


def batchModifyBalance(bank, **kwargs):
    bals = {}
    uids = kwargs["Uids"]
    n   = kwargs["Num"]
    if n < 0 :  # 暂只支持增加
        return {"Ubl":None}, None

    ret = session.query(bank).filter(bank.uid.in_(uids)).all()
    for r in ret:
        r.balance += n
        uids.remove(r.uid)
        bals[str(r.uid)] = r.balance

    for uid in uids:
        b = bank(uid, n)
        bals[str(uid)] = n
        session.add(b)

    session.commit()

    return {"Ubl":bals}, None


def batchModifyGold(**kwargs):
    print "batchModifyGold"
    return batchModifyBalance(GoldBank, **kwargs)


def batchModifySilver(**kwargs):
    print "batchModifySilver"
    return batchModifyBalance(SilverBank, **kwargs)


def modifyGold(**kwargs):
    print "modifyGold"
    return modifyBalance(GoldBank, **kwargs)


def modifySilver(**kwargs):
    print "modifySilver"
    return modifyBalance(SilverBank, **kwargs)


def getJudgeInfo(**kwargs):
    print "getJudgeInfo"
    ret = session.query(Judgement).first()
    if not ret:
        ret = Judgement(40, 1, 0, 0)
        session.add(ret)
        session.commit()
    return {"MercyCoef":ret.mercy_coef, "EvilCoef":ret.evil_coef,\
            "PandorasBox":ret.pandorasbox, "AngelFunds":ret.angel_funds}, None


def setJudgeInfo(**kwargs):
    print "setJudgeInfo"
    af = kwargs["AngelFunds"]
    pb = kwargs["PandorasBox"]
    ret = session.query(Judgement).first()
    if not ret:
        return {}, "no judge info"
    ret.angel_funds = af
    ret.pandorasbox = pb
    session.commit()
    return {}, None


def getBalance(**kwargs):
    print "getBalance"
    uids = kwargs["Uid"]
    ret = session.query(SilverBank).filter(SilverBank.uid.in_(uids)).all()
    bals = {}
    for r in ret:
        bals[str(r.uid)] = r.balance
    return {"Ubl":bals}, None


def setName(**kwargs):
    uid = kwargs["Uid"]
    name = kwargs["Name"]
    g_uid2name[uid] = name
    ret = session.query(Uname).get(uid)
    if ret:
        if name != ret.name:
            ret.name = name
    else:
        t = Uname(uid, name)
        session.add(t)
    session.commit()
    return {"Name":name}, None



def getBillboard(**kwargs):
    print "getBillboard"
    ret = session.query(SilverBank).order_by("balance desc")[:BILLBOARD_NUM]
    uids = []
    bals = []
    for i in ret:
        uids.append(i.uid)
        bals.append(i.balance)

    ret = []
    for i in range(len(uids)):
        name =  g_uid2name.get(uids[i])
        name = name if name else ""
        ret.append((name, str(bals[i])))

    print json.dumps(ret)
    return {"Billboard":ret}, None





if __name__ == '__main__':
    server = StreamServer(('127.0.0.1', 12100), accept)
    print "Starting pilipala's DB server on port 12100"
    server.serve_forever()


