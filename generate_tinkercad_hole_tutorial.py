import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, axes = plt.subplots(1, 4, figsize=(15, 4.5), facecolor='#0F172A')

for ax in axes:
    ax.set_facecolor('#1E293B')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

# STEP 1: Drag Box Hole
axes[0].set_title('LANGKAH 1:\nAmbil Box "Hole"', color='#38BDF8', fontsize=11, weight='bold', pad=10)
c1 = patches.Circle((50, 40), 32, facecolor='#EA580C', edgecolor='#C2410C', linewidth=1.5)
axes[0].add_patch(c1)
b1 = patches.Rectangle((37, 26), 26, 28, facecolor='#94A3B8', edgecolor='#E2E8F0', linewidth=1.5, linestyle='--', alpha=0.7)
axes[0].add_patch(b1)
axes[0].text(50, 40, 'Box "Hole"\n23 x 12.5 mm', color='#0F172A', fontsize=9, weight='bold', ha='center', va='center')
axes[0].text(50, 85, 'Tarik Box abu-abu\n(Tipe: Hole)', color='#F8FAFC', fontsize=9, ha='center')

# STEP 2: Atur Kedalaman Z
axes[1].set_title('LANGKAH 2:\nAtur Kedalaman (Z)', color='#38BDF8', fontsize=11, weight='bold', pad=10)
c2 = patches.Rectangle((18, 30), 64, 16, facecolor='#EA580C', edgecolor='#C2410C', linewidth=1.5)
axes[1].add_patch(c2)
b2 = patches.Rectangle((37, 36), 26, 30, facecolor='#94A3B8', edgecolor='#E2E8F0', linewidth=1.5, linestyle='--', alpha=0.7)
axes[1].add_patch(b2)
axes[1].annotate('', xy=(50, 32), xytext=(50, 68), arrowprops=dict(arrowstyle="->", color="#38BDF8", lw=2.5))
axes[1].text(50, 85, 'Turunkan ke bawah\n(Z tembus 1.5 - 3 mm)\npakai kerucut hitam', color='#F8FAFC', fontsize=9, ha='center')

# STEP 3: Align Center
axes[2].set_title('LANGKAH 3:\nPilih Keduanya & Align (L)', color='#38BDF8', fontsize=11, weight='bold', pad=10)
c3 = patches.Circle((50, 40), 32, facecolor='#EA580C', edgecolor='#38BDF8', linewidth=2)
axes[2].add_patch(c3)
b3 = patches.Rectangle((37, 26), 26, 28, facecolor='#94A3B8', edgecolor='#38BDF8', linewidth=2, linestyle='--', alpha=0.7)
axes[2].add_patch(b3)
axes[2].plot([50], [5], 'o', color='#38BDF8', markersize=8)
axes[2].plot([95], [40], 'o', color='#38BDF8', markersize=8)
axes[2].text(50, 85, 'Tekan Shift + Klik keduanya\nlalu tekan tombol "L"\npilih titik tengah bulat', color='#F8FAFC', fontsize=9, ha='center')

# STEP 4: Group (Ctrl+G)
axes[3].set_title('LANGKAH 4:\nTekan Ctrl + G (Group)', color='#10B981', fontsize=11, weight='bold', pad=10)
c4 = patches.Circle((50, 40), 32, facecolor='#EA580C', edgecolor='#C2410C', linewidth=1.5)
axes[3].add_patch(c4)
h4 = patches.Rectangle((37, 26), 26, 28, facecolor='#1E293B', edgecolor='#0F172A', linewidth=1.5)
axes[3].add_patch(h4)
axes[3].text(50, 40, 'LUBANG\nKOTAK\nTERBENTUK!', color='#38BDF8', fontsize=8.5, weight='bold', ha='center', va='center')
axes[3].text(50, 85, 'Selesai!\nServo tinggal\ndimasukkan ke dalam', color='#10B981', fontsize=9, weight='bold', ha='center')

plt.tight_layout()
out_tut = 'desain_arm_akrilik_rapi/tutorial_melubangi_tinkercad.png'
plt.savefig(out_tut, dpi=200, facecolor=fig.get_facecolor())
plt.close()
print(f"Saved tutorial image: {out_tut}")
