import time
import datetime
import pandas as pd
import json
import os
from colorama import init, Fore, Back, Style
import random
#初始化颜色显示符
B=Fore.BLUE
R=Fore.RED
Y=Fore.YELLOW
G=Fore.GREEN
W=Fore.WHITE
init(autoreset=True)
#配置文件加载获取词库文件，放进变量ciku，获得学习单词数放进ci_number
with open("程序文件\英语学习配置文件.json",'r',encoding='utf-8') as f1:
    peizhi=json.load(f1)
if peizhi['急速模式']:
    with open("程序文件\急速模式1800.json",'r',encoding='utf-8') as f2:
        ciku=json.load(f2)
        leixing='急速模式'
else:
    with open("程序文件\仔细模式5600.json",'r',encoding='utf-8') as f3:
        ciku=json.load(f3)
        leixing='仔细模式'
ci_number=peizhi['每天背诵单词']
if os.path.exists("程序文件\已学过的单词.json"):
    with open("程序文件\已学过的单词.json",'r',encoding='utf-8') as f4:
        ci_fu_zong=json.load(f4)
else:
    with open("程序文件\已学过的单词.json",'w',encoding='utf-8') as f5:
        fuxiku=[{"单词数量":0,"阶段序号":1,"已学单词":[],"保存时间":"","有效时期":0,"词库类型":leixing}]
        json.dump(fuxiku,f5,ensure_ascii=False,indent=4)
#判断复习时间和返回复习列表，格式为[([单词],阶段)]
def fuxi_plan():
    fuxi_list=[]
    today=datetime.date.today()
    for ci_fu in ci_fu_zong:
        if not ci_fu['已学单词'] or not ci_fu['保存时间']:
            continue
        ci_fu_time=datetime.datetime.strptime(ci_fu['保存时间'],"%Y-%m-%d").date()
        if today-ci_fu_time>=datetime.timedelta(days=ci_fu['有效时期']):
            yuanzu=(ci_fu['已学单词'],ci_fu['阶段序号'])
            fuxi_list.append(yuanzu)
    return fuxi_list
#有效时间修改
def youxiao_time(jieduan):
    if jieduan==1:
        return 1
    elif jieduan==2:
        return 3
    elif jieduan==3:
        return 3
    elif jieduan==4:
        return 7
    elif jieduan==5:
        return 15
    elif jieduan==6:
        return 30
    else:
        return 1
#判断阶段的复习模式
def jieduan_panduan(yuanzu):
    if yuanzu[1]<=3:
        return "字母组合模式"
    if 3<yuanzu[1]<=6:
        return "认读选词模式"
    if yuanzu[1]>6:
        return "删除"
#格式化输出单词
def shuchu(danci):
    return f'''\
单词：{danci['单词']}
音标：{danci['音标']}
释义：{danci['释义']}'''
#拼写模式，要求输入单词列表
def mods_zimuzuhe(danci_list):
    print('''\
===========
单词拼写模式
===========
'''+'说明:'+Y+'''\
该只模式给出单词释义，你需要
拼写出单词是否正确直到正确率满分为止！''')
    cishu=1
    xunhuan=True
    zong=len(danci_list)
    while xunhuan:
        print('这是第'+B+str(cishu)+W+'次复习')
        wrong_list=[]
        for danci in random.sample(danci_list,zong):
            print('单词释义：'+B+danci['释义'])
            shuru=input('单词:')
            if shuru==danci['单词']:
                print(G+'正确!')
                print(G+shuchu(danci))
            else:
                wrong_list.append(danci)
                print(R+'错误!')
                print(R+shuchu(danci))
        if len(wrong_list):
            cishu+=1
            current_lv=round((zong-len(wrong_list))/zong,4)*100
            print('''\
=======
总结清单
=======''')
            print('正确率:'+G+str(current_lv)+W+'%')
            for wrong_ci in wrong_list:
                print('错误清单:')
                print('——————————————————————————')
                print(shuchu(wrong_ci))
                print('——————————————————————————')
        else:
            print(Y+'恭喜全部正确,这一阶段共用了'+G+str(cishu)+Y+'次')
            xunhuan=False
#认读模式，要求输入单词列表
def mods_zumurengdu(danci_list):
    hunxiao=[]
    for danci in ciku:
        hunxiao.append(danci['释义'])
    print('''\
===========
单词认读模式
===========
'''+W+'说明:'+Y+'''\
该只模式给出单词，你需要
从所给A,B,C,D选出单词是否正确直到正确率满分为止！''')
    cishu=1
    xunhuan=True
    zong=len(danci_list)
    while xunhuan:
        print('这是第'+B+str(cishu)+W+'次复习')
        wrong_list=[]
        for danci in random.sample(danci_list,len(danci_list)):
            hunxiao_copy = [x for x in hunxiao if x != danci['释义']]
            lishi_list=random.sample(hunxiao_copy,3)
            lishi_list.append(danci['释义'])
            pai_list=random.sample(lishi_list,4)
            xuanxiang={'A':pai_list[0],'B':pai_list[1],'C':pai_list[2],'D':pai_list[3]}
            print('单词:'+B+danci['单词'])
            for xuan,shiyi_xuan in xuanxiang.items():
                print(xuan+'.'+shiyi_xuan)
            kongzhi=True
            while kongzhi:
                shuru=input('单词释义:')
                if shuru=='A' or shuru=='B' or shuru =='C' or shuru=='D':
                    kongzhi=False
                    if xuanxiang[shuru]==danci['释义']:
                        print(G+'正确!')
                        print(G+shuchu(danci))
                    else:
                        wrong_list.append(danci)
                        print(R+'错误!')
                        print(R+shuchu(danci))
                else:
                    print(R+'【输入错误，请输入A,B,C,D】')
        if len(wrong_list):
            cishu+=1
            current_lv=round((zong-len(wrong_list))/zong,4)*100
            print('''\
        =======
        总结清单
        =======''')
            print('正确率:'+G+str(current_lv)+W+'%')
            for wrong_ci in wrong_list:
                print('错误清单:')
                print('——————————————————————————')
                print(shuchu(wrong_ci))
                print('——————————————————————————')
        else:
            print(Y+'恭喜全部正确,这一阶段共用了'+G+str(cishu)+Y+'次')
            xunhuan=False

#主程序
today_time=datetime.date.today()
log=''
Control=True
while Control:
    print('''\
======================
六级英语学习终端显示程序
======================
1.学习
2.搜索单词(仅限6级词库中有的)
3.查看所有单词
4.学习翻译作文的常用词(共21个)
5.查看当前学习配置
6.退出程序''')
    contorl=input(Fore.YELLOW+'【你的输入】'+Fore.WHITE+':')
    if contorl=='1':
        new_leixing=ci_fu_zong[len(ci_fu_zong)-1]['词库类型']
        try:
            new_index=ci_fu_zong[len(ci_fu_zong)-1]['已学单词'][len(ci_fu_zong[len(ci_fu_zong)-1]['已学单词'])-1]['序号']
        except IndexError:
            new_index=0
            print(Y+'这是一个新的开始')
        print('''\
==============
六级英语单词学习
==============''')
        if len(fuxi_plan())==0:
            fuxi_open=False
        else:
            fuxi_open=True
        if fuxi_open:
            print(Y+'''————复习阶段————''')
            for F in fuxi_plan():
                for C,INDEX in zip(ci_fu_zong,range(len(ci_fu_zong))):
                    if C['已学单词']==F[0]:
                        index=INDEX
                        break
                mods_gengju=jieduan_panduan(F)
                if mods_gengju=="字母组合模式":
                    mods_zimuzuhe(F[0])
                    ci_fu_zong[index]['保存时间']=today_time.strftime("%Y-%m-%d")
                    ci_fu_zong[index]['阶段序号']+=1
                    ci_fu_zong[index]['有效时期']=youxiao_time(ci_fu_zong[index]['阶段序号'])
                elif mods_gengju=="认读选词模式":
                    mods_zumurengdu(F[0])
                    ci_fu_zong[index]['保存时间']=today_time.strftime("%Y-%m-%d")
                    ci_fu_zong[index]['阶段序号']+=1
                    ci_fu_zong[index]['有效时期']=youxiao_time(ci_fu_zong[index]['阶段序号'])
                elif mods_gengju=='删除':
                    del ci_fu_zong[index]
        else:
            print(B+'【无复习任务】')
        if log=='学习任务已完成':
            wen=True
            while wen:
                xunwen=input(G+'【今天的学习任务完成了是否要继续学习】'+W+'（输入是或否）:')
                if xunwen=='是':
                    wen=False
                    if new_leixing==leixing:
                        start_lip=new_index
                        end_lip=new_index+peizhi['每天背诵单词']
                        mods_zumurengdu(ciku[start_lip:end_lip])
                        mods_zimuzuhe(ciku[start_lip:end_lip])
                        ci_fu_zong.append({"单词数量":peizhi['每天背诵单词'],"阶段序号":1,"已学单词":ciku[start_lip:end_lip],"保存时间":today_time.strftime("%Y-%m-%d"),"有效时期":youxiao_time(1),"词库类型":leixing})
                        with open("程序文件\已学过的单词.json",'w',encoding='utf-8') as f:
                            json.dump(ci_fu_zong,f,ensure_ascii=False,indent=4)
                        print(G+'今天的学习任务超量完成了')
                        log='学习任务已完成'
                elif xunwen=='否':
                    wen=False
                else:
                    print(R+'输入出错请看提示输入')
        else:
            print(Y+"————新学单词阶段————")
            if new_leixing==leixing:
                start_lip=new_index
                end_lip=new_index+peizhi['每天背诵单词']
                mods_zumurengdu(ciku[start_lip:end_lip])
                mods_zimuzuhe(ciku[start_lip:end_lip])
                ci_fu_zong.append({"单词数量":peizhi['每天背诵单词'],"阶段序号":1,"已学单词":ciku[start_lip:end_lip],"保存时间":today_time.strftime("%Y-%m-%d"),"有效时期":youxiao_time(1),"词库类型":leixing})
                with open("程序文件\已学过的单词.json",'w',encoding='utf-8') as f:
                    json.dump(ci_fu_zong,f,ensure_ascii=False,indent=4)
                print(G+'今天的学习任务完成了')
                log='学习任务已完成'
            else:
                new_index=0
                for cha in reversed(ci_fu_zong):
                    if cha['词库类型']==leixing:
                        new_index=cha['已学单词'][len(cha['已学单词'])-1]['序号']
                        break
                start_lip=new_index
                end_lip=new_index+peizhi['每天背诵单词']
                mods_zumurengdu(ciku[start_lip:end_lip])
                mods_zimuzuhe(ciku[start_lip:end_lip])
                ci_fu_zong.append({"单词数量":peizhi['每天背诵单词'],"阶段序号":1,"已学单词":ciku[start_lip:end_lip],"保存时间":today_time.strftime("%Y-%m-%d"),"有效时期":youxiao_time(1),"词库类型":leixing})
                with open("程序文件\已学过的单词.json",'w',encoding='utf-8') as f:
                    json.dump(ci_fu_zong,f,ensure_ascii=False,indent=4)
                print(G+'今天的学习任务完成了')
                log='学习任务已完成'
    elif contorl=='2':
        with open("程序文件\仔细模式5600.json",'r',encoding='utf-8') as f0:
            chaxun_ku=json.load(f0)
        print('''\
========
单词查询
=======
(输入@退出)''')
        while True:
            danci=input('输入要查询的单词:')
            if danci=='@':
                break
            else:
                for cha in chaxun_ku:
                    dan=0
                    if cha['单词']==danci:
                        dan=cha
                        break
                if dan:
                    print(G+shuchu(dan))
                else:
                    print(R+'<没搜索到该单词>')
    elif contorl=='3':
        for danci in ciku:
            print(B+shuchu(danci))
    elif contorl=='4':
        print('说明:\n'+G+'由于翻译和作文的单词较少只有21个，所以不再遵循遗忘曲线学习\n这里只提供一个检测平台给你用!')
        with open('程序文件/翻译作文扩充.json','r',encoding='utf-8') as f:
            list1=json.load(f)
        mods_zumurengdu(list1)
        mods_zimuzuhe(list1)
        print(G+'<恭喜你学完一遍了>')
    elif contorl=='5':
        print(f'''
————————
当前配置
————————
模式：{leixing}
每日学习单词数为：{peizhi['每天背诵单词']}''')
    elif contorl=='6':
        with open("程序文件\已学过的单词.json",'w',encoding='utf-8') as f:
            json.dump(ci_fu_zong,f,ensure_ascii=False,indent=4)
        Control=False