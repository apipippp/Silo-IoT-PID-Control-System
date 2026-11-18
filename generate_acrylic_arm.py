import os
import math
import struct
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# ==========================================
# STL 3D MESH GENERATOR CLASS
# ==========================================
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

    def add_box(self, center_x, center_y, center_z, size_x, size_y, size_z):
        dx, dy, dz = size_x / 2.0, size_y / 2.0, size_z / 2.0
        x0, x1 = center_x - dx, center_x + dx
        y0, y1 = center_y - dy, center_y + dy
        z0, z1 = center_z - dz, center_z + dz

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

    def add_cylinder(self, cx, cy, z_bottom, z_top, radius_bottom, radius_top=None, segments=32, cap_bottom=True, cap_top=True):
        if radius_top is None:
            radius_top = radius_bottom
        angles = [2.0 * math.pi * i / segments for i in range(segments)]
        bot_pts = [(cx + radius_bottom * math.cos(a), cy + radius_bottom * math.sin(a), z_bottom) for a in angles]
        top_pts = [(cx + radius_top * math.cos(a), cy + radius_top * math.sin(a), z_top) for a in angles]

        for i in range(segments):
            ni = (i + 1) % segments
            self.add_quad(bot_pts[i], bot_pts[ni], top_pts[ni], top_pts[i])

        if cap_bottom and radius_bottom > 1e-4:
            c_bot = (cx, cy, z_bottom)
            for i in range(segments):
                ni = (i + 1) % segments
                self.add_triangle(c_bot, bot_pts[ni], bot_pts[i])

        if cap_top and radius_top > 1e-4:
            c_top = (cx, cy, z_top)
            for i in range(segments):
                ni = (i + 1) % segments
                self.add_triangle(c_top, top_pts[i], top_pts[ni])

    def add_cylinder_orient(self, p_start, p_end, radius, segments=20):
        # Cylinder between arbitrary two 3D points
        p1 = np.array(p_start, dtype=float)
        p2 = np.array(p_end, dtype=float)
        v = p2 - p1
        length = np.linalg.norm(v)
        if length < 1e-6:
            return
        z_dir = v / length
        
        # Arbitrary perpendicular vector
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

        # Caps
        cp1, cp2 = tuple(p1), tuple(p2)
        for i in range(segments):
            ni = (i + 1) % segments
            self.add_triangle(cp1, bot_pts[ni], bot_pts[i])
            self.add_triangle(cp2, top_pts[i], top_pts[ni])

    def add_sg90_servo(self, cx, cy, cz, rot_z_deg=0, rot_x_deg=0):
        # Realistic SG90 Micro Servo model
        # Body: 22.8 mm x 12.2 mm x 22.5 mm
        # Flange/Ears at top: 32.5 mm x 12.0 mm x 2.5 mm
        # Gear tower on top: dia 12 mm x 5 mm, Output shaft horn
        # Build in local coords then transform
        rot_z = math.radians(rot_z_deg)
        cos_z, sin_z = math.cos(rot_z), math.sin(rot_z)

        def transform(pt):
            x, y, z = pt
            rx = x * cos_z - y * sin_z + cx
            ry = x * sin_z + y * cos_z + cy
            rz = z + cz
            return (rx, ry, rz)

        # Servo main body (translucent blue in real life)
        # local box: center at (0, 0, 0)
        dx, dy, dz = 22.8 / 2, 12.2 / 2, 22.5 / 2
        # We can add transformed box
        # For simplicity, create local box vertices and add quads
        pts = [
            (-dx, -dy, -dz), (dx, -dy, -dz), (dx, dy, -dz), (-dx, dy, -dz),
            (-dx, -dy, dz), (dx, -dy, dz), (dx, dy, dz), (-dx, dy, dz)
        ]
        t = [transform(p) for p in pts]
        self.add_quad(t[0], t[3], t[2], t[1])
        self.add_quad(t[4], t[5], t[6], t[7])
        self.add_quad(t[0], t[1], t[5], t[4])
        self.add_quad(t[2], t[3], t[7], t[6])
        self.add_quad(t[3], t[0], t[4], t[7])
        self.add_quad(t[1], t[2], t[6], t[5])

        # Mounting ears (ears span 32.5 mm along X, at Z near top +8)
        edx, edy, edz = 32.5 / 2, 12.0 / 2, 2.0 / 2
        ez0 = 6.0
        e_pts = [
            (-edx, -edy, ez0 - edz), (edx, -edy, ez0 - edz), (edx, edy, ez0 - edz), (-edx, edy, ez0 - edz),
            (-edx, -edy, ez0 + edz), (edx, -edy, ez0 + edz), (edx, edy, ez0 + edz), (-edx, edy, ez0 + edz)
        ]
        et = [transform(p) for p in e_pts]
        self.add_quad(et[0], et[3], et[2], et[1])
        self.add_quad(et[4], et[5], et[6], et[7])
        self.add_quad(et[0], et[1], et[5], et[4])
        self.add_quad(et[2], et[3], et[7], et[6])
        self.add_quad(et[3], et[0], et[4], et[7])
        self.add_quad(et[1], et[2], et[6], et[5])

        # Gear tower cylinder (offset along X at +5.5 mm)
        g_center = transform((5.5, 0, dz + 2.5))
        g_base = transform((5.5, 0, dz))
        self.add_cylinder_orient(g_base, g_center, 6.0, segments=16)
        
        # White horn (single arm or cross horn)
        h_base = transform((5.5, 0, dz + 3.0))
        h_tip = transform((5.5 + 10.0, 0, dz + 3.0))
        self.add_cylinder_orient(h_base, h_tip, 2.5, segments=12)

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
# BUILD 3D ASSEMBLED ROBOTIC ARM MESH (ACRYLIC 3MM PLATES + SG90 SERVOS)
# =========================================================================
def build_acrylic_arm_3d():
    mesh = STLMesh()
    T = 3.0  # 3mm acrylic thickness

    # 1. BASE ASSEMBLY
    # Bottom Base Plate (80 mm x 80 mm with rounded corners, Z: 0 to 3 mm)
    mesh.add_box(0, 0, 1.5, 80, 80, 3)
    # 4 Rubber Feet pads under base
    for fx, fy in [(-32, -32), (32, -32), (32, 32), (-32, 32)]:
        mesh.add_cylinder(fx, fy, -2, 0, 4, 4, segments=16)

    # Base SG90 Servo (Mounted vertically inside the base center)
    mesh.add_sg90_servo(0, 0, 15, rot_z_deg=90)

    # Rotating Turntable Disc (Diameter 65 mm, Z: 28 to 31 mm)
    mesh.add_cylinder(0, 0, 28, 31, 32.5, 32.5, segments=36)

    # 2. SHOULDER BRACKET & SHOULDER SERVO
    # Left & Right Upright Brackets (Z: 31 to 75 mm)
    # Mounted on Turntable at Y = -18 mm and Y = +18 mm
    mesh.add_box(0, -18, 53, 30, T, 44)
    mesh.add_box(0, 18, 53, 30, T, 44)

    # Shoulder Servo (SG90) mounted horizontally at Z = 50 mm, facing along Y
    mesh.add_sg90_servo(0, 0, 50, rot_z_deg=0)

    # 3. LOWER ARM LINKAGE (HUMERUS / LENGAN BAWAH)
    # Length: 65 mm, tilted forward at ~35 degrees
    # Pivot at (0, -20, 50) reaching up to (38, -20, 102)
    p_shoulder_pivot = (0, -20, 50)
    p_elbow_pivot = (38, -20, 102)

    # Acrylic link plates (3mm thick) for lower arm
    mesh.add_cylinder_orient(p_shoulder_pivot, p_elbow_pivot, 6.0, segments=16)
    # Parallel stabilizing linkage rod
    p_para_bot = (0, -20, 62)
    p_para_top = (38, -20, 114)
    mesh.add_cylinder_orient(p_para_bot, p_para_top, 3.5, segments=12)

    # Elbow Servo (SG90) mounted at the elbow joint (Z = 102 mm)
    mesh.add_sg90_servo(38, -5, 102, rot_z_deg=0)

    # 4. UPPER FOREARM LINKAGE (RADIUS-ULNA / LENGAN ATAS)
    # Length: 60 mm, extending forward-downwards at ~15 degrees
    # From Elbow (38, -5, 102) reaching to Wrist (88, -5, 85)
    p_wrist = (88, -5, 85)
    mesh.add_cylinder_orient((38, 12, 102), (88, 12, 85), 5.5, segments=16)
    # Parallel rod for wrist leveling
    mesh.add_cylinder_orient((38, 12, 114), (88, 12, 97), 3.0, segments=12)

    # 5. WRIST PLATFORM & GRIPPER END EFFECTOR
    # Wrist plate (Z: 85 mm)
    mesh.add_box(92, 0, 85, 16, 28, T)

    # Gripper Servo (SG90) mounted horizontally flat on the wrist
    mesh.add_sg90_servo(106, 0, 85, rot_z_deg=180)

    # Gripper Base Plate (Z: 80 to 83 mm)
    mesh.add_box(115, 0, 81.5, 36, 42, T)

    # Gripper Jaws / Pincers (Capit Akrilik Kiri & Kanan dengan roda gigi interlock)
    # Left Jaw (open at angle)
    # Pivot point at (122, -14, 86)
    j_left_pivot = (122, -14, 86)
    j_left_mid = (142, -18, 86)
    j_left_tip = (156, -6, 86)
    mesh.add_cylinder_orient(j_left_pivot, j_left_mid, 4.0, segments=12)
    mesh.add_cylinder_orient(j_left_mid, j_left_tip, 3.5, segments=12)
    # Left finger rubber pad
    mesh.add_box(152, -7, 86, 12, 3, 8)

    # Right Jaw (symmetrical)
    # Pivot point at (122, 14, 86)
    j_right_pivot = (122, 14, 86)
    j_right_mid = (142, 18, 86)
    j_right_tip = (156, 6, 86)
    mesh.add_cylinder_orient(j_right_pivot, j_right_mid, 4.0, segments=12)
    mesh.add_cylinder_orient(j_right_mid, j_right_tip, 3.5, segments=12)
    # Right finger rubber pad
    mesh.add_box(152, 7, 86, 12, 3, 8)

    # Interlocking spur gear mesh cylinders between jaws
    mesh.add_cylinder(122, -14, 83, 86, 6.5, 6.5, segments=20)
    mesh.add_cylinder(122, 14, 83, 86, 6.5, 6.5, segments=20)

    # Target Object being gripped: Small Grain Cube / Mini Sample Box (16x16x16 mm)
    mesh.add_box(155, 0, 86, 14, 14, 14)

    return mesh


# =========================================================================
# BUILD 3D FLAT ACRYLIC PARTS SHEET FOR TINKERCAD
# (Semua kepingan akrilik 3mm diletakkan datar di Workplane Z=0..3 mm)
# =========================================================================
def build_flat_acrylic_parts_3d():
    mesh = STLMesh()
    T = 3.0  # 3mm thickness

    # 1. Base Plate (Square 80x80 with corner cutouts and SG90 servo hole 23x12.5)
    # Center at (-50, -45, 1.5)
    mesh.add_box(-50, -45, 1.5, 80, 80, T)

    # 2. Turntable Disc (Dia 65 mm)
    # Center at (45, -45, 1.5)
    mesh.add_cylinder(45, -45, 0, T, 32.5, 32.5, segments=36)

    # 3. Shoulder Upright Left & Right Brackets
    mesh.add_box(-70, 30, 1.5, 28, 48, T)
    mesh.add_box(-35, 30, 1.5, 28, 48, T)

    # 4. Lower Arm Links (Main Humerus & Parallel Rod)
    mesh.add_box(5, 30, 1.5, 16, 75, T)
    mesh.add_box(26, 30, 1.5, 10, 75, T)

    # 5. Upper Forearm Links
    mesh.add_box(45, 30, 1.5, 15, 68, T)
    mesh.add_box(65, 30, 1.5, 10, 68, T)

    # 6. Gripper Base Plate
    mesh.add_box(-60, 80, 1.5, 42, 38, T)

    # 7. Gripper Jaw Left & Right (Capit Akrilik)
    mesh.add_box(-15, 80, 1.5, 36, 18, T)
    mesh.add_box(25, 80, 1.5, 36, 18, T)

    # 8. Servo Horn Adapter Plates (Link pendorong capit)
    mesh.add_box(60, 80, 1.5, 20, 12, T)
    mesh.add_box(78, 80, 1.5, 20, 12, T)

    return mesh


# =========================================================================
# BUILD 2D LASER CUTTING SVG SHEET (PRECISE 1:1 VECTOR SCALE)
# =========================================================================
def generate_laser_cut_svg(out_path):
    # Standard Acrylic Sheet Size: 300 mm x 200 mm (A4 Laser Cutting Sheet)
    # Scale 1:1 in millimeters. Stroke: Red (#FF0000) hairline for CUTTING, Blue (#0066FF) for ENGRAVING/LABELS.
    svg = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 220" width="320mm" height="220mm" style="background:#0F172A; font-family:'Segoe UI',Roboto,Helvetica,sans-serif;">
  <defs>
    <!-- Laser Cut Hairline Styles -->
    <style>
      .cut { fill: none; stroke: #EF4444; stroke-width: 0.25; }
      .slot { fill: none; stroke: #EF4444; stroke-width: 0.25; }
      .hole { fill: none; stroke: #EF4444; stroke-width: 0.25; }
      .engrave { fill: #38BDF8; font-size: 3.2px; font-weight: bold; }
      .dim { stroke: #64748B; stroke-width: 0.2; stroke-dasharray: 1 0.5; }
      .dim-text { fill: #94A3B8; font-size: 2.5px; }
      .sheet-border { fill: none; stroke: #334155; stroke-width: 0.5; stroke-dasharray: 2 1; }
    </style>
  </defs>

  <!-- Sheet Border (300mm x 200mm Acrylic Stock, 3mm Thickness) -->
  <rect x="10" y="10" width="300" height="200" rx="3" class="sheet-border"/>
  
  <!-- Header / Metadata Engraving -->
  <text x="15" y="18" fill="#F8FAFC" font-size="5" font-weight="bold">POLA LASER CUTTING AKRILIK 3mm — MINI ROBOTIC ARM SG90 + 1-SERVO GRIPPER</text>
  <text x="15" y="24" fill="#94A3B8" font-size="3">Skala 1:1 mm | Garis Merah: Cut (Laser Potong) | Biru: Engrave (Penandaan Part &amp; Pinout) | Siap Impor Tinkercad</text>
  <text x="240" y="18" fill="#38BDF8" font-size="3.5" font-weight="bold">BAHAN: AKRILIK 3.0 mm</text>
  <text x="240" y="23" fill="#10B981" font-size="3">Toleransi Lubang: +0.2 mm</text>

  <!-- ======================================================= -->
  <!-- 1. BASE PLATE (80 mm x 80 mm) - Bottom Left (X: 15, Y: 30) -->
  <!-- ======================================================= -->
  <g id="part-base-plate">
    <!-- Outer Contour with rounded corners R5 -->
    <rect x="15" y="30" width="80" height="80" rx="6" class="cut"/>
    <!-- Center Cutout for Base SG90 Servo (23.0 x 12.5 mm) -->
    <rect x="43.5" y="63.75" width="23" height="12.5" rx="0.5" class="slot"/>
    <!-- Servo Mounting Screw Holes (2.0 mm dia, pitch 28 mm) -->
    <circle cx="39.5" cy="70" r="1.1" class="hole"/>
    <circle cx="70.5" cy="70" r="1.1" class="hole"/>
    <!-- 4 Corner Mounting Holes M3 (Dia 3.2 mm) -->
    <circle cx="23" cy="38" r="1.6" class="hole"/>
    <circle cx="87" cy="38" r="1.6" class="hole"/>
    <circle cx="23" cy="102" r="1.6" class="hole"/>
    <circle cx="87" cy="102" r="1.6" class="hole"/>
    <!-- Label -->
    <text x="55" y="45" class="engrave" text-anchor="middle">1. BASE BOTTOM</text>
    <text x="55" y="50" fill="#94A3B8" font-size="2.2" text-anchor="middle">80 x 80 mm (Akrilik 3mm)</text>
  </g>

  <!-- ======================================================= -->
  <!-- 2. ROTATING TURNTABLE DISC (Dia 65 mm) (X: 105, Y: 30) -->
  <!-- ======================================================= -->
  <g id="part-turntable">
    <circle cx="140" cy="70" r="32.5" class="cut"/>
    <!-- Center SG90 Horn Screw Hole -->
    <circle cx="140" cy="70" r="1.2" class="hole"/>
    <!-- 4 Horn fixing holes (pitch 7.5 mm) -->
    <circle cx="140" cy="62.5" r="0.9" class="hole"/>
    <circle cx="140" cy="77.5" r="0.9" class="hole"/>
    <circle cx="132.5" cy="70" r="0.9" class="hole"/>
    <circle cx="147.5" cy="70" r="0.9" class="hole"/>
    <!-- Interlocking Slots for Upright Brackets (3.0 mm x 15 mm) -->
    <rect x="122" y="55" width="3.2" height="15" rx="0.3" class="slot"/>
    <rect x="155" y="55" width="3.2" height="15" rx="0.3" class="slot"/>
    <rect x="122" y="75" width="3.2" height="15" rx="0.3" class="slot"/>
    <rect x="155" y="75" width="3.2" height="15" rx="0.3" class="slot"/>
    <!-- Label -->
    <text x="140" y="48" class="engrave" text-anchor="middle">2. TURNTABLE</text>
    <text x="140" y="95" fill="#94A3B8" font-size="2.2" text-anchor="middle">Dia 65 mm</text>
  </g>

  <!-- ======================================================= -->
  <!-- 3. SHOULDER UPRIGHT BRACKETS (Left & Right) (X: 180, Y: 30) -->
  <!-- ======================================================= -->
  <g id="part-shoulder-brackets">
    <!-- Left Upright (48 x 26 mm with tabs) -->
    <path d="M 180 35 L 206 35 L 206 75 L 201 75 L 201 80 L 185 80 L 185 75 L 180 75 Z" class="cut"/>
    <!-- SG90 Slot for Shoulder Servo (23 x 12.5 mm) -->
    <rect x="181.5" y="44" width="23" height="12.5" class="slot"/>
    <circle cx="193" cy="39" r="1.1" class="hole"/>
    <circle cx="193" cy="61" r="1.1" class="hole"/>
    <text x="193" y="71" class="engrave" text-anchor="middle">3A. SHOULDER L</text>

    <!-- Right Upright (Matching support) -->
    <path d="M 215 35 L 241 35 L 241 75 L 236 75 L 236 80 L 220 80 L 220 75 L 215 75 Z" class="cut"/>
    <!-- Bearing / Pivot Hole M3 (Dia 3.2 mm) -->
    <circle cx="228" cy="46" r="1.6" class="hole"/>
    <circle cx="228" cy="64" r="1.6" class="hole"/>
    <text x="228" y="71" class="engrave" text-anchor="middle">3B. SHOULDER R</text>
  </g>

  <!-- ======================================================= -->
  <!-- 4. LOWER LINKAGE ARMS (HUMERUS) (X: 250, Y: 30) -->
  <!-- ======================================================= -->
  <g id="part-lower-links">
    <!-- Main Bicep Arm (75 mm x 15 mm) -->
    <rect x="250" y="30" width="16" height="75" rx="6" class="cut"/>
    <circle cx="258" cy="38" r="1.6" class="hole"/>
    <circle cx="258" cy="97" r="1.6" class="hole"/>
    <!-- Slot for Servo Horn Connection -->
    <circle cx="258" cy="44" r="1.0" class="hole"/>
    <text x="258" y="68" class="engrave" text-anchor="middle" transform="rotate(-90 258 68)">4A. BICEP LINK (75mm)</text>

    <!-- Parallel Rod (Stabilizer) -->
    <rect x="272" y="30" width="10" height="75" rx="4" class="cut"/>
    <circle cx="277" cy="38" r="1.6" class="hole"/>
    <circle cx="277" cy="97" r="1.6" class="hole"/>
    <text x="277" y="68" class="engrave" text-anchor="middle" transform="rotate(-90 277 68)">4B. PARALLEL ROD</text>
  </g>

  <!-- ======================================================= -->
  <!-- 5. FOREARM LINKAGE (UPPER ARM) (X: 15, Y: 120) -->
  <!-- ======================================================= -->
  <g id="part-forearm-links">
    <!-- Forearm Main Plate (68 mm x 15 mm) with Elbow Servo Cutout -->
    <rect x="15" y="125" width="68" height="20" rx="5" class="cut"/>
    <circle cx="23" cy="135" r="1.6" class="hole"/>
    <circle cx="75" cy="135" r="1.6" class="hole"/>
    <!-- SG90 Slot for Wrist/Elbow Joint -->
    <rect x="34" y="128.75" width="23" height="12.5" class="slot"/>
    <circle cx="30" cy="135" r="1.1" class="hole"/>
    <circle cx="61" cy="135" r="1.1" class="hole"/>
    <text x="45" y="123" class="engrave" text-anchor="middle">5A. FOREARM (LENGAN ATAS)</text>

    <!-- Forearm Top Parallel Link -->
    <rect x="15" y="152" width="68" height="10" rx="4" class="cut"/>
    <circle cx="23" cy="157" r="1.6" class="hole"/>
    <circle cx="75" cy="157" r="1.6" class="hole"/>
    <text x="45" y="159" class="engrave" text-anchor="middle">5B. FOREARM PARALLEL ROD</text>
  </g>

  <!-- ======================================================= -->
  <!-- 6. GRIPPER BASE & WRIST MOUNT (X: 95, Y: 120) -->
  <!-- ======================================================= -->
  <g id="part-gripper-base">
    <!-- Wrist Adapter Flange -->
    <rect x="95" y="125" width="28" height="24" rx="4" class="cut"/>
    <circle cx="102" cy="137" r="1.6" class="hole"/>
    <circle cx="116" cy="137" r="1.6" class="hole"/>
    <text x="109" y="132" class="engrave" text-anchor="middle">WRIST</text>

    <!-- Gripper Main Base Plate (Holds 1 SG90 Servo) -->
    <path d="M 130 125 L 175 125 L 180 145 L 180 165 L 125 165 L 125 145 Z" class="cut"/>
    <!-- SG90 Gripper Servo Cutout (23 x 12.5 mm) -->
    <rect x="136" y="138" width="23" height="12.5" class="slot"/>
    <circle cx="132" cy="144.25" r="1.1" class="hole"/>
    <circle cx="163" cy="144.25" r="1.1" class="hole"/>
    <!-- Pivot Holes for Jaws (M3, Dia 3.2 mm) -->
    <circle cx="135" cy="158" r="1.6" class="hole"/>
    <circle cx="170" cy="158" r="1.6" class="hole"/>
    <text x="152" y="132" class="engrave" text-anchor="middle">6. GRIPPER BASE</text>
  </g>

  <!-- ======================================================= -->
  <!-- 7. GRIPPER JAWS (1-SERVO INTERLOCKING GEAR CLAWS) (X: 195, Y: 120) -->
  <!-- ======================================================= -->
  <g id="part-gripper-jaws">
    <!-- Left Jaw (Pincer A) with Integrated Spur Gear & Finger Claw -->
    <path d="M 205 135 
             C 208 132, 212 132, 215 135 
             L 220 142 
             L 238 140 
             C 246 140, 252 148, 250 156 
             L 246 156 
             C 244 150, 240 146, 235 146 
             L 218 148 
             L 216 156 
             C 212 158, 206 158, 203 154 
             Z" class="cut"/>
    <!-- Pivot Hole M3 (Dia 3.2 mm) -->
    <circle cx="210" cy="145" r="1.6" class="hole"/>
    <!-- Horn Drive Linkage Hole (Dia 2.0 mm) -->
    <circle cx="216" cy="139" r="1.1" class="hole"/>
    <text x="232" y="153" class="engrave" text-anchor="middle">7A. JAW L</text>

    <!-- Right Jaw (Pincer B) - Symmetrical Opposite -->
    <path d="M 205 175 
             C 208 172, 212 172, 215 175 
             L 220 182 
             L 238 180 
             C 246 180, 252 188, 250 196 
             L 246 196 
             C 244 190, 240 186, 235 186 
             L 218 188 
             L 216 196 
             C 212 198, 206 198, 203 194 
             Z" class="cut"/>
    <!-- Pivot Hole M3 (Dia 3.2 mm) -->
    <circle cx="210" cy="185" r="1.6" class="hole"/>
    <text x="232" y="193" class="engrave" text-anchor="middle">7B. JAW R</text>

    <!-- Gripper Connecting Link / Drive Arm (attaches to SG90 Horn) -->
    <rect x="260" y="130" width="24" height="10" rx="4" class="cut"/>
    <circle cx="265" cy="135" r="1.1" class="hole"/>
    <circle cx="279" cy="135" r="1.1" class="hole"/>
    <text x="272" y="146" class="engrave" text-anchor="middle">HORN LINK</text>

    <!-- Finger Friction Grip Pads (Akrilik gerigi untuk grip benda licin) -->
    <rect x="260" y="155" width="16" height="8" rx="1.5" class="cut"/>
    <rect x="280" y="155" width="16" height="8" rx="1.5" class="cut"/>
    <text x="278" y="169" class="engrave" text-anchor="middle">FINGER PADS</text>

    <!-- Spacer Washers M3 (8 pieces) -->
    <g id="washers">
      <circle cx="265" cy="185" r="4.0" class="cut"/><circle cx="265" cy="185" r="1.6" class="hole"/>
      <circle cx="275" cy="185" r="4.0" class="cut"/><circle cx="275" cy="185" r="1.6" class="hole"/>
      <circle cx="285" cy="185" r="4.0" class="cut"/><circle cx="285" cy="185" r="1.6" class="hole"/>
      <circle cx="295" cy="185" r="4.0" class="cut"/><circle cx="295" cy="185" r="1.6" class="hole"/>
      <circle cx="265" cy="195" r="4.0" class="cut"/><circle cx="265" cy="195" r="1.6" class="hole"/>
      <circle cx="275" cy="195" r="4.0" class="cut"/><circle cx="275" cy="195" r="1.6" class="hole"/>
      <circle cx="285" cy="195" r="4.0" class="cut"/><circle cx="285" cy="195" r="1.6" class="hole"/>
      <circle cx="295" cy="195" r="4.0" class="cut"/><circle cx="295" cy="195" r="1.6" class="hole"/>
      <text x="280" y="204" class="engrave" text-anchor="middle">M3 SPACER WASHERS (x8)</text>
    </g>
  </g>

  <!-- Technical Spec Legend (Bottom Margin) -->
  <g id="legend">
    <rect x="15" y="175" width="175" height="30" rx="3" fill="#1E293B" stroke="#334155" stroke-width="0.5"/>
    <text x="20" y="183" fill="#F8FAFC" font-size="2.8" font-weight="bold">BILL OF MATERIALS (HARDWARE):</text>
    <text x="20" y="189" fill="#94A3B8" font-size="2.3">• 4x Micro Servo TowerPro SG90 (Base, Shoulder, Elbow, Gripper)</text>
    <text x="20" y="195" fill="#94A3B8" font-size="2.3">• Baut &amp; Mur M3: M3x8mm (8 pcs), M3x12mm (6 pcs), M3x16mm (4 pcs)</text>
    <text x="20" y="201" fill="#94A3B8" font-size="2.3">• Mur Locknut M3 (Nylon lock nut agar engsel lengan bergerak lancar)</text>
  </g>
</svg>
"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Exported Laser Cut SVG: {out_path}")


# =========================================================================
# BUILD 2D DXF FILE (STANDARD CAD FORMAT FOR LASER CUTTER CNC)
# =========================================================================
def generate_laser_cut_dxf(out_path):
    # Minimal standard AutoCAD DXF Release 12 ASCII
    lines = []
    lines.append("0\nSECTION\n2\nENTITIES\n")

    def dxf_line(x1, y1, x2, y2, layer="CUT"):
        return f"0\nLINE\n8\n{layer}\n10\n{x1:.3f}\n20\n{y1:.3f}\n30\n0.0\n11\n{x2:.3f}\n21\n{y2:.3f}\n31\n0.0\n"

    def dxf_circle(cx, cy, r, layer="CUT"):
        return f"0\nCIRCLE\n8\n{layer}\n10\n{cx:.3f}\n20\n{cy:.3f}\n30\n0.0\n40\n{r:.3f}\n"

    def dxf_rect(x, y, w, h, layer="CUT"):
        res = ""
        res += dxf_line(x, y, x + w, y, layer)
        res += dxf_line(x + w, y, x + w, y + h, layer)
        res += dxf_line(x + w, y + h, x, y + h, layer)
        res += dxf_line(x, y + h, x, y, layer)
        return res

    # 1. Base Plate 80x80
    lines.append(dxf_rect(15, 30, 80, 80, "CUT"))
    lines.append(dxf_rect(43.5, 63.75, 23, 12.5, "CUT"))
    lines.append(dxf_circle(39.5, 70, 1.1, "HOLE"))
    lines.append(dxf_circle(70.5, 70, 1.1, "HOLE"))
    lines.append(dxf_circle(23, 38, 1.6, "HOLE"))
    lines.append(dxf_circle(87, 38, 1.6, "HOLE"))
    lines.append(dxf_circle(23, 102, 1.6, "HOLE"))
    lines.append(dxf_circle(87, 102, 1.6, "HOLE"))

    # 2. Turntable Disc Dia 65
    lines.append(dxf_circle(140, 70, 32.5, "CUT"))
    lines.append(dxf_circle(140, 70, 1.2, "HOLE"))
    lines.append(dxf_rect(122, 55, 3.2, 15, "CUT"))
    lines.append(dxf_rect(155, 55, 3.2, 15, "CUT"))

    # 3. Shoulder Brackets
    lines.append(dxf_rect(180, 35, 26, 45, "CUT"))
    lines.append(dxf_rect(181.5, 44, 23, 12.5, "CUT"))
    lines.append(dxf_rect(215, 35, 26, 45, "CUT"))
    lines.append(dxf_circle(228, 46, 1.6, "HOLE"))

    # 4. Links & Gripper
    lines.append(dxf_rect(250, 30, 16, 75, "CUT"))
    lines.append(dxf_rect(272, 30, 10, 75, "CUT"))
    lines.append(dxf_rect(15, 125, 68, 20, "CUT"))
    lines.append(dxf_rect(15, 152, 68, 10, "CUT"))
    lines.append(dxf_rect(130, 125, 45, 40, "CUT"))
    lines.append(dxf_rect(136, 138, 23, 12.5, "CUT"))

    lines.append("0\nENDSEC\n0\nEOF\n")

    with open(out_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"Exported Laser Cut DXF: {out_path}")


# =========================================================================
# MAIN EXECUTION SCRIPT
# =========================================================================
def main():
    target_dir = os.path.abspath("desain_arm_akrilik_sg90")
    os.makedirs(target_dir, exist_ok=True)
    
    repo_target = os.path.abspath("TugasBesarIOT_SiloMonitoringSystem/desain_arm_akrilik")
    os.makedirs(repo_target, exist_ok=True)

    print("Generating Robotic Arm Files (2D Laser Cut & 3D Tinkercad)...")

    # 1. 3D Assembled Arm Model (Tinkercad ready)
    arm_3d = build_acrylic_arm_3d()
    arm_3d.write_binary_stl(os.path.join(target_dir, "robotic_arm_sg90_assembly.stl"), "Robotic Arm SG90 Assembly")
    arm_3d.write_obj(os.path.join(target_dir, "robotic_arm_sg90_assembly.obj"))

    # 2. 3D Flat Acrylic Sheet Model (Tinkercad ready)
    flat_3d = build_flat_acrylic_parts_3d()
    flat_3d.write_binary_stl(os.path.join(target_dir, "acrylic_parts_flat_plate.stl"), "Flat Acrylic Parts Plate")
    flat_3d.write_obj(os.path.join(target_dir, "acrylic_parts_flat_plate.obj"))

    # 3. 2D Vector Laser Cutting Sheet (.SVG and .DXF)
    svg_path = os.path.join(target_dir, "pola_laser_cut_akrilik_arm_sg90.svg")
    generate_laser_cut_svg(svg_path)
    
    dxf_path = os.path.join(target_dir, "pola_laser_cut_akrilik_arm_sg90.dxf")
    generate_laser_cut_dxf(dxf_path)

    # 4. Render 3D Visual Preview
    print("Rendering 3D preview...")
    fig = plt.figure(figsize=(10, 8), facecolor='#0F172A')
    ax = fig.add_subplot(111, projection='3d', facecolor='#0F172A')
    
    # Sample triangles from assembly
    step = max(1, len(arm_3d.triangles) // 2500)
    t_sampled = [[t[1], t[2], t[3]] for i, t in enumerate(arm_3d.triangles) if i % step == 0]
    mesh_poly = Poly3DCollection(t_sampled, facecolors='#38BDF8', edgecolors='#0284C7', linewidths=0.3, alpha=0.85)
    ax.add_collection3d(mesh_poly)

    ax.set_xlim(-60, 180)
    ax.set_ylim(-60, 60)
    ax.set_zlim(0, 140)
    ax.set_xlabel('X (mm) [Jangkauan]', color='#94A3B8')
    ax.set_ylabel('Y (mm)', color='#94A3B8')
    ax.set_zlabel('Z (mm) [Tinggi]', color='#94A3B8')
    ax.tick_params(colors='#64748B')
    ax.view_init(elev=22, azim=-60)
    ax.set_title('PREVIEW 3D: MINI ROBOTIC ARM AKRILIK 3mm (SG90 + GRIPPER)\n(Siap Dibuka di Tinkercad / Mesin Laser Cutting)', color='#F8FAFC', fontsize=12, weight='bold')

    plt.tight_layout()
    preview_img = os.path.join(target_dir, "preview_robotic_arm_3d.png")
    plt.savefig(preview_img, dpi=200, facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved preview: {preview_img}")

    # Copy all to repo folder as well
    for f in os.listdir(target_dir):
        src = os.path.join(target_dir, f)
        dst = os.path.join(repo_target, f)
        if os.path.isfile(src):
            import shutil
            shutil.copy2(src, dst)

    print(f"\nAll files successfully generated in:\n  - {target_dir}\n  - {repo_target}")

if __name__ == "__main__":
    main()
