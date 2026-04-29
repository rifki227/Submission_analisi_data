import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Customer Analysis Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #f5f7fa;
    }

    /* Header */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        color: white;
    }
    .main-header h1 {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        margin: 0 0 0.5rem 0;
        color: white !important;
    }
    .main-header p {
        margin: 0;
        opacity: 0.85;
        font-size: 0.95rem;
        color: white !important;
    }

    /* Metric cards */
    .metric-row {
        display: flex;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border-top: 4px solid;
        flex: 1;
    }
    .metric-card.purple { border-color: #667eea; }
    .metric-card.pink   { border-color: #f093fb; }
    .metric-card.blue   { border-color: #4facfe; }
    .metric-card.green  { border-color: #43e97b; }
    .metric-card h3 {
        margin: 0 0 0.4rem 0;
        font-size: 0.78rem;
        color: #9ca3af !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .metric-card .value {
        font-size: 2rem;
        font-weight: 700;
        color: #111827 !important;
        line-height: 1;
    }
    .metric-card .label {
        font-size: 0.78rem;
        color: #6b7280 !important;
        margin-top: 0.25rem;
    }

    /* Section */
    .section-card {
        background: white;
        border-radius: 16px;
        padding: 1.75rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        margin-bottom: 1.5rem;
    }
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 0.5rem;
    }
    .section-badge {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white !important;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .section-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.2rem;
        color: #111827 !important;
        margin: 0;
    }
    .section-subtitle {
        color: #6b7280 !important;
        font-size: 0.88rem;
        margin: 0.25rem 0 1.25rem 0;
        font-style: italic;
    }

    /* Insight box */
    .insight-box {
        background: linear-gradient(135deg, #f8f9ff 0%, #f3f0ff 100%);
        border-left: 4px solid #667eea;
        border-radius: 0 10px 10px 0;
        padding: 1rem 1.25rem;
        margin-top: 1rem;
    }
    .insight-box h4 {
        color: #667eea !important;
        margin: 0 0 0.5rem 0;
        font-size: 0.9rem;
        font-weight: 600;
    }
    .insight-box ul {
        margin: 0;
        padding-left: 1.25rem;
    }
    .insight-box ul li {
        color: #374151 !important;
        font-size: 0.88rem;
        margin-bottom: 0.35rem;
        line-height: 1.5;
    }
    .insight-box ul li b {
        color: #111827 !important;
    }

    /* Conclusion box */
    .conclusion-box {
        background: white;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        height: 100%;
    }
    .conclusion-box h4 {
        font-size: 1rem;
        font-weight: 600;
        margin: 0 0 0.75rem 0;
    }
    .conclusion-box ul li {
        color: #374151 !important;
        font-size: 0.88rem;
        margin-bottom: 0.5rem;
        line-height: 1.5;
    }
    .conclusion-box ul li b {
        color: #111827 !important;
    }

    /* Search result table */
    .search-result {
        background: white;
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: white;
        border-right: 1px solid #e5e7eb;
    }
    section[data-testid="stSidebar"] .stMarkdown h2 {
        color: #111827 !important;
        font-size: 1rem;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #9ca3af !important;
        font-size: 0.8rem;
        padding: 1.5rem 0 0.5rem 0;
    }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('customers_dataset.csv')
        df['customer_city']  = df['customer_city'].str.strip().str.title()
        df['customer_state'] = df['customer_state'].str.strip().str.upper()
        return df
    except FileNotFoundError:
        st.error("❌ File customers_dataset.csv tidak ditemukan!")
        st.stop()

customers_df = load_data()
if customers_df is None:
    st.stop()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎛️ Filter & Pencarian")
    st.markdown("---")

    # Filter State
    st.markdown("**📍 Filter by State**")
    all_states = sorted(customers_df['customer_state'].unique())
    selected_states = st.multiselect(
        "Pilih State:",
        options=all_states,
        default=all_states,
        placeholder="Pilih state..."
    )

    st.markdown("---")

    # Filter Kota
    st.markdown("**🏙️ Filter by Kota**")
    available_cities = sorted(
        customers_df[customers_df['customer_state'].isin(selected_states)]['customer_city'].unique()
    )
    selected_cities = st.multiselect(
        "Pilih Kota:",
        options=available_cities,
        default=[],
        placeholder="Semua kota (opsional)..."
    )

    st.markdown("---")

    # Search Customer
    st.markdown("**🔍 Search Customer**")
    search_query = st.text_input(
        "Cari Customer ID:",
        placeholder="Masukkan customer_id...",
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Slider Top N
    st.markdown("**📊 Pengaturan Grafik**")
    top_n = st.slider("Top N Kota ditampilkan:", 5, 20, 10, 1)

    st.markdown("---")
    st.markdown("<small style='color:#9ca3af'>customers_dataset © 2016-2018</small>", unsafe_allow_html=True)

# ── Apply Filter ──────────────────────────────────────────────────────────────
filtered_df = customers_df[customers_df['customer_state'].isin(selected_states)]
if selected_cities:
    filtered_df = filtered_df[filtered_df['customer_city'].isin(selected_cities)]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>📦 Customer Analysis Dashboard</h1>
    <p>Analisis distribusi customer berdasarkan wilayah di Brasil — customers_dataset periode 2016-2018</p>
</div>
""", unsafe_allow_html=True)

# ── Metrics ───────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card purple">
        <h3>Total Customer</h3>
        <div class="value">{filtered_df['customer_id'].nunique():,}</div>
        <div class="label">customer terdaftar</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card pink">
        <h3>Customer Unik</h3>
        <div class="value">{filtered_df['customer_unique_id'].nunique():,}</div>
        <div class="label">unique customer</div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card blue">
        <h3>Total Kota</h3>
        <div class="value">{filtered_df['customer_city'].nunique():,}</div>
        <div class="label">kota tercakup</div>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card green">
        <h3>Total State</h3>
        <div class="value">{filtered_df['customer_state'].nunique():,}</div>
        <div class="label">state tercakup</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Search Result ─────────────────────────────────────────────────────────────
if search_query:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 🔍 Hasil Pencarian Customer")
    result = customers_df[customers_df['customer_id'].str.contains(search_query, case=False, na=False)]
    if len(result) > 0:
        st.success(f"Ditemukan **{len(result)}** customer")
        st.dataframe(result.reset_index(drop=True), use_container_width=True)
    else:
        st.warning("Customer tidak ditemukan.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

# ── Pertanyaan 1 ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-card">
    <div class="section-header">
        <span class="section-badge">Pertanyaan 1</span>
        <p class="section-title">Distribusi Customer per State</p>
    </div>
    <p class="section-subtitle">State mana yang memiliki jumlah customer terdaftar terbanyak dan bagaimana distribusinya terhadap total keseluruhan customer pada customers_dataset periode 2016-2018?</p>
</div>
""", unsafe_allow_html=True)

fig1, ax1 = plt.subplots(figsize=(14, 5))
fig1.patch.set_facecolor('white')
ax1.set_facecolor('#f8f9ff')

state_counts = filtered_df['customer_state'].value_counts()
colors = ['#667eea' if v == state_counts.max() else '#a5b4fc' for v in state_counts.values]

bars = ax1.bar(state_counts.index, state_counts.values, color=colors, alpha=0.9, width=0.6, zorder=3)
ax1.axhline(y=state_counts.mean(), color='#764ba2', linestyle='--', linewidth=1.5,
            label=f'Rata-rata ({state_counts.mean():.0f})', zorder=4)

ax1.set_title('Distribusi Jumlah Customer per State', fontsize=14, fontweight='bold', pad=15, color='#111827')
ax1.set_xlabel('State', fontsize=11, color='#6b7280')
ax1.set_ylabel('Jumlah Customer', fontsize=11, color='#6b7280')
ax1.tick_params(colors='#6b7280')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_color('#e5e7eb')
ax1.spines['bottom'].set_color('#e5e7eb')
ax1.yaxis.grid(True, color='#e5e7eb', zorder=0)
ax1.set_axisbelow(True)

highlight_patch = mpatches.Patch(color='#667eea', label='State tertinggi')
other_patch = mpatches.Patch(color='#a5b4fc', label='State lainnya')
ax1.legend(handles=[highlight_patch, other_patch,
           plt.Line2D([0], [0], color='#764ba2', linestyle='--', label=f'Rata-rata ({state_counts.mean():.0f})')],
           frameon=False, fontsize=9)

plt.tight_layout()
st.pyplot(fig1)

st.markdown("""
<div class="insight-box">
    <h4>📌 Insight Pertanyaan 1</h4>
    <ul>
        <li>State <b>SP (São Paulo)</b> mendominasi dengan 41.746 customer, jauh melampaui state lainnya.</li>
        <li>Hanya <b>4 state</b> yang berada di atas rata-rata: SP, RJ, MG, dan RS.</li>
        <li>State wilayah Utara seperti <b>AC, AP, dan RR</b> memiliki customer paling sedikit — potensi pasar yang belum tergarap.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Pertanyaan 2 ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-card">
    <div class="section-header">
        <span class="section-badge">Pertanyaan 2</span>
        <p class="section-title">Potensi Kota di Luar São Paulo</p>
    </div>
    <p class="section-subtitle">Kota mana di luar São Paulo yang memiliki jumlah customer terdaftar terbesar sebagai indikator potensi ekspansi pasar berdasarkan customers_dataset periode 2016-2018?</p>
</div>
""", unsafe_allow_html=True)

fig2, ax2 = plt.subplots(figsize=(12, 6))
fig2.patch.set_facecolor('white')
ax2.set_facecolor('#f8f9ff')

city_no_sp = filtered_df[filtered_df['customer_city'] != 'Sao Paulo']['customer_city'].value_counts().head(top_n)
colors2 = ['#667eea' if i == 0 else '#a5b4fc' for i in range(len(city_no_sp))]

ax2.barh(city_no_sp.index[::-1], city_no_sp.values[::-1], color=colors2[::-1], alpha=0.9, height=0.6, zorder=3)
ax2.set_title(f'Top {top_n} Kota dengan Customer Terbanyak (Exclude São Paulo)',
              fontsize=14, fontweight='bold', pad=15, color='#111827')
ax2.set_xlabel('Jumlah Customer', fontsize=11, color='#6b7280')
ax2.set_ylabel('Kota', fontsize=11, color='#6b7280')
ax2.tick_params(colors='#6b7280')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_color('#e5e7eb')
ax2.spines['bottom'].set_color('#e5e7eb')
ax2.xaxis.grid(True, color='#e5e7eb', zorder=0)
ax2.set_axisbelow(True)

for i, (val, idx) in enumerate(zip(city_no_sp.values[::-1], city_no_sp.index[::-1])):
    ax2.text(val + 50, i, f'{val:,}', va='center', fontsize=9, color='#374151')

plt.tight_layout()
st.pyplot(fig2)

st.markdown("""
<div class="insight-box">
    <h4>📌 Insight Pertanyaan 2</h4>
    <ul>
        <li><b>Rio de Janeiro</b> menjadi kota paling potensial di luar São Paulo dengan 6.882 customer.</li>
        <li><b>Belo Horizonte</b> (2.773) dan <b>Brasilia</b> (2.131) berada di posisi kedua dan ketiga.</li>
        <li>Kota <b>Curitiba, Campinas, dan Porto Alegre</b> memiliki jumlah customer serupa (1.300–1.500), cocok sebagai target ekspansi jangka menengah.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Conclusion & Recommendation ───────────────────────────────────────────────
st.markdown("### ✅ Conclusion & 🚀 Rekomendasi")
col_c, col_r = st.columns(2)

with col_c:
    st.markdown("""
    <div class="conclusion-box">
        <h4 style="color:#667eea;">✅ Conclusion</h4>
        <ul>
            <li><b>Pertanyaan 1:</b> Berdasarkan customers_dataset periode 2016-2018, SP mendominasi dengan 42% total customer. Hanya 4 state di atas rata-rata, sementara 23 state lainnya masih jauh di bawah rata-rata.</li>
            <li><b>Pertanyaan 2:</b> Berdasarkan customers_dataset periode 2016-2018, Rio de Janeiro adalah kota paling potensial di luar SP, diikuti Belo Horizonte dan Brasilia. Mayoritas kota masih dalam kategori Low Potential.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col_r:
    st.markdown("""
    <div class="conclusion-box">
        <h4 style="color:#764ba2;">🚀 Rekomendasi Action Item</h4>
        <ul>
            <li>Fokuskan 40% anggaran marketing di state <b>SP, RJ, dan MG</b> sebagai wilayah dengan customer terbesar.</li>
            <li>Jadikan <b>Rio de Janeiro</b> sebagai prioritas ekspansi pertama dengan layanan same-day delivery.</li>
            <li>Luncurkan campaign awareness di 23 state yang berada di bawah rata-rata, khususnya wilayah Utara.</li>
            <li>Evaluasi kota Medium Potential (<b>Curitiba, Campinas</b>) setiap kuartal untuk memantau pertumbuhan.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    © 2026 Customer Analysis Dashboard — customers_dataset Olist periode 2016-2018
</div>
""", unsafe_allow_html=True)
