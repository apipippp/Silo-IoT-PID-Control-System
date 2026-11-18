import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # Blank layout

    # Color Palette
    C_NAVY = RGBColor(15, 23, 42)       # #0F172A
    C_CARD_DARK = RGBColor(30, 41, 59)  # #1E293B
    C_BG_LIGHT = RGBColor(248, 250, 252) # #F8FAFC
    C_WHITE = RGBColor(255, 255, 255)
    C_TEAL = RGBColor(14, 165, 233)     # #0EA5E9 (Accent)
    C_TEXT_DARK = RGBColor(15, 23, 42)
    C_TEXT_MUTED = RGBColor(100, 116, 139) # #64748B
    C_BORDER_LIGHT = RGBColor(226, 232, 240)
    C_AMBER = RGBColor(245, 158, 11)    # #F59E0B
    C_GREEN = RGBColor(16, 185, 129)    # #10B981

    def add_background(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text, dark=False):
        # Category Tracker
        tb_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.35))
        tf_cat = tb_cat.text_frame
        tf_cat.word_wrap = True
        tf_cat.margin_left = tf_cat.margin_top = tf_cat.margin_right = tf_cat.margin_bottom = 0
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_TEAL if dark else C_TEAL
        p_cat.font.name = "Calibri"

        # Slide Title
        tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(11.7), Inches(0.65))
        tf_title = tb_title.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = C_WHITE if dark else C_TEXT_DARK
        p_title.font.name = "Calibri"

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Dark Navy)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    add_background(s1, C_NAVY)

    # Tag / Chip
    tag_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(3.8), Inches(0.4))
    tag_box.fill.solid()
    tag_box.fill.fore_color.rgb = C_CARD_DARK
    tag_box.line.color.rgb = C_TEAL
    tag_tf = tag_box.text_frame
    tag_p = tag_tf.paragraphs[0]
    tag_p.text = "PROPOSAL PROYEK SISTEM KENDALI"
    tag_p.font.size = Pt(11)
    tag_p.font.bold = True
    tag_p.font.color.rgb = C_TEAL
    tag_p.alignment = PP_ALIGN.CENTER

    # Main Title
    t_box = s1.shapes.add_textbox(Inches(0.8), Inches(2.2), Inches(11.7), Inches(1.8))
    t_tf = t_box.text_frame
    t_tf.word_wrap = True
    t_tf.margin_left = t_tf.margin_top = t_tf.margin_right = t_tf.margin_bottom = 0
    tp = t_tf.paragraphs[0]
    tp.text = "Rancang Bangun Sistem Kendali Tertutup\nAerasi Silo Bahan Baku Berbasis IoT"
    tp.font.size = Pt(36)
    tp.font.bold = True
    tp.font.color.rgb = C_WHITE
    tp.font.name = "Calibri"

    # Subtitle
    sub_box = s1.shapes.add_textbox(Inches(0.8), Inches(4.3), Inches(11.7), Inches(1.0))
    sub_tf = sub_box.text_frame
    sub_tf.word_wrap = True
    sub_tf.margin_left = sub_tf.margin_top = sub_tf.margin_right = sub_tf.margin_bottom = 0
    sub_p = sub_tf.paragraphs[0]
    sub_p.text = "Integrasi Closed-Loop PID Control, Pemodelan Fungsi Alih Orde-1, dan Telemetri Real-Time MQTT untuk Preservasi Kualitas Bahan Baku Curah (SCM)"
    sub_p.font.size = Pt(16)
    sub_p.font.color.rgb = RGBColor(148, 163, 184) # Slate 400
    sub_p.font.name = "Calibri"

    # Presenter Card
    card_p = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.6), Inches(11.7), Inches(1.1))
    card_p.fill.solid()
    card_p.fill.fore_color.rgb = C_CARD_DARK
    card_p.line.color.rgb = RGBColor(51, 65, 85)
    cp_tf = card_p.text_frame
    cp_tf.margin_left = Inches(0.4)
    cp_tf.margin_top = Inches(0.2)
    cp_p1 = cp_tf.paragraphs[0]
    cp_p1.text = "Mata Kuliah: Sistem Kendali & Arsitektur IoT  |  Gasal 2026"
    cp_p1.font.size = Pt(14)
    cp_p1.font.bold = True
    cp_p1.font.color.rgb = C_WHITE
    cp_p2 = cp_tf.add_paragraph()
    cp_p2.text = "Dosen Pengampu: Ucky Pradestha N, M.Kom  |  Presenter: Manuel & Tim"
    cp_p2.font.size = Pt(13)
    cp_p2.font.color.rgb = C_TEAL

    # =========================================================================
    # SLIDE 2: LATAR BELAKANG & PROBLEM STATEMENT
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_background(s2, C_BG_LIGHT)
    add_header(s2, "Latar Belakang & Masalah Sistem Konvensional", "Problem Context — Raw Material Silo")

    # 3 Cards
    # Card 1: Konteks Silo
    c1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(3.64), Inches(4.8))
    c1.fill.solid()
    c1.fill.fore_color.rgb = C_WHITE
    c1.line.color.rgb = C_BORDER_LIGHT
    tf1 = c1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_right = tf1.margin_top = Inches(0.3)
    p = tf1.paragraphs[0]
    p.text = "1. Karakteristik Silo"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p2 = tf1.add_paragraph()
    p2.text = "\n• Bahan Baku Curah (Bulk):\nMenyimpan biji-bijian, tepung, atau pelet pakan ternak.\n\n• Risiko Kerusakan:\nBahan bersifat higroskopis. Kelembapan tinggi memicu jamur dan fermentasi anaerobik yang menghasilkan gas berbahaya (CO2, alkohol, bau busuk).\n\n• Headspace Stagnant:\nGas terperangkap di atap silo dan memicu 'roof sweating' (kondensasi tetesan air) yang merusak bahan baku."
    p2.font.size = Pt(13)
    p2.font.color.rgb = C_TEXT_MUTED

    # Card 2: Masalah Saklar On-Off
    c2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.84), Inches(1.8), Inches(3.64), Inches(4.8))
    c2.fill.solid()
    c2.fill.fore_color.rgb = C_WHITE
    c2.line.color.rgb = C_AMBER
    tf2 = c2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_right = tf2.margin_top = Inches(0.3)
    p = tf2.paragraphs[0]
    p.text = "2. Kelemahan On-Off"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_AMBER
    p2 = tf2.add_paragraph()
    p2.text = "\n• Histeresis / Bang-Bang:\nKontrol relay biasa hanya bekerja 0% atau 100% saat tembus batas threshold.\n\n• Bahaya Dust Explosion:\nKipas yang langsung menyala 100% mendadak menimbulkan hembusan turbulen keras yang menerbangkan serbuk halus (debu suspensi rawan ledak).\n\n• Flapping & Boros Energi:\nRelay berbunyi cetak-cetek saat nilai sensor fluktuatif di sekitar garis ambang batas."
    p2.font.size = Pt(13)
    p2.font.color.rgb = C_TEXT_MUTED

    # Card 3: Solusi Closed-Loop
    c3 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.88), Inches(1.8), Inches(3.64), Inches(4.8))
    c3.fill.solid()
    c3.fill.fore_color.rgb = C_WHITE
    c3.line.color.rgb = C_GREEN
    tf3 = c3.text_frame
    tf3.word_wrap = True
    tf3.margin_left = tf3.margin_right = tf3.margin_top = Inches(0.3)
    p = tf3.paragraphs[0]
    p.text = "3. Solusi Proyek Kami"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_GREEN
    p2 = tf3.add_paragraph()
    p2.text = "\n• Closed-Loop PID Control:\nKecepatan kipas (PWM) dan sudut katup atap (Servo) diatur secara halus dan kontinu proporsional terhadap selisih gas.\n\n• Smooth Airflow Transition:\nAliran udara dinaikkan perlahan sehingga membuang gas tuntas tanpa menerbangkan serbuk bahan baku.\n\n• Parameter Terhitung Ilmiah:\nKonstanta PID dihitung dari kurva reaksi fisik alat, bukan hasil asumsi/trial-error liar."
    p2.font.size = Pt(13)
    p2.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 3: INTEGRASI ARSITEKTUR: IOT VS SISTEM KENDALI
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_background(s3, C_BG_LIGHT)
    add_header(s3, "Pemisahan Domain: Arsitektur IoT vs Sistem Kendali", "System Architecture & Scoping")

    # Left Container: IoT Layer (Supervisory)
    left_c = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
    left_c.fill.solid()
    left_c.fill.fore_color.rgb = C_WHITE
    left_c.line.color.rgb = C_TEAL
    ltf = left_c.text_frame
    ltf.word_wrap = True
    ltf.margin_left = ltf.margin_right = ltf.margin_top = Inches(0.35)
    lp1 = ltf.paragraphs[0]
    lp1.text = "LEVEL 1: IOT SUPERVISORY LAYER"
    lp1.font.size = Pt(16)
    lp1.font.bold = True
    lp1.font.color.rgb = C_TEAL
    lp2 = ltf.add_paragraph()
    lp2.text = "\nPeran: Akuisisi Data Lingkungan & Manajemen Gudang\n\n• Hardware:\n  - Sensor DHT22 (Monitoring Suhu & Kelembapan)\n  - Sensor MQ135 (Monitoring Indikator Gas Fermentasi)\n  - Modul WiFi ESP32 & MQTT Protocol\n\n• Fungsi Kerja:\n  - Membaca kondisi fisik ruang silo tiap interval 3 detik\n  - Menentukan status risiko bahan baku (NORMAL / WARNING / CRITICAL)\n  - Mem-publish payload JSON ke broker MQTT (HiveMQ)\n  - Menyajikan grafik pemantauan real-time ke Web Dashboard SCM\n  - Menerima konfigurasi Setpoint dan remote tuning dari operator"
    lp2.font.size = Pt(13)
    lp2.font.color.rgb = C_TEXT_MUTED

    # Right Container: Control System Layer
    right_c = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.8), Inches(5.6), Inches(4.8))
    right_c.fill.solid()
    right_c.fill.fore_color.rgb = C_WHITE
    right_c.line.color.rgb = C_NAVY
    rtf = right_c.text_frame
    rtf.word_wrap = True
    rtf.margin_left = rtf.margin_right = rtf.margin_top = Inches(0.35)
    rp1 = rtf.paragraphs[0]
    rp1.text = "LEVEL 2: CLOSED-LOOP CONTROL LAYER"
    rp1.font.size = Pt(16)
    rp1.font.bold = True
    rp1.font.color.rgb = C_NAVY
    rp2 = rtf.add_paragraph()
    rp2.text = "\nPeran: Eksekusi Dinamis Kualitas Udara Silo (Otomasi)\n\n• Komponen Kendali:\n  - Setpoint: Ambang batas toleransi gas/suhu aman (r)\n  - Feedback Sensor: Pembacaan aktual gas MQ135 (y)\n  - Komparator: Menghitung nilai galat / error e(t) = r(t) - y(t)\n  - Kontroler: Algoritma PID di firmware ESP32\n  - Aktuator: Driver MOSFET (PWM Motor Fan) + Servo Damper\n\n• Fungsi Kerja:\n  - Memodulasi daya motor kipas (0-255 PWM) secara halus\n  - Mengatur sudut bukaan katup pembuangan atap (0° - 90°)\n  - Menghilangkan Steady-State Error sehingga gas turun tuntas\n  - Menolak gangguan fisik (Disturbance Rejection)"
    rp2.font.size = Pt(13)
    rp2.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 4: ELEMEN SISTEM KENDALI & BLOK DIAGRAM
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_background(s4, C_BG_LIGHT)
    add_header(s4, "Anatomi Blok Diagram Sistem Kendali Tertutup", "Lecture 2 & 5 Alignment — Closed-Loop Elements")

    # Diagram Row (5 boxes connected)
    # Box 1: Setpoint
    b_sp = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(2.0), Inches(1.4))
    b_sp.fill.solid()
    b_sp.fill.fore_color.rgb = C_WHITE
    b_sp.line.color.rgb = C_TEAL
    b_sp_tf = b_sp.text_frame
    b_sp_tf.margin_top = Inches(0.2)
    p = b_sp_tf.paragraphs[0]
    p.text = "SETPOINT r(t)\nBatas Gas Aman\n(Misal: 1500 ADC)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.alignment = PP_ALIGN.CENTER

    # Box 2: Komparator + PID
    b_pid = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.3), Inches(1.8), Inches(2.7), Inches(1.4))
    b_pid.fill.solid()
    b_pid.fill.fore_color.rgb = C_NAVY
    b_pid.line.color.rgb = C_NAVY
    b_pid_tf = b_pid.text_frame
    b_pid_tf.margin_top = Inches(0.15)
    p = b_pid_tf.paragraphs[0]
    p.text = "KONTROLER PID\n(Firmware ESP32)\nu(t) = Kp e + Ki∫e + Kd de/dt"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.alignment = PP_ALIGN.CENTER

    # Box 3: Aktuator
    b_act = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.5), Inches(1.8), Inches(2.7), Inches(1.4))
    b_act.fill.solid()
    b_act.fill.fore_color.rgb = C_WHITE
    b_act.line.color.rgb = C_AMBER
    b_act_tf = b_act.text_frame
    b_act_tf.margin_top = Inches(0.2)
    p = b_act_tf.paragraphs[0]
    p.text = "AKTUATOR\n• Driver MOSFET (PWM Fan)\n• Servo SG90 (Katup Atap)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.alignment = PP_ALIGN.CENTER

    # Box 4: Plant
    b_plt = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.7), Inches(1.8), Inches(2.8), Inches(1.4))
    b_plt.fill.solid()
    b_plt.fill.fore_color.rgb = C_WHITE
    b_plt.line.color.rgb = C_GREEN
    b_plt_tf = b_plt.text_frame
    b_plt_tf.margin_top = Inches(0.2)
    p = b_plt_tf.paragraphs[0]
    p.text = "PLANT FISIK G(s)\nVolume Ruang Silo &\nDinamika Udara Gas"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.alignment = PP_ALIGN.CENTER

    # Bottom Box: Feedback Sensor
    b_fb = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.5), Inches(3.6), Inches(4.5), Inches(1.1))
    b_fb.fill.solid()
    b_fb.fill.fore_color.rgb = C_WHITE
    b_fb.line.color.rgb = C_TEAL
    b_fb_tf = b_fb.text_frame
    b_fb_tf.margin_top = Inches(0.15)
    p = b_fb_tf.paragraphs[0]
    p.text = "SENSOR FEEDBACK H(s): SENSOR MQ135\nMembaca konsentrasi gas aktual di dalam silo secara real-time"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    p.alignment = PP_ALIGN.CENTER

    # Table of 5 Canonical Elements
    table_shape = s4.shapes.add_table(5, 3, Inches(0.8), Inches(5.0), Inches(11.7), Inches(1.8))
    table = table_shape.table
    table.columns[0].width = Inches(2.2)
    table.columns[1].width = Inches(3.5)
    table.columns[2].width = Inches(6.0)

    headers = ["Elemen Standar", "Realisasi di Proyek", "Fungsi dalam Sistem"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = C_WHITE

    rows_data = [
        ("1. Input Acuan (r)", "Setpoint Gas (misal 1500 ADC)", "Target kondisi batas aman konsentrasi gas yang diizinkan di silo."),
        ("2. Kontroler C(s)", "Algoritma PID di ESP32", "Menghitung sinyal koreksi u(t) dari error e(t) secara proporsional, integral, derivatif."),
        ("3. Aktuator", "Driver MOSFET & Micro Servo", "Mengubah sinyal logika ESP32 menjadi hembusan kipas kontinu dan posisi katup."),
        ("4. Plant G(s) & Sensor", "Boks Silo & Sensor MQ135", "Sistem fisik yang dibersihkan, dengan pembacaan sensor sebagai loop umpan balik.")
    ]
    for r_idx, row in enumerate(rows_data, start=1):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(11)
            p.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 5: APA YANG DIHITUNG? PEMODELAN FUNGSI ALIH
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_background(s5, C_BG_LIGHT)
    add_header(s5, "Identifikasi Sistem: Pemodelan Fungsi Alih dari Data Riil", "Lecture 4 & 6 Alignment — Transfer Function")

    # Left Card: Uji Step Response Open Loop
    c_step = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
    c_step.fill.solid()
    c_step.fill.fore_color.rgb = C_WHITE
    c_step.line.color.rgb = C_BORDER_LIGHT
    stf = c_step.text_frame
    stf.word_wrap = True
    stf.margin_left = stf.margin_right = stf.margin_top = Inches(0.35)
    p = stf.paragraphs[0]
    p.text = "1. Prosedur Uji Step Response (Open-Loop)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p2 = stf.add_paragraph()
    p2.text = "\nMetode Ilmiah (Bukan Asumsi / Karangan):\n\n1. Miniatur silo diisi sedikit gas uji hingga pembacaan MQ135 stabil di nilai tinggi (misal: y0 = 2800 ADC).\n\n2. Kipas diberi masukan undak konstan (Step Input, misal Δu = 200 PWM) dan servo membuka katup 90°.\n\n3. Catat nilai pembacaan gas MQ135 tiap detik di Serial Plotter / CSV sampai stabil di nilai akhir (yss = 1600 ADC).\n\n4. Plot kurva respons penurunan gas terhadap waktu untuk mengekstrak parameter fisik boks silo."
    p2.font.size = Pt(13)
    p2.font.color.rgb = C_TEXT_MUTED

    # Right Card: Ekstraksi Parameter Orde-1
    c_param = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.8), Inches(5.6), Inches(4.8))
    c_param.fill.solid()
    c_param.fill.fore_color.rgb = C_WHITE
    c_param.line.color.rgb = C_TEAL
    ptf = c_param.text_frame
    ptf.word_wrap = True
    ptf.margin_left = ptf.margin_right = ptf.margin_top = Inches(0.35)
    p = ptf.paragraphs[0]
    p.text = "2. Perhitungan Parameter Orde-1 (Lecture 6)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    p2 = ptf.add_paragraph()
    p2.text = "\nDari kurva hasil pengukuran riil, dihitung 3 parameter fisik:\n\n• Gain Statis Sistem (K):\n  K = Δy / Δu = (2800 - 1600) / 200 = 6.0 ADC/PWM\n\n• Waktu Tunda / Dead Time (L):\n  Jeda waktu sejak kipas menyala sampai nilai gas mulai turun pertama kali (misal: L = 1.5 detik).\n\n• Konstanta Waktu (τ / Tau - Aturan 63.2%):\n  Waktu yang dibutuhkan sistem untuk mencapai 63.2% dari total penurunan gas. Didapatkan τ = 7.0 detik.\n\nFungsi Alih Fisik Silo:\n  G(s) = K / (τ s + 1) · e^(-Ls) = 6.0 / (7.0s + 1) · e^(-1.5s)"
    p2.font.size = Pt(13)
    p2.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 6: PENALAAN PID BERBASIS ZIEGLER-NICHOLS
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_background(s6, C_BG_LIGHT)
    add_header(s6, "Perancangan Kontroler: Penalaan PID Ziegler-Nichols", "Controller Design — Tuning & Justification")

    # Left Container: Rumus Penalaan
    c_zn = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(6.0), Inches(4.8))
    c_zn.fill.solid()
    c_zn.fill.fore_color.rgb = C_WHITE
    c_zn.line.color.rgb = C_NAVY
    ztf = c_zn.text_frame
    ztf.word_wrap = True
    ztf.margin_left = ztf.margin_right = ztf.margin_top = Inches(0.35)
    p = ztf.paragraphs[0]
    p.text = "Perhitungan Parameter Kp, Ki, Kd"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p2 = ztf.add_paragraph()
    p2.text = "\nMenggunakan Formula Kurva Reaksi Ziegler-Nichols:\n\n1. Proportional Gain (Kp):\n   Kp = 1.2 · τ / (K · L)\n   Kp = 1.2 · 7.0 / (6.0 · 1.5) = 8.4 / 9.0 ≈ 0.933\n\n2. Integral Time & Gain (Ti & Ki):\n   Ti = 2 · L = 2 · 1.5 = 3.0 detik\n   Ki = Kp / Ti = 0.933 / 3.0 ≈ 0.311\n\n3. Derivative Time & Gain (Td & Kd):\n   Td = 0.5 · L = 0.5 · 1.5 = 0.75 detik\n   Kd = Kp · Td = 0.933 · 0.75 ≈ 0.700\n\nSemua nilai diturunkan matematis dari fisik alat riil!"
    p2.font.size = Pt(13)
    p2.font.color.rgb = C_TEXT_MUTED

    # Right Container: Kenapa Harus PID?
    c_why = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.2), Inches(1.8), Inches(5.3), Inches(4.8))
    c_why.fill.solid()
    c_why.fill.fore_color.rgb = C_WHITE
    c_why.line.color.rgb = C_AMBER
    wtf = c_why.text_frame
    wtf.word_wrap = True
    wtf.margin_left = wtf.margin_right = wtf.margin_top = Inches(0.35)
    p = wtf.paragraphs[0]
    p.text = "Mengapa Harus PID? (Bukan Rumus Biasa)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_AMBER
    p2 = wtf.add_paragraph()
    p2.text = "\n• Kenapa Tidak Cukup Hanya P?\nJika hanya P, saat gas mendekati batas aman, tenaga kipas melemah sehingga gas NYANGKUT (ada Steady-State Error ess ≠ 0).\n\n• Peran Aksi Integral (I):\nMenjumlahkan sisa error terhadap waktu, terus menambah daya kipas perlahan sampai gas benar-benar turun tuntas ke batas aman (ess = 0).\n\n• Peran Aksi Derivatif (D):\nMembaca kecepatan laju penurunan gas, bertindak sebagai rem peredam untuk mencegah overshoot dan osilasi liar."
    p2.font.size = Pt(13)
    p2.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 7: RENCANA PENGUJIAN RESPON WAKTU
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_background(s7, C_BG_LIGHT)
    add_header(s7, "Rencana Pengujian Kinerja: Analisis Respons Waktu", "Lecture 6 & 7 Alignment — Performance Evaluation")

    # 4 Evaluation Cards (2x2 Grid)
    cards_data = [
        ("Rise Time (tr) & Settling Time (ts)", "Kecepatan Respon Sistem", "Mengukur waktu dari 10% ke 90% penurunan gas, dan waktu tempuh hingga kondisi udara silo stabil di toleransi 2% di bawah batas aman."),
        ("Steady-State Error (ess = 0)", "Ketuntasan Eliminasi Gas", "Membuktikan secara kuantitatif bahwa nilai konsentrasi gas akhir persis berada di garis target setpoint tanpa menyisakan gas berbahaya."),
        ("Maximum Overshoot (%OS)", "Peredaman & Kestabilan Katup", "Memastikan hembusan kipas dan bukaan servo katup teredam halus (critically damped) tanpa mengalami osilasi buka-tutup berulang."),
        ("Disturbance Rejection Test", "Uji Ketahanan Gangguan Fisik", "Memberikan gangguan mendadak (misal meniupkan gas tambahan atau menutup sebagian katup), lalu membuktikan PID otomatis mengembalikan sistem ke target.")
    ]

    coords = [
        (Inches(0.8), Inches(1.8)),
        (Inches(6.9), Inches(1.8)),
        (Inches(0.8), Inches(4.3)),
        (Inches(6.9), Inches(4.3))
    ]

    for (x, y), (title, sub, desc) in zip(coords, cards_data):
        c = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.6), Inches(2.3))
        c.fill.solid()
        c.fill.fore_color.rgb = C_WHITE
        c.line.color.rgb = C_BORDER_LIGHT
        ctf = c.text_frame
        ctf.word_wrap = True
        ctf.margin_left = ctf.margin_right = ctf.margin_top = Inches(0.25)
        p = ctf.paragraphs[0]
        p.text = title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = C_NAVY
        p_sub = ctf.add_paragraph()
        p_sub.text = sub.upper()
        p_sub.font.size = Pt(10)
        p_sub.font.bold = True
        p_sub.font.color.rgb = C_TEAL
        p_desc = ctf.add_paragraph()
        p_desc.text = "\n" + desc
        p_desc.font.size = Pt(12)
        p_desc.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 8: KESIMPULAN & ROADMAP EKSEKUSI (Dark Navy)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_background(s8, C_NAVY)
    add_header(s8, "Kesimpulan & Tahapan Eksekusi Proyek", "Summary & Next Steps", dark=True)

    # 4 Sequential Steps (Process Flow)
    steps = [
        ("Tahap 1", "Upgrade Aktuator", "Mengganti relay mekanik ke Driver MOSFET PWM dan menambahkan 1 Micro Servo SG90 untuk katup atap."),
        ("Tahap 2", "Eksperimen Open-Loop", "Merekam kurva respons undak penurunan gas di Serial Plotter untuk ekstraksi parameter fisik K, L, dan τ."),
        ("Tahap 3", "Kalkulasi Matematis", "Menghitung nilai Kp, Ki, Kd menggunakan formula resmi Ziegler-Nichols dan memverifikasi stabilitas."),
        ("Tahap 4", "Integrasi Closed-Loop", "Menanamkan algoritma PID ke firmware ESP32 dan menampilkan grafik respons transien di Dashboard Web.")
    ]

    w_step = Inches(2.7)
    gap = Inches(0.3)
    start_x = Inches(0.8)

    for i, (num, stitle, sdesc) in enumerate(steps):
        sx = start_x + i * (w_step + gap)
        sc = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, sx, Inches(2.0), w_step, Inches(4.5))
        sc.fill.solid()
        sc.fill.fore_color.rgb = C_CARD_DARK
        sc.line.color.rgb = C_TEAL if i == 0 else RGBColor(51, 65, 85)
        sctf = sc.text_frame
        sctf.word_wrap = True
        sctf.margin_left = sctf.margin_right = sctf.margin_top = Inches(0.3)
        p1 = sctf.paragraphs[0]
        p1.text = num.upper()
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

    # Save Presentation
    output_filename = "Proposal_Sistem_Kendali_Silo_IoT.pptx"
    prs.save(output_filename)
    print(f"Presentation saved successfully as '{output_filename}'")

if __name__ == "__main__":
    create_presentation()
