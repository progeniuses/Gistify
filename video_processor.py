import os
import subprocess
from pytube import YouTube

class VideoProcessor:
    def __init__(self, video_path=None, youtube_url=None):
        self.video_path = video_path
        self.youtube_url = youtube_url
        self.subtitle_file = "subtitles.srt"

    def download_youtube_video(self):
        if not self.youtube_url:
            raise ValueError("YouTube URL kiritilmadi!")
        try:
            yt = YouTube(self.youtube_url)
            stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            self.video_path = stream.download(filename="downloaded_video.mp4")
            print("YouTube videosi muvaffaqiyatli yuklandi.")
            return self.video_path
        except Exception as e:
            raise Exception(f"YouTube yuklashda xato: {e}")

    def extract_and_transcribe(self):
        if not self.video_path:
            raise ValueError("Video fayli yoki YouTube URL kiritilmadi!")
        if self.youtube_url:
            self.video_path = self.download_youtube_video()

        audio_file = "temp_audio.mp3"
        if os.path.exists(self.subtitle_file):
            print(f"Subtitr fayli allaqachon mavjud: {self.subtitle_file}")
            return True

        try:
            subprocess.run([
                r"C:\ProgramData\chocolatey\bin\ffmpeg.exe",
                "-i", self.video_path,
                "-vn",
                "-acodec", "mp3",
                "-ar", "16000",
                "-ac", "1",
                "-b:a", "32k",
                "-loglevel", "quiet",
                audio_file,
            ], check=True)
            print("Audio muvaffaqiyatli chiqarildi.")
        except subprocess.CalledProcessError as e:
            raise Exception(f"ffmpeg bilan audio chiqarishda xato: {e}")

        import assemblyai as aai
        aai.settings.api_key = "194a15ad0acf4bc4b8259fe4645144ae"
        config = aai.TranscriptionConfig(language_code="en", punctuate=True, format_text=True)
        transcriber = aai.Transcriber()
        try:
            transcript = transcriber.transcribe(audio_file, config=config)
            if transcript.status == aai.TranscriptStatus.error:
                raise Exception(f"Transkripsiya xatosi: {transcript.error}")
            print("Transkripsiya muvaffaqiyatli yakunlandi.")
        except Exception as e:
            raise Exception(f"AssemblyAI transkripsiyasida xato: {e}")

        with open(self.subtitle_file, "w", encoding="utf-8") as f:
            f.write(transcript.export_subtitles_srt())

        if os.path.exists(audio_file):
            os.remove(audio_file)
            print("Vaqtinchalik audio fayl o‘chirildi.")

        return True