import tkinter as tk
from tkinter import messagebox
import random
import os
import math
from PIL import Image, ImageTk
from cards import tarot_cards

# ==============================
# ตัวแปรระบบ (State Variables)
# ==============================
base_path = os.path.dirname(__file__)
image_folder = os.path.join(base_path, "images")

selected_cards = []  # เก็บไพ่ที่ถูกเลือก
max_picks = 1        # จำนวนที่ต้องเลือก (1 หรือ 10)
card_items = []      # เก็บ object ไพ่บน Canvas
canvas_cards_map = {} # แมป id ของไพ่บน canvas กับสถานะว่าถูกเลือกไปหรือยัง

# ==============================
# กลุ่มไพ่คัดกรองเฉพาะหมวด
# ==============================
love_pool = ["The Lovers", "The Sun", "The Star", "The Empress", "Wheel of Fortune", "The Fool", "The Moon", "Strength"]
career_pool = ["The Emperor", "The Chariot", "The Magician", "The Sun", "Wheel of Fortune", "The Hierophant", "Justice", "The Hermit"]

# ==============================
# ฟังก์ชันเริ่มใหม่ตามหมวด
# ==============================
def on_category_change():
    global selected_cards, max_picks
    selected_cards.clear()
    
    cat = category_var.get()
    max_picks = 10 if cat == "monthly" else 1
    
    card_label.config(text=f"กรุณาคลิกเลือกไพ่ {max_picks} ใบจากวงกลม")
    result_text.config(state="normal")
    result_text.delete(1.0, tk.END)
    result_text.config(state="disabled")
    
    image_label.config(image="")
    image_label.image = None
    
    draw_card_circle()

# ==============================
# วาดไพ่เป็นวงกลมบน Canvas
# ==============================
def draw_card_circle():
    card_canvas.delete("all")
    card_items.clear()
    canvas_cards_map.clear()
    
    center_x, center_y = 250, 150
    radius = 100
    num_cards = 15 # จำนวนไพ่จำลองที่วางโชว์ด้านหลัง
    
    for i in range(num_cards):
        angle = i * (2 * math.pi / num_cards) - (math.pi / 2) # เริ่มจากด้านบน
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        
        # วาดไพ่สีดำขอบทอง
        card_id = card_canvas.create_rectangle(x-20, y-30, x+20, y+30, fill="#2C2C2C", outline="gold", width=2)
        card_canvas.tag_bind(card_id, "<Button-1>", lambda event, cid=card_id: pick_card(cid))
        card_items.append(card_id)
        canvas_cards_map[card_id] = False # False = ยังไม่ถูกเลือก

# ==============================
# ฟังก์ชันผู้ใช้คลิกเลือกไพ่
# ==============================
def pick_card(card_id):
    global selected_cards, max_picks
    
    if len(selected_cards) >= max_picks:
        messagebox.showinfo("แจ้งเตือน", f"คุณเลือกครบ {max_picks} ใบแล้วครับ ดูคำทำนายได้เลย")
        return
        
    if canvas_cards_map[card_id]:
        return # ถ้าไพ่ใบนี้ถูกคลิกไปแล้ว ให้ข้าม
        
    category = category_var.get()
    
    # กรองกลุ่มไพ่ที่จะนำมาสุ่มตามหมวด
    pool = list(tarot_cards.keys())
    if category == "love":
        pool = [c for c in love_pool if c in tarot_cards]
    elif category == "career":
        pool = [c for c in career_pool if c in tarot_cards]
        
    # ตัดไพ่ที่ถูกสุ่มไปแล้วออก (ป้องกันไพ่ซ้ำ)
    available = [c for c in pool if c not in selected_cards]
    
    # ถ้าไพ่ในกลุ่มหมด ให้ดึงไพ่ที่เหลือในสำรับหลักมาเสริม (เผื่อกรณีดึงเยอะเกิน)
    if not available:
        available = [c for c in tarot_cards.keys() if c not in selected_cards]

    chosen_card = random.choice(available)
    selected_cards.append(chosen_card)
    
    # เปลี่ยนสีไพ่บน Canvas ให้รู้ว่าเลือกไปแล้ว
    card_canvas.itemconfig(card_id, fill="gray", outline="gray")
    canvas_cards_map[card_id] = True
    
    card_label.config(text=f"เลือกแล้ว {len(selected_cards)}/{max_picks} ใบ")
    
    # หากเลือกครบตามจำนวน ให้ทำนายทันที
    if len(selected_cards) == max_picks:
        predict()

# ==============================
# ฟังก์ชันแสดงคำทำนาย
# ==============================
def predict():
    category = category_var.get()
    
    result_text.config(state="normal")
    result_text.delete(1.0, tk.END)
    
    result_text.insert(tk.END, "✨ คำทำนายของคุณ ✨\n\n")
    
    for i, card_name in enumerate(selected_cards):
        prediction = tarot_cards[card_name][category]
        if max_picks > 1:
            result_text.insert(tk.END, f"ใบที่ {i+1}: {card_name}\nคำทำนาย: {prediction}\n\n")
        else:
            result_text.insert(tk.END, f"ไพ่ที่ได้: {card_name}\n\nคำทำนาย:\n{prediction}\n\n")
            
    result_text.config(state="disabled")
    
    # แสดงรูปไพ่ (แสดงใบสุดท้ายที่เลือก)
    show_card_image(selected_cards[-1])

# ==============================
# แสดงรูปไพ่ (ใบที่เพิ่งถูกเปิดล่าสุด)
# ==============================
def show_card_image(card_name):
    filename = card_name.lower().replace(" ", "_") + ".jpg"
    image_path = os.path.join(image_folder, filename)

    if os.path.exists(image_path):
        img = Image.open(image_path)
        img = img.resize((120, 180)) # ปรับขนาดรูปให้เล็กลงหน่อยเพื่อประหยัดพื้นที่
        photo = ImageTk.PhotoImage(img)
        image_label.config(image=photo)
        image_label.image = photo
    else:
        # หากไม่มีรูปให้ซ่อนไว้
        image_label.config(image="")
        image_label.image = None

# ==============================
# GUI Setup
# ==============================
root = tk.Tk()
root.title("Fortune Application")
root.geometry("500x750") # ปรับหน้าต่างให้สูงขึ้นรองรับเนื้อหา

title = tk.Label(root, text="Fortune Application", font=("Arial", 20, "bold"))
title.pack(pady=10)

# หมวดการทำนาย
category_var = tk.StringVar(value="daily")

frame_radio = tk.Frame(root)
frame_radio.pack()

tk.Radiobutton(frame_radio, text="รายวัน (1 ใบ)", variable=category_var, value="daily", command=on_category_change).pack(side="left", padx=5)
tk.Radiobutton(frame_radio, text="รายเดือน (10 ใบ)", variable=category_var, value="monthly", command=on_category_change).pack(side="left", padx=5)
tk.Radiobutton(frame_radio, text="ความรัก (1 ใบ)", variable=category_var, value="love", command=on_category_change).pack(side="left", padx=5)
tk.Radiobutton(frame_radio, text="การงาน (1 ใบ)", variable=category_var, value="career", command=on_category_change).pack(side="left", padx=5)

# Canvas สำหรับวงกลมไพ่
card_canvas = tk.Canvas(root, width=500, height=300, bg="#F0F0F0", highlightthickness=0)
card_canvas.pack(pady=10)

card_label = tk.Label(root, text="กรุณาคลิกเลือกไพ่ 1 ใบจากวงกลม", font=("Arial", 12, "bold"))
card_label.pack(pady=5)

# แสดงรูปไพ่
image_label = tk.Label(root)
image_label.pack(pady=5)

# กล่องข้อความแบบมี Scrollbar สำหรับคำทำนาย
frame_text = tk.Frame(root)
frame_text.pack(pady=10, fill="both", expand=True)

scrollbar = tk.Scrollbar(frame_text)
scrollbar.pack(side="right", fill="y")

result_text = tk.Text(frame_text, height=10, width=50, yscrollcommand=scrollbar.set, font=("Arial", 11), bg="#FAFAFA", state="disabled", wrap="word")
result_text.pack(side="left", fill="both", expand=True, padx=(20, 0))

scrollbar.config(command=result_text.yview)

# เริ่มต้นวาดไพ่ครั้งแรก
draw_card_circle()

root.mainloop()
