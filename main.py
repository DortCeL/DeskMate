import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import pystray
import os
import sys
import threading

WINDOW_SIZE = 400
RIGHT_GAP = 60
TASKBAR_HEIGHT = 48

if hasattr(sys, "_MEIPASS"):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

GIF_PATH = os.path.join(BASE_DIR, "chika.gif")
BG_TRANSPARENT_KEY = "black"


class DesktopPet:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)

        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        pos_x = screen_w - WINDOW_SIZE - RIGHT_GAP
        pos_y = screen_h - WINDOW_SIZE - TASKBAR_HEIGHT
        self.root.geometry(f"{WINDOW_SIZE}x{WINDOW_SIZE}+{pos_x}+{pos_y}")

        self.root.config(bg=BG_TRANSPARENT_KEY)
        self.root.attributes("-transparentcolor", BG_TRANSPARENT_KEY)

        self.canvas = tk.Canvas(
            self.root, width=WINDOW_SIZE, height=WINDOW_SIZE,
            bg=BG_TRANSPARENT_KEY, highlightthickness=0
        )
        self.canvas.pack()

        self.frames, self.frame_durations = self.load_gif_frames(GIF_PATH)
        self.frame_index = 0

        self.image_item = self.canvas.create_image(
            WINDOW_SIZE // 2, WINDOW_SIZE // 2,
            image=self.frames[0]
        )

        self.animate()
        self.root.bind("<Escape>", lambda e: self.exit_app())

        self.tray_icon = self.create_tray_icon()
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def create_tray_icon(self):
        gif = Image.open(GIF_PATH)
        icon_image = gif.convert("RGBA").resize((64, 64), Image.LANCZOS)

        menu = pystray.Menu(
            pystray.MenuItem("Exit", lambda icon, item: self.exit_app())
        )
        return pystray.Icon("desktop_pet", icon_image, "Desktop Pet", menu)

    def exit_app(self):
        self.tray_icon.stop()
        self.root.after(0, self.root.destroy)

    def load_gif_frames(self, path):
        gif = Image.open(path)
        frames = []
        durations = []
        for frame in ImageSequence.Iterator(gif):
            frame = frame.convert("RGBA").resize(
                (WINDOW_SIZE, WINDOW_SIZE), Image.LANCZOS)

            bg = Image.new("RGBA", frame.size, BG_TRANSPARENT_KEY)
            composited = Image.alpha_composite(bg, frame).convert("RGB")

            frames.append(ImageTk.PhotoImage(composited))
            durations.append(frame.info.get(
                "duration", 100))  # ms, default 100
        return frames, durations

    def animate(self):
        self.canvas.itemconfig(
            self.image_item, image=self.frames[self.frame_index])
        delay = self.frame_durations[self.frame_index]
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.root.after(delay, self.animate)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    DesktopPet().run()
