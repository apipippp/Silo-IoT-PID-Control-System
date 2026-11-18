import os
import math
import struct
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# =========================================================================
# STL EXPORTER (PRISMATIC EXTRUDED 2D PROFILES FOR LASER CUT ACRYLIC)
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

    def add_cylinder(self, cx, cy, z_bottom, z_top, radius, segments=32):
        angles = [2.0 * math.pi * i / segments for i in range(segments)]
        bot_pts = [(cx + radius * math.cos(a), cy + radius * math.sin(a), z_bottom) for a in angles]
        top_pts = [(cx + radius * math.cos(a), cy + radius * math.sin(a), z_top) for a in angles]

        for i in range(segments):
            ni = (i + 1) % segments
            self.add_quad(bot_pts[i], bot_pts[ni], top_pts[ni], top_pts[i])

        c_bot = (cx, cy, z_bottom)
        c_top = (cx, cy, z_top)
        for i in range(segments):
            ni = (i + 1) % segments
            self.add_triangle(c_bot, bot_pts[ni], bot_pts[i])
            self.add_triangle(c_top, top_pts[i], top_pts[ni])

    def extrude_polygon(self, pts_2d, z_bottom, z_top):
        # Clean sharp prismatic extrusion of any 2D polygon (laser cut slab)
        n = len(pts_2d)
        for i in range(n):
            ni = (i + 1) % n
            p1 = (pts_2d[i][0], pts_2d[i][1], z_bottom)
            p2 = (pts_2d[ni][0], pts_2d[ni][1], z_bottom)
            p3 = (pts_2d[ni][0], pts_2d[ni][1], z_top)
            p4 = (pts_2d[i][0], pts_2d[i][1], z_top)
            self.add_quad(p1, p2, p3, p4)

        # Polygon caps (ear clipping or fan from center)
        cx = sum(p[0] for p in pts_2d) / n
        cy = sum(p[1] for p in pts_2d) / n
        c_bot = (cx, cy, z_bottom)
        c_top = (cx, cy, z_top)
        for i in range(n):
            ni = (i + 1) % n
            self.add_triangle(c_bot, (pts_2d[ni][0], pts_2d[ni][1], z_bottom), (pts_2d[i][0], pts_2d[i][1], z_bottom))
            self.add_triangle(c_top, (pts_2d[i][0], pts_2d[i][1], z_top), (pts_2d[ni][0], pts_2d[ni][1], z_top))

    def write_binary_stl(self, filepath, name="CleanAcrylicArm"):
        header = f"Clean Acrylic Arm 3mm: {name}".encode('ascii')[:80]
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
        print(f"Exported STL: {filepath} ({count} tris, {os.path.getsize(filepath) / 1024:.1f} KB)")


# =========================================================================
# 1. GENERATE CLEAN 2D CONTOURS FOR EVERY ACRYLIC PART
# =========================================================================

# HELPER: Generate flat 2D claw with integrated spur gear sector
def get_geared_claw_polygon(is_left=True):
    # Center of rotation at (0, 0)
    # Pitch radius = 9.0 mm, 5 gear teeth along 70 degrees arc
    pts = []
    # Gear teeth sector (at angle range)
    # Pitch radius 9mm. Tooth addendum +1.5mm, dedendum -1.2mm
    num_teeth = 4
    if is_left:
        # Meshes towards +Y
        # Teeth between -30 to +40 degrees
        start_deg, end_deg = -35.0, 45.0
        claw_extend = 1.0
    else:
        # Meshes towards -Y
        start_deg, end_deg = 180.0 - 45.0, 180.0 + 35.0
        claw_extend = -1.0

    steps = num_teeth * 4
    for i in range(steps + 1):
        frac = i / steps
        ang = math.radians(start_deg + frac * (end_deg - start_deg))
        # Trapezoid tooth profile
        phase = frac * num_teeth * 2.0 * math.pi
        r = 9.0 + 1.4 * math.sin(phase)
        pts.append((r * math.cos(ang), r * math.sin(ang)))

    # Outer curved claw arm extending forward (+X)
    if is_left:
        pts.extend([
            (10.0, 7.0),
            (22.0, 14.0),
            (36.0, 12.0),
            (45.0, 4.0),   # Claw Tip
            (44.0, 2.0),
            (35.0, 6.0),   # Inner grip face
            (24.0, 5.0),
            (12.0, 0.0),
            (0.0, -5.0),
            (-7.0, -3.0)
        ])
    else:
        pts.extend([
            (-7.0, 3.0),
            (0.0, 5.0),
            (12.0, 0.0),
            (24.0, -5.0),
            (35.0, -6.0),
            (44.0, -2.0),
            (45.0, -4.0),  # Claw Tip
            (36.0, -12.0),
            (22.0, -14.0),
            (10.0, -7.0)
        ])
    return pts


# =========================================================================
# 2. BUILD CLEAN ASSEMBLED 3D MODEL (ALL FLAT 3MM ACRYLIC PLATES)
# =========================================================================
def build_clean_acrylic_arm_assembled():
    mesh = STLMesh()
    T = 3.0  # 3mm laser cut acrylic

    # BASE (X = 0, Y = 0)
    # 1. Base Plate: Round disc 60mm dia with 3 mounting ears (Z: 0 to 3mm)
    mesh.add_cylinder(0, 0, 0, T, 28)
    for a in [0, 120, 240]:
        rad = math.radians(a)
        mesh.add_cylinder(31 * math.cos(rad), 31 * math.sin(rad), 0, T, 4.5)

    # Servo 1 (Base SG90): sits upright inside base
    mesh.add_box(0, 0, 15, 23, 12.5, 22)
    mesh.add_cylinder(0, 0, 26, 29, 6)

    # 2. Turntable Plate: Round disc 56mm dia (Z: 29 to 32mm)
    mesh.add_cylinder(0, 0, 29, 32, 26)

    # 3. Shoulder Vertical Clevis Brackets (2 flat 3mm acrylic plates)
    # Upright plates at Y = -14 and Y = +14 (Z: 32 to 62mm)
    mesh.add_box(0, -14, 47, 18, T, 30)
    mesh.add_box(0, 14, 47, 18, T, 30)

    # Servo 2 (Shoulder SG90): horizontal at Z = 48mm
    mesh.add_box(0, 0, 48, 23, 12.5, 22)

    # 4. Lower Arm (Link 1 - Dual parallel flat acrylic beams 3mm)
    # Length: 65 mm. Rotated at 40 degrees forward-upward
    # Pivot at (0, 48), Elbow at (32, 85)
    # Flat rectangular beam at Y = -16 and Y = +16
    mesh.add_box(16, -15.5, 66.5, 50, T, 16)
    mesh.add_box(16, 15.5, 66.5, 50, T, 16)

    # Servo 3 (Elbow SG90): at X = 32, Z = 85
    mesh.add_box(32, 0, 85, 23, 12.5, 22)

    # 5. Upper Forearm (Link 2 - Flat acrylic beam 3mm)
    # From Elbow (32, 85) reaching forward-downward to Wrist (80, 75)
    mesh.add_box(56, -10, 80, 52, T, 14)

    # 6. Gripper Base Plate: Flat 3mm acrylic plate (Z: 73.5 to 76.5mm)
    # Size 36 x 40 x 3 mm
    mesh.add_box(86, 0, 75, 30, 40, T)

    # Servo 4 (Gripper SG90): sits flat on top of the plate
    mesh.add_box(80, 0, 85, 23, 12.5, 16)
    mesh.add_cylinder(85, -9, 93, 96, 5)

    # 7. Geared Claws (2 Flat 3mm Acrylic Plates with Teeth)
    # Claw Left (Meshes at Y = 0)
    claw_l = get_geared_claw_polygon(is_left=True)
    # Place at (X = 85, Y = -9, Z: 70 to 73 mm)
    t_claw_l = [(p[0] + 85, p[1] - 9) for p in claw_l]
    mesh.extrude_polygon(t_claw_l, z_bottom=70, z_top=73)

    # Claw Right (Meshes at Y = 0)
    claw_r = get_geared_claw_polygon(is_left=False)
    # Place at (X = 85, Y = +9, Z: 70 to 73 mm)
    t_claw_r = [(p[0] + 85, p[1] + 9) for p in claw_r]
    mesh.extrude_polygon(t_claw_r, z_bottom=70, z_top=73)

    # Baut poros M3 silinder halus
    mesh.add_cylinder(85, -9, 68, 78, 1.6)
    mesh.add_cylinder(85, 9, 68, 78, 1.6)

    # Red Box being clamped right between the flat claws!
    mesh.add_box(120, 0, 71.5, 18, 18, 18)

    return mesh


# =========================================================================
# 3. BUILD FLAT 2D/3D LASER CUT ACRYLIC PLATE (TEBAL PERSIS 3.0 MM)
# =========================================================================
def build_clean_acrylic_flat_sheet():
    mesh = STLMesh()
    T = 3.0

    # Part 1: Base Plate (Round 60mm with tabs)
    mesh.add_cylinder(-50, -40, 0, T, 28)
    for a in [0, 120, 240]:
        rad = math.radians(a)
        mesh.add_cylinder(-50 + 31 * math.cos(rad), -40 + 31 * math.sin(rad), 0, T, 4.5)

    # Part 2: Turntable (Round 56mm)
    mesh.add_cylinder(25, -40, 0, T, 26)

    # Part 3: Shoulder Uprights (2 pcs)
    mesh.add_box(70, -55, T/2, 18, 30, T)
    mesh.add_box(70, -20, T/2, 18, 30, T)

    # Part 4: Lower Arm Beams (2 pcs)
    mesh.add_box(-55, 25, T/2, 60, 16, T)
    mesh.add_box(-55, 50, T/2, 60, 16, T)

    # Part 5: Forearm Beam (1 pc)
    mesh.add_box(15, 25, T/2, 55, 14, T)

    # Part 6: Gripper Base Plate (1 pc)
    mesh.add_box(15, 55, T/2, 34, 40, T)

    # Part 7: Geared Claw Left (1 pc flat)
    c_l = get_geared_claw_polygon(is_left=True)
    t_cl = [(p[0] + 65, p[1] + 25) for p in c_l]
    mesh.extrude_polygon(t_cl, 0, T)

    # Part 8: Geared Claw Right (1 pc flat)
    c_r = get_geared_claw_polygon(is_left=False)
    t_cr = [(p[0] + 65, p[1] + 55) for p in c_r]
    mesh.extrude_polygon(t_cr, 0, T)

    return mesh


# =========================================================================
# 4. BUILD 2D LASER CUT VECTOR FILE (.SVG)
# =========================================================================
def generate_clean_laser_svg(out_path):
    # Generates exact 2D contours for laser cutting on acrylic 3mm sheet (220 x 160 mm)
    claw_l = get_geared_claw_polygon(is_left=True)
    claw_r = get_geared_claw_polygon(is_left=False)

    def poly_to_svg(pts, ox, oy):
        d = f"M {pts[0][0]+ox:.2f} {pts[0][1]+oy:.2f} "
        for p in pts[1:]:
            d += f"L {p[0]+ox:.2f} {p[1]+oy:.2f} "
        d += "Z"
        return d

    path_claw_l = poly_to_svg(claw_l, 160, 95)
    path_claw_r = poly_to_svg(claw_r, 160, 135)

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 160" width="220mm" height="160mm" style="background:#0F172A; font-family:'Segoe UI',Roboto,Helvetica,sans-serif;">
  <defs>
    <style>
      .cut {{ fill: none; stroke: #EF4444; stroke-width: 0.25; }}
      .slot {{ fill: none; stroke: #EF4444; stroke-width: 0.25; }}
      .hole {{ fill: none; stroke: #EF4444; stroke-width: 0.25; }}
      .engrave {{ fill: #38BDF8; font-size: 3.0px; font-weight: bold; }}
      .subtext {{ fill: #94A3B8; font-size: 2.2px; }}
      .sheet {{ fill: none; stroke: #334155; stroke-width: 0.5; stroke-dasharray: 2 1; }}
    </style>
  </defs>

  <rect x="5" y="5" width="210" height="150" rx="3" class="sheet"/>
  
  <text x="10" y="14" fill="#F8FAFC" font-size="4" font-weight="bold">POLA LASER CUT AKRILIK 3mm — MINI ROBOTIC ARM 4-DOF &amp; GEARED GRIPPER</text>
  <text x="10" y="19" fill="#94A3B8" font-size="2.4">Desain 100% Lempengan Datar (Flat Plates) | Roda Gigi Saling Mengunci | Skala 1:1 mm</text>

  <!-- 1. BASE PLATE (60mm disc dengan lubang servo SG90 di tengah) -->
  <g id="base">
    <circle cx="40" cy="50" r="28" class="cut"/>
    <!-- 3 Kaki Baut M3 -->
    <circle cx="71" cy="50" r="4.5" class="cut"/><circle cx="71" cy="50" r="1.6" class="hole"/>
    <circle cx="24.5" cy="76.8" r="4.5" class="cut"/><circle cx="24.5" cy="76.8" r="1.6" class="hole"/>
    <circle cx="24.5" cy="23.2" r="4.5" class="cut"/><circle cx="24.5" cy="23.2" r="1.6" class="hole"/>
    <!-- Slot Servo Base -->
    <rect x="28.5" y="43.75" width="23" height="12.5" class="slot"/>
    <circle cx="25" cy="50" r="1.1" class="hole"/><circle cx="55" cy="50" r="1.1" class="hole"/>
    <text x="40" y="38" class="engrave" text-anchor="middle">1. BASE (Ø60mm)</text>
  </g>

  <!-- 2. TURNTABLE DISC (Ø54mm) -->
  <g id="turntable">
    <circle cx="105" cy="50" r="26" class="cut"/>
    <circle cx="105" cy="50" r="1.2" class="hole"/>
    <!-- Slot penahan garpu bahu -->
    <rect x="94" y="42" width="3.2" height="16" class="slot"/>
    <rect x="113" y="42" width="3.2" height="16" class="slot"/>
    <text x="105" y="35" class="engrave" text-anchor="middle">2. TURNTABLE</text>
  </g>

  <!-- 3. SHOULDER BRACKETS (2 PCS) -->
  <g id="shoulders">
    <rect x="145" y="30" width="18" height="30" rx="3" class="cut"/>
    <rect x="147.5" y="38.75" width="13" height="12.5" class="slot"/>
    <circle cx="154" cy="54" r="1.6" class="hole"/>
    <text x="154" y="27" class="engrave" text-anchor="middle">3. BAHU (2x)</text>

    <rect x="170" y="30" width="18" height="30" rx="3" class="cut"/>
    <circle cx="179" cy="45" r="1.6" class="hole"/>
  </g>

  <!-- 4. LOWER ARM BEAMS (2 PCS - 60mm) -->
  <g id="lower-arm">
    <rect x="12" y="90" width="60" height="16" rx="5" class="cut"/>
    <circle cx="20" cy="98" r="1.6" class="hole"/>
    <circle cx="64" cy="98" r="1.6" class="hole"/>
    <text x="42" y="99" class="engrave" text-anchor="middle">4. LENGAN BAWAH (2x)</text>

    <rect x="12" y="112" width="60" height="16" rx="5" class="cut"/>
    <circle cx="20" cy="120" r="1.6" class="hole"/>
    <circle cx="64" cy="120" r="1.6" class="hole"/>
  </g>

  <!-- 5. FOREARM BEAM (1 PC - 55mm) -->
  <g id="forearm">
    <rect x="80" y="90" width="55" height="14" rx="4" class="cut"/>
    <circle cx="87" cy="97" r="1.6" class="hole"/>
    <circle cx="128" cy="97" r="1.6" class="hole"/>
    <text x="107" y="98" class="engrave" text-anchor="middle">5. LENGAN ATAS</text>
  </g>

  <!-- 6. GRIPPER BASE PLATE -->
  <g id="gripper-base">
    <rect x="80" y="110" width="34" height="40" rx="4" class="cut"/>
    <rect x="85.5" y="118.75" width="23" height="12.5" class="slot"/>
    <circle cx="82.5" cy="125" r="1.1" class="hole"/>
    <circle cx="111.5" cy="125" r="1.1" class="hole"/>
    <!-- 2 Lubang Poros Gear Capit M3 (jarak 18mm) -->
    <circle cx="106" cy="141" r="1.6" class="hole"/>
    <circle cx="106" cy="123" r="1.6" class="hole"/>
    <text x="97" y="115" class="engrave" text-anchor="middle">6. GRIPPER BASE</text>
  </g>

  <!-- 7. CAPIT BERGIGI SPUR (GEARED CLAWS - 100% FLAT AKRILIK 3MM) -->
  <g id="geared-claws">
    <!-- Capit Kiri dengan Gear -->
    <path d="{path_claw_l}" class="cut"/>
    <circle cx="160" cy="95" r="1.6" class="hole"/>
    <!-- Horn mount holes -->
    <circle cx="165" cy="95" r="0.9" class="hole"/><circle cx="155" cy="95" r="0.9" class="hole"/>
    <text x="180" y="87" class="engrave" text-anchor="middle">7A. CAPIT KIRI (GEAR)</text>

    <!-- Capit Kanan dengan Gear -->
    <path d="{path_claw_r}" class="cut"/>
    <circle cx="160" cy="135" r="1.6" class="hole"/>
    <text x="180" y="152" class="engrave" text-anchor="middle">7B. CAPIT KANAN (GEAR)</text>
  </g>

  <!-- Keterangan Laser -->
  <text x="12" y="142" fill="#38BDF8" font-size="2.6" font-weight="bold">SEMUA KOMPONEN 100% FLAT AKRILIK TEBAL 3.0 MM</text>
  <text x="12" y="148" fill="#94A3B8" font-size="2.1">Roda gigi capit dipotong langsung oleh laser akrilik. Rapi, presisi, nol tabrakan di Tinkercad.</text>
</svg>
"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Exported Clean Laser Cut SVG: {out_path}")


# =========================================================================
# MAIN EXECUTION
# =========================================================================
def main():
    target_dir = os.path.abspath("desain_arm_akrilik_rapi")
    os.makedirs(target_dir, exist_ok=True)
    
    repo_target = os.path.abspath("TugasBesarIOT_SiloMonitoringSystem/desain_arm_akrilik_rapi")
    os.makedirs(repo_target, exist_ok=True)

    print("Building Clean 100% Flat Acrylic Arm (Laser Cut Ready & Tinkercad)...")

    # 1. Assembled 3D Clean Arm (All Flat Slabs)
    arm = build_clean_acrylic_arm_assembled()
    arm.write_binary_stl(os.path.join(target_dir, "clean_acrylic_arm_assembled.stl"), "Clean Acrylic Arm")

    # 2. Flat Layout 3D (All Flat Plates lying on Workplane)
    flat_plates = build_clean_acrylic_flat_sheet()
    flat_plates.write_binary_stl(os.path.join(target_dir, "clean_acrylic_flat_plates.stl"), "Flat Acrylic Plates")

    # 3. 2D Laser Cut Vector SVG
    svg_file = os.path.join(target_dir, "pola_laser_cut_akrilik_3mm_rapi.svg")
    generate_clean_laser_svg(svg_file)

    # 4. Render Preview
    print("Rendering 3D preview...")
    fig = plt.figure(figsize=(13, 6.5), facecolor='#0F172A')

    # View 1: Assembled Arm
    ax1 = fig.add_subplot(121, projection='3d', facecolor='#0F172A')
    step = max(1, len(arm.triangles) // 2500)
    t1 = [[t[1], t[2], t[3]] for i, t in enumerate(arm.triangles) if i % step == 0]
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    m1 = Poly3DCollection(t1, facecolors='#38BDF8', edgecolors='#0284C7', linewidths=0.3, alpha=0.9)
    ax1.add_collection3d(m1)
    ax1.set_xlim(-40, 140)
    ax1.set_ylim(-50, 50)
    ax1.set_zlim(0, 110)
    ax1.view_init(elev=22, azim=-55)
    ax1.set_title('MODEL RAPI 100% FLAT AKRILIK 3mm (ASSEMBLED)\n(Semua Part Lempengan Datar, Capit Gigi Presisi)', color='#F8FAFC', fontsize=10, weight='bold')
    ax1.tick_params(colors='#64748B')

    # View 2: Flat Laser Cut Sheet (2D/3D Workplane View)
    ax2 = fig.add_subplot(122, projection='3d', facecolor='#0F172A')
    t2 = [[t[1], t[2], t[3]] for t in flat_plates.triangles]
    m2 = Poly3DCollection(t2, facecolors='#34D399', edgecolors='#059669', linewidths=0.3, alpha=0.95)
    ax2.add_collection3d(m2)
    ax2.set_xlim(-90, 100)
    ax2.set_ylim(-80, 80)
    ax2.set_zlim(-2, 15)
    ax2.view_init(elev=65, azim=-90) # Top-down flat sheet view
    ax2.set_title('TAMPILAN LEMPENGAN AKRILIK FLAT SEBELUM DIRAKIT\n(Tebal 3.0mm, Siap Laser Cutting & Impor Tinkercad)', color='#F8FAFC', fontsize=10, weight='bold')
    ax2.tick_params(colors='#64748B')

    plt.tight_layout()
    preview_path = os.path.join(target_dir, "preview_clean_acrylic_arm.png")
    plt.savefig(preview_path, dpi=200, facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved preview: {preview_path}")

    # Copy to repo folder
    import shutil
    for f in os.listdir(target_dir):
        src = os.path.join(target_dir, f)
        dst = os.path.join(repo_target, f)
        if os.path.isfile(src):
            shutil.copy2(src, dst)

    print(f"\nAll files successfully generated in:\n  - {target_dir}\n  - {repo_target}")

if __name__ == "__main__":
    main()
