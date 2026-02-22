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

selected_cards = []  
max_picks = 1        
card_items = []      
canvas_cards_map = {} 
image_refs = []      
back_card_image = None # เก็บรูป Blackcard

# ==============================
# กลุ่มไพ่คัดกรองเฉพาะหมวด
# ==============================
love_pool = ["The Lovers", "The Sun", "The Star", "The Empress", "Wheel of Fortune", "The Fool", "The Moon", "Strength"]
career_pool = ["The Emperor", "The Chariot", "The Magician", "The Sun", "Wheel of Fortune", "The Hierophant", "Justice", "The Hermit"]

# ==============================
# ฟังก์ชันเริ่ม/ทำนายใหม่
# ==============================
def reset_prediction():
    global selected_cards, max_picks
    selected_cards.clear()
    
    cat = category_var.get()
    max_picks = 10 if cat == "monthly" else 1
    
    card_label.config(text=f"กรุณาคลิกเลือกไพ่ {max_picks} ใบจากวงกลม")
    
    # ล้างหน้าจอคำทำนายเก่าทิ้ง
    for widget in prediction_container.winfo_children():
        widget.destroy()
    image_refs.clear()
    
    # วาดวงกลมไพ่ใหม่
    draw_card_circle()
    
    # เลื่อนจอกลับขึ้นไปบนสุด
    main_canvas.yview_moveto(0)

# ==============================
# วาดไพ่เป็นวงกลมบน Canvas (ใช้รูป Blackcard)
# ==============================
def draw_card_circle():
    global back_card_image
    card_canvas.delete("all")
    card_items.clear()
    canvas_cards_map.clear()
    
    center_x, center_y = 250, 160
    radius = 110
    num_cards = 78
    
    # โหลดรูป Blackcard (ถ้ามี)
    blackcard_path = os.path.join(image_folder, "blackcard.jpg") # <-- เปลี่ยนเป็น .png ได้ถ้าไฟล์คุณเป็น png
    has_image = os.path.exists(blackcard_path)
    
    if has_image:
        img = Image.open(blackcard_path).resize((40, 60)) # ปรับขนาดรูปหลังไพ่
        back_card_image = ImageTk.PhotoImage(img)

    for i in range(num_cards):
        angle = i * (2 * math.pi / num_cards) - (math.pi / 2)
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        
        # 1. วาดสี่เหลี่ยมสีเทาไว้เป็น "พื้นหลัง" เวลาไพ่ถูกเลือกไปแล้ว
        card_canvas.create_rectangle(x-20, y-30, x+20, y+30, fill="#888888", outline="#555555")
        
        # 2. วางรูป Blackcard หรือ สี่เหลี่ยมสีดำทับไว้ด้านบน
        if has_image:
            card_id = card_canvas.create_image(x, y, image=back_card_image)
        else:
            card_id = card_canvas.create_rectangle(x-20, y-30, x+20, y+30, fill="#2C2C2C", outline="gold", width=2)
            
        card_canvas.tag_bind(card_id, "<Button-1>", lambda event, cid=card_id: pick_card(cid))
        card_items.append(card_id)
        canvas_cards_map[card_id] = False

# ==============================
# ฟังก์ชันผู้ใช้คลิกเลือกไพ่
# ==============================
def pick_card(card_id):
    global selected_cards, max_picks
    
    if len(selected_cards) >= max_picks:
        messagebox.showinfo("แจ้งเตือน", f"คุณเลือกครบ {max_picks} ใบแล้วครับ ดูคำทำนายด้านล่างได้เลย")
        return
        
    if canvas_cards_map[card_id]:
        return 
        
    category = category_var.get()
    pool = list(tarot_cards.keys())
    
    if category == "love":
        pool = [c for c in love_pool if c in tarot_cards]
    elif category == "career":
        pool = [c for c in career_pool if c in tarot_cards]
        
    available = [c for c in pool if c not in selected_cards]
    if not available:
        available = [c for c in tarot_cards.keys() if c not in selected_cards]

    chosen_card = random.choice(available)
    selected_cards.append(chosen_card)
    
    # ซ่อนไพ่ที่ถูกคลิก เพื่อให้เห็นพื้นหลังสีเทา (แสดงว่าเลือกแล้ว)
    card_canvas.itemconfig(card_id, state='hidden')
    canvas_cards_map[card_id] = True
    
    card_label.config(text=f"เลือกแล้ว {len(selected_cards)}/{max_picks} ใบ")
    
    if len(selected_cards) == max_picks:
        predict()

# ==============================
# ฟังก์ชันแสดงคำทำนายพร้อมรูป
# ==============================
def predict():
    category = category_var.get()
    
    for widget in prediction_container.winfo_children():
        widget.destroy()
    image_refs.clear()
    
    tk.Label(prediction_container, text="✨ คำทำนายของคุณ ✨", font=("Arial", 16, "bold"), bg="#FAFAFA").pack(pady=15)
    
    for i, card_name in enumerate(selected_cards):
        card_frame = tk.Frame(prediction_container, bd=1, relief="solid", bg="white")
        card_frame.pack(pady=10, padx=20, fill="x")
        
        prediction_text = tarot_cards[card_name][category]
        
        filename = card_name.lower().replace(" ", "_") + ".jpg"
        image_path = os.path.join(image_folder, filename)
        
        img_label = tk.Label(card_frame, bg="white")
        img_label.pack(side="left", padx=15, pady=15)
        
        if os.path.exists(image_path):
            img = Image.open(image_path)
            img = img.resize((90, 140)) 
            photo = ImageTk.PhotoImage(img)
            img_label.config(image=photo)
            image_refs.append(photo) 
        else:
            img_label.config(text="[ไม่มีรูป]", width=12, height=8, bg="#EEEEEE")
            
        header = f"ใบที่ {i+1}: {card_name}" if max_picks > 1 else f"ไพ่ที่ได้: {card_name}"
        text_content = f"{header}\n\n{prediction_text}"
        
        text_label = tk.Label(card_frame, text=text_content, font=("Arial", 11), bg="white", justify="left", wraplength=300)
        text_label.pack(side="left", padx=10, pady=15, fill="both", expand=True)
        
    scrollable_frame.update_idletasks()
    main_canvas.configure(scrollregion=main_canvas.bbox("all"))

# ==============================
# GUI Setup (ระบบเลื่อนทั้งหน้าต่าง)
# ==============================
root = tk.Tk()
root.title("Fortune Application")
root.geometry("540x800")

main_canvas = tk.Canvas(root, highlightthickness=0)
main_scrollbar = tk.Scrollbar(root, orient="vertical", command=main_canvas.yview)
scrollable_frame = tk.Frame(main_canvas)

scrollable_frame.bind("<Configure>", lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all")))
canvas_window = main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

def on_canvas_configure(event):
    main_canvas.itemconfig(canvas_window, width=event.width)
main_canvas.bind('<Configure>', on_canvas_configure)

main_canvas.configure(yscrollcommand=main_scrollbar.set)
main_canvas.pack(side="left", fill="both", expand=True)
main_scrollbar.pack(side="right", fill="y")

def _on_mousewheel(event):
    main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
root.bind_all("<MouseWheel>", _on_mousewheel)

# ==============================
# ใส่ Widget
# ==============================
title = tk.Label(scrollable_frame, text="Fortune Application", font=("Arial", 20, "bold"))
title.pack(pady=20)

category_var = tk.StringVar(value="daily")
frame_radio = tk.Frame(scrollable_frame)
frame_radio.pack()

tk.Radiobutton(frame_radio, text="รายวัน", variable=category_var, value="daily", command=reset_prediction).pack(side="left", padx=5)
tk.Radiobutton(frame_radio, text="รายเดือน", variable=category_var, value="monthly", command=reset_prediction).pack(side="left", padx=5)
tk.Radiobutton(frame_radio, text="ความรัก", variable=category_var, value="love", command=reset_prediction).pack(side="left", padx=5)
tk.Radiobutton(frame_radio, text="การงาน", variable=category_var, value="career", command=reset_prediction).pack(side="left", padx=5)

# ------------------------------
# ปุ่มทำนายใหม่ (New Button!)
# ------------------------------
btn_reset = tk.Button(scrollable_frame, text="🔄 ทำนายใหม่", command=reset_prediction, bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), padx=10)
btn_reset.pack(pady=10)

card_canvas = tk.Canvas(scrollable_frame, width=500, height=320, highlightthickness=0)
card_canvas.pack(pady=5)

card_label = tk.Label(scrollable_frame, text="กรุณาคลิกเลือกไพ่ 1 ใบจากวงกลม", font=("Arial", 12, "bold"), fg="#333333")
card_label.pack(pady=5)

prediction_container = tk.Frame(scrollable_frame, bg="#FAFAFA")
prediction_container.pack(fill="both", expand=True, pady=10)

reset_prediction()

root.mainloop()
