import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_flowchart_xml():
    xml_content = """<mxfile host="app.diagrams.net" modified="2026-11-05T00:00:00.000Z" agent="Mozilla/5.0" version="21.6.8" type="device">
  <diagram id="flowchart_silo" name="Flowchart Sistem Silo ESP32">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="1654" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>

        <!-- Start -->
        <mxCell id="start" value="START / POWER ON" style="ellipse;whiteSpace=wrap;html=1;fillColor=#0F172A;strokeColor=#0EA5E9;strokeWidth=2;fontColor=#FFFFFF;fontStyle=1;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="460" y="40" width="160" height="50" as="geometry"/>
        </mxCell>

        <!-- Init -->
        <mxCell id="init" value="Inisialisasi Sistem:\n- GPIO Pin (MOSFET PWM, Servo, Buzzer, LED)\n- Sensor DHT22 &amp; ADC1 MQ-135\n- Setup WiFi &amp; MQTT HiveMQ" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#38BDF8;strokeWidth=1.5;fontColor=#FFFFFF;fontSize=11;align=left;spacingLeft=10;" vertex="1" parent="1">
          <mxGeometry x="420" y="120" width="240" height="70" as="geometry"/>
        </mxCell>

        <!-- Connect Check -->
        <mxCell id="check_conn" value="WiFi &amp; MQTT\nTerhubung?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#F59E0B;strokeWidth=1.5;fontColor=#FFFFFF;fontSize=11;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="465" y="220" width="150" height="70" as="geometry"/>
        </mxCell>

        <!-- Reconnect -->
        <mxCell id="reconnect" value="Reconnect WiFi &amp;\nMQTT Broker" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#451A03;strokeColor=#F59E0B;strokeWidth=1;fontColor=#FDE68A;fontSize=10;" vertex="1" parent="1">
          <mxGeometry x="670" y="235" width="130" height="40" as="geometry"/>
        </mxCell>

        <!-- Read Sensors -->
        <mxCell id="read_sensors" value="Membaca Sensor Lingkungan Silo:\n- DHT22 -> Suhu (°C) &amp; Kelembapan (%RH)\n- MQ-135 -> Indikator Gas (ADC 0-4095)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#38BDF8;strokeWidth=1.5;fontColor=#FFFFFF;fontSize=11;align=left;spacingLeft=10;" vertex="1" parent="1">
          <mxGeometry x="420" y="320" width="240" height="60" as="geometry"/>
        </mxCell>

        <!-- Validate NaN -->
        <mxCell id="check_nan" value="Data Sensor\nValid (Bukan NaN)?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#F59E0B;strokeWidth=1.5;fontColor=#FFFFFF;fontSize=11;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="465" y="410" width="150" height="70" as="geometry"/>
        </mxCell>

        <!-- Check Mode -->
        <mxCell id="check_mode" value="Mode Operasi?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#38BDF8;strokeWidth=1.5;fontColor=#FFFFFF;fontSize=11;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="465" y="510" width="150" height="70" as="geometry"/>
        </mxCell>

        <!-- Manual Exec -->
        <mxCell id="exec_manual" value="Mode MANUAL:\nEksekusi Perintah Operator dari Dashboard\n(Override PWM Fan &amp; Posisi Servo)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#312E81;strokeColor=#818CF8;strokeWidth=1.5;fontColor=#FFFFFF;fontSize=11;align=left;spacingLeft=10;" vertex="1" parent="1">
          <mxGeometry x="220" y="515" width="200" height="60" as="geometry"/>
        </mxCell>

        <!-- Auto: Risk Evaluation -->
        <mxCell id="eval_risk" value="Evaluasi Status Risiko SCM Silo:\n- NORMAL : Gas &lt; 2050 &amp; Lembap &lt; 62%\n- WARNING : Gas > 2175 || Lembap > 65%\n- CRITICAL: Gas > 2500 || Lembap > 75%" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#10B981;strokeWidth=1.5;fontColor=#FFFFFF;fontSize=11;align=left;spacingLeft=10;" vertex="1" parent="1">
          <mxGeometry x="420" y="610" width="240" height="75" as="geometry"/>
        </mxCell>

        <!-- PID Calculation -->
        <mxCell id="calc_pid" value="Perhitungan Algoritma PID Aerasi:\n1. Error = Gas_Aktual - Setpoint\n2. P = Kp * Error\n3. I = I_prev + Ki * Error * dt (Anti-Windup)\n4. D = Kd * (Error - Last_Error) / dt\n5. Output = P + I + D" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#0F172A;strokeColor=#0EA5E9;strokeWidth=2;fontColor=#FFFFFF;fontSize=11;fontStyle=0;align=left;spacingLeft=10;" vertex="1" parent="1">
          <mxGeometry x="420" y="720" width="240" height="95" as="geometry"/>
        </mxCell>

        <!-- Output Actuators -->
        <mxCell id="actuators" value="Output ke Hardware Aktuator:\n- PWM Motor Kipas via MOSFET = constrain(Output, 0, 255)\n- Sudut Servo Katup Atap = map(PWM, 0, 255, 0, 90°)\n- Status LED &amp; Tone Buzzer Alarm" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#38BDF8;strokeWidth=1.5;fontColor=#FFFFFF;fontSize=11;align=left;spacingLeft=10;" vertex="1" parent="1">
          <mxGeometry x="420" y="850" width="240" height="75" as="geometry"/>
        </mxCell>

        <!-- Check Timer Publish -->
        <mxCell id="check_timer" value="Timer Publish\n(Tiap 3 Detik)?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#F59E0B;strokeWidth=1.5;fontColor=#FFFFFF;fontSize=11;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="465" y="955" width="150" height="70" as="geometry"/>
        </mxCell>

        <!-- Publish MQTT -->
        <mxCell id="pub_mqtt" value="Publish JSON Telemetri via MQTT:\nTopic: silo/raw_material/telemetry\n{temp, hum, gas, status, pwm, servo, pid}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#064E3B;strokeColor=#10B981;strokeWidth=1.5;fontColor=#FFFFFF;fontSize=11;align=left;spacingLeft=10;" vertex="1" parent="1">
          <mxGeometry x="420" y="1060" width="240" height="65" as="geometry"/>
        </mxCell>

        <!-- Client Loop -->
        <mxCell id="client_loop" value="client.loop() — Dengarkan Pesan Masuk / Perintah MQTT dari Dashboard Laravel" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#64748B;strokeWidth=1;fontColor=#94A3B8;fontSize=10;" vertex="1" parent="1">
          <mxGeometry x="400" y="1160" width="280" height="35" as="geometry"/>
        </mxCell>

        <!-- Edges / Connectors -->
        <mxCell id="e1" edge="1" parent="1" source="start" target="init" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#38BDF8;strokeWidth=1.5;"/>
        <mxCell id="e2" edge="1" parent="1" source="init" target="check_conn" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#38BDF8;strokeWidth=1.5;"/>
        
        <mxCell id="e3" value="YA" edge="1" parent="1" source="check_conn" target="read_sensors" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#10B981;strokeWidth=1.5;fontColor=#10B981;fontStyle=1;"/>
        <mxCell id="e4" value="TIDAK" edge="1" parent="1" source="check_conn" target="reconnect" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#EF4444;strokeWidth=1.5;fontColor=#EF4444;fontStyle=1;"/>
        <mxCell id="e5" edge="1" parent="1" source="reconnect" target="read_sensors" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#38BDF8;strokeWidth=1.5;entryX=1;entryY=0.5;entryDx=0;entryDy=0;">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="735" y="350"/>
            </Array>
          </mxGeometry>
        </mxCell>

        <mxCell id="e6" edge="1" parent="1" source="read_sensors" target="check_nan" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#38BDF8;strokeWidth=1.5;"/>
        <mxCell id="e7" value="YA" edge="1" parent="1" source="check_nan" target="check_mode" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#10B981;strokeWidth=1.5;fontColor=#10B981;fontStyle=1;"/>
        <mxCell id="e8" value="TIDAK (Error)" edge="1" parent="1" source="check_nan" target="client_loop" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#EF4444;strokeWidth=1.5;fontColor=#EF4444;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="180" y="445"/>
              <mxPoint x="180" y="1178"/>
            </Array>
          </mxGeometry>
        </mxCell>

        <mxCell id="e9" value="MANUAL" edge="1" parent="1" source="check_mode" target="exec_manual" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#818CF8;strokeWidth=1.5;fontColor=#818CF8;fontStyle=1;"/>
        <mxCell id="e10" value="AUTO" edge="1" parent="1" source="check_mode" target="eval_risk" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#10B981;strokeWidth=1.5;fontColor=#10B981;fontStyle=1;"/>

        <mxCell id="e11" edge="1" parent="1" source="exec_manual" target="actuators" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#818CF8;strokeWidth=1.5;entryX=0;entryY=0.5;entryDx=0;entryDy=0;">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="320" y="888"/>
            </Array>
          </mxGeometry>
        </mxCell>

        <mxCell id="e12" edge="1" parent="1" source="eval_risk" target="calc_pid" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#38BDF8;strokeWidth=1.5;"/>
        <mxCell id="e13" edge="1" parent="1" source="calc_pid" target="actuators" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#38BDF8;strokeWidth=1.5;"/>
        <mxCell id="e14" edge="1" parent="1" source="actuators" target="check_timer" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#38BDF8;strokeWidth=1.5;"/>

        <mxCell id="e15" value="YA" edge="1" parent="1" source="check_timer" target="pub_mqtt" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#10B981;strokeWidth=1.5;fontColor=#10B981;fontStyle=1;"/>
        <mxCell id="e16" value="BELUM" edge="1" parent="1" source="check_timer" target="client_loop" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#94A3B8;strokeWidth=1.5;fontColor=#94A3B8;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="720" y="990"/>
              <mxPoint x="720" y="1178"/>
            </Array>
          </mxGeometry>
        </mxCell>

        <mxCell id="e17" edge="1" parent="1" source="pub_mqtt" target="client_loop" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#38BDF8;strokeWidth=1.5;"/>
        
        <!-- Loop Back -->
        <mxCell id="e18" value="Loop Berulang (delay non-blocking)" edge="1" parent="1" source="client_loop" target="read_sensors" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#38BDF8;strokeWidth=1.5;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0;entryY=0.25;entryDx=0;entryDy=0;">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="540" y="1220"/>
              <mxPoint x="140" y="1220"/>
              <mxPoint x="140" y="335"/>
            </Array>
          </mxGeometry>
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""
    with open("flowchart_sistem_silo.drawio", "w", encoding="utf-8") as f:
        f.write(xml_content)
    print("Saved flowchart_sistem_silo.drawio")

def render_flowchart_png():
    fig, ax = plt.subplots(figsize=(10, 14), dpi=300)
    ax.set_facecolor("#0F172A")
    fig.patch.set_facecolor("#0F172A")

    # Define nodes with coordinates (x_center, y_center, width, height, text, bg_color, border_color)
    nodes = [
        ("start", 5, 13.3, 3.2, 0.6, "START / POWER ON", "#1E293B", "#0EA5E9", True),
        ("init", 5, 12.1, 4.8, 1.0, "Inisialisasi Hardware & Koneksi:\n• GPIO MOSFET PWM, Servo, Buzzer, LED\n• DHT22 & MQ-135 (ADC1)\n• WiFi & MQTT HiveMQ Client", "#1E293B", "#38BDF8", False),
        ("conn", 5, 10.7, 3.2, 0.9, "WiFi & MQTT\nTerhubung?", "#1E293B", "#F59E0B", True),
        ("read", 5, 9.4, 4.8, 0.9, "Baca Sensor Lingkungan Silo:\n• Suhu & Kelembapan (DHT22)\n• Nilai Analog Gas (MQ-135)", "#1E293B", "#38BDF8", False),
        ("mode", 5, 8.1, 3.2, 0.8, "Mode Operasi?", "#1E293B", "#F59E0B", True),
        ("manual", 1.8, 8.1, 2.6, 0.8, "Mode MANUAL:\nEksekusi Perintah\nDashboard Operator", "#312E81", "#818CF8", False),
        ("eval", 5, 6.7, 4.8, 1.1, "Evaluasi Status SCM Silo:\n• NORMAL : Gas < 2050 & Lembap < 62%\n• WARNING: Gas > 2175 || Lembap > 65%\n• CRITICAL: Gas > 2500 || Lembap > 75%", "#1E293B", "#10B981", False),
        ("pid", 5, 5.0, 4.8, 1.4, "Kalkulasi Kontroler PID Aerasi:\n1. Error = Gas_Aktual - Setpoint\n2. Suku P = Kp * Error\n3. Suku I = I_prev + Ki * Error * dt (Anti-Windup)\n4. Suku D = Kd * (dError / dt)\n5. Total Kontrol u(t) = P + I + D", "#0B192C", "#0EA5E9", False),
        ("act", 5, 3.5, 4.8, 0.9, "Output ke Aktuator Fisik:\n• PWM Kipas = constrain(u, 0, 255)\n• Sudut Servo Katup = map(PWM, 0, 255, 0, 90°)\n• Indikator LED & Tone Buzzer", "#1E293B", "#38BDF8", False),
        ("pub", 5, 2.2, 4.8, 0.9, "Publish JSON Telemetri MQTT:\nTopic: silo/raw_material/telemetry\n{temp, hum, gas, status, pwm, servo}", "#064E3B", "#10B981", False),
        ("loop", 5, 1.0, 4.8, 0.6, "client.loop() — Dengarkan Perintah Dashboard", "#1E293B", "#64748B", False)
    ]

    for nid, xc, yc, w, h, text, bg, border, is_special in nodes:
        rect = patches.FancyBboxPatch((xc - w/2, yc - h/2), w, h,
                                      boxstyle="round,pad=0.08,rounding_size=0.15",
                                      facecolor=bg, edgecolor=border, linewidth=1.8)
        ax.add_patch(rect)
        ax.text(xc, yc, text, color="#FFFFFF", fontsize=8.5, ha="center", va="center",
                fontfamily="sans-serif", fontweight="bold" if is_special else "normal")

    # Connectors (arrows)
    arrows = [
        ((5, 13.0), (5, 12.6)),
        ((5, 11.6), (5, 11.15)),
        ((5, 10.25), (5, 9.85)),
        ((5, 8.95), (5, 8.5)),
        ((5, 7.7), (5, 7.25)),
        ((5, 6.15), (5, 5.7)),
        ((5, 4.3), (5, 3.95)),
        ((5, 3.05), (5, 2.65)),
        ((5, 1.75), (5, 1.3)),
        # manual branch
        ((3.4, 8.1), (3.1, 8.1)),
        ((1.8, 7.7), (1.8, 3.5), (2.6, 3.5))
    ]

    for pts in arrows:
        if len(pts) == 2:
            p1, p2 = pts
            ax.annotate("", xy=p2, xytext=p1,
                        arrowprops=dict(arrowstyle="-|>", color="#38BDF8", lw=1.5, mutation_scale=12))
        elif len(pts) == 3:
            p1, p2, p3 = pts
            ax.plot([p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]], color="#818CF8", lw=1.5)
            ax.annotate("", xy=(2.6, 3.5), xytext=(2.4, 3.5),
                        arrowprops=dict(arrowstyle="-|>", color="#818CF8", lw=1.5, mutation_scale=12))

    # Loop back arrow
    ax.plot([2.6, 0.4, 0.4, 2.6], [1.0, 1.0, 9.4, 9.4], color="#38BDF8", lw=1.5, linestyle="--")
    ax.annotate("", xy=(2.6, 9.4), xytext=(2.4, 9.4),
                arrowprops=dict(arrowstyle="-|>", color="#38BDF8", lw=1.5, mutation_scale=12))
    ax.text(0.5, 5.2, "Loop Berulang Tiap Siklus", color="#38BDF8", fontsize=8, rotation=90, va="center")

    ax.set_xlim(0, 10)
    ax.set_ylim(0.2, 14.0)
    ax.axis("off")
    plt.tight_layout()
    plt.savefig("flowchart_sistem_silo.png", dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print("Saved flowchart_sistem_silo.png")

if __name__ == "__main__":
    generate_flowchart_xml()
    render_flowchart_png()
