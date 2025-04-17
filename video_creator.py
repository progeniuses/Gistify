import os
import subprocess
import tempfile
import glob
import srt  # srt modulini import qildik

class VideoCreator:
    def __init__(self, video_path, subtitles_path, voiceover_dir, output_path):
        self.video_path = video_path
        self.subtitles_path = subtitles_path
        self.voiceover_dir = voiceover_dir
        self.output_path = output_path
        self.ffmpeg_path = r"C:\ProgramData\chocolatey\bin\ffmpeg.exe"
        self.ffprobe_path = r"C:\ProgramData\chocolatey\bin\ffprobe.exe"

    def get_audio_duration(self, audio_path):
        cmd = [self.ffprobe_path, "-v", "error", "-show_entries", "format=duration",
               "-of", "default=noprint_wrappers=1:nokey=1", audio_path]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(result.stdout.strip())

    def get_video_duration(self, video_path):
        cmd = [self.ffprobe_path, "-v", "error", "-show_entries", "format=duration",
               "-of", "default=noprint_wrappers=1:nokey=1", video_path]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(result.stdout.strip())

    def create_video(self):
        with open(self.subtitles_path, "r", encoding="utf-8") as f:
            subtitles = list(srt.parse(f))

        voiceover_files = sorted(glob.glob(os.path.join(self.voiceover_dir, "voiceover_*.mp3")))
        if len(voiceover_files) != len(subtitles):
            raise ValueError(f"Ovozli fayllar soni ({len(voiceover_files)}) subtitrlar soniga ({len(subtitles)}) mos kelmaydi!")

        voiceover_durations = []
        for voiceover_path in voiceover_files:
            duration = self.get_audio_duration(voiceover_path)
            voiceover_durations.append((voiceover_path, duration))

        voiceover_data = []
        for idx, (voiceover_path, duration) in enumerate(voiceover_durations):
            start_time = subtitles[idx].start.total_seconds()
            end_time = subtitles[idx].end.total_seconds()
            subtitr_duration = end_time - start_time
            if duration > subtitr_duration:
                duration = subtitr_duration
            voiceover_data.append((voiceover_path, start_time, duration))

        video_duration = self.get_video_duration(self.video_path)

        combined_audio_path = "combined_audio.mp3"
        with tempfile.TemporaryDirectory() as temp_dir:
            concat_file_path = os.path.join(temp_dir, "concat_list.txt")
            with open(concat_file_path, "w") as concat_file:
                last_end_time = 0
                for idx, (voiceover_path, start_time, duration) in enumerate(voiceover_data):
                    temp_audio_path = os.path.join(temp_dir, f"temp_{idx}.mp3")
                    if start_time > last_end_time:
                        silence_duration = start_time - last_end_time
                        silence_path = os.path.join(temp_dir, f"silence_{idx}.mp3")
                        subprocess.run([
                            self.ffmpeg_path, "-y", "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=mono",
                            "-t", str(silence_duration), silence_path
                        ], check=True)
                        concat_file.write(f"file '{silence_path}'\n")
                    subprocess.run([
                        self.ffmpeg_path, "-y", "-i", voiceover_path,
                        "-t", str(duration), temp_audio_path
                    ], check=True)
                    concat_file.write(f"file '{temp_audio_path}'\n")
                    last_end_time = start_time + duration

            subprocess.run([
                self.ffmpeg_path, "-y", "-f", "concat", "-safe", "0",
                "-i", concat_file_path, "-c:a", "mp3", combined_audio_path
            ], check=True)

        subprocess.run([
            self.ffmpeg_path, "-y", "-i", self.video_path, "-i", combined_audio_path,
            "-vf", f"subtitles={self.subtitles_path}:force_style='Fontsize=24,PrimaryColour=&H00FFFFFF&,BackColour=&H80000000&'",
            "-map", "0:v:0", "-map", "1:a:0", "-c:v", "libx264", "-c:a", "aac",
            self.output_path
        ], check=True)

        print(f"Video muvaffaqiyatli yaratildi: {self.output_path}")
        if os.path.exists(combined_audio_path):
            os.remove(combined_audio_path)