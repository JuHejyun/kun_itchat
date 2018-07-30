#!/usr/bin/env python
# coding:utf8
 
import itchat
from multiprocessing import Process, Queue
from itchat.content import *
 
# 自动回复文本等类别消息
# isGroupChat=False表示非群聊消息
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isGroupChat=False)
def text_reply(msg):
    itchat.send('这是我的小号，暂无调戏功能，有事请加我大号：BMstock1', msg['FromUserName'])
 
# 自动回复图片等类别消息
# isGroupChat=False表示非群聊消息
@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], isGroupChat=False)
def download_files(msg):
    itchat.send('这是我的小号，暂无调戏功能，有事请加我大号：BMstock1', msg['FromUserName'])
 
# 自动处理添加好友申请
@itchat.msg_register(FRIENDS)
def add_friend(msg):
    itchat.add_friend(**msg['Text']) # 该操作会自动将新好友的消息录入，不需要重载通讯录
    itchat.send_msg(u'你好哇', msg['RecommendInfo']['UserName'])
     
# 自动回复文本等类别的群聊消息
# isGroupChat=True表示为群聊消息
@itchat.msg_register([TEXT, SHARING], isGroupChat=True)
def group_reply_text(msg):
    # 消息来自于哪个群聊
    chatroom_id = msg['FromUserName']
    # 发送者的昵称
    username = msg['ActualNickName']
 
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
        for item in chatroom_sync:
            if not item['UserName'] == chatroom_id:
                itchat.send('%s\n%s' % (username, msg['Content']), item['UserName'])
    elif msg['Type'] == SHARING:
        for item in chatroom_sync:
            if not item['UserName'] == chatroom_id:
                itchat.send('%s\n%s\n%s' % (username, msg['Text'], msg['Url']), item['UserName'])
 
# 自动回复图片等类别的群聊消息
# isGroupChat=True表示为群聊消息          
@itchat.msg_register([PICTURE, ATTACHMENT, VIDEO], isGroupChat=True)
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
    msg['Text'](msg['FileName'])
    # 转发至其他需要同步消息的群聊
    for item in chatroom_sync:
        if not item['UserName'] == chatroom_id:
            itchat.send('@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName']), item['UserName'])

if __name__ == '__main__':
    # 扫二维码登录
    itchat.auto_login(hotReload=True)
    # 获取所有通讯录中的群聊
    # 需要在微信中将需要同步的群聊都保存至通讯录
    chatrooms = itchat.get_chatrooms(update=True, contactOnly=True)
    #print ('chatrooms：', chatrooms)
    #chatroom_ids = [c['UserName'] for c in chatrooms]
    chatroom_ids=[]
    chatroom_sync=[]
    for c in chatrooms:
        if c['NickName'] in ['华大小分队','华大']:
            chatroom_ids.append(c['UserName'])
        elif c['NickName'].find('那些年')>=0:
        # if c['NickName'].index("那些年")>=0:
            chatroom_sync.append(c)
        #else:
            #print ('排除的：',c['NickName'])


    print (' '.join([item['NickName'] for item in chatrooms]))
    print ('正在监测的群聊：', len(chatroom_ids), '个')
    print ('监测的群聊id：', chatroom_ids)
    print ('同步群id：', chatroom_sync)
    # 开始监测
    itchat.run()


