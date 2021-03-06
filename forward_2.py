#!/usr/bin/env python
# coding:utf8
import os

import itchat
import time
from multiprocessing import Process, Queue
from datetime import datetime
from itchat.content import *
 
# 自动回复文本等类别消息
# isGroupChat=False表示非群聊消息
# @itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isGroupChat=False)
# def text_reply(msg):
#     itchat.send('这是我的小号，暂无调戏功能，有事请加我大号：BMstock1', msg['FromUserName'])
 
# 自动回复图片等类别消息
# isGroupChat=False表示非群聊消息
# @itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], isGroupChat=False)
# def download_files(msg):
#     itchat.send('这是我的小号，暂无调戏功能，有事请加我大号：BMstock1', msg['FromUserName'])
 
# 自动处理添加好友申请
# @itchat.msg_register(FRIENDS)
# def add_friend(msg):
#     itchat.add_friend(**msg['Text']) # 该操作会自动将新好友的消息录入，不需要重载通讯录
#     itchat.send_msg(u'你好哇', msg['RecommendInfo']['UserName'])
     
# 自动回复文本等类别的群聊消息
# isGroupChat=True表示为群聊消息
@itchat.msg_register([TEXT, SHARING], isGroupChat=True)
def group_reply_text(msg):
    # 消息来自于哪个群聊
    chatroom_id = msg['FromUserName']
    # 发送者的昵称
    username = msg['ActualNickName']
    createtime = msg['CreateTime']

    # 消息并不是来自于需要同步的群
    if not chatroom_id in chatroom_ids:
        return
 
    if msg['Type'] == TEXT:
        content = msg['Content']
    elif msg['Type'] == SHARING:
        content = msg['Text']
 
    print (msg['Content'])

    # 根据消息类型转发至其他需要同步消息的群聊
    if msg['Type'] == TEXT:
        if chatroom_id in chatroom_delay_ids:
            q.put('%s %s:\n%s' % (time.strftime("%H:%M:%S",time.localtime(createtime)),username, msg['Content']))
        else:
            for item in chatroom_sync:
                if not item['UserName'] == chatroom_id:
                    itchat.send('%s %s:\n%s' % (time.strftime("%H:%M:%S",time.localtime(createtime)),username, msg['Content']), item['UserName'])
    elif msg['Type'] == SHARING:
        if chatroom_id in chatroom_delay_ids:
            q.put('%s %s(share):\n%s\n%s' % (time.strftime("%H:%M:%S",time.localtime(createtime)),username, msg['Text'], msg['Url']))
        else:
            for item in chatroom_sync:
                if not item['UserName'] == chatroom_id:
                    itchat.send('%s %s(share):\n%s\n%s' % (time.strftime("%H:%M:%S",time.localtime(createtime)),username, msg['Text'], msg['Url']), item['UserName'])
 
# 自动回复图片等类别的群聊消息
# isGroupChat=True表示为群聊消息          
@itchat.msg_register([PICTURE, ATTACHMENT, VIDEO, RECORDING], isGroupChat=True)
def group_reply_media(msg):
    # 消息来自于哪个群聊
    chatroom_id = msg['FromUserName']
    # 发送者的昵称
    username = msg['ActualNickName']
 
    # 消息并不是来自于需要同步的群
    if not chatroom_id in chatroom_ids:
        return
 
    # 如果为gif图片则不转发
    if msg['FileName'][-4:] == '.gif':
        return

    # 下载图片等文件
    msg['Text'](filepath+msg['FileName'])

    #语音文件仅保存
    if msg['Type'] == "Recording":
        return

    if chatroom_id in chatroom_delay_ids:
        tu.put('@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), filepath+msg['FileName']))
        return


    # 转发至其他需要同步消息的群聊
    for item in chatroom_sync:
        if not item['UserName'] == chatroom_id:
            itchat.send('@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), filepath+msg['FileName']), item['UserName'])

#获取文件路径
def getfilepath():
    # 系统当前时间年份
    year = time.strftime('%Y', time.localtime(time.time()))
    # 月份
    month = time.strftime('%m', time.localtime(time.time()))
    # 日期
    day = time.strftime('%d', time.localtime(time.time()))
    fileYear = year
    fileMonth = fileYear + '/' + month
    fileDay = fileMonth + '/' + day
    if not os.path.exists(fileYear):
        os.mkdir(fileYear)
        os.mkdir(fileMonth)
        os.mkdir(fileDay)
    else:
        if not os.path.exists(fileMonth):
            os.mkdir(fileMonth)
            os.mkdir(fileDay)
        else:
            if not os.path.exists(fileDay):
                os.mkdir(fileDay)
    return fileDay+'/'

def send_msg(q,tu,chatroom_sync):
    itchat.auto_login(hotReload=True)
    while True:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        allmsg=list()
        while not q.empty():
            value = q.get(True)  # 获取
            # print('Get %s from queue.' % value)
            allmsg.append('%s\n' % value)
        if len(allmsg):
            for item in chatroom_sync:
                # if not item['UserName'] == chatroom_id:
                # allmsg.reverse()
                print(''.join(str(e) for e in allmsg))
                itchat.send(''.join(str(e) for e in allmsg), item['UserName'])
        while not tu.empty():
            value = tu.get(True)  # 获取
            for item in chatroom_sync:
                itchat.send(value,item['UserName'])
        time.sleep(60*5)


#要监听的所有群
chatroom_ids=[]
#延时同步的群
chatroom_delay_ids=[]
#要同步的所有群
chatroom_sync=[]
# 父进程创建Queue，并传给各个子进程：
q = Queue()
tu = Queue()
filepath=''
if __name__ == '__main__':
    filepath = getfilepath()
    # 扫二维码登录
    itchat.auto_login(hotReload=True)
    # 获取所有通讯录中的群聊
    # 需要在微信中将需要同步的群聊都保存至通讯录
    chatrooms = itchat.get_chatrooms(update=True, contactOnly=True)
    #print ('chatrooms：', chatrooms)
    #chatroom_ids = [c['UserName'] for c in chatrooms]
    for c in chatrooms:
        # if c['NickName'] in ['华大小分队','华大']:
        if c['NickName'].find('北美股市科研小组')>=0 or c['NickName'].find('北美股市实战')>=0 or c['NickName'].find('投资交流')>=0 or c['NickName'].find('内购')>=0 or c['NickName'].find('代购')>=0 or c['NickName'].find('银行')>=0:
            chatroom_ids.append(c['UserName'])
            if c['NickName'].find('北美股市科研小组') >= 0 or c['NickName'].find('北美股市实战') >= 0 or c['NickName'].find('投资交流') >= 0 or c['NickName'].find('银行')>=0:
                chatroom_delay_ids.append(c['UserName'])
        elif c['NickName'].find('robot测试')>=0:
            chatroom_sync.append(c)
        #else:
            #print ('排除的：',c['NickName'])

    pr = Process(target=send_msg, args=(q,tu,chatroom_sync,))
    # 启动子进程pr，读取:
    pr.start()
    print (' '.join([item['NickName'] for item in chatrooms]))
    print ('正在监测的群聊：', len(chatroom_ids), '个')
    print ('监测的群聊id：', chatroom_ids)
    print ('同步群id：', chatroom_sync)
    # 开始监测
    itchat.run()


