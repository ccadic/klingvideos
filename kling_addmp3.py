import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip

class AudioVideoMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio-Video Merger")

        # Variables pour les fichiers sélectionnés
        self.video_path = None
        self.audio_path = None

        # Option pour écraser ou mixer le son
        self.replace_audio = tk.BooleanVar(value=True)

        # Boutons pour sélectionner les fichiers vidéo et audio
        self.select_video_button = tk.Button(root, text="Select Video (MP4)", command=self.select_video)
        self.select_video_button.pack(pady=10)

        self.select_audio_button = tk.Button(root, text="Select Audio (MP3)", command=self.select_audio, state=tk.DISABLED)
        self.select_audio_button.pack(pady=10)

        # Case à cocher pour choisir l'option d'écrasement du son
        self.replace_audio_checkbox = tk.Checkbutton(
            root, text="Replace existing audio with MP3", variable=self.replace_audio
        )
        self.replace_audio_checkbox.pack(pady=10)

        # Bouton pour coller la bande son et sauvegarder la vidéo
        self.merge_button = tk.Button(root, text="Merge Audio and Video", command=self.merge_files, state=tk.DISABLED)
        self.merge_button.pack(pady=10)

    def select_video(self):
        # Sélectionner une vidéo MP4
        self.video_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
        if self.video_path:
            messagebox.showinfo("Video Selected", f"Selected video:\n{self.video_path}")
            self.select_audio_button.config(state=tk.NORMAL)

    def select_audio(self):
        # Sélectionner un fichier audio MP3
        self.audio_path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
        if self.audio_path:
            messagebox.showinfo("Audio Selected", f"Selected audio:\n{self.audio_path}")
            self.merge_button.config(state=tk.NORMAL)

    def merge_files(self):
        if not self.video_path or not self.audio_path:
            messagebox.showerror("Error", "Please select both video and audio files.")
            return

        # Choisir le fichier de sortie
        save_path = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[("MP4 files", "*.mp4")]
        )
        if not save_path:
            return

        try:
            # Charger la vidéo et l'audio
            video_clip = VideoFileClip(self.video_path)
            new_audio = AudioFileClip(self.audio_path)

            if self.replace_audio.get():
                # Option : Remplacer complètement l'audio existant
                final_audio = new_audio
            else:
                # Option : Mixer l'audio existant avec le nouvel audio
                original_audio = video_clip.audio
                final_audio = CompositeAudioClip([original_audio, new_audio])

            # Ajouter l'audio final à la vidéo
            video_with_audio = video_clip.set_audio(final_audio)
            video_with_audio.write_videofile(save_path, codec="libx264", audio_codec="aac")

            # Libérer les ressources
            video_clip.close()
            new_audio.close()
            if not self.replace_audio.get():
                original_audio.close()

            messagebox.showinfo("Success", f"Video saved successfully at:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

# Lancer l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = AudioVideoMergerApp(root)
    root.mainloop()
