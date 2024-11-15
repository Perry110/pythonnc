import tkinter as tk 
from tkinter import ttk

#Create instance 
win = tk.Tk()

#Add a title 
win.title("Carculator")


#Add a frame
nhap_frame = ttk.LabelFrame(win, text='Nhap')
nhap_frame.grid(column=0 , row=0 )
tinh_frame = ttk.LabelFrame(win, text='Tinh')
tinh_frame.grid(column=0, row=1)
result_frame = ttk.LabelFrame(win, text='Ket qua')
result_frame.grid(column=0, row=2)


#Button Click Event Function
def plus_me() :
    try:
        total = float(a.get()) + float(b.get())
        output_result.insert(0,f"Tổng là : {total} ")
    except:
        output_result.insert(0,"Nhap sai")

def minus_me() :
    try:
        total = float(a.get()) - float(b.get())
        output_result.insert(0,f" Hiệu là : {total} ")
    except:
        output_result.insert(0,"Nhap sai")
def core_me() :
    try:
        total = float(a.get()) * float(b.get())
        output_result.insert(0,f" Tích là : {total} ")
    except:
        output_result.insert(0,"Nhap sai")
def divide_me() :
    try:
        total = float(a.get()) / float(b.get())
        output_result.insert(0,f" Thương là : {total} ")
    except:
        output_result.insert(0,"Nhap sai")

#Changing out label 
ttk.Label(nhap_frame, text="Nhập a : ").grid(column=0, row=0)
ttk.Label(nhap_frame, text="Nhập b : ").grid(column=0, row=1)

#Adding a button 
Plus = ttk.Button(tinh_frame, text="+", command=plus_me)
Plus.grid(column=0, row=0)
Minus = ttk.Button(tinh_frame, text="-", command=minus_me)
Minus.grid(column=1,row=0)
Core = ttk.Button(tinh_frame, text=".", command=core_me)
Core.grid(column=0,row=1)
Divide = ttk.Button(tinh_frame, text=":", command=divide_me)
Divide.grid(column=1,row=1)


#Adding a Text box Entry widget 
a = tk.StringVar()
b = tk.StringVar()
a_entered = ttk.Entry(nhap_frame, width=12, textvariable=a)
a_entered.grid(column=1, row=0)
b_entered = ttk.Entry(nhap_frame, width=12, textvariable=b)
b_entered.grid(column=1, row=1)
a_entered.focus()
output_result = ttk.Entry(result_frame, width=12)
output_result.grid(column=0, row=0)

win.mainloop()