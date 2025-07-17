import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import time
import math
import random

class DeskFrien:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)        
        self.root.wm_attributes("-transparentcolor", 'white')  
        self.root.configure(bg='white')

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.base_x = screen_width - 200
        self.base_y = screen_height - 200
        self.root.geometry(f"+{self.base_x}+{self.base_y}")

        #assets
        self.gifs = {
            "hop": self.load_gif("jumping_cat.gif"),       
            "idle_fly": self.load_gif("idle_fly_cat.gif"), 
            "fly": self.load_gif("balloon_cat.gif"),        
            "sleep": self.load_gif("sleeping_cat.gif")     
        }

        self.label = tk.Label(root, bg='white')
        self.label.pack()

        self.mode = "hop"
        self.last_activity = time.time()
        self.frame_index = 0
        self.floating = False
        self.float_offset = 0
        self.animate()
        self.idle_check()

        #control
        self.label.bind("<Enter>", self.fly_mode)
        self.label.bind("<ButtonPress-1>", self.start_drag)
        self.label.bind("<B1-Motion>", self.do_drag)

    def load_gif(self, filename):
        gif = Image.open(filename)
        return [ImageTk.PhotoImage(frame.convert("RGBA")) for frame in ImageSequence.Iterator(gif)]

    def set_mode(self, mode):
        if mode == "happy":
            
            mode = random.choice(["hop", "idle_fly"])

        if self.mode != mode:
            self.mode = mode
            self.frame_index = 0

            if mode == "fly":
                self.start_floating()
                self.root.after(5000, self.stop_floating_and_return)

    def animate(self):
        frames = self.gifs[self.mode]
        self.label.configure(image=frames[self.frame_index])
        self.frame_index = (self.frame_index + 1) % len(frames)
        self.root.after(100, self.animate)

    def idle_check(self):
        if time.time() - self.last_activity > 90 and self.mode != "sleep":
            self.set_mode("sleep")
        self.root.after(1000, self.idle_check)

    def fly_mode(self, event=None):
        self.last_activity = time.time()
        self.set_mode("fly")

    def start_floating(self):
        self.floating = True
        self.float_offset = 0
        self.float()

    def stop_floating_and_return(self):
        self.floating = False
        self.set_mode("happy")
        self.root.geometry(f"+{self.base_x}+{self.base_y}")

    def float(self):
        if not self.floating:
            return
        self.float_offset += 1
        offset_y = int(10 * math.sin(self.float_offset / 5))
        self.root.geometry(f"+{self.base_x}+{self.base_y + offset_y}")
        self.root.after(50, self.float)

    def start_drag(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def do_drag(self, event):
        x = self.root.winfo_x() + event.x - self.drag_start_x
        y = self.root.winfo_y() + event.y - self.drag_start_y
        self.root.geometry(f"+{x}+{y}")
        self.base_x = x
        self.base_y = y



root = tk.Tk()
app = DeskFrien(root)
root.mainloop()