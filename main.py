import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageSequence
import subprocess  


def show_frame(frame):
    frame.tkraise()


def run_realtime_script():
    subprocess.run(['python', 'real.py'])  


root = tk.Tk()
root.title("Sign Language Project")
root.geometry("800x600")


gif_files = ["back.gif", "back2.gif", "back3.gif", "back4.gif"]
gif_frames = {}  


def animate_gif(frame_label, gif_frames, current_gif, ind):
    frames = gif_frames[current_gif]
    frame_label.configure(image=frames[ind])
    ind = (ind + 1) % len(frames)  
    root.after(100, animate_gif, frame_label, gif_frames, current_gif, ind)  


def load_gif_frames(gif_files):
    for gif in gif_files:
        gif_image = Image.open(gif)
        frames = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(gif_image)]
        gif_frames[gif] = frames


def switch_gif():
    global current_gif_index
    current_gif_index = (current_gif_index + 1) % len(gif_files)
    current_gif = gif_files[current_gif_index]

   
    animate_gif(home_background_label, gif_frames, current_gif, 0)
    animate_gif(about_background_label, gif_frames, current_gif, 0)
    animate_gif(contact_background_label, gif_frames, current_gif, 0)
    
    root.after(30000, switch_gif)  


load_gif_frames(gif_files)


container = tk.Frame(root)
container.place(relwidth=1, relheight=1)


container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)


home_frame = tk.Frame(container)
about_frame = tk.Frame(container)
contact_frame = tk.Frame(container)

for frame in (home_frame, about_frame, contact_frame):
    frame.grid(row=0, column=0, sticky="nsew")


home_background_label = tk.Label(home_frame)
home_background_label.place(relwidth=1, relheight=1)

about_background_label = tk.Label(about_frame)
about_background_label.place(relwidth=1, relheight=1)

contact_background_label = tk.Label(contact_frame)
contact_background_label.place(relwidth=1, relheight=1)

# Home Page - Align content without an additional frame
home_label = tk.Label(home_frame, text="Sign Language Project 🤟💬", font=("Arial", 26, "bold"), bg="black", fg="lightblue")
home_label.pack(pady=(40, 20), anchor="center")

project_button = ttk.Button(home_frame, text="About the Project", command=lambda: show_frame(about_frame), style='Accent.TButton')
project_button.pack(pady=20, anchor="center")

contact_button = ttk.Button(home_frame, text="Contact", command=lambda: show_frame(contact_frame), style='Accent.TButton')
contact_button.pack(pady=10, anchor="center")

# Add "Try" button on the home page
try_button = ttk.Button(home_frame, text="Try", command=run_realtime_script, style='Accent.TButton')  # This will run realtime.py
try_button.pack(pady=20, anchor="center")

# About Project Page
about_label = tk.Label(about_frame, text="About Our Sign Language Project", font=("Arial", 24, "bold"), bg="black", fg="lightblue")
about_label.pack(pady=(30, 20))

about_text = tk.Label(about_frame, text="This project aims to enable sign language recognition using AI technology. It helps to bridge the communication gap for the speech and hearing impaired. Sign language gestures can be recognized through a camera and interpreted into text or voice, making it accessible for all.\n\nFeatures include:\n- Sign language recognition\n- Voice and text translation\n- Continuous monitoring for accessibility.", font=("Arial", 14), bg="black", fg="lightblue", wraplength=500, justify="center")
about_text.pack(pady=20)

home_button = ttk.Button(about_frame, text="Back to Home", command=lambda: show_frame(home_frame), style='Accent.TButton')
home_button.pack(pady=10)

# Contact Page
contact_label = tk.Label(contact_frame, text="Contact Us", font=("Arial", 24, "bold"), bg="black", fg="lightblue")
contact_label.pack(pady=(30, 20))

contact_text = tk.Label(contact_frame, text="For any inquiries, feel free to reach out to us:\n\nEmail: gowtham.signproject@example.com\nPhone: +1-234-567-890", font=("Arial", 14), bg="black", fg="lightblue", justify="center")
contact_text.pack(pady=20)

home_button = ttk.Button(contact_frame, text="Back to Home", command=lambda: show_frame(home_frame), style='Accent.TButton')
home_button.pack(pady=10)

# Customize button styles
style = ttk.Style()
style.configure('Accent.TButton', font=('Arial', 12, 'bold'), padding=10)
style.map('Accent.TButton', background=[('active', '#FF4500'), ('!active', '#FFD700')])

# Start with the first GIF
current_gif_index = 0

# Start the GIF animation and switch every 30 seconds
switch_gif()

# Show the home page first
show_frame(home_frame)

# Run the application
root.mainloop()
