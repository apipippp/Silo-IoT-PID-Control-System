import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_ultimate_xml():
    xml_content = """<mxfile host="app.diagrams.net" modified="2026-11-09T00:00:00.000Z" agent="Mozilla/5.0" version="21.6.8" type="device">
  <diagram id="ultimate_flowchart_silo" name="Diagram Alur Lengkap Sistem Silo &amp; Conveyor">
    <mxGraphModel dx="1600" dy="1200" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1920" pageHeight="2800" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>

        <!-- HEADER BANNER -->
        <mxCell id="header" value="DIAGRAM ALUR KERJA LENGKAP SISTEM SILO RAW MATERIAL DENGAN CONVEYOR PID &amp; QUALITY GATE KAMERA" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#0F172A;strokeColor=#0EA5E9;strokeWidth=2;fontColor=#38BDF8;fontStyle=1;fontSize=14;" vertex="1" parent="1">
          <mxGeometry x="140" y="30" width="1120" height="50" as="geometry"/>
        </mxCell>

        <!-- 1. START -->
        <mxCell id="start" value="START / POWER ON" style="ellipse;whiteSpace=wrap;html=1;fillColor=#0F172A;strokeColor=#0EA5E9;strokeWidth=2;fontColor=#FFFFFF;fontStyle=1;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="610" y="110" width="180" height="50" as="geometry"/>
        </mxCell>

        <!-- 2. INIT -->
        <mxCell id="init" value="Inisialisasi Sistem:&#xa;• Setup WiFi &amp; MQTT HiveMQ Broker (Client ID Unik)&#xa;• Inisialisasi Sensor: HC-SR04 (Ultrasonik), DHT22, MQ-135&#xa;• Inisialisasi Aktuator: Motor DC Conveyor (PWM), 2 Kipas 5V, Servo SG90&#xa;• Aktifkan Kamera Scanner (Webcam Inbound Station)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#38BDF8;strokeWidth=1.5;fontColor=#FFFFFF;fontSize=11;align=left;spacingLeft=12;" vertex="1" parent="1">
          <mxGeometry x="510" y="190" width="380" height="85" as="geometry"/>
        </mxCell>

        <!-- 3. DECISION 1: DETEKSI BARANG AWAL (HC-SR04) -->
        <mxCell id="dec_detect_item" value="Sensor Ultrasonik (HC-SR04)&#xa;Mendeteksi Ada Barang?&#xa;(Jarak d &lt; Jarak Maksimal Silo)" style="rhombus;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#F59E0B;strokeWidth=2;fontColor=#FFFFFF;fontSize=11;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="580" y="310" width="240" height="90" as="geometry"/>
        </mxCell>

        <!-- IDLE / STANDBY LOOP -->
        <mxCell id="standby_node" value="STANDBY / SIAGA:&#xa;• Motor Conveyor MATI (PWM = 0)&#xa;• Kirim Status 'IDLE: Menunggu Bahan Baku' ke HP via MQTT&#xa;• Terus Membaca Sensor Ultrasonik Tiap 200 ms" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#64748B;strokeWidth=1.5;fontColor=#94A3B8;fontSize=11;align=left;spacingLeft=10;" vertex="1" parent="1">
          <mxGeometry x="920" y="317.5" width="310" height="75" as="geometry"/>
        </mxCell>

        <!-- 4. ITEM DETECTED: CONVEYOR MOVES TO SCANNER -->
        <mxCell id="move_to_cam" value="BARANG TERDETEKSI:&#xa;• Motor DC Kuning Aktif (Kecepatan Konstan Inflow)&#xa;• Membawa Bahan Mentah Kopi Menuju ke Bawah Pos Webcam&#xa;• Menghentikan Conveyor Tepat di Titik Scanning" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#10B981;strokeWidth=1.5;fontColor=#FFFFFF;fontSize=11;align=left;spacingLeft=12;" vertex="1" parent="1">
          <mxGeometry x="530" y="440" width="340" height="75" as="geometry"/>
        </mxCell>

        <!-- 5. WEBCAM SCANNING -->
        <mxCell id="cam_scan" value="WEBCAM IMAGE PROCESSING &amp; SCANNING:&#xa;• Membaca Barcode / QR Code pada Wadah Bahan Baku&#xa;• Merekap Data: ID Batch, Tanggal Panen, Varietas Kopi&#xa;• Pengecekan Timeout Kamera (Maksimal 3 Detik / 3x Percobaan)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#312E81;strokeColor=#818CF8;strokeWidth=2;fontColor=#FFFFFF;fontSize=11;align=left;spacingLeft=12;" vertex="1" parent="1">
          <mxGeometry x="520" y="550" width="360" height="75" as="geometry"/>
        </mxCell>

        <!-- 6. DECISION 2: HASIL SCAN KAMERA -->
        <mxCell id="dec_scan_result" value="Hasil Scanning Valid &amp;&#xa;Kualifikasi Bahan Lolos?&#xa;(Barcode Terbaca &amp; Panen Segar)" style="rhombus;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#F59E0B;strokeWidth=2;fontColor=#FFFFFF;fontSize=11;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="580" y="660" width="240" height="95" as="geometry"/>
        </mxCell>

        <!-- ERROR BRANCH: REJECT / SCAN ERROR -->
        <mxCell id="err_scan_stop" value="DETEKSI GAGAL / BAHAN REJECT:&#xa;• Motor Conveyor Berhenti Total (STOP)&#xa;• Buzzer Membunyikan Pola Alarm Error (Beep Cepat)&#xa;• LED Merah Berkedip (Blinking Alert)&#xa;• Notifikasi MQTT ke HP: 'ALERT: SCAN FAILED / REJECT'" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#450A0A;strokeColor=#EF4444;strokeWidth=2;fontColor=#FCA5A5;fontSize=11;align=left;spacingLeft=12;" vertex="1" parent="1">
          <mxGeometry x="140" y="665" width="350" height="85" as="geometry"/>
        </mxCell>

        <mxCell id="manual_quarantine" value="KEPUTUSAN OPERATOR MANUAL (SENGJA MANUAL):&#xa;Operator Mengambil Barang Cacat/Error Tersebut dengan TANGAN&#xa;dari Atas Conveyor dan Memindahkannya ke Keranjang Karantina" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#EF4444;strokeWidth=1.5;fontColor=#FFFFFF;fontSize=11;align=center;" vertex="1" parent="1">
          <mxGeometry x="140" y="790" width="350" height="65" as="geometry"/>
        </mxCell>

        <mxCell id="reset_button" value="Operator Menekan Tombol 'Acknowledge / Reset' di Aplikasi HP&#xa;Alarm Berhenti, Sistem Kembali Siaga Menunggu Barang Baru" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#64748B;strokeWidth=1.5;fontColor=#CBD5E1;fontSize=10;align=center;" vertex="1" parent="1">
          <mxGeometry x="165" y="890" width="300" height="50" as="geometry"/>
        </mxCell>

        <!-- SUCCESS BRANCH: ENTERING SILO -->
        <mxCell id="scan_success" value="DATA VALID &amp; LOLOS INSPEKSI:&#xa;• Simpan Data Batch &amp; Tanggal Panen ke SQLite via Laravel&#xa;• Kirim Status Telemetri 'INBOUND VALID' ke Aplikasi HP&#xa;• Conveyor Melanjutkan Gerak Menuju ke Dalam Silo" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#064E3B;strokeColor=#10B981;strokeWidth=2;fontColor=#FFFFFF;fontSize=11;align=left;spacingLeft=12;" vertex="1" parent="1">
          <mxGeometry x="530" y="790" width="340" height="75" as="geometry"/>
        </mxCell>

        <!-- 7. CONVEYOR POSITION PID LOOP -->
        <mxCell id="pid_conveyor" value="SISTEM KENDALI PID POSISI CONVEYOR (ULTRASONIK FEEDBACK):&#xa;1. Sensor Ultrasonik Terus Mengukur Jarak: d_aktual (cm)&#xa;2. Setpoint Titik Berhenti di Dalam Silo: d_setpoint = 5.0 cm&#xa;3. Perhitungan Galat: e(t) = d_aktual - 5.0 cm&#xa;4. Sinyal Kontrol Motor: PWM = Kp·e(t) + Ki·∫e(t)dt + Kd·(de/dt)&#xa;5. Respons: Mendekati Silo Motor Melambat Halus (Teredam Kritis)&#xa;6. Berhenti Sempurna di 5.0 cm (Tanpa Menabrak Dinding &amp; Tanpa Overshoot)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#0B192C;strokeColor=#0EA5E9;strokeWidth=2;fontColor=#FFFFFF;fontSize=11;align=left;spacingLeft=12;" vertex="1" parent="1">
          <mxGeometry x="490" y="900" width="420" height="120" as="geometry"/>
        </mxCell>

        <!-- DECISION 3: MOTOR JAMMED / TIMEOUT CHECK -->
        <mxCell id="dec_timeout" value="Apakah Barang Mencapai&#xa;Titik 5.0 cm Tepat Waktu?&#xa;(Timeout Check &lt; 10 Detik)" style="rhombus;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#F59E0B;strokeWidth=2;fontColor=#FFFFFF;fontSize=11;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="580" y="1060" width="240" height="90" as="geometry"/>
        </mxCell>

        <!-- JAMMED ERROR -->
        <mxCell id="jammed_node" value="ERROR MEKANIK (CONVEYOR JAMMED):&#xa;• Matikan Motor Segera (Cegah Motor DC Terbakar)&#xa;• Alarm Buzzer + Kirim Notifikasi Darurat ke HP&#xa;• Operator Memeriksa Jalur Mekanik Konveyor" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#450A0A;strokeColor=#EF4444;strokeWidth=2;fontColor=#FCA5A5;fontSize=11;align=left;spacingLeft=12;" vertex="1" parent="1">
          <mxGeometry x="140" y="1062.5" width="350" height="85" as="geometry"/>
        </mxCell>

        <!-- 8. ITEM SAFELY STORED -->
        <mxCell id="stored_node" value="BARANG TELAH TERSIMPAN DI DALAM SILO:&#xa;• Motor Conveyor Dinonaktifkan (PWM = 0)&#xa;• Status Inbound Selesai, Waktu Masuk Tercatat di Database&#xa;• Sistem Mengaktifkan Loop Monitoring &amp; Preservasi Silo" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#10B981;strokeWidth=1.5;fontColor=#FFFFFF;fontSize=11;align=left;spacingLeft=12;" vertex="1" parent="1">
          <mxGeometry x="525" y="1190" width="350" height="70" as="geometry"/>
        </mxCell>

        <!-- 9. SENSOR MONITORING DHT22 & MQ135 -->
        <mxCell id="env_monitor" value="MONITORING MULTI-SENSOR BERDAMPINGAN DI DALAM SILO:&#xa;• DHT22  ➔ Membaca Suhu (°C) &amp; Kelembapan Relatif (%RH)&#xa;• MQ-135 ➔ Membaca Nilai Analog Gas Fermentasi (ADC 0-4095)&#xa;Korelasi Biokimia: Respirasi Kopi = Reaksi Eksotermik Alami&#xa;(Gas Fermentasi Naik ➔ Suhu Panas &amp; Kelembapan Ikut Naik)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#38BDF8;strokeWidth=1.5;fontColor=#FFFFFF;fontSize=11;align=left;spacingLeft=12;" vertex="1" parent="1">
          <mxGeometry x="500" y="1300" width="400" height="85" as="geometry"/>
        </mxCell>

        <!-- 10. DECISION 4: EVALUASI KONDISI LINGKUNGAN -->
        <mxCell id="dec_climate" value="Kondisi Lingkungan Silo&#xa;Melebihi Ambang Batas Aman?&#xa;(Gas > 2175 || Suhu > 35°C || Lembap > 65%)" style="rhombus;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#F59E0B;strokeWidth=2;fontColor=#FFFFFF;fontSize=11;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="560" y="1420" width="280" height="95" as="geometry"/>
        </mxCell>

        <!-- CLIMATE ACTIVE (AERATION + SERVO) -->
        <mxCell id="act_aeration" value="AKTUASI AERASI DINAMIS (KONDISI BAHAYA / WARNING):&#xa;• 2 Buah Kipas 5V Raspberry Pi Menyala (Modulasi PWM MOSFET)&#xa;  Mengalirkan Udara Segar untuk Membuang Panas &amp; Menurunkan Lembap&#xa;• 1 Buah Micro Servo SG90 Membuka Katup Atap (0° ➔ 90°)&#xa;  Melepaskan Akumulasi Gas Fermentasi ke Luar Silo&#xa;• LED Merah Menyala + Buzzer Berbunyi Sesuai Tingkat Risiko" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#0F172A;strokeColor=#0EA5E9;strokeWidth=2;fontColor=#FFFFFF;fontSize=11;align=left;spacingLeft=12;" vertex="1" parent="1">
          <mxGeometry x="500" y="1560" width="400" height="105" as="geometry"/>
        </mxCell>

        <!-- CLIMATE STANDBY -->
        <mxCell id="act_standby" value="KONDISI AMAN / NORMAL:&#xa;• 2 Kipas 5V Mati (Standby / PWM = 0)&#xa;• Katup Servo Atap Menutup Rapat (0°)&#xa;• LED Hijau Aktif, Udara Silo Stabil &amp; Hemat Energi" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#064E3B;strokeColor=#10B981;strokeWidth=1.5;fontColor=#FFFFFF;fontSize=11;align=left;spacingLeft=12;" vertex="1" parent="1">
          <mxGeometry x="930" y="1425" width="310" height="85" as="geometry"/>
        </mxCell>

        <!-- 11. TELEMETRY & MOBILE DASHBOARD -->
        <mxCell id="telemetry_mobile" value="STREAMING TELEMETRI MQTT KE APLIKASI HP OPERATOR:&#xa;• Publish JSON tiap 3 Detik: Suhu, Lembap, Nilai Gas, Status Kipas, Posisi Katup&#xa;• Tampilan Grafik Real-Time &amp; Riwayat Mutu Bahan Baku di Layar HP&#xa;• Operator Dapat Mengatur Setpoint atau Menjalankan Override Manual Jarak Jauh" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#10B981;strokeWidth=1.5;fontColor=#FFFFFF;fontSize=11;align=left;spacingLeft=12;" vertex="1" parent="1">
          <mxGeometry x="500" y="1710" width="400" height="85" as="geometry"/>
        </mxCell>

        <!-- CONNECTORS / EDGES -->
        <mxCell id="e1" edge="1" parent="1" source="start" target="init" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#38BDF8;strokeWidth=2;"/>
        <mxCell id="e2" edge="1" parent="1" source="init" target="dec_detect_item" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#38BDF8;strokeWidth=2;"/>
        
        <!-- Decision Item Detect -->
        <mxCell id="e_item_no" value="TIDAK ADA BARANG&#xa;(Conveyor Kosong)" edge="1" parent="1" source="dec_detect_item" target="standby_node" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#94A3B8;strokeWidth=2;fontColor=#94A3B8;fontStyle=1;"/>
        <mxCell id="e_standby_loop" value="Cek Ulang" edge="1" parent="1" source="standby_node" target="dec_detect_item" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#94A3B8;strokeWidth=1.5;strokeDashArray=3;fontColor=#94A3B8;exitX=0.5;exitY=0;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="1075" y="290"/>
              <mxPoint x="700" y="290"/>
            </Array>
          </mxGeometry>
        </mxCell>

        <mxCell id="e_item_yes" value="ADA BARANG TERDETEKSI" edge="1" parent="1" source="dec_detect_item" target="move_to_cam" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#10B981;strokeWidth=2;fontColor=#10B981;fontStyle=1;"/>
        
        <mxCell id="e3" edge="1" parent="1" source="move_to_cam" target="cam_scan" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#38BDF8;strokeWidth=2;"/>
        <mxCell id="e4" edge="1" parent="1" source="cam_scan" target="dec_scan_result" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#38BDF8;strokeWidth=2;"/>

        <!-- Decision Scan: ERROR -->
        <mxCell id="e_scan_err" value="GAGAL / CACAT&#xa;(Barcode Rusak/Expired)" edge="1" parent="1" source="dec_scan_result" target="err_scan_stop" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#EF4444;strokeWidth=2;fontColor=#EF4444;fontStyle=1;"/>
        <mxCell id="e_err1" edge="1" parent="1" source="err_scan_stop" target="manual_quarantine" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#EF4444;strokeWidth=2;"/>
        <mxCell id="e_err2" edge="1" parent="1" source="manual_quarantine" target="reset_button" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#64748B;strokeWidth=1.5;"/>
        <mxCell id="e_err_loop" value="Kembali Siaga" edge="1" parent="1" source="reset_button" target="dec_detect_item" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#64748B;strokeWidth=1.5;fontColor=#94A3B8;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="90" y="915"/>
              <mxPoint x="90" y="355"/>
            </Array>
          </mxGeometry>
        </mxCell>

        <!-- Decision Scan: VALID -->
        <mxCell id="e_scan_val" value="VALID &amp; LOLOS" edge="1" parent="1" source="dec_scan_result" target="scan_success" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#10B981;strokeWidth=2;fontColor=#10B981;fontStyle=1;"/>
        <mxCell id="e5" edge="1" parent="1" source="scan_success" target="pid_conveyor" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#10B981;strokeWidth=2;"/>
        <mxCell id="e6" edge="1" parent="1" source="pid_conveyor" target="dec_timeout" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#38BDF8;strokeWidth=2;"/>

        <!-- Decision Timeout -->
        <mxCell id="e_time_err" value="TIMEOUT &gt; 10s&#xa;(Conveyor Macet)" edge="1" parent="1" source="dec_timeout" target="jammed_node" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#EF4444;strokeWidth=2;fontColor=#EF4444;fontStyle=1;"/>
        <mxCell id="e_time_ok" value="SUKSES (d = 5.0 cm)" edge="1" parent="1" source="dec_timeout" target="stored_node" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#10B981;strokeWidth=2;fontColor=#10B981;fontStyle=1;"/>

        <mxCell id="e7" edge="1" parent="1" source="stored_node" target="env_monitor" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#38BDF8;strokeWidth=2;"/>
        <mxCell id="e8" edge="1" parent="1" source="env_monitor" target="dec_climate" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#38BDF8;strokeWidth=2;"/>

        <!-- Decision Climate -->
        <mxCell id="e_clim_yes" value="YA (Gas / Suhu / Lembap Tinggi)" edge="1" parent="1" source="dec_climate" target="act_aeration" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#EF4444;strokeWidth=2;fontColor=#EF4444;fontStyle=1;"/>
        <mxCell id="e_clim_no" value="TIDAK (Normal)" edge="1" parent="1" source="dec_climate" target="act_standby" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#10B981;strokeWidth=2;fontColor=#10B981;fontStyle=1;"/>

        <mxCell id="e9" edge="1" parent="1" source="act_aeration" target="telemetry_mobile" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#38BDF8;strokeWidth=2;"/>
        <mxCell id="e10" edge="1" parent="1" source="act_standby" target="telemetry_mobile" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#10B981;strokeWidth=2;entryX=1;entryY=0.5;entryDx=0;entryDy=0;">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="1085" y="1752.5"/>
            </Array>
          </mxGeometry>
        </mxCell>

        <!-- Continuous Climate Loop -->
        <mxCell id="e_clim_loop" value="Loop Pemantauan Lingkungan Terus Berjalan" edge="1" parent="1" source="telemetry_mobile" target="env_monitor" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#0EA5E9;strokeWidth=1.5;strokeDashArray=3;fontColor=#38BDF8;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="440" y="1752.5"/>
              <mxPoint x="440" y="1342.5"/>
            </Array>
          </mxGeometry>
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""
    filename = "diagram_alur_sistem_silo_conveyor_v2.drawio"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(xml_content)
    print(f"Saved {filename}")

def render_ultimate_png():
    fig, ax = plt.subplots(figsize=(15, 24), dpi=300)
    ax.set_facecolor("#0B132B")
    fig.patch.set_facecolor("#0B132B")

    # Title Banner
    r_title = patches.FancyBboxPatch((0.8, 23.0), 13.4, 0.75, boxstyle="round,pad=0.08,rounding_size=0.15",
                                     facecolor="#1E293B", edgecolor="#0EA5E9", linewidth=2.0)
    ax.add_patch(r_title)
    ax.text(7.5, 23.38, "DIAGRAM ALUR KERJA LENGKAP: SMART SILO RAW MATERIAL DENGAN CONVEYOR PID & SCANNING",
            color="#38BDF8", fontsize=11, fontweight="bold", ha="center", va="center")

    # Nodes: (id, xc, yc, w, h, text, bg, border, is_special)
    nodes = [
        ("start", 7.5, 22.3, 3.8, 0.6, "START / POWER ON", "#0F172A", "#0EA5E9", True),
        ("init", 7.5, 21.1, 7.6, 1.2, "Inisialisasi Hardware & Jaringan:\n• WiFi & MQTT HiveMQ Broker (Client ID Unik)\n• Sensor: HC-SR04 (Ultrasonik), DHT22, MQ-135\n• Aktuator: Motor DC Conveyor (PWM), 2 Kipas 5V, Servo Hatch\n• Standby Kamera Scanner (Webcam Inbound Station)", "#1E293B", "#38BDF8", False),
        
        # Check Item At Inlet
        ("dec_detect", 7.5, 19.4, 4.4, 1.2, "Sensor Ultrasonik (HC-SR04)\nMendeteksi Ada Barang?\n(Jarak d < Jarak Maksimal Silo)", "#1E293B", "#F59E0B", True),
        ("standby", 12.2, 19.4, 3.2, 1.1, "STANDBY / SIAGA:\n• Motor Conveyor MATI (PWM = 0)\n• Kirim Status 'IDLE' ke HP via MQTT\n• Cek Ulang Tiap 200 ms", "#1E293B", "#64748B", False),
        
        # Conveyor Move To Scanner
        ("move_scan", 7.5, 17.6, 7.6, 1.1, "BARANG TERDETEKSI DI INLET:\n• Motor DC Kuning Aktif (Maju Membawa Barang)\n• Mengarahkan Wadah Kopi ke Bawah Webcam\n• Menghentikan Conveyor Tepat di Posisi Scan", "#1E293B", "#10B981", False),
        ("cam_scan", 7.5, 16.0, 7.6, 1.2, "WEBCAM IMAGE PROCESSING & SCANNING:\n• Membaca Barcode / QR Code pada Wadah Bahan Baku\n• Merekap Data: ID Batch, Tanggal Panen, Varietas Kopi\n• Pengecekan Timeout Kamera (Maksimal 3 Detik / 3x Percobaan)", "#312E81", "#818CF8", False),
        ("dec_scan", 7.5, 14.3, 4.4, 1.2, "Hasil Scanning Valid &\nKualifikasi Bahan Lolos?\n(Barcode Terbaca & Panen Segar)", "#1E293B", "#F59E0B", True),
        
        # Reject Branch (Left)
        ("rej_stop", 2.5, 14.3, 4.0, 1.2, "MOTOR CONVEYOR STOP\nAlarm Buzzer Bunyi + LED Merah\nNotifikasi 'REJECT / SCAN ERROR'\nke HP via MQTT", "#450A0A", "#EF4444", False),
        ("rej_man", 2.5, 12.6, 4.0, 1.2, "KEPUTUSAN OPERATOR MANUAL:\nOperator Memindahkan Barang Cacat/Error\nSecara MANUAL dengan TANGAN\nke Keranjang Karantina", "#1E293B", "#EF4444", False),
        ("rej_reset", 2.5, 11.1, 4.0, 0.9, "Operator Tekan 'Reset / Acknowledge' di HP\nAlarm Mati, Sistem Kembali Siaga", "#1E293B", "#64748B", False),
        
        # Valid Path (Center)
        ("scan_val", 7.5, 12.6, 7.6, 1.1, "DATA VALID & LOLOS INSPEKSI:\n• Simpan Data Batch & Tanggal Panen ke SQLite via Laravel\n• Kirim Status Telemetri 'INBOUND VALID' ke Aplikasi HP\n• Conveyor Lanjut Meluncur Masuk ke Dalam Silo", "#064E3B", "#10B981", False),
        ("pid_conv", 7.5, 10.6, 7.6, 1.9, "KENDALI PID POSISI CONVEYOR (ULTRASONIK FEEDBACK):\n1. Sensor Ultrasonik Mengukur Jarak: d_aktual (cm)\n2. Setpoint Titik Berhenti di Dalam Silo: d_setpoint = 5.0 cm\n3. Perhitungan Galat: e(t) = d_aktual - 5.0 cm\n4. Sinyal Kontrol Motor: PWM = Kp·e(t) + Ki·∫e(t)dt + Kd·(de/dt)\n5. Respons: Mendekati Silo Motor Melambat Halus (Teredam Kritis)\n6. Berhenti Presisi di 5.0 cm (Anti-Tabrak Dinding & Zero Overshoot)", "#0B192C", "#0EA5E9", False),
        ("dec_time", 7.5, 8.8, 4.4, 1.1, "Apakah Barang Mencapai\nTitik 5.0 cm Tepat Waktu?\n(Timeout Check < 10 Detik)", "#1E293B", "#F59E0B", True),
        ("jammed", 2.5, 8.8, 4.0, 1.1, "ERROR MEKANIK (JAMMED):\n• Matikan Motor Segera (Cegah Rusak)\n• Alarm Buzzer + Notifikasi Darurat HP\n• Operator Periksa Jalur Mekanik", "#450A0A", "#EF4444", False),
        
        ("stored", 7.5, 7.2, 7.6, 1.1, "BARANG TELAH TERSIMPAN DI DALAM SILO:\n• Motor Conveyor Dinonaktifkan (PWM = 0)\n• Status Inbound Selesai, Waktu Masuk Tercatat di Database\n• Sistem Mengaktifkan Loop Monitoring & Preservasi Silo", "#1E293B", "#10B981", False),
        ("sensing", 7.5, 5.6, 7.6, 1.3, "MONITORING MULTI-SENSOR BERDAMPINGAN DI DALAM SILO:\n• DHT22  ➔ Membaca Suhu (°C) & Kelembapan Relatif (%RH)\n• MQ-135 ➔ Membaca Nilai Analog Gas Fermentasi (ADC 0-4095)\nKorelasi Biokimia: Respirasi Kopi = Reaksi Eksotermik Alami\n(Gas Fermentasi Naik ➔ Suhu Panas & Kelembapan Ikut Naik)", "#1E293B", "#38BDF8", False),
        ("dec_clim", 7.5, 4.0, 4.4, 1.1, "Kondisi Lingkungan Silo\nMelebihi Ambang Batas Aman?\n(Gas > 2175 || Suhu > 35°C || Lembap > 65%)", "#1E293B", "#F59E0B", True),
        
        # Climate Actions
        ("act_aer", 7.5, 2.2, 7.6, 1.6, "AKTUASI AERASI DINAMIS (KONDISI BAHAYA / WARNING):\n• 2 Buah Kipas 5V Raspberry Pi Menyala (Modulasi PWM MOSFET)\n  Mengalirkan Udara Segar untuk Membuang Panas & Menurunkan Lembap\n• 1 Buah Micro Servo SG90 Membuka Katup Atap (0° ➔ 90°)\n  Melepaskan Akumulasi Gas Fermentasi ke Luar Silo\n• LED Merah Menyala + Buzzer Berbunyi Sesuai Tingkat Risiko", "#0F172A", "#0EA5E9", False),
        ("act_norm", 12.2, 4.0, 3.2, 1.1, "KONDISI AMAN / NORMAL:\n• 2 Kipas 5V Mati (Standby / PWM = 0)\n• Katup Servo Tutup Rapat (0°)\n• Mutu Terjaga & Hemat Energi", "#064E3B", "#10B981", False),
        ("telemetry", 7.5, 0.7, 7.6, 0.9, "STREAMING TELEMETRI MQTT KE APLIKASI HP OPERATOR:\nPublish JSON tiap 3 Detik: Suhu, Lembap, Gas, Status Kipas, Posisi Katup, Status Batch\nOperator Dapat Memantau & Mengoverride Jarak Jauh", "#1E293B", "#10B981", False)
    ]

    for nid, xc, yc, w, h, text, bg, border, is_special in nodes:
        rect = patches.FancyBboxPatch((xc - w/2, yc - h/2), w, h,
                                      boxstyle="round,pad=0.08,rounding_size=0.15",
                                      facecolor=bg, edgecolor=border, linewidth=1.8)
        ax.add_patch(rect)
        ax.text(xc, yc, text, color="#FFFFFF", fontsize=8.5, ha="center", va="center",
                fontfamily="sans-serif", fontweight="bold" if is_special else "normal")

    # Arrows
    arrows = [
        ((7.5, 22.0), (7.5, 21.7)),
        ((7.5, 20.5), (7.5, 20.0)),
        # Item detect
        ((9.7, 19.4), (10.6, 19.4)),
        ((7.5, 18.8), (7.5, 18.15)),
        ((7.5, 17.05), (7.5, 16.6)),
        ((7.5, 15.4), (7.5, 14.9)),
        # Scan reject
        ((5.3, 14.3), (4.5, 14.3)),
        ((2.5, 13.7), (2.5, 13.2)),
        ((2.5, 12.0), (2.5, 11.55)),
        # Scan valid
        ((7.5, 13.7), (7.5, 13.15)),
        ((7.5, 12.05), (7.5, 11.55)),
        ((7.5, 9.65), (7.5, 9.35)),
        # Timeout branches
        ((5.3, 8.8), (4.5, 8.8)),
        ((7.5, 8.25), (7.5, 7.75)),
        ((7.5, 6.65), (7.5, 6.25)),
        ((7.5, 4.95), (7.5, 4.55)),
        # Climate branches
        ((7.5, 3.45), (7.5, 3.0)),
        ((9.7, 4.0), (10.6, 4.0)),
        ((7.5, 1.4), (7.5, 1.15))
    ]

    for p1, p2 in arrows:
        ax.annotate("", xy=p2, xytext=p1,
                    arrowprops=dict(arrowstyle="-|>", color="#38BDF8", lw=1.8, mutation_scale=14))

    # Reject loop back to inlet
    ax.plot([0.3, 0.3, 3.7], [11.1, 19.4, 19.4], color="#EF4444", lw=1.5, linestyle="--")
    ax.plot([2.5, 0.3], [11.1, 11.1], color="#EF4444", lw=1.5, linestyle="--")
    ax.annotate("", xy=(5.3, 19.4), xytext=(5.1, 19.4),
                arrowprops=dict(arrowstyle="-|>", color="#EF4444", lw=1.5, mutation_scale=12))
    ax.text(0.4, 15.2, "Reset & Siaga Terima Barang Baru", color="#FCA5A5", fontsize=8, rotation=90, va="center")

    # Standby loop back to check
    ax.plot([12.2, 12.2, 8.5], [18.85, 18.0, 18.0], color="#94A3B8", lw=1.5, linestyle=":")
    ax.annotate("", xy=(8.5, 18.0), xytext=(8.7, 18.0),
                arrowprops=dict(arrowstyle="-|>", color="#94A3B8", lw=1.5, mutation_scale=12))
    ax.text(12.3, 18.4, "Polling Tiap 200ms", color="#94A3B8", fontsize=7.5, va="center")

    # Standby connect to telemetry
    ax.plot([12.2, 12.2, 11.3], [3.45, 0.7, 0.7], color="#10B981", lw=1.5)
    ax.annotate("", xy=(11.3, 0.7), xytext=(11.5, 0.7),
                arrowprops=dict(arrowstyle="-|>", color="#10B981", lw=1.5, mutation_scale=12))

    # Climate monitoring loop back
    ax.plot([3.5, 3.5, 3.5], [0.7, 5.6, 5.6], color="#0EA5E9", lw=1.5, linestyle=":")
    ax.plot([3.7, 3.5], [0.7, 0.7], color="#0EA5E9", lw=1.5, linestyle=":")
    ax.annotate("", xy=(3.7, 5.6), xytext=(3.5, 5.6),
                arrowprops=dict(arrowstyle="-|>", color="#0EA5E9", lw=1.5, mutation_scale=12))
    ax.text(3.6, 3.1, "Loop Monitoring Berkelanjutan", color="#38BDF8", fontsize=8, rotation=90, va="center")

    # Labels for decisions
    ax.text(10.1, 19.6, "TIDAK", color="#94A3B8", fontsize=8, fontweight="bold")
    ax.text(7.9, 18.4, "ADA BARANG", color="#10B981", fontsize=8, fontweight="bold")
    ax.text(4.9, 14.5, "GAGAL / REJECT", color="#EF4444", fontsize=8, fontweight="bold")
    ax.text(7.9, 13.4, "VALID", color="#10B981", fontsize=8, fontweight="bold")
    ax.text(4.9, 9.0, "TIMEOUT (>10s)", color="#EF4444", fontsize=8, fontweight="bold")
    ax.text(7.9, 8.5, "SAMPAI (5 cm)", color="#10B981", fontsize=8, fontweight="bold")
    ax.text(7.9, 3.2, "YA (BAHAYA)", color="#EF4444", fontsize=8, fontweight="bold")
    ax.text(10.1, 4.2, "NORMAL", color="#10B981", fontsize=8, fontweight="bold")

    ax.set_xlim(0, 15)
    ax.set_ylim(0.0, 24.0)
    ax.axis("off")
    plt.tight_layout()
    png_filename = "diagram_alur_sistem_silo_conveyor_v2.png"
    plt.savefig(png_filename, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"Saved {png_filename}")

if __name__ == "__main__":
    generate_ultimate_xml()
    render_ultimate_png()
