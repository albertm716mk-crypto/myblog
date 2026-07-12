import matplotlib.pyplot as plt
import numpy as np
import os

plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

def generate_bar_chart(output_dir="assets", filename="bar_chart.png"):
    os.makedirs(output_dir, exist_ok=True)
    categories = ['Python', 'JavaScript', 'HTML/CSS', 'SQL', 'C++']
    values = [85, 70, 65, 60, 45]
    colors = ['#4E79A7', '#F28E2B', '#E15759', '#76B7B2', '#59A14F']
    fig, ax = plt.subplots(figsize=(8, 5.5), dpi=300)
    bars = ax.bar(categories, values, color=colors, width=0.6, edgecolor='none')
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height}%', xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=10, fontweight='bold', color='#333333')
    ax.set_title('Skills', fontsize=16, fontweight='bold', pad=20, color='#2C3E50')
    ax.set_ylabel('Proportion', fontsize=12, labelpad=10, color='#2C3E50')
    ax.set_ylim(0, 100)
    ax.tick_params(axis='both', which='major', labelsize=11, colors='#2C3E50')
    ax.grid(axis='y', linestyle=':', alpha=0.5, color='#BDC3C7')
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#BDC3C7')
    ax.spines['bottom'].set_color('#BDC3C7')
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, bbox_inches='tight', dpi=300)
    plt.close(fig)
    print(f"saved to {filepath}")

if __name__ == '__main__':
    generate_bar_chart()