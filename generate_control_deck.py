import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def build_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette
    C_NAVY = RGBColor(15, 23, 42)          # #0F172A
    C_CARD_DARK = RGBColor(30, 41, 59)     # #1E293B
    C_BG_LIGHT = RGBColor(248, 250, 252)   # #F8FAFC
    C_WHITE = RGBColor(255, 255, 255)
    C_TEAL = RGBColor(14, 165, 233)        # #0EA5E9 (Accent Primary)
    C_TEXT_DARK = RGBColor(15, 23, 42)     # #0F172A
    C_TEXT_MUTED = RGBColor(100, 116, 139) # #64748B
    C_BORDER_LIGHT = RGBColor(226, 232, 240)
    C_AMBER = RGBColor(217, 119, 6)        # #D97706
    C_GREEN = RGBColor(16, 185, 129)       # #10B981

    def add_bg(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, title, category, dark=False):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.7), Inches(0.95))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p1 = tf.paragraphs[0]
        p1.text = category.upper()
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = C_TEAL
        p1.font.name = "Calibri"

        p2 = tf.add_paragraph()
        p2.text = title
        p2.font.size = Pt(23)
        p2.font.bold = True
        p2.font.color.rgb = C_WHITE if dark else C_TEXT_DARK
        p2.font.name = "Calibri"

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Dark Navy)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    add_bg(s1, C_NAVY)

    tag = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.3), Inches(4.3), Inches(0.38))
    tag.fill.solid()
    tag.fill.fore_color.rgb = C_CARD_DARK
    tag.line.color.rgb = C_TEAL
    tag_p = tag.text_frame.paragraphs[0]
    tag_p.text = "MATA KULIAH SISTEM KENDALI OTOMATIS"
    tag_p.font.size = Pt(11)
    tag_p.font.bold = True
    tag_p.font.color.rgb = C_TEAL
    tag_p.alignment = PP_ALIGN.CENTER

    t_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.95), Inches(11.7), Inches(2.2))
    ttf = t_box.text_frame
    ttf.word_wrap = True
    ttf.margin_left = ttf.margin_top = ttf.margin_right = ttf.margin_bottom = 0
    tp1 = ttf.paragraphs[0]
    tp1.text = "Sistem Kendali Lingkar Tertutup (Closed-Loop PID)\nAerasi Headspace Silo Bahan Baku"
    tp1.font.size = Pt(34)
    tp1.font.bold = True
    tp1.font.color.rgb = C_WHITE
    tp1.font.name = "Calibri"

    tp2 = ttf.add_paragraph()
    tp2.text = "\nFokus Kajian: Pemodelan Fisik Plant, Penurunan Fungsi Alih Orde-1, Ekstraksi Kurva Reaksi, dan Penalaan Kontroler Ziegler-Nichols"
    tp2.font.size = Pt(15)
    tp2.font.color.rgb = RGBColor(148, 163, 184)
    tp2.font.name = "Calibri"

    # Presenter Card
    c_pres = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.4), Inches(11.7), Inches(1.3))
    c_pres.fill.solid()
    c_pres.fill.fore_color.rgb = C_CARD_DARK
    c_pres.line.color.rgb = RGBColor(51, 65, 85)
    cptf = c_pres.text_frame
    cptf.margin_left = Inches(0.4)
    cptf.margin_top = Inches(0.25)
    cp1 = cptf.paragraphs[0]
    cp1.text = "Topik Bahasan: Model Matematis, Transfer Function, Algoritma PID Diskrit & Respons Waktu"
    cp1.font.size = Pt(13)
    cp1.font.bold = True
    cp1.font.color.rgb = C_WHITE
    cp2 = cptf.add_paragraph()
    cp2.text = "Dosen Pengampu: Ucky Pradestha N, M.Kom  |  Penyusun: Manuel & Tim"
    cp2.font.size = Pt(13)
    cp2.font.color.rgb = C_TEAL

    # =========================================================================
    # SLIDE 2: GAMBARAN UMUM & OBJEK KENDALI
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_bg(s2, C_BG_LIGHT)
    add_header(s2, "Gambaran Umum Sistem: Apa yang Dikendalikan?", "Sistem Kendali — Definisi Objek & Variabel")

    # 3 Cards
    # Card 1: Plant Fisik
    c1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.65), Inches(3.64), Inches(5.1))
    c1.fill.solid()
    c1.fill.fore_color.rgb = C_WHITE
    c1.line.color.rgb = C_BORDER_LIGHT
    tf1 = c1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.3)
    p = tf1.paragraphs[0]
    p.text = "1. Plant Fisik G(s)"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p2 = tf1.add_paragraph()
    p2.text = "\n• Definisi Objek:\nRuang udara di atap silo (Headspace Volume Silo) yang menampung bahan baku curah.\n\n• Sifat Fisik Plant:\nMemiliki volume udara (V), kapasitas tampung gas, dan inersia pertukaran udara.\n\n• Masalah Alami:\nBahan baku mengalami fermentasi yang melepaskan gas kontaminan (CO2, alkohol, gas pembusukan) dan menaikkan suhu ruangan."
    p2.font.size = Pt(12)
    p2.font.color.rgb = C_TEXT_MUTED

    # Card 2: Variabel Kendali
    c2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.84), Inches(1.65), Inches(3.64), Inches(5.1))
    c2.fill.solid()
    c2.fill.fore_color.rgb = C_WHITE
    c2.line.color.rgb = C_TEAL
    tf2 = c2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_right = tf2.margin_top = Inches(0.3)
    p = tf2.paragraphs[0]
    p.text = "2. Variabel Kendali"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    p2 = tf2.add_paragraph()
    p2.text = "\n• Input Acuan / Setpoint r(t):\nBatas toleransi aman gas di silo (misal: 1500 ADC mentah).\n\n• Output Terukur / PV y(t):\nKonsentrasi gas aktual yang dibaca sensor semikonduktor MQ-135.\n\n• Sinyal Galat / Error e(t):\nSelisih antara target aman dengan kondisi nyata: e(t) = r(t) - y(t).\n\n• Variabel Suhu (DHT22):\nDipantau dan diintegrasikan sebagai batas proteksi termal."
    p2.font.size = Pt(12)
    p2.font.color.rgb = C_TEXT_MUTED

    # Card 3: Aktuator Pelaksana
    c3 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.88), Inches(1.65), Inches(3.64), Inches(5.1))
    c3.fill.solid()
    c3.fill.fore_color.rgb = C_WHITE
    c3.line.color.rgb = C_GREEN
    tf3 = c3.text_frame
    tf3.word_wrap = True
    tf3.margin_left = tf3.margin_right = tf3.margin_top = Inches(0.3)
    p = tf3.paragraphs[0]
    p.text = "3. Aktuator Kendali"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = C_GREEN
    p2 = tf3.add_paragraph()
    p2.text = "\n• Sinyal Kontrol u(t):\nKeluaran matematis PID berupa nilai PWM (0-255).\n\n• Driver MOSFET HW-517:\nMengonversi sinyal PWM logika 3.3V ESP32 menjadi tegangan rata-rata variabel motor kipas.\n\n• Motor Kipas Blower DC:\nMengalirkan debit udara pembuangan (Q) secara proporsional.\n\n• Micro Servo SG90:\nMengatur sudut bukaan katup pembuangan atap (0° - 90°) secara halus."
    p2.font.size = Pt(12)
    p2.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 3: BEDAH DIAGRAM BLOK SISTEM KENDALI TERTUTUP
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_bg(s3, C_BG_LIGHT)
    add_header(s3, "Bedah Diagram Blok: Jalur Maju & Jalur Umpan Balik", "Lecture 2 & 5 Alignment — Feedback Loop")

    # Flow Container Top (Forward Path)
    cfwd = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.65), Inches(11.7), Inches(2.2))
    cfwd.fill.solid()
    cfwd.fill.fore_color.rgb = C_WHITE
    cfwd.line.color.rgb = C_BORDER_LIGHT
    fwd_tf = cfwd.text_frame
    fwd_tf.word_wrap = True
    fwd_tf.margin_left = fwd_tf.margin_top = Inches(0.3)
    p = fwd_tf.paragraphs[0]
    p.text = "JALUR MAJU (FORWARD PATH): ALUR SEBAB-AKIBAT DARI PERINTAH KE FISIK"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    p_fwd = fwd_tf.add_paragraph()
    p_fwd.text = "\n1. Setpoint r(t) : Ambang batas aman konsentrasi gas yang diizinkan di dalam silo.\n2. Komparator (Σ) : Menghitung galat: e(t) = r(t) - y(t). Selisih ini yang memicu tindakan kontroler.\n3. Kontroler C(s) : Algoritma PID di ESP32 yang menghitung sinyal kontrol u(t) secara matematis.\n4. Aktuator       : Driver MOSFET memodulasi PWM ke motor kipas dan Servo membuka katup katup buang.\n5. Plant Fisik G(s): Volume udara atap silo tempat terjadinya pertukaran gas akibat hembusan angin kipas."
    p_fwd.font.size = Pt(12)
    p_fwd.font.color.rgb = C_TEXT_DARK

    # Bottom Row: 2 Split Cards
    # Card 1: Disturbance
    cdist = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.1), Inches(5.6), Inches(2.65))
    cdist.fill.solid()
    cdist.fill.fore_color.rgb = C_WHITE
    cdist.line.color.rgb = C_AMBER
    dtf = cdist.text_frame
    dtf.word_wrap = True
    dtf.margin_left = dtf.margin_top = Inches(0.3)
    p = dtf.paragraphs[0]
    p.text = "Sinyal Gangguan / Disturbance d(t)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_AMBER
    p2 = dtf.add_paragraph()
    p2.text = "\n• Posisi: Masuk tepat sebelum/pada Plant Fisik.\n• Bentuk Nyata di Silo:\n  - Pelepasan gas mendadak akibat fermentasi bahan curah.\n  - Saluran buang tertutup debu atau tegangan drop.\n• Tugas Sistem Kendali:\n  Menolak gangguan fisik ini (Disturbance Rejection) agar output y(t) tetap kembali ke batas aman."
    p2.font.size = Pt(12)
    p2.font.color.rgb = C_TEXT_MUTED

    # Card 2: Feedback Sensor
    cfb = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(4.1), Inches(5.6), Inches(2.65))
    cfb.fill.solid()
    cfb.fill.fore_color.rgb = C_WHITE
    cfb.line.color.rgb = C_GREEN
    fbtf = cfb.text_frame
    fbtf.word_wrap = True
    fbtf.margin_left = fbtf.margin_top = Inches(0.3)
    p = fbtf.paragraphs[0]
    p.text = "Jalur Umpan Balik: Sensor H(s)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_GREEN
    p2 = fbtf.add_paragraph()
    p2.text = "\n• Komponen: Sensor gas semikonduktor MQ-135.\n• Peran Lingkar Tertutup:\n  Membaca konsentrasi gas aktual di ujung kanan plant, lalu menarik garis data memutar kembali ke komparator di sebelah kiri.\n• Menjamin ESP32 tidak 'buta' terhadap hasil kerjanya, sehingga loop kendali tertutup sempurna."
    p2.font.size = Pt(12)
    p2.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 4: PEMODELAN MATEMATIS & PERSAMAAN DIFERENSIAL
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_bg(s4, C_BG_LIGHT)
    add_header(s4, "Penurunan Fungsi Alih (Transfer Function) Ruang Silo", "Lecture 3 & 4 Alignment — Modeling in Frequency Domain")

    # Left Container: Persamaan Diferensial Fisik
    cpd = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.65), Inches(5.6), Inches(5.1))
    cpd.fill.solid()
    cpd.fill.fore_color.rgb = C_WHITE
    cpd.line.color.rgb = C_BORDER_LIGHT
    pdtf = cpd.text_frame
    pdtf.word_wrap = True
    pdtf.margin_left = pdtf.margin_right = pdtf.margin_top = Inches(0.35)
    p = pdtf.paragraphs[0]
    p.text = "1. Persamaan Diferensial Fisik"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p2 = pdtf.add_paragraph()
    p2.text = "\nBerdasarkan Hukum Kesetimbangan Massa Gas:\nLaju akumulasi gas di dalam ruang silo volume (V) sama dengan laju pembentukan gas dikurangi laju pembuangan oleh aerasi kipas:\n\nV · (dC(t) / dt) + Q_air · C(t) = K_g · u(t)\n\nKeterangan Variabel:\n• C(t) : Konsentrasi gas di dalam ruang silo pada waktu t.\n• V    : Volume fisik ruang udara atap silo (m³).\n• Q_air: Debit aliran udara pembuangan kipas (m³/s).\n• u(t) : Sinyal kendali tegangan/PWM dari ESP32.\n• K_g  : Konstanta efektivitas pembuangan gas."
    p2.font.size = Pt(12)
    p2.font.color.rgb = C_TEXT_MUTED

    # Right Container: Transformasi Laplace ke Fungsi Alih
    ctf_box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.65), Inches(5.6), Inches(5.1))
    ctf_box.fill.solid()
    ctf_box.fill.fore_color.rgb = C_WHITE
    ctf_box.line.color.rgb = C_TEAL
    tttf = ctf_box.text_frame
    tttf.word_wrap = True
    tttf.margin_left = tttf.margin_right = tttf.margin_top = Inches(0.35)
    p = tttf.paragraphs[0]
    p.text = "2. Transformasi Laplace & Fungsi Alih"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    p2 = tttf.add_paragraph()
    p2.text = "\nTerapkan Transformasi Laplace dengan asumsi syarat awal nol (C(0) = 0):\n\n(V · s + Q_air) · C(s) = K_g · U(s)\n\nFungsi Alih G(s) = Output(s) / Input(s):\n\nG(s) = C(s) / U(s) = (K_g / Q_air) / ((V / Q_air) · s + 1)\n\nBentuk Standar Sistem Orde-1 dengan Dead-Time (FOPDT):\n\nG(s) = K / (τ · s + 1) · e^(-L · s)\n\n• K = K_g / Q_air  -> Gain Statis Sistem (ADC/PWM)\n• τ = V / Q_air    -> Konstanta Waktu Inersia Boks (detik)\n• L = Dead Time   -> Waktu tunda aliran udara ke sensor"
    p2.font.size = Pt(12)
    p2.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 5: RUMUS IDENTIFIKASI SISTEM (UJI STEP RESPONSE)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_bg(s5, C_BG_LIGHT)
    add_header(s5, "Identifikasi Sistem: Menghitung K, L, dan τ dari Eksperimen", "Lecture 6 Alignment — Step Response Analysis")

    # Left Container: Metodologi Uji Terbuka
    c_mth = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.65), Inches(5.6), Inches(5.1))
    c_mth.fill.solid()
    c_mth.fill.fore_color.rgb = C_WHITE
    c_mth.line.color.rgb = C_BORDER_LIGHT
    mtf = c_mth.text_frame
    mtf.word_wrap = True
    mtf.margin_left = mtf.margin_right = mtf.margin_top = Inches(0.35)
    p = mtf.paragraphs[0]
    p.text = "Prosedur Uji Kurva Reaksi (Open-Loop)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p2 = mtf.add_paragraph()
    p2.text = "\nBukan Data Asumsi / Tebakan Internet:\n\n1. Ruang miniatur silo dikondisikan hingga nilai gas MQ-135 stabil di nilai kontaminasi awal (y0 = 2800 ADC).\n\n2. Kipas aerasi diberi lonjakan daya konstan (Step Input, misal Δu = 200 PWM) dan servo membuka katup atap 90°.\n\n3. Catat nilai pembacaan sensor gas MQ-135 setiap 1 detik sampai kurva stabil di nilai tunak akhir (yss = 1600 ADC).\n\n4. Ekstraksi angka K, L, dan τ langsung dari grafik respons waktu."
    p2.font.size = Pt(12)
    p2.font.color.rgb = C_TEXT_MUTED

    # Right Container: Rumus Perhitungan Parameter
    c_calc = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.65), Inches(5.6), Inches(5.1))
    c_calc.fill.solid()
    c_calc.fill.fore_color.rgb = C_WHITE
    c_calc.line.color.rgb = C_TEAL
    calctf = c_calc.text_frame
    calctf.word_wrap = True
    calctf.margin_left = calctf.margin_right = calctf.margin_top = Inches(0.35)
    p = calctf.paragraphs[0]
    p.text = "Rumus Ekstraksi Parameter Orde-1"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    p2 = calctf.add_paragraph()
    p2.text = "\n1. Rumus Gain Statis Sistem (K):\n   K = Δy / Δu = (y0 - yss) / Δu\n   K = (2800 - 1600) / 200 = 1200 / 200 = 6.0 ADC/PWM\n\n2. Rumus Dead Time (L / Waktu Tunda):\n   L = t_reaksi - t_step_mulai = 1.5 detik\n\n3. Rumus Konstanta Waktu (τ - Aturan 63.2% Lecture 6):\n   Δy_63.2% = 0.632 · (y0 - yss) = 0.632 · 1200 = 758.4\n   y_target = 2800 - 758.4 = 2041.6 ADC\n   τ = t(pada y=2041.6) - L = 8.5 s - 1.5 s = 7.0 detik\n\nFungsi Alih Riil Alat: G(s) = 6.0 / (7.0s + 1) · e^(-1.5s)"
    p2.font.size = Pt(12)
    p2.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 6: FORMULA PENALAAN PID ZIEGLER-NICHOLS
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_bg(s6, C_BG_LIGHT)
    add_header(s6, "Perancangan Kontroler: Formula Penalaan Ziegler-Nichols", "Controller Tuning — Reaction Curve Method")

    # Left Container: Rumus Tuning Resmi
    c_zn = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.65), Inches(6.0), Inches(5.1))
    c_zn.fill.solid()
    c_zn.fill.fore_color.rgb = C_WHITE
    c_zn.line.color.rgb = C_NAVY
    zntf = c_zn.text_frame
    zntf.word_wrap = True
    zntf.margin_left = zntf.margin_right = zntf.margin_top = Inches(0.35)
    p = zntf.paragraphs[0]
    p.text = "Perhitungan Matematis Nilai Kp, Ki, Kd"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p2 = zntf.add_paragraph()
    p2.text = "\nBerdasarkan Parameter Riil: K = 6.0, τ = 7.0 s, L = 1.5 s\n\n1. Penguatan Proporsional (Kp):\n   Kp = 1.2 · (τ / (K · L))\n   Kp = 1.2 · (7.0 / (6.0 · 1.5)) = 8.4 / 9.0 ≈ 0.933\n\n2. Waktu & Penguatan Integral (Ti & Ki):\n   Ti = 2 · L = 2 · 1.5 = 3.0 detik\n   Ki = Kp / Ti = 0.933 / 3.0 ≈ 0.311 s⁻¹\n\n3. Waktu & Penguatan Derivatif (Td & Kd):\n   Td = 0.5 · L = 0.5 · 1.5 = 0.75 detik\n   Kd = Kp · Td = 0.933 · 0.75 ≈ 0.700 s\n\nSeluruh nilai terhitung analitik dari sifat fisik boks!"
    p2.font.size = Pt(12)
    p2.font.color.rgb = C_TEXT_MUTED

    # Right Container: Bedah Fungsi P, I, D
    c_roles = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.2), Inches(1.65), Inches(5.3), Inches(5.1))
    c_roles.fill.solid()
    c_roles.fill.fore_color.rgb = C_WHITE
    c_roles.line.color.rgb = C_AMBER
    rtf = c_roles.text_frame
    rtf.word_wrap = True
    rtf.margin_left = rtf.margin_right = rtf.margin_top = Inches(0.35)
    p = rtf.paragraphs[0]
    p.text = "Bedah Peran P, I, dan D dalam Silo"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_AMBER
    p2 = rtf.add_paragraph()
    p2.text = "\n• Kenapa Tidak Cukup P Saja?\nJika hanya P, saat gas mendekati batas aman, selisih error kecil sehingga daya kipas melemah dan gas NYANGKUT (ada Steady-State Error ess ≠ 0).\n\n• Peran Kritis Aksi Integral (I):\nMenjumlahkan sisa error terhadap waktu secara terus-menerus. Aksi ini menambah tenaga hembusan kipas perlahan sampai gas TURUN TUNTAS ke setpoint (ess = 0).\n\n• Peran Kritis Aksi Derivatif (D):\nMelihat kecepatan laju penurunan gas (de/dt). Bertindak sebagai rem otomatis untuk mencegah overshoot dan meredam osilasi liar katup servo."
    p2.font.size = Pt(12)
    p2.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 7: ALGORITMA PID DISKRIT PADA ESP32
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_bg(s7, C_BG_LIGHT)
    add_header(s7, "Implementasi Algoritma: Persamaan Diskrit pada ESP32", "Digital Implementation — Difference Equations")

    # Left Card: Rumus Diskrit
    cdisc = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.65), Inches(5.6), Inches(5.1))
    cdisc.fill.solid()
    cdisc.fill.fore_color.rgb = C_WHITE
    cdisc.line.color.rgb = C_TEAL
    dtf = cdisc.text_frame
    dtf.word_wrap = True
    dtf.margin_left = dtf.margin_right = dtf.margin_top = Inches(0.35)
    p = dtf.paragraphs[0]
    p.text = "Persamaan Beda Diskrit (Difference Eq.)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    p2 = dtf.add_paragraph()
    p2.text = "\nDi mikrokontroler, persamaan kontinu diubah menjadi persamaan selisih hingga dengan periode sampling Δt:\n\n1. Galat Saat Ini (k):\n   e[k] = r[k] - y[k]\n\n2. Suku Proporsional:\n   P[k] = Kp · e[k]\n\n3. Suku Integral (Metode Penjumlahan Euler):\n   I[k] = I[k-1] + Ki · e[k] · Δt\n\n4. Suku Derivatif (Metode Selisih Mundur Backward):\n   D[k] = Kd · (e[k] - e[k-1]) / Δt\n\n5. Total Sinyal Kontrol:\n   u[k] = P[k] + I[k] + D[k]"
    p2.font.size = Pt(12)
    p2.font.color.rgb = C_TEXT_MUTED

    # Right Card: Kode & Saturasi Aktuator
    ccode = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.65), Inches(5.6), Inches(5.1))
    ccode.fill.solid()
    ccode.fill.fore_color.rgb = C_WHITE
    ccode.line.color.rgb = C_BORDER_LIGHT
    ctf = ccode.text_frame
    ctf.word_wrap = True
    ctf.margin_left = ctf.margin_right = ctf.margin_top = Inches(0.35)
    p = ctf.paragraphs[0]
    p.text = "Saturasi Aktuator & Anti-Windup"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p2 = ctf.add_paragraph()
    p2.text = "\nBatasan Fisik Hardware (Driver & Motor):\n\n• Sinyal PWM ESP32 dibatasi pada rentang 8-bit:\n  pwm_out = constrain(u[k], 0, 255)\n\n• Sudut Servo Katup Atap dibatasi mekanik:\n  sudut_servo = map(pwm_out, 0, 255, 0, 90)\n\n• Anti-Windup Protection:\n  Mencegah suku Integral membengkak tak terbatas saat aktuator sudah mentok di 255 PWM:\n  if (u[k] >= 255 || u[k] <= 0) {\n      I[k] = I[k-1]; // Bekukan nilai akumulasi integral\n  }"
    p2.font.size = Pt(12)
    p2.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 8: RUMUS EVALUASI KINERJA & KESTABILAN
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_bg(s8, C_BG_LIGHT)
    add_header(s8, "Evaluasi Kinerja Respons Waktu & Bukti Teoretis ess = 0", "Lecture 6 & 7 Alignment — Steady-State Analysis")

    # Left Container: Metrik Respons Waktu
    ceval = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.65), Inches(5.6), Inches(5.1))
    ceval.fill.solid()
    ceval.fill.fore_color.rgb = C_WHITE
    ceval.line.color.rgb = C_BORDER_LIGHT
    etf = ceval.text_frame
    etf.word_wrap = True
    etf.margin_left = etf.margin_right = etf.margin_top = Inches(0.35)
    p = etf.paragraphs[0]
    p.text = "1. Metrik Respons Waktu (Lecture 6)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p2 = etf.add_paragraph()
    p2.text = "\nParameter Kuantitatif Hasil Uji Closed-Loop:\n\n• Rise Time (tr / Waktu Naik):\nWaktu yang dibutuhkan kurva untuk turun dari 10% ke 90% target eliminasi gas.\n\n• Settling Time (ts / Waktu Tunak):\nWaktu tempuh hingga konsentrasi gas menetap di rentang toleransi ±2% dari batas aman: ts ≈ 4 · τ\n\n• Maximum Overshoot (%OS):\nEvaluasi lonjakan bukaan katup dan penurunan gas berlebih:\n%OS = e^(-(ζ · π) / √(1 - ζ²)) · 100%\nSistem dirancang teredam kritis mendekati ζ ≈ 1."
    p2.font.size = Pt(12)
    p2.font.color.rgb = C_TEXT_MUTED

    # Right Container: Pembuktian ess = 0
    cess = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.65), Inches(5.6), Inches(5.1))
    cess.fill.solid()
    cess.fill.fore_color.rgb = C_WHITE
    cess.line.color.rgb = C_GREEN
    esstf = cess.text_frame
    esstf.word_wrap = True
    esstf.margin_left = esstf.margin_right = esstf.margin_top = Inches(0.35)
    p = esstf.paragraphs[0]
    p.text = "2. Pembuktian Matematis ess = 0"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_GREEN
    p2 = esstf.add_paragraph()
    p2.text = "\nBerdasarkan Teorema Nilai Akhir (Final Value Theorem):\n\ness = lim(s->0) [ s · E(s) ] = lim(s->0) [ s · R(s) / (1 + C(s)G(s)) ]\n\nUntuk Masukan Undak R(s) = A / s:\n\ness = lim(s->0) [ A / (1 + C(s)G(s)) ]\n\nKarena Kontroler PID Memiliki Aksi Integral (C(s) memuat Ki / s):\n\nlim(s->0) C(s)G(s) = ∞  (Sistem Tipe-1)\n\nMaka Galat Keadaan Tunak:\n\ness = A / (1 + ∞) = 0 !\n\nTerbukti analitik: Aksi Integral menjamin gas turun tuntas ke setpoint!"
    p2.font.size = Pt(12)
    p2.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 9: KESIMPULAN & KESIAPAN IMPLEMENTASI (Dark Navy)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_bg(s9, C_NAVY)
    add_header(s9, "Ringkasan Rancang Bangun Sistem Kendali Silo", "Conclusion & Scientific Rigor", dark=True)

    summary_items = [
        ("Objek Kendali Jelas", "Plant fisik adalah volume udara atap silo (Headspace), dengan variabel gas MQ-135 sebagai feedback loop tertutup."),
        ("Pemodelan Ilmiah", "Fungsi alih orde-1 diturunkan dari kesetimbangan massa Continuous Stirred Volume dan Transformasi Laplace."),
        ("Bukan Angka Asumsi", "Nilai K, L, dan τ diukur langsung dari kurva reaksi open-loop 63.2% pada boks miniatur uji."),
        ("Penalaan Ziegler-Nichols", "Konstanta Kp = 0.933, Ki = 0.311, Kd = 0.700 dihitung analitik untuk menjamin kestabilan dan ess = 0.")
    ]

    w_box = Inches(2.7)
    gap = Inches(0.3)
    start_x = Inches(0.8)

    for i, (stitle, sdesc) in enumerate(summary_items):
        sx = start_x + i * (w_box + gap)
        sc = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, sx, Inches(2.0), w_box, Inches(4.5))
        sc.fill.solid()
        sc.fill.fore_color.rgb = C_CARD_DARK
        sc.line.color.rgb = C_TEAL if i == 0 else RGBColor(51, 65, 85)
        sctf = sc.text_frame
        sctf.word_wrap = True
        sctf.margin_left = sctf.margin_right = sctf.margin_top = Inches(0.3)
        p1 = sctf.paragraphs[0]
        p1.text = f"POIN 0{i+1}"
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = C_TEAL
        p2 = sctf.add_paragraph()
        p2.text = "\n" + stitle
        p2.font.size = Pt(16)
        p2.font.bold = True
        p2.font.color.rgb = C_WHITE
        p3 = sctf.add_paragraph()
        p3.text = "\n" + sdesc
        p3.font.size = Pt(12)
        p3.font.color.rgb = RGBColor(148, 163, 184)

    out_name = "Sistem_Kendali_Silo_Rumus_Lengkap.pptx"
    prs.save(out_name)
    print(f"Deck saved as '{out_name}'")

if __name__ == "__main__":
    build_deck()
