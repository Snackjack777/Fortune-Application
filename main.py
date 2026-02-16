import tkinter as tk
from tkinter import messagebox
import random
from cards import tarot_cards

selected_card = None

def select_card(card):
    global selected_card
    selected_card = card
    messagebox.showinfo("เลือกไพ่", f"คุณเลือกไพ่ {card}")

def predict():
    if not selected_card:
        messagebox.showwarning("แจ้งเตือน", "กรุณาเลือกไพ่ก่อน")
        return
    
    category = category_var.get()
    result = tarot_cards[selected_card][category]
    result_label.config(text=f"ผลการทำนาย:\n{result}")

# สร้างหน้าต่าง
root = tk.Tk()
root.title("Fortune Application")
root.geometry("500x600")

title = tk.Label(root, text="Fortune Application", font=("Arial", 20))
title.pack(pady=10)

# หมวดทำนาย
category_var = tk.StringVar(value="daily")

tk.Radiobutton(root, text="รายวัน", variable=category_var, value="daily").pack()
tk.Radiobutton(root, text="รายเดือน", variable=category_var, value="monthly").pack()
tk.Radiobutton(root, text="ความรัก", variable=category_var, value="love").pack()
tk.Radiobutton(root, text="การงาน", variable=category_var, value="career").pack()

# สุ่มไพ่ตัวอย่าง 5 ใบ
for card in list(tarot_cards.keys()):
    btn = tk.Button(root, text=card, command=lambda c=card: select_card(c))
    btn.pack(pady=5)

tk.Button(root, text="ทำนายผล", bg="gold", command=predict).pack(pady=20)

result_label = tk.Label(root, text="", wraplength=400)
result_label.pack()

root.mainloop()
