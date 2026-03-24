#!/usr/bin/env python3
"""
Generate figures for LaTeX document
Author: Andrew Baker
Date: March 2026
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path

def create_economic_multiplier_figure():
    """Create economic multiplier comparison chart"""
    
    sectors = ['Building\nRetrofits', 'EV\nInfrastructure', 'Battery\nRecycling', 
               'Urban\nGreening', 'Weighted\nAverage']
    multipliers = [4.2, 4.8, 3.9, 4.5, 4.35]
    colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#59CD90']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(sectors, multipliers, color=colors, edgecolor='black', linewidth=1.2)
    
    ax.axhline(y=4.0, color='red', linestyle='--', linewidth=2, label='Target (4.0x)')
    ax.set_ylabel('Economic Multiplier (x)', fontsize=12, fontweight='bold')
    ax.set_title('Economic Multipliers by Sector', fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='upper left')
    ax.set_ylim(0, 6)
    
    # Add value labels on bars
    for bar, mult in zip(bars, multipliers):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
               f'{mult}x', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    
    # Save to figures directory
    output_dir = Path(__file__).parent.parent / 'latex' / 'figures'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    plt.savefig(output_dir / 'economic_multipliers.pdf', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'economic_multipliers.png', dpi=300, bbox_inches='tight')
    print("✅ Created economic_multipliers figure")
    plt.close()

def create_fuel_excise_trend():
    """Create fuel excise revenue trend"""
    
    years = list(range(2020, 2027))
    revenue = [16.2, 15.9, 15.7, 15.1, 14.3, 13.2, 12.1]  # Billions AUD
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, revenue, marker='o', linewidth=3, markersize=8, color='#2E86AB')
    ax.fill_between(years, revenue, alpha=0.3, color='#2E86AB')
    
    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_ylabel('Fuel Excise Revenue (AUD Billions)', fontsize=12, fontweight='bold')
    ax.set_title('Declining Fuel Excise Revenue', fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)
    
    output_dir = Path(__file__).parent.parent / 'latex' / 'figures'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    plt.savefig(output_dir / 'fuel_excise_trend.pdf', dpi=300, bbox_inches='tight')
    print("✅ Created fuel_excise_trend figure")
    plt.close()

def create_policy_timeline():
    """Create policy implementation timeline"""
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    phases = ['Phase 1:\nFoundation\n(0-12 mo)', 'Phase 2:\nScale-Up\n(1-3 yr)', 
              'Phase 3:\nTransformation\n(3-10 yr)']
    budgets = [0.75, 1.2, 2.5]  # Billions AUD
    colors = ['#59CD90', '#F18F01', '#A23B72']
    
    bars = ax.bar(phases, budgets, color=colors, edgecolor='black', linewidth=1.2)
    
    ax.set_ylabel('Budget (AUD Billions)', fontsize=12, fontweight='bold')
    ax.set_title('Implementation Timeline & Budget', fontsize=14, fontweight='bold', pad=20)
    
    # Add value labels
    for bar, budget in zip(bars, budgets):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, 
               f'${budget}B', ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    output_dir = Path(__file__).parent.parent / 'latex' / 'figures'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    plt.savefig(output_dir / 'policy_timeline.pdf', dpi=300, bbox_inches='tight')
    print("✅ Created policy_timeline figure")
    plt.close()

def create_revenue_replacement_chart():
    """Create revenue replacement comparison"""
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    categories = ['Current Fuel\nExcise', 'Direct\nRevenue', 'Indirect\nRevenue', 'Total\nReplacement']
    values = [15.71, 8.3, 9.6, 17.9]
    colors = ['#95A5A6', '#3498DB', '#27AE60', '#2ECC71']
    
    bars = ax.bar(categories, values, color=colors, edgecolor='black', linewidth=1.2)
    
    ax.set_ylabel('Revenue (AUD Billions)', fontsize=12, fontweight='bold')
    ax.set_title('Fuel Excise Replacement Strategy', fontsize=14, fontweight='bold', pad=20)
    
    # Add value labels
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2, 
               f'${val}B', ha='center', va='bottom', fontweight='bold')
    
    # Add target line
    ax.axhline(y=15.71, color='red', linestyle='--', linewidth=2, label='Current Revenue')
    ax.legend()
    
    output_dir = Path(__file__).parent.parent / 'latex' / 'figures'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    plt.savefig(output_dir / 'revenue_replacement.pdf', dpi=300, bbox_inches='tight')
    print("✅ Created revenue_replacement figure")
    plt.close()

def main():
    """Generate all figures"""
    print("📊 Generating figures for LaTeX document...")
    print("=" * 50)
    
    create_economic_multiplier_figure()
    create_fuel_excise_trend()
    create_policy_timeline()
    create_revenue_replacement_chart()
    
    print("=" * 50)
    print("✅ All figures generated successfully!")
    print(f"📁 Output: latex/figures/")

if __name__ == "__main__":
    main()
