# -*- coding: utf-8 -*-
import os
DOWNLOAD_PATH = os.getcwd()
Config_ini = DOWNLOAD_PATH + '\\Config\\Config.ini'
Lang_ini = DOWNLOAD_PATH + '\\Config\\Lang.ini'
import importlib.util
def module_exists(module_name):
    spec = importlib.util.find_spec(module_name)
    return spec is not None
def CheckModule(ModuleName):
    # 检测模块是否存在
    if module_exists(ModuleName):
        pass
    else:
        os.system(f"pip install {ModuleName}")
CheckModule("requests")
CheckModule("urllib3")
CheckModule("configparser")
CheckModule("patool")
CheckModule("zip_files")
CheckModule("python-wordpress-xmlrpc")
CheckModule("telegram")
# 导入模块
from colorama import init,Fore
init(autoreset=True)
import telegram
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
import random
import string
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
# 加载配置文件
config = configparser.ConfigParser()
config.read(Config_ini, encoding='utf-8')
# 读取配置文件中的变量
LANG = config['Set']['Lang']
CN = config['Set']['CN']
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
UseTg = config['Tg']['Use']
TgToken = config['Tg']['Token']
Chatid = config['Tg']['Chatid']
smtp_log_config = {'server': Server,'user': User,'password': PassWord,'sender': Sender,'receiver': Receiver,'subject': Subject}
Verison =  Fore.RED + '1.2.1'
updateId = ''
V = 'Releases'
TempISO = DOWNLOAD_PATH + '\\Temp\\' + 'ISO'
MountDir = DOWNLOAD_PATH +  '\\Mount'
Temp = DOWNLOAD_PATH + '\\Temp'
cmd = Temp + '\\uup_download_windows.cmd'
ESD = Temp + '\\' + ImageName + '.esd'
WIM = Temp + '\\' + ImageName + '.wim'
Webdb = DOWNLOAD_PATH + '\\Db\\web.db'
DataDb = DOWNLOAD_PATH + '\\Db\\data.db'
OK=1
class db:
    def ERROR():
            # 连接到数据库
            conn = sqlite3.connect(Webdb)
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
            db.Change
            # 连接到数据库
            conn = sqlite3.connect(Webdb)
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
            conn = sqlite3.connect(Webdb)
            # 创建游标
            cursor = conn.cursor()
            db.Change
            # 插入值
            cursor.execute("INSERT INTO log(starttime,endtime,rid,status) VALUES (?,?,?,?)", (localtime, None, rid, 3))
            # 提交事务
            conn.commit()
            # 关闭连接
            conn.close()
    def Change(id):
    #修改状态
        conn = sqlite3.connect(Webdb)
        cursor = conn.cursor()
        cursor.execute("UPDATE status SET status = ?", (id,))
        conn.commit()
        conn.close()
        return
class ctrl:
    def random_string(length):
        return ''.join(random.choices(string.ascii_uppercase+string.ascii_lowercase+string.digits+string.ascii_uppercase+string.ascii_lowercase, k=length))
    def gettime():
        # 获取当前时间
        global localtime
        localtime = time.localtime()
        localtime = time.strftime("%Y-%m-%d %H:%M:%S", localtime)
def init():
    # 初始化程序
    if not os.path.exists(DataDb):
        conn = sqlite3.connect(DataDb)
        cursor = conn.cursor()
        try:
            cursor.execute("CREATE TABLE IF NOT EXISTS verison (updateId INTEGER)")
        except sqlite3.Operationaldb.ERROR:
            pass
        conn.commit()
        conn.close()
    if not os.path.exists(Webdb):
        conn = sqlite3.connect(Webdb)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS status (status int)''')
        cursor.execute("INSERT INTO status (status) VALUES (2)")
        cursor.execute("CREATE TABLE IF NOT EXISTS log (starttime timestamp, endtime timestamp, rid integer, status integer)")
        conn.commit()
        conn.close()



class Logger:
    # 日志类
    def __init__(self, log_types, log_configs):
        self.log_types = log_types
        self.log_configs = log_configs
    def log_to_smtp(self, message, config):
        db.Change
        msg = f"信息报告: {localtime} :{Subject}\n\n{message}"
        server = smtplib.SMTP()
        server.sendmail(Sender,Receiver, msg)
        server.quit()
    def log_to_tg(self, message):
        if UseTg != 1:
            return
        if CN == 1 :
            return
        db.Change
        bot = telegram.Bot(token=TgToken)
        bot.send_message(chat_id=Chatid, text=f'最新状态{localtime}:{message}')
    def log_to_console(self, message):
        db.Change
        print(localtime + " ： " + message)
    def log(self, id):
        for log_type, log_config in zip(self.log_types, self.log_configs):
                # 加载配置文件
            config = configparser.ConfigParser()
            config.read(Lang_ini, encoding='utf-8')

            message = config[LANG][str(id)]
            if log_type == 'smtp':
                if UseMail != 1:
                    return
                self.log_to_smtp(message, log_config)
            elif log_type == 'tg':
                self.log_to_tg(message)
            elif log_type == 'console':
                self.log_to_console(message)
def search_updateId(updateId):
        conn = sqlite3.connect(DataDb)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM verison WHERE updateId=?", (updateId,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return True
        else:
            return False
def Welcome():
    #欢迎
    print("欢迎使用Auto Build Windows")
    print("自动构建第三方Windows辅助工具")
    print("本项目不是Microsoft旗下项目")
    print("官网:https://autobuild.win")
    print("程序版本: " + Verison)
    print("此程序仅支持Windows")
    resp = urllib.request.urlopen(ApiUrl)
    if resp.status == 200:
        NewVerison = resp.read()
        data = json.loads(NewVerison)
        NewVerison = data['response']['apiVersion']
        print("UUP API最新版本：" + NewVerison)
        NewVerison = data['jsonApiVersion']
        print("UUP API最新版本：" + NewVerison)
    else:
        db.Change(0)
        print("连接到API服务器错误!")
def Check():
    #检查环境
    db.Change(1)
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
    # 获取版本
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
        print(f'您的短版本为{foundBuild}')
    else:
        db.Change(0)
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
    # 获取镜像
    db.Change(2)
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
    urllib.request.urlretrieve('https://cdn.jsdelivr.net/gh/eteam666/files/config.ini', filepath)
    if CN ==1:       
        filename = 'Temp\\files\\depends_win.ps1'
        filepath = os.path.join(folder, filename)
        urllib.request.urlretrieve('https://cdn.jsdelivr.net/gh/eteam666/files/depends_win.ps1', filepath)
    cmd = Temp + "\\uup_download_windows.cmd"
    os.system(cmd)
    logger.log(11)
    return
def Build():
    # 开始构建
    db.Change(3)
    logger.log(12)
    files = os.listdir(Temp)
    for file in files:
        if os.path.splitext(file)[1] == ".ISO":
            logger.log(13)
            break
    ISO =  DOWNLOAD_PATH + '\\Temp\\' + file
    logger.log(14)
    patoolib.extract_archive(ISO, outdir=TempISO)
    Wim = DOWNLOAD_PATH + "\\Temp\\ISO\\sources\\install.wim"
    logger.log(15)
    subprocess.run(["dism", "/Mount-Wim", "/WimFile:" + Wim , "/index:2", "/MountDir:" + MountDir ])
    if not os.path.exists(DOWNLOAD_PATH + '\\Pack.ini'):
        print("正在执行CMD......")
    else:
        config.read('Pack.ini', encoding='utf-8')
        PackName = ["Config"]["Name"]
        To = ["Config"]["To"]
        if To == "MountDir":
            To=MountDir
        if To == "Root":
            To=DOWNLOAD_PATH
        if To == "Temp":
            To=Temp
        File = To + '\\' + PackName
        patoolib.extract_archive(File, outdir=To)
        Run = ["Config"]["Run"]
        CMD = f'cd {To}\\ && {Run}'
        os.system(CMD)
        logger.log(16)
        return
    os.system(DOWNLOAD_PATH + "\\File\\Build.cmd")
    logger.log(16)
    return
def Mount():
    # 挂载镜像
    db.Change(4)
    logger.log(17)
    if(UseESD == 1):
        cmd = 'wimlib-imagex.exe capture ' + MountDir + ' ' + ESD + ' ' + ImageName + '--check --solid'  
    else:
        cmd = 'dism /Capture-Image /ImageFile:' + WIM +' /CaptureDir:' + MountDir
    os.system(cmd)
    logger.log(18)
    return
def fina():
    # 收尾工作
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
    conn = sqlite3.connect(DataDb)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO verison (updateId) VALUES (?)", (updateId))
    conn.commit()
    conn.close()
    logger.log(31)
    print("部署已经完成，将自动退出")
    print("updateId:" + updateId)
    return
def Upload():
    # 上传
    db.Change(5)
    logger.log("19")
    if UseRclone:
        for remote in remotes:
            subprocess.run(["rclone", "copy", ESD, f"{remote}:backup"])
    logger.log("20")
def NewPost():
    # 新建文章
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
        rid = ctrl.random_string()(8)
        db.NewLog()
        time.sleep(int(TIME))
        logger = Logger(['console', 'smtp', 'tg'], [{},smtp_log_config])
        OK=1
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
                db.END(1)
        if OK != 1:
            db.END(2)
