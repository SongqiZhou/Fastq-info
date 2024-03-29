import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import *
import tkinter.messagebox

#判断输入序列是否正常
def isnormal(seq):
    num_A = seq.count("A")
    num_T = seq.count("T")
    num_C = seq.count("C")
    num_G = seq.count("G")
    return num_A + num_T + num_C + num_G == len(seq)

#每条序列的长度
def Every_len(seq):
    L = []
    for i in range(0,len(seq)):
        if isnormal(seq[i]):
            L.append(len(seq[i]))
        else:
            tkinter.messagebox.showinfo('提示','序列含ATCG之外字符')
    return L

#求一条序列GC含量
def CG_content(seq):
    num_C = seq.count("C")
    num_G = seq.count("G")
    return (num_C + num_G) / len(seq)

#求若干条序列中每条序列GC含量
def CG_contents(seq):
    values = []
    for i in range(0,len(seq)):
        values.append(CG_content(seq[i]))
    return values

#求一条序列平均质量
def value(seq):
    values = []
    for i in range(0,len(seq)):
        values.append(ord(seq[i]))
    max_value = max(values)
    min_value = min(values)
    if (max_value <= 73) and (min_value >= 33):    ##sanger测序
        return ((sum(values) / len(values)) - 33)
    elif (max_value <= 104) and (min_value >= 59):   ##illumina测序
        return ((sum(values) / len(values)) - 64)
    else:
        print("ERROR")
    
#求文件中每条序列平均质量
def Average_value(v):
    values = []
    for i in range(0,len(v)):
        values.append(value(v[i]))
    return values
    
#获取文件路径
def getLocalFile():
    root=tk.Tk()
    root.withdraw()
    filePath=filedialog.askopenfilename()
    #print('文件路径：',filePath)
    return filePath

#保存文件路径
def saveLocalFile():
    root=tk.Tk()
    root.withdraw()
    filePath=filedialog.asksaveasfilename()
    #print('文件路径：',filePath)
    return filePath

#读取文件
def read_fastq(filePath): #用def定义函数read_fasta()，并向函数传递参数用变量input接收
    with open(filePath,'r') as f: # 打开文件
        seq = [] # 定义一个列表存储序列
        values = [] # 定义一个列表存储序列质量
        i = 0
        for line in f:
            line = line.strip() # 去除末尾换行符
            if (i%4 == 1):
                seq.append(line)
            if (i%4 == 3):
                values.append(line)
            i += 1
        #print(seq)
        #print(values)
    return seq, values

def Download():
    filePath = saveLocalFile()
    out = open(filePath,"w",encoding='utf8')
    out.write("每条序列的长度：\n%s \n 平均质量：\n %s \n GC含量：\n %s"%(L,Values,CG))
    out.close()
    tkinter.messagebox.showinfo('提示','下载完成')
    #print("下载完成")
    
#序列互补功能封装
def Function(seq,v):
    global L,CG,Values
    L = Every_len(seq)
    CG = CG_contents(seq)
    Values = Average_value(v)
    root1 = tk.Tk()
    root1.title("RESULT")
    
    text = tk.Text(root1,width=60,height=40)
    text.pack()
    text.insert(tk.INSERT,"原始序列：\n")
    text.insert(tk.INSERT,'%s'%seq)
    text.insert(tk.INSERT,"\n\n每条序列的长度：\n")
    text.insert(tk.INSERT,'%s'%L)
    text.insert(tk.INSERT,"\n\n平均质量：\n")
    text.insert(tk.INSERT,'%s'%Values)
    text.insert(tk.INSERT,"\n\nGC含量：\n")
    text.insert(tk.INSERT,'%s\n\t'%CG)
    
    b1 = tk.Button(text, text="下载", width=15, height=2, command=Download)
    text.window_create(END,window=b1)

    #root1.mainloop()

#本地文件查询
def F1():
    filePath = getLocalFile()
    seq,v = read_fastq(filePath)
    Function(seq,v)

#输入序列查询
def F2():
    data = entry1.get("1.0",END)
    data = data.strip()
    print(type(data))
    s = data.split("\n")
    #print(s)
    seq = [] # 定义一个列表存储序列
    values = [] # 定义一个列表存储序列质量
    i = 0
    for line in s:
        line = line.strip() # 去除末尾换行符
        if (i%4 == 1):
            seq.append(line)
        if (i%4 == 3):
            values.append(line)
        i += 1
    #print(seq)
    #print(values)
    Function(seq,values)

if __name__ == '__main__':
    root = tk.Tk()
    root.title("求Fastq文件信息")
    root.geometry('450x400')

    label1 = tk.Label(text="Sequence", width=50, height=2)
    label1.pack()
    entry1 = tk.Text(root, width=200 , height=22)
    entry1.pack()

    button1 = tk.Button(text="本地文件查询" ,width=15, height=2, command=F1)
    button1.pack(padx=40, pady=10, side="left")
    button2 = tk.Button(text="输入序列查询" ,width=15, height=2, command=F2)
    button2.pack(padx=35, pady=10, side="left")

    root.mainloop()
