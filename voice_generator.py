import os
import requests
import time
import srt  # srt modulini import qildik

class VoiceGenerator:
    def __init__(self, subtitle_file="subtitles_uz.srt", output_dir="voiceovers"):
        self.subtitle_file = subtitle_file
        self.output_dir = output_dir

    def generate_voiceover(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        with open(self.subtitle_file, "r", encoding="utf-8") as f:
            subtitles = list(srt.parse(f))

        url = f"https://api.elevenlabs.io/v1/text-to-speech/xnLd1PNITY1Y4iALLfii"
        headers = {
            "xi-api-key": "sk_4eced4646b049c8fffb1a2bd9f14c4d486466a4f426eb322",
            "Content-Type": "application/json"
        }

        for idx, subtitle in enumerate(subtitles):
            text = subtitle.content
            payload = {
                "text": text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.75,
                    "similarity_boost": 0.85,
                    "style": 0.6
                }
            }

            try:
                response = requests.post(url, json=payload, headers=headers)
                response.raise_for_status()
                audio_path = os.path.join(self.output_dir, f"voiceover_{idx + 1}.mp3")
                with open(audio_path, "wb") as audio_file:
                    audio_file.write(response.content)
                print(f"Ovozli fayl yaratildi: {audio_path}")
                time.sleep(2)
            except Exception as e:
                print(f"Ovozlashtirishda xato (subtitr {idx + 1}): {e}")