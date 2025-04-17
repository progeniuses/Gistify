import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import threading
from video_processor import VideoProcessor
from subtitle_analyzer import SubtitleAnalyzer
from translator import Translator
from voice_generator import VoiceGenerator
from video_creator import VideoCreator
from PIL import Image, ImageTk
import vlc

class VideoProcessingApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Video Magic Studio")
        self.geometry("1100x700")
        ctk.set_appearance_mode("system")
        self.configure(fg_color="#2C2C2C")  # Umumiy fon qora

        # VLC yo'lini aniqlash
        try:
            self.instance = vlc.Instance()
        except AttributeError:
            messagebox.showerror("Xato", "VLC Media Player o'rnatilmagan yoki yo'nalishi noto'g'ri! Iltimos, VLC o'rnating va qayta urining.")
            self.destroy()
            return

        # Asosiy oyna ikkiga bo'linadi: chap (20%) va o'ng (80%)
        self.grid_columnconfigure(0, weight=2)  # Chap 20%
        self.grid_columnconfigure(1, weight=8)  # O'ng 80%
        self.grid_rowconfigure(0, weight=1)

        # Chap panel (ko'k)
        self.left_frame = ctk.CTkFrame(self, fg_color="#3498DB", corner_radius=0)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.left_frame.grid_rowconfigure(0, weight=1)  # Logotip
        self.left_frame.grid_rowconfigure(1, weight=1)  # Inputlar
        self.left_frame.grid_rowconfigure(2, weight=1)  # Tugma

        # Logotip (D:\my_coding\PycharmProjects\Gistify\logo yo'lidan yuklanadi, chap panelga mos o'lchamda)
        logo_path = r"D:\my_coding\PycharmProjects\Gistify\logo\logo.jpg"
        if os.path.exists(logo_path):
            logo_image = Image.open(logo_path)
            # Chap panelning kengligiga mos ravishda o'lcham (200x100)
            logo_image = logo_image.resize((200, 120), Image.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_image)
            self.logo_label = ctk.CTkLabel(self.left_frame, image=self.logo_photo, text="")
            self.logo_label.pack(pady=10, padx=10, anchor="w")  # Chap tomoniga joylashtirish
        else:
            self.logo_label = ctk.CTkLabel(self.left_frame, text="Video Magic", font=("Helvetica", 20, "bold"), text_color="white")
            self.logo_label.pack(pady=10, padx=10, anchor="w")  # Chap tomoniga joylashtirish

        # Input elementlari (chap panelda)
        self.input_container = ctk.CTkFrame(self.left_frame, fg_color="#3498DB")
        self.input_container.pack(fill="both", expand=True, padx=5, pady=5)

        self.upload_frame = ctk.CTkFrame(self.input_container, fg_color="#3498DB")
        self.upload_frame.pack(fill="x", pady=5)
        self.upload_label = ctk.CTkLabel(self.upload_frame, text="Yuklash:", text_color="white")
        self.upload_label.pack(side="left", padx=5)
        self.video_path_var = tk.StringVar()
        self.video_entry = ctk.CTkEntry(self.upload_frame, textvariable=self.video_path_var, width=120, fg_color="#4A4A4A", border_color="white")
        self.video_entry.pack(side="left", padx=5)
        self.browse_button = ctk.CTkButton(self.upload_frame, text="Browse", width=60, command=self.browse_video, fg_color="#F39C12", hover_color="#E67E22", text_color="white")
        self.browse_button.pack(side="left", padx=5)

        self.youtube_frame = ctk.CTkFrame(self.input_container, fg_color="#3498DB")
        self.youtube_frame.pack(fill="x", pady=5)
        self.youtube_label = ctk.CTkLabel(self.youtube_frame, text="YouTube:", text_color="white")
        self.youtube_label.pack(side="left", padx=5)
        self.youtube_url_var = tk.StringVar()
        self.youtube_entry = ctk.CTkEntry(self.youtube_frame, textvariable=self.youtube_url_var, width=120, fg_color="#4A4A4A", border_color="white")
        self.youtube_entry.pack(side="left", padx=5)

        # Generate tugmasi (ko'k fonda)
        self.generate_button = ctk.CTkButton(self.input_container, text="Generate", command=self.start_processing, fg_color="#F39C12", hover_color="#E67E22", text_color="white", corner_radius=10)
        self.generate_button.pack(pady=10)

        # O'ng panel (qora)
        self.right_frame = ctk.CTkFrame(self, fg_color="#2C2C2C")
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.right_frame.grid_rowconfigure(0, weight=1)  # Tugmalar
        self.right_frame.grid_rowconfigure(1, weight=8)  # Video
        self.right_frame.grid_rowconfigure(2, weight=1)  # Tahlil
        self.right_frame.grid_columnconfigure(0, weight=1)

        # Yuqori tugmalar (o'ng panelda)
        self.button_frame = ctk.CTkFrame(self.right_frame, fg_color="#2C2C2C")
        self.button_frame.pack(fill="x", pady=5)
        self.play_button = ctk.CTkButton(self.button_frame, text="▶", width=40, fg_color="#3498DB", hover_color="#2980B9", command=self.play_video, state="disabled")
        self.play_button.pack(side="right", padx=5)
        self.download_button = ctk.CTkButton(self.button_frame, text="Download", width=100, fg_color="#3498DB", hover_color="#2980B9", command=self.save_result, state="disabled")
        self.download_button.pack(side="right", padx=5)

        # Video ko'rish maydoni
        self.video_frame = ctk.CTkFrame(self.right_frame, fg_color="#1C1C1C", border_width=2, border_color="white")
        self.video_frame.pack(fill="both", expand=True, pady=10, padx=10)
        self.video_label = ctk.CTkLabel(self.video_frame, text="Video bu yerda ko'rinadi", text_color="white", font=("Arial", 14))
        self.video_label.pack(expand=True)
        self.video_player = None  # VLC uchun o'zgaruvchi

        # Tahlil qismi
        self.analysis_frame = ctk.CTkFrame(self.right_frame, fg_color="#3C3C3C", border_width=2, border_color="white")
        self.analysis_frame.pack(fill="both", expand=True, pady=10, padx=10)
        self.analysis_label = ctk.CTkLabel(self.analysis_frame, text="Tahlil natijasi:", text_color="white")
        self.analysis_label.pack(anchor="w", padx=5)
        self.analysis_text = ctk.CTkTextbox(self.analysis_frame, height=80, fg_color="#4A4A4A", border_color="white")
        self.analysis_text.pack(fill="both", expand=True, padx=5, pady=5)

    def browse_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.mov *.avi")])
        if file_path:
            self.video_path_var.set(file_path)
            self.youtube_url_var.set("")

    def save_result(self):
        if hasattr(self, 'result_video_path_var') and self.result_video_path_var.get():
            output_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
            if output_path:
                os.rename(self.result_video_path_var.get(), output_path)
                self.result_video_path_var.set(output_path)
                messagebox.showinfo("Muvaffaqiyat", f"Video {output_path} ga saqlandi!")

    def play_video(self):
        if hasattr(self, 'result_video_path_var') and self.result_video_path_var.get():
            if self.video_player:
                self.video_player.stop()
            self.video_player = self.instance.media_player_new()
            media = self.instance.media_new(self.result_video_path_var.get())
            self.video_player.set_media(media)
            self.video_player.set_hwnd(self.video_frame.winfo_id())  # Windows uchun
            self.video_player.play()
            self.video_label.configure(text="Video o'ynatilmoqda...")

    def process_pipeline(self):
        video_path = self.video_path_var.get() or None
        youtube_url = self.youtube_url_var.get() or None
        output_path = "output_video.mp4"
        self.result_video_path_var = tk.StringVar(value=output_path)

        if not video_path and not youtube_url:
            messagebox.showerror("Xato", "Iltimos, video faylni tanlang yoki YouTube URL kiriting!")
            return

        self.generate_button.configure(state="disabled")

        try:
            processor = VideoProcessor(video_path, youtube_url)
            processor.extract_and_transcribe()

            analyzer = SubtitleAnalyzer()
            analyzer.save_analysis()

            translator = Translator()
            translator.translate_analysis()
            translated_subtitle_file = translator.translate_subtitles()
            with open("analysis_uz.txt", "r", encoding="utf-8") as f:
                analysis_text = f.read()
            self.analysis_text.delete("0.0", tk.END)
            self.analysis_text.insert("0.0", analysis_text)

            voice_generator = VoiceGenerator()
            voice_generator.generate_voiceover()

            video_creator = VideoCreator(video_path, translated_subtitle_file, "voiceovers", output_path)
            video_creator.create_video()
            self.result_video_path_var.set(output_path)

            # Video avtomatik o'ynatiladi
            self.play_video()

            self.download_button.configure(state="normal")
            self.play_button.configure(state="normal")
            messagebox.showinfo("Muvaffaqiyat", "Jarayon tugadi!")

        except Exception as e:
            messagebox.showerror("Xato", f"Jarayon xatosi: {e}")
        finally:
            self.generate_button.configure(state="normal")

    def start_processing(self):
        thread = threading.Thread(target=self.process_pipeline)
        thread.start()

if __name__ == "__main__":
    app = VideoProcessingApp()
    app.mainloop()