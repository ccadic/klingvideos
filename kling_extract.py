import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import simpledialog
from PIL import Image, ImageTk

class VideoFrameExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Frame Extractor")

        # Variables pour la vidéo et les frames
        self.video_path = None
        self.first_frame = None
        self.last_frame = None

        # Bouton pour sélectionner une vidéo
        self.select_button = tk.Button(root, text="Select Video", command=self.select_video)
        self.select_button.pack(pady=10)

        # Canvas pour afficher les images
        self.first_frame_canvas = tk.Label(root, text="First Frame")
        self.first_frame_canvas.pack(pady=10)

        self.last_frame_canvas = tk.Label(root, text="Last Frame")
        self.last_frame_canvas.pack(pady=10)

        # Bouton pour sauvegarder la dernière image
        self.save_button = tk.Button(root, text="Save Last Frame", command=self.save_last_frame, state=tk.DISABLED)
        self.save_button.pack(pady=10)

    def select_video(self):
        # Ouvrir le dialogue pour sélectionner une vidéo
        self.video_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")])
        if not self.video_path:
            return

        # Charger la vidéo et extraire les frames
        cap = cv2.VideoCapture(self.video_path)

        if not cap.isOpened():
            messagebox.showerror("Error", "Unable to open video file.")
            return

        # Lire la première frame
        ret, first_frame = cap.read()
        if ret:
            self.first_frame = cv2.cvtColor(first_frame, cv2.COLOR_BGR2RGB)
            self.display_image(self.first_frame, self.first_frame_canvas)
        else:
            messagebox.showerror("Error", "Unable to read the first frame.")

        # Aller au dernier frame
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames - 1)

        # Lire le dernier frame
        ret, last_frame = cap.read()
        if ret:
            self.last_frame = cv2.cvtColor(last_frame, cv2.COLOR_BGR2RGB)
            self.display_image(self.last_frame, self.last_frame_canvas)
        else:
            messagebox.showerror("Error", "Unable to read the last frame.")

        # Activer le bouton "Save" si les frames sont chargées
        self.save_button.config(state=tk.NORMAL if self.last_frame is not None else tk.DISABLED)

        # Libérer la vidéo
        cap.release()

    def display_image(self, frame, canvas):
        # Convertir l'image en format compatible Tkinter
        image = Image.fromarray(frame)
        image = image.resize((300, 200))  # Redimensionner pour l'affichage
        photo = ImageTk.PhotoImage(image)

        # Mettre à jour le canvas avec l'image
        canvas.config(image=photo)
        canvas.image = photo

    def save_last_frame(self):
        if self.last_frame is None:
            messagebox.showerror("Error", "No last frame to save.")
            return

        # Ouvrir un dialogue pour choisir le fichier de sauvegarde
        save_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")]
        )
        if not save_path:
            return

        # Sauvegarder l'image
        try:
            image = Image.fromarray(self.last_frame)
            image.save(save_path)
            messagebox.showinfo("Success", f"Image saved successfully at {save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image: {e}")

# Lancer l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = VideoFrameExtractorApp(root)
    root.mainloop()
