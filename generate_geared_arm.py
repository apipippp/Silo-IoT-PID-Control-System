import os
import math
import struct
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# =========================================================================
# STL MESH BUILDER
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

    def add_cylinder_orient(self, p_start, p_end, radius, segments=16):
        p1 = np.array(p_start, dtype=float)
        p2 = np.array(p_end, dtype=float)
        v = p2 - p1
        length = np.linalg.norm(v)
        if length < 1e-6:
            return
        z_dir = v / length
        if abs(z_dir[0]) < 0.8:
            perp = np.cross(z_dir, [1, 0, 0])
        else:
            perp = np.cross(z_dir, [0, 1, 0])
        x_dir = perp / np.linalg.norm(perp)
        y_dir = np.cross(z_dir, x_dir)

        angles = [2.0 * math.pi * i / segments for i in range(segments)]
        bot_pts = [tuple(p1 + radius * math.cos(a) * x_dir + radius * math.sin(a) * y_dir) for a in angles]
        top_pts = [tuple(p2 + radius * math.cos(a) * x_dir + radius * math.sin(a) * y_dir) for a in angles]

        for i in range(segments):
            ni = (i + 1) % segments
            self.add_quad(bot_pts[i], bot_pts[ni], top_pts[ni], top_pts[i])

        cp1, cp2 = tuple(p1), tuple(p2)
        for i in range(segments):
            ni = (i + 1) % segments
            self.add_triangle(cp1, bot_pts[ni], bot_pts[i])
            self.add_triangle(cp2, top_pts[i], top_pts[ni])

    def add_spur_gear_sector(self, cx, cy, z_bot, z_top, r_pitch, num_teeth, tooth_depth, angle_start_deg, angle_end_deg):
        # Generates realistic spur gear teeth along an arc
        a_start = math.radians(angle_start_deg)
        a_end = math.radians(angle_end_deg)
        total_angle = a_end - a_start
        steps = num_teeth * 4
        
        pts_2d = []
        for i in range(steps + 1):
            t = a_start + total_angle * (i / steps)
            # Tooth profile modulation (square/trapezoid wave on pitch circle)
            phase = (i / steps) * num_teeth * 2.0 * math.pi
            r = r_pitch + (tooth_depth / 2.0) * math.sin(phase)
            pts_2d.append((cx + r * math.cos(t), cy + r * math.sin(t)))

        # Close inner base arc
        for i in range(steps, -1, -1):
            t = a_start + total_angle * (i / steps)
            r = r_pitch - tooth_depth * 1.2
            pts_2d.append((cx + r * math.cos(t), cy + r * math.sin(t)))

        # Extrude 2D polygon into 3D prism
        n = len(pts_2d)
        for i in range(n):
            ni = (i + 1) % n
            p1 = (pts_2d[i][0], pts_2d[i][1], z_bot)
            p2 = (pts_2d[ni][0], pts_2d[ni][1], z_bot)
            p3 = (pts_2d[ni][0], pts_2d[ni][1], z_top)
            p4 = (pts_2d[i][0], pts_2d[i][1], z_top)
            self.add_quad(p1, p2, p3, p4)

        # Caps
        c_b = (cx, cy, z_bot)
        c_t = (cx, cy, z_top)
        for i in range(n):
            ni = (i + 1) % n
            self.add_triangle(c_b, (pts_2d[ni][0], pts_2d[ni][1], z_bot), (pts_2d[i][0], pts_2d[i][1], z_bot))
            self.add_triangle(c_t, (pts_2d[i][0], pts_2d[i][1], z_top), (pts_2d[ni][0], pts_2d[ni][1], z_top))

    def write_binary_stl(self, filepath, name="Model"):
        header = f"Tinkercad Geared Robotic Arm: {name}".encode('ascii')[:80]
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

    def write_obj(self, filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("# Tinkercad Geared Robotic Arm Wavefront OBJ\n")
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
# 1. BUILD COMPLETE ROBOTIC ARM WITH 4 SERVOS & INTERLOCKING GEARED GRIPPER
# =========================================================================
def build_geared_arm_system():
    mesh = STLMesh()
    T = 3.0  # 3mm acrylic thickness

    # Base position beside the conveyor
    bx, by, bz = -55.0, 0.0, 0.0

    # =========================================================
    # DOF 1: ROTASI BASE (Yaw Rotation Horizontal)
    # =========================================================
    # Base Plate Akrilik (65 x 65 mm, tebal 3 mm)
    mesh.add_box(bx, by, 1.5, 65, 65, T)
    # Bracket jepit ke rel conveyor
    mesh.add_box(bx + 22, by, 1.5, 22, 28, T)
    # Baut M3 pengikat ke conveyor
    mesh.add_cylinder(bx + 28, by - 8, 0, 5, 1.8, 1.8, segments=12)
    mesh.add_cylinder(bx + 28, by + 8, 0, 5, 1.8, 1.8, segments=12)

    # SERVO 1: Base Rotation SG90 (berdiri tegak di tengah base)
    mesh.add_box(bx, by, 14, 22.8, 12.2, 22.5)
    mesh.add_cylinder(bx, by, 25, 29, 6.0, 6.0, segments=16) # Poros putar

    # Turntable Piringan Putar Akrilik (Diameter 48 mm, Z: 29..32 mm)
    mesh.add_cylinder(bx, by, 29, 32, 24.0, 24.0, segments=28)

    # =========================================================
    # DOF 2: BAHU / SHOULDER (Pitch Vertikal Lengan Bawah)
    # =========================================================
    # Plat tegak penahan servo bahu (menempel kokoh di atas turntable)
    mesh.add_box(bx - 10, by, 48, T, 30, 32)

    # SERVO 2: Shoulder SG90 (Posisi horizontal di Z = 48 mm)
    mesh.add_box(bx + 3, by, 48, 22.8, 12.2, 22.5)
    p_shoulder_pivot = (bx + 8, by + 6.5, 48)

    # LENGAN BAWAH (Bicep Link): Akrilik tebal 3mm, panjang 60mm
    # Mengangkat dari bahu (Z=48) mengarah naik-maju ke siku (Z=85)
    p_elbow_pivot = (bx + 30, by + 6.5, 85)
    mesh.add_cylinder_orient(p_shoulder_pivot, p_elbow_pivot, 6.0, segments=16)

    # =========================================================
    # DOF 3: SIKU / ELBOW (Pitch Vertikal Lengan Atas)
    # =========================================================
    # SERVO 3: Elbow SG90 (Terpasang di persendian siku)
    mesh.add_box(bx + 30, by, 85, 22.8, 12.2, 22.5)

    # LENGAN ATAS (Forearm Link): Akrilik tebal 3mm, panjang 55mm
    # Menghubungkan siku ke dudukan gripper di atas conveyor
    p_wrist = (0.0, 0.0, 52.0)
    mesh.add_cylinder_orient((bx + 30, by - 6.5, 85), p_wrist, 5.0, segments=16)

    # =========================================================
    # DOF 4: END EFFECTOR GEARED GRIPPER (1 SERVO DENGAN SATU PAKET GEAR)
    # =========================================================
    # Plat Dasar Gripper (Gripper Base Plate) di pergelangan tangan (Z = 50..53 mm)
    # Lebar 44 mm, Panjang 34 mm
    mesh.add_box(0, 0, 51.5, 36, 46, T)

    # SERVO 4: Gripper Servo SG90 (terpasang tidur rata di plat dasar)
    mesh.add_box(-6, 0, 60, 22.8, 12.2, 16)
    # Poros output gear horn servo di (X = 0, Y = -10, Z = 68)
    p_servo_horn = (0, -10, 68)
    mesh.add_cylinder(0, -10, 68, 71, 5.0, 5.0, segments=16)

    # DUA POROS GEAR PIVOT BERJARAK 20 mm:
    # Poros 1 (Digerakkan langsung oleh horn servo): (0, -10, Z)
    # Poros 2 (Pivot capit kedua yang bertaut gigi): (0, +10, Z)
    p_pivot1 = (0, -10)
    p_pivot2 = (0, +10)

    # Baut poros pivot M3 akrilik
    mesh.add_cylinder(p_pivot1[0], p_pivot1[1], 46, 56, 1.6, 1.6, segments=12)
    mesh.add_cylinder(p_pivot2[0], p_pivot2[1], 46, 56, 1.6, 1.6, segments=12)

    # PAKET RODA GIGI (SPUR GEAR PAIR):
    # R_pitch = 10.0 mm. Jarak pusat = 20.0 mm (Saling bersinggungan di Y = 0!)
    # Gear 1 (Kiri): Sektor gigi menghadap ke arah Y=0 (+X)
    # Gear 2 (Kanan): Sektor gigi bersinggungan sempurna dengan Gear 1!
    tooth_depth = 2.4
    mesh.add_spur_gear_sector(0, -10, 48, 51, r_pitch=10.0, num_teeth=5, tooth_depth=tooth_depth, angle_start_deg=40, angle_end_deg=130)
    mesh.add_spur_gear_sector(0, 10, 48, 51, r_pitch=10.0, num_teeth=5, tooth_depth=tooth_depth, angle_start_deg=230, angle_end_deg=320)

    # DUA JARI CAPIT SIMETRIS (PINCER CLAWS):
    # Capit Kiri (Left Jaw): Menyatu dengan Gear 1
    # Dari poros (0, -10) melengkung ke depan dan mengarah ke dalam
    claw_pts_l = [
        (0, -10, 49.5),
        (18, -14, 49.5),
        (32, -10, 49.5),
        (38, -6, 49.5)  # Ujung penjepit
    ]
    mesh.add_cylinder_orient(claw_pts_l[0], claw_pts_l[1], 3.5, segments=12)
    mesh.add_cylinder_orient(claw_pts_l[1], claw_pts_l[2], 3.0, segments=12)
    mesh.add_cylinder_orient(claw_pts_l[2], claw_pts_l[3], 2.8, segments=12)
    # Bantalan penjepit jari kiri (Finger Grip Pad)
    mesh.add_box(36, -7.5, 49.5, 10, 3.5, 8)

    # Capit Kanan (Right Jaw): Menyatu dengan Gear 2 (Simetris sempurna!)
    claw_pts_r = [
        (0, 10, 49.5),
        (18, 14, 49.5),
        (32, 10, 49.5),
        (38, 6, 49.5)   # Ujung penjepit
    ]
    mesh.add_cylinder_orient(claw_pts_r[0], claw_pts_r[1], 3.5, segments=12)
    mesh.add_cylinder_orient(claw_pts_r[1], claw_pts_r[2], 3.0, segments=12)
    mesh.add_cylinder_orient(claw_pts_r[2], claw_pts_r[3], 2.8, segments=12)
    # Bantalan penjepit jari kanan (Finger Grip Pad)
    mesh.add_box(36, 7.5, 49.5, 10, 3.5, 8)

    # Link pendorong antara horn servo ke Capit Kiri
    mesh.add_cylinder_orient((0, -10, 69), (12, -12, 51), 1.8, segments=12)

    # BENDA KERJA: RED BOX (Sedang dijepit mantap di antara kedua capit di X=36, Y=0, Z=49.5)
    # Ukuran 18x18x18 mm (Pas dengan balok merah conveyor Tinkercad Manuel!)
    mesh.add_box(36, 0, 49.5, 18, 18, 18)

    return mesh


# =========================================================================
# 2. BUILD STANDALONE GEARED GRIPPER MECHANISM FOR CLOSEUP INSPECTION
# =========================================================================
def build_geared_gripper_standalone():
    mesh = STLMesh()
    T = 3.0

    # Base Plate
    mesh.add_box(0, 0, 1.5, 40, 50, T)
    # Servo Cutout
    mesh.add_box(-5, 0, 10, 22.8, 12.2, 18)
    mesh.add_cylinder(0, -10, 18, 22, 5.0, 5.0, segments=16)

    # Spur Gears
    mesh.add_spur_gear_sector(0, -10, 0, T, r_pitch=10.0, num_teeth=5, tooth_depth=2.4, angle_start_deg=40, angle_end_deg=130)
    mesh.add_spur_gear_sector(0, 10, 0, T, r_pitch=10.0, num_teeth=5, tooth_depth=2.4, angle_start_deg=230, angle_end_deg=320)

    # Claws
    mesh.add_cylinder_orient((0, -10, 1.5), (20, -15, 1.5), 3.5, segments=12)
    mesh.add_cylinder_orient((20, -15, 1.5), (38, -6, 1.5), 3.0, segments=12)
    mesh.add_box(36, -7.5, 1.5, 10, 3.5, 8)

    mesh.add_cylinder_orient((0, 10, 1.5), (20, 14, 1.5), 3.5, segments=12)
    mesh.add_cylinder_orient((20, 14, 1.5), (38, 6, 1.5), 3.0, segments=12)
    mesh.add_box(36, 7.5, 1.5, 10, 3.5, 8)

    # Pivot Pins
    mesh.add_cylinder(0, -10, 0, 8, 1.6, 1.6, segments=12)
    mesh.add_cylinder(0, 10, 0, 8, 1.6, 1.6, segments=12)

    return mesh


# =========================================================================
# 3. BUILD FULL CONVEYOR SCENE WITH THE GEARED ARM
# =========================================================================
def build_conveyor_scene_with_geared_arm():
    mesh = STLMesh()

    # Add the Geared Arm
    arm = build_geared_arm_system()
    mesh.triangles.extend(arm.triangles)

    # Add the Conveyor System (Sesuai Tinkercad Manuel)
    # Conveyor Bed: X = 0 to 140, Y = -25 to +25, Z = 22 mm
    mesh.add_box(70, 0, 21, 140, 48, 4)
    mesh.add_box(70, -25, 14, 140, 3, 18)
    mesh.add_box(70, 25, 14, 140, 3, 18)
    mesh.add_cylinder(140, 0, 8, 8, 10, 10, segments=20)
    mesh.add_cylinder(0, 0, 8, 8, 10, 10, segments=20)
    # Yellow TT Motor
    mesh.add_box(142, 33, 12, 22, 16, 18)
    mesh.add_cylinder(142, 25, 12, 12, 4, 4, segments=12)

    # Silo Chamber with sensors at conveyor end
    mesh.add_box(165, 0, 2, 50, 70, 4)
    mesh.add_box(190, 0, 50, 4, 70, 96)
    mesh.add_box(165, -35, 50, 50, 4, 96)
    mesh.add_box(165, 35, 50, 50, 4, 96)
    # Ultrasonic HC-SR04
    mesh.add_box(186, -10, 60, 4, 38, 18)
    mesh.add_cylinder(184, -20, 60, 60, 6, 6, segments=16)
    mesh.add_cylinder(184, 0, 60, 60, 6, 6, segments=16)

    # Cyan Control Box
    mesh.add_box(130, 80, 40, 45, 60, 80)
    mesh.add_box(128, 80, 55, 3, 35, 14)

    return mesh


# =========================================================================
# 4. BUILD 2D LASER CUT VECTOR WITH REAL INVOLUTE/SPUR GEAR TEETH
# =========================================================================
def generate_geared_laser_svg(out_path):
    svg = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 180" width="240mm" height="180mm" style="background:#0F172A; font-family:'Segoe UI',Roboto,Helvetica,sans-serif;">
  <defs>
    <style>
      .cut { fill: none; stroke: #EF4444; stroke-width: 0.25; }
      .slot { fill: none; stroke: #EF4444; stroke-width: 0.25; }
      .hole { fill: none; stroke: #EF4444; stroke-width: 0.25; }
      .engrave { fill: #38BDF8; font-size: 3.2px; font-weight: bold; }
      .subtext { fill: #94A3B8; font-size: 2.2px; }
      .sheet { fill: none; stroke: #334155; stroke-width: 0.5; stroke-dasharray: 2 1; }
    </style>
  </defs>

  <rect x="5" y="5" width="230" height="170" rx="3" class="sheet"/>
  
  <text x="12" y="15" fill="#F8FAFC" font-size="4.5" font-weight="bold">POLA LASER CUT 2D — ROBOTIC ARM 4-DOF DENGAN GEARED GRIPPER</text>
  <text x="12" y="21" fill="#94A3B8" font-size="2.6">Sistem Roda Gigi Simetris (Spur Gear) + Rotasi Base + Naik/Turun Bahu &amp; Siku | Akrilik 3mm</text>

  <!-- ========================================================= -->
  <!-- 1. BASE PLATE & BRACKET REL CONVEYOR -->
  <!-- ========================================================= -->
  <g id="base-plate">
    <path d="M 15 30 L 75 30 L 75 45 L 90 45 L 90 75 L 75 75 L 75 90 L 15 90 Z" class="cut"/>
    <rect x="33.5" y="53.75" width="23" height="12.5" class="slot"/>
    <circle cx="29.5" cy="60" r="1.1" class="hole"/>
    <circle cx="60.5" cy="60" r="1.1" class="hole"/>
    <circle cx="82" cy="52" r="1.6" class="hole"/>
    <circle cx="82" cy="68" r="1.6" class="hole"/>
    <text x="45" y="40" class="engrave" text-anchor="middle">1. BASE PLATE</text>
    <text x="45" y="45" class="subtext" text-anchor="middle">(Rotasi Horizontal)</text>
  </g>

  <!-- ========================================================= -->
  <!-- 2. TURNTABLE DISC -->
  <!-- ========================================================= -->
  <g id="turntable">
    <circle cx="120" cy="58" r="24" class="cut"/>
    <circle cx="120" cy="58" r="1.2" class="hole"/>
    <circle cx="120" cy="50" r="0.9" class="hole"/>
    <circle cx="120" cy="66" r="0.9" class="hole"/>
    <rect x="106" y="50" width="3.2" height="16" class="slot"/>
    <text x="120" y="40" class="engrave" text-anchor="middle">2. TURNTABLE</text>
  </g>

  <!-- ========================================================= -->
  <!-- 3. SHOULDER VERTICAL BRACKET -->
  <!-- ========================================================= -->
  <g id="shoulder">
    <path d="M 155 30 L 185 30 L 185 60 L 177 60 L 177 64 L 163 64 L 163 60 L 155 60 Z" class="cut"/>
    <rect x="158.5" y="38" width="23" height="12.5" class="slot"/>
    <circle cx="155.5" cy="44.25" r="1.1" class="hole"/>
    <circle cx="184.5" cy="44.25" r="1.1" class="hole"/>
    <text x="170" y="35" class="engrave" text-anchor="middle">3. BAHU (Naik/Turun)</text>
  </g>

  <!-- ========================================================= -->
  <!-- 4. LENGAN BAWAH (BICEP LINK - 60mm) -->
  <!-- ========================================================= -->
  <g id="bicep">
    <rect x="15" y="100" width="60" height="16" rx="5" class="cut"/>
    <circle cx="23" cy="108" r="1.2" class="hole"/>
    <circle cx="19" cy="108" r="0.9" class="hole"/>
    <circle cx="27" cy="108" r="0.9" class="hole"/>
    <circle cx="67" cy="108" r="1.6" class="hole"/>
    <text x="45" y="109" class="engrave" text-anchor="middle">4. BICEP (60mm)</text>
  </g>

  <!-- ========================================================= -->
  <!-- 5. LENGAN ATAS (FOREARM LINK - 55mm) -->
  <!-- ========================================================= -->
  <g id="forearm">
    <rect x="85" y="100" width="55" height="14" rx="5" class="cut"/>
    <circle cx="92" cy="107" r="1.2" class="hole"/>
    <circle cx="88" cy="107" r="0.9" class="hole"/>
    <circle cx="96" cy="107" r="0.9" class="hole"/>
    <circle cx="132" cy="107" r="1.6" class="hole"/>
    <text x="112" y="108" class="engrave" text-anchor="middle">5. FOREARM (55mm)</text>
  </g>

  <!-- ========================================================= -->
  <!-- 6. GRIPPER BASE MOUNTING PLATE -->
  <!-- ========================================================= -->
  <g id="gripper-plate">
    <rect x="150" y="75" width="44" height="36" rx="4" class="cut"/>
    <rect x="153.5" y="86.75" width="23" height="12.5" class="slot"/>
    <circle cx="150.5" cy="93" r="1.1" class="hole"/>
    <circle cx="179.5" cy="93" r="1.1" class="hole"/>
    <!-- Dua lubang pivot poros gear M3 (jarak pitch 20 mm) -->
    <circle cx="187" cy="83" r="1.6" class="hole"/>
    <circle cx="187" cy="103" r="1.6" class="hole"/>
    <text x="172" y="82" class="engrave" text-anchor="middle">6. GRIPPER BASE</text>
  </g>

  <!-- ========================================================= -->
  <!-- 7A. CAPIT KIRI DENGAN SEKTOR GEAR SPUR INTEGRATED -->
  <!-- ========================================================= -->
  <g id="jaw-left">
    <!-- Gear teeth sector meshing with Jaw Right -->
    <path d="M 200 65 
             L 208 65 
             L 210 68 L 213 68 L 214 71 L 217 71 L 218 74 L 221 74 L 222 77 L 225 77 
             L 226 80 L 223 83 L 220 83 
             L 235 90 
             L 238 98 
             L 232 98 
             L 222 90 
             L 205 85 
             C 198 85, 195 75, 200 65 Z" class="cut"/>
    <!-- Pivot hole M3 -->
    <circle cx="206" cy="74" r="1.6" class="hole"/>
    <!-- Horn actuator drive hole -->
    <circle cx="212" cy="80" r="1.1" class="hole"/>
    <text x="215" y="62" class="engrave" text-anchor="middle">7A. JAW L (GEAR)</text>
  </g>

  <!-- ========================================================= -->
  <!-- 7B. CAPIT KANAN DENGAN SEKTOR GEAR SPUR (SIMETRIS) -->
  <!-- ========================================================= -->
  <g id="jaw-right">
    <!-- Matching gear teeth sector -->
    <path d="M 200 120 
             L 208 120 
             L 210 117 L 213 117 L 214 114 L 217 114 L 218 111 L 221 111 L 222 108 L 225 108 
             L 226 105 L 223 102 L 220 102 
             L 235 95 
             L 238 87 
             L 232 87 
             L 222 95 
             L 205 100 
             C 198 100, 195 110, 200 120 Z" class="cut"/>
    <!-- Pivot hole M3 -->
    <circle cx="206" cy="111" r="1.6" class="hole"/>
    <text x="215" y="128" class="engrave" text-anchor="middle">7B. JAW R (GEAR)</text>
  </g>

  <!-- BANTALAN JARI PENJEPIT KUBUS (FINGER GRIP PADS) -->
  <rect x="15" y="130" width="18" height="8" rx="2" class="cut"/>
  <rect x="38" y="130" width="18" height="8" rx="2" class="cut"/>
  <text x="35" y="145" class="subtext" text-anchor="middle">GRIP PADS</text>

  <!-- MEKANISME KERJA GEAR & SERVO -->
  <rect x="75" y="125" width="155" height="38" rx="2" fill="#1E293B" stroke="#334155" stroke-width="0.5"/>
  <text x="82" y="134" fill="#38BDF8" font-size="3.0" font-weight="bold">MEKANISME KERJA GRIPPER GEAR (1 SERVO):</text>
  <text x="82" y="141" fill="#F8FAFC" font-size="2.4">1. Servo SG90 memutar poros Capit Kiri (7A).</text>
  <text x="82" y="147" fill="#F8FAFC" font-size="2.4">2. Gigi spur gear pada Capit Kiri langsung mengunci &amp; memutar gigi Capit Kanan (7B).</text>
  <text x="82" y="153" fill="#F8FAFC" font-size="2.4">3. Hasil: Kedua capit membuka &amp; menutup bersamaan secara simetris menjepit box merah!</text>
  <text x="82" y="159" fill="#10B981" font-size="2.3">4. Sumbu Arm: 1x Base Rotasi, 1x Bahu Naik/Turun, 1x Siku Jangkauan, 1x Gripper Gear.</text>
</svg>
"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Exported Geared Laser SVG: {out_path}")


# =========================================================================
# MAIN EXECUTION
# =========================================================================
def main():
    target_dir = os.path.abspath("desain_arm_geared_gripper")
    os.makedirs(target_dir, exist_ok=True)
    
    repo_target = os.path.abspath("TugasBesarIOT_SiloMonitoringSystem/desain_arm_geared_gripper")
    os.makedirs(repo_target, exist_ok=True)

    print("Building Geared Gripper Robotic Arm...")

    # 1. Arm STL (Solo Assembly with Geared Claws)
    arm = build_geared_arm_system()
    arm.write_binary_stl(os.path.join(target_dir, "geared_robotic_arm_conveyor.stl"), "Geared Robotic Arm")
    arm.write_obj(os.path.join(target_dir, "geared_robotic_arm_conveyor.obj"))

    # 2. Standalone Gripper Assembly STL
    gripper = build_geared_gripper_standalone()
    gripper.write_binary_stl(os.path.join(target_dir, "geared_gripper_standalone.stl"), "Geared Gripper Standalone")
    gripper.write_obj(os.path.join(target_dir, "geared_gripper_standalone.obj"))

    # 3. Full Scene STL (Conveyor + Silo + Red Box + Geared Arm)
    full_scene = build_conveyor_scene_with_geared_arm()
    full_scene.write_binary_stl(os.path.join(target_dir, "scene_conveyor_geared_arm.stl"), "Scene Conveyor Geared Arm")
    full_scene.write_obj(os.path.join(target_dir, "scene_conveyor_geared_arm.obj"))

    # 4. 2D Laser Cut Pattern (SVG)
    svg_file = os.path.join(target_dir, "pola_laser_cut_arm_geared_gripper.svg")
    generate_geared_laser_svg(svg_file)

    # 5. Render 3D Visual Preview (Gripper Close-Up + Full Arm)
    print("Rendering 3D preview...")
    fig = plt.figure(figsize=(12, 6.5), facecolor='#0F172A')

    # Subplot 1: Gripper Mechanism Close-up
    ax1 = fig.add_subplot(121, projection='3d', facecolor='#0F172A')
    t_grip = [[t[1], t[2], t[3]] for t in gripper.triangles]
    m1 = Poly3DCollection(t_grip, facecolors='#38BDF8', edgecolors='#0284C7', linewidths=0.3, alpha=0.9)
    ax1.add_collection3d(m1)
    ax1.set_xlim(-10, 45)
    ax1.set_ylim(-30, 30)
    ax1.set_zlim(-5, 25)
    ax1.view_init(elev=50, azim=-60)
    ax1.set_title('DETAIL 1: MEKANISME GEARED GRIPPER (1 SERVO)\n(Dua Gigi Saling Mengunci Membuka-Tutup Capit)', color='#F8FAFC', fontsize=10, weight='bold')
    ax1.tick_params(colors='#64748B')

    # Subplot 2: Full Scene with Conveyor & Arm
    ax2 = fig.add_subplot(122, projection='3d', facecolor='#0F172A')
    step = max(1, len(full_scene.triangles) // 2500)
    t_full = [[t[1], t[2], t[3]] for i, t in enumerate(full_scene.triangles) if i % step == 0]
    m2 = Poly3DCollection(t_full, facecolors='#38BDF8', edgecolors='#0284C7', linewidths=0.2, alpha=0.85)
    ax2.add_collection3d(m2)
    ax2.set_xlim(-70, 200)
    ax2.set_ylim(-50, 100)
    ax2.set_zlim(0, 110)
    ax2.view_init(elev=25, azim=-55)
    ax2.set_title('DETAIL 2: SISTEM UTUH DENGAN CONVEYOR TINKERCAD\n(Rotasi Base + Naik/Turun Bahu-Siku + Geared Gripper)', color='#F8FAFC', fontsize=10, weight='bold')
    ax2.tick_params(colors='#64748B')

    plt.tight_layout()
    preview_file = os.path.join(target_dir, "preview_geared_arm_system.png")
    plt.savefig(preview_file, dpi=200, facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved: {preview_file}")

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
