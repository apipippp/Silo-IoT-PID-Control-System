import struct
import numpy as np
import os
import math

class STLMesh:
    def __init__(self):
        self.triangles = []  # list of ((nx, ny, nz), (v1x, v1y, v1z), (v2x, v2y, v2z), (v3x, v3y, v3z))

    def add_triangle(self, p1, p2, p3):
        # calculate normal
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
        # Quad split into two triangles (p1, p2, p3) and (p1, p3, p4)
        self.add_triangle(p1, p2, p3)
        self.add_triangle(p1, p3, p4)

    def add_box(self, center_x, center_y, center_z, size_x, size_y, size_z):
        dx, dy, dz = size_x / 2.0, size_y / 2.0, size_z / 2.0
        x0, x1 = center_x - dx, center_x + dx
        y0, y1 = center_y - dy, center_y + dy
        z0, z1 = center_z - dz, center_z + dz

        # 8 corners
        c000 = (x0, y0, z0)
        c100 = (x1, y0, z0)
        c110 = (x1, y1, z0)
        c010 = (x0, y1, z0)
        c001 = (x0, y0, z1)
        c101 = (x1, y0, z1)
        c111 = (x1, y1, z1)
        c011 = (x0, y1, z1)

        # Bottom (z0)
        self.add_quad(c000, c010, c110, c100)
        # Top (z1)
        self.add_quad(c001, c101, c111, c011)
        # Front (y0)
        self.add_quad(c000, c100, c101, c001)
        # Back (y1)
        self.add_quad(c110, c010, c011, c111)
        # Left (x0)
        self.add_quad(c010, c000, c001, c011)
        # Right (x1)
        self.add_quad(c100, c110, c111, c101)

    def add_cylinder(self, cx, cy, z_bottom, z_top, radius_bottom, radius_top=None, segments=32, cap_bottom=True, cap_top=True):
        if radius_top is None:
            radius_top = radius_bottom

        angles = [2.0 * math.pi * i / segments for i in range(segments)]
        
        # Bottom ring and top ring
        bot_pts = [(cx + radius_bottom * math.cos(a), cy + radius_bottom * math.sin(a), z_bottom) for a in angles]
        top_pts = [(cx + radius_top * math.cos(a), cy + radius_top * math.sin(a), z_top) for a in angles]

        # Side quads
        for i in range(segments):
            next_i = (i + 1) % segments
            self.add_quad(bot_pts[i], bot_pts[next_i], top_pts[next_i], top_pts[i])

        # Bottom cap
        if cap_bottom and radius_bottom > 1e-4:
            c_bot = (cx, cy, z_bottom)
            for i in range(segments):
                next_i = (i + 1) % segments
                self.add_triangle(c_bot, bot_pts[next_i], bot_pts[i])

        # Top cap
        if cap_top and radius_top > 1e-4:
            c_top = (cx, cy, z_top)
            for i in range(segments):
                next_i = (i + 1) % segments
                self.add_triangle(c_top, top_pts[i], top_pts[next_i])

    def add_horizontal_cylinder(self, x_start, x_end, cy, cz, radius, segments=24):
        # Cylinder aligned along X-axis
        angles = [2.0 * math.pi * i / segments for i in range(segments)]
        s_pts = [(x_start, cy + radius * math.cos(a), cz + radius * math.sin(a)) for a in angles]
        e_pts = [(x_end, cy + radius * math.cos(a), cz + radius * math.sin(a)) for a in angles]

        for i in range(segments):
            next_i = (i + 1) % segments
            self.add_quad(s_pts[i], e_pts[i], e_pts[next_i], s_pts[next_i])

        # Caps
        c_s = (x_start, cy, cz)
        c_e = (x_end, cy, cz)
        for i in range(segments):
            next_i = (i + 1) % segments
            self.add_triangle(c_s, s_pts[next_i], s_pts[i])
            self.add_triangle(c_e, e_pts[i], e_pts[next_i])

    def add_ring(self, cx, cy, z_bottom, z_top, r_inner, r_outer, segments=32):
        angles = [2.0 * math.pi * i / segments for i in range(segments)]
        b_in = [(cx + r_inner * math.cos(a), cy + r_inner * math.sin(a), z_bottom) for a in angles]
        b_out = [(cx + r_outer * math.cos(a), cy + r_outer * math.sin(a), z_bottom) for a in angles]
        t_in = [(cx + r_inner * math.cos(a), cy + r_inner * math.sin(a), z_top) for a in angles]
        t_out = [(cx + r_outer * math.cos(a), cy + r_outer * math.sin(a), z_top) for a in angles]

        for i in range(segments):
            ni = (i + 1) % segments
            # outer side
            self.add_quad(b_out[i], b_out[ni], t_out[ni], t_out[i])
            # inner side
            self.add_quad(b_in[ni], b_in[i], t_in[i], t_in[ni])
            # top cap
            self.add_quad(t_in[i], t_out[i], t_out[ni], t_in[ni])
            # bottom cap
            self.add_quad(b_out[i], b_in[i], b_in[ni], b_out[ni])

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

    def write_obj(self, filepath):
        # Optional Wavefront OBJ format for Tinkercad
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("# Tinkercad 3D Wavefront OBJ\n")
            vert_map = {}
            vert_list = []
            faces = []

            def get_v_idx(pt):
                # round to 4 decimals to weld vertices
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

print("STLMesh class defined successfully.")
