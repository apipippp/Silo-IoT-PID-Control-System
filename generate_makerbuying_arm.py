import os
import math
import struct
import numpy as np
import matplotlib.pyplot as plt
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

    def add_sg90_detail(self, cx, cy, cz, rot_x=0, rot_y=0, rot_z=0):
        # Precise SG90 Micro Servo 3D Body (Blue Box + Tower + White Horn)
        # Dimensions: 22.8 x 12.2 x 22.5 mm
        # Local transformation
        rx, ry, rz = math.radians(rot_x), math.radians(rot_y), math.radians(rot_z)
        
        # Rotation matrix Rz * Ry * Rx
        cx_c, sx_s = math.cos(rx), math.sin(rx)
        cy_c, sy_s = math.cos(ry), math.sin(ry)
        cz_c, sz_s = math.cos(rz), math.sin(rz)
        
        R = np.array([
            [cz_c*cy_c, cz_c*sy_s*sx_s - sz_s*cx_c, cz_c*sy_s*cx_c + sz_s*sx_s],
            [sz_s*cy_c, sz_s*sy_s*sx_s + cz_c*cx_c, sz_s*sy_s*cx_c - cz_c*sx_s],
            [-sy_s,     cy_c*sx_s,                  cy_c*cx_c]
        ])

        def tf(pt):
            p = np.array(pt, dtype=float)
            res = R @ p + np.array([cx, cy, cz])
            return tuple(res)

        # 1. Main Blue Body (-11.4 to +11.4, -6.1 to +6.1, -11.25 to +11.25)
        b_pts = [
            (-11.4, -6.1, -11.25), (11.4, -6.1, -11.25), (11.4, 6.1, -11.25), (-11.4, 6.1, -11.25),
            (-11.4, -6.1, 11.25), (11.4, -6.1, 11.25), (11.4, 6.1, 11.25), (-11.4, 6.1, 11.25)
        ]
        t = [tf(p) for p in b_pts]
        self.add_quad(t[0], t[3], t[2], t[1])
        self.add_quad(t[4], t[5], t[6], t[7])
        self.add_quad(t[0], t[1], t[5], t[4])
        self.add_quad(t[2], t[3], t[7], t[6])
        self.add_quad(t[3], t[0], t[4], t[7])
        self.add_quad(t[1], t[2], t[6], t[5])

        # 2. Mounting Flange Ears (-16 to +16, -6 to +6, +6 to +8.5)
        e_pts = [
            (-16.0, -6.0, 6.0), (16.0, -6.0, 6.0), (16.0, 6.0, 6.0), (-16.0, 6.0, 6.0),
            (-16.0, -6.0, 8.5), (16.0, -6.0, 8.5), (16.0, 6.0, 8.5), (-16.0, 6.0, 8.5)
        ]
        et = [tf(p) for p in e_pts]
        self.add_quad(et[0], et[3], et[2], et[1])
        self.add_quad(et[4], et[5], et[6], et[7])
        self.add_quad(et[0], et[1], et[5], et[4])
        self.add_quad(et[2], et[3], et[7], et[6])
        self.add_quad(et[3], et[0], et[4], et[7])
        self.add_quad(et[1], et[2], et[6], et[5])

        # 3. Gear Tower & Spline Shaft (at local X = +5.5, Y = 0, Z = +11.25 to +16)
        p_t_bot = tf((5.5, 0, 11.25))
        p_t_top = tf((5.5, 0, 15.5))
        self.add_cylinder_orient(p_t_bot, p_t_top, 5.8, segments=16)

        # 4. White Horn Arm (extends in +X direction from spline)
        p_h_base = tf((5.5, 0, 16.5))
        p_h_tip = tf((18.5, 0, 16.5))
        self.add_cylinder_orient(p_h_base, p_h_tip, 2.8, segments=12)

    def add_spur_gear(self, cx, cy, cz, radius, thickness, num_teeth=12, tooth_h=2.2):
        # Precise Spur Gear with involute-like teeth
        z0, z1 = cz - thickness / 2.0, cz + thickness / 2.0
        steps = num_teeth * 4
        pts_2d = []
        for i in range(steps):
            angle = 2.0 * math.pi * i / steps
            # Tooth profile modulation
            t_wave = math.sin(i * 2.0 * math.pi / 4.0)
            r = radius + (tooth_h / 2.0) * t_wave
            pts_2d.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))

        n = len(pts_2d)
        for i in range(n):
            ni = (i + 1) % n
            p1 = (pts_2d[i][0], pts_2d[i][1], z0)
            p2 = (pts_2d[ni][0], pts_2d[ni][1], z0)
            p3 = (pts_2d[ni][0], pts_2d[ni][1], z1)
            p4 = (pts_2d[i][0], pts_2d[i][1], z1)
            self.add_quad(p1, p2, p3, p4)

        # Center caps
        c_b = (cx, cy, z0)
        c_t = (cx, cy, z1)
        for i in range(n):
            ni = (i + 1) % n
            self.add_triangle(c_b, (pts_2d[ni][0], pts_2d[ni][1], z0), (pts_2d[i][0], pts_2d[i][1], z0))
            self.add_triangle(c_t, (pts_2d[i][0], pts_2d[i][1], z1), (pts_2d[ni][0], pts_2d[ni][1], z1))

    def write_binary_stl(self, filepath, name="Model"):
        header = f"Tinkercad 3D: {name}".encode('ascii')[:80]
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
# REPRODUCE EXACT MAKERBUYING ARM (FROM IMAGES #1 - #5)
# =========================================================================
def build_exact_makerbuying_arm():
    mesh = STLMesh()

    # 1. BASE CYLINDRICAL HOUSING (The round white base tub)
    # Diameter: 56 mm, Height: 30 mm (Z: 0 to 30 mm)
    mesh.add_cylinder(0, 0, 0, 30, 28, 28, segments=36, cap_bottom=True, cap_top=True)
    # Cable outlet hole on the side (visible in Image #2)
    mesh.add_cylinder(27, 0, 8, 14, 4.0, 4.0, segments=16)
    # 3 Mounting tabs on the bottom rim (visible in Image #1, #2, #4)
    for a_deg in [0, 120, 240]:
        rad = math.radians(a_deg)
        tx = 31.0 * math.cos(rad)
        ty = 31.0 * math.sin(rad)
        mesh.add_cylinder(tx, ty, 0, 3, 4.5, 4.5, segments=16)
        mesh.add_cylinder(tx, ty, 0, 3.5, 1.8, 1.8, segments=12) # screw hole

    # SERVO 1: Base Yaw SG90 (hidden inside the base cylinder, shaft drives top disc)
    # We include it inside
    mesh.add_sg90_detail(0, 0, 15, rot_z=90)

    # 2. ROTATING TURNTABLE DISC WITH CLEVIS FORK (Piringan putar dengan braket garpu)
    # Turntable disc: Dia 56 mm, Z: 30 to 34 mm
    mesh.add_cylinder(0, 0, 30, 34, 28, 28, segments=36, cap_bottom=False, cap_top=True)

    # U-bracket Clevis Fork (garpu tegak penahan bahu di Z: 34 to 62 mm)
    # Left Ear: Y = -16 mm, Right Ear: Y = +16 mm
    mesh.add_box(0, -15.5, 48, 20, 4, 28)
    mesh.add_box(0, 15.5, 48, 20, 4, 28)
    # Pivot hole detail on ears
    mesh.add_cylinder(0, -15.5, 52, 52, 3.0, 3.0, segments=12)
    mesh.add_cylinder(0, 15.5, 52, 52, 3.0, 3.0, segments=12)

    # SERVO 2: SHOULDER SERVO SG90 (Mounted in the fork, shaft drives Link 1)
    # In Image #1, #2, #3, #4: Shoulder servo is mounted vertically inside the fork at Z = 48 mm
    mesh.add_sg90_detail(0, 0, 48, rot_x=0, rot_y=0, rot_z=0)

    # 3. LINK 1: LOWER ARM (Hollow Rectangular White Bracket holding Servo 3)
    # Pivot at (0, 0, 52), tilts forward-upward to Elbow pivot at (28, 0, 95)
    # In the photos (especially #1 and #3), Link 1 is a C-channel / box bracket holding Servo 3 right inside it!
    p_sh = np.array([0.0, 0.0, 52.0])
    p_el = np.array([28.0, 0.0, 95.0])
    v_link1 = p_el - p_sh
    l_link1 = np.linalg.norm(v_link1)

    # Lower arm side beams (2 beams sandwiching the shoulder horn)
    mesh.add_cylinder_orient((0, -12, 52), (28, -12, 95), 5.0, segments=16)
    mesh.add_cylinder_orient((0, 12, 52), (28, 12, 95), 5.0, segments=16)
    # Cross housing plates holding Servo 3
    mesh.add_box(14, 0, 73.5, 18, 22, 4)

    # SERVO 3: ELBOW SERVO SG90 (Embedded in the top of Link 1, shaft at Z = 95 mm)
    # In Image #1 & #3: Blue servo sitting in the elbow frame!
    mesh.add_sg90_detail(28, 0, 95, rot_x=0, rot_y=45, rot_z=0)

    # 4. LINK 2: UPPER FOREARM (Link connecting Elbow to Wrist Gripper Plate)
    # From Elbow (28, 0, 95) reaching forward to Wrist at (75, 0, 85)
    p_wr = np.array([75.0, 0.0, 85.0])
    mesh.add_cylinder_orient((28, 9, 95), (75, 9, 85), 4.5, segments=16)
    mesh.add_cylinder_orient((28, -9, 95), (75, -9, 85), 4.5, segments=16)
    # Horn boss detail on forearm (the white horn shape molded into the arm, clearly visible in Image #2 & #5!)
    mesh.add_box(40, 11, 93, 22, 3, 8)

    # 5. WRIST & GRIPPER CARRIER PLATE
    # Transverse plate at Z = 85 mm, holding Servo 4 vertically
    # As seen in Image #1: Front side has the blue SG90 servo body facing outward!
    mesh.add_box(78, 0, 85, 4, 34, 42)
    # Front servo mounting brackets
    mesh.add_box(84, -13, 85, 10, 4, 22)
    mesh.add_box(84, 13, 85, 10, 4, 22)

    # SERVO 4: GRIPPER SG90 (Mounted on the FRONT face of the gripper plate)
    # Body at X = 86, Y = 0, Z = 85 mm (blue body facing front!)
    mesh.add_sg90_detail(86, 0, 85, rot_x=90, rot_y=0, rot_z=0)

    # 6. DUAL MESHING SPUR GEARS ON THE BACK (Visible in Image #2!)
    # On the rear/underside of the plate (X = 74 mm):
    # Two intermeshing white spur gears:
    # Gear 1 (Upper Jaw Gear): at Y = -9 mm, Z = 85 mm, Radius = 9.5 mm
    # Gear 2 (Lower Jaw Gear): at Y = +9 mm, Z = 85 mm, Radius = 9.5 mm
    # Jarak pusat gear = 18.0 mm -> Radius 9.0 mm (Saling mengunci sempurna!)
    mesh.add_spur_gear(75, -9, 85, radius=9.0, thickness=3.5, num_teeth=14, tooth_h=2.0)
    mesh.add_spur_gear(75, 9, 85, radius=9.0, thickness=3.5, num_teeth=14, tooth_h=2.0)

    # Pivot Screws / Horn screw connecting Gear 1 to Servo 4 shaft
    mesh.add_cylinder(73, -9, 85, 85, 1.8, 1.8, segments=12)
    mesh.add_cylinder(73, 9, 85, 85, 1.8, 1.8, segments=12)
    # Servo horn cross bar on Gear 1 (visible in Image #2 screwed to the jaw!)
    mesh.add_box(73.5, -9, 85, 1.5, 15, 4)

    # 7. SERRATED CLAWS / PINCERS (Persis bentuk capit di foto #1, #2, #4!)
    # Claw 1 (Upper / Left Pincer): Melengkung ke luar lalu mencengkeram ke dalam, ujung bergerigi
    c1_pts = [
        (75, -9, 85),
        (92, -18, 85),
        (108, -16, 85),
        (116, -6, 85) # Tip
    ]
    mesh.add_cylinder_orient(c1_pts[0], c1_pts[1], 4.0, segments=12)
    mesh.add_cylinder_orient(c1_pts[1], c1_pts[2], 3.8, segments=12)
    mesh.add_cylinder_orient(c1_pts[2], c1_pts[3], 3.2, segments=12)
    # Serrated teeth on inner face of Claw 1 (3 gigi cengkeram)
    for tx in [102, 108, 114]:
        mesh.add_box(tx, -11, 85, 2.5, 2.5, 7)

    # Claw 2 (Lower / Right Pincer): Simetris persis
    c2_pts = [
        (75, 9, 85),
        (92, 18, 85),
        (108, 16, 85),
        (116, 6, 85)  # Tip
    ]
    mesh.add_cylinder_orient(c2_pts[0], c2_pts[1], 4.0, segments=12)
    mesh.add_cylinder_orient(c2_pts[1], c2_pts[2], 3.8, segments=12)
    mesh.add_cylinder_orient(c2_pts[2], c2_pts[3], 3.2, segments=12)
    # Serrated teeth on inner face of Claw 2
    for tx in [102, 108, 114]:
        mesh.add_box(tx, 11, 85, 2.5, 2.5, 7)

    # 8. CABLE HARNESS SIMULATION (Kabel pita 3-warna yang rapi di foto)
    # Routing along the back of the arm
    mesh.add_cylinder_orient((78, -13, 85), (28, -12, 95), 1.2, segments=8)
    mesh.add_cylinder_orient((28, -12, 95), (0, -12, 52), 1.5, segments=8)
    mesh.add_cylinder_orient((0, -12, 52), (22, 0, 12), 2.0, segments=8)

    return mesh


# =========================================================================
# STANDALONE GEARED GRIPPER MECHANISM (CLOSE-UP FROM PHOTO #2)
# =========================================================================
def build_exact_geared_gripper_standalone():
    mesh = STLMesh()

    # Front Mount Plate
    mesh.add_box(0, 0, 0, 4, 34, 42)
    # Front Servo SG90 Body
    mesh.add_sg90_detail(8, 0, 0, rot_x=90, rot_y=0, rot_z=0)

    # Two intermeshing gears on the back
    mesh.add_spur_gear(-3, -9, 0, radius=9.0, thickness=3.5, num_teeth=14, tooth_h=2.0)
    mesh.add_spur_gear(-3, 9, 0, radius=9.0, thickness=3.5, num_teeth=14, tooth_h=2.0)

    # Horn on Upper Gear
    mesh.add_box(-4.5, -9, 0, 1.5, 15, 4)

    # Symmetrical claws with serrated teeth
    # Claw 1
    c1_pts = [(0, -9, 0), (18, -18, 0), (34, -16, 0), (42, -6, 0)]
    mesh.add_cylinder_orient(c1_pts[0], c1_pts[1], 4.0, segments=12)
    mesh.add_cylinder_orient(c1_pts[1], c1_pts[2], 3.8, segments=12)
    mesh.add_cylinder_orient(c1_pts[2], c1_pts[3], 3.2, segments=12)
    for tx in [28, 34, 40]:
        mesh.add_box(tx, -11, 0, 2.5, 2.5, 7)

    # Claw 2
    c2_pts = [(0, 9, 0), (18, 18, 0), (34, 16, 0), (42, 6, 0)]
    mesh.add_cylinder_orient(c2_pts[0], c2_pts[1], 4.0, segments=12)
    mesh.add_cylinder_orient(c2_pts[1], c2_pts[2], 3.8, segments=12)
    mesh.add_cylinder_orient(c2_pts[2], c2_pts[3], 3.2, segments=12)
    for tx in [28, 34, 40]:
        mesh.add_box(tx, 11, 0, 2.5, 2.5, 7)

    return mesh


# =========================================================================
# FULL INTEGRATED SCENE: EXACT MAKERBUYING ARM + CONVEYOR + RED BOX
# =========================================================================
def build_conveyor_scene_with_exact_arm():
    mesh = STLMesh()

    # The exact MakerBuying arm
    arm = build_exact_makerbuying_arm()
    mesh.triangles.extend(arm.triangles)

    # Conveyor Bed from Manuel's Tinkercad project
    # Arm base is at (0, 0, 0), claws reach to X ~ 116 mm.
    # Conveyor runs along Y, positioned at X = 115 mm!
    cx = 115.0
    mesh.add_box(cx, 0, 24, 50, 160, 4)      # Belt surface at Z = 24 mm
    mesh.add_box(cx - 25, 0, 16, 3, 160, 20)  # Left rail
    mesh.add_box(cx + 25, 0, 16, 3, 160, 20)  # Right rail
    mesh.add_cylinder(cx, -80, 12, 12, 10, 10, segments=20)
    mesh.add_cylinder(cx, 80, 12, 12, 10, 10, segments=20)
    # Yellow DC TT Motor on conveyor side
    mesh.add_box(cx + 35, 70, 14, 18, 24, 18)

    # Red Box (Workpiece from Manuel's Tinkercad) being gripped right above the belt
    # Size 18 x 18 x 18 mm at (X = 114, Y = 0, Z = 85 mm in air, or at Z = 34 mm on belt)
    mesh.add_box(cx, 0, 85, 18, 18, 18)

    # Silo / Chamber at the end of the conveyor (Y = 80 to 140)
    mesh.add_box(cx, 110, 50, 60, 50, 96)
    # Ultrasonic sensor eyes
    mesh.add_cylinder(cx - 10, 84, 60, 60, 6, 6, segments=16)
    mesh.add_cylinder(cx + 10, 84, 60, 60, 6, 6, segments=16)

    return mesh


# =========================================================================
# MAIN EXECUTION
# =========================================================================
def main():
    target_dir = os.path.abspath("desain_arm_makerbuying_real")
    os.makedirs(target_dir, exist_ok=True)
    
    repo_target = os.path.abspath("TugasBesarIOT_SiloMonitoringSystem/desain_arm_makerbuying_real")
    os.makedirs(repo_target, exist_ok=True)

    print("Generating EXACT MakerBuying 4-DOF Robotic Arm (from Images #1-#5)...")

    # 1. Full Assembled Arm
    arm = build_exact_makerbuying_arm()
    arm.write_binary_stl(os.path.join(target_dir, "arm_makerbuying_sg90_assembly.stl"), "MakerBuying Arm SG90")
    arm.write_obj(os.path.join(target_dir, "arm_makerbuying_sg90_assembly.obj"))

    # 2. Standalone Gripper Module with Dual Gears
    gripper = build_exact_geared_gripper_standalone()
    gripper.write_binary_stl(os.path.join(target_dir, "gripper_dual_gear_sg90.stl"), "Dual Gear Gripper")
    gripper.write_obj(os.path.join(target_dir, "gripper_dual_gear_sg90.obj"))

    # 3. Full Integrated Scene with Conveyor
    scene = build_conveyor_scene_with_exact_arm()
    scene.write_binary_stl(os.path.join(target_dir, "scene_conveyor_makerbuying_arm.stl"), "Conveyor With MakerBuying Arm")
    scene.write_obj(os.path.join(target_dir, "scene_conveyor_makerbuying_arm.obj"))

    # 4. Render High-Resolution 3D Visual Previews
    print("Rendering 3D preview comparisons...")
    fig = plt.figure(figsize=(14, 7), facecolor='#0F172A')

    # View 1: Isometric View of Arm
    ax1 = fig.add_subplot(121, projection='3d', facecolor='#0F172A')
    step = max(1, len(arm.triangles) // 2500)
    t1 = [[t[1], t[2], t[3]] for i, t in enumerate(arm.triangles) if i % step == 0]
    m1 = Poly3DCollection(t1, facecolors='#F8FAFC', edgecolors='#0284C7', linewidths=0.25, alpha=0.92)
    ax1.add_collection3d(m1)
    ax1.set_xlim(-40, 130)
    ax1.set_ylim(-50, 50)
    ax1.set_zlim(0, 120)
    ax1.view_init(elev=24, azim=-50)
    ax1.set_title('MODEL 3D PERSIS FOTO: MAKERBUYING 4-DOF ARM SG90\n(Base Drum + Fork Bahu + Siku + Geared Gripper Depan)', color='#F8FAFC', fontsize=10, weight='bold')
    ax1.tick_params(colors='#64748B')

    # View 2: Close-up of Dual Geared Gripper (Matching Photo #2)
    ax2 = fig.add_subplot(122, projection='3d', facecolor='#0F172A')
    t2 = [[t[1], t[2], t[3]] for t in gripper.triangles]
    m2 = Poly3DCollection(t2, facecolors='#F8FAFC', edgecolors='#38BDF8', linewidths=0.3, alpha=0.95)
    ax2.add_collection3d(m2)
    ax2.set_xlim(-15, 50)
    ax2.set_ylim(-30, 30)
    ax2.set_zlim(-25, 25)
    ax2.view_init(elev=35, azim=-140)  # Rear view showing the intermeshing gears!
    ax2.set_title('TAMPAK BELAKANG CAPIT (PERSIS FOTO #2):\nDUAL GEAR SPUR SALING MENGAIT DIKENDALIKAN 1 SERVO SG90', color='#F8FAFC', fontsize=10, weight='bold')
    ax2.tick_params(colors='#64748B')

    plt.tight_layout()
    preview_img = os.path.join(target_dir, "preview_exact_makerbuying_arm.png")
    plt.savefig(preview_img, dpi=200, facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved render preview: {preview_img}")

    # Copy all to repo
    import shutil
    for f in os.listdir(target_dir):
        src = os.path.join(target_dir, f)
        dst = os.path.join(repo_target, f)
        if os.path.isfile(src):
            shutil.copy2(src, dst)

    print(f"\nAll files successfully generated in:\n  - {target_dir}\n  - {repo_target}")

if __name__ == "__main__":
    main()
