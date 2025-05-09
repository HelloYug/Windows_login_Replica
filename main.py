import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageFilter, ImageDraw
import random
import os
import time
import threading
import mysql.connector
from datetime import datetime
from collections import Counter
import pyautogui

# MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tiger",
    database="osproject"
)
cursor = conn.cursor(dictionary=True)

# Globals
failed_attempts = 0
locked_out = False
selected_user = None

# Load Random Background (Images only)
bg_images = [f for f in os.listdir("Wallpapers") if f.lower().endswith((".png", ".jpg", ".jpeg"))]
random_image_path = os.path.join("Wallpapers", random.choice(bg_images))
original_img = Image.open(random_image_path)

# GUI Setup
root = tk.Tk()
root.attributes("-fullscreen", True)
root.configure(bg="black")
screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
root.title("OS Security Screen")

# configuring window icon
WindowIcon = tk.PhotoImage(file = "Windows-New-Logo.png")
root.iconphoto(False, WindowIcon)

# Resize and Blur
resized_img = original_img.resize((screen_width, screen_height))
blurred_img = resized_img.filter(ImageFilter.GaussianBlur(8))
bg_photo = ImageTk.PhotoImage(resized_img)
blurred_photo = ImageTk.PhotoImage(blurred_img)

# Get readable foreground color based on image
avg_color = resized_img.resize((1, 1)).getpixel((0, 0))
r, g, b = avg_color[:3]
brightness = (r*299 + g*587 + b*114) / 1000
print (brightness)
fg_color = "black" if brightness > 125 else "white"

# Canvas Setup
canvas = tk.Canvas(root, width=screen_width, height=screen_height, highlightthickness=0)
canvas.pack()
bg_id = canvas.create_image(0, 0, anchor="nw", image=bg_photo)
time_text = canvas.create_text(screen_width // 2, screen_height // 2 - 20, text="", font=("Segoe UI", 38, "bold"), fill=fg_color, tags="time")
date_text = canvas.create_text(screen_width // 2, screen_height // 2 + 25, text="", font=("Segoe UI", 20), fill=fg_color, tags="date")
tap_text = canvas.create_text(screen_width // 2, screen_height - 100, text="Tap to Continue", font=("Segoe UI", 18, "bold"), fill=fg_color, tags="tap")
tap_arrow = canvas.create_text(screen_width // 2, screen_height - 120, text="^", font=("Segoe UI", 20, "bold"), fill=fg_color, tags="tap")

# Update Time
is_first_screen = True

def update_time():
    while True:
        now = datetime.now()
        t = now.strftime("%H:%M:%S")
        d = now.strftime("%A, %d %B %Y")
        if is_first_screen:
            canvas.itemconfigure("time", text=t)
            canvas.itemconfigure("date", text=d)
        else:
            canvas.coords("time", screen_width - 100, screen_height - 30)
            canvas.itemconfigure("time", text=t)
            canvas.itemconfigure("date", text="")
        time.sleep(1)

# Slide Up
slide_y = 0

def slide_up():
    global slide_y, is_first_screen
    canvas.delete("tap", "date", "time")
    for i in range(0, screen_height, 25):
        slide_y -= 20
        canvas.move(bg_id, 0, -25)
        canvas.update()
        time.sleep(0.005)
    is_first_screen = False
    show_users()

# Entry Point
canvas.bind("<Button-1>", lambda e: slide_up())

# Show User Circles
def show_users():
    canvas.itemconfig(bg_id, image=blurred_photo)
    canvas.create_image(0, 0, anchor="nw", image=blurred_photo)
    canvas.image = blurred_photo

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    start_x = (screen_width - (len(users) * 160)) // 2

    sizeofimage = 140

    for idx, user in enumerate(users):
        img_path = os.path.join("User Profiles", user["image"])
        if not os.path.exists(img_path):
            continue
        img = Image.open(img_path).resize((sizeofimage, sizeofimage)).convert("RGBA")
        circle = Image.new("L", (sizeofimage, sizeofimage), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, sizeofimage, sizeofimage), fill=255)
        img.putalpha(circle)
        user_tk = ImageTk.PhotoImage(img)

        x_pos = start_x + idx * 180
        btn = tk.Button(root, image=user_tk, bd=0, bg="black", activebackground="black",
                        command=lambda u=user: show_password_input(u))
        btn.image = user_tk
        btn.place(x=x_pos + 60, y=275, anchor="center")

        name = tk.Label(root, text=user["username"], font=("Segoe UI", 12, "bold"), fg=fg_color )
        name.place(x=x_pos + 70, y=375, anchor="center")

        email = tk.Label(root, text=user["email"], font=("Segoe UI", 8), foreground=fg_color)
        email.place(x=x_pos + 70, y=400, anchor="center")

# Freeze logic
def freeze_system(duration):
    center_x, center_y = screen_width // 2, screen_height // 2
    stop_event = threading.Event()
    def lock_mouse():
        while not stop_event.is_set():
            pyautogui.moveTo(center_x, center_y)
            root.attributes("-topmost", True)
            time.sleep(0.01)
    thread = threading.Thread(target=lock_mouse)
    thread.daemon = True
    thread.start()
    root.after(duration, stop_event.set)  # Freeze for 10 seconds


# Password Input
def show_password_input(user):
    global selected_user
    selected_user = user
    canvas.delete("all")
    canvas.create_image(0, 0, anchor="nw", image=blurred_photo)
    canvas.image = blurred_photo
    canvas.create_text(screen_width//2, 135, text=f"Welcome {user['username']}", font=("Segoe UI", 24, "bold"), fill=fg_color, anchor="n")

    label = tk.Label(root, text="Enter Password", font=("Segoe UI", 14))
    label.place(x=screen_width//2, y=440, anchor="n")

    entry = tk.Entry(root, show="*", font=("Segoe UI", 14))
    entry.place(x=screen_width//2, y=470, anchor="n")

    def verify():
        global failed_attempts, locked_out
        if locked_out:
            return
        if entry.get() == user["password"]:
            messagebox.showinfo("Login", "Access Granted!")
            pyautogui.hotkey("win", "d")
            root.destroy()
        else:
            failed_attempts += 1
            if failed_attempts >= 5:
                locked_out = True
                messagebox.showwarning("Locked", "Too many attempts. System is frozen for 15 seconds.")
                duration = 15000
                freeze_system(duration)
                root.after(duration, unlock)
            else:
                messagebox.showerror("Error", f"Wrong password! Attempt {failed_attempts}/5.")

    btn = tk.Button(root, text="Login", command=verify, font=("Segoe UI", 12), bg="white", fg="black")
    btn.place(x=screen_width//2, y=510, anchor="n")

    entry.bind("<Return>", lambda e: verify())
    entry.focus_set()

def unlock():
    global failed_attempts, locked_out, is_first_screen
    failed_attempts = 0
    locked_out = False
    is_first_screen = False
    canvas.delete("all")
    canvas.create_image(0, 0, anchor="nw", image=blurred_photo)
    canvas.image = blurred_photo
    show_users()

# Clock Thread
clock_thread = threading.Thread(target=update_time, daemon=True)
clock_thread.start()

root.mainloop()