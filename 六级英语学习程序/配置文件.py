import time
import datetime
import pandas as pd
import json
import os
from colorama import init, Fore, Back, Style

try:
    with open(r'程序文件\英语学习配置文件.json','r',encoding='utf-8') as f:
        peizhi=json.load(f)
except FileNotFoundError:
    peizhi={'急速模式':True,'每天背诵单词':0}
    with open(r'程序文件\英语学习配置文件.json','w',encoding='utf-8') as f:
        json.dump(peizhi,f,ensure_ascii=False,indent=4)

init(autoreset=True)

r=Fore.RED
b=Fore.BLUE
g=Fore.GREEN
w=Fore.WHITE

def mod():
    if peizhi['急速模式']:
        string='急速模式'
    else:
        string='仔细模式'
    return string

while True:
    print(b+f'''\
————————
当前配置
————————
模式：{mod()}
每日学习单词数为：{peizhi['每天背诵单词']}''')
    print(r+'说明：'+'\n'+g+'急速模式'+w+'是让你在'+g+'两个月内'+w+'背完6级高频词汇，不覆盖全部六级')
    print(g+'仔细模式'+w+'是让你背完整个六级单词，时间在'+g+'10个月'+w+'，覆盖整个六级')
    a=input('''\
======================
六级英语配置终端显示程序
======================
1.修改模式
2.修改每天背诵的单词
3.导出词汇为xlsx表格
4.退出\n'''+g+'【你的操作】'+w+':')
    if a=='1':
        print(g+'说明：'+w+'\n'+'输入@表示默认')
        while True:
            fix1=input('选择学习模式'+g+'【填：仔细模式/急速模式/@】'+w+':')
            if fix1=='急速模式':
                peizhi['急速模式']=True
                print('当前配置为:'+g+f'{mod()}')
                break
            elif fix1=='仔细模式':
                peizhi['急速模式']=False
                print('当前配置为:'+g+f'{mod()}')
                break
            elif fix1=='@':
                print('当前配置为:'+g+f'{mod()}')
                break
            else:
                print(r+'输入有误，请仔细查看输入提示')
    elif a=='2':
        print(g+'说明：'+w+'\n'+'输入@表示默认')
        while True:
            fix2=input('每天背诵的单词'+g+'【填：整数/@】'+w+':')
            if fix2=='@':
                print('当前配置为:每天背诵单词数'+g+f"{peizhi['每天背诵单词']}"+w+'个')
                break
            else:
                try:
                    numbers=int(fix2)
                    peizhi['每天背诵单词']=numbers
                    print('当前配置为:每天背诵单词数'+g+f"{peizhi['每天背诵单词']}"+w+'个')
                    break
                except ValueError:
                    print(r+'输入有误，请仔细查看输入提示')
                    continue
    elif a=='3':
        while True:
            if os.path.exists('六级英语词汇5600.xlsx'):
                print('【目录中存在'+g+'六级英语词汇5600.xlsx'+w+'】')
            if os.path.exists('六级英语词汇1800.xlsx'):
                print('【目录中存在'+g+'六级英语词汇1800.xlsx'+w+'】')
            if os.path.exists('六级英语作文翻译21词.xlsx'):
                print('【目录中存在'+g+'六级英语作文翻译21词.xlsx'+w+'】')
            print('''\
——————————————
一共有3个词汇库
——————————————
1.仔细模式5600
2.急速模式1800
3.翻译作文扩充21词
4.全部导出
5.返回''')
            cong=input(g+'【你的输入】'+w+':')
            if cong=='1':
                if os.path.isfile('六级英语词汇5600.xlsx'):
                    print(r+'文件已存在，不需要再次导出')
                else:
                    with open(r'程序文件\仔细模式5600.json','r',encoding='utf-8') as f:
                        ci=json.load(f)
                        df=pd.DataFrame(ci)
                        df.to_excel('六级英语词汇5600.xlsx',index=False,sheet_name='仔细模式5600')
                        print(g+'【导出成功，请在同一目录下查看】')
            elif cong=='2':
                if os.path.isfile('六级英语词汇1800.xlsx'):
                    print(r+'【文件已存在，不需要再次导出】')
                else:    
                    with open(r'程序文件\急速模式1800.json','r',encoding='utf-8') as f:
                        ci=json.load(f)
                        df=pd.DataFrame(ci)
                        df.to_excel('六级英语词汇1800.xlsx',index=False,sheet_name='急速模式1800')
                        print(g+'【导出成功，请在同一目录下查看】')
            elif cong=='3':
                if os.path.isfile('六级英语作文翻译21词.xlsx'):
                    print(r+'文件已存在，不需要再次导出')
                else:
                    with open(r'程序文件\翻译作文扩充.json','r',encoding='utf-8') as f:
                        ci=json.load(f)
                        df=pd.DataFrame(ci)
                        df.to_excel('六级英语作文翻译21词.xlsx',index=False,sheet_name='翻译作文扩充')
                        print(g+'【导出成功，请在同一目录下查看】')
            elif cong=='4':
                if os.path.exists('六级英语词汇5600.xlsx') and os.path.exists('六级英语词汇1800.xlsx') and os.path.exists('六级英语作文翻译21词.xlsx'):
                    print(g+'【文件已全部导出，请在当前目录下查看】')
                else:
                    with open(r'程序文件\急速模式1800.json','r',encoding='utf-8') as f:
                        ci=json.load(f)
                        df=pd.DataFrame(ci)
                        df.to_excel('六级英语词汇1800.xlsx',index=False,sheet_name='急速模式1800')
                    with open(r'程序文件\仔细模式5600.json','r',encoding='utf-8') as f:
                        ci=json.load(f)
                        df=pd.DataFrame(ci)
                        df.to_excel('六级英语词汇5600.xlsx',index=False,sheet_name='仔细模式5600')
                    with open(r'程序文件\翻译作文扩充.json','r',encoding='utf-8') as f:
                        ci=json.load(f)
                        df=pd.DataFrame(ci)
                        df.to_excel('六级英语作文翻译21词.xlsx',index=False,sheet_name='翻译作文扩充')
                    print(g+'【全部导出成功】')
            elif cong=='5':
                break
    elif a=='4':
        with open(r'程序文件\英语学习配置文件.json','w',encoding='utf-8') as f:
            json.dump(peizhi,f,ensure_ascii=False,indent=4)
        break               