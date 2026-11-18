import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def generate_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Colors
    C_NAVY = RGBColor(15, 23, 42)          # #0F172A (Dark Theme BG)
    C_CARD_DARK = RGBColor(30, 41, 59)     # #1E293B (Dark Cards)
    C_BG_LIGHT = RGBColor(248, 250, 252)   # #F8FAFC (Light Theme BG)
    C_WHITE = RGBColor(255, 255, 255)
    C_TEAL = RGBColor(14, 165, 233)        # #0EA5E9 (Accent Cyan/Teal)
    C_TEXT_DARK = RGBColor(15, 23, 42)     # #0F172A (Primary Heading / Body)
    C_TEXT_BODY = RGBColor(30, 41, 59)     # #1E293B (Dark Slate for crisp body)
    C_TEXT_MUTED = RGBColor(71, 85, 105)   # #475569 (Secondary Text)
    C_BORDER_LIGHT = RGBColor(203, 213, 225) # #CBD5E1 (Solid crisp border)
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
        
        # Category Run
        p1 = tf.paragraphs[0]
        r1 = p1.add_run()
        r1.text = category.upper()
        r1.font.size = Pt(11)
        r1.font.bold = True
        r1.font.name = "Calibri"
        r1.font.color.rgb = C_TEAL

        # Title Run
        p2 = tf.add_paragraph()
        r2 = p2.add_run()
        r2.text = title
        r2.font.size = Pt(23)
        r2.font.bold = True
        r2.font.name = "Calibri"
        r2.font.color.rgb = C_WHITE if dark else C_TEXT_DARK

    def add_card_box(slide, x, y, w, h, bg_color=C_WHITE, border_color=C_BORDER_LIGHT):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1.5)
        else:
            card.line.fill.background()
        return card

    def add_card_text(slide, x, y, w, h, lines, pad=Inches(0.25)):
        tb = slide.shapes.add_textbox(x + pad, y + pad, w - (pad * 2), h - (pad * 2))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        for i, item in enumerate(lines):
            text, size, bold, color, space_after = item
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            if space_after > 0:
                p.space_after = Pt(space_after)
            if text:
                r = p.add_run()
                r.text = text
                r.font.size = Pt(size)
                r.font.bold = bold
                r.font.name = "Calibri"
                r.font.color.rgb = color
        return tb

    # =========================================================================
    # SLIDE 1: COVER SLIDE (Dark Navy)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    add_bg(s1, C_NAVY)

    # Tag Badge
    add_card_box(s1, Inches(0.8), Inches(1.2), Inches(4.5), Inches(0.4), bg_color=C_CARD_DARK, border_color=C_TEAL)
    tb_tag = s1.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(4.5), Inches(0.4))
    r_tag = tb_tag.text_frame.paragraphs[0].add_run()
    r_tag.text = "MATA KULIAH SISTEM KENDALI OTOMATIS"
    r_tag.font.size = Pt(11)
    r_tag.font.bold = True
    r_tag.font.name = "Calibri"
    r_tag.font.color.rgb = C_TEAL
    tb_tag.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    # Main Title & Subtitle in Textbox
    tb_title = s1.shapes.add_textbox(Inches(0.8), Inches(1.85), Inches(11.7), Inches(3.2))
    tf1 = tb_title.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.space_after = Pt(8)
    r = p.add_run()
    r.text = "Sistem Kendali Lingkar Tertutup (Closed-Loop PID)\nAerasi Headspace Silo Bahan Baku"
    r.font.size = Pt(32)
    r.font.bold = True
    r.font.name = "Calibri"
    r.font.color.rgb = C_WHITE

    p_sub = tf1.add_paragraph()
    r_sub = p_sub.add_run()
    r_sub.text = "Fokus Kajian: Pemodelan Fisik Plant, Penurunan Fungsi Alih Orde-1, Ekstraksi Kurva Reaksi 63.2%, dan Penalaan Kontroler Ziegler-Nichols"
    r_sub.font.size = Pt(15)
    r_sub.font.name = "Calibri"
    r_sub.font.color.rgb = RGBColor(148, 163, 184)

    # Presenter Card
    add_card_box(s1, Inches(0.8), Inches(5.3), Inches(11.7), Inches(1.4), bg_color=C_CARD_DARK, border_color=RGBColor(51, 65, 85))
    lines_p = [
        ("Topik Bahasan: Model Matematis, Transfer Function, Algoritma PID Diskrit, dan Respons Waktu", 13, True, C_WHITE, 4),
        ("Mata Kuliah: Sistem Kendali & IoT  |  Gasal 2026", 12, False, RGBColor(148, 163, 184), 4),
        ("Dosen Pengampu: Ucky Pradestha N, M.Kom  |  Presenter: Manuel & Tim", 13, True, C_TEAL, 0)
    ]
    add_card_text(s1, Inches(0.8), Inches(5.3), Inches(11.7), Inches(1.4), lines_p, pad=Inches(0.25))

    # =========================================================================
    # SLIDE 2: OBJEK YANG DIKENDALIKAN & DEFINISI VARIABEL
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_bg(s2, C_BG_LIGHT)
    add_header(s2, "Gambaran Umum Sistem: Apa yang Dikendalikan?", "Sistem Kendali — Definisi Objek & Variabel")

    # Card 1: Plant Fisik
    add_card_box(s2, Inches(0.8), Inches(1.65), Inches(3.64), Inches(5.1), bg_color=C_WHITE, border_color=C_BORDER_LIGHT)
    lines_c1 = [
        ("1. Plant Fisik G(s)", 17, True, C_TEXT_DARK, 10),
        ("• Definisi Objek:", 12, True, C_TEXT_BODY, 2),
        ("Ruang udara di atap silo (Headspace Volume Silo) yang menampung bahan baku curah.", 12, False, C_TEXT_MUTED, 8),
        ("• Sifat Fisik Plant:", 12, True, C_TEXT_BODY, 2),
        ("Memiliki volume udara (V), kapasitas tampung gas, dan inersia pertukaran udara.", 12, False, C_TEXT_MUTED, 8),
        ("• Masalah Fisik:", 12, True, C_TEXT_BODY, 2),
        ("Bahan curah mengalami fermentasi alami yang melepaskan gas kontaminan dan memicu kenaikan suhu.", 12, False, C_TEXT_MUTED, 0)
    ]
    add_card_text(s2, Inches(0.8), Inches(1.65), Inches(3.64), Inches(5.1), lines_c1)

    # Card 2: Variabel Kendali
    add_card_box(s2, Inches(4.84), Inches(1.65), Inches(3.64), Inches(5.1), bg_color=C_WHITE, border_color=C_TEAL)
    lines_c2 = [
        ("2. Variabel Kendali", 17, True, C_TEAL, 10),
        ("• Input Acuan / Setpoint r(t):", 12, True, C_TEXT_BODY, 2),
        ("Batas toleransi aman gas di silo (misal: 1500 ADC mentah).", 12, False, C_TEXT_MUTED, 8),
        ("• Output Terukur / PV y(t):", 12, True, C_TEXT_BODY, 2),
        ("Konsentrasi gas aktual yang dibaca sensor semikonduktor MQ-135.", 12, False, C_TEXT_MUTED, 8),
        ("• Sinyal Galat / Error e(t):", 12, True, C_TEXT_BODY, 2),
        ("e(t) = r(t) - y(t). Selisih ini yang menggerakkan aksi kontroler.", 12, False, C_TEXT_MUTED, 8),
        ("• Variabel Suhu (DHT22):", 12, True, C_TEXT_BODY, 2),
        ("Dipantau sebagai batas proteksi termal ganda.", 12, False, C_TEXT_MUTED, 0)
    ]
    add_card_text(s2, Inches(4.84), Inches(1.65), Inches(3.64), Inches(5.1), lines_c2)

    # Card 3: Aktuator Pelaksana
    add_card_box(s2, Inches(8.88), Inches(1.65), Inches(3.64), Inches(5.1), bg_color=C_WHITE, border_color=C_GREEN)
    lines_c3 = [
        ("3. Aktuator Kendali", 17, True, C_GREEN, 10),
        ("• Sinyal Kontrol u(t):", 12, True, C_TEXT_BODY, 2),
        ("Keluaran matematis PID berupa nilai PWM (0 - 255).", 12, False, C_TEXT_MUTED, 8),
        ("• Driver MOSFET HW-517:", 12, True, C_TEXT_BODY, 2),
        ("Mengonversi sinyal PWM logika 3.3V ESP32 menjadi tegangan rata-rata variabel motor kipas.", 12, False, C_TEXT_MUTED, 8),
        ("• Motor Kipas Blower DC:", 12, True, C_TEXT_BODY, 2),
        ("Mengalirkan debit aerasi pembuangan (Q) secara proporsional.", 12, False, C_TEXT_MUTED, 8),
        ("• Micro Servo SG90:", 12, True, C_TEXT_BODY, 2),
        ("Mengatur sudut bukaan katup pembuangan atap (0° - 90°).", 12, False, C_TEXT_MUTED, 0)
    ]
    add_card_text(s2, Inches(8.88), Inches(1.65), Inches(3.64), Inches(5.1), lines_c3)

    # =========================================================================
    # SLIDE 3: BEDAH DIAGRAM BLOK SISTEM KENDALI TERTUTUP
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_bg(s3, C_BG_LIGHT)
    add_header(s3, "Bedah Diagram Blok: Jalur Maju & Jalur Umpan Balik", "Lecture 2 & 5 Alignment — Feedback Loop")

    # Top Card: Forward Path
    add_card_box(s3, Inches(0.8), Inches(1.65), Inches(11.7), Inches(2.2), bg_color=C_WHITE, border_color=C_BORDER_LIGHT)
    lines_fwd = [
        ("JALUR MAJU (FORWARD PATH): ALUR SEBAB-AKIBAT DARI PERINTAH KE DUNIA FISIK", 13, True, C_TEAL, 8),
        ("1. Setpoint r(t) : Ambang batas aman konsentrasi gas yang diizinkan di dalam ruang silo.", 12, False, C_TEXT_BODY, 4),
        ("2. Komparator (Σ) : Menghitung nilai galat: e(t) = r(t) - y(t). Selisih ini yang memicu tindakan kontroler.", 12, False, C_TEXT_BODY, 4),
        ("3. Kontroler C(s) : Algoritma PID di ESP32 yang menghitung sinyal kontrol u(t) secara matematis.", 12, False, C_TEXT_BODY, 4),
        ("4. Aktuator       : Driver MOSFET memodulasi PWM ke motor kipas dan Servo membuka katup katup buang.", 12, False, C_TEXT_BODY, 4),
        ("5. Plant Fisik G(s): Volume udara atap silo tempat terjadinya pertukaran gas akibat hembusan angin kipas.", 12, False, C_TEXT_BODY, 0)
    ]
    add_card_text(s3, Inches(0.8), Inches(1.65), Inches(11.7), Inches(2.2), lines_fwd, pad=Inches(0.2))

    # Bottom Left Card: Disturbance
    add_card_box(s3, Inches(0.8), Inches(4.1), Inches(5.6), Inches(2.65), bg_color=C_WHITE, border_color=C_AMBER)
    lines_dist = [
        ("Sinyal Gangguan / Disturbance d(t)", 15, True, C_AMBER, 8),
        ("• Posisi Sinyal: Masuk tepat sebelum / pada Plant Fisik.", 12, True, C_TEXT_BODY, 4),
        ("• Bentuk Nyata di Silo:", 12, True, C_TEXT_BODY, 2),
        ("  - Pelepasan gas mendadak akibat fermentasi bahan curah.", 12, False, C_TEXT_MUTED, 2),
        ("  - Saluran buang tertutup debu atau tegangan motor drop.", 12, False, C_TEXT_MUTED, 6),
        ("• Tugas Kontroler: Menolak gangguan fisik ini (Disturbance Rejection) agar output y(t) tetap kembali ke batas aman.", 12, True, C_TEXT_BODY, 0)
    ]
    add_card_text(s3, Inches(0.8), Inches(4.1), Inches(5.6), Inches(2.65), lines_dist, pad=Inches(0.25))

    # Bottom Right Card: Feedback Sensor
    add_card_box(s3, Inches(6.9), Inches(4.1), Inches(5.6), Inches(2.65), bg_color=C_WHITE, border_color=C_GREEN)
    lines_fb = [
        ("Jalur Umpan Balik: Sensor H(s)", 15, True, C_GREEN, 8),
        ("• Komponen: Sensor gas semikonduktor MQ-135.", 12, True, C_TEXT_BODY, 4),
        ("• Peran Lingkar Tertutup:", 12, True, C_TEXT_BODY, 2),
        ("  Membaca konsentrasi gas aktual di ujung kanan plant, lalu menarik garis data memutar kembali ke komparator di sebelah kiri.", 12, False, C_TEXT_MUTED, 6),
        ("• Kepentingan Akademis: Menjamin ESP32 tidak 'buta' terhadap hasil kerjanya, sehingga tercipta sistem lingkar tertutup (closed-loop).", 12, True, C_TEXT_BODY, 0)
    ]
    add_card_text(s3, Inches(6.9), Inches(4.1), Inches(5.6), Inches(2.65), lines_fb, pad=Inches(0.25))

    # =========================================================================
    # SLIDE 4: PEMODELAN MATEMATIS & PERSAMAAN DIFERENSIAL
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_bg(s4, C_BG_LIGHT)
    add_header(s4, "Penurunan Fungsi Alih (Transfer Function) Ruang Silo", "Lecture 3 & 4 Alignment — Modeling in Frequency Domain")

    # Left Card: Persamaan Diferensial Fisik
    add_card_box(s4, Inches(0.8), Inches(1.65), Inches(5.6), Inches(5.1), bg_color=C_WHITE, border_color=C_BORDER_LIGHT)
    lines_pd = [
        ("1. Persamaan Diferensial Fisik", 16, True, C_TEXT_DARK, 8),
        ("Berdasarkan Hukum Kesetimbangan Massa Gas:", 12, True, C_TEXT_BODY, 4),
        ("Laju akumulasi gas di dalam ruang silo volume (V) sama dengan laju pembentukan gas dikurangi laju pembuangan oleh aerasi kipas:", 12, False, C_TEXT_MUTED, 8),
        ("V · (dC(t) / dt) + Q_air · C(t) = K_g · u(t)", 13, True, C_TEAL, 10),
        ("Keterangan Variabel Fisik:", 12, True, C_TEXT_BODY, 4),
        ("• C(t) : Konsentrasi gas dalam ruang silo pada waktu t.", 12, False, C_TEXT_MUTED, 3),
        ("• V    : Volume fisik ruang udara atap silo (m³).", 12, False, C_TEXT_MUTED, 3),
        ("• Q_air: Debit aliran udara pembuangan kipas (m³/s).", 12, False, C_TEXT_MUTED, 3),
        ("• u(t) : Sinyal kendali tegangan/PWM dari ESP32.", 12, False, C_TEXT_MUTED, 3),
        ("• K_g  : Konstanta efektivitas pembuangan gas.", 12, False, C_TEXT_MUTED, 0)
    ]
    add_card_text(s4, Inches(0.8), Inches(1.65), Inches(5.6), Inches(5.1), lines_pd)

    # Right Card: Transformasi Laplace
    add_card_box(s4, Inches(6.9), Inches(1.65), Inches(5.6), Inches(5.1), bg_color=C_WHITE, border_color=C_TEAL)
    lines_laplace = [
        ("2. Transformasi Laplace & Fungsi Alih", 16, True, C_TEAL, 8),
        ("Terapkan Transformasi Laplace dengan asumsi C(0) = 0:", 12, True, C_TEXT_BODY, 4),
        ("(V · s + Q_air) · C(s) = K_g · U(s)", 13, True, C_TEXT_DARK, 8),
        ("Fungsi Alih G(s) = Output(s) / Input(s):", 12, True, C_TEXT_BODY, 4),
        ("G(s) = C(s) / U(s) = (K_g / Q_air) / ((V / Q_air) · s + 1)", 13, True, C_NAVY, 10),
        ("Bentuk Standar Orde-1 dengan Dead-Time (FOPDT):", 12, True, C_TEXT_BODY, 4),
        ("G(s) = [ K / (τ · s + 1) ] · e^(-L · s)", 14, True, C_TEAL, 10),
        ("• K = K_g / Q_air  -> Gain Statis Sistem (ADC/PWM)", 12, False, C_TEXT_MUTED, 3),
        ("• τ = V / Q_air    -> Konstanta Waktu Inersia Boks (detik)", 12, False, C_TEXT_MUTED, 3),
        ("• L = Dead Time   -> Waktu tunda aliran gas ke sensor (detik)", 12, False, C_TEXT_MUTED, 0)
    ]
    add_card_text(s4, Inches(6.9), Inches(1.65), Inches(5.6), Inches(5.1), lines_laplace)

    # =========================================================================
    # SLIDE 5: RUMUS IDENTIFIKASI SISTEM (UJI STEP RESPONSE)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_bg(s5, C_BG_LIGHT)
    add_header(s5, "Identifikasi Sistem: Menghitung K, L, dan τ dari Eksperimen", "Lecture 6 Alignment — Step Response Analysis")

    # Left Card: Metodologi Uji Terbuka
    add_card_box(s5, Inches(0.8), Inches(1.65), Inches(5.6), Inches(5.1), bg_color=C_WHITE, border_color=C_BORDER_LIGHT)
    lines_open = [
        ("Prosedur Uji Kurva Reaksi (Open-Loop)", 16, True, C_TEXT_DARK, 8),
        ("Bukan Data Asumsi / Tebakan Internet:", 12, True, C_TEXT_BODY, 6),
        ("1. Kondisi Awal:", 12, True, C_TEXT_BODY, 2),
        ("   Ruang miniatur silo diisi gas hingga nilai stabil (y0 = 2800 ADC).", 12, False, C_TEXT_MUTED, 6),
        ("2. Masukan Undak (Step Input):", 12, True, C_TEXT_BODY, 2),
        ("   Kipas diberi lonjakan daya konstan (Δu = 200 PWM) dan servo membuka katup 90°.", 12, False, C_TEXT_MUTED, 6),
        ("3. Rekam Data:", 12, True, C_TEXT_BODY, 2),
        ("   Catat nilai pembacaan sensor MQ-135 tiap detik sampai kurva stabil di nilai akhir (yss = 1600 ADC).", 12, False, C_TEXT_MUTED, 6),
        ("4. Ekstraksi Ilmiah:", 12, True, C_TEXT_BODY, 2),
        ("   Hitung parameter K, L, dan τ langsung dari grafik respons waktu.", 12, False, C_TEXT_MUTED, 0)
    ]
    add_card_text(s5, Inches(0.8), Inches(1.65), Inches(5.6), Inches(5.1), lines_open)

    # Right Card: Rumus Ekstraksi Parameter
    add_card_box(s5, Inches(6.9), Inches(1.65), Inches(5.6), Inches(5.1), bg_color=C_WHITE, border_color=C_TEAL)
    lines_calc = [
        ("Rumus Ekstraksi Parameter Orde-1", 16, True, C_TEAL, 8),
        ("1. Rumus Gain Statis Sistem (K):", 12, True, C_TEXT_BODY, 2),
        ("   K = Δy / Δu = (y0 - yss) / Δu", 12, True, C_TEXT_DARK, 2),
        ("   K = (2800 - 1600) / 200 = 1200 / 200 = 6.0 ADC/PWM", 12, False, C_TEXT_MUTED, 8),
        ("2. Rumus Dead Time (L / Waktu Tunda):", 12, True, C_TEXT_BODY, 2),
        ("   L = t_reaksi - t_step_mulai = 1.5 detik", 12, False, C_TEXT_MUTED, 8),
        ("3. Rumus Konstanta Waktu (τ - Aturan 63.2% Lecture 6):", 12, True, C_TEXT_BODY, 2),
        ("   Δy_63.2% = 0.632 · (y0 - yss) = 0.632 · 1200 = 758.4", 12, False, C_TEXT_MUTED, 2),
        ("   y_target = 2800 - 758.4 = 2041.6 ADC", 12, False, C_TEXT_MUTED, 2),
        ("   τ = t(pada y=2041.6) - L = 8.5 s - 1.5 s = 7.0 detik", 12, False, C_TEXT_MUTED, 8),
        ("Fungsi Alih Riil: G(s) = [ 6.0 / (7.0s + 1) ] · e^(-1.5s)", 13, True, C_GREEN, 0)
    ]
    add_card_text(s5, Inches(6.9), Inches(1.65), Inches(5.6), Inches(5.1), lines_calc)

    # =========================================================================
    # SLIDE 6: FORMULA PENALAAN PID ZIEGLER-NICHOLS
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_bg(s6, C_BG_LIGHT)
    add_header(s6, "Perancangan Kontroler: Formula Penalaan Ziegler-Nichols", "Controller Tuning — Reaction Curve Method")

    # Left Card: Rumus Tuning Resmi
    add_card_box(s6, Inches(0.8), Inches(1.65), Inches(6.0), Inches(5.1), bg_color=C_WHITE, border_color=C_NAVY)
    lines_zn = [
        ("Perhitungan Matematis Nilai Kp, Ki, Kd", 16, True, C_TEXT_DARK, 8),
        ("Berdasarkan Parameter Riil: K = 6.0, τ = 7.0 s, L = 1.5 s", 12, True, C_TEXT_BODY, 6),
        ("1. Penguatan Proporsional (Kp):", 12, True, C_TEXT_BODY, 2),
        ("   Kp = 1.2 · (τ / (K · L))", 12, True, C_TEXT_DARK, 2),
        ("   Kp = 1.2 · (7.0 / (6.0 · 1.5)) = 8.4 / 9.0 ≈ 0.933", 12, False, C_TEXT_MUTED, 8),
        ("2. Waktu & Penguatan Integral (Ti & Ki):", 12, True, C_TEXT_BODY, 2),
        ("   Ti = 2 · L = 2 · 1.5 = 3.0 detik", 12, False, C_TEXT_MUTED, 2),
        ("   Ki = Kp / Ti = 0.933 / 3.0 ≈ 0.311 s⁻¹", 12, True, C_TEXT_DARK, 8),
        ("3. Waktu & Penguatan Derivatif (Td & Kd):", 12, True, C_TEXT_BODY, 2),
        ("   Td = 0.5 · L = 0.5 · 1.5 = 0.75 detik", 12, False, C_TEXT_MUTED, 2),
        ("   Kd = Kp · Td = 0.933 · 0.75 ≈ 0.700 s", 12, True, C_TEXT_DARK, 8),
        ("Seluruh nilai terhitung analitik dari sifat fisik boks!", 12, True, C_GREEN, 0)
    ]
    add_card_text(s6, Inches(0.8), Inches(1.65), Inches(6.0), Inches(5.1), lines_zn)

    # Right Card: Bedah Fungsi P, I, D
    add_card_box(s6, Inches(7.2), Inches(1.65), Inches(5.3), Inches(5.1), bg_color=C_WHITE, border_color=C_AMBER)
    lines_roles = [
        ("Bedah Peran P, I, dan D dalam Silo", 16, True, C_AMBER, 8),
        ("• Kenapa Tidak Cukup P Saja?", 12, True, C_TEXT_BODY, 2),
        ("Jika hanya P, saat gas mendekati batas aman, selisih error kecil sehingga daya kipas melemah dan gas NYANGKUT (ada Steady-State Error ess ≠ 0).", 12, False, C_TEXT_MUTED, 8),
        ("• Peran Kritis Aksi Integral (I):", 12, True, C_TEXT_BODY, 2),
        ("Menjumlahkan sisa error terhadap waktu secara terus-menerus. Aksi ini menambah tenaga hembusan kipas perlahan sampai gas TURUN TUNTAS ke setpoint (ess = 0).", 12, False, C_TEXT_MUTED, 8),
        ("• Peran Kritis Aksi Derivatif (D):", 12, True, C_TEXT_BODY, 2),
        ("Melihat kecepatan laju penurunan gas (de/dt). Bertindak sebagai rem otomatis untuk mencegah overshoot dan meredam osilasi liar katup servo.", 12, False, C_TEXT_MUTED, 0)
    ]
    add_card_text(s6, Inches(7.2), Inches(1.65), Inches(5.3), Inches(5.1), lines_roles)

    # =========================================================================
    # SLIDE 7: ALGORITMA PID DISKRIT PADA ESP32
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_bg(s7, C_BG_LIGHT)
    add_header(s7, "Implementasi Algoritma: Persamaan Diskrit pada ESP32", "Digital Implementation — Difference Equations")

    # Left Card: Rumus Diskrit
    add_card_box(s7, Inches(0.8), Inches(1.65), Inches(5.6), Inches(5.1), bg_color=C_WHITE, border_color=C_TEAL)
    lines_disc = [
        ("Persamaan Beda Diskrit (Difference Eq.)", 16, True, C_TEAL, 8),
        ("Di mikrokontroler, persamaan kontinu dihitung tiap periode sampling Δt:", 12, True, C_TEXT_BODY, 6),
        ("1. Galat Saat Ini (k):", 12, True, C_TEXT_BODY, 2),
        ("   e[k] = r[k] - y[k]", 12, True, C_TEXT_DARK, 6),
        ("2. Suku Proporsional:", 12, True, C_TEXT_BODY, 2),
        ("   P[k] = Kp · e[k]", 12, True, C_TEXT_DARK, 6),
        ("3. Suku Integral (Metode Penjumlahan Euler):", 12, True, C_TEXT_BODY, 2),
        ("   I[k] = I[k-1] + Ki · e[k] · Δt", 12, True, C_TEXT_DARK, 6),
        ("4. Suku Derivatif (Metode Selisih Mundur Backward):", 12, True, C_TEXT_BODY, 2),
        ("   D[k] = Kd · (e[k] - e[k-1]) / Δt", 12, True, C_TEXT_DARK, 6),
        ("5. Total Sinyal Kendali:  u[k] = P[k] + I[k] + D[k]", 13, True, C_NAVY, 0)
    ]
    add_card_text(s7, Inches(0.8), Inches(1.65), Inches(5.6), Inches(5.1), lines_disc)

    # Right Card: Saturasi Aktuator & Anti-Windup
    add_card_box(s7, Inches(6.9), Inches(1.65), Inches(5.6), Inches(5.1), bg_color=C_WHITE, border_color=C_BORDER_LIGHT)
    lines_sat = [
        ("Saturasi Aktuator & Anti-Windup", 16, True, C_TEXT_DARK, 8),
        ("Batasan Fisik Hardware (Driver & Motor):", 12, True, C_TEXT_BODY, 6),
        ("• Sinyal PWM ESP32 dibatasi pada rentang 8-bit:", 12, True, C_TEXT_BODY, 2),
        ("  pwm_out = constrain(u[k], 0, 255)", 12, True, C_TEAL, 8),
        ("• Sudut Servo Katup Atap dibatasi mekanik:", 12, True, C_TEXT_BODY, 2),
        ("  sudut_servo = map(pwm_out, 0, 255, 0, 90)", 12, True, C_TEAL, 8),
        ("• Proteksi Anti-Windup:", 12, True, C_TEXT_BODY, 2),
        ("  Mencegah suku Integral membengkak saat aktuator sudah mencapai daya maksimum 255 PWM:", 12, False, C_TEXT_MUTED, 4),
        ("  if (u[k] >= 255 || u[k] <= 0) { I[k] = I[k-1]; }", 12, True, C_AMBER, 0)
    ]
    add_card_text(s7, Inches(6.9), Inches(1.65), Inches(5.6), Inches(5.1), lines_sat)

    # =========================================================================
    # SLIDE 8: RUMUS EVALUASI KINERJA & KESTABILAN
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_bg(s8, C_BG_LIGHT)
    add_header(s8, "Evaluasi Kinerja Respons Waktu & Bukti Teoretis ess = 0", "Lecture 6 & 7 Alignment — Steady-State Analysis")

    # Left Card: Metrik Respons Waktu
    add_card_box(s8, Inches(0.8), Inches(1.65), Inches(5.6), Inches(5.1), bg_color=C_WHITE, border_color=C_BORDER_LIGHT)
    lines_metrics = [
        ("1. Metrik Respons Waktu (Lecture 6)", 16, True, C_TEXT_DARK, 8),
        ("Parameter Kuantitatif Hasil Uji Closed-Loop:", 12, True, C_TEXT_BODY, 6),
        ("• Rise Time (tr / Waktu Naik):", 12, True, C_TEXT_BODY, 2),
        ("  Waktu yang dibutuhkan kurva untuk turun dari 10% ke 90% target eliminasi gas.", 12, False, C_TEXT_MUTED, 8),
        ("• Settling Time (ts / Waktu Tunak):", 12, True, C_TEXT_BODY, 2),
        ("  Waktu tempuh hingga gas menetap di rentang toleransi ±2% dari batas aman: ts ≈ 4 · τ", 12, False, C_TEXT_MUTED, 8),
        ("• Maximum Overshoot (%OS):", 12, True, C_TEXT_BODY, 2),
        ("  Evaluasi lonjakan bukaan katup dan penurunan gas berlebih.", 12, False, C_TEXT_MUTED, 2),
        ("  Sistem dirancang teredam kritis mendekati ζ ≈ 1 (tanpa osilasi).", 12, True, C_TEAL, 0)
    ]
    add_card_text(s8, Inches(0.8), Inches(1.65), Inches(5.6), Inches(5.1), lines_metrics)

    # Right Card: Pembuktian ess = 0
    add_card_box(s8, Inches(6.9), Inches(1.65), Inches(5.6), Inches(5.1), bg_color=C_WHITE, border_color=C_GREEN)
    lines_ess = [
        ("2. Pembuktian Matematis ess = 0", 16, True, C_GREEN, 8),
        ("Berdasarkan Teorema Nilai Akhir (Final Value Theorem):", 12, True, C_TEXT_BODY, 4),
        ("ess = lim(s->0) [ s · E(s) ] = lim(s->0) [ s · R(s) / (1 + C(s)G(s)) ]", 12, True, C_TEXT_DARK, 8),
        ("Untuk Masukan Undak R(s) = A / s:", 12, True, C_TEXT_BODY, 4),
        ("ess = lim(s->0) [ A / (1 + C(s)G(s)) ]", 12, True, C_TEXT_DARK, 8),
        ("Karena Kontroler PID Memiliki Aksi Integral (C(s) memuat Ki / s):", 12, True, C_TEXT_BODY, 4),
        ("lim(s->0) C(s)G(s) = ∞   (Sistem Tipe-1)", 13, True, C_TEAL, 8),
        ("Maka Galat Keadaan Tunak:", 12, True, C_TEXT_BODY, 2),
        ("ess = A / (1 + ∞) = 0 !", 15, True, C_GREEN, 8),
        ("Terbukti analitik: Aksi Integral menjamin gas turun tuntas ke setpoint!", 12, True, C_TEXT_BODY, 0)
    ]
    add_card_text(s8, Inches(6.9), Inches(1.65), Inches(5.6), Inches(5.1), lines_ess)

    # =========================================================================
    # SLIDE 9: KESIMPULAN ILMIAH (Dark Navy)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_bg(s9, C_NAVY)
    add_header(s9, "Ringkasan Rancang Bangun Sistem Kendali Silo", "Conclusion & Scientific Rigor", dark=True)

    summary_items = [
        ("Objek Kendali Jelas", "Plant fisik adalah volume udara atap silo (Headspace), dengan variabel gas MQ-135 sebagai feedback loop tertutup."),
        ("Pemodelan Ilmiah", "Fungsi alih orde-1 diturunkan dari kesetimbangan massa Continuous Stirred Volume dan Transformasi Laplace."),
        ("Bukan Angka Asumsi", "Nilai K, L, dan τ diukur langsung dari kurva reaksi open-loop 63.2% pada boks miniatur uji."),
        ("Penalaan Terbukti Stabil", "Konstanta Kp = 0.933, Ki = 0.311, Kd = 0.700 dihitung analitik via Ziegler-Nichols dan terbukti matematis menghasilkan ess = 0.")
    ]

    w_box = Inches(2.7)
    gap = Inches(0.3)
    start_x = Inches(0.8)

    for i, (stitle, sdesc) in enumerate(summary_items):
        sx = start_x + i * (w_box + gap)
        add_card_box(s9, sx, Inches(2.0), w_box, Inches(4.5), bg_color=C_CARD_DARK, border_color=C_TEAL if i == 0 else RGBColor(51, 65, 85))
        lines_s = [
            (f"POIN 0{i+1}", 11, True, C_TEAL, 12),
            (stitle, 16, True, C_WHITE, 12),
            (sdesc, 12, False, RGBColor(148, 163, 184), 0)
        ]
        add_card_text(s9, sx, Inches(2.0), w_box, Inches(4.5), lines_s, pad=Inches(0.3))

    out_file = "Sistem_Kendali_Silo_Rumus_Lengkap.pptx"
    prs.save(out_file)
    print(f"File saved successfully: {out_file}")

if __name__ == "__main__":
    generate_deck()
