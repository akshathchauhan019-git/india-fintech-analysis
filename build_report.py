"""
Builds India_Fintech_Analysis_Final.pdf — a self-contained, shareable report.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.lines import Line2D
import warnings
warnings.filterwarnings('ignore')

# ── Shared style ────────────────────────────────────────────────────────────
plt.rcParams.update({
    'font.family':        'DejaVu Sans',
    'axes.spines.top':    False,
    'axes.spines.right':  False,
    'axes.grid':          True,
    'grid.alpha':         0.22,
    'grid.linestyle':     '--',
    'figure.facecolor':   'white',
    'axes.facecolor':     '#f8f9fb',
    'axes.labelcolor':    '#333333',
    'xtick.color':        '#555555',
    'ytick.color':        '#555555',
})

C = {
    'primary':    '#635BFF',
    'accent':     '#00D924',
    'red':        '#E25950',
    'orange':     '#F5A623',
    'blue':       '#0073E6',
    'teal':       '#00B5AD',
    'dark':       '#1A1A2E',
    'mid':        '#2D2D44',
    'PhonePe':    '#5F259F',
    'Google Pay': '#4285F4',
    'Paytm':      '#002970',
    'Others':     '#AAAAAA',
    'India':      '#FF6B35',
    'China':      '#E63946',
    'USA':        '#457B9D',
    'Brazil':     '#2DC653',
    'p2p':        '#635BFF',
    'p2m':        '#00D924',
}

# ── Load data ────────────────────────────────────────────────────────────────
DATA = 'data/'
df_upi     = pd.read_csv(DATA + 'upi_monthly.csv',         parse_dates=['date'])
df_share   = pd.read_csv(DATA + 'market_share.csv')
df_funding = pd.read_csv(DATA + 'fintech_funding.csv')
df_pen     = pd.read_csv(DATA + 'digital_penetration.csv')
df_p2m     = pd.read_csv(DATA + 'p2m_split.csv')
df_eco     = pd.read_csv(DATA + 'upi_ecosystem.csv')
df_sector  = pd.read_csv(DATA + 'sector_funding.csv')
df_intl    = pd.read_csv(DATA + 'upi_international.csv')

df_upi['avg_ticket_inr'] = (df_upi['value_bn_inr'] * 1e9) / (df_upi['volume_mn'] * 1e6)
df_upi_annual = df_upi.groupby('year').agg(
    total_volume_mn    = ('volume_mn',       'sum'),
    total_value_bn_inr = ('value_bn_inr',    'sum'),
    avg_ticket_inr     = ('avg_ticket_inr',  'mean'),
).reset_index()
df_upi_annual['yoy_growth'] = df_upi_annual['total_volume_mn'].pct_change() * 100
df_funding['avg_deal_mn']   = df_funding['funding_usd_bn'] * 1000 / df_funding['deal_count']


# ═══════════════════════════════════════════════════════════════════════════
#  Helpers
# ═══════════════════════════════════════════════════════════════════════════
def styled_fig(w=16, h=9):
    fig = plt.figure(figsize=(w, h))
    fig.patch.set_facecolor('white')
    return fig


def section_header(fig, title, subtitle=''):
    fig.text(0.5, 0.97, title,   ha='center', fontsize=17, fontweight='bold', color=C['dark'])
    if subtitle:
        fig.text(0.5, 0.935, subtitle, ha='center', fontsize=10, color='#666666', style='italic')


def rule(fig, y=0.925):
    fig.add_artist(plt.Line2D([0.04, 0.96], [y, y], transform=fig.transFigure,
                              color='#ddddee', linewidth=1.0))


def insight_box(ax, text, loc='lower right'):
    """Light-coloured callout box on an axes."""
    x = 0.98 if 'right' in loc else 0.02
    y = 0.05 if 'lower' in loc else 0.95
    ha = 'right' if 'right' in loc else 'left'
    va = 'bottom' if 'lower' in loc else 'top'
    ax.text(x, y, text, transform=ax.transAxes, fontsize=8, ha=ha, va=va,
            style='italic', color='#444',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#fffbe6',
                      edgecolor='#F5A623', lw=0.8, alpha=0.95))


# ═══════════════════════════════════════════════════════════════════════════
#  PAGE BUILDERS
# ═══════════════════════════════════════════════════════════════════════════

def page_cover():
    fig = plt.figure(figsize=(16, 9))
    fig.patch.set_facecolor(C['dark'])

    # Background accent bar
    bar = fig.add_axes([0, 0.18, 1, 0.005])
    bar.set_facecolor(C['primary'])
    bar.set_xticks([]); bar.set_yticks([])
    for s in bar.spines.values(): s.set_visible(False)

    fig.text(0.5, 0.82, 'INDIA FINTECH MARKET ANALYSIS',
             ha='center', fontsize=32, fontweight='bold', color='white')
    fig.text(0.5, 0.70,
             'UPI Growth  ·  Market Share  ·  Transaction Composition\n'
             'Ecosystem Scale  ·  Funding Landscape  ·  Digital Penetration  ·  Global Expansion',
             ha='center', fontsize=13, color='#BBBBCC', linespacing=1.8)

    # KPI strip
    kpis = [
        ('18.26 Bn',  'UPI transactions\n(Mar 2025)'),
        ('390 Mn',    'Merchant QR\nacceptance points'),
        ('74%',       'Digital payments\npenetration (2024)'),
        ('22+',       'Countries\naccepting UPI'),
        ('$3.1 Bn',   'Fintech funding\n(2024)'),
    ]
    stripe_colors = [C['primary'], C['teal'], C['orange'], C['India'], C['blue']]
    for i, ((val, lbl), col) in enumerate(zip(kpis, stripe_colors)):
        x = 0.04 + i * 0.192
        tile = fig.add_axes([x, 0.22, 0.17, 0.16])
        tile.set_facecolor(col)
        tile.set_xticks([]); tile.set_yticks([])
        for s in tile.spines.values(): s.set_visible(False)
        tile.text(0.5, 0.63, val, ha='center', va='center', transform=tile.transAxes,
                  fontsize=18, fontweight='bold', color='white')
        tile.text(0.5, 0.18, lbl, ha='center', va='center', transform=tile.transAxes,
                  fontsize=8, color='white', alpha=0.9)

    fig.text(0.5, 0.11,
             'Author: Akshath Chauhan  ·  Data Sources: NPCI · RBI · DPIIT · World Bank · Tracxn / Crunchbase aggregates',
             ha='center', fontsize=9, color='#888899')
    fig.text(0.5, 0.07, 'June 2025',
             ha='center', fontsize=9, color='#666677')
    return fig


def page_upi_growth():
    fig = styled_fig()
    section_header(fig, 'UPI Transaction Growth  (2016 – 2025)',
                   'From 0.09 million transactions at launch to 18.26 billion in March 2025 — ~200,000× in under 9 years')
    rule(fig)

    gs = gridspec.GridSpec(2, 2, figure=fig, top=0.90, bottom=0.07,
                           hspace=0.48, wspace=0.32,
                           left=0.07, right=0.97)

    # ── Monthly volume ──────────────────────────────────────────────────────
    ax1 = fig.add_subplot(gs[0, :])
    ax1.fill_between(df_upi['date'], df_upi['volume_mn'] / 1000, alpha=0.12, color=C['primary'])
    ax1.plot(df_upi['date'], df_upi['volume_mn'] / 1000, color=C['primary'], linewidth=2.2)
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:.0f} Bn'))
    ax1.set_ylabel('Monthly Transactions', fontsize=10)
    ax1.set_title('Monthly Transaction Volume — 2016 to 2025', fontsize=12, fontweight='semibold')

    events = [
        ('2016-11-08', 'Demonetisation\n(Nov 2016)',         0.15, 'left'),
        ('2020-03-24', 'COVID Lockdown\n(Mar 2020)',          0.35, 'left'),
        ('2021-10-01', 'UPI One World\n(NRI wallets)',        0.55, 'right'),
        ('2022-09-01', 'UPI Lite &\nCredit on UPI',          0.72, 'left'),
    ]
    ymax = (df_upi['volume_mn'] / 1000).max()
    for ds, lbl, ypos, ha in events:
        xv = pd.Timestamp(ds)
        ax1.axvline(xv, color=C['red'], linestyle=':', alpha=0.45, linewidth=1.4)
        ax1.text(xv, ymax * ypos, lbl, fontsize=7.5, color=C['red'], ha=ha, style='italic',
                 bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.82, edgecolor='none'))

    peak_v = df_upi[df_upi['date'] == pd.Timestamp('2025-03-01')]['volume_mn'].values[0] / 1000
    ax1.scatter([pd.Timestamp('2025-03-01')], [peak_v], color=C['accent'], s=70, zorder=5)
    ax1.text(pd.Timestamp('2025-03-01'), peak_v + 0.5, '18.26 Bn\n(Mar 2025)',
             fontsize=8.5, ha='center', color=C['accent'], fontweight='bold')

    # ── Annual YoY growth ──────────────────────────────────────────────────
    ax2 = fig.add_subplot(gs[1, 0])
    aplot = df_upi_annual[(df_upi_annual['year'] >= 2018) & (df_upi_annual['year'] <= 2024)]
    bc    = [C['primary'] if g > 0 else C['red'] for g in aplot['yoy_growth']]
    bars  = ax2.bar(aplot['year'], aplot['yoy_growth'], color=bc, alpha=0.85, width=0.6, edgecolor='white')
    ax2.axhline(0, color='black', linewidth=0.8)
    ax2.set_ylabel('YoY Growth (%)', fontsize=10)
    ax2.set_title('Annual Volume Growth (2018–2024)', fontsize=11, fontweight='semibold')
    ax2.set_xticks(aplot['year'])
    for bar, val in zip(bars, aplot['yoy_growth']):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
                 f'{val:.0f}%', ha='center', fontsize=8.5, fontweight='bold', color=C['dark'])
    insight_box(ax2, '2017: +7,182% (off-scale)\n2025: partial year (Jan–Mar)')

    # ── Average ticket size ────────────────────────────────────────────────
    ax3 = fig.add_subplot(gs[1, 1])
    af   = df_upi_annual[df_upi_annual['year'].between(2018, 2024)]
    ax3.plot(af['year'], af['avg_ticket_inr'], color=C['orange'], marker='o',
             linewidth=2.2, markersize=8)
    ax3.fill_between(af['year'], af['avg_ticket_inr'], alpha=0.1, color=C['orange'])
    ax3.set_ylabel('Avg Ticket Size (₹)', fontsize=10)
    ax3.set_title('Avg Transaction Value — Democratisation Signal', fontsize=11, fontweight='semibold')
    ax3.set_xticks(af['year'])
    for _, row in af.iterrows():
        ax3.text(row['year'], row['avg_ticket_inr'] + 25, f'₹{row["avg_ticket_inr"]:.0f}',
                 ha='center', fontsize=8.5, color=C['dark'], fontweight='bold')
    insight_box(ax3, 'Falling ticket size = small merchants\n& Tier 2/3 users joining UPI')

    return fig


def page_market_share():
    fig = styled_fig()
    section_header(fig, 'UPI App Market Share  (2021 – 2024)',
                   'PhonePe + Google Pay control ~85% of volume — an effective duopoly')
    rule(fig)

    gs   = gridspec.GridSpec(1, 2, figure=fig, top=0.88, bottom=0.09,
                             wspace=0.35, left=0.07, right=0.97)
    apps  = ['PhonePe', 'Google Pay', 'Paytm', 'Others']
    years = [2021, 2022, 2023, 2024]

    # Stacked bar
    ax1 = fig.add_subplot(gs[0, 0])
    bottoms = [0] * 4
    for app in apps:
        vals = [df_share[(df_share['year']==y) & (df_share['app']==app)]['share_pct'].values[0] for y in years]
        bars = ax1.bar(years, vals, bottom=bottoms, label=app,
                       color=C[app], alpha=0.9, width=0.5, edgecolor='white', linewidth=0.5)
        for bar, v, b in zip(bars, vals, bottoms):
            if v > 5:
                ax1.text(bar.get_x() + bar.get_width()/2, b + v/2, f'{v:.0f}%',
                         ha='center', va='center', fontsize=11, fontweight='bold', color='white')
        bottoms = [b+v for b, v in zip(bottoms, vals)]
    ax1.set_ylim(0, 110)
    ax1.set_ylabel('Market Share (%)', fontsize=10)
    ax1.set_title('Market Share by Transaction Volume', fontsize=12, fontweight='semibold')
    ax1.legend(loc='upper right', framealpha=0.85, fontsize=9)
    ax1.set_xticks(years)
    ax1.annotate('PhonePe + Google Pay\n= 85% of all UPI volume',
                 xy=(2024, 85), xytext=(2021.8, 100),
                 arrowprops=dict(arrowstyle='->', color=C['dark'], lw=1.2),
                 fontsize=8, color=C['dark'],
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#fffbe6', edgecolor=C['orange'], lw=0.8))

    # Trend lines
    ax2 = fig.add_subplot(gs[0, 1])
    for app in ['PhonePe', 'Google Pay', 'Paytm']:
        vals = [df_share[(df_share['year']==y) & (df_share['app']==app)]['share_pct'].values[0] for y in years]
        ax2.plot(years, vals, marker='o', linewidth=2.5, markersize=9, color=C[app], label=app, zorder=3)
        ax2.fill_between(years, vals, alpha=0.06, color=C[app])
        ax2.text(years[-1]+0.1, vals[-1], f'{app}\n{vals[-1]:.0f}%',
                 fontsize=8.5, color=C[app], va='center', fontweight='bold')
    ax2.axvline(2024, color=C['red'], linestyle=':', alpha=0.55, linewidth=1.3)
    ax2.text(2023.88, 9, 'RBI restricts\nPaytm Payments Bank\n(Jan 2024)',
             fontsize=7.5, color=C['red'], ha='right', style='italic',
             bbox=dict(boxstyle='round,pad=0.25', facecolor='white', alpha=0.85, edgecolor='none'))
    ax2.set_ylabel('Market Share (%)', fontsize=10)
    ax2.set_title('Share Trajectory — Where Is the Market Heading?', fontsize=12, fontweight='semibold')
    ax2.set_xticks(years)
    ax2.set_xlim(2020.5, 2025.8)
    ax2.legend(framealpha=0.85, fontsize=9, loc='center left')

    return fig


def page_transaction_composition():
    fig = styled_fig()
    section_header(fig, 'Transaction Composition — The P2P → P2M Structural Shift  (2018 – 2024)',
                   'For the first time in 2024, merchant payments (P2M) crossed 50% of UPI transaction volume')
    rule(fig)

    gs = gridspec.GridSpec(1, 3, figure=fig, top=0.88, bottom=0.10,
                           wspace=0.38, left=0.06, right=0.97)
    years_p2m = df_p2m['year'].tolist()

    # Stacked area
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.stackplot(years_p2m, df_p2m['p2p_pct'], df_p2m['p2m_pct'],
                  labels=['P2P', 'P2M'], colors=[C['p2p'], C['p2m']], alpha=0.75)
    ax1.axhline(50, color='white', linestyle='--', linewidth=1.5, alpha=0.65)
    ax1.text(2021.3, 52, '50% threshold', fontsize=8, color='white', style='italic')
    ax1.annotate('P2M crosses 50%\n(2024)',
                 xy=(2024, 51.9), xytext=(2021.2, 70),
                 arrowprops=dict(arrowstyle='->', color='white', lw=1.2),
                 fontsize=8, color='white',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#333355', alpha=0.85, edgecolor='none'))
    ax1.set_ylim(0, 100); ax1.set_xlim(2018, 2024); ax1.set_xticks(years_p2m)
    ax1.set_ylabel('Share of UPI Volume (%)', fontsize=10)
    ax1.set_title('P2P vs P2M — Volume Share', fontsize=11, fontweight='semibold')
    ax1.legend(loc='upper right', fontsize=8, framealpha=0.5)
    ax1.set_facecolor(C['mid'])

    # Absolute volumes
    ax2 = fig.add_subplot(gs[0, 1])
    merged = df_upi_annual[df_upi_annual['year'].between(2018, 2024)].merge(df_p2m, on='year')
    merged['p2p_vol'] = merged['total_volume_mn'] * merged['p2p_pct'] / 100 / 1000
    merged['p2m_vol'] = merged['total_volume_mn'] * merged['p2m_pct'] / 100 / 1000
    ax2.bar(merged['year'], merged['p2p_vol'], label='P2P', color=C['p2p'], alpha=0.8, width=0.45)
    ax2.bar(merged['year'], merged['p2m_vol'], bottom=merged['p2p_vol'],
            label='P2M', color=C['p2m'], alpha=0.8, width=0.45)
    ax2.set_ylabel('Transaction Volume (Billions)', fontsize=10)
    ax2.set_title('Absolute Volume by Type', fontsize=11, fontweight='semibold')
    ax2.set_xticks(merged['year'])
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:.0f}Bn'))
    ax2.legend(fontsize=9)

    # P2M adoption curve
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.plot(df_p2m['year'], df_p2m['p2m_pct'], color=C['p2m'], marker='o',
             linewidth=2.5, markersize=9, zorder=3)
    ax3.fill_between(df_p2m['year'], df_p2m['p2m_pct'], alpha=0.15, color=C['p2m'])
    ax3.axhline(50, color=C['red'], linestyle='--', linewidth=1.2, alpha=0.6, label='50% line')
    for _, row in df_p2m.iterrows():
        ax3.text(row['year'], row['p2m_pct'] + 1.5, f"{row['p2m_pct']}%",
                 ha='center', fontsize=8.5, color=C['dark'], fontweight='bold')
    ax3.set_ylabel('P2M Share (%)', fontsize=10)
    ax3.set_title('Merchant Payment Adoption Curve', fontsize=11, fontweight='semibold')
    ax3.set_xticks(df_p2m['year']); ax3.set_ylim(0, 70); ax3.legend(fontsize=9)
    insight_box(ax3, '390M merchant QR codes active\nby end-2024 — world\'s largest\nmerchant acceptance network', 'lower right')

    return fig


def page_ecosystem():
    fig = styled_fig()
    section_header(fig, 'UPI Ecosystem Scale  (2017 – 2024)',
                   'Every Indian scheduled bank reachable, 390M merchant QR codes, 1.15 billion registered users')
    rule(fig)

    gs = gridspec.GridSpec(1, 3, figure=fig, top=0.88, bottom=0.10,
                           wspace=0.38, left=0.06, right=0.97)

    # Banks
    ax1 = fig.add_subplot(gs[0, 0])
    bars = ax1.bar(df_eco['year'], df_eco['banks_live'],
                   color=C['blue'], alpha=0.82, width=0.6, edgecolor='white')
    for bar, val in zip(bars, df_eco['banks_live']):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 4,
                 str(val), ha='center', fontsize=9, fontweight='bold', color=C['dark'])
    ax1.set_ylabel('Banks Live on UPI', fontsize=10)
    ax1.set_title('Member Banks on UPI Rail', fontsize=11, fontweight='semibold')
    ax1.set_xticks(df_eco['year'])
    insight_box(ax1, 'Full interoperability:\nany Indian bank account\ncan send/receive via UPI', 'lower right')

    # Merchant QR
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(df_eco['year'], df_eco['merchant_qr_mn'], color=C['p2m'], marker='s',
             linewidth=2.5, markersize=9, zorder=3)
    ax2.fill_between(df_eco['year'], df_eco['merchant_qr_mn'], alpha=0.12, color=C['p2m'])
    for _, row in df_eco.iterrows():
        ax2.text(row['year'], row['merchant_qr_mn'] + 7, f"{row['merchant_qr_mn']:.0f}M",
                 ha='center', fontsize=8, fontweight='bold', color=C['dark'])
    ax2.set_ylabel('Merchant QR Points (Millions)', fontsize=10)
    ax2.set_title('Merchant QR Code Rollout', fontsize=11, fontweight='semibold')
    ax2.set_xticks(df_eco['year'])
    ax2.annotate('~3× jump:\nZero-MDR policy drives\nkirana store adoption',
                 xy=(2022, 78.3), xytext=(2019.5, 180),
                 arrowprops=dict(arrowstyle='->', color=C['dark'], lw=1.2),
                 fontsize=8, color=C['dark'],
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#f0fff4', edgecolor=C['p2m'], lw=0.8))

    # Users
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.plot(df_eco['year'], df_eco['registered_users_mn'], color=C['orange'],
             marker='D', linewidth=2.5, markersize=8, zorder=3)
    ax3.fill_between(df_eco['year'], df_eco['registered_users_mn'], alpha=0.12, color=C['orange'])
    for _, row in df_eco.iterrows():
        ax3.text(row['year'], row['registered_users_mn'] + 20, f"{row['registered_users_mn']:.0f}M",
                 ha='center', fontsize=8, fontweight='bold', color=C['dark'])
    ax3.axhline(900, color='grey', linestyle=':', linewidth=1.1, alpha=0.55)
    ax3.text(2017.2, 918, "India internet users ~900M", fontsize=7.5, color='grey', style='italic')
    ax3.set_ylabel('Registered Users (Millions)', fontsize=10)
    ax3.set_title('Registered User Base', fontsize=11, fontweight='semibold')
    ax3.set_xticks(df_eco['year'])

    return fig


def page_funding():
    fig = styled_fig()
    section_header(fig, 'India Fintech Funding Landscape  (2017 – 2024)',
                   'Post-ZIRP correction complete — 2024 shows recovery with smaller, more disciplined deals')
    rule(fig)

    gs = gridspec.GridSpec(1, 3, figure=fig, top=0.88, bottom=0.11,
                           wspace=0.40, left=0.06, right=0.97)

    # Funding bars
    ax1 = fig.add_subplot(gs[0, 0])
    fc = [C['accent'] if y==2021 else (C['red'] if y in [2022,2023] else C['primary']) for y in df_funding['year']]
    bars = ax1.bar(df_funding['year'], df_funding['funding_usd_bn'],
                   color=fc, alpha=0.88, width=0.6, edgecolor='white')
    for bar, val in zip(bars, df_funding['funding_usd_bn']):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.07,
                 f'${val:.1f}B', ha='center', fontsize=8.5, fontweight='bold', color=C['dark'])
    ax1.annotate('2021 Peak\n(ZIRP / cheap money)', xy=(2021, 8.5), xytext=(2018.5, 7.2),
                 arrowprops=dict(arrowstyle='->', color=C['red'], lw=1.2),
                 fontsize=8, color=C['red'],
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.85, edgecolor='none'))
    ax1.set_ylabel('Funding (USD Billion)', fontsize=10)
    ax1.set_title('Annual Fintech Funding', fontsize=11, fontweight='semibold')
    ax1.set_xticks(df_funding['year']); ax1.tick_params(axis='x', rotation=30)

    # Deal count + funding overlay
    ax2 = fig.add_subplot(gs[0, 1])
    ax2b = ax2.twinx()
    ax2.bar(df_funding['year'], df_funding['deal_count'],
            color=C['blue'], alpha=0.4, width=0.6, label='Deal Count')
    ax2b.plot(df_funding['year'], df_funding['funding_usd_bn'],
              color=C['primary'], marker='o', linewidth=2.5, markersize=8)
    for _, row in df_funding.iterrows():
        ax2b.text(row['year'], row['funding_usd_bn'] + 0.18,
                  f'~${row["avg_deal_mn"]:.0f}M avg', fontsize=6.5,
                  ha='center', color=C['primary'], alpha=0.85)
    ax2.set_ylabel('Number of Deals', fontsize=10)
    ax2b.set_ylabel('Funding (USD Bn)', fontsize=10)
    ax2.set_title('Deal Count vs Funding Value', fontsize=11, fontweight='semibold')
    ax2.set_xticks(df_funding['year']); ax2.tick_params(axis='x', rotation=30)
    handles = [
        mpatches.Patch(color=C['blue'], alpha=0.5, label='Deal Count'),
        mpatches.Patch(color=C['primary'], label='Funding $Bn'),
    ]
    ax2.legend(handles=handles, loc='upper left', fontsize=8.5, framealpha=0.85)

    # Sector donut
    ax3 = fig.add_subplot(gs[0, 2])
    sc = [C['primary'], C['blue'], C['orange'], C['teal'], C['PhonePe'], C['red'], '#AAAAAA']
    wedges, _, autos = ax3.pie(
        df_sector['share_pct'], labels=None, autopct='%1.0f%%',
        colors=sc, startangle=90, pctdistance=0.74,
        wedgeprops=dict(width=0.55, edgecolor='white', linewidth=1.5),
    )
    for at in autos:
        at.set_fontsize(8.5); at.set_fontweight('bold'); at.set_color('white')
    ax3.legend(wedges, df_sector['sector'], loc='lower center',
               bbox_to_anchor=(0.5, -0.22), fontsize=7.5, ncol=2, framealpha=0.85)
    ax3.set_title('2024 Funding by Sub-Sector', fontsize=11, fontweight='semibold')
    ax3.text(0, 0, '$3.1B\nTotal\n2024', ha='center', va='center',
             fontsize=9, fontweight='bold', color=C['dark'])

    return fig


def page_penetration():
    fig = styled_fig()
    section_header(fig, 'Digital Payments Penetration — India vs Global Benchmarks  (2019 – 2024)',
                   'India\'s 21% CAGR dwarfs all peer markets — gap to USA has closed from 44 pp to 13 pp in five years')
    rule(fig)

    gs      = gridspec.GridSpec(1, 3, figure=fig, top=0.88, bottom=0.10,
                                wspace=0.38, left=0.06, right=0.97)
    yrs     = [2019, 2020, 2021, 2022, 2023, 2024]
    marks   = {'India': 'o', 'China': 's', 'USA': 'D', 'Brazil': '^'}
    countries = ['India', 'China', 'USA', 'Brazil']

    # Trend
    ax1 = fig.add_subplot(gs[0, 0])
    for country in countries:
        data = df_pen[df_pen['country'] == country].sort_values('year')
        lw   = 3.0 if country == 'India' else 2.0
        ax1.plot(data['year'], data['penetration_pct'],
                 marker=marks[country], linewidth=lw,
                 markersize=9 if country == 'India' else 7,
                 color=C[country], label=country, zorder=3 if country=='India' else 2)
        last = data[data['year'] == 2024]
        ax1.text(2024.12, last['penetration_pct'].values[0],
                 f"{country}  {last['penetration_pct'].values[0]}%",
                 fontsize=8.5, color=C[country], va='center', fontweight='bold')
    ax1.set_ylabel('Population Using Digital Payments (%)', fontsize=10)
    ax1.set_title('Penetration Rate by Country', fontsize=11, fontweight='semibold')
    ax1.set_xlim(2018.5, 2026.2); ax1.set_xticks(yrs)
    ax1.legend(framealpha=0.85, fontsize=9)

    # Gap closing
    ax2 = fig.add_subplot(gs[0, 1])
    india_d = df_pen[df_pen['country']=='India'].set_index('year')
    china_d = df_pen[df_pen['country']=='China'].set_index('year')
    usa_d   = df_pen[df_pen['country']=='USA'].set_index('year')
    g_china = china_d['penetration_pct'] - india_d['penetration_pct']
    g_usa   = usa_d['penetration_pct']   - india_d['penetration_pct']
    ax2.fill_between(g_china.index, g_china.values, alpha=0.18, color=C['China'])
    ax2.fill_between(g_usa.index,   g_usa.values,   alpha=0.18, color=C['USA'])
    ax2.plot(g_china.index, g_china.values, color=C['China'], linewidth=2.5, marker='s', label='Gap vs China')
    ax2.plot(g_usa.index,   g_usa.values,   color=C['USA'],   linewidth=2.5, marker='D', label='Gap vs USA')
    for yr in yrs:
        ax2.text(yr, g_china[yr]+0.8, f'{g_china[yr]:.0f}pp',
                 ha='center', fontsize=7.5, color=C['China'], fontweight='bold')
        ax2.text(yr, g_usa[yr]-2.8, f'{g_usa[yr]:.0f}pp',
                 ha='center', fontsize=7.5, color=C['USA'], fontweight='bold')
    ax2.set_ylabel('Penetration Gap (pp)', fontsize=10)
    ax2.set_title("India's Closing Gap vs China & USA", fontsize=11, fontweight='semibold')
    ax2.legend(framealpha=0.85, fontsize=9); ax2.set_xticks(yrs)

    # CAGR bar
    ax3 = fig.add_subplot(gs[0, 2])
    cagr = {}
    for c in countries:
        d = df_pen[df_pen['country']==c].set_index('year')
        cagr[c] = ((d.loc[2024,'penetration_pct'] / d.loc[2019,'penetration_pct']) ** (1/5) - 1) * 100
    cdf = pd.DataFrame.from_dict(cagr, orient='index', columns=['cagr']).reset_index()
    cdf.columns = ['country', 'cagr']
    cdf = cdf.sort_values('cagr', ascending=True)
    bars = ax3.barh(cdf['country'], cdf['cagr'],
                    color=[C[c] for c in cdf['country']],
                    alpha=0.85, height=0.5, edgecolor='white')
    for bar, (_, row) in zip(bars, cdf.iterrows()):
        ax3.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                 f'+{row["cagr"]:.1f}% CAGR', va='center', fontsize=9,
                 fontweight='bold', color=C[row['country']])
    ax3.set_xlabel('Penetration CAGR 2019–2024', fontsize=10)
    ax3.set_title('5-Year Penetration CAGR', fontsize=11, fontweight='semibold')
    ax3.set_xlim(0, 28)
    insight_box(ax3, 'India CAGR 21% — fastest growing\ndigital payments market globally')

    return fig


def page_global():
    fig = styled_fig()
    section_header(fig, 'UPI Goes Global — International Expansion  (2022 – 2025)',
                   '22+ countries now accept UPI; top remittance corridors carry $120B+/year')
    rule(fig)

    gs = gridspec.GridSpec(1, 2, figure=fig, top=0.88, bottom=0.10,
                           wspace=0.38, left=0.07, right=0.97)

    # Country count
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(df_intl['year'], df_intl['countries'], color=C['India'],
             marker='o', linewidth=2.5, markersize=11, zorder=3)
    ax1.fill_between(df_intl['year'], df_intl['countries'], alpha=0.12, color=C['India'])
    for _, row in df_intl.iterrows():
        ax1.text(row['year'], row['countries'] + 0.4, str(row['countries']),
                 ha='center', fontsize=10, fontweight='bold', color=C['India'])
    ax1.set_ylabel('Countries Accepting UPI', fontsize=10)
    ax1.set_title('UPI International Footprint', fontsize=11, fontweight='semibold')
    ax1.set_xlim(2021.5, 2025.8); ax1.set_xticks(df_intl['year'])

    milestones = [
        (2022, 1,  'Bhutan: first\ninternational launch', 'left'),
        (2023, 8,  'France (Eiffel Tower\npilot)', 'right'),
        (2025, 22, 'G20 cross-border\npush', 'right'),
    ]
    for yr, cnt, lbl, ha in milestones:
        off = 0.6 if ha == 'right' else -0.6
        ax1.annotate(lbl, xy=(yr, cnt), xytext=(yr + off, cnt + 3.5),
                     arrowprops=dict(arrowstyle='->', color=C['dark'], lw=1.1),
                     fontsize=8, color=C['dark'],
                     bbox=dict(boxstyle='round,pad=0.25', facecolor='#fff3e0',
                               edgecolor=C['India'], lw=0.7))

    # Remittance corridors
    ax2 = fig.add_subplot(gs[0, 1])
    corridors = ['UAE', 'USA', 'UK', 'Singapore', 'Saudi Arabia']
    remit     = [18.0, 22.0, 10.5, 4.2, 11.3]
    live      = [True, False, True, True, False]
    bclr = [C['India'] if e else '#CCCCCC' for e in live]
    bars = ax2.barh(corridors, remit, color=bclr, alpha=0.87, height=0.5, edgecolor='white')
    for bar, val, enabled in zip(bars, remit, live):
        lbl = f'${val:.1f}B  {"✓ UPI live" if enabled else "○ Not yet"}'
        ax2.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                 lbl, va='center', fontsize=9,
                 color=C['India'] if enabled else '#999999')
    ax2.set_xlabel('India Remittance Inflow (USD Bn, FY2024 est.)', fontsize=10)
    ax2.set_title('Top Remittance Corridors — UPI Coverage', fontsize=11, fontweight='semibold')
    ax2.set_xlim(0, 30)
    handles = [mpatches.Patch(color=C['India'],  alpha=0.87, label='UPI accepted'),
               mpatches.Patch(color='#CCCCCC',   alpha=0.87, label='Not yet live')]
    ax2.legend(handles=handles, fontsize=9, framealpha=0.85)
    insight_box(ax2, 'India receives ~$120B/yr\nin remittances. UPI coverage\ncould cut fees from 5–7% to ~0')

    return fig


def page_dashboard():
    fig = plt.figure(figsize=(16, 9))
    fig.patch.set_facecolor(C['dark'])

    fig.text(0.5, 0.968, 'India Fintech Market — Executive Dashboard',
             ha='center', fontsize=21, fontweight='bold', color='white')
    fig.text(0.5, 0.940,
             'Akshath Chauhan  ·  NPCI · RBI · DPIIT · Industry Reports  ·  June 2025',
             ha='center', fontsize=9, color='#AAAAAA')
    fig.add_artist(plt.Line2D([0.03, 0.97], [0.928, 0.928],
                              transform=fig.transFigure, color='#444466', linewidth=0.8))

    kpis = [
        ('18.26 Bn',  'UPI Transactions\n(Mar 2025)',      C['primary']),
        ('₹23.82 Tn', 'Monthly UPI Value\n(Mar 2025)',     C['teal']),
        ('48%',       'PhonePe Market\nShare (2024)',       C['PhonePe']),
        ('74%',       'Digital Payments\nPenetration',      C['orange']),
        ('390 Mn',    'Merchant QR\nAcceptance Points',     C['p2m']),
        ('22+',       'Countries\nAccepting UPI',           C['India']),
        ('$3.1 Bn',   'Fintech Funding\n(2024)',            C['blue']),
        ('427',       'Banks Live\non UPI Rail',            C['red']),
    ]
    tw = 0.106
    for i, (val, lbl, col) in enumerate(kpis):
        x = 0.022 + i * (tw + 0.011)
        ax = fig.add_axes([x, 0.775, tw, 0.135])
        ax.set_facecolor(col)
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values(): s.set_visible(False)
        ax.text(0.5, 0.63, val, ha='center', va='center', transform=ax.transAxes,
                fontsize=15, fontweight='bold', color='white')
        ax.text(0.5, 0.18, lbl, ha='center', va='center', transform=ax.transAxes,
                fontsize=7.5, color='white', alpha=0.92)

    # Mini: UPI volume
    ax_v = fig.add_axes([0.02, 0.07, 0.30, 0.65])
    ax_v.set_facecolor('#1e1e2e')
    recent = df_upi[df_upi['year'] >= 2022]
    ax_v.fill_between(recent['date'], recent['volume_mn']/1000, alpha=0.25, color=C['primary'])
    ax_v.plot(recent['date'], recent['volume_mn']/1000, color=C['primary'], linewidth=1.8)
    ax_v.set_title('UPI Monthly Volume (2022–2025)', color='white', fontsize=10, pad=7)
    ax_v.tick_params(colors='white', labelsize=7.5)
    ax_v.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:.0f}Bn'))
    ax_v.set_ylabel('Transactions', color='#AAAAAA', fontsize=8.5)
    for s in ax_v.spines.values(): s.set_color('#444')
    ax_v.grid(color='#333', linestyle='--', alpha=0.4)

    # Mini: P2M
    ax_p = fig.add_axes([0.36, 0.07, 0.28, 0.65])
    ax_p.set_facecolor('#1e1e2e')
    ax_p.stackplot(df_p2m['year'], df_p2m['p2p_pct'], df_p2m['p2m_pct'],
                   colors=[C['primary'], C['p2m']], alpha=0.72)
    ax_p.axhline(50, color='white', linestyle=':', linewidth=1.1, alpha=0.5)
    ax_p.set_title('P2P vs P2M Share (2018–2024)', color='white', fontsize=10, pad=7)
    ax_p.tick_params(colors='white', labelsize=7.5)
    ax_p.set_ylim(0, 100)
    ax_p.set_ylabel('Share of Volume (%)', color='#AAAAAA', fontsize=8.5)
    for s in ax_p.spines.values(): s.set_color('#444')
    ax_p.grid(color='#333', linestyle='--', alpha=0.4)
    ax_p.legend(handles=[mpatches.Patch(color=C['primary'], alpha=0.72, label='P2P'),
                          mpatches.Patch(color=C['p2m'],    alpha=0.72, label='P2M')],
                fontsize=8, framealpha=0.35, labelcolor='white', facecolor='#2a2a40', loc='upper right')

    # Mini: Funding
    ax_f = fig.add_axes([0.68, 0.07, 0.30, 0.65])
    ax_f.set_facecolor('#1e1e2e')
    fc = [C['accent'] if y==2021 else (C['red'] if y in [2022,2023] else C['primary']) for y in df_funding['year']]
    ax_f.bar(df_funding['year'], df_funding['funding_usd_bn'], color=fc, alpha=0.88, width=0.6)
    ax_f.set_title('Fintech Funding by Year (USD Bn)', color='white', fontsize=10, pad=7)
    ax_f.tick_params(colors='white', labelsize=7.5)
    ax_f.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:.0f}B'))
    ax_f.set_ylabel('USD Billion', color='#AAAAAA', fontsize=8.5)
    for s in ax_f.spines.values(): s.set_color('#444')
    ax_f.grid(color='#333', linestyle='--', alpha=0.4)
    ax_f.tick_params(axis='x', rotation=30)

    return fig


def page_takeaways():
    fig = styled_fig(16, 10)
    fig.patch.set_facecolor(C['dark'])
    fig.text(0.5, 0.955, 'Key Takeaways & Strategic Outlook',
             ha='center', fontsize=20, fontweight='bold', color='white')
    fig.add_artist(plt.Line2D([0.04, 0.96], [0.935, 0.935],
                              transform=fig.transFigure, color='#444466', linewidth=0.8))

    points = [
        (C['primary'],   '01', 'UPI is the world\'s largest real-time payments rail',
         'At 18.26 Bn transactions/month (Mar 2025), UPI exceeds PayPal\'s annual volume circa 2020. '
         'It processes more transactions per month than Visa + Mastercard combined in many recent months.'),
        (C['p2m'],       '02', 'The P2M crossover (51.9% in 2024) redefines the infrastructure requirement',
         'UPI is no longer a transfer tool — it is the primary merchant payments rail for 1.4 billion people. '
         'Merchant-grade challenges: settlement disputes, chargebacks, GST reconciliation, now at UPI scale.'),
        (C['PhonePe'],   '03', 'Effective duopoly — but not permanent',
         'PhonePe + Google Pay = 85%. Paytm fell 11% → 6% in 3 years from regulatory & trust shocks. '
         'A third entrant (Amazon Pay, WhatsApp Pay, CRED) gaining real share within 3–5 years is plausible.'),
        (C['orange'],    '04', 'Merchant QR (390M) is the world\'s largest informal acceptance network',
         'Zero-MDR policy unlocked what decades of card POS terminal incentives could not. '
         'Any policy reversal on MDR would be an acute ecosystem disruption.'),
        (C['India'],     '05', 'UPI\'s 22-country expansion targets $120B+/year in diaspora remittances',
         'Major corridors (UAE, Singapore, UK) are live. Covering USA + Saudi Arabia would capture '
         '~$33B more at near-zero transfer cost vs incumbent 5–7% wire transfer fees.'),
        (C['blue'],      '06', 'Fintech funding normalised — discipline, not exit',
         '$3.1B in 2024 with smaller avg deal size signals a market selecting for unit-economics-positive '
         'businesses. Survivors of 2022–2023 compression are stronger IPO/Series C candidates.'),
        (C['teal'],      '07', '26 percentage points of penetration headroom remain',
         'Concentrated in rural, 60+ age, and feature-phone-only segments. '
         'Next leg requires: offline UPI (UPI Lite X), assisted digital (BC agents), vernacular UX.'),
    ]

    total = len(points)
    col_h = 0.88 / total
    for i, (col, num, title, body) in enumerate(points):
        y = 0.915 - i * col_h - col_h * 0.1

        # Number badge
        badge = fig.add_axes([0.03, y, 0.045, col_h * 0.72])
        badge.set_facecolor(col)
        badge.set_xticks([]); badge.set_yticks([])
        for s in badge.spines.values(): s.set_visible(False)
        badge.text(0.5, 0.5, num, ha='center', va='center', transform=badge.transAxes,
                   fontsize=14, fontweight='bold', color='white')

        # Title + body
        fig.text(0.085, y + col_h * 0.50, title,
                 fontsize=10.5, fontweight='bold', color='white', va='center')
        fig.text(0.085, y + col_h * 0.12, body,
                 fontsize=8.5, color='#AAAACC', va='center', wrap=True)

        # Divider
        if i < total - 1:
            fig.add_artist(plt.Line2D([0.03, 0.97], [y - 0.005, y - 0.005],
                                      transform=fig.transFigure, color='#2a2a44', linewidth=0.7))

    fig.text(0.5, 0.025,
             'Data: NPCI · RBI · DPIIT · World Bank · Tracxn/Crunchbase. '
             '2025 figures reflect partial year (Jan–Mar). International remittance figures are estimates.',
             ha='center', fontsize=7.5, color='#666677')
    return fig


# ═══════════════════════════════════════════════════════════════════════════
#  ASSEMBLE PDF
# ═══════════════════════════════════════════════════════════════════════════
OUT = 'outputs/India_Fintech_Analysis_Final.pdf'

with PdfPages(OUT) as pdf:
    pages = [
        ('Cover',                    page_cover),
        ('UPI Growth',               page_upi_growth),
        ('Market Share',             page_market_share),
        ('Transaction Composition',  page_transaction_composition),
        ('Ecosystem Scale',          page_ecosystem),
        ('Funding Landscape',        page_funding),
        ('Global Penetration',       page_penetration),
        ('UPI Goes Global',          page_global),
        ('Executive Dashboard',      page_dashboard),
        ('Key Takeaways',            page_takeaways),
    ]
    for name, builder in pages:
        print(f'  Building: {name}')
        fig = builder()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)

    # PDF metadata
    d = pdf.infodict()
    d['Title']    = 'India Fintech Market Analysis'
    d['Author']   = 'Akshath Chauhan'
    d['Subject']  = 'UPI Growth, Market Share, Funding, Digital Penetration 2016–2025'
    d['Keywords'] = 'UPI, India, Fintech, Payments, NPCI, Digital Payments'
    d['Creator']  = 'Python / matplotlib'

print(f'\nDone → {OUT}')
