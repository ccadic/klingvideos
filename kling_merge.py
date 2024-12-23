import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip, concatenate_videoclips
from PIL import Image, ImageTk
import os

class VideoJoinerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Joiner")

        # Variables pour les vidéos
        self.video1_path = None
        self.video2_path = None
        self.video1_frame = None
        self.video2_frame = None

        # Boutons pour sélectionner les vidéos
        self.video1_button = tk.Button(root, text="Select Video 1", command=self.select_video1)
        self.video1_button.pack(pady=10)

        self.video2_button = tk.Button(root, text="Select Video 2", command=self.select_video2)
        self.video2_button.pack(pady=10)

        # Canvas pour afficher les premières images des vidéos
        self.video1_canvas = tk.Label(root, text="Video 1 Frame")
        self.video1_canvas.pack(pady=10)

        self.video2_canvas = tk.Label(root, text="Video 2 Frame")
        self.video2_canvas.pack(pady=10)

        # Bouton pour joindre les vidéos
        self.join_button = tk.Button(root, text="Join Videos", command=self.join_videos, state=tk.DISABLED)
        self.join_button.pack(pady=10)

    def select_video1(self):
        # Sélectionner la première vidéo
        self.video1_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")])
        if self.video1_path:
            self.video1_frame = self.get_first_frame(self.video1_path)
            self.display_image(self.video1_frame, self.video1_canvas)

        self.update_join_button_state()

    def select_video2(self):
        # Sélectionner la deuxième vidéo
        self.video2_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")])
        if self.video2_path:
            self.video2_frame = self.get_first_frame(self.video2_path)
            self.display_image(self.video2_frame, self.video2_canvas)

        self.update_join_button_state()

    def get_first_frame(self, video_path):
        # Utiliser MoviePy pour extraire la première frame
        try:
            clip = VideoFileClip(video_path)
            frame = clip.get_frame(0)  # Première frame (0 seconde)
            clip.close()
            return frame
        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract frame: {e}")
            return None

    def display_image(self, frame, canvas):
        # Convertir l'image en format compatible Tkinter
        if frame is not None:
            image = Image.fromarray(frame)
            image = image.resize((300, 200))  # Redimensionner pour l'affichage
            photo = ImageTk.PhotoImage(image)

            # Mettre à jour le canvas avec l'image
            canvas.config(image=photo)
            canvas.image = photo

    def update_join_button_state(self):
        # Activer le bouton "Join" si les deux vidéos sont sélectionnées
        self.join_button.config(state=tk.NORMAL if self.video1_path and self.video2_path else tk.DISABLED)

    def join_videos(self):
        if not self.video1_path or not self.video2_path:
            messagebox.showerror("Error", "Both videos must be selected.")
            return

        # Demander le chemin pour sauvegarder la vidéo finale
        save_path = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")]
        )
        if not save_path:
            return

        # Joindre les vidéos
        try:
            clip1 = VideoFileClip(self.video1_path)
            clip2 = VideoFileClip(self.video2_path)
            final_clip = concatenate_videoclips([clip1, clip2])
            final_clip.write_videofile(save_path, codec="libx264", audio_codec="aac")
            clip1.close()
            clip2.close()
            messagebox.showinfo("Success", f"Video saved successfully at {save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to join videos: {e}")

# Lancer l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = VideoJoinerApp(root)
    root.mainloop()
