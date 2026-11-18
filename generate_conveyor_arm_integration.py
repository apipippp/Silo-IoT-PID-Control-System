import os
import math
import struct
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# =========================================================================
# STL BUILDER CLASS
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

    def write_binary_stl(self, filepath, name="Model"):
        header = f"Tinkercad Ready 3D: {name}".encode('ascii')[:80]
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
# 1. BUILD MINI ROBOTIC ARM DESIGNED SPECIFICALLY FOR THE CONVEYOR
# =========================================================================
def build_conveyor_loading_arm():
    mesh = STLMesh()
    T = 3.0  # 3mm acrylic

    # The arm sits beside the conveyor.
    # In Manuel's Tinkercad: Conveyor is centered along X or angled.
    # Let's place the Arm Base at (X = -65, Y = 0, Z = 0)
    # The Conveyor Belt surface is at Z = 30 mm, width = 45 mm (from Y = -22.5 to +22.5), centered at X = 0.
    
    # BASE OF THE ARM (Placed on left side of the conveyor)
    bx, by, bz = -55.0, 0.0, 0.0

    # 1. Base Plate (Akrilik 60 x 60 x 3 mm) dengan kaki tumpuan
    mesh.add_box(bx, by, 1.5, 60, 60, T)
    # Clamp bracket connecting Arm base to Conveyor frame rail
    mesh.add_box(bx + 20, by, 1.5, 20, 25, T)

    # Base SG90 Servo (Rotation / Yaw)
    mesh.add_box(bx, by, 14, 22.8, 12.2, 22.5)
    # Output gear tower
    mesh.add_cylinder(bx, by, 25, 28, 6.0, 6.0, segments=16)

    # 2. Turntable Disc (Diameter 46 mm, Z: 28 to 31 mm)
    mesh.add_cylinder(bx, by, 28, 31, 23.0, 23.0, segments=24)

    # 3. Shoulder Vertical Bracket (Plat tegak penahan servo bahu)
    # Z: 31 to 58 mm
    mesh.add_box(bx - 8, by, 44.5, T, 26, 27)

    # Shoulder SG90 Servo (Bahu - Pitch 1)
    mesh.add_box(bx + 4, by, 45, 22.8, 12.2, 22.5)

    # 4. Lower Arm / Bicep Link (Lengan Bawah)
    # Pivot at (bx + 4, by + 8, 45), reach up & forward to Elbow at (bx + 25, by + 8, 80)
    p_shoulder = (bx + 4, by + 8, 45)
    p_elbow = (bx + 25, by + 8, 80)
    mesh.add_cylinder_orient(p_shoulder, p_elbow, 5.5, segments=16)

    # Elbow SG90 Servo (Siku - Pitch 2)
    mesh.add_box(bx + 25, by, 80, 22.8, 12.2, 22.5)

    # 5. Forearm Link (Lengan Atas)
    # Reaching down from Elbow (bx + 25, by - 8, 80) to Gripper above conveyor at (0, 0, 48)
    p_wrist = (0, 0, 48)
    mesh.add_cylinder_orient((bx + 25, by - 8, 80), p_wrist, 5.0, segments=16)

    # 6. Gripper Base Plate + Fixed Jaw (Menghadap lurus ke bawah/miring)
    # Center at (0, 0, 45)
    mesh.add_box(0, 0, 45, 26, 32, T)
    # Gripper Servo SG90
    mesh.add_box(0, 0, 55, 12.2, 22.8, 18)

    # Fixed Claw (Jari Capit Tetap di Y = -13 mm)
    mesh.add_box(0, -13, 33, 14, 6, 22)
    mesh.add_box(0, -9, 23, 14, 5, 5) # Grip tip

    # 7. Moving Claw (Jari Capit Gerak di Y = +13 mm, digerakkan servo horn)
    mesh.add_box(0, 13, 33, 14, 6, 22)
    mesh.add_box(0, 9, 23, 14, 5, 5) # Grip tip

    # Red Box / Workpiece Cube (Being clamped or placed onto conveyor)
    # Size 18 x 18 x 18 mm, sitting right on belt at Z = 30 to 48 mm!
    mesh.add_box(0, 0, 31, 18, 18, 18)

    return mesh


# =========================================================================
# 2. BUILD THE COMPLETE SCENE (CONVEYOR + SILO + SENSORS + RED BOX + ARM)
# (Persis seperti screenshot Tinkercad Manuel, tapi sudah ada Arm-nya!)
# =========================================================================
def build_full_scene_with_arm():
    mesh = STLMesh()

    # Add the Arm first
    arm = build_conveyor_loading_arm()
    mesh.triangles.extend(arm.triangles)

    # CONVEYOR MOCKUP (Persis proporsi di Tinkercad Manuel)
    # Conveyor Bed: Length 140 mm (from X = -30 to X = 110), Width 50 mm (Y: -25 to +25), Top at Z = 22 mm
    # Belt (black)
    mesh.add_box(40, 0, 21, 140, 48, 4)
    # Left & Right Rails
    mesh.add_box(40, -25, 14, 140, 3, 18)
    mesh.add_box(40, 25, 14, 140, 3, 18)
    # Rollers at ends
    mesh.add_cylinder(110, 0, 8, 8, 10, 10, segments=20) # front
    # Yellow TT Motor on conveyor side (like in Manuel's Tinkercad!)
    mesh.add_box(112, 33, 12, 22, 16, 18)
    mesh.add_cylinder(112, 25, 12, 12, 4, 4, segments=12)

    # SILO / CHAMBER ENCLOSURE AT CONVEYOR END (X = 110 to 160)
    # Base floor
    mesh.add_box(135, 0, 2, 50, 70, 4)
    # Back wall (where sensors are mounted)
    mesh.add_box(160, 0, 50, 4, 70, 96)
    # Left & Right Chamber Walls
    mesh.add_box(135, -35, 50, 50, 4, 96)
    mesh.add_box(135, 35, 50, 50, 4, 96)
    # Slanted roof
    mesh.add_box(135, 0, 98, 50, 70, 4)

    # SENSORS MOUNTED ON BACK WALL:
    # 1. Ultrasonic Sensor (HC-SR04) dual eyes facing the conveyor
    mesh.add_box(156, -10, 60, 4, 38, 18)
    mesh.add_cylinder(154, -20, 60, 60, 6, 6, segments=16) # eye 1
    mesh.add_cylinder(154, 0, 60, 60, 6, 6, segments=16)   # eye 2

    # 2. Climate / Gas Sensor
    mesh.add_box(156, 20, 65, 4, 16, 22)

    # CONTROL BOX (CYAN / TRANSLUCENT BOX on the right side)
    mesh.add_box(100, 80, 40, 45, 60, 80)
    mesh.add_box(98, 80, 55, 3, 35, 14) # LCD display bezel

    # PICK TRAY / FEEDING STATION (Where the arm grabs new boxes from)
    # Located at (X = -55, Y = -50, Z = 0)
    mesh.add_box(-55, -45, 12, 30, 30, 24)
    # Spare red cube waiting to be loaded
    mesh.add_box(-55, -45, 30, 16, 16, 16)

    return mesh


# =========================================================================
# 3. BUILD 2D LASER CUT VECTOR FOR THE ARM
# =========================================================================
def generate_arm_conveyor_svg(out_path):
    svg = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 150" width="200mm" height="150mm" style="background:#0F172A; font-family:'Segoe UI',Roboto,Helvetica,sans-serif;">
  <defs>
    <style>
      .cut { fill: none; stroke: #EF4444; stroke-width: 0.25; }
      .slot { fill: none; stroke: #EF4444; stroke-width: 0.25; }
      .hole { fill: none; stroke: #EF4444; stroke-width: 0.25; }
      .engrave { fill: #38BDF8; font-size: 2.8px; font-weight: bold; }
      .subtext { fill: #94A3B8; font-size: 2.1px; }
      .sheet { fill: none; stroke: #334155; stroke-width: 0.5; stroke-dasharray: 2 1; }
    </style>
  </defs>

  <rect x="5" y="5" width="190" height="140" rx="3" class="sheet"/>
  
  <text x="10" y="14" fill="#F8FAFC" font-size="3.8" font-weight="bold">POLA MINI ROBOTIC ARM — LOADER BOX CONVEYOR (AKRILIK 3mm)</text>
  <text x="10" y="19" fill="#94A3B8" font-size="2.4">Desain Khusus Dudukan Samping Conveyor Silo | Skala 1:1 mm | Merah: Potong Laser</text>

  <!-- 1. BASE PLATE DENGAN BRACKET JEPIT CONVEYOR -->
  <g id="base">
    <!-- Base 60x60 dengan kuping baut ke rel conveyor -->
    <path d="M 12 25 L 72 25 L 72 40 L 88 40 L 88 70 L 72 70 L 72 85 L 12 85 Z" class="cut"/>
    <!-- Slot Servo Base SG90 -->
    <rect x="30.5" y="48.75" width="23" height="12.5" class="slot"/>
    <circle cx="26.5" cy="55" r="1.1" class="hole"/>
    <circle cx="57.5" cy="55" r="1.1" class="hole"/>
    <!-- Lubang baut ke frame conveyor M3 -->
    <circle cx="80" cy="48" r="1.6" class="hole"/>
    <circle cx="80" cy="62" r="1.6" class="hole"/>
    <text x="42" y="34" class="engrave" text-anchor="middle">1. BASE PLATE</text>
    <text x="42" y="39" class="subtext" text-anchor="middle">+ Conveyor Clamp</text>
  </g>

  <!-- 2. TURNTABLE DISC -->
  <g id="turntable">
    <circle cx="118" cy="50" r="23" class="cut"/>
    <circle cx="118" cy="50" r="1.2" class="hole"/>
    <circle cx="118" cy="43" r="0.9" class="hole"/>
    <circle cx="118" cy="57" r="0.9" class="hole"/>
    <rect x="104" y="42" width="3.2" height="16" class="slot"/>
    <text x="118" y="33" class="engrave" text-anchor="middle">2. TURNTABLE</text>
  </g>

  <!-- 3. SHOULDER BRACKET -->
  <g id="shoulder">
    <path d="M 150 25 L 180 25 L 180 54 L 172 54 L 172 58 L 158 58 L 158 54 L 150 54 Z" class="cut"/>
    <rect x="153.5" y="32" width="23" height="12.5" class="slot"/>
    <circle cx="150.5" cy="38.25" r="1.1" class="hole"/>
    <circle cx="179.5" cy="38.25" r="1.1" class="hole"/>
    <text x="165" y="30" class="engrave" text-anchor="middle">3. BAHU</text>
  </g>

  <!-- 4. BICEP LINK (Panjang 55mm agar proporsional dengan tinggi conveyor) -->
  <g id="bicep">
    <rect x="12" y="95" width="58" height="16" rx="5" class="cut"/>
    <circle cx="20" cy="103" r="1.2" class="hole"/>
    <circle cx="16" cy="103" r="0.9" class="hole"/>
    <circle cx="24" cy="103" r="0.9" class="hole"/>
    <circle cx="62" cy="103" r="1.6" class="hole"/>
    <text x="41" y="104" class="engrave" text-anchor="middle">4. BICEP (58mm)</text>
  </g>

  <!-- 5. FOREARM LINK -->
  <g id="forearm">
    <rect x="80" y="95" width="52" height="14" rx="5" class="cut"/>
    <circle cx="87" cy="102" r="1.2" class="hole"/>
    <circle cx="83" cy="102" r="0.9" class="hole"/>
    <circle cx="91" cy="102" r="0.9" class="hole"/>
    <circle cx="125" cy="102" r="1.6" class="hole"/>
    <text x="106" y="103" class="engrave" text-anchor="middle">5. FOREARM</text>
  </g>

  <!-- 6. GRIPPER BASE + FIXED CLAW (Dirancang khusus menjepit Box Merah 20mm!) -->
  <g id="gripper-base">
    <path d="M 142 68 
             L 172 68 
             L 172 90 
             L 190 90 
             L 192 98 
             L 186 98 
             L 186 94 
             L 172 94 
             L 172 104 
             L 142 104 Z" class="cut"/>
    <rect x="145.5" y="75" width="23" height="12.5" class="slot"/>
    <circle cx="142.5" cy="81.25" r="1.1" class="hole"/>
    <circle cx="170.5" cy="81.25" r="1.1" class="hole"/>
    <text x="157" y="73" class="engrave" text-anchor="middle">6. GRIPPER BASE</text>
    <text x="157" y="100" class="subtext" text-anchor="middle">+ JARI DIAM</text>
  </g>

  <!-- 7. MOVING CLAW (Jari gerak) -->
  <g id="moving-claw">
    <path d="M 142 112 
             L 175 112 
             L 180 120 
             L 174 120 
             L 174 116 
             L 154 116 
             C 146 116, 142 114, 142 112 Z" class="cut"/>
    <circle cx="148" cy="114" r="1.2" class="hole"/>
    <circle cx="152" cy="114" r="0.9" class="hole"/>
    <circle cx="156" cy="114" r="0.9" class="hole"/>
    <text x="160" y="125" class="engrave" text-anchor="middle">7. JARI GERAK</text>
  </g>

  <!-- Catatan Ringkas -->
  <rect x="12" y="118" width="120" height="20" rx="2" fill="#1E293B" stroke="#334155" stroke-width="0.4"/>
  <text x="16" y="125" fill="#38BDF8" font-size="2.4" font-weight="bold">UKURAN PAS DENGAN CONVEYOR TINKERCAD:</text>
  <text x="16" y="131" fill="#94A3B8" font-size="2.0">Bukaan capit: 24 mm (pas jepit kubus merah 18-20 mm pada conveyor).</text>
  <text x="16" y="136" fill="#94A3B8" font-size="2.0">Jangkauan arm: Pas memindah dari tray samping ke atas sabuk conveyor.</text>
</svg>
"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Exported Conveyor Arm SVG: {out_path}")


# =========================================================================
# MAIN EXECUTION
# =========================================================================
def main():
    target_dir = os.path.abspath("desain_arm_conveyor_tinkercad")
    os.makedirs(target_dir, exist_ok=True)
    
    repo_target = os.path.abspath("TugasBesarIOT_SiloMonitoringSystem/desain_arm_conveyor_tinkercad")
    os.makedirs(repo_target, exist_ok=True)

    print("Building Conveyor Mini Robotic Arm...")

    # 1. Arm STL (Solo Assembly)
    arm = build_conveyor_loading_arm()
    arm.write_binary_stl(os.path.join(target_dir, "mini_arm_conveyor_loader.stl"), "Mini Arm Conveyor Loader")
    arm.write_obj(os.path.join(target_dir, "mini_arm_conveyor_loader.obj"))

    # 2. Full Scene STL (Conveyor + Silo + Red Box + Mini Arm)
    full_scene = build_full_scene_with_arm()
    full_scene.write_binary_stl(os.path.join(target_dir, "conveyor_system_with_arm_scene.stl"), "Conveyor With Arm Scene")
    full_scene.write_obj(os.path.join(target_dir, "conveyor_system_with_arm_scene.obj"))

    # 3. 2D Laser Cut SVG & DXF
    svg_file = os.path.join(target_dir, "pola_laser_cut_arm_conveyor_3mm.svg")
    generate_arm_conveyor_svg(svg_file)

    # 4. Render 3D Scene Preview showing the Arm + Conveyor setup
    print("Rendering 3D scene preview...")
    fig = plt.figure(figsize=(11, 8.5), facecolor='#0F172A')
    ax = fig.add_subplot(111, projection='3d', facecolor='#0F172A')

    # Color coded meshes
    step_full = max(1, len(full_scene.triangles) // 2500)
    t_sampled = [[t[1], t[2], t[3]] for i, t in enumerate(full_scene.triangles) if i % step_full == 0]
    mesh_poly = Poly3DCollection(t_sampled, facecolors='#38BDF8', edgecolors='#0284C7', linewidths=0.2, alpha=0.85)
    ax.add_collection3d(mesh_poly)

    ax.set_xlim(-80, 180)
    ax.set_ylim(-60, 120)
    ax.set_zlim(0, 110)
    ax.set_xlabel('X (mm) [Sumbu Conveyor]', color='#94A3B8')
    ax.set_ylabel('Y (mm)', color='#94A3B8')
    ax.set_zlabel('Z (mm) [Tinggi]', color='#94A3B8')
    ax.tick_params(colors='#64748B')
    ax.view_init(elev=28, azim=-50)
    ax.set_title('HASIL INTEGRASI: MINI ROBOTIC ARM SG90 + CONVEYOR & SILO CHAMBER\n(Skala & Posisi Pas Menaruh Box Merah ke Conveyor)', color='#F8FAFC', fontsize=11, weight='bold')

    plt.tight_layout()
    preview_scene = os.path.join(target_dir, "preview_conveyor_with_arm_3d.png")
    plt.savefig(preview_scene, dpi=200, facecolor=fig.get_facecolor())
    plt.close()

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
