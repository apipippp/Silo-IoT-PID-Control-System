import os
import math
import struct
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# =========================================================================
# STL 3D MESH GENERATOR
# =========================================================================
class STLMesh:
    def __init__(self):
        self.triangles = []

    def add_triangle(self, p1, p2, p3):
        v1 = np.array(p1, dtype=float)
        v2 = np.array(p2, dtype=float)
        v3 = np.array(p3, dtype=float)
        normal = np.cross(v2 - v1, v3 - v1)
        norm = np.linalg.norm(normal)
        if norm > 1e-9:
            normal = normal / norm
        else:
            normal = np.array([0.0, 0.0, 1.0])
        self.triangles.append((tuple(normal), tuple(p1), tuple(p2), tuple(p3)))

    def add_quad(self, p1, p2, p3, p4):
        self.add_triangle(p1, p2, p3)
        self.add_triangle(p1, p3, p4)

    def add_box(self, cx, cy, cz, sx, sy, sz):
        dx, dy, dz = sx / 2.0, sy / 2.0, sz / 2.0
        x0, x1 = cx - dx, cx + dx
        y0, y1 = cy - dy, cy + dy
        z0, z1 = cz - dz, cz + dz

        c000, c100 = (x0, y0, z0), (x1, y0, z0)
        c110, c010 = (x1, y1, z0), (x0, y1, z0)
        c001, c101 = (x0, y0, z1), (x1, y0, z1)
        c111, c011 = (x1, y1, z1), (x0, y1, z1)

        self.add_quad(c000, c010, c110, c100)
        self.add_quad(c001, c101, c111, c011)
        self.add_quad(c000, c100, c101, c001)
        self.add_quad(c110, c010, c011, c111)
        self.add_quad(c010, c000, c001, c011)
        self.add_quad(c100, c110, c111, c101)

    def add_cylinder(self, cx, cy, z_bottom, z_top, radius_bottom, radius_top=None, segments=24):
        if radius_top is None:
            radius_top = radius_bottom
        angles = [2.0 * math.pi * i / segments for i in range(segments)]
        bot_pts = [(cx + radius_bottom * math.cos(a), cy + radius_bottom * math.sin(a), z_bottom) for a in angles]
        top_pts = [(cx + radius_top * math.cos(a), cy + radius_top * math.sin(a), z_top) for a in angles]

        for i in range(segments):
            ni = (i + 1) % segments
            self.add_quad(bot_pts[i], bot_pts[ni], top_pts[ni], top_pts[i])

        c_bot = (cx, cy, z_bottom)
        c_top = (cx, cy, z_top)
        for i in range(segments):
            ni = (i + 1) % segments
            self.add_triangle(c_bot, bot_pts[ni], bot_pts[i])
            self.add_triangle(c_top, top_pts[i], top_pts[ni])

    def add_sg90_simple(self, cx, cy, cz, rot_y_deg=0, rot_z_deg=0):
        # Clean representation of SG90 (Body: 23x12x22mm + Top Gear + Horn)
        # Main body
        self.add_box(cx, cy, cz, 22.8, 12.2, 22.5)
        # Mounting ears
        self.add_box(cx, cy, cz + 6.0, 32.0, 12.0, 2.5)
        # Gear tower
        self.add_cylinder(cx + 5.5, cy, cz + 11.25, cz + 16.0, 6.0, 6.0, segments=16)
        # White Horn
        self.add_box(cx + 10.5, cy, cz + 16.5, 14.0, 5.0, 2.0)

    def write_binary_stl(self, filepath, name="Model"):
        header = f"Tinkercad Ready 3D Model: {name}".encode('ascii')[:80]
        header = header.ljust(80, b'\0')
        count = len(self.triangles)

        with open(filepath, "wb") as f:
            f.write(header)
            f.write(struct.pack("<I", count))
            for normal, v1, v2, v3 in self.triangles:
                f.write(struct.pack("<3f", *normal))
                f.write(struct.pack("<3f", *v1))
                f.write(struct.pack("<3f", *v2))
                f.write(struct.pack("<3f", *v3))
                f.write(struct.pack("<H", 0))
        print(f"Exported STL: {filepath} ({count} triangles, {os.path.getsize(filepath) / 1024:.1f} KB)")

    def write_obj(self, filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("# Tinkercad Ready Wavefront OBJ\n")
            vert_map = {}
            vert_list = []
            faces = []

            def get_v_idx(pt):
                key = (round(pt[0], 4), round(pt[1], 4), round(pt[2], 4))
                if key not in vert_map:
                    vert_map[key] = len(vert_list) + 1
                    vert_list.append(key)
                return vert_map[key]

            for normal, v1, v2, v3 in self.triangles:
                i1 = get_v_idx(v1)
                i2 = get_v_idx(v2)
                i3 = get_v_idx(v3)
                faces.append((i1, i2, i3))

            for v in vert_list:
                f.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")
            for face in faces:
                f.write(f"f {face[0]} {face[1]} {face[2]}\n")
        print(f"Exported OBJ: {filepath} ({len(faces)} faces, {os.path.getsize(filepath) / 1024:.1f} KB)")


# =========================================================================
# 1. BUILD ULTRA SIMPLE 3D ROBOTIC ARM ASSEMBLY
# =========================================================================
def build_ultra_simple_arm_3d():
    mesh = STLMesh()
    T = 3.0  # 3mm acrylic thickness

    # PART 1: BASE PLATE (Alas meja 70 x 70 mm, tebal 3mm di Z: 0..3 mm)
    mesh.add_box(0, 0, 1.5, 70, 70, T)
    # 4 Kaki karet
    for fx, fy in [(-28, -28), (28, -28), (28, 28), (-28, 28)]:
        mesh.add_cylinder(fx, fy, -2, 0, 3.5, 3.5, segments=12)

    # SERVO 1: BASE ROTATION SERVO (di dalam lubang base)
    mesh.add_sg90_simple(0, 0, 12)

    # PART 2: TURNTABLE DISC (Diameter 50 mm, Z: 26..29 mm)
    mesh.add_cylinder(0, 0, 26, 29, 25, 25, segments=28)

    # PART 3: SHOULDER UPRIGHT L-BRACKET (Plat tegak penahan servo bahu, Z: 29..65 mm)
    # Menempel di atas turntable
    mesh.add_box(-10, 0, 47, T, 32, 36)

    # SERVO 2: SHOULDER SERVO (Bahu, Z = 50 mm)
    mesh.add_box(5, 0, 50, 22.8, 12.2, 22.5)
    # Gear tower keluar ke arah Y+
    mesh.add_cylinder(10.5, 6.1, 50, 50, 5.5, 5.5, segments=16)

    # PART 4: MAIN ARM (BICEP / LENGAN BAWAH)
    # Satu batang akrilik lurus ramping (65 mm x 16 mm x 3 mm)
    # Menghubungkan bahu (Z=50) ke siku (X=35, Z=85)
    p1 = np.array([10.5, 8.0, 50.0])
    p2 = np.array([45.5, 8.0, 85.0])
    v = p2 - p1
    length = np.linalg.norm(v)
    mid = (p1 + p2) / 2.0
    # Add arm beam
    mesh.add_box(mid[0], mid[1], mid[2], length, T, 16)

    # SERVO 3: ELBOW SERVO (Siku di X=45.5, Z=85)
    mesh.add_box(45.5, 0, 85, 22.8, 12.2, 22.5)

    # PART 5: FOREARM (LENGAN ATAS)
    # Satu batang akrilik lurus ramping (55 mm x 14 mm x 3 mm)
    # Dari siku (45.5, 85) mengarah ke gripper (95, 75)
    p3 = np.array([45.5, -8.0, 85.0])
    p4 = np.array([92.0, -8.0, 75.0])
    v2 = p4 - p3
    l2 = np.linalg.norm(v2)
    mid2 = (p3 + p4) / 2.0
    mesh.add_box(mid2[0], mid2[1], mid2[2], l2, T, 14)

    # PART 6: GRIPPER BASE PLATE + FIXED CLAW (Hanya 1 keping!)
    # Plat dudukan servo gripper + jari tetap yang memanjang ke depan
    # Terletak di X = 105, Z = 75
    mesh.add_box(110, 0, 73.5, 34, 26, T)
    # Fixed claw (Jari capit diam menonjol ke depan)
    mesh.add_box(135, -9, 73.5, 28, 6, T)
    mesh.add_box(148, -5, 73.5, 6, 8, T)  # Kait ujung

    # SERVO 4: GRIPPER SERVO (SG90 diletakkan tidur rata di gripper base)
    mesh.add_box(108, 0, 83, 22.8, 12.2, 16)
    # Gear tower & horn di Z = 92 mm
    mesh.add_cylinder(113.5, 0, 91, 93, 5.0, 5.0, segments=16)

    # PART 7: MOVING CLAW (Jari capit gerak, langsung dibaut ke servo horn!)
    # Memutar dari poros servo horn di (113.5, 0)
    mesh.add_box(135, 7, 93.5, 28, 6, T)
    mesh.add_box(148, 4, 93.5, 6, 8, T)  # Kait ujung capit gerak

    # Benda yang dijepit (Mini Box 14x14x14 mm)
    mesh.add_box(147, 0, 83.5, 12, 12, 12)

    return mesh


# =========================================================================
# 2. BUILD 3D FLAT ACRYLIC SHEET (7 PARTS TOTAL)
# =========================================================================
def build_ultra_simple_flat_3d():
    mesh = STLMesh()
    T = 3.0

    # 1. Base Plate (70x70 mm)
    mesh.add_box(-45, -45, 1.5, 70, 70, T)

    # 2. Turntable Disc (Dia 50 mm)
    mesh.add_cylinder(35, -45, 0, T, 25, 25, segments=28)

    # 3. Shoulder Upright Bracket (36x30 mm)
    mesh.add_box(75, -45, 1.5, 28, 36, T)

    # 4. Main Arm (Bicep) (70x16 mm)
    mesh.add_box(-45, 25, 1.5, 16, 70, T)

    # 5. Forearm (60x14 mm)
    mesh.add_box(-15, 25, 1.5, 14, 60, T)

    # 6. Gripper Base + Fixed Claw (1 keping gabungan)
    mesh.add_box(25, 25, 1.5, 45, 26, T)

    # 7. Gripper Moving Claw (1 keping langsung ke horn)
    mesh.add_box(70, 25, 1.5, 34, 12, T)

    return mesh


# =========================================================================
# 3. BUILD ULTRA SIMPLE 2D LASER CUT VECTOR (SVG & DXF)
# =========================================================================
def generate_simple_laser_svg(out_path):
    # Minimalist Sheet: 200 mm x 150 mm (Super compact, hemat bahan akrilik!)
    svg = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 210 160" width="210mm" height="160mm" style="background:#0F172A; font-family:'Segoe UI',Roboto,Helvetica,sans-serif;">
  <defs>
    <style>
      .cut { fill: none; stroke: #EF4444; stroke-width: 0.25; }
      .slot { fill: none; stroke: #EF4444; stroke-width: 0.25; }
      .hole { fill: none; stroke: #EF4444; stroke-width: 0.25; }
      .engrave { fill: #38BDF8; font-size: 3.0px; font-weight: bold; }
      .subtext { fill: #94A3B8; font-size: 2.2px; }
      .sheet { fill: none; stroke: #334155; stroke-width: 0.5; stroke-dasharray: 2 1; }
    </style>
  </defs>

  <!-- Sheet Boundary: 190 mm x 140 mm Acrylic Sheet (3mm Thickness) -->
  <rect x="10" y="10" width="190" height="140" rx="3" class="sheet"/>
  
  <text x="15" y="17" fill="#F8FAFC" font-size="4" font-weight="bold">POLA ULTRA-SIMPLE ROBOTIC ARM SG90 (HANYA 7 KEPING AKRILIK 3mm)</text>
  <text x="15" y="22" fill="#94A3B8" font-size="2.4">Desain Minimalis: Hemat Bahan, Nol Roda Gigi, Cepat Dirakit | Skala 1:1 mm | Merah: Laser Cut</text>

  <!-- ======================================================= -->
  <!-- 1. BASE PLATE (70 x 70 mm) - Keping 1 -->
  <!-- ======================================================= -->
  <g id="part-1-base">
    <rect x="15" y="27" width="70" height="70" rx="5" class="cut"/>
    <!-- Slot Servo Base SG90 (23 x 12.5 mm) -->
    <rect x="38.5" y="55.75" width="23" height="12.5" class="slot"/>
    <circle cx="34.5" cy="62" r="1.1" class="hole"/>
    <circle cx="65.5" cy="62" r="1.1" class="hole"/>
    <!-- 4 Lubang Kaki Karet / Meja M3 -->
    <circle cx="22" cy="34" r="1.6" class="hole"/>
    <circle cx="78" cy="34" r="1.6" class="hole"/>
    <circle cx="22" cy="90" r="1.6" class="hole"/>
    <circle cx="78" cy="90" r="1.6" class="hole"/>
    <text x="50" y="40" class="engrave" text-anchor="middle">1. BASE PLATE</text>
    <text x="50" y="44" class="subtext" text-anchor="middle">70 x 70 mm</text>
  </g>

  <!-- ======================================================= -->
  <!-- 2. TURNTABLE DISC (Dia 50 mm) - Keping 2 -->
  <!-- ======================================================= -->
  <g id="part-2-turntable">
    <circle cx="120" cy="55" r="25" class="cut"/>
    <!-- Center Horn Screw -->
    <circle cx="120" cy="55" r="1.2" class="hole"/>
    <!-- Horn Fixing holes -->
    <circle cx="120" cy="48" r="0.9" class="hole"/>
    <circle cx="120" cy="62" r="0.9" class="hole"/>
    <!-- Slot kancing siku plat bahu (3.0 x 18 mm) -->
    <rect x="105" y="46" width="3.2" height="18" rx="0.3" class="slot"/>
    <text x="120" y="38" class="engrave" text-anchor="middle">2. TURNTABLE</text>
    <text x="120" y="74" class="subtext" text-anchor="middle">Dia 50 mm</text>
  </g>

  <!-- ======================================================= -->
  <!-- 3. SHOULDER BRACKET (34 x 26 mm) - Keping 3 -->
  <!-- ======================================================= -->
  <g id="part-3-shoulder">
    <!-- Plat tegak penahan servo bahu -->
    <path d="M 155 30 L 185 30 L 185 62 L 175 62 L 175 66 L 165 66 L 165 62 L 155 62 Z" class="cut"/>
    <!-- Slot Servo Bahu SG90 -->
    <rect x="158.5" y="38" width="23" height="12.5" class="slot"/>
    <circle cx="155.5" cy="44.25" r="1.1" class="hole"/>
    <circle cx="184.5" cy="44.25" r="1.1" class="hole"/>
    <text x="170" y="35" class="engrave" text-anchor="middle">3. SHOULDER</text>
  </g>

  <!-- ======================================================= -->
  <!-- 4. MAIN BICEP ARM (70 x 16 mm) - Keping 4 -->
  <!-- ======================================================= -->
  <g id="part-4-bicep">
    <!-- Lengan Bawah: Satu batang ramping lurus -->
    <rect x="15" y="105" width="65" height="16" rx="4" class="cut"/>
    <!-- Lubang pasang servo horn bahu di ujung kiri -->
    <circle cx="23" cy="113" r="1.2" class="hole"/>
    <circle cx="19" cy="113" r="0.9" class="hole"/>
    <circle cx="27" cy="113" r="0.9" class="hole"/>
    <!-- Lubang baut servo siku di ujung kanan -->
    <circle cx="72" cy="113" r="1.6" class="hole"/>
    <text x="47" y="114" class="engrave" text-anchor="middle">4. BICEP ARM (65mm)</text>
  </g>

  <!-- ======================================================= -->
  <!-- 5. FOREARM (58 x 14 mm) - Keping 5 -->
  <!-- ======================================================= -->
  <g id="part-5-forearm">
    <!-- Lengan Atas: Satu batang ramping lurus -->
    <rect x="88" y="105" width="55" height="14" rx="4" class="cut"/>
    <!-- Lubang pasang servo horn siku di ujung kiri -->
    <circle cx="95" cy="112" r="1.2" class="hole"/>
    <circle cx="91" cy="112" r="0.9" class="hole"/>
    <circle cx="99" cy="112" r="0.9" class="hole"/>
    <!-- Lubang pasang plat gripper di ujung kanan -->
    <circle cx="136" cy="112" r="1.6" class="hole"/>
    <text x="116" y="113" class="engrave" text-anchor="middle">5. FOREARM (55mm)</text>
  </g>

  <!-- ======================================================= -->
  <!-- 6. GRIPPER BASE + FIXED CLAW (All-In-One) - Keping 6 -->
  <!-- ======================================================= -->
  <g id="part-6-gripper-base">
    <!-- Dudukan servo SG90 dan Capit Tetap (Fixed Jaw) jadi 1 keping utuh! -->
    <path d="M 150 75 
             L 178 75 
             L 178 95 
             L 195 95 
             L 198 100 
             L 195 103 
             L 178 103 
             L 178 112 
             L 150 112 Z" class="cut"/>
    <!-- Slot Servo Gripper SG90 -->
    <rect x="152.5" y="82" width="23" height="12.5" class="slot"/>
    <circle cx="149.5" cy="88.25" r="1.1" class="hole"/>
    <circle cx="177.5" cy="88.25" r="1.1" class="hole"/>
    <text x="164" y="80" class="engrave" text-anchor="middle">6. GRIPPER BASE</text>
    <text x="164" y="108" class="subtext" text-anchor="middle">+ FIXED CLAW</text>
  </g>

  <!-- ======================================================= -->
  <!-- 7. GRIPPER MOVING CLAW - Keping 7 -->
  <!-- ======================================================= -->
  <g id="part-7-moving-claw">
    <!-- Jari capit gerak yang langsung dibaut ke servo horn putih SG90 -->
    <path d="M 150 120 
             L 182 120 
             L 186 126 
             L 182 130 
             L 158 130 
             C 152 130, 148 126, 150 120 Z" class="cut"/>
    <!-- Lubang horn servo SG90 -->
    <circle cx="155" cy="125" r="1.2" class="hole"/>
    <circle cx="160" cy="125" r="0.9" class="hole"/>
    <circle cx="165" cy="125" r="0.9" class="hole"/>
    <text x="168" y="137" class="engrave" text-anchor="middle">7. MOVING CLAW</text>
  </g>

  <!-- Ringkasan Kebutuhan Hardware -->
  <g id="spec">
    <rect x="15" y="128" width="128" height="18" rx="2" fill="#1E293B" stroke="#334155" stroke-width="0.4"/>
    <text x="20" y="135" fill="#38BDF8" font-size="2.4" font-weight="bold">TOTAL PART: HANYA 7 KEPING AKRILIK!</text>
    <text x="20" y="141" fill="#94A3B8" font-size="2.0">Baut tambahan: Cuma butuh 4 pcs Baut M3x10mm. Sisanya pakai horn &amp; baut bawaan SG90.</text>
  </g>
</svg>
"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Exported Ultra Simple SVG: {out_path}")


def generate_simple_laser_dxf(out_path):
    lines = ["0\nSECTION\n2\nENTITIES\n"]
    def dxf_line(x1, y1, x2, y2):
        return f"0\nLINE\n8\nCUT\n10\n{x1:.3f}\n20\n{y1:.3f}\n30\n0.0\n11\n{x2:.3f}\n21\n{y2:.3f}\n31\n0.0\n"
    def dxf_circle(cx, cy, r):
        return f"0\nCIRCLE\n8\nCUT\n10\n{cx:.3f}\n20\n{cy:.3f}\n30\n0.0\n40\n{r:.3f}\n"
    def dxf_rect(x, y, w, h):
        return dxf_line(x, y, x+w, y) + dxf_line(x+w, y, x+w, y+h) + dxf_line(x+w, y+h, x, y+h) + dxf_line(x, y+h, x, y)

    # 1. Base Plate
    lines.append(dxf_rect(15, 27, 70, 70))
    lines.append(dxf_rect(38.5, 55.75, 23, 12.5))
    lines.append(dxf_circle(22, 34, 1.6))
    lines.append(dxf_circle(78, 34, 1.6))
    lines.append(dxf_circle(22, 90, 1.6))
    lines.append(dxf_circle(78, 90, 1.6))

    # 2. Turntable Disc
    lines.append(dxf_circle(120, 55, 25))
    lines.append(dxf_circle(120, 55, 1.2))

    # 3. Shoulder
    lines.append(dxf_rect(155, 30, 30, 32))
    lines.append(dxf_rect(158.5, 38, 23, 12.5))

    # 4. Bicep Arm
    lines.append(dxf_rect(15, 105, 65, 16))

    # 5. Forearm
    lines.append(dxf_rect(88, 105, 55, 14))

    # 6. Gripper Base
    lines.append(dxf_rect(150, 75, 28, 37))
    lines.append(dxf_rect(178, 95, 17, 8))

    # 7. Moving Claw
    lines.append(dxf_rect(150, 120, 32, 10))

    lines.append("0\nENDSEC\n0\nEOF\n")
    with open(out_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"Exported Ultra Simple DXF: {out_path}")


# =========================================================================
# MAIN EXECUTION
# =========================================================================
def main():
    target_dir = os.path.abspath("desain_arm_simple_7part")
    os.makedirs(target_dir, exist_ok=True)
    
    repo_target = os.path.abspath("TugasBesarIOT_SiloMonitoringSystem/desain_arm_simple_7part")
    os.makedirs(repo_target, exist_ok=True)

    print("Generating Ultra-Simple 7-Part Arm for Tinkercad & Laser Cutting...")

    # 1. 3D Assembly
    arm_3d = build_ultra_simple_arm_3d()
    arm_3d.write_binary_stl(os.path.join(target_dir, "arm_simple_7part_assembly.stl"), "Simple Arm Assembly")
    arm_3d.write_obj(os.path.join(target_dir, "arm_simple_7part_assembly.obj"))

    # 2. 3D Flat Sheet Plate
    flat_3d = build_ultra_simple_flat_3d()
    flat_3d.write_binary_stl(os.path.join(target_dir, "arm_simple_flat_parts.stl"), "Flat Acrylic Parts")
    flat_3d.write_obj(os.path.join(target_dir, "arm_simple_flat_parts.obj"))

    # 3. 2D Vector Laser Cut Files (SVG & DXF)
    svg_file = os.path.join(target_dir, "pola_laser_cut_arm_simple_7part.svg")
    generate_simple_laser_svg(svg_file)

    dxf_file = os.path.join(target_dir, "pola_laser_cut_arm_simple_7part.dxf")
    generate_simple_laser_dxf(dxf_file)

    # 4. Render 3D Preview
    print("Rendering 3D preview...")
    fig = plt.figure(figsize=(9, 7.5), facecolor='#0F172A')
    ax = fig.add_subplot(111, projection='3d', facecolor='#0F172A')
    
    step = max(1, len(arm_3d.triangles) // 2000)
    t_sampled = [[t[1], t[2], t[3]] for i, t in enumerate(arm_3d.triangles) if i % step == 0]
    mesh_poly = Poly3DCollection(t_sampled, facecolors='#38BDF8', edgecolors='#0369A1', linewidths=0.3, alpha=0.9)
    ax.add_collection3d(mesh_poly)

    ax.set_xlim(-50, 160)
    ax.set_ylim(-50, 50)
    ax.set_zlim(0, 120)
    ax.set_xlabel('X (mm)', color='#94A3B8')
    ax.set_ylabel('Y (mm)', color='#94A3B8')
    ax.set_zlabel('Z (mm)', color='#94A3B8')
    ax.tick_params(colors='#64748B')
    ax.view_init(elev=24, azim=-55)
    ax.set_title('PREVIEW 3D: ULTRA-SIMPLE ROBOTIC ARM (7-PART AKRILIK 3mm)\n(Ready Tinkercad .STL & Laser Cutting .SVG)', color='#F8FAFC', fontsize=11, weight='bold')

    plt.tight_layout()
    preview_3d_file = os.path.join(target_dir, "preview_simple_arm_3d.png")
    plt.savefig(preview_3d_file, dpi=200, facecolor=fig.get_facecolor())
    plt.close()

    # 5. Render 2D Layout Preview
    print("Rendering 2D layout preview...")
    fig2, ax2 = plt.subplots(figsize=(9, 7), facecolor='#0F172A')
    ax2.set_facecolor('#0F172A')

    # Sheet outline
    ax2.add_patch(patches.Rectangle((10, 10), 190, 140, edgecolor='#475569', facecolor='#1E293B', linestyle='--', linewidth=1))

    # 7 Parts Boxes
    # 1. Base
    ax2.add_patch(patches.Rectangle((15, 27), 70, 70, edgecolor='#EF4444', facecolor='#0284C7', alpha=0.35, linewidth=1.5))
    ax2.text(50, 62, '1. BASE PLATE\\n70x70 mm', color='#F8FAFC', ha='center', va='center', weight='bold', fontsize=8)

    # 2. Turntable
    ax2.add_patch(patches.Circle((120, 55), 25, edgecolor='#EF4444', facecolor='#0284C7', alpha=0.35, linewidth=1.5))
    ax2.text(120, 55, '2. TURNTABLE\\nDia 50 mm', color='#F8FAFC', ha='center', va='center', weight='bold', fontsize=8)

    # 3. Shoulder
    ax2.add_patch(patches.Rectangle((155, 30), 30, 32, edgecolor='#EF4444', facecolor='#0284C7', alpha=0.35, linewidth=1.5))
    ax2.text(170, 46, '3. SHOULDER\\nBRACKET', color='#F8FAFC', ha='center', va='center', weight='bold', fontsize=7.5)

    # 4. Bicep
    ax2.add_patch(patches.Rectangle((15, 105), 65, 16, edgecolor='#EF4444', facecolor='#0284C7', alpha=0.35, linewidth=1.5))
    ax2.text(47, 113, '4. BICEP LINK (65mm)', color='#F8FAFC', ha='center', va='center', weight='bold', fontsize=7.5)

    # 5. Forearm
    ax2.add_patch(patches.Rectangle((88, 105), 55, 14, edgecolor='#EF4444', facecolor='#0284C7', alpha=0.35, linewidth=1.5))
    ax2.text(115, 112, '5. FOREARM (55mm)', color='#F8FAFC', ha='center', va='center', weight='bold', fontsize=7.5)

    # 6. Gripper Base
    ax2.add_patch(patches.Rectangle((150, 75), 45, 26, edgecolor='#EF4444', facecolor='#0284C7', alpha=0.35, linewidth=1.5))
    ax2.text(172, 88, '6. GRIPPER BASE\\n+ FIXED JAW', color='#F8FAFC', ha='center', va='center', weight='bold', fontsize=7.5)

    # 7. Moving Claw
    ax2.add_patch(patches.Rectangle((150, 115), 36, 15, edgecolor='#EF4444', facecolor='#0284C7', alpha=0.35, linewidth=1.5))
    ax2.text(168, 122, '7. MOVING JAW\\n(Baut ke Horn)', color='#F8FAFC', ha='center', va='center', weight='bold', fontsize=7.5)

    ax2.set_xlim(0, 210)
    ax2.set_ylim(160, 0)
    ax2.tick_params(colors='#64748B')
    ax2.set_xlabel('X (mm)', color='#94A3B8')
    ax2.set_ylabel('Y (mm)', color='#94A3B8')
    ax2.set_title('LAYOUT POLA LASER CUT 2D (AKRILIK 3mm) — TOTAL HANYA 7 KEPING', color='#F8FAFC', fontsize=11, weight='bold')

    plt.tight_layout()
    preview_2d_file = os.path.join(target_dir, "preview_simple_arm_2d.png")
    plt.savefig(preview_2d_file, dpi=200, facecolor=fig2.get_facecolor())
    plt.close()

    # Copy all to repo folder
    import shutil
    for f in os.listdir(target_dir):
        src = os.path.join(target_dir, f)
        dst = os.path.join(repo_target, f)
        if os.path.isfile(src):
            shutil.copy2(src, dst)

    print(f"\nAll files successfully generated in:\n  - {target_dir}\n  - {repo_target}")

if __name__ == "__main__":
    main()
