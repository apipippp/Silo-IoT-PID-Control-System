import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_arch_xml():
    xml_content = """<mxfile host="app.diagrams.net" modified="2026-11-05T00:00:00.000Z" agent="Mozilla/5.0" version="21.6.8" type="device">
  <diagram id="arsitektur_silo" name="Arsitektur Sistem Terpadu Silo IoT">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>

        <!-- TIER 1: HARDWARE LAYER -->
        <mxCell id="tier1_bg" value="TIER 1: PERANGKAT KERAS &amp; SISTEM KENDALI FISIK (ESP32 EDGE NODE)" style="swimlane;whiteSpace=wrap;html=1;fillColor=#0F172A;strokeColor=#0EA5E9;strokeWidth=2;fontColor=#0EA5E9;fontStyle=1;fontSize=13;startSize=30;rounded=1;" vertex="1" parent="1">
          <mxGeometry x="40" y="40" width="340" height="540" as="geometry"/>
        </mxCell>
        
        <mxCell id="sensors_box" value="SENSOR LINGKUNGAN SILO&#xa;• DHT22 (Suhu &amp; Kelembapan - GPIO 15)&#xa;• MQ-135 (Kualitas Udara/Gas - ADC1 GPIO 34)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#38BDF8;fontColor=#FFFFFF;fontSize=11;align=left;spacingLeft=10;" vertex="1" parent="tier1_bg">
          <mxGeometry x="20" y="50" width="300" height="70" as="geometry"/>
        </mxCell>

        <mxCell id="esp32_box" value="ESP32 EDGE CONTROLLER&#xa;• Dual-Core 240 MHz, ADC1 12-bit&#xa;• Modul WiFi 2.4 GHz Bawaan&#xa;• Loop Kendali Tertutup PID Diskrit&#xa;• State Machine: NORMAL / WARN / CRIT" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#10B981;fontColor=#FFFFFF;fontSize=11;fontStyle=1;align=left;spacingLeft=10;" vertex="1" parent="tier1_bg">
          <mxGeometry x="20" y="160" width="300" height="110" as="geometry"/>
        </mxCell>

        <mxCell id="actuators_box" value="AKTUATOR &amp; DRIVER FISIK&#xa;• Driver MOSFET HW-517 (PWM GPIO 18)&#xa;• Motor DC Blower Kipas (Aerasi Silo)&#xa;• Micro Servo SG90 (Katup Atap GPIO 13)&#xa;• Indikator LED &amp; Buzzer Peringatan" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#F59E0B;fontColor=#FFFFFF;fontSize=11;align=left;spacingLeft=10;" vertex="1" parent="tier1_bg">
          <mxGeometry x="20" y="310" width="300" height="90" as="geometry"/>
        </mxCell>

        <mxCell id="silo_plant" value="PLANT FISIK: RUANG SILO RAW MATERIAL&#xa;Volume Headspace Penyimpanan Bahan Baku Curah" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#334155;strokeColor=#64748B;fontColor=#F8FAFC;fontSize=10;fontStyle=2;" vertex="1" parent="tier1_bg">
          <mxGeometry x="20" y="440" width="300" height="50" as="geometry"/>
        </mxCell>

        <!-- TIER 2: COMMUNICATION LAYER -->
        <mxCell id="tier2_bg" value="TIER 2: PROTOKOL KOMUNIKASI &amp; BROKER (MQTT)" style="swimlane;whiteSpace=wrap;html=1;fillColor=#0F172A;strokeColor=#10B981;strokeWidth=2;fontColor=#10B981;fontStyle=1;fontSize=13;startSize=30;rounded=1;" vertex="1" parent="1">
          <mxGeometry x="420" y="40" width="320" height="540" as="geometry"/>
        </mxCell>

        <mxCell id="broker_box" value="HIVEMQ CLOUD / MQTT BROKER&#xa;Port 1883 (TCP) / Port 8884 (WebSocket WSS)&#xa;QoS Level: 0/1 | Light &amp; High-Throughput" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#064E3B;strokeColor=#10B981;fontColor=#FFFFFF;fontSize=11;fontStyle=1;" vertex="1" parent="tier2_bg">
          <mxGeometry x="20" y="60" width="280" height="80" as="geometry"/>
        </mxCell>

        <mxCell id="pub_topic" value="TELEMETRY TOPIC (Publish):&#xa;silo/raw_material/telemetry&#xa;Payload: JSON&#xa;{temp, hum, gas, status, pwm, servo, pid}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#38BDF8;fontColor=#FFFFFF;fontSize=10;align=left;spacingLeft=10;" vertex="1" parent="tier2_bg">
          <mxGeometry x="20" y="190" width="280" height="90" as="geometry"/>
        </mxCell>

        <mxCell id="sub_topic" value="COMMAND TOPIC (Subscribe):&#xa;silo/raw_material/control&#xa;Payload: JSON&#xa;{mode: &quot;AUTO&quot;/&quot;MANUAL&quot;, fan, servo, kp, ki, kd}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#F59E0B;fontColor=#FFFFFF;fontSize=10;align=left;spacingLeft=10;" vertex="1" parent="tier2_bg">
          <mxGeometry x="20" y="330" width="280" height="90" as="geometry"/>
        </mxCell>

        <!-- TIER 3: APPLICATION & STORAGE LAYER -->
        <mxCell id="tier3_bg" value="TIER 3: APLIKASI WEB SCM &amp; DATABASE (LARAVEL + SQLITE)" style="swimlane;whiteSpace=wrap;html=1;fillColor=#0F172A;strokeColor=#F59E0B;strokeWidth=2;fontColor=#F59E0B;fontStyle=1;fontSize=13;startSize=30;rounded=1;" vertex="1" parent="1">
          <mxGeometry x="780" y="40" width="350" height="540" as="geometry"/>
        </mxCell>

        <mxCell id="laravel_box" value="BACKEND FRAMEWORK: LARAVEL&#xa;• Controller: SCM Silo &amp; Telemetry Manager&#xa;• Background MQTT Client / Daemon Worker&#xa;• REST API &amp; WebSocket Broadcaster" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#451A03;strokeColor=#F59E0B;fontColor=#FFFFFF;fontSize=11;fontStyle=1;align=left;spacingLeft=10;" vertex="1" parent="tier3_bg">
          <mxGeometry x="25" y="60" width="300" height="90" as="geometry"/>
        </mxCell>

        <mxCell id="db_box" value="DATABASE: SQLITE&#xa;• Table: silo_telemetries (temp, hum, gas, risk)&#xa;• Table: control_logs (mode, pwm, servo, pid)&#xa;• Ringan, Zero-Config, File-Based Embedded" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#38BDF8;fontColor=#FFFFFF;fontSize=10;align=left;spacingLeft=10;" vertex="1" parent="tier3_bg">
          <mxGeometry x="25" y="190" width="300" height="90" as="geometry"/>
        </mxCell>

        <mxCell id="web_box" value="WEB DASHBOARD SCM &amp; OPERATOR UI&#xa;• Real-Time Monitoring Kualitas Bahan Baku&#xa;• Chart.js: Live Step-Response PID Plotter&#xa;• Kontrol Manual Fan &amp; Servo Hatch&#xa;• Remote Slider Penalaan Parameter Kp, Ki, Kd" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#10B981;fontColor=#FFFFFF;fontSize=10;align=left;spacingLeft=10;" vertex="1" parent="tier3_bg">
          <mxGeometry x="25" y="320" width="300" height="120" as="geometry"/>
        </mxCell>

        <!-- Inter-tier Connectors -->
        <mxCell id="e_sensors_esp" edge="1" parent="1" source="sensors_box" target="esp32_box" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#38BDF8;strokeWidth=1.5;"/>
        <mxCell id="e_esp_act" edge="1" parent="1" source="esp32_box" target="actuators_box" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#F59E0B;strokeWidth=1.5;"/>
        <mxCell id="e_act_silo" edge="1" parent="1" source="actuators_box" target="silo_plant" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#64748B;strokeWidth=1.5;"/>

        <mxCell id="e_esp_mqtt_pub" edge="1" parent="1" source="esp32_box" target="pub_topic" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#10B981;strokeWidth=2;exitX=1;exitY=0.5;entryX=0;entryY=0.5;"/>
        <mxCell id="e_mqtt_cmd_esp" edge="1" parent="1" source="sub_topic" target="esp32_box" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#F59E0B;strokeWidth=2;exitX=0;exitY=0.5;entryX=1;entryY=0.75;"/>

        <mxCell id="e_pub_laravel" edge="1" parent="1" source="pub_topic" target="laravel_box" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#10B981;strokeWidth=2;exitX=1;exitY=0.5;entryX=0;entryY=0.5;"/>
        <mxCell id="e_laravel_db" edge="1" parent="1" source="laravel_box" target="db_box" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#38BDF8;strokeWidth=1.5;"/>
        <mxCell id="e_laravel_web" edge="1" parent="1" source="laravel_box" target="web_box" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#F59E0B;strokeWidth=1.5;"/>
        <mxCell id="e_web_cmd_sub" edge="1" parent="1" source="web_box" target="sub_topic" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#F59E0B;strokeWidth=2;exitX=0;exitY=0.5;entryX=1;entryY=0.5;"/>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""
    with open("arsitektur_sistem_silo.drawio", "w", encoding="utf-8") as f:
        f.write(xml_content)
    print("Saved arsitektur_sistem_silo.drawio")

def render_arch_png():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_facecolor("#0F172A")
    fig.patch.set_facecolor("#0F172A")

    # Tier 1 Container
    rect_t1 = patches.FancyBboxPatch((0.5, 0.5), 4.0, 7.0, boxstyle="round,pad=0.1,rounding_size=0.2",
                                     facecolor="#1E293B", edgecolor="#0EA5E9", linewidth=2.0)
    ax.add_patch(rect_t1)
    ax.text(2.5, 7.15, "TIER 1: PERANGKAT KERAS (ESP32 EDGE)", color="#38BDF8", fontsize=11, fontweight="bold", ha="center")

    # Tier 2 Container
    rect_t2 = patches.FancyBboxPatch((4.9, 0.5), 3.8, 7.0, boxstyle="round,pad=0.1,rounding_size=0.2",
                                     facecolor="#1E293B", edgecolor="#10B981", linewidth=2.0)
    ax.add_patch(rect_t2)
    ax.text(6.8, 7.15, "TIER 2: KOMUNIKASI (MQTT HIVEMQ)", color="#10B981", fontsize=11, fontweight="bold", ha="center")

    # Tier 3 Container
    rect_t3 = patches.FancyBboxPatch((9.1, 0.5), 4.4, 7.0, boxstyle="round,pad=0.1,rounding_size=0.2",
                                     facecolor="#1E293B", edgecolor="#F59E0B", linewidth=2.0)
    ax.add_patch(rect_t3)
    ax.text(11.3, 7.15, "TIER 3: LARAVEL & SQLITE DASHBOARD", color="#F59E0B", fontsize=11, fontweight="bold", ha="center")

    # Inner boxes Tier 1
    t1_boxes = [
        (2.5, 6.0, 3.4, 1.2, "SENSOR LINGKUNGAN SILO\n• DHT22: Suhu & Kelembapan (GPIO 15)\n• MQ-135: Gas Fermentasi (GPIO 34)", "#0F172A", "#38BDF8"),
        (2.5, 4.1, 3.4, 1.6, "ESP32 EDGE CONTROLLER\n• FreeRTOS & Dual Core 240 MHz\n• Loop Kendali PID Diskrit & State Machine\n• WiFi Client & JSON Serializer", "#0B192C", "#10B981"),
        (2.5, 2.0, 3.4, 1.5, "AKTUATOR & DRIVER PWM\n• Driver MOSFET HW-517 (PWM GPIO 18)\n• Motor Kipas Blower DC (Aerasi Silo)\n• Micro Servo SG90 (Katup Atap GPIO 13)", "#0F172A", "#F59E0B"),
        (2.5, 0.9, 3.4, 0.5, "PLANT FISIK: Headspace Silo Bahan Baku", "#334155", "#64748B")
    ]
    for xc, yc, w, h, txt, bg, border in t1_boxes:
        r = patches.FancyBboxPatch((xc - w/2, yc - h/2), w, h, boxstyle="round,pad=0.05,rounding_size=0.1",
                                   facecolor=bg, edgecolor=border, linewidth=1.5)
        ax.add_patch(r)
        ax.text(xc, yc, txt, color="#FFFFFF", fontsize=8.5, ha="center", va="center")

    # Inner boxes Tier 2
    t2_boxes = [
        (6.8, 5.8, 3.2, 1.4, "HIVEMQ CLOUD BROKER\n• TCP Port 1883 & WSS Port 8884\n• High Reliability / Low Latency\n• Message Routing QoS 0/1", "#064E3B", "#10B981"),
        (6.8, 3.8, 3.2, 1.3, "TELEMETRY TOPIC (Pub)\nsilo/raw_material/telemetry\n{temp, hum, gas, status,\npwm_duty, servo_angle, pid}", "#0F172A", "#38BDF8"),
        (6.8, 1.8, 3.2, 1.3, "CONTROL TOPIC (Sub)\nsilo/raw_material/control\n{mode: 'AUTO'/'MANUAL',\nfan_cmd, servo_cmd, kp, ki, kd}", "#0F172A", "#F59E0B")
    ]
    for xc, yc, w, h, txt, bg, border in t2_boxes:
        r = patches.FancyBboxPatch((xc - w/2, yc - h/2), w, h, boxstyle="round,pad=0.05,rounding_size=0.1",
                                   facecolor=bg, edgecolor=border, linewidth=1.5)
        ax.add_patch(r)
        ax.text(xc, yc, txt, color="#FFFFFF", fontsize=8.5, ha="center", va="center")

    # Inner boxes Tier 3
    t3_boxes = [
        (11.3, 5.8, 3.8, 1.4, "LARAVEL BACKEND APPLICATION\n• Telemetry Ingest Daemon\n• SCM Business Logic & Alert Dispatcher\n• RESTful API & WebSocket Broadcaster", "#451A03", "#F59E0B"),
        (11.3, 4.0, 3.8, 1.2, "SQLITE EMBEDDED DATABASE\n• silo_telemetries (Riwayat Kondisi)\n• control_logs (Histori PID & Aktuator)\n• Zero-Config, Fast File-Based Storage", "#0F172A", "#38BDF8"),
        (11.3, 1.9, 3.8, 1.7, "WEB DASHBOARD SCM & CONTROL UI\n• Live Telemetri Suhu, Lembap, & Gas\n• Chart.js: Real-Time Step-Response Plotter\n• Tombol Override Manual Fan & Servo\n• Remote Tuning Slider (Kp, Ki, Kd)", "#0F172A", "#10B981")
    ]
    for xc, yc, w, h, txt, bg, border in t3_boxes:
        r = patches.FancyBboxPatch((xc - w/2, yc - h/2), w, h, boxstyle="round,pad=0.05,rounding_size=0.1",
                                   facecolor=bg, edgecolor=border, linewidth=1.5)
        ax.add_patch(r)
        ax.text(xc, yc, txt, color="#FFFFFF", fontsize=8.5, ha="center", va="center")

    # Arrows between tiers
    # ESP32 -> Telemetry Pub
    ax.annotate("", xy=(5.2, 3.8), xytext=(4.2, 4.1),
                arrowprops=dict(arrowstyle="-|>", color="#10B981", lw=2, mutation_scale=15))
    ax.text(4.7, 4.2, "Publish", color="#10B981", fontsize=8, fontweight="bold", ha="center")

    # Telemetry Pub -> Laravel
    ax.annotate("", xy=(9.4, 5.8), xytext=(8.4, 3.8),
                arrowprops=dict(arrowstyle="-|>", color="#10B981", lw=2, mutation_scale=15))

    # Web Dashboard -> Control Sub
    ax.annotate("", xy=(8.4, 1.8), xytext=(9.4, 1.9),
                arrowprops=dict(arrowstyle="-|>", color="#F59E0B", lw=2, mutation_scale=15))
    ax.text(8.9, 2.1, "Publish Cmd", color="#F59E0B", fontsize=8, fontweight="bold", ha="center")

    # Control Sub -> ESP32
    ax.annotate("", xy=(4.2, 3.8), xytext=(5.2, 1.8),
                arrowprops=dict(arrowstyle="-|>", color="#F59E0B", lw=2, mutation_scale=15))
    ax.text(4.7, 2.7, "Subscribe", color="#F59E0B", fontsize=8, fontweight="bold", ha="center")

    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8.0)
    ax.axis("off")
    plt.tight_layout()
    plt.savefig("arsitektur_sistem_silo.png", dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print("Saved arsitektur_sistem_silo.png")

if __name__ == "__main__":
    generate_arch_xml()
    render_arch_png()
