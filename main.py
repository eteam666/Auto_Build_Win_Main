# -*- coding: utf-8 -*-
import sqlite3
import os
import requests
from requests import HTTPError
from sys import platform
import json
import urllib.request
import zipfile
import configparser
import shutil
import smtplib
import subprocess
import patoolib
import time
from multiprocessing import Process
import random
import string
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
# 加载配置文件
config = configparser.ConfigParser()
config.read('Config.ini')
# 读取配置文件中的变量
LANG = config['Set']['Lang']
UUPUrl = config['Set']['UUPUrl']
TIME = config['Set']['Time']
UseESD = config['Set']['UseESD']
ApiUrl = config['Api']['Url']
BuildID = config['Build']['BuildID']
ImageName = config['Build']['ImageName']
UseMail = config['Mail']['Use']
Sender = config['Mail']['Sender']
Receiver = config['Mail']['Receiver']
Subject = config['Mail']['Subject']
Server = config['Mail']['Server']
User = config['Mail']['User']
PassWord= config['Mail']['Password']
remotes = config.get('Rclone', 'remotes').split(',')
folder = config['Rclone']['folder']
UseRclone = config['Rclone']['Use']
UseNewPost = config['NewPost']['Use']
WPURL = config['NewPost']['WPURL']
WPUser = config['NewPost']['WPUser']
WPPassword = config['NewPost']['WPPassword']
PostTitle = config['NewPost']['WPTitle']
smtp_log_config = {'server': Server,'user': User,'password': PassWord,'sender': Sender,'receiver': Receiver,'subject': Subject}
txt_log_config = {'file': 'log.txt'}
Verison = '1.1.0'
DOWNLOAD_PATH = os.getcwd()
updateId = ''
TempISO = DOWNLOAD_PATH + '\\Temp\\' + 'ISO'
MountDir = DOWNLOAD_PATH +  '\\Mount'
Temp = DOWNLOAD_PATH + '\\Temp'
cmd = Temp + '\\uup_download_windows.cmd'
ESD = Temp + '\\' + ImageName + '.esd'
OK=1
def ERROR():
        # 连接到数据库
        conn = sqlite3.connect('web.db')
        # 创建游标
        cursor = conn.cursor()
        if id == 1:
            status = 1
        else:
            status = 2
        # 更新指定行的值
        cursor.execute("UPDATE status SET status = ? WHERE rid = ?", (0, rid))
        # 提交事务
        conn.commit()
        # 关闭连接
        conn.close()
def END(id):
        gettime()
        # 连接到数据库
        conn = sqlite3.connect('web.db')
        # 创建游标
        cursor = conn.cursor()
        # 更新指定行的值
        cursor.execute("UPDATE log SET endtime = ? WHERE rid = ?", (localtime, rid))
        # 提交事务
        conn.commit()
        # 关闭连接
        conn.close()
        # 创建游标
        cursor = conn.cursor()
        if id == 1:
            status = 1
        else:
            status = 2
        # 更新指定行的值
        cursor.execute("UPDATE log SET status = ? WHERE rid = ?", (status, rid))
        # 提交事务
        conn.commit()
        # 关闭连接
        conn.close()
def NewLog():
        # 连接到数据库（如果数据库不存在，会自动新建）
        conn = sqlite3.connect('web.db')
        # 创建游标
        cursor = conn.cursor()
        gettime()
        # 插入值
        cursor.execute("INSERT INTO log(starttime,endtime,rid,status) VALUES (?,?,?,?)", (localtime, None, rid, 3))
        # 提交事务
        conn.commit()
        # 关闭连接
        conn.close()
def random_string(length):
    return ''.join(random.choices(string.ascii_uppercase+string.ascii_lowercase+string.digits+string.ascii_uppercase+string.ascii_lowercase, k=length))
def init():
    if not os.path.exists('data.db'):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        try:
            cursor.execute("CREATE TABLE verison (updateId INTEGER)")
        except sqlite3.OperationalError:
            pass
        conn.commit()
        conn.close()
    if not os.path.exists('web.db'):
        conn = sqlite3.connect('web.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE status (status int)''')
        cursor.execute("INSERT INTO status (status) VALUES (2)")
        conn.commit()
        conn.close()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE log (starttime TIMESTAMP DEFAULT NULL, endtime TIMESTAMP DEFAULT NULL, rid INTEGER DEFAULT NULL, status INTEGER DEFAULT NULL)''')
        conn.commit()
        conn.close()

def Change(id):
    conn = sqlite3.connect("web.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE status SET status = ?", (id,))
    conn.commit()
    conn.close()
    return
def gettime():
    global localtime
    localtime = time.localtime()
    localtime = time.strftime("%Y-%m-%d %H:%M:%S", localtime)
class Logger:
    def __init__(self, log_types, log_configs):
        self.log_types = log_types
        self.log_configs = log_configs
    def log_to_smtp(self, message, config):
        gettime()
        msg = f"信息报告: {localtime} :{Subject}\n\n{message}"
        server = smtplib.SMTP()
        server.sendmail(Sender,Receiver, msg)
        server.quit()
    def log_to_txt(self, message, config):
        with open(config['file'], 'a') as f:
            gettime()
            f.write(localtime + " ： " + message + '\n')
    def log_to_console(self, message):
        gettime()
        print(localtime + " ： " + message)
    def log(self, id):
        for log_type, log_config in zip(self.log_types, self.log_configs):
                # 加载配置文件
            config = configparser.ConfigParser()
            config.read('Lang.ini', encoding='utf-8')

            message = config[LANG][str(id)]
            if log_type == 'smtp':
                if UseMail != 1:
                    return
                self.log_to_smtp(message, log_config)
            elif log_type == 'txt':
                self.log_to_txt(message, log_config)
            elif log_type == 'console':
                self.log_to_console(message)
def search_updateId(updateId):
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM verison WHERE updateId=?", (updateId,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return True
        else:
            return False
def Welcome():                                                          #欢迎
    print("欢迎使用Auto Build Windows")
    print("自动构建第三方Windows辅助工具")
    print("本项目不是Microsoft旗下项目")
    print("官网:https://autobuild.win")
    print("程序版本: " + Verison)
    resp = urllib.request.urlopen(ApiUrl)
    if resp.status == 200:
        NewVerison = resp.read()
        data = json.loads(NewVerison)
        NewVerison = data['response']['apiVersion']
        print("UUP API最新版本：" + NewVerison)
        NewVerison = data['jsonApiVersion']
        print("UUP API最新版本：" + NewVerison)
    print("""
                _          ____        _ _     _  __          ___           _                   
     /\        | |        |  _ \      (_) |   | | \ \        / (_)         | |                  
    /  \  _   _| |_ ___   | |_) |_   _ _| | __| |  \ \  /\  / / _ _ __   __| | _____      _____ 
   / /\ \| | | | __/ _ \  |  _ <| | | | | |/ _` |   \ \/  \/ / | | '_ \ / _` |/ _ \ \ /\ / / __|
  / ____ \ |_| | || (_) | | |_) | |_| | | | (_| |    \  /\  /  | | | | | (_| | (_) \ V  V /\__ \
 /_/    \_\__,_|\__\___/  |____/ \__,_|_|_|\__,_|     \/  \/   |_|_| |_|\__,_|\___/ \_/\_/ |___/
""")
def Check():
    Change(1)                                                           #检察环境
    logger.log(1)
    OS_StringName = "系统: "
    if platform == "linux" or platform == "linux2":
        OS_StringName += "Linux ("+platform+")"
        DOWNLOAD_PATH = os.path.dirname(os.path.realpath(__file__)) + "/"
        logger.log(2)
        OK=0
    elif platform == "darwin":
        OS_StringName += "macOS X ("+platform+")"
        DOWNLOAD_PATH = os.path.dirname(os.path.realpath(__file__)) + "/"
        logger.log(3)
        OK=0
    elif platform == "win32":
        OS_StringName += "Windows ("+platform+")"
        DOWNLOAD_PATH = os.path.dirname(os.path.realpath(__file__)) + "\\"
        print ("系统信息",OS_StringName)
        print ("文件将会保存在" + DOWNLOAD_PATH + "\n")
        print ("服务器赞助商：Catixs")
    if os.path.exists(MountDir):
  # 如果存在，递归删除再创建
        shutil.rmtree(MountDir)
        os.makedirs(MountDir)
    else:
  # 如果不存在，创建再挂载
        os.makedirs(MountDir)
    if os.path.exists(TempISO):
  # 如果存在，递归删除再创建
        shutil.rmtree(TempISO)
        os.makedirs(TempISO)
    else:
  # 如果不存在，创建再挂载
        os.makedirs(TempISO)
    logger.log(4)
    return
def CheckVerison():
    global updateId
    global NewVer
    global foundBuild
    logger.log(5)
    CheckUrl = f'{ApiUrl}/fetchupd.php?arch=amd64&ring=retail&build={BuildID}'
    response = requests.get(CheckUrl)
    if response.status_code == 200:
        data = json.loads(response.content)
        updateId = data['response']['updateId']
        foundBuild = data['response']["foundBuild"]
    else:
        Change(0)
        logger.log(6)
        OK=0
    if search_updateId(updateId):
        logger.log(7)
        OK=0
    else:
        NewVer=1
        logger.log(8)    
    logger.log(9)
def Get():
    Change(2)
    logger.log(10)
    GetUrl = f'{UUPUrl}/get.php?id={updateId}&pack={LANG}&edition=core;professional&autodl=2'
    urllib.request.urlretrieve(GetUrl, "uupdown.zip")
    temp_dir = "Temp"
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)
    zip_ref = zipfile.ZipFile("uupdown.zip", "r")
    zip_ref.extractall(temp_dir)
    zip_ref.close()
    folder = DOWNLOAD_PATH
    filename = 'Temp\\ConvertConfig.ini'
    filepath = os.path.join(folder, filename)
    urllib.request.urlretrieve('https://file.autobuild.win/config.ini', filepath)
    filename = 'Temp\\files\\depends_win.ps1'
    filepath = os.path.join(folder, filename)
    urllib.request.urlretrieve('https://file.autobuild.win/depends_win.ps1', filepath)
    cmd = Temp + "\\uup_download_windows.cmd"
    os.system(cmd)
    logger.log(11)
    return
def Build():
    Change(3)
    logger.log(12)
    files = os.listdir(Temp)
    for file in files:
        if os.path.splitext(file)[1] == ".ISO":
            logger.log(13)
            break
    DOWNLOAD_PATH = os.getcwd()
    ISO =  DOWNLOAD_PATH + '\\Temp\\' + file
    logger.log(14)
    patoolib.extract_archive(ISO, outdir=TempISO)
    Wim = DOWNLOAD_PATH + "\\Temp\\ISO\\sources\\install.wim"
    logger.log(15)
    subprocess.run(["dism", "/Mount-Wim", "/WimFile:" + Wim , "/index:2", "/MountDir:" + MountDir ])
    os.system(DOWNLOAD_PATH + "\\Build.cmd")
    logger.log(16)
    return
def Mount():
    Change(4)
    logger.log(17)
    if(UseESD == 1):
        cmd ='wimlib-imagex.exe capture ' + MountDir + ' ' + ESD + ' ' + ImageName + '--check --solid'  
    else:
        cmd = 'dism /Capture-Image /ImageFile:' + Temp +' /CaptureDir:' + MountDir
    os.system(cmd)
    logger.log(18)
    return
def fina():
    logger.log(23)
    logger.log(24)
    folder = DOWNLOAD_PATH + 'Temp'
    if os.path.exists(MountDir):
        cmd = 'dism /Unmount-Image /MountDir:' + MountDir + ' /Discard'
        os.system(cmd)
        logger.log(25)
    else:
        logger.log(26) 
    if os.path.exists(Temp):
        shutil.rmtree(Temp)
        logger.log(27)
    else:
        logger.log(28)
    if os.path.exists(TempISO):
        shutil.rmtree(TempISO)
        logger.log(29)
    else:
        logger.log(30)
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO verison (updateId) VALUES (?)", (updateId))
    conn.commit()
    conn.close()
    logger.log(31)
    print("部署已经完成，将自动退出")
    print("updateId:" + updateId)
    return
def Upload():
    Change(5)
    logger.log("19")
    if UseRclone:
        for remote in remotes:
            subprocess.run(["rclone", "copy", ESD, f"{remote}:backup"])
    logger.log("20")
def NewPost():
    logger.log(21)
    if UseNewPost != 1:
        return
    else:
        Post = f'''
    # 欢迎使用自动构建~
    镜像名称：{ImageName}
    版本号：{foundBuild}
    构建ID:{rid}
    '''
        # Connect to WordPress
        wp = Client(WPURL, WPUser, WPPassword)
        # Create a new post
        post = WordPressPost()
        post.title = PostTitle
        post.content = Post
        post.post_status = 'publish'
        post.id = wp.call(NewPost(post))
    logger.log(22)
if __name__ == '__main__':
    init()
    while True:
        rid = random_string(8)
        NewLog()
        time.sleep(int(TIME))
        logger = Logger(['console', 'smtp', 'txt'], [{},smtp_log_config, txt_log_config])
        if OK==1:
            Welcome()
        if OK==1:
            Check()
        if OK==1:
            CheckVerison()
        if NewVer == 1:
            if OK==1:
                Get()
            if OK==1:
                Build()   
            if OK==1:     
                Mount()
            if OK==1:
                fina()
            if OK==1:
                Upload()
            if OK==1:
                NewPost()
                END(1)
        END(2)
