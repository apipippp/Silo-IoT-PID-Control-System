import os
import math
import struct
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Output directory
OUT_DIR = r"C:\KULIAHHHHHHHHH\TUGAS KULIAH\SEMESTER 5\IOT + SISTEM KENDALI\desain_arm_stik_eskrim"
os.makedirs(OUT_DIR, exist_ok=True)

# =========================================================================
# STL & OBJ 3D MESH BUILDER
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

    def add_cylinder(self, cx, cy, z_bottom, z_top, radius_bottom, radius_top=None, segments=20):
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

    def add_stick(self, x1, y1, z1, x2, y2, z2, width=10.0, thickness=2.0):
        """Menambahkan sebatang stik es krim dari koordinat p1 ke p2 dengan penampang width x thickness."""
        p1 = np.array([x1, y1, z1], dtype=float)
        p2 = np.array([x2, y2, z2], dtype=float)
        d = p2 - p1
        L = np.linalg.norm(d)
        if L < 1e-6:
            return
        axis = d / L

        # Normal tegak lurus terhadap sumbu batang
        if abs(axis[2]) < 0.9:
            up = np.array([0, 0, 1.0])
        else:
            up = np.array([0, 1.0, 0])
        right = np.cross(axis, up)
        right = right / np.linalg.norm(right)
        up_actual = np.cross(right, axis)
        up_actual = up_actual / np.linalg.norm(up_actual)

        hw = width / 2.0
        ht = thickness / 2.0

        # 8 sudut box batang stik
        c1 = p1 - right * hw - up_actual * ht
        c2 = p1 + right * hw - up_actual * ht
        c3 = p1 + right * hw + up_actual * ht
        c4 = p1 - right * hw + up_actual * ht

        c5 = p2 - right * hw - up_actual * ht
        c6 = p2 + right * hw - up_actual * ht
        c7 = p2 + right * hw + up_actual * ht
        c8 = p2 - right * hw + up_actual * ht

        # 6 muka
        self.add_quad(c1, c4, c3, c2) # end 1
        self.add_quad(c5, c6, c7, c8) # end 2
        self.add_quad(c1, c2, c6, c5) # bottom
        self.add_quad(c3, c4, c8, c7) # top
        self.add_quad(c1, c5, c8, c4) # left
        self.add_quad(c2, c3, c7, c6) # right

    def add_sg90(self, cx, cy, cz, rot_axis="z", angle_deg=0):
        """Menambahkan representasi servo SG90 mini."""
        # Body dasar 22.8 x 12.2 x 22.5 mm
        self.add_box(cx, cy, cz, 22.8, 12.2, 22.5)
        # Telinga baut
        self.add_box(cx, cy, cz + 6.0, 32.0, 12.0, 2.0)
        # Menara gir
        self.add_cylinder(cx + 5.5, cy, cz + 11.25, cz + 16.0, 5.5, 5.5, segments=16)
        # Horn putih
        self.add_cylinder(cx + 5.5, cy, cz + 16.0, cz + 18.0, 3.5, 3.5, segments=12)
        self.add_box(cx + 10.5, cy, cz + 17.0, 12.0, 4.0, 1.8)

    def write_binary_stl(self, filepath, name="Model"):
        header = f"Popsicle Stick Robotic Arm: {name}".encode('ascii')[:80]
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
            f.write("# Popsicle Stick Robotic Arm - Tinkercad & SolidWorks Ready\n")
            vert_map = {}
            vert_list = []
            faces = []

            def get_v_idx(pt):
                key = (round(pt[0], 3), round(pt[1], 3), round(pt[2], 3))
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
                f.write(f"v {v[0]:.3f} {v[1]:.3f} {v[2]:.3f}\n")
            for face in faces:
                f.write(f"f {face[0]} {face[1]} {face[2]}\n")
        print(f"Exported OBJ: {filepath} ({len(faces)} faces, {os.path.getsize(filepath) / 1024:.1f} KB)")


# =========================================================================
# 1. BUILD COMPLETE 3D ASSEMBLY ROBOT ARM STIK ES KRIM
# =========================================================================
def build_assembly_3d():
    mesh = STLMesh()
    W = 10.0  # Lebar stik es krim
    T = 2.0   # Tebal stik tunggal
    T2 = 4.0  # Tebal stik ganda (laminasi 2 lapis)

    # -------------------------------------------------------------
    # 1. BASE RAFT (Tatakan Meja dari 8 Stik Es Krim Sejajar 80 x 114 mm)
    # -------------------------------------------------------------
    for i in range(8):
        y_pos = -35.0 + i * 10.0
        # Di tengah kita beri celah untuk Servo 1 (Base Yaw)
        if -12.0 < y_pos < 12.0:
            # Bagian kiri & kanan servo slot
            mesh.add_box(-35.0, y_pos, 1.0, 44.0, 9.6, T)
            mesh.add_box(35.0, y_pos, 1.0, 44.0, 9.6, T)
        else:
            mesh.add_box(0, y_pos, 1.0, 114.0, 9.6, T)

    # 2 Stik Penguat Melintang di Bawah Base
    mesh.add_box(-45.0, 0, -1.0, 9.6, 80.0, T)
    mesh.add_box(45.0, 0, -1.0, 9.6, 80.0, T)

    # SERVO 1: BASE ROTATION SERVO (di tengah tatakan)
    mesh.add_sg90(0, 0, 12.0)

    # -------------------------------------------------------------
    # 2. TURNTABLE PLATFORM (Piringan Putar di atas Servo Base)
    # Terbuat dari 4 stik es krim silang/persegi (Z = 28..32 mm)
    # -------------------------------------------------------------
    mesh.add_box(0, 0, 30.0, 50.0, 50.0, T2)
    # Poros tumpuan putar
    mesh.add_cylinder(0, 0, 27.0, 30.0, 4.0, 4.0, segments=16)

    # -------------------------------------------------------------
    # 3. UPRIGHT BRACKET (Tiang Penopang Servo Bahu & Pivot)
    # Berdiri di sisi kiri & kanan turntable (Z = 32..65 mm)
    # -------------------------------------------------------------
    # Tiang Kiri (Penyangga Servo 2 - Shoulder)
    mesh.add_box(-16.0, 0, 48.0, T2, 28.0, 34.0)
    # Tiang Kanan (Penyangga Servo 3 - Elbow / Parallel Linkage)
    mesh.add_box(16.0, 0, 48.0, T2, 28.0, 34.0)

    # SERVO 2: SHOULDER SERVO (Bahu Kiri, Z = 52 mm)
    mesh.add_box(-22.0, 0, 52.0, 12.2, 22.8, 22.5)
    # Poros output keluar ke arah kanan (dalam)
    mesh.add_cylinder(-16.0, 5.5, 52.0, 52.0, 5.0, 5.0, segments=12)

    # SERVO 3: ELBOW SERVO (Siku Kanan - Ditempatkan di Base agar enteng!)
    mesh.add_box(22.0, -15.0, 52.0, 12.2, 22.8, 22.5)
    mesh.add_cylinder(16.0, -9.5, 52.0, 52.0, 5.0, 5.0, segments=12)

    # -------------------------------------------------------------
    # 4. LOWER ARM (LENGAN BAHU / BICEP) - Stik Ganda Laminasi 95mm
    # Poros Bawah: (-16, 5.5, 52) -> Poros Siku: (-16, 45, 105)
    # Panjang link Center-to-Center = 80 mm
    # -------------------------------------------------------------
    p_shoulder = np.array([-16.0, 5.5, 52.0])
    p_elbow = np.array([-16.0, 45.0, 105.0])
    mesh.add_stick(p_shoulder[0], p_shoulder[1], p_shoulder[2],
                   p_elbow[0], p_elbow[1], p_elbow[2], width=W, thickness=T2)

    # -------------------------------------------------------------
    # 5. PARALLEL ROD (Batang Jajar Genjang Penggerak Siku)
    # Menghubungkan tuas servo 3 di base ke tuas segitiga siku
    # Panjang persis 80 mm agar paralel dengan Bicep!
    # -------------------------------------------------------------
    p_link_bot = np.array([16.0, -9.5, 52.0])
    p_link_top = np.array([16.0, 30.0, 105.0])
    mesh.add_stick(p_link_bot[0], p_link_bot[1], p_link_bot[2],
                   p_link_top[0], p_link_top[1], p_link_top[2], width=W, thickness=T)

    # Palang segitiga siku penghubung kiri & kanan (Cross bar siku)
    mesh.add_box(0, 45.0, 105.0, 36.0, W, T2)
    mesh.add_cylinder(-16.0, 45.0, 102.0, 108.0, 2.5, 2.5, segments=12)
    mesh.add_cylinder(16.0, 30.0, 102.0, 108.0, 2.5, 2.5, segments=12)

    # -------------------------------------------------------------
    # 6. FOREARM (LENGAN DEPAN) - Stik Ganda Laminasi 95mm
    # Dari Siku (-16, 45, 105) memanjang ke Pergelangan (Wrist): (-16, 115, 85)
    # Center-to-Center = 80 mm
    # -------------------------------------------------------------
    p_wrist = np.array([-16.0, 115.0, 85.0])
    mesh.add_stick(p_elbow[0], p_elbow[1], p_elbow[2],
                   p_wrist[0], p_wrist[1], p_wrist[2], width=W, thickness=T2)

    # -------------------------------------------------------------
    # 7. GRIPPER ASSEMBLY (Dudukan Servo Capit & Cakar Stik Es Krim)
    # Terletak di ujung lengan depan (Z = 85 mm, Y = 115..165 mm)
    # -------------------------------------------------------------
    # Dudukan Servo 4 Gripper (Dibuat dari 3 potong stik es krim kotak)
    mesh.add_box(-16.0, 125.0, 85.0, 30.0, 24.0, T2)

    # SERVO 4: GRIPPER SERVO (SG90 mini posisi flat tidur)
    mesh.add_box(-16.0, 125.0, 93.0, 22.8, 12.2, 16.0)
    # Poros gir horn di Z = 100 mm
    mesh.add_cylinder(-10.5, 125.0, 98.0, 101.5, 4.5, 4.5, segments=12)

    # Cakar Kiri (Fixed / Linkage Claw) dari stik es krim
    mesh.add_box(-26.0, 150.0, 85.0, 6.0, 42.0, T2)
    mesh.add_box(-23.0, 168.0, 85.0, 10.0, 6.0, T2) # Ujung kait capit kiri

    # Cakar Kanan (Moving Claw) digerakkan langsung oleh Horn Servo
    mesh.add_box(-6.0, 150.0, 85.0, 6.0, 42.0, T2)
    mesh.add_box(-9.0, 168.0, 85.0, 10.0, 6.0, T2) # Ujung kait capit kanan

    # Target Object: Balok kubus mini 15x15x15 mm (simulasi benda yang diangkat)
    mesh.add_box(-16.0, 165.0, 85.0, 14.0, 14.0, 14.0)

    return mesh


# =========================================================================
# 2. BUILD 3D FLAT PATTERN (KOMPONEN STIK ES KRIM TERURAI DATAR)
# =========================================================================
def build_flat_parts_3d():
    mesh = STLMesh()
    T = 2.0
    T2 = 4.0
    W = 10.0

    # Layout part stik terurai di bidang datar XY (Z = 0..4 mm)
    # 1. Stik Lengan Utama 1 (Bicep Link 95 mm - Double tebal 4mm)
    mesh.add_box(-40.0, 0, 2.0, W, 95.0, T2)
    # Lubang pivot atas & bawah
    mesh.add_cylinder(-40.0, -40.0, -0.5, 4.5, 1.5, 1.5, segments=12)
    mesh.add_cylinder(-40.0, 40.0, -0.5, 4.5, 1.5, 1.5, segments=12)

    # 2. Stik Lengan Utama 2 (Forearm Link 95 mm - Double tebal 4mm)
    mesh.add_box(-25.0, 0, 2.0, W, 95.0, T2)
    mesh.add_cylinder(-25.0, -40.0, -0.5, 4.5, 1.5, 1.5, segments=12)
    mesh.add_cylinder(-25.0, 40.0, -0.5, 4.5, 1.5, 1.5, segments=12)

    # 3. Batang Paralel (Linkage Rod 95 mm - Tebal 2mm)
    mesh.add_box(-10.0, 0, 1.0, W, 95.0, T)
    mesh.add_cylinder(-10.0, -40.0, -0.5, 2.5, 1.5, 1.5, segments=12)
    mesh.add_cylinder(-10.0, 40.0, -0.5, 2.5, 1.5, 1.5, segments=12)

    # 4. Tiang Penopang Turntable (2 keping 45 mm x 20 mm)
    mesh.add_box(10.0, -25.0, 2.0, 20.0, 45.0, T2)
    mesh.add_box(10.0, 25.0, 2.0, 20.0, 45.0, T2)

    # 5. Cakar Capit Gripper (2 keping stik lancip 50 mm)
    mesh.add_box(30.0, -20.0, 1.0, W, 50.0, T)
    mesh.add_box(30.0, 20.0, 1.0, W, 50.0, T)

    # 6. Plat Turntable (50 x 50 mm)
    mesh.add_box(55.0, 0, 1.0, 50.0, 50.0, T2)
    mesh.add_cylinder(55.0, 0, -0.5, 4.5, 3.0, 3.0, segments=16)

    return mesh


# =========================================================================
# 3. GENERATE 2D BLUEPRINT & CUTTING PATTERN (SVG & DXF)
# =========================================================================
def generate_blueprint_svg(out_path):
    svg = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 620" width="850px" height="620px" style="background:#0F172A; font-family:'Segoe UI',Roboto,Helvetica,sans-serif;">
  <defs>
    <style>
      .title { fill: #38BDF8; font-size: 18px; font-weight: bold; }
      .subtitle { fill: #94A3B8; font-size: 11px; }
      .header-box { fill: #1E293B; stroke: #334155; stroke-width: 1.5; }
      .wood { fill: #FDE68A; stroke: #D97706; stroke-width: 1.5; rx: 5; }
      .wood-laminate { fill: #FCD34D; stroke: #B45309; stroke-width: 2.0; rx: 5; }
      .hole { fill: #0F172A; stroke: #EF4444; stroke-width: 1.5; }
      .center-line { stroke: #EF4444; stroke-width: 0.8; stroke-dasharray: 4 2; }
      .dim-line { stroke: #38BDF8; stroke-width: 1.0; }
      .dim-text { fill: #38BDF8; font-size: 10px; font-weight: bold; text-anchor: middle; }
      .part-name { fill: #F8FAFC; font-size: 12px; font-weight: bold; }
      .part-desc { fill: #94A3B8; font-size: 9.5px; }
      .badge { fill: #0284C7; rx: 3; }
      .badge-text { fill: #FFFFFF; font-size: 9px; font-weight: bold; text-anchor: middle; }
      .note-box { fill: #1E293B; stroke: #0284C7; stroke-width: 1; rx: 4; }
      .note-text { fill: #E2E8F0; font-size: 10px; }
      .warn-text { fill: #FBBF24; font-size: 10px; font-weight: bold; }
    </style>
    <!-- Arrow marker -->
    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#38BDF8"/>
    </marker>
  </defs>

  <!-- TITLE BLOCK -->
  <rect x="20" y="15" width="810" height="60" class="header-box" rx="6"/>
  <text x="35" y="40" class="title">BLUEPRINT RANGKA ROBOT ARM STIK ES KRIM (4/5 SERVO SG90)</text>
  <text x="35" y="58" class="subtitle">Skala Pemotongan &amp; Titik Pengeboran Presisi | Tinkercad &amp; SolidWorks Ready Reference</text>
  <text x="680" y="42" class="badge-text" style="fill:#38BDF8; font-size:12px;">SISTEM KENDALI &amp; IOT</text>
  <text x="680" y="58" class="badge-text" style="fill:#94A3B8; font-size:10px;">SEMESTER 5</text>

  <!-- PART 1: LENGAN BAWAH (BICEP / LOWER ARM) -->
  <g transform="translate(30, 95)">
    <rect x="0" y="0" width="230" height="155" class="header-box" rx="4"/>
    <text x="12" y="22" class="part-name">1. Lengan Bahu (Bicep)</text>
    <rect x="155" y="10" width="65" height="16" class="badge"/>
    <text x="187" y="22" class="badge-text">2 LAPIS STIK</text>

    <!-- Stick representation (Horizontal: 95mm equivalent scale x2.0) -->
    <!-- Length: 95mm * 2.0 = 190px, Width: 10mm * 2.0 = 20px -->
    <rect x="20" y="50" width="190" height="20" class="wood-laminate"/>
    <!-- Lubang Pivot 1 (7.5mm dari tepi -> 15px) -->
    <circle cx="35" cy="60" r="4" class="hole"/>
    <!-- Lubang Pivot 2 (80mm jarak -> 160px) -->
    <circle cx="195" cy="60" r="4" class="hole"/>
    
    <!-- Garis Dimensi Jarak Lubang (80 mm) -->
    <line x1="35" y1="85" x2="195" y2="85" class="dim-line" marker-start="url(#arrow)" marker-end="url(#arrow)"/>
    <text x="115" y="98" class="dim-text">80.0 mm (Center-to-Center)</text>

    <!-- Garis Dimensi Panjang Total (95 mm) -->
    <line x1="20" y1="112" x2="210" y2="112" class="dim-line" marker-start="url(#arrow)" marker-end="url(#arrow)"/>
    <text x="115" y="125" class="dim-text">Panjang Total Potong: 95.0 mm</text>

    <text x="12" y="145" class="part-desc">• Lem rangkap 2 stik agar kaku (tebal 4mm). Bor lubang Ø 2.5mm.</text>
  </g>

  <!-- PART 2: LENGAN DEPAN (FOREARM) -->
  <g transform="translate(280, 95)">
    <rect x="0" y="0" width="230" height="155" class="header-box" rx="4"/>
    <text x="12" y="22" class="part-name">2. Lengan Depan (Forearm)</text>
    <rect x="155" y="10" width="65" height="16" class="badge"/>
    <text x="187" y="22" class="badge-text">2 LAPIS STIK</text>

    <rect x="20" y="50" width="190" height="20" class="wood-laminate"/>
    <circle cx="35" cy="60" r="4" class="hole"/>
    <circle cx="195" cy="60" r="4" class="hole"/>

    <line x1="35" y1="85" x2="195" y2="85" class="dim-line" marker-start="url(#arrow)" marker-end="url(#arrow)"/>
    <text x="115" y="98" class="dim-text">80.0 mm (Center-to-Center)</text>

    <line x1="20" y1="112" x2="210" y2="112" class="dim-line" marker-start="url(#arrow)" marker-end="url(#arrow)"/>
    <text x="115" y="125" class="dim-text">Panjang Total Potong: 95.0 mm</text>

    <text x="12" y="145" class="part-desc">• Ujung depan dipasangi dudukan servo capit (Gripper).</text>
  </g>

  <!-- PART 3: BATANG PARALEL (PARALLEL LINKAGE ROD) -->
  <g transform="translate(530, 95)">
    <rect x="0" y="0" width="290" height="155" class="header-box" rx="4"/>
    <text x="12" y="22" class="part-name">3. Batang Paralel (Siku Rendah)</text>
    <rect x="210" y="10" width="68" height="16" class="badge" style="fill:#10B981;"/>
    <text x="244" y="22" class="badge-text">1 LAPIS (RINGAN)</text>

    <rect x="20" y="50" width="190" height="20" class="wood"/>
    <circle cx="35" cy="60" r="4" class="hole"/>
    <circle cx="195" cy="60" r="4" class="hole"/>

    <line x1="35" y1="85" x2="195" y2="85" class="dim-line" marker-start="url(#arrow)" marker-end="url(#arrow)"/>
    <text x="115" y="98" class="dim-text">80.0 mm (Wajib Sama dgn Bahu!)</text>

    <text x="12" y="125" class="warn-text">KUNCI ANTI-LETOY:</text>
    <text x="12" y="142" class="part-desc">Menyalurkan torsi servo siku dari bawah ke atas tanpa</text>
    <text x="12" y="153" class="part-desc">beban servo bertumpuk di siku arm.</text>
  </g>

  <!-- PART 4: UPRIGHT PILLARS / TIANG PENOPANG -->
  <g transform="translate(30, 270)">
    <rect x="0" y="0" width="230" height="165" class="header-box" rx="4"/>
    <text x="12" y="22" class="part-name">4. Tiang Penopang Bahu (x2)</text>
    <text x="12" y="38" class="part-desc">Tegak di atas turntable menopang Servo 2 &amp; 3</text>

    <!-- Upright Stick (Vertical 45mm x 20mm scale) -->
    <rect x="35" y="55" width="40" height="90" class="wood-laminate"/>
    <!-- Slot Servo SG90: 23mm x 12.2mm -> scale: 24px x 46px -->
    <rect x="43" y="75" width="24" height="46" class="hole"/>
    <circle cx="55" cy="65" r="3" class="hole"/>
    <circle cx="55" cy="130" r="3" class="hole"/>

    <text x="100" y="75" class="dim-text" style="text-anchor:start;">Tinggi: 45 mm</text>
    <text x="100" y="95" class="dim-text" style="text-anchor:start;">Lebar: 20 mm (2 stik)</text>
    <text x="100" y="115" class="dim-text" style="text-anchor:start;">Slot: 23 x 12.5 mm</text>
    <text x="100" y="135" class="dim-text" style="text-anchor:start;">(Pas body SG90)</text>
  </g>

  <!-- PART 5: MEKANISME CAPIT (GRIPPER STIK ES KRIM) -->
  <g transform="translate(280, 270)">
    <rect x="0" y="0" width="230" height="165" class="header-box" rx="4"/>
    <text x="12" y="22" class="part-name">5. Sepasang Cakar Capit</text>
    <text x="12" y="38" class="part-desc">2 bilah stik dipotong serong membentuk paruh</text>

    <!-- Jari 1 -->
    <polygon points="30,65 140,55 135,70 30,75" class="wood"/>
    <circle cx="45" cy="70" r="3" class="hole"/>
    <text x="155" y="65" class="dim-text" style="text-anchor:start;">Panjang: 55 mm</text>

    <!-- Jari 2 -->
    <polygon points="30,105 140,115 135,100 30,95" class="wood"/>
    <circle cx="45" cy="100" r="3" class="hole"/>
    <text x="155" y="110" class="dim-text" style="text-anchor:start;">Sudut Serong 15°</text>

    <rect x="12" y="130" width="206" height="26" class="note-box"/>
    <text x="18" y="147" class="note-text" style="fill:#38BDF8;">Tip: Pasang karet gelang di ujung paruh agar cengkeram kuat!</text>
  </g>

  <!-- PART 6: TURNTABLE & BASE RAFT -->
  <g transform="translate(530, 270)">
    <rect x="0" y="0" width="290" height="165" class="header-box" rx="4"/>
    <text x="12" y="22" class="part-name">6. Turntable &amp; Tatakan Meja (Base)</text>
    
    <!-- Base Raft (8 sticks) -->
    <rect x="20" y="50" width="100" height="95" class="wood" style="fill:#334155; stroke:#64748B;"/>
    <text x="70" y="85" class="dim-text" style="fill:#F8FAFC;">Base Meja</text>
    <text x="70" y="100" class="dim-text" style="fill:#94A3B8;">80 x 114 mm</text>
    <rect x="58" y="105" width="24" height="13" class="hole"/>
    <text x="70" y="115" style="font-size:7px; fill:#EF4444; text-anchor:middle;">Slot SG90</text>

    <!-- Turntable Disc -->
    <circle cx="190" cy="95" r="35" class="wood-laminate"/>
    <circle cx="190" cy="95" r="5" class="hole"/>
    <text x="190" y="145" class="dim-text">Turntable Ø 50mm</text>
    <text x="190" y="157" class="part-desc" style="text-anchor:middle;">Dilem ke Horn Servo 1</text>
  </g>

  <!-- PANDUAN PERAKITAN & ATURAN TEKNIS -->
  <g transform="translate(30, 455)">
    <rect x="0" y="0" width="790" height="145" class="note-box" style="stroke:#0284C7; stroke-width:1.5;"/>
    <text x="20" y="25" class="part-name" style="fill:#38BDF8;">PANDUAN PERAKITAN CEPAT (ASSEMBLY CHECKLIST)</text>

    <text x="20" y="48" class="note-text">1. ALAT: Cutter tajam, penggaris besi, bor mini/solder runcing (Ø 2–2.5mm), lem tembak (hot glue) + lem Korea (Alteco).</text>
    <text x="20" y="68" class="note-text">2. LAMINASI: Bagian Lengan Bahu (Part 1) dan Lengan Depan (Part 2) HARUS 2 lapis stik yang dilem rapat dengan lem Alteco.</text>
    <text x="20" y="88" class="note-text">3. PIVOT (SENDI): Gunakan baut M2 x 12mm atau tusuk sate/tusuk gigi bambu yang ujungnya ditahan tetesan lem tembak.</text>
    <text x="20" y="108" class="note-text">4. KALIBRASI 90°: Sebelum memasang lengan ke gir servo SG90, tancapkan servo ke Arduino dan beri sinyal posisi 90° (tengah).</text>
    <text x="20" y="128" class="warn-text">5. POWER SUPPLY: Jangan supply 4/5 servo langsung dari pin 5V Arduino! Gunakan Adaptor eksternal 5V 2A-3A (Common Ground).</text>
  </g>
</svg>
"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Exported SVG: {out_path}")


# =========================================================================
# 4. GENERATE 2D DXF FOR SOLIDWORKS SKETCH
# =========================================================================
def generate_dxf(out_path):
    # Minimalist DXF R12 output containing the exact cutting outlines and hole centers
    lines = [
        "0", "SECTION",
        "2", "ENTITIES",
    ]

    def add_dxf_line(x1, y1, x2, y2, layer="CUT"):
        lines.extend([
            "0", "LINE",
            "8", layer,
            "10", f"{x1:.3f}",
            "20", f"{y1:.3f}",
            "30", "0.0",
            "11", f"{x2:.3f}",
            "21", f"{y2:.3f}",
            "31", "0.0"
        ])

    def add_dxf_circle(cx, cy, radius, layer="HOLE"):
        lines.extend([
            "0", "CIRCLE",
            "8", layer,
            "10", f"{cx:.3f}",
            "20", f"{cy:.3f}",
            "30", "0.0",
            "40", f"{radius:.3f}"
        ])

    def add_stick_dxf(x, y, length, width, hole_dist, layer="WOOD"):
        hw = width / 2.0
        # Kotak stik
        add_dxf_line(x, y - hw, x + length, y - hw, layer)
        add_dxf_line(x + length, y - hw, x + length, y + hw, layer)
        add_dxf_line(x + length, y + hw, x, y + hw, layer)
        add_dxf_line(x, y + hw, x, y - hw, layer)
        # Dua lubang pivot
        margin = (length - hole_dist) / 2.0
        add_dxf_circle(x + margin, y, 1.25, "HOLE")
        add_dxf_circle(x + margin + hole_dist, y, 1.25, "HOLE")

    # Part 1: Bicep (95 mm, hole dist 80 mm)
    add_stick_dxf(10, 20, 95.0, 10.0, 80.0)
    # Part 2: Forearm (95 mm, hole dist 80 mm)
    add_stick_dxf(10, 40, 95.0, 10.0, 80.0)
    # Part 3: Parallel Rod (95 mm, hole dist 80 mm)
    add_stick_dxf(10, 60, 95.0, 10.0, 80.0)

    # Turntable Circle Dia 50mm
    add_dxf_circle(150, 40, 25.0, "CUT")
    add_dxf_circle(150, 40, 3.0, "HOLE")

    lines.extend(["0", "ENDSEC", "0", "EOF"])

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Exported DXF: {out_path}")


# =========================================================================
# 5. RENDER HIGH-RES PNG PREVIEW (2D BLUEPRINT & 3D ASSEMBLY)
# =========================================================================
def render_visual_previews():
    # A. 2D BLUEPRINT DIAGRAM (Matplotlib High-Res)
    fig, ax = plt.subplots(figsize=(12, 8), dpi=180)
    fig.patch.set_facecolor('#0F172A')
    ax.set_facecolor('#0F172A')

    # Draw diagram elements
    # Title
    ax.text(0.5, 0.96, "BLUEPRINT DIMENSI POTONG STIK ES KRIM (ROBOT ARM SG90)",
            color='#38BDF8', fontsize=15, weight='bold', ha='center', transform=ax.transAxes)
    ax.text(0.5, 0.92, "Standar Ukuran Stik: Panjang 114 mm x Lebar 10 mm x Tebal 2 mm | Lubang Baut M2 (Ø 2.5 mm)",
            color='#94A3B8', fontsize=9.5, ha='center', transform=ax.transAxes)

    # Helper function to draw stick in matplotlib
    def draw_stick_dim(x, y, L, W, hole_span, name, qty, is_double=True):
        color = '#F59E0B' if is_double else '#FBBF24'
        # Body
        rect = patches.FancyBboxPatch((x, y - W/2), L, W, boxstyle="round,pad=0.5,rounding_size=4",
                                      facecolor=color, edgecolor='#B45309', linewidth=2.0)
        ax.add_patch(rect)
        # Holes
        margin = (L - hole_span) / 2.0
        h1 = patches.Circle((x + margin, y), 1.6, facecolor='#0F172A', edgecolor='#EF4444', linewidth=1.5)
        h2 = patches.Circle((x + margin + hole_span, y), 1.6, facecolor='#0F172A', edgecolor='#EF4444', linewidth=1.5)
        ax.add_patch(h1)
        ax.add_patch(h2)

        # Dimension arrows
        ax.annotate('', xy=(x + margin, y + W/2 + 5), xytext=(x + margin + hole_span, y + W/2 + 5),
                    arrowprops=dict(arrowstyle='<->', color='#38BDF8', lw=1.2))
        ax.text(x + margin + hole_span/2, y + W/2 + 7, f"{hole_span} mm", color='#38BDF8',
                fontsize=9, weight='bold', ha='center')

        # Total length
        ax.annotate('', xy=(x, y - W/2 - 5), xytext=(x + L, y - W/2 - 5),
                    arrowprops=dict(arrowstyle='<->', color='#94A3B8', lw=1.0))
        ax.text(x + L/2, y - W/2 - 11, f"Total Potong: {L} mm", color='#94A3B8', fontsize=8.5, ha='center')

        # Labels
        tag = "DOUBLE (Laminasi 4mm)" if is_double else "SINGLE (2mm)"
        ax.text(x + L/2, y + W/2 + 18, f"{name} ({qty})", color='#F8FAFC', fontsize=10.5, weight='bold', ha='center')
        ax.text(x + L/2, y + W/2 + 27, tag, color='#38BDF8', fontsize=8, weight='bold', ha='center')

    # Draw sticks
    draw_stick_dim(20, 110, 95, 12, 80, "1. Lengan Bahu (Bicep)", "2 batang ganda", is_double=True)
    draw_stick_dim(160, 110, 95, 12, 80, "2. Lengan Depan (Forearm)", "2 batang ganda", is_double=True)
    draw_stick_dim(20, 45, 95, 12, 80, "3. Batang Paralel Siku", "1 batang tunggal", is_double=False)
    draw_stick_dim(160, 45, 55, 12, 40, "4. Capit / Cakar Gripper", "2 keping potong serong", is_double=False)

    # Turntable & Base diagram
    ax.text(20, -5, "5. Turntable & Upright Mounts:", color='#F8FAFC', fontsize=11, weight='bold')
    ax.text(20, -15, "• Turntable: 4 stik silang atau piringan diameter 50 mm (dilem ke Horn Base Servo)\n"
                     "• Tiang Bahu: 2 pasang stik tinggi 45 mm x lebar 20 mm dengan lubang servo SG90 (23 x 12.5 mm)\n"
                     "• Tatakan Meja (Base): 8 stik dijejer sejajar membentuk rakit 80 x 114 mm.",
            color='#CBD5E1', fontsize=9.5, va='top')

    ax.set_xlim(0, 290)
    ax.set_ylim(-50, 160)
    ax.axis('off')

    plt.tight_layout()
    bp_png = os.path.join(OUT_DIR, "blueprint_dimensi_stik_eskrim.png")
    plt.savefig(bp_png, dpi=180, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Exported Blueprint PNG: {bp_png}")

    # B. 3D ASSEMBLY PREVIEW RENDER
    fig = plt.figure(figsize=(10, 8), dpi=150)
    fig.patch.set_facecolor('#0B0F19')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('#0B0F19')

    # Visual stick lines in 3D
    # Base
    ax.plot([-40, 40, 40, -40, -40], [-40, -40, 40, 40, -40], [0, 0, 0, 0, 0], color='#475569', lw=2)
    # Turntable
    theta = np.linspace(0, 2*np.pi, 30)
    ax.plot(25*np.cos(theta), 25*np.sin(theta), np.full_like(theta, 28), color='#F59E0B', lw=2)
    # Shoulder Pillar
    ax.plot([-16, -16], [0, 0], [28, 52], color='#B45309', lw=4)
    ax.plot([16, 16], [0, 0], [28, 52], color='#B45309', lw=4)
    # Bicep
    ax.plot([-16, -16], [5.5, 45], [52, 105], color='#FBBF24', lw=6, label='Bicep (95mm Double)')
    # Parallel Link
    ax.plot([16, 16], [-9.5, 30], [52, 105], color='#38BDF8', lw=3, label='Parallel Linkage Rod')
    # Forearm
    ax.plot([-16, -16], [45, 115], [105, 85], color='#FBBF24', lw=5, label='Forearm (95mm Double)')
    # Gripper
    ax.plot([-22, -22], [115, 155], [85, 85], color='#EF4444', lw=4, label='Gripper Claws')
    ax.plot([-10, -10], [115, 155], [85, 85], color='#EF4444', lw=4)
    # Target Box
    ax.scatter([-16], [150], [85], color='#10B981', s=150, marker='s', label='Target Object (Box)')

    ax.set_title("3D PREVIEW ROBOT ARM STIK ES KRIM (4-SERVO SG90)", color='#38BDF8', fontsize=13, weight='bold', pad=15)
    ax.set_xlabel("X (mm)", color='#94A3B8')
    ax.set_ylabel("Y (mm)", color='#94A3B8')
    ax.set_zlabel("Z (mm)", color='#94A3B8')
    ax.tick_params(colors='#64748B')
    ax.view_init(elev=22, azim=-55)
    ax.legend(facecolor='#1E293B', edgecolor='#334155', labelcolor='#F8FAFC', loc='upper left')

    prev_png = os.path.join(OUT_DIR, "preview_3d_assembly.png")
    plt.savefig(prev_png, dpi=150, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Exported 3D Preview PNG: {prev_png}")


# =========================================================================
# 6. WRITE COMPLETE ASSEMBLY & SOLIDWORKS/TINKERCAD GUIDE (MARKDOWN)
# =========================================================================
def write_markdown_guide():
    md = """# PANDUAN LENGKAP ROBOT ARM STIK ES KRIM (4 / 5 SERVO SG90)
**Tugas Kuliah: Sistem Kendali & IoT - Semester 5**  
*CAD Ready: SolidWorks & Tinkercad Compatible*

---

## 1. Daftar File Hasil Generate

Semua file telah di-generate secara presisi dalam folder `desain_arm_stik_eskrim`:

1. **`arm_stik_eskrim_assembly.stl`** & **`.obj`**:
   * Model 3D utuh assembly (tatakan, turntable, lengan, hingga gripper capit).
   * Siap langsung di-drag & drop ke **Tinkercad** atau di-import via *Insert > Part* di **SolidWorks**.
2. **`arm_stik_eskrim_flat_parts.stl`** & **`.obj`**:
   * Seluruh part stik es krim dalam bentuk kepingan datar terurai (flat pattern). Cocok untuk acuan pemotongan 1:1.
3. **`pola_potong_stik_eskrim.dxf`**:
   * File vektor standar CAD. Bisa langsung di-*Import into New Part as 2D Sketch* di **SolidWorks**.
4. **`pola_potong_stik_eskrim.svg`**:
   * Gambar vektor resolusi tinggi skala millimeter untuk print kertas pola.
5. **`blueprint_dimensi_stik_eskrim.png`**:
   * Gambar teknis visual berisi ukuran potong (mm) dan jarak lubang baut.
6. **`preview_3d_assembly.png`**:
   * Visualisasi render 3D tampak isometrik.

---

## 2. Kebutuhan Bahan & Alat (BOM)

| No | Bahan / Komponen | Jumlah | Keterangan |
|---|---|---|---|
| 1 | **Stik Es Krim Standar** | 15–20 batang | Dimensi standar ~114 mm x 10 mm x 2 mm |
| 2 | **Micro Servo TowerPro SG90** | 4 pcs (atau 5 pcs) | Dilengkapi horn & sekrup bawaan |
| 3 | **Baut & Mur M2 atau M2.5** | 6–8 pasang | Panjang 10–15 mm untuk sendi pivot (bisa diganti tusuk sate + lem) |
| 4 | **Lem Tembak (Hot Glue)** | 2–3 stik | Untuk merekatkan servo & base |
| 5 | **Lem Cyanoacrylate (Alteco / Lem G / Korea)** | 1 botol | **WAJIB** untuk melaminasi 2 lapis stik agar kaku |
| 6 | **Karet Gelang / Busa Tipis** | 1–2 pcs | Ditempel pada ujung capit (gripper) agar tidak licin |
| 7 | **Mikrokontroler (Arduino Uno / ESP32)** | 1 unit | Kontroler sinyal PWM servo |
| 8 | **Power Supply Eksternal 5V 2A-3A** | 1 unit | Sangat penting! Hindari memberi daya 4 servo dari pin 5V Arduino |

---

## 3. Ukuran Pemotongan Stik (Cutting Table)

| Kode Part | Nama Bagian | Panjang Potong | Jarak Lubang (Center-to-Center) | Jumlah Lapisan | Fungsi |
|---|---|---|---|---|---|
| **A1 & A2** | Lengan Bahu (Bicep) | **95 mm** | **80.0 mm** | 2 Lapis (Laminasi 4mm) | Mengangkat lengan bawah |
| **B1 & B2** | Lengan Depan (Forearm) | **95 mm** | **80.0 mm** | 2 Lapis (Laminasi 4mm) | Menjangkau target |
| **C** | Batang Paralel Siku | **95 mm** | **80.0 mm** | 1 Lapis (Tunggal 2mm) | Meneruskan torsi servo siku dari bawah |
| **D1 & D2** | Tiang Dudukan Bahu | **45 mm** | Slot 23 x 12.5 mm | 2 Lapis | Penahan servo bahu & siku di turntable |
| **E1 & E2** | Cakar Capit (Gripper) | **55 mm** | Lubang pivot 15 mm | 1 Lapis | Menjepit benda uji |
| **F** | Piringan Turntable | **Ø 50 mm** | Poros tengah Ø 3 mm | 2 Lapis Silang | Berputar horizontal (Yaw) |
| **G** | Rakit Base (Alas) | **114 x 80 mm** | Slot tengah SG90 | 8 stik sejajar | Tatakan penopang seluruh robot |

---

## 4. Cara Buka di SolidWorks & Tinkercad

### A. Di Tinkercad:
1. Buka [tinkercad.com](https://www.tinkercad.com) dan buat design baru (*Create new 3D design*).
2. Di pojok kanan atas, klik tombol **Import**.
3. Drag & drop file `arm_stik_eskrim_assembly.stl` atau `arm_stik_eskrim_flat_parts.stl`.
4. Model akan muncul dengan skala millimeter asli 1:1. Kamu bisa memberi warna berbeda pada tiap part.

### B. Di SolidWorks:
1. Buka SolidWorks > Klik **Open** > Ganti file format ke **STL Files (*.stl)**.
2. Di jendela Open, klik tombol **Options...**:
   * Ubah *Import as* menjadi: **Solid Body** (atau Graphic Body).
   * Ubah *Unit* menjadi: **Millimeters**.
3. Pilih `arm_stik_eskrim_assembly.stl` lalu klik **Open**.
4. Atau jika ingin membuat part dari sketch 2D: Buka file `pola_potong_stik_eskrim.dxf`, pilih *Import to a new part as 2D sketch*, dan lakukan *Extrude Boss* setebal 2 mm (untuk stik tunggal) atau 4 mm (laminasi ganda).

---

## 5. Tips Sukses Mekanik & Anti-Gagal

1. **Kenapa Harus Laminasi (Double Stick)?**
   Stik es krim tunggal sangat mudah melintir karena serat kayunya tipis. Dengan menempelkan 2 stik menggunakan lem tetes Alteco, kekakuannya meningkat lebih dari 4x lipat!
2. **Kunci Torsi Ringan (Parallel Linkage):**
   Dengan menaruh Servo Bahu dan Servo Siku keduanya di turntable bawah, lengan tidak perlu menggotong berat motor servo di atas siku. Hasilnya lengan bergerak sangat mulus dan tidak loyo.
3. **Zero Positioning Sebelum Pasang:**
   Sebelum membaut horn putih servo ke gir servo, nyalakan Arduino dengan program kendali dan posisikan seluruh servo ke **90 derajat** (posisi netral tengah). Pasang lengan dalam posisi sudut 90 derajat siku-siku, baru kencangkan baut pengunci horn.
"""
    md_path = os.path.join(OUT_DIR, "PANDUAN_RAKIT_LENGKAP.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Exported Guide MD: {md_path}")


# =========================================================================
# MAIN EXECUTION
# =========================================================================
if __name__ == "__main__":
    print("=== GENERATING POPSICLE STICK ROBOTIC ARM CAD & BLUEPRINT ===")

    # 1. 3D Assembly Mesh
    assembly = build_assembly_3d()
    assembly.write_binary_stl(os.path.join(OUT_DIR, "arm_stik_eskrim_assembly.stl"), name="Assembly")
    assembly.write_obj(os.path.join(OUT_DIR, "arm_stik_eskrim_assembly.obj"))

    # 2. 3D Flat Parts Mesh
    flat = build_flat_parts_3d()
    flat.write_binary_stl(os.path.join(OUT_DIR, "arm_stik_eskrim_flat_parts.stl"), name="FlatParts")
    flat.write_obj(os.path.join(OUT_DIR, "arm_stik_eskrim_flat_parts.obj"))

    # 3. 2D Blueprint SVG
    generate_blueprint_svg(os.path.join(OUT_DIR, "pola_potong_stik_eskrim.svg"))

    # 4. 2D DXF for SolidWorks
    generate_dxf(os.path.join(OUT_DIR, "pola_potong_stik_eskrim.dxf"))

    # 5. Visual PNG Previews
    render_visual_previews()

    # 6. Complete Assembly Markdown Guide
    write_markdown_guide()

    print("=== ALL CAD & BLUEPRINT ASSETS GENERATED SUCCESSFULLY! ===")
