import sys
import os
import requests
from random import randrange
from urllib.parse import quote
import tkinter as tk
from tkinter import messagebox

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def get_credentials():
    dialog = tk.Toplevel()
    dialog.title("上网认证客户端")
    dialog.iconbitmap(resource_path("favicon.ico"))
    
    tk.Label(dialog, text="统一认证账号:").grid(row=0, column=0, padx=10, pady=10)
    tk.Label(dialog, text="统一认证密码:").grid(row=1, column=0, padx=10, pady=10)
    username_var = tk.StringVar()
    password_var = tk.StringVar()
    username_entry = tk.Entry(dialog, textvariable=username_var)
    password_entry = tk.Entry(dialog, textvariable=password_var, show="*")
    username_entry.grid(row=0, column=1, padx=10, pady=10)
    password_entry.grid(row=1, column=1, padx=10, pady=10)
    
    def submit():
        username = username_var.get()
        password = password_var.get()
        if username and password:
            dialog.destroy()
        else:
            messagebox.showerror("错误", "账号或密码不能为空！")
    
    def on_close():
        messagebox.showinfo("退出", "程序已退出，因为未输入账号密码。")
        dialog.destroy()
        exit(1)
    
    dialog.protocol("WM_DELETE_WINDOW", on_close)
    
    submit_button = tk.Button(dialog, text="提交", command=submit)
    submit_button.grid(row=2, column=0, columnspan=2, pady=10)
    
    dialog.wait_window(dialog)

    return username_var.get(), password_var.get()

root = tk.Tk()
root.withdraw()
root.iconbitmap(resource_path("favicon.ico"))

username, password = get_credentials()

if not username or not password:
    messagebox.showerror("错误", "账号或密码为空，程序退出。")
    exit(1)

data = {
    'callback': 'dr1004',
    'DDDDD': username,
    'upass': password,
    '0MKKey': '123456',
    'R1': '0',
    'R3': '0',
    'R6': '0',
    'para': '00',
    'v6ip': '',
    'v': str(randrange(1000, 9999))
}
header = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Host': '192.168.9.18',
    'Referer': 'http://192.168.9.18/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
}

url = 'http://192.168.9.18/drcom/login?callback=dr1004&DDDDD=' + quote(data['DDDDD']) + '&upass=' + quote(data['upass']) + '&0MKKey=&R1=0&R3=0&R6=0&para=00&v6ip=&v=6901'
response = requests.post(url, data=data, headers=header).status_code

if response == 200:
    messagebox.showinfo("成功", "已连接（Code:200）")
else:
    messagebox.showerror("错误", f"连接失败（Code:{response}）")