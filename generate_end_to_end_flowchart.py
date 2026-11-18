import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_end_to_end_flowchart_xml():
    xml_content = """<mxfile host="app.diagrams.net" modified="2026-11-09T00:00:00.000Z" agent="Mozilla/5.0" version="21.6.8" type="device">
  <diagram id="flowchart_silo_conveyor" name="Alur Lengkap Silo &amp; Conveyor Terintegrasi">
    <mxGraphModel dx="1400" dy="1000" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1654" pageHeight="2339" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>

        <!-- TITLE CONTAINER -->
        <mxCell id="title_box" value="DIAGRAM ALUR KERJA LENGKAP: SMART SILO RAW MATERIAL DENGAN CONVEYOR PID &amp; SCANNING KAMERA" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#0F172A;strokeColor=#0EA5E9;strokeWidth=2;fontColor=#38BDF8;fontStyle=1;fontSize=14;" vertex="1" parent="1">
          <mxGeometry x="120" y="30" width="960" height="50" as="geometry"/>
        </mxCell>

        <!-- 1. START -->
        <mxCell id="start" value="START / POWER ON" style="ellipse;whiteSpace=wrap;html=1;fillColor=#0F172A;strokeColor=#0EA5E9;strokeWidth=2;fontColor=#FFFFFF;fontStyle=1;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="510" y="110" width="180" height="50" as="geometry"/>
        </mxCell>

        <!-- 2. INIT -->
        <mxCell id="init" value="Inisialisasi Sistem:&#xa;• Koneksi WiFi &amp; MQTT HiveMQ Broker&#xa;• Inisialisasi Sensor: DHT22, MQ-135, Ultrasonik (HC-SR04)&#xa;• Inisialisasi Aktuator: Motor Conveyor (PWM), 2 Fan (5V), Servo Hatch&#xa;• Standby Kamera Scanner (Webcam)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#38BDF8;strokeWidth=1.5;fontColor=#FFFFFF;fontSize=11;align=left;spacingLeft=12;" vertex="1" parent="1">
          <mxGeometry x="440" y="190" width="320" height="85" as="geometry"/>
        </mxCell>

        <!-- 3. DETEKSI BARANG DATANG -->
        <mxCell id="place_item" value="Bahan Mentah Kopi Diletakkan di Ujung Inlet Conveyor&#xa;Motor DC Kuning Mulai Berjalan Membawa Barang Menuju Pos Scan" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#F59E0B;strokeWidth=1.5;fontColor=#FFFFFF;fontSize=11;align=center;" vertex="1" parent="1">
          <mxGeometry x="440" y="310" width="320" height="55" as="geometry"/>
        </mxCell>

        <!-- 4. SCAN KAMERA -->
        <mxCell id="camera_scan" value="Barang Berada di Bawah Webcam:&#xa;Scanning Barcode / QR Code / Kualitas Fisik Bahan&#xa;(Merekap Data: ID Batch, Tanggal Panen, Grade Kopi)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#312E81;strokeColor=#818CF8;strokeWidth=2;fontColor=#FFFFFF;fontSize=11;align=center;" vertex="1" parent="1">
          <mxGeometry x="440" y="400" width="320" height="65" as="geometry"/>
        </mxCell>

        <!-- 5. DECISION SCAN -->
        <mxCell id="decision_scan" value="Hasil Scan Valid &amp;&#xa;Lolos Kualifikasi?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#F59E0B;strokeWidth=2;fontColor=#FFFFFF;fontSize=11;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="510" y="500" width="180" height="80" as="geometry"/>
        </mxCell>

        <!-- BRANCH ERROR / REJECT -->
        <mxCell id="reject_stop" value="MOTOR CONVEYOR STOP&#xa;Alarm Buzzer Bunyi + LED Merah Aktif&#xa;Kirim Notifikasi 'REJECT / SCAN ERROR' ke HP via MQTT" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#450A0A;strokeColor=#EF4444;strokeWidth=2;fontColor=#FCA5A5;fontSize=11;align=left;spacingLeft=10;" vertex="1" parent="1">
          <mxGeometry x="120" y="502.5" width="310" height="75" as="geometry"/>
        </mxCell>

        <mxCell id="manual_quarantine" value="INTERVENSI MANUAL (Human-in-the-Loop):&#xa;Operator Memindahkan Barang Secara Manual dengan Tangan&#xa;ke Keranjang Karantina / Reject" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#EF4444;strokeWidth=1.5;fontColor=#FFFFFF;fontSize=11;align=center;" vertex="1" parent="1">
          <mxGeometry x="120" y="615" width="310" height="60" as="geometry"/>
        </mxCell>

        <mxCell id="confirm_reset" value="Operator Menekan Tombol Reset / Konfirmasi di HP&#xa;Sistem Kembali Siaga untuk Barang Berikutnya" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#64748B;strokeWidth=1;fontColor=#CBD5E1;fontSize=10;align=center;" vertex="1" parent="1">
          <mxGeometry x="145" y="710" width="260" height="45" as="geometry"/>
        </mxCell>

        <!-- BRANCH VALID / SUCCESS -->
        <mxCell id="log_success" value="Data Bahan Baku Terekap &amp; Valid&#xa;Simpan ke Database SQLite &amp; Publish Telemetri ke HP&#xa;Conveyor Lanjut Berjalan Masuk ke Dalam Rumah Silo" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#064E3B;strokeColor=#10B981;strokeWidth=2;fontColor=#FFFFFF;fontSize=11;align=center;" vertex="1" parent="1">
          <mxGeometry x="440" y="620" width="320" height="60" as="geometry"/>
        </mxCell>

        <!-- 6. PID CONVEYOR LOOP -->
        <mxCell id="conveyor_pid" value="KENDALI PID POSISI/JARAK CONVEYOR:&#xa;1. Sensor Ultrasonik Mengukur Jarak Barang: d_aktual&#xa;2. Galat Posisi: Error = d_aktual - Setpoint_Silo (misal: 5 cm)&#xa;3. Sinyal Kendali: PWM = Kp·e + Ki·∫e·dt + Kd·(de/dt)&#xa;4. Respons: Mendekati Silo, Motor Melambat Halus (Teredam Kritis)&#xa;5. Berhenti Presisi Tepat di Setpoint (Zero Overshoot / Tidak Tabrak Dinding)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#0B192C;strokeColor=#0EA5E9;strokeWidth=2;fontColor=#FFFFFF;fontSize=11;align=left;spacingLeft=12;" vertex="1" parent="1">
          <mxGeometry x="410" y="720" width="380" height="105" as="geometry"/>
        </mxCell>

        <!-- 7. ITEM INSIDE SILO -->
        <mxCell id="item_settled" value="Barang Selesai Diposisikan di Dalam Silo&#xa;Motor Conveyor Dinonaktifkan (PWM = 0)&#xa;Sistem Memulai Monitoring Kualitas Lingkungan Internal Silo" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#10B981;strokeWidth=1.5;fontColor=#FFFFFF;fontSize=11;align=center;" vertex="1" parent="1">
          <mxGeometry x="440" y="865" width="320" height="60" as="geometry"/>
        </mxCell>

        <!-- 8. ENVIRONMENTAL SENSING -->
        <mxCell id="env_sensing" value="Monitoring Berdampingan: DHT22 (Suhu &amp; Lembap) &amp; MQ-135 (Gas)&#xa;Reaksi Biologis Kopi: Pembusukan = Fermentasi Eksotermik&#xa;(Gas Naik ➔ Suhu &amp; Kelembapan Ikut Naik Secara Simultan)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#38BDF8;strokeWidth=1.5;fontColor=#FFFFFF;fontSize=11;align=left;spacingLeft=10;" vertex="1" parent="1">
          <mxGeometry x="420" y="960" width="360" height="65" as="geometry"/>
        </mxCell>

        <!-- 9. DECISION SILO CLIMATE -->
        <mxCell id="decision_climate" value="Kondisi Silo Melebihi&#xa;Batas Setpoint Aman?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#F59E0B;strokeWidth=2;fontColor=#FFFFFF;fontSize=11;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="505" y="1060" width="190" height="80" as="geometry"/>
        </mxCell>

        <!-- BRANCH CLIMATE ACTION (ACTIVE) -->
        <mxCell id="action_aeration" value="AKTUASI AERASI &amp; VENTILASI DINAMIS:&#xa;• 2 Buah Kipas 5V Raspberry Pi Menyala (Modulasi PWM)&#xa;  Menyerap dan Membuang Kalor Panas &amp; Kelembapan Berlebih&#xa;• 1 Buah Servo Membuka Katup Atap Silo (0° ➔ 90°)&#xa;  Membuang Akumulasi Gas Pembusukan / Fermentasi Alami" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#0F172A;strokeColor=#0EA5E9;strokeWidth=2;fontColor=#FFFFFF;fontSize=11;align=left;spacingLeft=10;" vertex="1" parent="1">
          <mxGeometry x="420" y="1180" width="360" height="90" as="geometry"/>
        </mxCell>

        <!-- BRANCH CLIMATE NORMAL (STANDBY) -->
        <mxCell id="action_standby" value="KONDISI STABIL / NORMAL:&#xa;• 2 Kipas 5V Mati (Standby)&#xa;• Katup Servo Atap Menutup Rapat (0°)&#xa;• Menjaga Mutu Bahan Baku Tetap Higienis &amp; Hemat Energi" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#064E3B;strokeColor=#10B981;strokeWidth=1.5;fontColor=#FFFFFF;fontSize=11;align=left;spacingLeft=10;" vertex="1" parent="1">
          <mxGeometry x="830" y="1065" width="310" height="70" as="geometry"/>
        </mxCell>

        <!-- 10. TELEMETRY STREAMING -->
        <mxCell id="telemetry_pub" value="STREAMING TELEMETRI MQTT KE APLIKASI HP / WEB:&#xa;Kirim Payload JSON: Suhu, Kelembapan, Nilai Gas, Status Kipas,&#xa;Posisi Servo, dan Riwayat Data Bahan Baku&#xa;Operator Dapat Mengontrol Manual Jarak Jauh Jika Diperlukan" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#10B981;strokeWidth=1.5;fontColor=#FFFFFF;fontSize=11;align=left;spacingLeft=10;" vertex="1" parent="1">
          <mxGeometry x="420" y="1310" width="360" height="80" as="geometry"/>
        </mxCell>

        <!-- CONNECTORS / ARROWS -->
        <mxCell id="e1" edge="1" parent="1" source="start" target="init" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#38BDF8;strokeWidth=2;"/>
        <mxCell id="e2" edge="1" parent="1" source="init" target="place_item" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#38BDF8;strokeWidth=2;"/>
        <mxCell id="e3" edge="1" parent="1" source="place_item" target="camera_scan" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#38BDF8;strokeWidth=2;"/>
        <mxCell id="e4" edge="1" parent="1" source="camera_scan" target="decision_scan" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#38BDF8;strokeWidth=2;"/>

        <!-- Scan Reject Path -->
        <mxCell id="e_scan_no" value="ERROR / TIDAK VALID" edge="1" parent="1" source="decision_scan" target="reject_stop" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#EF4444;strokeWidth=2;fontColor=#EF4444;fontStyle=1;"/>
        <mxCell id="e_rej1" edge="1" parent="1" source="reject_stop" target="manual_quarantine" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#EF4444;strokeWidth=2;"/>
        <mxCell id="e_rej2" edge="1" parent="1" source="manual_quarantine" target="confirm_reset" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#64748B;strokeWidth=1.5;"/>
        <mxCell id="e_rej_loop" value="Kembali ke Siaga" edge="1" parent="1" source="confirm_reset" target="place_item" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#64748B;strokeWidth=1.5;fontColor=#94A3B8;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="80" y="732.5"/>
              <mxPoint x="80" y="337.5"/>
            </Array>
          </mxGeometry>
        </mxCell>

        <!-- Scan Valid Path -->
        <mxCell id="e_scan_yes" value="VALID / LOLOS" edge="1" parent="1" source="decision_scan" target="log_success" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#10B981;strokeWidth=2;fontColor=#10B981;fontStyle=1;"/>
        <mxCell id="e5" edge="1" parent="1" source="log_success" target="conveyor_pid" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#10B981;strokeWidth=2;"/>
        <mxCell id="e6" edge="1" parent="1" source="conveyor_pid" target="item_settled" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#38BDF8;strokeWidth=2;"/>
        <mxCell id="e7" edge="1" parent="1" source="item_settled" target="env_sensing" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#38BDF8;strokeWidth=2;"/>
        <mxCell id="e8" edge="1" parent="1" source="env_sensing" target="decision_climate" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#38BDF8;strokeWidth=2;"/>

        <!-- Climate Paths -->
        <mxCell id="e_clim_yes" value="YA (Gas / Suhu Naik)" edge="1" parent="1" source="decision_climate" target="action_aeration" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#EF4444;strokeWidth=2;fontColor=#EF4444;fontStyle=1;"/>
        <mxCell id="e_clim_no" value="TIDAK (Normal)" edge="1" parent="1" source="decision_climate" target="action_standby" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#10B981;strokeWidth=2;fontColor=#10B981;fontStyle=1;"/>
        
        <mxCell id="e9" edge="1" parent="1" source="action_aeration" target="telemetry_pub" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#38BDF8;strokeWidth=2;"/>
        <mxCell id="e10" edge="1" parent="1" source="action_standby" target="telemetry_pub" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#10B981;strokeWidth=2;entryX=1;entryY=0.5;entryDx=0;entryDy=0;">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="985" y="1350"/>
            </Array>
          </mxGeometry>
        </mxCell>

        <!-- Continuous Climate Loop -->
        <mxCell id="e_clim_loop" value="Loop Monitoring Berkelanjutan" edge="1" parent="1" source="telemetry_pub" target="env_sensing" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#0EA5E9;strokeWidth=1.5;strokeDashArray=3;fontColor=#38BDF8;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="360" y="1350"/>
              <mxPoint x="360" y="992.5"/>
            </Array>
          </mxGeometry>
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""
    filename = "diagram_alur_sistem_silo_conveyor.drawio"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(xml_content)
    print(f"Saved {filename}")

def render_end_to_end_png():
    fig, ax = plt.subplots(figsize=(13, 20), dpi=300)
    ax.set_facecolor("#0B132B")
    fig.patch.set_facecolor("#0B132B")

    # Title Banner
    r_title = patches.FancyBboxPatch((0.8, 19.1), 11.4, 0.7, boxstyle="round,pad=0.08,rounding_size=0.15",
                                     facecolor="#1E293B", edgecolor="#0EA5E9", linewidth=2.0)
    ax.add_patch(r_title)
    ax.text(6.5, 19.45, "DIAGRAM ALUR KERJA LENGKAP: SMART SILO RAW MATERIAL & CONVEYOR PID",
            color="#38BDF8", fontsize=11, fontweight="bold", ha="center", va="center")

    # Nodes definition: (id, xc, yc, w, h, text, bg, border, is_special)
    nodes = [
        ("start", 6.5, 18.4, 3.6, 0.6, "START / POWER ON", "#0F172A", "#0EA5E9", True),
        ("init", 6.5, 17.2, 6.6, 1.2, "Inisialisasi Hardware & Jaringan:\n• WiFi & MQTT HiveMQ Broker\n• Sensor: DHT22, MQ-135, Ultrasonik (HC-SR04)\n• Aktuator: Motor Conveyor (PWM), 2 Kipas 5V, Servo Hatch\n• Standby Kamera Scanner (Webcam)", "#1E293B", "#38BDF8", False),
        ("place", 6.5, 15.8, 6.6, 0.9, "Bahan Baku Kopi Diletakkan di Ujung Inlet Conveyor\nMotor DC Kuning Berjalan Membawa Barang Menuju Pos Scan", "#1E293B", "#F59E0B", False),
        ("scan", 6.5, 14.5, 6.6, 1.0, "Barang Berada Tepat di Bawah Webcam:\nScanning Barcode / QR Code / Kualitas Fisik Bahan\n(Merekap Data: ID Batch, Tanggal Panen, Grade Kopi)", "#312E81", "#818CF8", False),
        ("dec_scan", 6.5, 13.0, 3.8, 1.0, "Hasil Scan Valid &\nLolos Kualifikasi?", "#1E293B", "#F59E0B", True),
        
        # Reject Branch (Left)
        ("rej_stop", 2.2, 13.0, 3.4, 1.1, "MOTOR CONVEYOR STOP\nAlarm Buzzer + LED Merah\nNotifikasi 'REJECT / SCAN ERROR'\nke HP via MQTT", "#450A0A", "#EF4444", False),
        ("rej_man", 2.2, 11.4, 3.4, 1.1, "INTERVENSI MANUAL:\nOperator Memindahkan Barang\nSecara Manual dengan Tangan\nke Keranjang Karantina", "#1E293B", "#EF4444", False),
        ("rej_reset", 2.2, 10.0, 3.4, 0.8, "Operator Tekan Reset / Konfirmasi di HP\nSistem Siaga untuk Barang Baru", "#1E293B", "#64748B", False),
        
        # Valid Path (Center)
        ("valid_log", 6.5, 11.5, 6.6, 1.0, "Data Bahan Baku Terekap & Valid di SQLite\nPublish Status 'VALID' ke HP via MQTT\nConveyor Lanjut Masuk ke Dalam Silo", "#064E3B", "#10B981", False),
        ("pid_conv", 6.5, 9.8, 6.6, 1.6, "KENDALI PID POSISI / JARAK CONVEYOR:\n• Sensor Ultrasonik Mengukur Jarak: d_aktual\n• Galat: Error = d_aktual - Setpoint_Silo (5 cm)\n• PWM Motor = Kp·e + Ki·∫e·dt + Kd·(de/dt)\n• Motor Melambat Halus Mendekati Target (Teredam Kritis)\n• Berhenti Tepat di Setpoint (Zero Overshoot / Anti-Tabrak)", "#0B192C", "#0EA5E9", False),
        ("item_in", 6.5, 8.2, 6.6, 0.9, "Barang Berhenti Sempurna di Titik Simpan Silo\nMotor Conveyor Dinonaktifkan (PWM = 0)\nSistem Mulai Memantau Kualitas Udara Internal", "#1E293B", "#10B981", False),
        ("sensing", 6.5, 6.8, 6.6, 1.1, "Monitoring Berdampingan: DHT22 (Suhu/Lembap) & MQ-135 (Gas)\nPrinsip Biologis: Fermentasi = Reaksi Eksotermik Alami\n(Gas Fermentasi Naik ➔ Suhu & Kelembapan Naik Simultan)", "#1E293B", "#38BDF8", False),
        ("dec_clim", 6.5, 5.3, 3.8, 1.0, "Kondisi Silo Melebihi\nBatas Setpoint Aman?", "#1E293B", "#F59E0B", True),
        
        # Climate Branches
        ("act_aer", 6.5, 3.5, 6.6, 1.5, "AKTUASI AERASI & VENTILASI DINAMIS:\n• 2 Buah Kipas 5V Raspberry Pi Menyala (PWM)\n  Membuang Panas & Menurunkan Kelembapan\n• 1 Buah Servo Membuka Katup Atap (0° ➔ 90°)\n  Melepas Akumulasi Gas Pembusukan ke Luar", "#0F172A", "#0EA5E9", False),
        ("act_norm", 10.8, 5.3, 2.8, 1.0, "KONDISI NORMAL:\n• 2 Kipas 5V Mati\n• Katup Servo Tutup (0°)\n• Mutu Terjaga & Hemat Daya", "#064E3B", "#10B981", False),
        ("telemetry", 6.5, 1.8, 6.6, 1.1, "STREAMING TELEMETRI MQTT KE HP / WEB DASHBOARD:\nPublish JSON: Suhu, Lembap, Gas, Status Kipas, Posisi Servo, Status Batch\nOperator Dapat Memantau & Mengoverride Jarak Jauh", "#1E293B", "#10B981", False)
    ]

    for nid, xc, yc, w, h, text, bg, border, is_special in nodes:
        rect = patches.FancyBboxPatch((xc - w/2, yc - h/2), w, h,
                                      boxstyle="round,pad=0.08,rounding_size=0.15",
                                      facecolor=bg, edgecolor=border, linewidth=1.8)
        ax.add_patch(rect)
        ax.text(xc, yc, text, color="#FFFFFF", fontsize=8.5, ha="center", va="center",
                fontfamily="sans-serif", fontweight="bold" if is_special else "normal")

    # Connectors
    arrows = [
        ((6.5, 18.1), (6.5, 17.8)),
        ((6.5, 16.6), (6.5, 16.25)),
        ((6.5, 15.35), (6.5, 15.0)),
        ((6.5, 14.0), (6.5, 13.5)),
        # Decision Scan -> Reject (Left)
        ((4.6, 13.0), (3.9, 13.0)),
        ((2.2, 12.45), (2.2, 11.95)),
        ((2.2, 10.85), (2.2, 10.4)),
        # Decision Scan -> Valid (Down)
        ((6.5, 12.5), (6.5, 12.0)),
        ((6.5, 11.0), (6.5, 10.6)),
        ((6.5, 9.0), (6.5, 8.65)),
        ((6.5, 7.75), (6.5, 7.35)),
        ((6.5, 6.25), (6.5, 5.8)),
        # Climate decisions
        ((6.5, 4.8), (6.5, 4.25)),
        ((8.4, 5.3), (9.4, 5.3)),
        ((6.5, 2.75), (6.5, 2.35))
    ]

    for p1, p2 in arrows:
        ax.annotate("", xy=p2, xytext=p1,
                    arrowprops=dict(arrowstyle="-|>", color="#38BDF8", lw=1.8, mutation_scale=14))

    # Reject loop back to inlet
    ax.plot([0.5, 0.5, 3.2], [10.0, 15.8, 15.8], color="#EF4444", lw=1.5, linestyle="--")
    ax.plot([2.2, 0.5], [10.0, 10.0], color="#EF4444", lw=1.5, linestyle="--")
    ax.annotate("", xy=(3.2, 15.8), xytext=(2.9, 15.8),
                arrowprops=dict(arrowstyle="-|>", color="#EF4444", lw=1.5, mutation_scale=12))
    ax.text(0.6, 12.8, "Reset & Siap Terima Barang Baru", color="#FCA5A5", fontsize=8, rotation=90, va="center")

    # Standby connect to telemetry
    ax.plot([10.8, 10.8, 9.8], [4.8, 1.8, 1.8], color="#10B981", lw=1.5)
    ax.annotate("", xy=(9.8, 1.8), xytext=(10.0, 1.8),
                arrowprops=dict(arrowstyle="-|>", color="#10B981", lw=1.5, mutation_scale=12))

    # Climate monitoring loop back
    ax.plot([3.2, 3.2, 3.2], [1.8, 6.8, 6.8], color="#0EA5E9", lw=1.5, linestyle=":")
    ax.plot([4.2, 3.2], [1.8, 1.8], color="#0EA5E9", lw=1.5, linestyle=":")
    ax.annotate("", xy=(4.2, 6.8), xytext=(3.5, 6.8),
                arrowprops=dict(arrowstyle="-|>", color="#0EA5E9", lw=1.5, mutation_scale=12))
    ax.text(3.3, 4.3, "Loop Monitoring Berkelanjutan", color="#38BDF8", fontsize=8, rotation=90, va="center")

    # Labels for decisions
    ax.text(4.2, 13.2, "ERROR / TIDAK VALID", color="#EF4444", fontsize=8, fontweight="bold", ha="center")
    ax.text(6.9, 12.2, "VALID", color="#10B981", fontsize=8, fontweight="bold")
    ax.text(6.9, 4.5, "YA (Bahaya)", color="#EF4444", fontsize=8, fontweight="bold")
    ax.text(8.9, 5.5, "NORMAL", color="#10B981", fontsize=8, fontweight="bold")

    ax.set_xlim(0, 13)
    ax.set_ylim(0.5, 20.0)
    ax.axis("off")
    plt.tight_layout()
    png_filename = "diagram_alur_sistem_silo_conveyor.png"
    plt.savefig(png_filename, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"Saved {png_filename}")

if __name__ == "__main__":
    generate_end_to_end_flowchart_xml()
    render_end_to_end_png()
