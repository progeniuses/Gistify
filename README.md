# Gistify - Hackathon 2025

## Loyiha haqida

### Umumiy tavsif
**Gistify** — bu YouTube yoki mahalliy videolarni avtomatik qayta ishlash, ulardan subtitrlar chiqarish, o‘zbek tiliga tarjima qilish, ta’limiy tahlil qilish va ovozli qo‘shilgan yangi video yaratish imkonini beruvchi innovatsion vosita. Ushbu loyiha Hackathon 2025 uchun ishlab chiqildi va ta’lim sohasida raqamli kontentni mahalliylashtirish va foydalanuvchilar uchun qulayroq qilish maqsadiga xizmat qiladi.

### Qanday muammoga yechim beradi?
Bugungi kunda ta’limiy videolar (masalan, YouTube’dagi darslar, kurslar) ko‘pincha ingliz tilida bo‘lib, o‘zbek tilida so‘zlashuvchi auditoriya uchun foydalanish qiyin bo‘ladi. Quyidagi muammolar mavjud:
- **Til to‘siqlari**: O‘zbek tilida so‘zlashuvchilar ingliz tilidagi kontentni tushunishda qiynaladi, chunki avtomatik subtitrlar ko‘pincha noaniq yoki noto‘g‘ri bo‘ladi.
- **Subtitr sifati**: Mavjud vositalar (masalan, YouTube Auto Subtitles) kontekstga mos va aniq tarjimalar taqdim eta olmaydi.
- **Mahalliylashtirishning yo‘qligi**: O‘zbek tiliga sifatli tarjima qilingan ta’limiy kontent kam, bu esa o‘quvchilarning bilim olish imkoniyatlarini cheklaydi.
- **Tahlil va qo‘shimcha resurslar**: Ta’limiy videolarga asoslangan qo‘shimcha materiallar (savollar, tahlillar) yaratish qo‘lda bajariladi va ko‘p vaqt talab qiladi.
- **Foydalanuvchi tajribasi**: Mavjud vositalar foydalanuvchilarga bir platformada video qayta ishlash, tarjima va tahlil qilish imkonini bermaydi.

**Gistify** ushbu muammolarni hal qiladi:
- Videodan avtomatik ravishda aniq subtitrlar chiqaradi (AssemblyAI yordamida).
- Subtitrlar va tahlil matnlarini o‘zbek tiliga tabiiy va kontekstga mos tarzda tarjima qiladi (OpenAI va Google Translator).
- Ta’limiy kontentni tahlil qilib, o‘quvchilar uchun savollar va qisqacha xulosalar ishlab chiqaradi.
- Tarjima qilingan subtitrlarga mos ovozli qo‘shilgan yangi video yaratadi, bu esa kontentni yanada qulay qiladi.
- CustomTkinter asosidagi intuitiv grafik interfeys orqali barcha jarayonlarni bitta platformada birlashtiradi.

### Dolzarbligi
Ta’lim sohasida raqamli kontentning o‘sishi bilan mahalliylashtirish va qulay foydalanuvchi tajribasi dolzarb muammoga aylandi. O‘zbekistonda:
- **Ta’lim platformalari**: O‘zbek tilida sifatli ta’limiy resurslar yetishmaydi, ayniqsa onlayn kurslar va videolar sohasida.
- **Global raqobat**: Xalqaro ta’lim platformalari (Coursera, Khan Academy) ingliz tilida bo‘lib, mahalliy foydalanuvchilar uchun moslashtirish talab qilinadi.
- **Texnologik rivojlanish**: AI va avtomatlashtirish vositalari yordamida kontentni mahalliylashtirish jarayonini tezlashtirish mumkin, bu esa ta’limni ommalashtirishga yordam beradi.
Gistify ushbu ehtiyojlarga javob beradi, chunki u o‘zbek tilidagi ta’limiy kontentni yaratish jarayonini soddalashtiradi va sifatni oshiradi.

### Noyobligi
Gistify’ning noyob xususiyatlari uni boshqa vositalardan ajratib turadi:
- **Birlashtirilgan yechim**: Video yuklash, subtitr yaratish, tarjima, tahlil va ovozli video ishlab chiqarishni bir platformada amalga oshiradi.
- **O‘zbek tiliga moslashuv**: OpenAI va Google Translator yordamida tabiiy va kontekstga mos o‘zbek tilidagi tarjimalarni taqdim etadi.
- **Ta’limiy tahlil**: Subtitrlar asosida avtomatik ravishda savollar va tahlillar ishlab chiqaradi, bu o‘quvchilar va o‘qituvchilar uchun qo‘shimcha resurslar beradi.
- **Foydalanuvchi interfeysi**: CustomTkinter asosidagi zamonaviy va qulay interfeys foydalanuvchilarga jarayonni soddalashtiradi.
- **Moslashuvchanlik**: Mahalliy video fayllar va YouTube videolarini qo‘llab-quvvatlaydi, bu esa foydalanish doirasini kengaytiradi.

### Kod qanday ishlaydi?
Gistify loyihasi modulli tuzilishga ega bo‘lib, har bir komponent alohida vazifani bajaradi. Quyida asosiy jarayon va kodning ishlash mexanizmi:

1. **Video yuklash (`video_processor.py`)**:
   - **Funksiya**: YouTube videolarini yuklaydi (`pytube`) yoki mahalliy video faylni qabul qiladi.
   - **Jarayon**: YouTube URL yoki mahalliy fayl yo‘lini oladi, agar URL bo‘lsa, yuqori sifatli videoni yuklaydi.
   - **Chiqish**: `downloaded_video.mp4` fayli.

2. **Subtitr yaratish (`video_processor.py`)**:
   - **Funksiya**: Videodan audio chiqaradi (`ffmpeg`) va AssemblyAI yordamida subtitrlar yaratadi.
   - **Jarayon**: Video fayldan MP3 formatida audio chiqariladi, so‘ng AssemblyAI API orqali ingliz tilida transkripsiya qilinadi va `.srt` formatida subtitrlar saqlanadi.
   - **Chiqish**: `subtitles.srt` fayli.

3. **Tahlil qilish (`subtitle_analyzer.py`)**:
   - **Funksiya**: Subtitrlar matnini tahlil qiladi va ta’limiy savollar ishlab chiqaradi (`openai`).
   - **Jarayon**: Subtitrlar matni OpenAI GPT-4o-mini modeliga yuboriladi, unda asosiy g‘oyalar tahlil qilinadi, xulosa chiqariladi va 3-5 ta savol ishlab chiqariladi.
   - **Chiqish**: `analysis.txt` fayli.

4. **Tarjima (`translator.py`)**:
   - **Funksiya**: Subtitrlar va tahlil matnini o‘zbek tiliga tarjima qiladi (`deep_translator` va `openai`).
   - **Jarayon**: Google Translator orqali tahlil matni, OpenAI orqali subtitrlar tabiiy o‘zbek tiliga tarjima qilinadi.
   - **Chiqish**: `subtitles_uz.srt` va `analysis_uz.txt` fayllari.

5. **Ovozli qo‘shish (`voice_generator.py`)**:
   - **Funksiya**: Tarjima qilingan subtitrlarga mos ovozli fayllar yaratadi.
   - **Jarayon**: (Siz bu faylni yubormagansiz, lekin taxminan matnni ovozga aylantiruvchi API, masalan, ElevenLabs yoki Google Text-to-Speech ishlatiladi). Har bir subtitr uchun alohida `.mp3` fayllari yaratiladi.
   - **Chiqish**: `voiceovers/voiceover_*.mp3` fayllari.

6. **Yangi video yaratish (`video_creator.py`)**:
   - **Funksiya**: Asl video, tarjima qilingan subtitrlar va ovozli fayllarni birlashtirib, yangi video ishlab chiqaradi (`ffmpeg`).
   - **Jarayon**: Ovozli fayllar subtitrlar vaqtlariga moslashtiriladi, sukunatlar qo‘shiladi, subtitrlar videoga joylashtiriladi va yakuniy video kodlanadi.
   - **Chiqish**: `output_video.mp4` fayli.

7. **Grafik interfeys (`main.py`)**:
   - **Funksiya**: Foydalanuvchilarga jarayonni boshqarish va natijalarni ko‘rish imkonini beradi (`customtkinter`, `python-vlc`).
   - **Jarayon**: Foydalanuvchi video faylni tanlaydi yoki YouTube URL kiritadi, “Generate” tugmasi bilan jarayon boshlanadi, natijalar (video va tahlil) interfeysda ko‘rsatiladi.
   - **Chiqish**: Foydalanuvchi yangi videoni ko‘radi va saqlay oladi.

**Umumiy ish oqimi**:
```
Video yuklash → Audio chiqarish → Subtitr yaratish → Tahlil qilish → Tarjima qilish → Ovozli fayllar yaratish → Yangi video ishlab chiqarish → Interfeysda ko‘rsatish
```

### Raqobatchilar va afzalliklar
Gistify’ning raqobatchilarini va ulardan afzalliklarini quyidagicha taqqoslash mumkin:

1. **YouTube Auto Subtitles**:
   - **Tavsif**: YouTube videolariga avtomatik subtitrlar qo‘shadi.
   - **Kamchiliklari**:
     - Subtitrlar sifati past, ko‘pincha noaniq.
     - O‘zbek tiliga tarjima qilish imkoni yo‘q.
     - Tahlil yoki ovozli qo‘shish funksiyasi yo‘q.
   - **Gistify afzalliklari**: Aniq subtitrlar, o‘zbek tiliga sifatli tarjima, tahlil va ovozli video yaratish.

2. **Adobe Premiere Pro (Subtitr va video tahrirlash)**:
   - **Tavsif**: Professional video tahrirlash dasturi, subtitrlar qo‘shish imkonini beradi.
   - **Kamchiliklari**:
     - Qo‘lda subtitr yaratish va sinxronlashtirish talab qilinadi.
     - Tarjima va tahlil funksiyalari yo‘q.
     - Foydalanish murakkab va pullik.
   - **Gistify afzalliklari**: Avtomatlashtirilgan jarayon, o‘zbek tiliga moslashuv, bepul va foydalanuvchi uchun qulay.

3. **Sonix yoki Otter.ai (Transkripsiya vositalari)**:
   - **Tavsif**: Audio va videolardan transkripsiya qilish uchun AI vositalari.
   - **Kamchiliklari**:
     - O‘zbek tilini qo‘llab-quvvatlamaydi.
     - Video tahrirlash yoki ovozli qo‘shish imkoni yo‘q.
     - Faqat transkripsiya bilan cheklanadi.
   - **Gistify afzalliklari**: To‘liq yechim (transkripsiya, tarjima, tahlil, video yaratish), o‘zbek tiliga moslashuv.

4. **Descript**:
   - **Tavsif**: Audio va video tahrirlash, transkripsiya va ovozli sintez uchun vosita.
   - **Kamchiliklari**:
     - O‘zbek tiliga tarjima qilish imkoni cheklangan.
     - Pullik va resurs talab qiladi.
     - Ta’limiy tahlil funksiyasi yo‘q.
   - **Gistify afzalliklari**: O‘zbek tiliga moslashuv, ta’limiy tahlil, bepul va ochiq manbali.

**Gistify’ning umumiy afzalligi**: U barcha jarayonlarni (yuklash, transkripsiya, tarjima, tahlil, ovozli qo‘shish, video yaratish) bir platformada birlashtiradi, o‘zbek tiliga moslashuvchan va ta’lim sohasiga yo‘naltirilgan.

### Xususiyatlar
- YouTube’dan yuqori sifatli video yuklash.
- AssemblyAI yordamida aniq subtitrlar yaratish.
- OpenAI va Google Translator orqali o‘zbek tiliga tabiiy tarjima.
- Subtitrlar asosida ta’limiy tahlil va savollar ishlab chiqarish.
- Tarjima qilingan subtitrlarga mos ovozli fayllar qo‘shish.
- CustomTkinter asosidagi zamonaviy grafik interfeys.
- VLC Media Player yordamida natijalarni ko‘rish.

## Texnologiyalar
- **Dasturlash tili**: Python 3.10+
- **Kutubxonalar**:
  - `pytube`: YouTube videolarini yuklash
  - `assemblyai`: Subtitrlar yaratish
  - `openai`: Tarjima va tahlil
  - `deep-translator`: Matnli tarjima
  - `srt`: Subtitr fayllarini boshqarish
  - `customtkinter`, `Pillow`: Grafik interfeys
  - `python-vlc`: Video o‘ynatish
- **Tashqi vositalar**:
  - `ffmpeg`: Audio va video qayta ishlash
  - `VLC Media Player`: Video ko‘rish

## O‘rnatish va ishga tushirish
### Talablar
- Python 3.10 yoki undan yuqori
- [ffmpeg](https://ffmpeg.org/download.html) o‘rnatilgan bo‘lishi kerak
- [VLC Media Player](https://www.videolan.org/vlc/) o‘rnatilgan bo‘lishi kerak

### O‘rnatish qadamlari
1. Repozitoriyni klonlang:
   ```bash
   git clone https://github.com/username/Gistify.git
   cd Gistify
   ```
2. Virtual muhit yarating va faollashtiring:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows uchun: venv\Scripts\activate
   ```
3. Kerakli kutubxonalarni o‘rnating:
   ```bash
   pip install -r requirements.txt
   ```
4. `ffmpeg` va `VLC Media Player` ni o‘rnating:
   - Windows uchun: [Chocolatey](https://chocolatey.org/) orqali:
     ```bash
     choco install ffmpeg
     choco install vlc
     ```
5. API kalitlarini sozlang:
   - `.env` faylida AssemblyAI va OpenAI kalitlarini qo‘shing (qarang: `.env.example`).
6. Loyihani ishga tushiring:
   ```bash
   python main.py
   ```

## Foydalanish
1. **Video yuklash**:
   - Mahalliy video faylni tanlang (`.mp4`, `.mov`, `.avi`) yoki YouTube URL’ni kiriting.
2. **Generate tugmasi**:
   - Videoni qayta ishlash, subtitrlar yaratish, tarjima qilish, tahlil qilish va yangi video yaratish jarayonini boshlaydi.
3. **Natija**:
   - Yangi video avtomatik o‘ynatiladi va tahlil natijasi interfeysdagi matn maydonida ko‘rsatiladi.
   - Videoni saqlash uchun **Download** tugmasidan foydalaning.

## Demo
![Interfeys skrinshoti](screenshots/interface.png)
[Demo Video](https://www.youtube.com/watch?v=your_video_id) *(Eslatma: Videoni yuklang va havolani yangilang)*

## Fayl tuzilmasi
```
Gistify/
├── main.py              # Asosiy dastur
├── video_processor.py   # Video yuklash va subtitr yaratish
├── video_creator.py     # Yangi video yaratish
├── translator.py        # Tarjima qilish
├── subtitle_analyzer.py # Subtitr tahlili
├── requirements.txt     # Kutubxonalar ro‘yxati
├── README.md           # Loyiha haqida ma‘lumot
├── .gitignore          # E’tiborsiz fayllar
├── logo/               # Logotip fayllari
│   └── logo.jpg
├── screenshots/        # Skrinshotlar
└── voiceovers/         # Ovozli fayllar (gitignore’da)
```

## Jamoa
- [Ismingiz]: Loyiha rahbari, Backend va Frontend ishlab chiqaruvchi
- [Boshqa jamoa a’zolari, agar bo‘lsa]: [Ularning rollari]

## Litsenziya
MIT License

## Eslatmalar
- Loyiha faqat ta’limiy maqsadlarda ishlatilishi kerak.
- API kalitlarni maxfiy saqlang va repozitoriyga qo‘shmang.
- Hakamlar uchun sinov kalitlari alohida taqdim etilishi mumkin.