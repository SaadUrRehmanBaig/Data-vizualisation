#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
import os
warnings.filterwarnings('ignore')

# Create output directory for images
script_dir = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(script_dir, '..', 'assets', 'images')
os.makedirs(OUTPUT_DIR, exist_ok=True)

plt.style.use('default')

PROFESSIONAL_COLORS = {
    'primary_blue': '#2E4A6B',      # Deep professional blue
    'secondary_blue': '#4A6B8A',    # Medium blue
    'accent_blue': '#6B8BAA',       # Light blue
    'primary_red': '#8B2635',       # Deep burgundy red
    'secondary_red': '#A64452',     # Medium red
    'accent_red': '#C1626F',        # Light red
    'primary_green': '#2D5A3D',     # Deep forest green
    'secondary_green': '#4A7A5A',   # Medium green
    'accent_green': '#679A77',      # Light green
    'primary_teal': '#2D5A5A',      # Deep teal
    'secondary_teal': '#4A7A7A',    # Medium teal
    'accent_teal': '#679A9A',       # Light teal
    'charcoal': '#2C3E50',          # Professional charcoal
    'slate': '#34495E',             # Slate gray
    'silver': '#7F8C8D',            # Silver gray
    'background': '#FAFBFC',        # Ultra-light background
    'grid': '#E8EAED',              # Subtle grid lines
    'text_primary': '#1A1A1A',      # Primary text
    'text_secondary': '#2C3E50'     # Secondary text
}

plt.rcParams['figure.figsize'] = (16, 12)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Helvetica', 'Arial', 'DejaVu Sans']
plt.rcParams['font.size'] = 14
plt.rcParams['axes.titlesize'] = 22
plt.rcParams['axes.labelsize'] = 16
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['legend.fontsize'] = 14
plt.rcParams['figure.titlesize'] = 24
plt.rcParams['axes.linewidth'] = 1.5
plt.rcParams['grid.linewidth'] = 1.0
plt.rcParams['lines.linewidth'] = 3.0

def load_data():
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to project root, then into data directory
    data_file = os.path.join(script_dir, '..', 'data', 'tour_occ_nim__custom_19389427_linear_2_0.csv')
    
    if not os.path.exists(data_file):
        raise FileNotFoundError(f"Data file not found: {data_file}")
    
    df = pd.read_csv(data_file)
    
    clean_df = df.iloc[:, [5, 7, 9, 11, 13, 15]].copy()
    clean_df.columns = ['c_resid', 'unit', 'nace_r2', 'geo', 'time_period', 'obs_value']
    
    clean_df = clean_df.dropna(subset=['time_period', 'obs_value'])
    clean_df['obs_value'] = pd.to_numeric(clean_df['obs_value'], errors='coerce')
    clean_df['date'] = pd.to_datetime(clean_df['time_period'], format='%Y-%m', errors='coerce')
    clean_df = clean_df.dropna(subset=['date', 'obs_value'])
    clean_df['year'] = clean_df['date'].dt.year
    clean_df['month'] = clean_df['date'].dt.month
    
    return clean_df

def chart1_covid_impact_professional(df):
    
    # EU countries (consistent with official EU statistics)
    eu27_countries = ['ES', 'IT', 'FR', 'DE', 'NL', 'PT', 'EL', 'HR', 'CY', 'MT',
                     'PL', 'CZ', 'HU', 'DK', 'SE', 'AT', 'BE', 'RO', 'BG', 'SK', 
                     'SI', 'FI', 'IE', 'LU', 'EE', 'LV', 'LT']
    
    impact_data = df[
        (df['geo'].isin(eu27_countries)) &
        (df['unit'] == 'NR') &
        (df['nace_r2'] == 'I551-I553') &
        (df['c_resid'] == 'TOTAL') &
        (df['year'].isin([2019, 2020]))
    ]
    
    annual_totals = impact_data.groupby(['geo', 'year'])['obs_value'].sum().reset_index()
    pivot_data = annual_totals.pivot(index='geo', columns='year', values='obs_value')
    
    if 2019 in pivot_data.columns and 2020 in pivot_data.columns:
        pivot_data['pct_change'] = ((pivot_data[2020] - pivot_data[2019]) / pivot_data[2019]) * 100
        pivot_data = pivot_data.dropna(subset=['pct_change'])
        
        country_names = {
            'ES': 'Spain', 'IT': 'Italy', 'FR': 'France', 'DE': 'Germany', 'PT': 'Portugal', 
            'EL': 'Greece', 'HR': 'Croatia', 'AT': 'Austria', 'NL': 'Netherlands', 'BE': 'Belgium',
            'PL': 'Poland', 'CZ': 'Czechia', 'HU': 'Hungary', 'RO': 'Romania', 'BG': 'Bulgaria',
            'SK': 'Slovakia', 'SI': 'Slovenia', 'FI': 'Finland', 'DK': 'Denmark', 'SE': 'Sweden',
            'IE': 'Ireland', 'LU': 'Luxembourg', 'MT': 'Malta', 'CY': 'Cyprus', 'EE': 'Estonia',
            'LV': 'Latvia', 'LT': 'Lithuania'
        }
        
        impact_sorted = pivot_data['pct_change'].sort_values()
        
        fig, ax = plt.subplots(figsize=(16, 12))
        fig.patch.set_facecolor(PROFESSIONAL_COLORS['background'])
        
        n_countries = len(impact_sorted)
        red_colors = []
        for i in range(n_countries):
            if i < n_countries // 3:
                red_colors.append('#C85450')    # Light-medium red - worst impact
            elif i < 2 * n_countries // 3:
                red_colors.append('#D67570')    # Lighter red - medium impact
            else:
                red_colors.append('#E49690')    # Lightest red - least impact
        
        bars = ax.barh([country_names.get(geo, geo) for geo in impact_sorted.index], 
                      impact_sorted.values, color=red_colors, alpha=0.85, height=0.75,
                      edgecolor='white', linewidth=1.5)
        
        for i, (geo, value) in enumerate(impact_sorted.items()):
            ax.text(value - 2.5, i, f'{value:.1f}%', 
                   va='center', ha='right', fontweight='bold', 
                   color='white', fontsize=12)
        
        ax.set_title('COVID-19 Impact on EU Tourism Markets\nTourist Arrivals Decline (2020 vs 2019 Baseline)', 
                    fontsize=24, fontweight='bold', pad=30, color=PROFESSIONAL_COLORS['text_primary'])
        ax.set_xlabel('Percentage Decline (%)', fontsize=18, color=PROFESSIONAL_COLORS['text_secondary'])
        ax.set_ylabel('Market', fontsize=18, color=PROFESSIONAL_COLORS['text_secondary'])
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(PROFESSIONAL_COLORS['silver'])
        ax.spines['bottom'].set_color(PROFESSIONAL_COLORS['silver'])
        ax.spines['left'].set_linewidth(1.5)
        ax.spines['bottom'].set_linewidth(1.5)
        
        ax.grid(axis='x', alpha=0.4, linestyle='-', linewidth=1.0, color=PROFESSIONAL_COLORS['grid'])
        ax.set_axisbelow(True)
        ax.set_xlim(min(impact_sorted.values) * 1.1, 0)
        
        ax.tick_params(axis='both', which='major', labelsize=12, colors=PROFESSIONAL_COLORS['text_secondary'])
        ax.tick_params(axis='x', length=8, width=1.5, color=PROFESSIONAL_COLORS['silver'])
        ax.tick_params(axis='y', length=0)
        
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, 'covid_impact.png'), dpi=300, bbox_inches='tight', 
                   facecolor=PROFESSIONAL_COLORS['background'], edgecolor='none', pad_inches=0.3)
        plt.show()

def chart1_covid_impact_map(df):
    import plotly.express as px
    import plotly.graph_objects as go
    
    # EU countries (consistent with official EU statistics)
    eu27_countries = ['ES', 'IT', 'FR', 'DE', 'NL', 'PT', 'EL', 'HR', 'CY', 'MT',
                     'PL', 'CZ', 'HU', 'DK', 'SE', 'AT', 'BE', 'RO', 'BG', 'SK', 
                     'SI', 'FI', 'IE', 'LU', 'EE', 'LV', 'LT']
    
    impact_data = df[
        (df['geo'].isin(eu27_countries)) &
        (df['unit'] == 'NR') &
        (df['nace_r2'] == 'I551-I553') &
        (df['c_resid'] == 'TOTAL') &
        (df['year'].isin([2019, 2020]))
    ]
    
    if not impact_data.empty:
        annual_totals = impact_data.groupby(['geo', 'year'])['obs_value'].sum().reset_index()
        pivot_data = annual_totals.pivot(index='geo', columns='year', values='obs_value')
        
        if 2019 in pivot_data.columns and 2020 in pivot_data.columns:
            pivot_data['pct_change'] = ((pivot_data[2020] - pivot_data[2019]) / pivot_data[2019]) * 100
            pivot_data = pivot_data.dropna(subset=['pct_change'])
            
            country_mapping = {
                'ES': 'ESP', 'IT': 'ITA', 'FR': 'FRA', 'DE': 'DEU', 'PT': 'PRT', 
                'EL': 'GRC', 'HR': 'HRV', 'AT': 'AUT', 'NL': 'NLD', 'BE': 'BEL',
                'PL': 'POL', 'CZ': 'CZE', 'HU': 'HUN', 'RO': 'ROU', 'BG': 'BGR',
                'SK': 'SVK', 'SI': 'SVN', 'FI': 'FIN', 'DK': 'DNK', 'SE': 'SWE',
                'IE': 'IRL', 'LU': 'LUX', 'MT': 'MLT', 'CY': 'CYP', 'EE': 'EST',
                'LV': 'LVA', 'LT': 'LTU'
            }
            
            country_names = {
                'ES': 'Spain', 'IT': 'Italy', 'FR': 'France', 'DE': 'Germany', 'PT': 'Portugal', 
                'EL': 'Greece', 'HR': 'Croatia', 'AT': 'Austria', 'NL': 'Netherlands', 'BE': 'Belgium',
                'PL': 'Poland', 'CZ': 'Czechia', 'HU': 'Hungary', 'RO': 'Romania', 'BG': 'Bulgaria',
                'SK': 'Slovakia', 'SI': 'Slovenia', 'FI': 'Finland', 'DK': 'Denmark', 'SE': 'Sweden',
                'IE': 'Ireland', 'LU': 'Luxembourg', 'MT': 'Malta', 'CY': 'Cyprus', 'EE': 'Estonia',
                'LV': 'Latvia', 'LT': 'Lithuania'
            }
            
            map_data = []
            for geo_code in pivot_data.index:
                if geo_code in country_mapping:
                    impact_val = pivot_data.loc[geo_code, 'pct_change']
                    
                    # Add journalism context for hover
                    if impact_val <= -60:
                        severity = "DEVASTATING"
                        context = "Tourism industry collapsed"
                    elif impact_val <= -50:
                        severity = "SEVERE"
                        context = "Major economic disruption"
                    elif impact_val <= -40:
                        severity = "SIGNIFICANT"
                        context = "Substantial losses"
                    elif impact_val <= -30:
                        severity = "MODERATE"
                        context = "Notable decline"
                    else:
                        severity = "LIMITED"
                        context = "Relatively resilient"
                    
                    map_data.append({
                        'iso_alpha': country_mapping[geo_code],
                        'country': country_names.get(geo_code, geo_code),
                        'impact': impact_val,
                        'severity': severity,
                        'context': context,
                        'impact_display': f"{impact_val:.1f}%"
                    })
            
            map_df = pd.DataFrame(map_data)
            
            # Find key countries for annotations
            worst_hit = map_df.loc[map_df['impact'].idxmin()]
            least_hit = map_df.loc[map_df['impact'].idxmax()]
            
            # Create choropleth map with journalism-grade storytelling
            fig = px.choropleth(
                map_df,
                locations='iso_alpha',
                color='impact',
                hover_name='country',
                hover_data={
                    'impact_display': True,
                    'severity': True, 
                    'context': True,
                    'iso_alpha': False,
                    'impact': False
                },
                color_continuous_scale=[
                    [0.0, '#8B0000'],    # Crisis red - "Blood red" for journalism impact
                    [0.2, '#B22222'],    # Deep red - Major story
                    [0.4, '#DC143C'],    # Crimson - Significant news
                    [0.6, '#CD5C5C'],    # Indian red - Notable story
                    [0.8, '#F08080'],    # Light coral - Minor story
                    [1.0, '#FFB6C1']     # Light pink - Background story
                ],
                range_color=[map_df['impact'].min(), map_df['impact'].max()],
                labels={
                    'impact': 'Tourism Decline (%)',
                    'impact_display': 'Decline',
                    'severity': 'Impact Level',
                    'context': 'Economic Effect'
                }
            )
            
            # Focus on Europe with journalism-appropriate styling
            fig.update_geos(
                projection_type="natural earth",
                showocean=True, oceancolor="#E6F3FF",  # Softer blue for professional look
                showlakes=True, lakecolor="#E6F3FF",
                showland=True, landcolor="#F5F5F5",    # Neutral gray for non-data countries
                showcountries=True, countrycolor="#CCCCCC",  # Subtle borders
                fitbounds="locations",
                resolution=50,
                scope='europe'
            )
            
            # Add key annotations for immediate story understanding
            # Add data source and credibility
            fig.add_annotation(
                x=0.98, y=0.02,
                xref="paper", yref="paper",
                text="Source: Eurostat Official Tourism Statistics<br>Data: Tourist nights at accommodation establishments<br>Analysis: 2020 vs 2019 baseline comparison",
                showarrow=False,
                align="right",
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="#CCCCCC",
                borderwidth=1,
                font=dict(size=11, color="#666666", family="Arial")
            )
            
            # Update layout for journalism standards
            fig.update_layout(
                title={
                    'text': '<b>COVID-19 DEVASTATED EU TOURISM</b><br><span style="font-size:18px">Worst-affected countries in 2020</span>',
                    'x': 0.5,
                    'xanchor': 'center',
                    'y': 0.95,
                    'font': {'size': 28, 'color': '#1A1A1A', 'family': 'Arial Black'}
                },
                font={'size': 14, 'color': '#2C3E50', 'family': 'Arial'},
                paper_bgcolor='white',
                plot_bgcolor='white',
                width=1800,
                height=1400,
                margin=dict(t=120, b=80, l=60, r=60),
                coloraxis_colorbar={
                    'title': {
                        'text': '<b>Tourism Decline (%)</b><br>Darker = Worse Impact', 
                        'font': {'size': 16, 'family': 'Arial Black'}
                    },
                    'tickfont': {'size': 14, 'family': 'Arial'},
                    'len': 0.6,
                    'thickness': 25,
                    'x': 1.02,
                    'tickmode': 'array',
                    'tickvals': [-70, -60, -50, -40, -30, -20],
                    'ticktext': ['-70%', '-60%', '-50%', '-40%', '-30%', '-20%']
                }
            )
            
            fig.write_image(os.path.join(OUTPUT_DIR, 'covid_impact_map_journalism.png'), width=1800, height=1400, scale=2)
            
def chart2_recovery_map_journalism(df):
    import plotly.express as px
    import plotly.graph_objects as go
    
    # EU countries (consistent with official EU statistics)
    eu27_countries = ['ES', 'IT', 'FR', 'DE', 'NL', 'PT', 'EL', 'HR', 'CY', 'MT',
                     'PL', 'CZ', 'HU', 'DK', 'SE', 'AT', 'BE', 'RO', 'BG', 'SK', 
                     'SI', 'FI', 'IE', 'LU', 'EE', 'LV', 'LT']
    
    recovery_data = df[
        (df['geo'].isin(eu27_countries)) &
        (df['unit'] == 'PCH_SM_19') & 
        (df['nace_r2'] == 'I551-I553') &
        (df['c_resid'] == 'TOTAL') &
        (df['year'] == 2024)
    ]
    
    if not recovery_data.empty:
        country_recovery = recovery_data.groupby('geo')['obs_value'].mean().reset_index()
        country_recovery = country_recovery.dropna()
        
        if not country_recovery.empty:
            country_mapping = {
                'ES': 'ESP', 'IT': 'ITA', 'FR': 'FRA', 'DE': 'DEU', 'PT': 'PRT', 
                'EL': 'GRC', 'HR': 'HRV', 'AT': 'AUT', 'NL': 'NLD', 'BE': 'BEL',
                'PL': 'POL', 'CZ': 'CZE', 'HU': 'HUN', 'RO': 'ROU', 'BG': 'BGR',
                'SK': 'SVK', 'SI': 'SVN', 'FI': 'FIN', 'DK': 'DNK', 'SE': 'SWE',
                'IE': 'IRL', 'LU': 'LUX', 'MT': 'MLT', 'CY': 'CYP', 'EE': 'EST',
                'LV': 'LVA', 'LT': 'LTU'
            }
            
            country_names = {
                'ES': 'Spain', 'IT': 'Italy', 'FR': 'France', 'DE': 'Germany', 'PT': 'Portugal', 
                'EL': 'Greece', 'HR': 'Croatia', 'AT': 'Austria', 'NL': 'Netherlands', 'BE': 'Belgium',
                'PL': 'Poland', 'CZ': 'Czechia', 'HU': 'Hungary', 'RO': 'Romania', 'BG': 'Bulgaria',
                'SK': 'Slovakia', 'SI': 'Slovenia', 'FI': 'Finland', 'DK': 'Denmark', 'SE': 'Sweden',
                'IE': 'Ireland', 'LU': 'Luxembourg', 'MT': 'Malta', 'CY': 'Cyprus', 'EE': 'Estonia',
                'LV': 'Latvia', 'LT': 'Lithuania'
            }
            
            map_data = []
            for _, row in country_recovery.iterrows():
                geo_code = row['geo']
                if geo_code in country_mapping:
                    recovery_val = row['obs_value']
                    
                    # Add journalism context for recovery performance
                    if recovery_val >= 20:
                        performance = "EXCEPTIONAL"
                        context = "Tourism boom - far above pre-pandemic"
                        color_category = "exceptional"
                    elif recovery_val >= 10:
                        performance = "STRONG"
                        context = "Solid growth above 2019 levels"
                        color_category = "strong"
                    elif recovery_val >= 0:
                        performance = "RECOVERED"
                        context = "Back to pre-pandemic levels"
                        color_category = "recovered"
                    elif recovery_val >= -10:
                        performance = "STRUGGLING"
                        context = "Still below pre-pandemic levels"
                        color_category = "struggling"
                    else:
                        performance = "LAGGING"
                        context = "Significant recovery challenges"
                        color_category = "lagging"
                    
                    map_data.append({
                        'iso_alpha': country_mapping[geo_code],
                        'country': country_names.get(geo_code, geo_code),
                        'recovery': recovery_val,
                        'performance': performance,
                        'context': context,
                        'recovery_display': f"{recovery_val:+.1f}%",
                        'color_category': color_category
                    })
            
            map_df = pd.DataFrame(map_data)
            
            if not map_df.empty:
                best_performer = map_df.loc[map_df['recovery'].idxmax()]
                worst_performer = map_df.loc[map_df['recovery'].idxmin()]
                
                # Set fixed range for better color visualization: -15% to +15%
                color_min = -15
                color_max = 15
                
                # Create a capped version for color mapping
                map_df['recovery_capped'] = map_df['recovery'].clip(lower=color_min, upper=color_max)
                
                # Create choropleth map with journalism-grade storytelling
                fig = px.choropleth(
                    map_df,
                    locations='iso_alpha',
                    color='recovery_capped',  # Use capped version for colors
                    hover_name='country',
                    hover_data={
                        'recovery_display': True,
                        'performance': True, 
                        'context': True,
                        'iso_alpha': False,
                        'recovery': False,
                        'recovery_capped': False
                    },
                    color_continuous_scale=[
                        [0.0, '#D32F2F'],    # Red - Strong negative recovery (-15%)
                        [0.2, '#FFCDD2'],    # Light red - Moderate negative recovery
                        [0.4, '#FFEBEE'],    # Very light pink - Small negative recovery
                        [0.5, '#F5F5F5'],    # Neutral gray - Zero recovery
                        [0.6, '#E8F5E8'],    # Very light green - Small positive recovery
                        [0.8, '#C8E6C9'],    # Light green - Moderate positive recovery
                        [1.0, '#4CAF50']     # Green - Strong positive recovery (+15%)
                    ],
                    range_color=[color_min, color_max],
                    labels={
                        'recovery_capped': '2024 Performance vs 2019 (%)',
                        'recovery_display': 'Performance',
                        'performance': 'Recovery Level',
                        'context': 'Tourism Status'
                    }
                )
                
                # Focus on Europe with journalism-appropriate styling
                fig.update_geos(
                    projection_type="natural earth",
                    showocean=True, oceancolor="#E6F3FF",  # Softer blue for professional look
                    showlakes=True, lakecolor="#E6F3FF",
                    showland=True, landcolor="#F5F5F5",    # Neutral gray for non-data countries
                    showcountries=True, countrycolor="#CCCCCC",  # Subtle borders
                    fitbounds="locations",
                    resolution=50,
                    scope='europe'
                )
                
                # Add data source and credibility (keep only this annotation)
                fig.add_annotation(
                    x=0.98, y=0.02,
                    xref="paper", yref="paper",
                    text="Source: Eurostat Official Tourism Statistics<br>Data: 2024 performance vs 2019 baseline<br>Analysis: Average annual tourism growth",
                    showarrow=False,
                    align="right",
                    bgcolor="rgba(255,255,255,0.8)",
                    bordercolor="#CCCCCC",
                    borderwidth=1,
                    font=dict(size=11, color="#666666", family="Arial")
                )
                
                # Update layout for journalism standards
                fig.update_layout(
                    title={
                        'text': '<b>EU TOURISM: THE GREAT RECOVERY</b><br><span style="font-size:18px">2024 performance shows who bounced back strongest</span>',
                        'x': 0.5,
                        'xanchor': 'center',
                        'y': 0.95,
                        'font': {'size': 28, 'color': '#1A1A1A', 'family': 'Arial Black'}
                    },
                    font={'size': 14, 'color': '#2C3E50', 'family': 'Arial'},
                    paper_bgcolor='white',
                    plot_bgcolor='white',
                    width=1800,
                    height=1400,
                    margin=dict(t=120, b=80, l=60, r=60),
                    coloraxis_colorbar={
                        'title': {
                            'text': '<b>2024 vs 2019 (%)</b><br>Red = Below 2019<br>Green = Above 2019', 
                            'font': {'size': 16, 'family': 'Arial Black'}
                        },
                        'tickfont': {'size': 14, 'family': 'Arial'},
                        'len': 0.6,
                        'thickness': 25,
                        'x': 1.02,
                        'tickmode': 'array',
                        'tickvals': [-15, -10, -5, 0, 5, 10, 15],
                        'ticktext': ['-15%', '-10%', '-5%', '0%', '+5%', '+10%', '+15%']
                    }
                )
                
                fig.write_image(os.path.join(OUTPUT_DIR, 'recovery_2024_map_journalism.png'), width=1800, height=1400, scale=2)
                
def chart2_recovery_trajectory_professional(df):
    
    # European Union recovery data
    recovery_data = df[
        (df['geo'] == 'EU27_2020') &
        (df['unit'] == 'PCH_SM_19') &
        (df['nace_r2'] == 'I551-I553') &
        (df['c_resid'] == 'TOTAL') &
        (df['year'].between(2020, 2024))
    ]
    
    if not recovery_data.empty:
        monthly_recovery = recovery_data.groupby('date')['obs_value'].mean()
        
        fig, ax = plt.subplots(figsize=(18, 12))
        fig.patch.set_facecolor(PROFESSIONAL_COLORS['background'])
        
        recovery_color = PROFESSIONAL_COLORS['primary_blue']
        baseline_color = PROFESSIONAL_COLORS['primary_red']
        
        ax.plot(monthly_recovery.index, monthly_recovery.values, 
               color=recovery_color, linewidth=5, marker='o', markersize=10,
               markerfacecolor='white', markeredgecolor=recovery_color, 
               markeredgewidth=3, alpha=0.9, zorder=3)
        
        ax.axhline(y=0, color=baseline_color, linestyle='--', linewidth=3.5, alpha=0.8,
                  label='Pre-Pandemic Baseline (2019)', zorder=2)
        
        crisis_bg = '#FFD6D6'      # More visible light red tint for crisis
        recovery_bg = '#D6E8FF'    # More visible light blue tint for recovery
        
        ax.axvspan(pd.to_datetime('2020-03'), pd.to_datetime('2021-06'), 
                  alpha=0.6, color=crisis_bg, label='Crisis Period', zorder=1)
        ax.axvspan(pd.to_datetime('2023-01'), pd.to_datetime('2024-12'), 
                  alpha=0.6, color=recovery_bg, label='Full Recovery Period', zorder=1)
        
        ax.set_title('European Tourism Recovery Trajectory\nPerformance vs Pre-Pandemic Baseline (2019)', 
                    fontsize=26, fontweight='bold', pad=35, color=PROFESSIONAL_COLORS['text_primary'])
        ax.set_xlabel('Year', fontsize=18, color=PROFESSIONAL_COLORS['text_secondary'])
        ax.set_ylabel('Performance vs 2019 Baseline (%)', fontsize=18, color=PROFESSIONAL_COLORS['text_secondary'])
        
        legend = ax.legend(loc='lower right', frameon=True, fancybox=True, 
                          shadow=True, fontsize=14, framealpha=0.95)
        legend.get_frame().set_facecolor(PROFESSIONAL_COLORS['background'])
        legend.get_frame().set_edgecolor(PROFESSIONAL_COLORS['silver'])
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(PROFESSIONAL_COLORS['silver'])
        ax.spines['bottom'].set_color(PROFESSIONAL_COLORS['silver'])
        ax.spines['left'].set_linewidth(1.5)
        ax.spines['bottom'].set_linewidth(1.5)
        
        ax.grid(True, alpha=0.4, linestyle='-', linewidth=1.0, color=PROFESSIONAL_COLORS['grid'], zorder=0)
        ax.set_axisbelow(True)
        
        ax.tick_params(axis='both', which='major', labelsize=14, colors=PROFESSIONAL_COLORS['text_secondary'])
        ax.tick_params(axis='both', length=8, width=1.5, color=PROFESSIONAL_COLORS['silver'])
        
        ax.annotate('Full Recovery\nAchieved', 
                   xy=(pd.to_datetime('2023-01'), 0), 
                   xytext=(pd.to_datetime('2021-09'), 15),
                   arrowprops=dict(arrowstyle='->', color='#4A4A4A', lw=3),
                   fontsize=14, ha='center', color='#4A4A4A', fontweight='bold',
                   bbox=dict(boxstyle="round,pad=0.5", facecolor=PROFESSIONAL_COLORS['background'], 
                            edgecolor='#4A4A4A', alpha=0.9, linewidth=2))
        
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, 'recovery_trajectory.png'), dpi=300, bbox_inches='tight', 
                   facecolor=PROFESSIONAL_COLORS['background'], edgecolor='none', pad_inches=0.3)
        plt.show()

def chart3_country_performance_professional(df):     
    # EU countries (consistent with official EU statistics)
    eu27_countries = ['ES', 'IT', 'FR', 'DE', 'NL', 'PT', 'EL', 'HR', 'CY', 'MT',
                     'PL', 'CZ', 'HU', 'DK', 'SE', 'AT', 'BE', 'RO', 'BG', 'SK', 
                     'SI', 'FI', 'IE', 'LU', 'EE', 'LV', 'LT']
    
    # 2024 performance data
    performance_data = df[
        (df['geo'].isin(eu27_countries)) &
        (df['unit'] == 'PCH_SM_19') &
        (df['nace_r2'] == 'I551-I553') &
        (df['c_resid'] == 'TOTAL') &
        (df['year'] == 2024)
    ]
    
    if not performance_data.empty:
        performance = performance_data.groupby('geo')['obs_value'].mean().sort_values(ascending=False)
        performance = performance.dropna()
        
        # EU country names
        country_names = {
            'ES': 'Spain', 'IT': 'Italy', 'FR': 'France', 'DE': 'Germany', 'NL': 'Netherlands',
            'PT': 'Portugal', 'EL': 'Greece', 'HR': 'Croatia', 'CY': 'Cyprus', 'MT': 'Malta',
            'PL': 'Poland', 'CZ': 'Czechia', 'HU': 'Hungary', 'DK': 'Denmark', 'SE': 'Sweden',
            'AT': 'Austria', 'BE': 'Belgium', 'RO': 'Romania', 'BG': 'Bulgaria', 'SK': 'Slovakia',
            'SI': 'Slovenia', 'FI': 'Finland', 'IE': 'Ireland', 'LU': 'Luxembourg', 'EE': 'Estonia',
            'LV': 'Latvia', 'LT': 'Lithuania'
        }
        
        fig, ax = plt.subplots(figsize=(16, 12))
        fig.patch.set_facecolor(PROFESSIONAL_COLORS['background'])
        
        colors = []
        for x in performance.values:
            if x < 0: 
                colors.append('#C85450')                             # Same light red as COVID chart for negative
            elif x > 15: 
                colors.append(PROFESSIONAL_COLORS['primary_green'])     # Exceptional - darkest green
            elif x > 10: 
                colors.append(PROFESSIONAL_COLORS['secondary_green'])   # Strong - medium green
            elif x > 5: 
                colors.append('#5A9B6A')                             # Good - lighter green
            else: 
                colors.append('#7BB88A')                             # Modest - lightest green
        
        bars = ax.barh([country_names.get(geo, geo) for geo in performance.index], 
                      performance.values, color=colors, alpha=0.85, height=0.75,
                      edgecolor='white', linewidth=1.5)
        
        for i, (geo, value) in enumerate(performance.items()):
            if value > 0:
                label_x = value - 0.3  # Position inside the bar for positive values
                ha = 'right'
                color = 'white'  # White text on colored bars
            else:
                label_x = value + 0.3  # Position inside the bar for negative values  
                ha = 'left'
                color = 'white'  # White text on colored bars
            ax.text(label_x, i, f'{value:+.1f}%', 
                   va='center', ha=ha, fontweight='bold', fontsize=12, 
                   color=color)
        
        ax.axvline(x=0, color=PROFESSIONAL_COLORS['primary_red'], linestyle='-', 
                  linewidth=3, alpha=0.8, zorder=2)
        
        ax.set_title('Market Performance in 2024 vs Pre-Pandemic Baseline\nPercentage Change Compared to 2019 Performance', 
                    fontsize=24, fontweight='bold', pad=30, color=PROFESSIONAL_COLORS['text_primary'])
        ax.set_xlabel('Performance vs 2019 Baseline (%)', fontsize=18, color=PROFESSIONAL_COLORS['text_secondary'])
        ax.set_ylabel('Market', fontsize=18, color=PROFESSIONAL_COLORS['text_secondary'])
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(PROFESSIONAL_COLORS['silver'])
        ax.spines['bottom'].set_color(PROFESSIONAL_COLORS['silver'])
        ax.spines['left'].set_linewidth(1.5)
        ax.spines['bottom'].set_linewidth(1.5)
        
        ax.grid(axis='x', alpha=0.4, linestyle='-', linewidth=1.0, color=PROFESSIONAL_COLORS['grid'], zorder=0)
        ax.set_axisbelow(True)
        
        ax.tick_params(axis='both', which='major', labelsize=12, colors=PROFESSIONAL_COLORS['text_secondary'])
        ax.tick_params(axis='x', length=8, width=1.5, color=PROFESSIONAL_COLORS['silver'])
        ax.tick_params(axis='y', length=0)
        
        legend_elements = [
            plt.Rectangle((0,0),1,1, facecolor=PROFESSIONAL_COLORS['primary_green'], alpha=0.85, label='Exceptional Growth (>15%)'),
            plt.Rectangle((0,0),1,1, facecolor=PROFESSIONAL_COLORS['secondary_green'], alpha=0.85, label='Strong Growth (10-15%)'),
            plt.Rectangle((0,0),1,1, facecolor='#5A9B6A', alpha=0.85, label='Good Growth (5-10%)'),
            plt.Rectangle((0,0),1,1, facecolor='#7BB88A', alpha=0.85, label='Modest Growth (0-5%)'),
            plt.Rectangle((0,0),1,1, facecolor='#C85450', alpha=0.85, label='Below Baseline (<0%)')
        ]
        legend = ax.legend(handles=legend_elements, loc='upper right', frameon=True, 
                          fancybox=True, shadow=True, fontsize=12, framealpha=0.95)
        legend.get_frame().set_facecolor(PROFESSIONAL_COLORS['background'])
        legend.get_frame().set_edgecolor(PROFESSIONAL_COLORS['silver'])
        
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, '3_country_performance.png'), dpi=300, bbox_inches='tight', 
                   facecolor=PROFESSIONAL_COLORS['background'], edgecolor='none', pad_inches=0.3)
        plt.show()

def chart4_accommodation_sectors_professional(df):
    
    # Accommodation sector data
    sector_data = df[
        (df['nace_r2'].isin(['I551', 'I552', 'I553'])) &
        (df['unit'] == 'PCH_SM_19') &
        (df['c_resid'] == 'TOTAL') &
        (df['year'] == 2024)
    ]
    
    if not sector_data.empty:
        sector_performance = sector_data.groupby('nace_r2')['obs_value'].mean()
        
        sector_names = {
            'I553': 'Camping &\nOutdoor Tourism',
            'I552': 'Holiday Rentals &\nShort-term Stays', 
            'I551': 'Hotels &\nTraditional Lodging'
        }
        
        ordered_sectors = ['I553', 'I552', 'I551']
        values = [sector_performance[sector] for sector in ordered_sectors]
        names = [sector_names[sector] for sector in ordered_sectors]
        
        fig, ax = plt.subplots(figsize=(14, 12))
        fig.patch.set_facecolor(PROFESSIONAL_COLORS['background'])
        
        # Beautiful gradient colors - warm to cool representing growth levels
        colors = ['#2ECC71',    # Emerald green - Camping (highest growth, positive growth)
                 '#4ECDC4',     # Turquoise - Holiday Rentals (medium growth, modern)
                 '#45B7D1']     # Sky blue - Hotels (traditional, stable)
        
        bars = ax.bar(names, values, color=colors, alpha=0.9, width=0.6,
                     edgecolor='white', linewidth=2.5)
        
        for bar, value in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 4, 
                   f'+{value:.0f}%', ha='center', va='bottom', 
                   fontweight='bold', fontsize=18, color=PROFESSIONAL_COLORS['text_primary'])
        
        ax.set_title('Accommodation Sector Performance in 2024\nGrowth vs Pre-Pandemic Baseline (2019)', 
                    fontsize=24, fontweight='bold', pad=35, color=PROFESSIONAL_COLORS['text_primary'])
        ax.set_ylabel('Growth vs 2019 Baseline (%)', fontsize=18, color=PROFESSIONAL_COLORS['text_secondary'])
        ax.set_xlabel('Accommodation Sector', fontsize=18, color=PROFESSIONAL_COLORS['text_secondary'])
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(PROFESSIONAL_COLORS['silver'])
        ax.spines['bottom'].set_color(PROFESSIONAL_COLORS['silver'])
        ax.spines['left'].set_linewidth(1.5)
        ax.spines['bottom'].set_linewidth(1.5)
        
        ax.grid(axis='y', alpha=0.4, linestyle='-', linewidth=1.0, color=PROFESSIONAL_COLORS['grid'], zorder=0)
        ax.set_axisbelow(True)
        ax.set_ylim(0, max(values) * 1.25)
        
        ax.tick_params(axis='both', which='major', labelsize=14, colors=PROFESSIONAL_COLORS['text_secondary'])
        ax.tick_params(axis='y', length=8, width=1.5, color=PROFESSIONAL_COLORS['silver'])
        ax.tick_params(axis='x', length=0)
        
        ax.annotate('Outdoor Tourism\nRevolution', 
                   xy=(0, values[0]), 
                   xytext=(1, values[0] * 0.7),
                   arrowprops=dict(arrowstyle='->', color='#4A4A4A', lw=3),
                   fontsize=15, ha='center', color='#4A4A4A', fontweight='bold',
                   bbox=dict(boxstyle="round,pad=0.5", facecolor=PROFESSIONAL_COLORS['background'], 
                            edgecolor='#4A4A4A', alpha=0.9, linewidth=2))
        
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, '4_accommodation_sectors.png'), dpi=300, bbox_inches='tight', 
                   facecolor=PROFESSIONAL_COLORS['background'], edgecolor='none', pad_inches=0.3)
        plt.show()

def chart5_monthly_tourism_journey(df):
    
    # Get monthly data for 2019 and 2020 only
    monthly_data = df[
        (df['geo'] == 'EU27_2020') &
        (df['unit'] == 'NR') &
        (df['nace_r2'] == 'I551-I553') &
        (df['c_resid'] == 'TOTAL') &
        (df['year'].isin([2019, 2020]))
    ]
    
    if not monthly_data.empty:
        # Group by year and month
        monthly_totals = monthly_data.groupby(['year', 'month'])['obs_value'].sum().reset_index()
        
        # Create C-suite executive visualization
        fig, ax = plt.subplots(figsize=(16, 10))
        fig.patch.set_facecolor(PROFESSIONAL_COLORS['background'])
        
        # Month labels for x-axis
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        # Plot only 2019 and 2020
        years_colors = {
            2019: (PROFESSIONAL_COLORS['charcoal'], 'o', '2019 (Baseline Year)'),
            2020: ('#C85450', 's', '2020 (Crisis Year)')
        }
        
        for year in [2019, 2020]:
            year_data = monthly_totals[monthly_totals['year'] == year].copy()
            if not year_data.empty:
                # Sort by month and ensure we have all 12 months
                year_data = year_data.sort_values('month')
                
                # Get values for each month
                monthly_values = []
                month_numbers = []
                for month in range(1, 13):
                    month_data = year_data[year_data['month'] == month]
                    if not month_data.empty:
                        monthly_values.append(month_data['obs_value'].iloc[0])
                        month_numbers.append(month)
                
                # Plot the line for this year
                color, marker, label = years_colors[year]
                linewidth = 6 if year == 2020 else 5  # Emphasize crisis year slightly more
                markersize = 12 if year == 2020 else 10
                
                ax.plot(month_numbers, monthly_values, 
                       color=color, linewidth=linewidth, marker=marker, markersize=markersize,
                       label=label, alpha=0.9, markerfacecolor='white', 
                       markeredgecolor=color, markeredgewidth=3)
        
        ax.set_title('EU Tourism: 2019 Baseline vs 2020 Crisis\nMonthly Performance Comparison', 
                    fontsize=24, fontweight='bold', pad=30, color=PROFESSIONAL_COLORS['text_primary'])
        ax.set_xlabel('Month', fontsize=18, color=PROFESSIONAL_COLORS['text_secondary'])
        ax.set_ylabel('Tourist Arrivals (Millions)', fontsize=18, color=PROFESSIONAL_COLORS['text_secondary'])
        
        # Set month labels on x-axis
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(months)
        
        legend = ax.legend(loc='upper right', frameon=True, fancybox=True, 
                          shadow=True, fontsize=16, framealpha=0.95)
        legend.get_frame().set_facecolor(PROFESSIONAL_COLORS['background'])
        legend.get_frame().set_edgecolor(PROFESSIONAL_COLORS['silver'])
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(PROFESSIONAL_COLORS['silver'])
        ax.spines['bottom'].set_color(PROFESSIONAL_COLORS['silver'])
        ax.spines['left'].set_linewidth(1.5)
        ax.spines['bottom'].set_linewidth(1.5)
        
        ax.grid(True, alpha=0.4, linestyle='-', linewidth=1.0, color=PROFESSIONAL_COLORS['grid'], zorder=0)
        ax.set_axisbelow(True)
        
        ax.tick_params(axis='both', which='major', labelsize=14, colors=PROFESSIONAL_COLORS['text_secondary'])
        ax.tick_params(axis='both', length=8, width=1.5, color=PROFESSIONAL_COLORS['silver'])
        
        # Get actual data values for annotations
        baseline_2019 = monthly_totals[monthly_totals['year'] == 2019].copy()
        crisis_2020 = monthly_totals[monthly_totals['year'] == 2020].copy()
        
        # Find August 2019 peak (month 8) for summer annotation
        aug_2019 = baseline_2019[baseline_2019['month'] == 8]
        if not aug_2019.empty:
            aug_value = aug_2019['obs_value'].iloc[0]
            ax.annotate('Normal Summer\nPeak Season', 
                       xy=(8, aug_value), 
                       xytext=(10.5, aug_value - 100000000),
                       arrowprops=dict(arrowstyle='->', color='#4A4A4A', lw=2.5),
                       fontsize=14, ha='center', color='#4A4A4A', fontweight='bold',
                       bbox=dict(boxstyle="round,pad=0.5", facecolor=PROFESSIONAL_COLORS['background'], 
                                edgecolor='#4A4A4A', alpha=0.9, linewidth=2))
        
        # Find March 2020 lockdown impact (month 3) for COVID annotation
        mar_2020 = crisis_2020[crisis_2020['month'] == 3]
        if not mar_2020.empty:
            mar_value = mar_2020['obs_value'].iloc[0]
            ax.annotate('COVID-19\nLockdown Impact', 
                       xy=(3, mar_value), 
                       xytext=(1.5, mar_value - 2.5),
                       arrowprops=dict(arrowstyle='->', color='#4A4A4A', lw=2.5),
                       fontsize=14, ha='center', color='#4A4A4A', fontweight='bold',
                       bbox=dict(boxstyle="round,pad=0.5", facecolor=PROFESSIONAL_COLORS['background'], 
                                edgecolor='#4A4A4A', alpha=0.9, linewidth=2))
        
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, '6_monthly_journey.png'), dpi=300, bbox_inches='tight', 
                   facecolor=PROFESSIONAL_COLORS['background'], edgecolor='none', pad_inches=0.3)
        plt.show()

def chart7_domestic_vs_international_recovery(df):
    
    # Get EU domestic and international recovery data
    recovery_data = df[
        (df['geo'] == 'EU27_2020') &
        (df['unit'] == 'PCH_SM_19') &
        (df['nace_r2'] == 'I551-I553') &
        (df['c_resid'].isin(['DOM', 'FOR'])) &
        (df['year'].between(2020, 2024))
    ]
    
    if not recovery_data.empty:
        # Group by year, month, and residence type
        monthly_recovery = recovery_data.groupby(['date', 'c_resid'])['obs_value'].mean().reset_index()
        
        # Create executive visualization
        fig, ax = plt.subplots(figsize=(18, 12))
        fig.patch.set_facecolor(PROFESSIONAL_COLORS['background'])
        
        # Color scheme for domestic vs international - consistent with executive palette
        colors = {
            'DOM': PROFESSIONAL_COLORS['primary_blue'],    # Blue for domestic (consistent)
            'FOR': PROFESSIONAL_COLORS['primary_green']    # Green for international (consistent)
        }
        
        labels = {
            'DOM': 'Domestic Tourism (EU Residents)',
            'FOR': 'International Tourism (Non-EU Visitors)'
        }
        
        # Plot lines for each category
        for c_resid in ['DOM', 'FOR']:
            data_subset = monthly_recovery[monthly_recovery['c_resid'] == c_resid]
            if not data_subset.empty:
                ax.plot(data_subset['date'], data_subset['obs_value'], 
                       color=colors[c_resid], linewidth=5, marker='o', markersize=8,
                       label=labels[c_resid], alpha=0.9, markerfacecolor='white', 
                       markeredgecolor=colors[c_resid], markeredgewidth=3)
        
        # Add baseline and background shading
        ax.axhline(y=0, color=PROFESSIONAL_COLORS['primary_red'], linestyle='--', 
                  linewidth=3, alpha=0.8, label='Pre-Pandemic Baseline (2019)')
        
        # Background periods
        ax.axvspan(pd.to_datetime('2020-03'), pd.to_datetime('2021-06'), 
                  alpha=0.3, color='#FFD6D6', label='Crisis Period', zorder=1)
        
        # Styling
        ax.set_title('Domestic vs International Tourism Recovery\nEU Performance Comparison (2020-2024)', 
                    fontsize=26, fontweight='bold', pad=35, color=PROFESSIONAL_COLORS['text_primary'])
        ax.set_xlabel('Year', fontsize=18, color=PROFESSIONAL_COLORS['text_secondary'])
        ax.set_ylabel('Performance vs 2019 Baseline (%)', fontsize=18, color=PROFESSIONAL_COLORS['text_secondary'])
        
        # Legend
        legend = ax.legend(loc='lower right', frameon=True, fancybox=True, 
                          shadow=True, fontsize=14, framealpha=0.95)
        legend.get_frame().set_facecolor(PROFESSIONAL_COLORS['background'])
        legend.get_frame().set_edgecolor(PROFESSIONAL_COLORS['silver'])
        
        # Executive styling
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(PROFESSIONAL_COLORS['silver'])
        ax.spines['bottom'].set_color(PROFESSIONAL_COLORS['silver'])
        ax.spines['left'].set_linewidth(1.5)
        ax.spines['bottom'].set_linewidth(1.5)
        
        ax.grid(True, alpha=0.4, linestyle='-', linewidth=1.0, color=PROFESSIONAL_COLORS['grid'], zorder=0)
        ax.set_axisbelow(True)
        
        ax.tick_params(axis='both', which='major', labelsize=14, colors=PROFESSIONAL_COLORS['text_secondary'])
        ax.tick_params(axis='both', length=8, width=1.5, color=PROFESSIONAL_COLORS['silver'])
        
        # Get actual data for annotations
        dom_data = monthly_recovery[monthly_recovery['c_resid'] == 'DOM'].copy()
        for_data = monthly_recovery[monthly_recovery['c_resid'] == 'FOR'].copy()
        
        # Key insights annotations - point to actual data
        if not dom_data.empty:
            # Sort domestic data by date
            dom_sorted = dom_data.sort_values('date').reset_index(drop=True)
            
            # Find first 2022 point and go 6 points before (5 + 1 additional)
            dom_2022_mask = dom_sorted['date'].dt.year == 2022
            if dom_2022_mask.any():
                first_2022_pos = dom_2022_mask.idxmax()  # First True index
                target_pos = max(0, first_2022_pos - 6)  # 6 points back instead of 5
                
                dom_date = dom_sorted.iloc[target_pos]['date']
                dom_value = dom_sorted.iloc[target_pos]['obs_value']
                
                ax.annotate('Domestic Tourism\nResilient Recovery', 
                           xy=(dom_date, dom_value), 
                           xytext=(pd.to_datetime('2021-03'), dom_value + 5),  # Lowered from +20 to +5
                           arrowprops=dict(arrowstyle='->', color='#4A4A4A', lw=4,
                                         connectionstyle="arc3,rad=0.2", shrinkA=5, shrinkB=5),
                           fontsize=14, ha='center', color='#4A4A4A', fontweight='bold',
                           bbox=dict(boxstyle="round,pad=0.5", facecolor=PROFESSIONAL_COLORS['background'], 
                                    edgecolor='#4A4A4A', alpha=0.9, linewidth=2))
        
        if not for_data.empty:
            # Sort international data by date
            for_sorted = for_data.sort_values('date').reset_index(drop=True)
            
            # Find first 2023 point and go 1 point after
            for_2023_mask = for_sorted['date'].dt.year == 2023
            if for_2023_mask.any():
                first_2023_pos = for_2023_mask.idxmax()  # First True index
                target_pos = min(len(for_sorted) - 1, first_2023_pos + 1)  # Ensure we don't exceed bounds
                
                for_date = for_sorted.iloc[target_pos]['date']
                for_value = for_sorted.iloc[target_pos]['obs_value']
                
                ax.annotate('International Tourism\nSlower Recovery', 
                           xy=(for_date, for_value), 
                           xytext=(pd.to_datetime('2023-09'), for_value - 20),  # Moved text to the right (Sept 2023)
                           arrowprops=dict(arrowstyle='->', color='#4A4A4A', lw=4,
                                         connectionstyle="arc3,rad=-0.2", shrinkA=5, shrinkB=5),
                           fontsize=14, ha='center', color='#4A4A4A', fontweight='bold',
                           bbox=dict(boxstyle="round,pad=0.5", facecolor=PROFESSIONAL_COLORS['background'], 
                                    edgecolor='#4A4A4A', alpha=0.9, linewidth=2))
        
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, '7_domestic_vs_international.png'), dpi=300, bbox_inches='tight', 
                   facecolor=PROFESSIONAL_COLORS['background'], edgecolor='none', pad_inches=0.3)
        plt.show()

def chart8_seasonal_patterns_comparison(df):
    
    # Get EU monthly data for comparison periods
    seasonal_data = df[
        (df['geo'] == 'EU27_2020') &
        (df['unit'] == 'NR') &
        (df['nace_r2'] == 'I551-I553') &
        (df['c_resid'] == 'TOTAL') &
        (df['year'].isin([2019, 2022, 2023, 2024]))  # Pre-pandemic vs recent years
    ]
    
    if not seasonal_data.empty:
        # Group by year and month
        monthly_totals = seasonal_data.groupby(['year', 'month'])['obs_value'].sum().reset_index()
        
        # Create executive visualization
        fig, ax = plt.subplots(figsize=(18, 12))
        fig.patch.set_facecolor(PROFESSIONAL_COLORS['background'])
        
        # Month labels
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        # Color scheme for different periods
        period_colors = {
            2019: '#34495E',      # Dark gray - Pre-pandemic baseline
            2022: '#F39C12',      # Orange - Early recovery
            2023: '#3498DB',      # Blue - Full recovery
            2024: '#2ECC71'       # Green - Current performance
        }
        
        period_labels = {
            2019: '2019 (Pre-Pandemic Baseline)',
            2022: '2022 (Early Recovery)',
            2023: '2023 (Full Recovery)',
            2024: '2024 (Current Performance)'
        }
        
        # Plot lines for each year
        for year in [2019, 2022, 2023, 2024]:
            year_data = monthly_totals[monthly_totals['year'] == year].copy()
            if not year_data.empty:
                year_data = year_data.sort_values('month')
                
                # Get values for each month
                monthly_values = []
                month_numbers = []
                for month in range(1, 13):
                    month_data = year_data[year_data['month'] == month]
                    if not month_data.empty:
                        monthly_values.append(month_data['obs_value'].iloc[0])
                        month_numbers.append(month)
                
                # Plot styling based on year
                linewidth = 6 if year == 2019 else 4
                alpha = 1.0 if year in [2019, 2024] else 0.8
                linestyle = '--' if year == 2019 else '-'
                
                ax.plot(month_numbers, monthly_values, 
                       color=period_colors[year], linewidth=linewidth, 
                       marker='o', markersize=10 if year in [2019, 2024] else 8,
                       label=period_labels[year], alpha=alpha, 
                       linestyle=linestyle, markerfacecolor='white', 
                       markeredgecolor=period_colors[year], markeredgewidth=3)
        
        # Styling
        ax.set_title('Seasonal Tourism Patterns: Recovery Evolution\nMonthly Performance Comparison (2019 vs 2022-2024)', 
                    fontsize=26, fontweight='bold', pad=35, color=PROFESSIONAL_COLORS['text_primary'])
        ax.set_xlabel('Month', fontsize=18, color=PROFESSIONAL_COLORS['text_secondary'])
        ax.set_ylabel('Tourist Arrivals (Millions)', fontsize=18, color=PROFESSIONAL_COLORS['text_secondary'])
        
        # Set month labels
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(months)
        
        # Legend
        legend = ax.legend(loc='upper left', frameon=True, fancybox=True, 
                          shadow=True, fontsize=14, framealpha=0.95)
        legend.get_frame().set_facecolor(PROFESSIONAL_COLORS['background'])
        legend.get_frame().set_edgecolor(PROFESSIONAL_COLORS['silver'])
        
        # Executive styling
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(PROFESSIONAL_COLORS['silver'])
        ax.spines['bottom'].set_color(PROFESSIONAL_COLORS['silver'])
        ax.spines['left'].set_linewidth(1.5)
        ax.spines['bottom'].set_linewidth(1.5)
        
        ax.grid(True, alpha=0.4, linestyle='-', linewidth=1.0, color=PROFESSIONAL_COLORS['grid'], zorder=0)
        ax.set_axisbelow(True)
        
        ax.tick_params(axis='both', which='major', labelsize=14, colors=PROFESSIONAL_COLORS['text_secondary'])
        ax.tick_params(axis='both', length=8, width=1.5, color=PROFESSIONAL_COLORS['silver'])
        
        # Key insights annotations
        ax.annotate('Summer Peak\nFully Restored', 
                   xy=(7, 120), 
                   xytext=(9, 140),
                   arrowprops=dict(arrowstyle='->', color='#4A4A4A', lw=3),
                   fontsize=14, ha='center', color='#4A4A4A', fontweight='bold',
                   bbox=dict(boxstyle="round,pad=0.5", facecolor=PROFESSIONAL_COLORS['background'], 
                            edgecolor='#4A4A4A', alpha=0.9, linewidth=2))
        
        ax.annotate('Shoulder Seasons\nStronger Than 2019', 
                   xy=(4, 85), 
                   xytext=(2, 110),
                   arrowprops=dict(arrowstyle='->', color='#4A4A4A', lw=3),
                   fontsize=14, ha='center', color='#4A4A4A', fontweight='bold',
                   bbox=dict(boxstyle="round,pad=0.5", facecolor=PROFESSIONAL_COLORS['background'], 
                            edgecolor='#4A4A4A', alpha=0.9, linewidth=2))
        
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, '8_seasonal_patterns.png'), dpi=300, bbox_inches='tight', 
                   facecolor=PROFESSIONAL_COLORS['background'], edgecolor='none', pad_inches=0.3)
        plt.show()

def main():
    
    df = load_data()

    chart5_monthly_tourism_journey(df)
    
    print("1. Creating COVID-19 impact analysis (Executive Version)...")
    chart1_covid_impact_professional(df)
    
    print("1b. Creating COVID-19 impact map (EU Countries)...")
    chart1_covid_impact_map(df)
    
    print("2a. Creating 2024 recovery map (EU Countries)...")
    chart2_recovery_map_journalism(df)
    
    print("2. Creating recovery trajectory analysis (Executive Version)...")
    chart2_recovery_trajectory_professional(df)
    
    print("3. Creating market performance comparison (Executive Version)...")
    chart3_country_performance_professional(df)
    
    print("4. Creating accommodation sector analysis (Executive Version)...")
    chart4_accommodation_sectors_professional(df)
    
    print("7. Creating domestic vs international recovery comparison...")
    chart7_domestic_vs_international_recovery(df)
    
    print("8. Creating seasonal patterns analysis...")
    chart8_seasonal_patterns_comparison(df)

if __name__ == "__main__":
    main()