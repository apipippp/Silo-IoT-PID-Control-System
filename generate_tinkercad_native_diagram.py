import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(12, 8.5), facecolor='#0F172A')
ax.set_facecolor('#0F172A')

# Workspace area
ax.add_patch(patches.Rectangle((20, 20), 650, 480, facecolor='#1E293B', edgecolor='#334155', linewidth=1.5))
# Workplane Grid simulation
for x in range(50, 640, 40):
    ax.plot([x, x], [40, 480], color='#334155', linewidth=0.5, linestyle=':')
for y in range(60, 470, 40):
    ax.plot([40, 650], [y, y], color='#334155', linewidth=0.5, linestyle=':')

# Sidebar on the right
ax.add_patch(patches.Rectangle((690, 20), 280, 480, facecolor='#1E293B', edgecolor='#38BDF8', linewidth=1.5))
ax.text(830, 470, 'SIDEBAR TINKERCAD', color='#38BDF8', fontsize=11, weight='bold', ha='center')
ax.text(830, 450, 'Kategori: "Basic Shapes" & "Electronics"', color='#94A3B8', fontsize=8, ha='center')

# Sidebar Shape Cards
# Card 1: Box
ax.add_patch(patches.Rectangle((710, 395), 110, 45, facecolor='#0F172A', edgecolor='#EF4444', linewidth=1))
ax.text(765, 420, '1. BOX (Solid)\nTebal Z = 3 mm', color='#F8FAFC', fontsize=8, weight='bold', ha='center')

# Card 2: Cylinder
ax.add_patch(patches.Rectangle((840, 395), 110, 45, facecolor='#0F172A', edgecolor='#3B82F6', linewidth=1))
ax.text(895, 420, '2. CYLINDER\nTinggi Z = 3 mm', color='#F8FAFC', fontsize=8, weight='bold', ha='center')

# Card 3: Hole Box/Cylinder
ax.add_patch(patches.Rectangle((710, 335), 110, 45, facecolor='#0F172A', edgecolor='#94A3B8', linewidth=1, linestyle='--'))
ax.text(765, 360, '3. HOLE (Lubang)\nUntuk Baut & Slot', color='#94A3B8', fontsize=8, weight='bold', ha='center')

# Card 4: Micro Servo
ax.add_patch(patches.Rectangle((840, 335), 110, 45, facecolor='#0F172A', edgecolor='#10B981', linewidth=1))
ax.text(895, 360, '4. MICRO SERVO\nAda di "Electronics"', color='#10B981', fontsize=8, weight='bold', ha='center')

# Assembly Layout in Workplane
# 1. Base Plate (Box)
ax.add_patch(patches.Rectangle((60, 60), 140, 140, facecolor='#0284C7', edgecolor='#38BDF8', alpha=0.4, linewidth=2))
ax.text(130, 175, '1. BASE (Box)\n70 x 70 x 3 mm', color='#F8FAFC', fontsize=9, weight='bold', ha='center')
# Servo Slot Hole in Base
ax.add_patch(patches.Rectangle((107, 105), 46, 25, facecolor='#0F172A', edgecolor='#EF4444', linewidth=1.5, linestyle='--'))
ax.text(130, 117, 'Slot Hole\n23x12.5mm', color='#EF4444', fontsize=7, ha='center', va='center')

# 2. Turntable (Cylinder)
ax.add_patch(patches.Circle((270, 130), 50, facecolor='#0284C7', edgecolor='#38BDF8', alpha=0.4, linewidth=2))
ax.text(270, 130, '2. TURNTABLE (Cylinder)\nDia 50 mm, Tinggi 3 mm', color='#F8FAFC', fontsize=8, weight='bold', ha='center')

# 3. Shoulder (Box with Hole)
ax.add_patch(patches.Rectangle((350, 70), 60, 64, facecolor='#0284C7', edgecolor='#38BDF8', alpha=0.4, linewidth=2))
ax.add_patch(patches.Rectangle((357, 85), 46, 25, facecolor='#0F172A', edgecolor='#EF4444', linewidth=1.2, linestyle='--'))
ax.text(380, 120, '3. BAHU (Box)\n30 x 32 x 3 mm', color='#F8FAFC', fontsize=8, weight='bold', ha='center')

# 4. Bicep Arm (Box with radius)
ax.add_patch(patches.Rectangle((60, 240), 130, 32, facecolor='#0284C7', edgecolor='#38BDF8', alpha=0.4, linewidth=2))
ax.text(125, 256, '4. LENGAN BAWAH\n(Box: 65 x 16 x 3 mm)', color='#F8FAFC', fontsize=8, weight='bold', ha='center')

# 5. Forearm (Box with radius)
ax.add_patch(patches.Rectangle((220, 240), 110, 28, facecolor='#0284C7', edgecolor='#38BDF8', alpha=0.4, linewidth=2))
ax.text(275, 254, '5. LENGAN ATAS\n(Box: 55 x 14 x 3 mm)', color='#F8FAFC', fontsize=8, weight='bold', ha='center')

# 6. Gripper Base + Fixed Jaw
ax.add_patch(patches.Rectangle((360, 240), 70, 52, facecolor='#0284C7', edgecolor='#38BDF8', alpha=0.4, linewidth=2))
ax.add_patch(patches.Rectangle((430, 240), 50, 16, facecolor='#0284C7', edgecolor='#38BDF8', alpha=0.4, linewidth=2))
ax.text(415, 280, '6. GRIPPER BASE + FIXED JAW\n(2 Box di-Group)', color='#F8FAFC', fontsize=8, weight='bold', ha='center')

# 7. Moving Jaw
ax.add_patch(patches.Rectangle((510, 240), 65, 20, facecolor='#0284C7', edgecolor='#38BDF8', alpha=0.4, linewidth=2))
ax.text(542, 250, '7. MOVING JAW\n(Box 32x10x3mm)', color='#F8FAFC', fontsize=7.5, weight='bold', ha='center')

# Tips & Shortcut Box in Sidebar
ax.add_patch(patches.Rectangle((710, 50), 240, 260, facecolor='#0F172A', edgecolor='#64748B', linewidth=1))
ax.text(725, 290, 'SHORTCUT & FITUR ASLI TINKERCAD:', color='#F8FAFC', fontsize=9, weight='bold')
ax.text(725, 265, '• Tebal Akrilik: Set tinggi Z = 3 mm', color='#38BDF8', fontsize=8)
ax.text(725, 240, '• Lubang Baut: Silinder Hole 3.2 mm', color='#38BDF8', fontsize=8)
ax.text(725, 215, '• Melubangi: Pilih Solid + Hole -> Ctrl+G', color='#38BDF8', fontsize=8)
ax.text(725, 190, '• Duplikasi Cepat: Klik part -> Ctrl+D', color='#38BDF8', fontsize=8)
ax.text(725, 165, '• Pasang di Permukaan: Tekan W (Workplane)', color='#38BDF8', fontsize=8)
ax.text(725, 140, '• Rata Tengah / Presisi: Tombol L (Align)', color='#38BDF8', fontsize=8)
ax.text(725, 100, 'EXPORT KE LASER CUTTING AKRILIK:\nKlik Export (Kanan Atas) -> Pilih .SVG\nTinkercad langsung ekspor pola 2D!', color='#10B981', fontsize=8.5, weight='bold')

ax.set_xlim(0, 1000)
ax.set_ylim(0, 520)
ax.axis('off')

plt.tight_layout()
out_img = 'desain_arm_simple_7part/tinkercad_native_recipe_guide.png'
plt.savefig(out_img, dpi=200, facecolor=fig.get_facecolor())
plt.close()
print(f"Saved guide diagram: {out_img}")
