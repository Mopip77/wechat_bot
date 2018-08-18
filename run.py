#!/usr/bin/env python3
import itchat
import time
import os


from trans import trans_from_text
from ocr import trans_from_img
from itchat.content import *

BAKFILE_PATH = 'bakfile/'
LOG_PATH = 'log/'
HISTORY_FILE_PATH = LOG_PATH + 'history.log'
VOICE_PATH = 'voice/'
IMG_PATH = 'img/'

def format_time(_time):
    t = _time
    t = time.localtime(t)
    t = time.strftime("%Y-%m-%d %H:%M:%S", t)
    return t

@itchat.msg_register(TEXT)
def text_reply(msg):
    from_nickname = msg.User.NickName
    create_time = format_time(msg.CreateTime)
    operate = msg.text.split(' ')[0]
    data = ' '.join(msg.text.split(' ')[1:])
    with open(HISTORY_FILE_PATH, 'a') as f:
        f.write(','.join([create_time,from_nickname,operate,data]) + '\n')
        f.close()
    operate = operate.upper()

    if operate == 'LS':
        res = ''
        for f in os.listdir(BAKFILE_PATH):
            res += f + '\n'
        return res
    
    elif operate == 'DL':
        if not data in os.listdir(BAKFILE_PATH):
            return '抱歉，没有该文件\n请用listfile命令查询所有文件'
        else:
            IMG_FORMAT = ['jpg', 'png', 'gif']
            VIDEO_FORMAT = ['mp4', 'mov']
            
            msg_type = 'fil'
            if data.split('.')[-1] in IMG_FORMAT:
                msg_type = 'img'
            elif data.split('.')[-1] in VIDEO_FORMAT:
                msg_type = 'vid'
            print(msg_type, data)
            itchat.send('@%s@%s' % (
                msg_type, BAKFILE_PATH + data),
                msg['FromUserName']
            )
    
    elif operate == 'TRANSZH':
        text = trans_from_text(data, 'zh')
        return text
    
    elif operate == 'TRANSEN':
        text = trans_from_text(data, 'en')
        return text


    elif operate == 'HELP':
        return '''ls,   查看共享文件夹下的文件
dl <file>,  下载共享文件夹的指定文件
trans<en, zh> <text>，  翻译text到中文或英文
发送图片,     ORC识别
发送语音，    保存下来（好像没卵用）'''
    else:
        return ('无该条指令！\n请输入help获取帮助！')
            
        
        
@itchat.msg_register(PICTURE)
def trans_img(msg):
    from_nickname = msg.User.NickName
    create_time = format_time(msg.CreateTime)
    
    file_path = IMG_PATH + msg.user.NickName + '_' + msg.fileName
    msg.download(file_path)
    trans_res = trans_from_img(file_path)
    
    with open(HISTORY_FILE_PATH, 'a') as f:
        f.write(','.join([create_time,from_nickname,'img',file_path]) + '\n')
        f.close()
    if trans_res:
        return trans_res
    else:
        return '抱歉，这张文件没有文字或服务器出现问题！'

@itchat.msg_register(VOICE, RECORDING)
def trans_voice(msg):
    from_nickname = msg.User.NickName
    create_time = format_time(msg.CreateTime)
    
    file_path = VOICE_PATH + msg.user.NickName +  '_' + msg.fileName
    msg.download(file_path)
    
    with open(HISTORY_FILE_PATH, 'a') as f:
        f.write(','.join([create_time,from_nickname,'voice',file_path]) + '\n')
        f.close()
    return '保存录音成功'

    

if __name__ == '__main__':
    if not os.path.exists(BAKFILE_PATH):
        os.mkdir(BAKFILE_PATH)
    if not os.path.exists(IMG_PATH):
        os.mkdir(IMG_PATH)
    if not os.path.exists(LOG_PATH):
        os.mkdir(LOG_PATH)
    if not os.path.exists(VOICE_PATH):
        os.mkdir(VOICE_PATH)
    if not os.path.exists(HISTORY_FILE_PATH):
        with open(HISTORY_FILE_PATH, 'w') as f:
            f.write('date, user, operate, data\n')
            f.close()
    
    itchat.auto_login(enableCmdQR=-2, hotReload=True)
    itchat.run()
