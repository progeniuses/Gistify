import srt
from openai import OpenAI

class SubtitleAnalyzer:
    def __init__(self, subtitle_file="subtitles.srt"):
        self.subtitle_file = subtitle_file
        self.analysis_file = "analysis.txt"
        self.openai_client = OpenAI(api_key="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")

    def read_subtitles(self):
        with open(self.subtitle_file, "r", encoding="utf-8") as f:
            subtitles = list(srt.parse(f))
        return " ".join(subtitle.content for subtitle in subtitles)

    def analyze_subtitles(self):
        text = self.read_subtitles()
        analysis_prompt = f"""
        This text is from the subtitles of an educational video in English. Analyze the content, provide a detailed explanation of its main ideas, and expand on the key concepts. Then, write a concise summary of the video's overall content. Finally, generate 3-5 questions suitable for educational purposes based on the content.

        Text: "{text}"

        Provide your response in the following format:
        1. Detailed Analysis and Explanation: [Detailed explanation of the content and key concepts]
        2. Summary: [A concise summary of the video's overall content]
        3. Questions:
           - Question 1
           - Question 2
           - Question 3
        """
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an assistant that analyzes educational content and generates questions."},
                    {"role": "user", "content": analysis_prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI tahlilida xato: {e}")

    def save_analysis(self):
        analysis_result = self.analyze_subtitles()
        with open(self.analysis_file, "w", encoding="utf-8") as f:
            f.write(analysis_result)
        return self.analysis_file