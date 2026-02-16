import tkinter as tk
from tkinter import messagebox
import random
import os
from PIL import Image, ImageTk

# ==============================
# ข้อมูลไพ่ (Dictionary)
# ==============================

tarot_cards = {
    "The Fool": {
        "daily": "วันนี้เหมาะกับการเริ่มต้นสิ่งใหม่",
        "monthly": "เดือนนี้มีโอกาสใหม่เข้ามา",
        "love": "ความรักสดใส มีโอกาสเริ่มต้นใหม่",
        "career": "อาจได้งานใหม่หรือโปรเจคใหม่"
    },
    "The Magician": {
        "daily": "คุณมีพลังและความสามารถเต็มที่",
        "monthly": "เป็นเดือนแห่งความสำเร็จ",
        "love": "คุณมีเสน่ห์มากในช่วงนี้",
        "career": "ควบคุมสถานการณ์งานได้ดี"
    },
    "The Sun": {
        "daily": "เป็นวันที่ดี มีความสุข",
        "monthly": "เดือนแห่งความสำเร็จและข่าวดี",
        "love": "ความรักมีความสุขและอบอุ่น",
        "career": "งานประสบความสำเร็จ"
    },
    "The Moon": {
        "daily": "ควรระวังความสับสน",
        "monthly": "เดือนนี้ต้องใช้สติในการตัดสินใจ",
        "love": "ความรักยังไม่ชัดเจน",
        "career": "ระวังเรื่องเอกสารและการสื่อสาร"
    },
    "The Star": {
        "daily": "มีความหวังและพลังบวก",
        "monthly": "อนาคตสดใส มีโอกาสดีเข้ามา",
        "love": "ความสัมพันธ์พัฒนาไปในทางที่ดี",
        "career": "มีคนสนับสนุนช่วยเหลือ"
    }
}

# ==============================
# ตั้งค่า path รูปภาพ
# ==============================

base_path = os.path.dirname(__file__)
image_folder = os.path.join(base_path, "images")

selected_card = None

# ==============================
# ฟังก์ชันสุ่มไพ่
# ==============================

def shuffle_cards():
    global selected_card
    selected_card = random.choice(list(tarot_cards.keys()))
    card_label.config(text="ไพ่ถูกสุ่มแล้ว กดทำนายผล")

# ==============================
# ฟังก์ชันทำนาย
# ==============================

def predict():
    if not selected_card:
        messagebox.showwarning("แจ้งเตือน", "กรุณากดสุ่มไพ่ก่อน")
        return

    category = category_var.get()
    result = tarot_cards[selected_card][category]

    result_label.config(
        text=f"ไพ่ที่ได้: {selected_card}\n\nคำทำนาย:\n{result}"
    )

    show_card_image(selected_card)

# ==============================
# แสดงรูปไพ่ (ถ้ามี)
# ==============================

def show_card_image(card_name):
    filename = card_name.lower().replace(" ", "_") + ".jpg"
    image_path = os.path.join(image_folder, filename)

    if os.path.exists(image_path):
        img = Image.open(image_path)
        img = img.resize((150, 230))
        photo = ImageTk.PhotoImage(img)
        image_label.config(image=photo)
        image_label.image = photo
    else:
        image_label.config(image="")
        image_label.image = None

# ==============================
# GUI
# ==============================

root = tk.Tk()
root.title("Fortune Application")
root.geometry("500x600")

title = tk.Label(root, text="Fortune Application", font=("Arial", 20, "bold"))
title.pack(pady=10)

# หมวดการทำนาย
category_var = tk.StringVar(value="daily")

tk.Radiobutton(root, text="รายวัน", variable=category_var, value="daily").pack()
tk.Radiobutton(root, text="รายเดือน", variable=category_var, value="monthly").pack()
tk.Radiobutton(root, text="ความรัก", variable=category_var, value="love").pack()
tk.Radiobutton(root, text="การงาน", variable=category_var, value="career").pack()

tk.Button(root, text="🎴 สุ่มไพ่", bg="orange", command=shuffle_cards).pack(pady=10)
tk.Button(root, text="🔮 ทำนายผล", bg="gold", command=predict).pack(pady=10)

card_label = tk.Label(root, text="กดสุ่มไพ่เพื่อเริ่ม", font=("Arial", 12))
card_label.pack(pady=5)

image_label = tk.Label(root)
image_label.pack(pady=10)

result_label = tk.Label(root, text="", wraplength=400, justify="center")
result_label.pack(pady=20)

root.mainloop()
