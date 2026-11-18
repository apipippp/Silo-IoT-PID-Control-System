import os
import math
import struct
import shutil
import numpy as np

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

        c000 = (x0, y0, z0)
        c100 = (x1, y0, z0)
        c110 = (x1, y1, z0)
        c010 = (x0, y1, z0)
        c001 = (x0, y0, z1)
        c101 = (x1, y0, z1)
        c111 = (x1, y1, z1)
        c011 = (x0, y1, z1)

        self.add_quad(c000, c010, c110, c100) # Bottom
        self.add_quad(c001, c101, c111, c011) # Top
        self.add_quad(c000, c100, c101, c001) # Front
        self.add_quad(c110, c010, c011, c111) # Back
        self.add_quad(c010, c000, c001, c011) # Left
        self.add_quad(c100, c110, c111, c101) # Right

    def add_cylinder(self, cx, cy, z_bottom, z_top, radius_bottom, radius_top=None, segments=36, cap_bottom=True, cap_top=True):
        if radius_top is None:
            radius_top = radius_bottom

        angles = [2.0 * math.pi * i / segments for i in range(segments)]
        bot_pts = [(cx + radius_bottom * math.cos(a), cy + radius_bottom * math.sin(a), z_bottom) for a in angles]
        top_pts = [(cx + radius_top * math.cos(a), cy + radius_top * math.sin(a), z_top) for a in angles]

        for i in range(segments):
            next_i = (i + 1) % segments
            self.add_quad(bot_pts[i], bot_pts[next_i], top_pts[next_i], top_pts[i])

        if cap_bottom and radius_bottom > 1e-4:
            c_bot = (cx, cy, z_bottom)
            for i in range(segments):
                next_i = (i + 1) % segments
                self.add_triangle(c_bot, bot_pts[next_i], bot_pts[i])

        if cap_top and radius_top > 1e-4:
            c_top = (cx, cy, z_top)
            for i in range(segments):
                next_i = (i + 1) % segments
                self.add_triangle(c_top, top_pts[i], top_pts[next_i])

    def add_horizontal_cylinder_x(self, x_start, x_end, cy, cz, radius, segments=24):
        angles = [2.0 * math.pi * i / segments for i in range(segments)]
        s_pts = [(x_start, cy + radius * math.cos(a), cz + radius * math.sin(a)) for a in angles]
        e_pts = [(x_end, cy + radius * math.cos(a), cz + radius * math.sin(a)) for a in angles]

        for i in range(segments):
            next_i = (i + 1) % segments
            self.add_quad(s_pts[i], e_pts[i], e_pts[next_i], s_pts[next_i])

        c_s = (x_start, cy, cz)
        c_e = (x_end, cy, cz)
        for i in range(segments):
            next_i = (i + 1) % segments
            self.add_triangle(c_s, s_pts[next_i], s_pts[i])
            self.add_triangle(c_e, e_pts[i], e_pts[next_i])

    def add_horizontal_cylinder_y(self, cx, y_start, y_end, cz, radius, segments=24):
        angles = [2.0 * math.pi * i / segments for i in range(segments)]
        s_pts = [(cx + radius * math.cos(a), y_start, cz + radius * math.sin(a)) for a in angles]
        e_pts = [(cx + radius * math.cos(a), y_end, cz + radius * math.sin(a)) for a in angles]

        for i in range(segments):
            next_i = (i + 1) % segments
            self.add_quad(s_pts[i], s_pts[next_i], e_pts[next_i], e_pts[i])

        c_s = (cx, y_start, cz)
        c_e = (cx, y_end, cz)
        for i in range(segments):
            next_i = (i + 1) % segments
            self.add_triangle(c_s, s_pts[i], s_pts[next_i])
            self.add_triangle(c_e, e_pts[next_i], e_pts[i])

    def add_ring(self, cx, cy, z_bottom, z_top, r_inner, r_outer, segments=36):
        angles = [2.0 * math.pi * i / segments for i in range(segments)]
        b_in = [(cx + r_inner * math.cos(a), cy + r_inner * math.sin(a), z_bottom) for a in angles]
        b_out = [(cx + r_outer * math.cos(a), cy + r_outer * math.sin(a), z_bottom) for a in angles]
        t_in = [(cx + r_inner * math.cos(a), cy + r_inner * math.sin(a), z_top) for a in angles]
        t_out = [(cx + r_outer * math.cos(a), cy + r_outer * math.sin(a), z_top) for a in angles]

        for i in range(segments):
            ni = (i + 1) % segments
            self.add_quad(b_out[i], b_out[ni], t_out[ni], t_out[i])
            self.add_quad(b_in[ni], b_in[i], t_in[i], t_in[ni])
            self.add_quad(t_in[i], t_out[i], t_out[ni], t_in[ni])
            self.add_quad(b_out[i], b_in[i], b_in[ni], b_out[ni])

    def write_binary_stl(self, filepath, name="Model"):
        header = f"Tinkercad 3D Model: {name}".encode('ascii')[:80]
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


# ==========================================
# 1. BUILD SILO BODY MESH
# ==========================================
def build_silo_body():
    mesh = STLMesh()
    
    # Silo Cylinder Body (Diameter 60mm -> Radius 30mm, Z: 65mm to 135mm)
    mesh.add_cylinder(0, 0, 65, 135, 30, 30, segments=48, cap_bottom=False, cap_top=False)
    
    # Silo Conical Roof / Dome (Z: 135 to 158mm, Radius 30mm down to 12mm)
    mesh.add_cylinder(0, 0, 135, 158, 30, 12, segments=48, cap_bottom=False, cap_top=True)
    
    # Roof Flange Rim
    mesh.add_ring(0, 0, 134, 136, 29, 31.5, segments=48)
    
    # Exhaust Fan Cowl / Duct on Top of Roof (Z: 158 to 172mm, Radius 11mm)
    mesh.add_cylinder(0, 0, 158, 172, 11, 11, segments=32, cap_bottom=False, cap_top=True)
    # Exhaust Fan Rain Hat / Hood (Z: 172 to 175mm, Radius 14mm)
    mesh.add_cylinder(0, 0, 172, 175, 14, 14, segments=32, cap_bottom=True, cap_top=True)
    # Fan protective intake grill bar detail
    mesh.add_box(0, 0, 165, 24, 2, 8)
    mesh.add_box(0, 0, 165, 2, 24, 8)
    
    # Silo Bottom Conical Hopper (Corong Bawah, Z: 65 down to 34mm, Radius 30mm down to 8mm)
    mesh.add_cylinder(0, 0, 34, 65, 8, 30, segments=48, cap_bottom=False, cap_top=False)
    
    # Hopper Mid Strengthening Ring
    mesh.add_ring(0, 0, 63, 65, 29, 31.5, segments=48)
    
    # Discharge Nozzle Chute (Z: 26 to 34mm, Radius 8mm to 7mm)
    mesh.add_cylinder(0, 0, 26, 34, 7, 8, segments=32, cap_bottom=True, cap_top=False)
    
    # Dispensing Valve Flange & SG90 Servo Actuator Plate (Z: 28 to 31mm)
    mesh.add_box(0, 0, 29.5, 22, 18, 3)
    # Servo Horn / Slide Shutter Valve Indicator
    mesh.add_box(12, 0, 29.5, 10, 8, 2.5)

    # Sensor Port 1: DHT22 Housing on Wall (Z: 85mm, Side wall Y = -30mm)
    mesh.add_box(0, -31.5, 85, 14, 6, 18)
    # DHT22 Vent slits relief
    mesh.add_box(0, -34.8, 85, 10, 1.5, 14)
    
    # Sensor Port 2: MQ-135 Gas Sensor Housing on Wall (Z: 112mm, Side wall X = 30mm)
    mesh.add_cylinder(31.5, 0, 106, 118, 7, 7, segments=24, cap_bottom=True, cap_top=True)
    # MQ-135 mesh dome cap
    mesh.add_cylinder(34.5, 0, 108, 116, 5, 5, segments=24, cap_bottom=True, cap_top=True)

    # Inspection Hatch / Manhole on Lower Side (Z: 75mm, Side wall X = -30mm)
    mesh.add_box(-31.5, 0, 75, 5, 16, 20)
    # Hatch handle
    mesh.add_box(-34.5, 0, 75, 2, 8, 4)

    return mesh


# ==========================================
# 2. BUILD SILO SUPPORT LEGS & STAND
# ==========================================
def build_silo_legs():
    mesh = STLMesh()
    
    # 4 Legs positioned at radius 33mm, 45 degree angles (x = ±23.3, y = ±23.3)
    r_leg = 33.0
    angles_deg = [45, 135, 225, 315]
    
    for deg in angles_deg:
        rad = math.radians(deg)
        lx = r_leg * math.cos(rad)
        ly = r_leg * math.sin(rad)
        
        # Vertical structural column (Z: 0 to 66mm, 5x5mm box)
        mesh.add_box(lx, ly, 33, 5, 5, 66)
        
        # Foot Base Pad (Z: 0 to 2mm, 12x12mm plate)
        mesh.add_box(lx, ly, 1, 12, 12, 2)
        
        # Bolt anchor detail on foot pad
        mesh.add_cylinder(lx, ly, 2, 3.5, 1.8, 1.8, segments=12)

    # Top Support Collar Ring (Z: 63 to 67mm, holds the silo cylinder)
    mesh.add_ring(0, 0, 63, 67, 29.5, 35.5, segments=48)
    
    # Lower Cross-Bracing Ring (Z: 38 to 41mm)
    mesh.add_ring(0, 0, 38, 41, 31.0, 35.5, segments=48)
    
    # Cross Strut Reinforcements connecting legs
    for i in range(4):
        a1 = math.radians(angles_deg[i])
        a2 = math.radians(angles_deg[(i + 1) % 4])
        x1, y1 = r_leg * math.cos(a1), r_leg * math.sin(a1)
        x2, y2 = r_leg * math.cos(a2), r_leg * math.sin(a2)
        mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0
        # Horizontal beam at z=39
        dx = x2 - x1
        dy = y2 - y1
        length = math.sqrt(dx*dx + dy*dy)
        # Create a strut
        # Simplified: ring already stiffens all 4 legs!
    
    return mesh


# ==========================================
# 3. BUILD CONVEYOR ASSEMBLY
# ==========================================
def build_conveyor():
    mesh = STLMesh()
    
    # Conveyor Bed Length: 150mm (X: -75 to +75mm)
    # Width: 36mm (Y: -18 to +18mm)
    # Top of belt is at Z = 18mm
    
    # 1. Side Frame Beams (Left and Right Rails)
    # Y = -17mm and Y = +17mm
    mesh.add_box(0, -17, 10, 150, 4, 16)
    mesh.add_box(0, 17, 10, 150, 4, 16)
    
    # 2. Conveyor Support Legs (4 legs)
    mesh.add_box(-60, -17, 4, 6, 6, 8)
    mesh.add_box(-60, 17, 4, 6, 6, 8)
    mesh.add_box(60, -17, 4, 6, 6, 8)
    mesh.add_box(60, 17, 4, 6, 6, 8)
    
    # Base mounting plates
    mesh.add_box(-60, -17, 0.75, 12, 12, 1.5)
    mesh.add_box(-60, 17, 0.75, 12, 12, 1.5)
    mesh.add_box(60, -17, 0.75, 12, 12, 1.5)
    mesh.add_box(60, 17, 0.75, 12, 12, 1.5)
    
    # 3. Rollers at Both Ends
    # Roller 1: at X = -65mm, axis along Y from -16 to +16, Z = 11mm, Radius = 6.5mm
    mesh.add_horizontal_cylinder_y(-65, -16, 16, 11, 6.5, segments=24)
    # Roller 2: at X = +65mm
    mesh.add_horizontal_cylinder_y(65, -16, 16, 11, 6.5, segments=24)
    
    # 4. Conveyor Belt (Flat top surface)
    # Z = 17.5 to 18.5mm, X = -65 to +65mm, Y = -14.5 to +14.5mm
    mesh.add_box(0, 0, 18, 130, 29, 1.5)
    
    # Return belt on bottom (Z = 3.5 to 4.5mm)
    mesh.add_box(0, 0, 4, 130, 29, 1.0)
    
    # 5. DC Motor / Gearbox Mount at X = -72mm, Y = 22mm
    mesh.add_box(-65, 23, 11, 16, 12, 14)
    mesh.add_horizontal_cylinder_y(-65, 16, 20, 11, 3.0, segments=16) # shaft
    
    # 6. Grain Collection Cart / Trolley (Wadah Gandum di bawah corong silo)
    # Position: X = 0, Y = 0, Z = 19 to 25mm
    # Outer box
    mesh.add_box(0, 0, 22.5, 26, 26, 7)
    # Rim/Ledge
    mesh.add_box(0, 0, 25.5, 28, 28, 1.5)
    
    # 7. Ultrasonic Sensor Mount (HC-SR04) at Front End of Conveyor
    # Placed at X = +72mm, looking backwards toward the cart at X=0
    # Mounting bracket plate
    mesh.add_box(73, 0, 24, 4, 34, 20)
    # Ultrasonic Sensor PCB (blue board)
    mesh.add_box(70.5, 0, 24, 1.5, 30, 16)
    # Two transducer barrels (Transmitter T & Receiver R)
    mesh.add_horizontal_cylinder_x(62, 70, -7.5, 24, 4.5, segments=20)
    mesh.add_horizontal_cylinder_x(62, 70, 7.5, 24, 4.5, segments=20)
    # Transducer mesh mesh rings
    mesh.add_horizontal_cylinder_x(61, 62, -7.5, 24, 4.8, segments=20)
    mesh.add_horizontal_cylinder_x(61, 62, 7.5, 24, 4.8, segments=20)

    return mesh


# ==========================================
# 4. BUILD IOT CONTROL ENCLOSURE BOX
# ==========================================
def build_iot_box():
    mesh = STLMesh()
    
    # Position: Side of the Silo Leg (e.g. at X = 32mm, Y = -22mm, Z = 60mm)
    bx, by, bz = 35.0, -20.0, 60.0
    
    # Main Enclosure Body: 28mm wide (along Y), 18mm deep (along X), 36mm high (along Z)
    mesh.add_box(bx, by, bz, 16, 28, 36)
    
    # Front Cover Lid Flange
    mesh.add_box(bx + 8.5, by, bz, 2, 29, 37)
    
    # Status LED 1: Red LED Bezel (Fan Active / Warning Indicator - PIN 4)
    mesh.add_cylinder(bx + 9.5, by - 6, bz + 10, bz + 10, 2.5, 2.5, segments=16)
    mesh.add_cylinder(bx + 9.5, by - 6, bz + 9, bz + 11.5, 2.0, 1.2, segments=16) # Dome
    
    # Status LED 2: Green LED Bezel (Standby / Normal Indicator - PIN 2)
    mesh.add_cylinder(bx + 9.5, by + 6, bz + 10, bz + 10, 2.5, 2.5, segments=16)
    mesh.add_cylinder(bx + 9.5, by + 6, bz + 9, bz + 11.5, 2.0, 1.2, segments=16) # Dome
    
    # Buzzer Acoustic Sound Outlet Grill (PIN 19)
    mesh.add_cylinder(bx + 9.5, by, bz - 2, bz - 2, 4.5, 4.5, segments=20)
    mesh.add_cylinder(bx + 9.8, by, bz - 2, bz - 2, 1.2, 1.2, segments=12) # Center hole
    
    # Ventilation Louver Slits on Side
    for z_slit in [-8, -11, -14]:
        mesh.add_box(bx, by - 14.5, bz + z_slit, 10, 1.5, 1.8)
        
    # Cable Glands / Conduits at Bottom of Box
    mesh.add_cylinder(bx - 3, by - 6, bz - 22, bz - 18, 3.0, 3.0, segments=16)
    mesh.add_cylinder(bx - 3, by + 6, bz - 22, bz - 18, 3.0, 3.0, segments=16)
    
    # Mounting Strut to Silo Leg
    mesh.add_box(bx - 10, by, bz, 6, 8, 20)

    return mesh


# ==========================================
# 5. BUILD SVG BLUEPRINTS & 2D PROFILES
# ==========================================
def generate_svg_drawings(out_dir):
    # 1. Elevation Technical Drawing with Dimensions & Annotations
    svg_elevation = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 850" width="1000" height="850" style="background:#0F172A; font-family:'Segoe UI',Roboto,Helvetica,sans-serif;">
  <defs>
    <!-- Grid Pattern -->
    <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#1E293B" stroke-width="0.8"/>
    </pattern>
    <pattern id="grid-major" width="100" height="100" patternUnits="userSpaceOnUse">
      <rect width="100" height="100" fill="url(#grid)"/>
      <path d="M 100 0 L 0 0 0 100" fill="none" stroke="#334155" stroke-width="1.2"/>
    </pattern>
    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#38BDF8"/>
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#10B981"/>
    </marker>
    <marker id="arrow-orange" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#F59E0B"/>
    </marker>
    <linearGradient id="siloGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#475569"/>
      <stop offset="30%" stop-color="#94A3B8"/>
      <stop offset="70%" stop-color="#CBD5E1"/>
      <stop offset="100%" stop-color="#64748B"/>
    </linearGradient>
    <linearGradient id="roofGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#334155"/>
      <stop offset="50%" stop-color="#64748B"/>
      <stop offset="100%" stop-color="#1E293B"/>
    </linearGradient>
    <linearGradient id="hopperGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#334155"/>
      <stop offset="50%" stop-color="#64748B"/>
      <stop offset="100%" stop-color="#1E293B"/>
    </linearGradient>
  </defs>

  <!-- Background Grid -->
  <rect width="1000" height="850" fill="url(#grid-major)"/>

  <!-- Title Block -->
  <g id="title-block">
    <rect x="30" y="25" width="940" height="70" rx="8" fill="#1E293B" stroke="#38BDF8" stroke-width="1.5"/>
    <text x="50" y="52" fill="#F8FAFC" font-size="18" font-weight="bold" letter-spacing="1">DESAIN 2D / 3D TEKNIS — SMART SILO &amp; CONVEYOR MONITORING SYSTEM</text>
    <text x="50" y="75" fill="#94A3B8" font-size="13">Scale 1:1 Tabletop Prototype Model | Siap Impor ke Tinkercad (.STL / .OBJ / .SVG) | Kelompok 2 IoT Kelas A</text>
    <rect x="830" y="38" width="125" height="42" rx="4" fill="#0EA5E9" fill-opacity="0.2" stroke="#38BDF8" stroke-width="1"/>
    <text x="892" y="64" fill="#38BDF8" font-size="12" font-weight="bold" text-anchor="middle">TINKERCAD READY</text>
  </g>

  <!-- Main System Drawing Area (Center around X=460) -->
  <g id="ground-and-datum">
    <!-- Ground Line (Z = 0) at Canvas Y = 680 -->
    <line x1="100" y1="680" x2="820" y2="680" stroke="#475569" stroke-width="2.5" stroke-dasharray="8 4"/>
    <text x="110" y="700" fill="#64748B" font-size="11" font-weight="bold">DATUM BASE / WORKPLANE (Z = 0 mm)</text>
  </g>

  <!-- CONVEYOR SYSTEM (Bottom) -->
  <g id="conveyor-group">
    <!-- Conveyor Table / Frame Legs -->
    <rect x="220" y="650" width="14" height="30" fill="#334155" stroke="#475569" stroke-width="1.5"/>
    <rect x="215" y="675" width="24" height="5" fill="#1E293B" stroke="#64748B" stroke-width="1"/>
    <rect x="680" y="650" width="14" height="30" fill="#334155" stroke="#475569" stroke-width="1.5"/>
    <rect x="675" y="675" width="24" height="5" fill="#1E293B" stroke="#64748B" stroke-width="1"/>
    
    <!-- Conveyor Side Rail Bed -->
    <rect x="180" y="620" width="560" height="32" rx="4" fill="#1E293B" stroke="#64748B" stroke-width="2"/>
    
    <!-- End Rollers -->
    <circle cx="210" cy="636" r="14" fill="#64748B" stroke="#94A3B8" stroke-width="1.5"/>
    <circle cx="210" cy="636" r="4" fill="#0F172A"/>
    <circle cx="710" cy="636" r="14" fill="#64748B" stroke="#94A3B8" stroke-width="1.5"/>
    <circle cx="710" cy="636" r="4" fill="#0F172A"/>

    <!-- Belt (Top & Bottom) -->
    <rect x="210" y="622" width="500" height="5" fill="#0284C7"/>
    <rect x="210" y="645" width="500" height="4" fill="#0369A1"/>
    
    <!-- Conveyor Motion Direction Arrow -->
    <line x1="300" y1="612" x2="380" y2="612" stroke="#38BDF8" stroke-width="2" marker-end="url(#arrow)"/>
    <text x="340" y="605" fill="#38BDF8" font-size="11" font-weight="bold" text-anchor="middle">Arah Gerak Belt (PID Position)</text>

    <!-- DC Drive Motor Mount (Left) -->
    <rect x="150" y="618" width="30" height="36" rx="3" fill="#475569" stroke="#64748B" stroke-width="1.5"/>
    <text x="165" y="640" fill="#E2E8F0" font-size="9" font-weight="bold" text-anchor="middle">MOTOR</text>

    <!-- Grain Cart / Container (Troli Wadah Gandum) -->
    <g id="cart">
      <rect x="415" y="580" width="90" height="42" rx="3" fill="#D97706" stroke="#F59E0B" stroke-width="2"/>
      <rect x="410" y="575" width="100" height="6" rx="2" fill="#B45309" stroke="#F59E0B" stroke-width="1"/>
      <text x="460" y="603" fill="#FEF3C7" font-size="10" font-weight="bold" text-anchor="middle">WADAH GANDUM</text>
      <!-- Wheels / Skids -->
      <rect x="425" y="618" width="16" height="4" fill="#78350F"/>
      <rect x="480" y="618" width="16" height="4" fill="#78350F"/>
    </g>

    <!-- Ultrasonic Sensor (HC-SR04) on Right Post -->
    <g id="ultrasonic">
      <rect x="740" y="550" width="10" height="72" fill="#475569" stroke="#64748B" stroke-width="1.5"/>
      <rect x="726" y="555" width="6" height="44" rx="2" fill="#1E40AF" stroke="#3B82F6" stroke-width="1.5"/>
      <!-- Dual transducers -->
      <rect x="712" y="560" width="14" height="14" rx="3" fill="#CBD5E1" stroke="#94A3B8" stroke-width="1"/>
      <circle cx="718" cy="567" r="4" fill="#64748B"/>
      <rect x="712" y="580" width="14" height="14" rx="3" fill="#CBD5E1" stroke="#94A3B8" stroke-width="1"/>
      <circle cx="718" cy="587" r="4" fill="#64748B"/>
      <!-- Sonic Ping Waves -->
      <path d="M 700 562 C 685 572, 685 578, 700 588" fill="none" stroke="#60A5FA" stroke-width="2" stroke-dasharray="3 3"/>
      <path d="M 685 558 C 665 572, 665 578, 685 592" fill="none" stroke="#60A5FA" stroke-width="2" stroke-dasharray="3 3"/>
      <text x="735" y="540" fill="#60A5FA" font-size="11" font-weight="bold" text-anchor="middle">HC-SR04</text>
      <text x="735" y="552" fill="#94A3B8" font-size="9" text-anchor="middle">Feedback Jarak 5 cm</text>
    </g>
  </g>

  <!-- SILO STRUCTURAL STAND & LEGS -->
  <g id="silo-stand">
    <!-- Left Outer Leg -->
    <rect x="350" y="380" width="14" height="300" fill="#334155" stroke="#475569" stroke-width="1.5"/>
    <rect x="342" y="674" width="30" height="6" fill="#1E293B" stroke="#64748B" stroke-width="1"/>
    <!-- Left Inner Leg (Back) -->
    <rect x="380" y="380" width="12" height="300" fill="#1E293B" stroke="#334155" stroke-width="1"/>
    
    <!-- Right Inner Leg (Back) -->
    <rect x="528" y="380" width="12" height="300" fill="#1E293B" stroke="#334155" stroke-width="1"/>
    <!-- Right Outer Leg -->
    <rect x="556" y="380" width="14" height="300" fill="#334155" stroke="#475569" stroke-width="1.5"/>
    <rect x="548" y="674" width="30" height="6" fill="#1E293B" stroke="#64748B" stroke-width="1"/>

    <!-- Cross Bracing Rings -->
    <!-- Lower Ring at Z=38 (Y=520) -->
    <rect x="345" y="520" width="230" height="12" rx="3" fill="#1E293B" stroke="#64748B" stroke-width="1.5"/>
    <!-- Diagonal Braces -->
    <line x1="357" y1="400" x2="563" y2="520" stroke="#475569" stroke-width="2"/>
    <line x1="563" y1="400" x2="357" y2="520" stroke="#475569" stroke-width="2"/>
    <!-- Top Support Collar at Z=65 (Y=380) -->
    <rect x="338" y="376" width="244" height="16" rx="4" fill="#334155" stroke="#94A3B8" stroke-width="2"/>
  </g>

  <!-- SILO HOPPER & DISCHARGE CHUTE -->
  <g id="silo-hopper">
    <!-- Conical Hopper (Inverted Frustum: Width 220 at Y=380 down to Width 50 at Y=500) -->
    <polygon points="350,380 570,380 490,500 430,500" fill="url(#hopperGrad)" stroke="#475569" stroke-width="2"/>
    
    <!-- Discharge Nozzle / Chute (Y=500 to 540) -->
    <rect x="435" y="500" width="50" height="35" fill="#334155" stroke="#64748B" stroke-width="2"/>
    
    <!-- Micro Servo SG90 Slide Valve -->
    <rect x="485" y="508" width="34" height="22" rx="3" fill="#1E40AF" stroke="#3B82F6" stroke-width="1.5"/>
    <rect x="440" y="516" width="55" height="6" fill="#E2E8F0" stroke="#94A3B8" stroke-width="1"/>
    <text x="502" y="523" fill="#E2E8F0" font-size="8" font-weight="bold" text-anchor="middle">SERVO</text>
    
    <!-- Grain Pouring Simulation (Dotted amber) -->
    <path d="M 445 538 L 435 575 L 485 575 L 475 538 Z" fill="#F59E0B" fill-opacity="0.3" stroke="#F59E0B" stroke-width="1" stroke-dasharray="2 3"/>
  </g>

  <!-- MAIN SILO BODY (Cylinder) -->
  <g id="silo-cylinder">
    <!-- Main Cylinder Body (Width 220, Height 210 -> Y=170 to 380) -->
    <rect x="350" y="170" width="220" height="210" fill="url(#siloGrad)" stroke="#475569" stroke-width="2"/>
    
    <!-- Horizontal Welded Panel Lines -->
    <line x1="350" y1="220" x2="570" y2="220" stroke="#64748B" stroke-width="1.5"/>
    <line x1="350" y1="270" x2="570" y2="270" stroke="#64748B" stroke-width="1.5"/>
    <line x1="350" y1="320" x2="570" y2="320" stroke="#64748B" stroke-width="1.5"/>

    <!-- Silo Dome Roof (Y=100 to 170) -->
    <path d="M 350 170 C 350 120, 410 100, 460 100 C 510 100, 570 120, 570 170 Z" fill="url(#roofGrad)" stroke="#475569" stroke-width="2"/>
    
    <!-- Roof Rim -->
    <ellipse cx="460" cy="170" rx="112" ry="7" fill="none" stroke="#94A3B8" stroke-width="2"/>

    <!-- Inspection Hatch (Manhole) -->
    <rect x="430" y="315" width="60" height="40" rx="6" fill="#1E293B" stroke="#64748B" stroke-width="1.5"/>
    <circle cx="440" cy="335" r="3" fill="#94A3B8"/>
    <text x="460" y="339" fill="#94A3B8" font-size="9" text-anchor="middle">HATCH</text>
  </g>

  <!-- EXHAUST VENTILATION FAN (Top of Silo Dome) -->
  <g id="exhaust-fan">
    <!-- Fan Cowl / Duct (Y=65 to 100) -->
    <rect x="425" y="65" width="70" height="35" rx="3" fill="#1E293B" stroke="#EF4444" stroke-width="2"/>
    <!-- Exhaust Fan Rain Cowl Cap -->
    <path d="M 410 65 L 510 65 L 495 52 L 425 52 Z" fill="#DC2626" stroke="#F87171" stroke-width="1.5"/>
    <!-- Fan Grill Slits -->
    <line x1="435" y1="78" x2="485" y2="78" stroke="#EF4444" stroke-width="2"/>
    <line x1="435" y1="86" x2="485" y2="86" stroke="#EF4444" stroke-width="2"/>
    <!-- Air Exhaust Flow Arrows (Red/Hot air outlet) -->
    <line x1="440" y1="48" x2="430" y2="28" stroke="#F87171" stroke-width="2" marker-end="url(#arrow)"/>
    <line x1="460" y1="48" x2="460" y2="24" stroke="#F87171" stroke-width="2" marker-end="url(#arrow)"/>
    <line x1="480" y1="48" x2="490" y2="28" stroke="#F87171" stroke-width="2" marker-end="url(#arrow)"/>
    <text x="460" y="16" fill="#F87171" font-size="11" font-weight="bold" text-anchor="middle">12V BLOWER EXHAUST FAN (PIN 18)</text>
  </g>

  <!-- IOT SENSORS ON SILO -->
  <!-- 1. DHT22 Sensor (Temperature & Humidity) -->
  <g id="dht22-sensor">
    <rect x="330" y="240" width="22" height="36" rx="3" fill="#FFFFFF" stroke="#0284C7" stroke-width="2"/>
    <!-- Grill mesh lines on DHT22 -->
    <line x1="334" y1="248" x2="348" y2="248" stroke="#0284C7" stroke-width="1.5"/>
    <line x1="334" y1="254" x2="348" y2="254" stroke="#0284C7" stroke-width="1.5"/>
    <line x1="334" y1="260" x2="348" y2="260" stroke="#0284C7" stroke-width="1.5"/>
    <circle cx="341" cy="269" r="2" fill="#0284C7"/>
    <!-- DHT22 Callout -->
    <polyline points="330,258 240,258 220,280" fill="none" stroke="#38BDF8" stroke-width="1.5"/>
    <rect x="110" y="270" width="115" height="42" rx="4" fill="#0F172A" stroke="#38BDF8" stroke-width="1"/>
    <text x="167" y="287" fill="#38BDF8" font-size="11" font-weight="bold" text-anchor="middle">DHT22 CLIMATE</text>
    <text x="167" y="303" fill="#94A3B8" font-size="9" text-anchor="middle">PIN 15 (Suhu &amp; RH)</text>
  </g>

  <!-- 2. MQ-135 Gas Sensor (Air Quality / Gas Detection) -->
  <g id="mq135-sensor">
    <rect x="568" y="200" width="24" height="30" rx="3" fill="#1E293B" stroke="#F59E0B" stroke-width="1.5"/>
    <circle cx="580" cy="215" r="9" fill="#D97706" stroke="#FEF3C7" stroke-width="1.5"/>
    <circle cx="580" cy="215" r="5" fill="#78350F"/>
    <!-- MQ-135 Callout -->
    <polyline points="592,215 670,215 690,190" fill="none" stroke="#F59E0B" stroke-width="1.5"/>
    <rect x="685" y="170" width="125" height="42" rx="4" fill="#0F172A" stroke="#F59E0B" stroke-width="1"/>
    <text x="747" y="187" fill="#F59E0B" font-size="11" font-weight="bold" text-anchor="middle">MQ-135 GAS SENSOR</text>
    <text x="747" y="203" fill="#94A3B8" font-size="9" text-anchor="middle">PIN 34 (Kualitas Udara)</text>
  </g>

  <!-- IOT CONTROL ENCLOSURE BOX (ESP32 + Relay/MOSFET) -->
  <g id="iot-box">
    <!-- Box mounted on right leg at Y=390 to 490 -->
    <rect x="580" y="390" width="80" height="110" rx="6" fill="#1E293B" stroke="#38BDF8" stroke-width="2"/>
    <rect x="585" y="395" width="70" height="100" rx="4" fill="#0F172A"/>
    
    <!-- Status LEDs -->
    <!-- Red LED (PIN 4: Fan ON) -->
    <circle cx="605" cy="415" r="6" fill="#EF4444" stroke="#F87171" stroke-width="1"/>
    <text x="605" y="432" fill="#F87171" font-size="8" font-weight="bold" text-anchor="middle">RED</text>
    <!-- Green LED (PIN 2: Fan OFF) -->
    <circle cx="635" cy="415" r="6" fill="#10B981" stroke="#34D399" stroke-width="1"/>
    <text x="635" y="432" fill="#34D399" font-size="8" font-weight="bold" text-anchor="middle">GRN</text>
    
    <!-- Buzzer Port (PIN 19) -->
    <circle cx="620" cy="455" r="12" fill="#334155" stroke="#64748B" stroke-width="1.5"/>
    <circle cx="620" cy="455" r="3" fill="#0F172A"/>
    <text x="620" y="478" fill="#94A3B8" font-size="8" text-anchor="middle">BUZZER</text>
    
    <!-- Box Label -->
    <text x="620" y="490" fill="#38BDF8" font-size="9" font-weight="bold" text-anchor="middle">ESP32 + RELAY</text>
    
    <!-- Conduit Pipes -->
    <path d="M 605 500 L 605 530 L 580 540" fill="none" stroke="#64748B" stroke-width="3"/>
    <path d="M 635 500 L 635 520 L 650 530" fill="none" stroke="#64748B" stroke-width="3"/>

    <!-- Callout Box -->
    <polyline points="660,445 740,445 760,470" fill="none" stroke="#38BDF8" stroke-width="1.5"/>
    <rect x="755" y="450" width="165" height="55" rx="4" fill="#0F172A" stroke="#38BDF8" stroke-width="1"/>
    <text x="837" y="470" fill="#38BDF8" font-size="11" font-weight="bold" text-anchor="middle">ENCLOSURE KONTROL IOT</text>
    <text x="837" y="486" fill="#94A3B8" font-size="9" text-anchor="middle">ESP32, Relay Fan, Buzzer</text>
    <text x="837" y="498" fill="#94A3B8" font-size="9" text-anchor="middle">LED Status &amp; HiveMQ MQTT</text>
  </g>

  <!-- DIMENSION LINES & TECHNICAL ANNOTATIONS -->
  <g id="dimensions" stroke="#64748B" stroke-width="1">
    <!-- Height of Silo Total (Top of Fan Y=52 to Ground Y=680 -> 180 mm equivalent) -->
    <line x1="80" y1="52" x2="80" y2="680" stroke="#38BDF8" stroke-width="1.5"/>
    <line x1="70" y1="52" x2="90" y2="52" stroke="#38BDF8" stroke-width="1.5"/>
    <line x1="70" y1="680" x2="90" y2="680" stroke="#38BDF8" stroke-width="1.5"/>
    <text x="65" y="375" fill="#38BDF8" font-size="13" font-weight="bold" text-anchor="middle" transform="rotate(-90 65 375)">TOTAL HEIGHT: 180 mm</text>

    <!-- Diameter Silo (Width 220 mm -> 60 mm equivalent) -->
    <line x1="350" y1="150" x2="570" y2="150" stroke="#F59E0B" stroke-width="1.5"/>
    <line x1="350" y1="140" x2="350" y2="160" stroke="#F59E0B" stroke-width="1.5"/>
    <line x1="570" y1="140" x2="570" y2="160" stroke="#F59E0B" stroke-width="1.5"/>
    <text x="460" y="142" fill="#F59E0B" font-size="12" font-weight="bold" text-anchor="middle">DIAMETER SILO: 60 mm</text>

    <!-- Conveyor Length (Width 560 -> 150 mm equivalent) -->
    <line x1="180" y1="730" x2="740" y2="730" stroke="#10B981" stroke-width="1.5"/>
    <line x1="180" y1="720" x2="180" y2="740" stroke="#10B981" stroke-width="1.5"/>
    <line x1="740" y1="720" x2="740" y2="740" stroke="#10B981" stroke-width="1.5"/>
    <text x="460" y="748" fill="#10B981" font-size="12" font-weight="bold" text-anchor="middle">PANJANG CONVEYOR: 150 mm (LEBAR: 36 mm)</text>
  </g>

  <!-- Legend & Specification Summary Table (Bottom Left) -->
  <g id="spec-legend">
    <rect x="30" y="770" width="940" height="60" rx="6" fill="#1E293B" stroke="#334155" stroke-width="1"/>
    <text x="50" y="792" fill="#F8FAFC" font-size="11" font-weight="bold">PARAMETER TINKERCAD:</text>
    <text x="50" y="812" fill="#94A3B8" font-size="10">Unit: mm (Workplane 200x200mm) | Format 3D: Binary STL &amp; Wavefront OBJ | Format 2D Extrude: SVG</text>
    <text x="520" y="792" fill="#F8FAFC" font-size="11" font-weight="bold">KOMPONEN ELEKTRONIK:</text>
    <text x="520" y="812" fill="#94A3B8" font-size="10">ESP32 NodeMCU, DHT22 (Pin 15), MQ-135 (Pin 34), Relay Fan (Pin 18), SG90 Servo, HC-SR04, Buzzer, LED</text>
  </g>
</svg>
"""

    with open(os.path.join(out_dir, "silo_conveyor_technical_elevation.svg"), "w", encoding="utf-8") as f:
        f.write(svg_elevation)
    print("Exported SVG: silo_conveyor_technical_elevation.svg")

    # 2. Extrude Pack SVG (Pure solid outlines for Tinkercad 2D import)
    # Tinkercad imports closed paths and extrudes them into 3D shapes.
    svg_extrude = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" width="800" height="600" style="background:#FFFFFF;">
  <!-- PART 1: SILO MAIN PROFILE (Silinder + Atap Kerucut + Corong Bawah) -->
  <path d="M 80 200 L 140 200 L 140 380 L 125 450 L 125 480 L 95 480 L 95 450 L 80 380 Z" fill="#475569" stroke="#000000" stroke-width="2"/>
  
  <!-- PART 2: CONVEYOR BED PROFILE -->
  <rect x="200" y="200" width="300" height="30" rx="5" fill="#1E293B" stroke="#000000" stroke-width="2"/>
  <circle cx="215" cy="215" r="10" fill="#64748B"/>
  <circle cx="485" cy="215" r="10" fill="#64748B"/>
  
  <!-- PART 3: IOT CONTROL BOX CASING -->
  <rect x="200" y="280" width="70" height="100" rx="8" fill="#0284C7" stroke="#000000" stroke-width="2"/>
  <circle cx="220" cy="305" r="6" fill="#FFFFFF"/>
  <circle cx="250" cy="305" r="6" fill="#FFFFFF"/>
  <circle cx="235" cy="340" r="12" fill="#FFFFFF"/>

  <!-- PART 4: GRAIN CART / WADAH -->
  <polygon points="320,280 400,280 390,340 330,340" fill="#D97706" stroke="#000000" stroke-width="2"/>

  <!-- PART 5: SILO LEGS & CROSS BRACE -->
  <polygon points="460,280 475,280 475,480 460,480" fill="#334155" stroke="#000000" stroke-width="2"/>
  <polygon points="500,280 515,280 515,480 500,480" fill="#334155" stroke="#000000" stroke-width="2"/>
  <rect x="450" y="380" width="75" height="12" fill="#64748B" stroke="#000000" stroke-width="1.5"/>
</svg>
"""
    with open(os.path.join(out_dir, "silo_parts_tinkercad_extrude.svg"), "w", encoding="utf-8") as f:
        f.write(svg_extrude)
    print("Exported SVG: silo_parts_tinkercad_extrude.svg")


# ==========================================
# MAIN EXECUTION
# ==========================================
def main():
    target_dir = os.path.abspath("desain_tinkercad_3d_2d")
    os.makedirs(target_dir, exist_ok=True)
    
    repo_target_dir = os.path.abspath("TugasBesarIOT_SiloMonitoringSystem/desain_tinkercad")
    os.makedirs(repo_target_dir, exist_ok=True)

    print("Building Silo Models for Tinkercad...")
    
    # 1. Silo Body
    silo_body = build_silo_body()
    silo_body.write_binary_stl(os.path.join(target_dir, "silo_body.stl"), "Silo Body Tank")
    silo_body.write_obj(os.path.join(target_dir, "silo_body.obj"))

    # 2. Silo Support Legs & Stand
    silo_legs = build_silo_legs()
    silo_legs.write_binary_stl(os.path.join(target_dir, "silo_support_legs.stl"), "Silo Support Stand")
    silo_legs.write_obj(os.path.join(target_dir, "silo_support_legs.obj"))

    # 3. Conveyor Assembly
    conveyor = build_conveyor()
    conveyor.write_binary_stl(os.path.join(target_dir, "conveyor_system.stl"), "Conveyor System")
    conveyor.write_obj(os.path.join(target_dir, "conveyor_system.obj"))

    # 4. IoT Enclosure Box
    iot_box = build_iot_box()
    iot_box.write_binary_stl(os.path.join(target_dir, "iot_enclosure_box.stl"), "IoT Enclosure Box")
    iot_box.write_obj(os.path.join(target_dir, "iot_enclosure_box.obj"))

    # 5. Combined Complete System Assembly
    complete_mesh = STLMesh()
    complete_mesh.triangles.extend(silo_body.triangles)
    complete_mesh.triangles.extend(silo_legs.triangles)
    complete_mesh.triangles.extend(conveyor.triangles)
    complete_mesh.triangles.extend(iot_box.triangles)
    complete_mesh.write_binary_stl(os.path.join(target_dir, "silo_monitoring_system_complete.stl"), "Complete Silo Monitoring Assembly")
    complete_mesh.write_obj(os.path.join(target_dir, "silo_monitoring_system_complete.obj"))

    # 6. Technical 2D SVGs
    generate_svg_drawings(target_dir)

    # Copy all generated files to repo directory as well
    for f in os.listdir(target_dir):
        src = os.path.join(target_dir, f)
        dst = os.path.join(repo_target_dir, f)
        shutil.copy2(src, dst)

    print(f"\nAll files successfully generated in:\n  - {target_dir}\n  - {repo_target_dir}")

if __name__ == "__main__":
    main()
