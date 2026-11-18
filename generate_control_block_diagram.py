import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_block_xml():
    xml_content = """<mxfile host="app.diagrams.net" modified="2026-11-05T00:00:00.000Z" agent="Mozilla/5.0" version="21.6.8" type="device">
  <diagram id="blok_kendali_silo" name="Blok Diagram Sistem Kendali Tertutup Silo">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>

        <!-- Outer Boundary -->
        <mxCell id="outer_bg" value="SISTEM KENDALI LINGKAR TERTUTUP (CLOSED-LOOP PID) AERASI HEADSPACE SILO" style="swimlane;whiteSpace=wrap;html=1;fillColor=#0F172A;strokeColor=#0EA5E9;strokeWidth=2;fontColor=#0EA5E9;fontStyle=1;fontSize=13;startSize=30;rounded=1;" vertex="1" parent="1">
          <mxGeometry x="40" y="40" width="1080" height="420" as="geometry"/>
        </mxCell>

        <!-- Summing Point 1 -->
        <mxCell id="sum1" value="" style="ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor=#1E293B;strokeColor=#38BDF8;strokeWidth=2;" vertex="1" parent="outer_bg">
          <mxGeometry x="150" y="140" width="40" height="40" as="geometry"/>
        </mxCell>
        <mxCell id="sum1_plus" value="+" style="text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#10B981;fontStyle=1;fontSize=16;" vertex="1" parent="outer_bg">
          <mxGeometry x="120" y="130" width="30" height="30" as="geometry"/>
        </mxCell>
        <mxCell id="sum1_minus" value="-" style="text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#EF4444;fontStyle=1;fontSize=18;" vertex="1" parent="outer_bg">
          <mxGeometry x="155" y="180" width="30" height="30" as="geometry"/>
        </mxCell>

        <!-- Controller Box -->
        <mxCell id="controller" value="KONTROLER C(s)&#xa;Algoritma PID Diskrit (ESP32)&#xa;u(t) = Kp·e(t) + Ki∫e(t)dt + Kd·(de/dt)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#0EA5E9;strokeWidth=2;fontColor=#FFFFFF;fontStyle=1;fontSize=11;" vertex="1" parent="outer_bg">
          <mxGeometry x="250" y="120" width="220" height="80" as="geometry"/>
        </mxCell>

        <!-- Actuator Box -->
        <mxCell id="actuator" value="AKTUATOR&#xa;• Driver MOSFET HW-517 (PWM)&#xa;• Motor Kipas Blower Aerasi&#xa;• Micro Servo SG90 (Katup Atap)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#F59E0B;strokeWidth=2;fontColor=#FFFFFF;fontStyle=1;fontSize=11;" vertex="1" parent="outer_bg">
          <mxGeometry x="520" y="120" width="200" height="80" as="geometry"/>
        </mxCell>

        <!-- Summing Point 2 (Disturbance) -->
        <mxCell id="sum2" value="" style="ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor=#1E293B;strokeColor=#F59E0B;strokeWidth=2;" vertex="1" parent="outer_bg">
          <mxGeometry x="760" y="140" width="40" height="40" as="geometry"/>
        </mxCell>
        <mxCell id="sum2_plus1" value="+" style="text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#10B981;fontStyle=1;fontSize=16;" vertex="1" parent="outer_bg">
          <mxGeometry x="735" y="130" width="30" height="30" as="geometry"/>
        </mxCell>
        <mxCell id="sum2_plus2" value="+" style="text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#F59E0B;fontStyle=1;fontSize=16;" vertex="1" parent="outer_bg">
          <mxGeometry x="765" y="100" width="30" height="30" as="geometry"/>
        </mxCell>

        <!-- Disturbance Input -->
        <mxCell id="dist_input" value="d(t) GANGGUAN FISIK (DISTURBANCE)&#xa;Pelepasan Gas Fermentasi Bahan Curah / Saluran Tertutup Debu" style="text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#F59E0B;fontSize=10;fontStyle=1;" vertex="1" parent="outer_bg">
          <mxGeometry x="630" y="60" width="320" height="30" as="geometry"/>
        </mxCell>

        <!-- Plant Box -->
        <mxCell id="plant" value="PLANT FISIK G(s)&#xa;Ruang Headspace Silo (Volume V)&#xa;G(s) = [ K / (τ·s + 1) ] · e^(-L·s)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#10B981;strokeWidth=2;fontColor=#FFFFFF;fontStyle=1;fontSize=11;" vertex="1" parent="outer_bg">
          <mxGeometry x="840" y="120" width="200" height="80" as="geometry"/>
        </mxCell>

        <!-- Sensor Box (Feedback) -->
        <mxCell id="sensor" value="SENSOR FEEDBACK H(s)&#xa;Sensor Kualitas Udara MQ-135&#xa;Pembacaan Konsentrasi Gas Aktual (ADC 0-4095)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#38BDF8;strokeWidth=2;fontColor=#FFFFFF;fontStyle=1;fontSize=11;" vertex="1" parent="outer_bg">
          <mxGeometry x="500" y="280" width="240" height="70" as="geometry"/>
        </mxCell>

        <!-- Input Label -->
        <mxCell id="input_label" value="SETPOINT r(t)&#xa;Batas Gas Aman&#xa;(1500 ADC)" style="text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#38BDF8;fontStyle=1;fontSize=11;" vertex="1" parent="outer_bg">
          <mxGeometry x="20" y="130" width="100" height="50" as="geometry"/>
        </mxCell>

        <!-- Output Label -->
        <mxCell id="output_label" value="OUTPUT FISIK y(t)&#xa;Konsentrasi Gas Terkendali&#xa;(Mencapai Kondisi Aman)" style="text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontColor=#10B981;fontStyle=1;fontSize=11;" vertex="1" parent="outer_bg">
          <mxGeometry x="940" y="130" width="140" height="50" as="geometry"/>
        </mxCell>

        <!-- Edges -->
        <mxCell id="e_in" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#38BDF8;strokeWidth=2;" edge="1" parent="outer_bg" target="sum1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="110" y="160" as="sourcePoint"/>
          </mxGeometry>
        </mxCell>

        <mxCell id="e_err" value="Galat e(t)" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#38BDF8;strokeWidth=2;fontColor=#38BDF8;fontSize=10;" edge="1" parent="outer_bg" source="sum1" target="controller"/>
        
        <mxCell id="e_ctrl" value="u(t) (PWM)" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#0EA5E9;strokeWidth=2;fontColor=#0EA5E9;fontSize=10;" edge="1" parent="outer_bg" source="controller" target="actuator"/>

        <mxCell id="e_act_sum" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#F59E0B;strokeWidth=2;" edge="1" parent="outer_bg" source="actuator" target="sum2"/>

        <mxCell id="e_dist_sum" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#F59E0B;strokeWidth=2;" edge="1" parent="outer_bg" source="dist_input" target="sum2"/>

        <mxCell id="e_sum_plant" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#10B981;strokeWidth=2;" edge="1" parent="outer_bg" source="sum2" target="plant"/>

        <mxCell id="e_out" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#10B981;strokeWidth=2;" edge="1" parent="outer_bg" source="plant">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="1060" y="160" as="targetPoint"/>
          </mxGeometry>
        </mxCell>

        <!-- Feedback branch -->
        <mxCell id="e_fb_down" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#38BDF8;strokeWidth=2;" edge="1" parent="outer_bg" source="plant" target="sensor">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="1000" y="315"/>
            </Array>
          </mxGeometry>
        </mxCell>

        <mxCell id="e_fb_left" value="Umpan Balik y(t)" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#38BDF8;strokeWidth=2;fontColor=#38BDF8;fontSize=10;" edge="1" parent="outer_bg" source="sensor" target="sum1">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="170" y="315"/>
            </Array>
          </mxGeometry>
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""
    with open("blok_diagram_kendali_pid.drawio", "w", encoding="utf-8") as f:
        f.write(xml_content)
    print("Saved blok_diagram_kendali_pid.drawio")

def render_block_png():
    fig, ax = plt.subplots(figsize=(14, 5.5), dpi=300)
    ax.set_facecolor("#0F172A")
    fig.patch.set_facecolor("#0F172A")

    # Title Container
    rect_outer = patches.FancyBboxPatch((0.4, 0.4), 13.2, 4.7, boxstyle="round,pad=0.1,rounding_size=0.2",
                                        facecolor="#0B132B", edgecolor="#0EA5E9", linewidth=2.0)
    ax.add_patch(rect_outer)
    ax.text(7.0, 4.8, "SISTEM KENDALI LINGKAR TERTUTUP (CLOSED-LOOP PID) AERASI HEADSPACE SILO",
            color="#38BDF8", fontsize=11, fontweight="bold", ha="center")

    # Summing point 1
    circ1 = patches.Circle((2.3, 3.2), 0.3, facecolor="#1E293B", edgecolor="#38BDF8", linewidth=1.8)
    ax.add_patch(circ1)
    ax.text(2.3, 3.2, "+", color="#10B981", fontsize=14, fontweight="bold", ha="center", va="center")
    ax.text(2.3, 2.65, "-", color="#EF4444", fontsize=16, fontweight="bold", ha="center", va="center")

    # Input Setpoint r(t)
    ax.text(0.9, 3.2, "SETPOINT r(t)\nBatas Gas Aman\n(1500 ADC)", color="#38BDF8", fontsize=9, fontweight="bold", ha="center", va="center")
    ax.annotate("", xy=(2.0, 3.2), xytext=(1.5, 3.2), arrowprops=dict(arrowstyle="-|>", color="#38BDF8", lw=2, mutation_scale=14))

    # Error text
    ax.text(3.05, 3.45, "Error e(t)", color="#38BDF8", fontsize=9, ha="center")
    ax.annotate("", xy=(3.5, 3.2), xytext=(2.6, 3.2), arrowprops=dict(arrowstyle="-|>", color="#38BDF8", lw=2, mutation_scale=14))

    # Controller Box
    rect_c = patches.FancyBboxPatch((3.5, 2.4), 2.5, 1.6, boxstyle="round,pad=0.08,rounding_size=0.15",
                                    facecolor="#1E293B", edgecolor="#0EA5E9", linewidth=2.0)
    ax.add_patch(rect_c)
    ax.text(4.75, 3.2, "KONTROLER C(s)\nAlgoritma PID Diskrit\n(ESP32 NodeMCU)\nu(t) = Kp e + Ki∫e + Kd de/dt",
            color="#FFFFFF", fontsize=8.5, fontweight="bold", ha="center", va="center")

    # Control signal u(t)
    ax.text(6.4, 3.45, "u(t) (PWM)", color="#0EA5E9", fontsize=9, ha="center")
    ax.annotate("", xy=(6.7, 3.2), xytext=(6.0, 3.2), arrowprops=dict(arrowstyle="-|>", color="#0EA5E9", lw=2, mutation_scale=14))

    # Actuator Box
    rect_act = patches.FancyBboxPatch((6.7, 2.4), 2.3, 1.6, boxstyle="round,pad=0.08,rounding_size=0.15",
                                      facecolor="#1E293B", edgecolor="#F59E0B", linewidth=2.0)
    ax.add_patch(rect_act)
    ax.text(7.85, 3.2, "AKTUATOR\n• Driver MOSFET HW-517\n• Motor Kipas Blower DC\n• Micro Servo SG90 Katup",
            color="#FFFFFF", fontsize=8.5, fontweight="bold", ha="center", va="center")

    # Summing point 2 (Disturbance)
    circ2 = patches.Circle((9.5, 3.2), 0.25, facecolor="#1E293B", edgecolor="#F59E0B", linewidth=1.8)
    ax.add_patch(circ2)
    ax.text(9.5, 3.2, "+", color="#10B981", fontsize=12, fontweight="bold", ha="center", va="center")
    ax.annotate("", xy=(9.25, 3.2), xytext=(9.0, 3.2), arrowprops=dict(arrowstyle="-|>", color="#F59E0B", lw=2, mutation_scale=14))

    # Disturbance arrow & text
    ax.text(9.5, 4.3, "d(t) DISTURBANCE\nPelepasan Gas Fermentasi /\nSaluran Tersumbat Debu",
            color="#F59E0B", fontsize=8, fontweight="bold", ha="center", va="center")
    ax.annotate("", xy=(9.5, 3.45), xytext=(9.5, 3.9), arrowprops=dict(arrowstyle="-|>", color="#F59E0B", lw=2, mutation_scale=14))

    # Plant Box
    ax.annotate("", xy=(10.2, 3.2), xytext=(9.75, 3.2), arrowprops=dict(arrowstyle="-|>", color="#10B981", lw=2, mutation_scale=14))
    rect_plt = patches.FancyBboxPatch((10.2, 2.4), 2.3, 1.6, boxstyle="round,pad=0.08,rounding_size=0.15",
                                      facecolor="#1E293B", edgecolor="#10B981", linewidth=2.0)
    ax.add_patch(rect_plt)
    ax.text(11.35, 3.2, "PLANT FISIK G(s)\nRuang Headspace Silo\n(Volume V Bahan Baku)\nG(s) = [ K / (τ s + 1) ] · e^(-Ls)",
            color="#FFFFFF", fontsize=8.5, fontweight="bold", ha="center", va="center")

    # Output Arrow
    ax.annotate("", xy=(13.2, 3.2), xytext=(12.5, 3.2), arrowprops=dict(arrowstyle="-|>", color="#10B981", lw=2, mutation_scale=14))
    ax.text(13.0, 3.7, "OUTPUT y(t)\nKonsentrasi Gas\n(Aman & Stabil)", color="#10B981", fontsize=8.5, fontweight="bold", ha="center", va="center")

    # Feedback Loop Box
    rect_fb = patches.FancyBboxPatch((5.7, 0.8), 3.2, 1.1, boxstyle="round,pad=0.08,rounding_size=0.15",
                                     facecolor="#1E293B", edgecolor="#38BDF8", linewidth=2.0)
    ax.add_patch(rect_fb)
    ax.text(7.3, 1.35, "SENSOR FEEDBACK H(s)\nSensor Kualitas Udara MQ-135\nMembaca Konsentrasi Gas Aktual (ADC)",
            color="#FFFFFF", fontsize=8.5, fontweight="bold", ha="center", va="center")

    # Feedback lines
    ax.plot([12.7, 12.7, 8.9], [3.2, 1.35, 1.35], color="#38BDF8", lw=2)
    ax.annotate("", xy=(8.9, 1.35), xytext=(9.1, 1.35), arrowprops=dict(arrowstyle="-|>", color="#38BDF8", lw=2, mutation_scale=14))

    ax.plot([5.7, 2.3, 2.3], [1.35, 1.35, 2.9], color="#38BDF8", lw=2)
    ax.annotate("", xy=(2.3, 2.9), xytext=(2.3, 2.7), arrowprops=dict(arrowstyle="-|>", color="#38BDF8", lw=2, mutation_scale=14))
    ax.text(3.8, 1.55, "Sinyal Umpan Balik y(t)", color="#38BDF8", fontsize=8.5, ha="center")

    ax.set_xlim(0, 14)
    ax.set_ylim(0.2, 5.3)
    ax.axis("off")
    plt.tight_layout()
    plt.savefig("blok_diagram_kendali_pid.png", dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print("Saved blok_diagram_kendali_pid.png")

if __name__ == "__main__":
    generate_block_xml()
    render_block_png()
