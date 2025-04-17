import srt
from openai import OpenAI
from deep_translator import GoogleTranslator


class Translator:
    def __init__(self, analysis_file="analysis.txt", subtitle_file="subtitles.srt"):
        self.analysis_file = analysis_file
        self.subtitle_file = subtitle_file
        self.translated_analysis_file = "analysis_uz.txt"
        self.translated_subtitle_file = "subtitles_uz.srt"
        self.openai_client = OpenAI(
            api_key="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")

    def translate_to_uzbek_text(self, text):
        try:
            translator = GoogleTranslator(source='en', target='uz')
            return translator.translate(text)
        except Exception as e:
            raise Exception(f"Tarjima qilishda xato: {e}")

    def translate_analysis(self):
        with open(self.analysis_file, "r", encoding="utf-8") as f:
            analysis_text = f.read()
        translated_text = self.translate_to_uzbek_text(analysis_text)
        with open(self.translated_analysis_file, "w", encoding="utf-8") as f:
            f.write(translated_text)
        return self.translated_analysis_file

    def translate_subtitles(self):
        with open(self.subtitle_file, "r", encoding="utf-8") as f:
            subtitles = list(srt.parse(f))
        for subtitle in subtitles:
            translation_prompt = f"""
            Siz ingliz tilidan o‘zbek tiliga subtitrlar uchun tarjima qiluvchi mutaxassisiz. Quyidagi inglizcha matnni tabiiy, o‘zbek tiliga mos va ma’noli tarzda tarjima qiling. Tarjima quyidagi talablarga javob berishi kerak:
            - Matnning ma’nosi, ohangi va konteksti saqlansin.
            - So‘zma-so‘z tarjimadan qoching, o‘zbek tilidagi muqobil iboralarni ishlating.
            - Subtitrlar uchun qisqa va o‘qilishi oson bo‘lsin.
            - Ingliz tilidagi idiomalar yoki madaniy iboralarni o‘zbek tiliga moslashtiring.

            Tarjima qilinadigan matn: "{subtitle.content}"

            Faqat o‘zbek tilidagi tarjima matnni qaytaring.
            """
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system",
                         "content": "Siz ingliz tilidan o‘zbek tiliga subtitrlar uchun tarjima qiluvchi mutaxassisiz."},
                        {"role": "user", "content": translation_prompt}
                    ],
                    max_tokens=200,
                    temperature=0.7
                )
                subtitle.content = response.choices[0].message.content.strip()
            except Exception as e:
                raise Exception(f"Tarjima qilishda xato: {e}")

        with open(self.translated_subtitle_file, "w", encoding="utf-8") as f:
            f.write(srt.compose(subtitles))
        return self.translated_subtitle_file