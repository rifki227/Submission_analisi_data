import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Customer Analysis",
    page_icon="📦",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }
    h1, h2, h3 {
        font-family: 'DM Serif Display', serif;
    }
    .metric-card {
        background: #f8f4ef;
        border-left: 4px solid #c8773a;
        padding: 1rem 1.25rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
    }
    .metric-card h3 {
        margin: 0 0 0.25rem 0;
        font-size: 0.85rem;
        color: #888 !important;
        font-family: 'DM Sans', sans-serif;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-card p {
        margin: 0;
        font-size: 1.8rem;
        font-weight: 700;
        color: #1a1a1a !important;
    }
    .insight-box {
        background: #fdf6ee;
        border: 1px solid #e8d5bf;
        border-radius: 10px;
        padding: 1.25rem 1.5rem;
        margin-top: 1rem;
    }
    .insight-box h4 {
        color: #c8773a !important;
        margin-top: 0;
        font-family: 'DM Serif Display', serif;
    }
    .insight-box ul li {
        color: #1a1a1a !important;
    }
    .insight-box ul li b {
        color: #1a1a1a !important;
    }
    .insight-box p {
        color: #1a1a1a !important;
    }
    .section-title {
        font-family: 'DM Serif Display', serif;
        font-size: 1.5rem;
        color: #1a1a1a !important;
        border-bottom: 2px solid #c8773a;
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('customers_dataset.csv')
        df['customer_city'] = df['customer_city'].str.strip().str.title()
        df['customer_state'] = df['customer_state'].str.strip().str.upper()
        return df
    except FileNotFoundError:
        st.error("❌ File tidak ditemukan!")
        st.stop()

customers_df = load_data()

if customers_df is None:
    st.stop()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("# 📦  Customer Analysis Dashboard")
st.markdown("Analisis distribusi customer berdasarkan wilayah di Brasil — dataset Olist E-Commerce.")
st.markdown("---")

# ── Metrics ───────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h3>Total Customer</h3>
        <p>{customers_df['customer_id'].nunique():,}</p>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <h3>Total Kota</h3>
        <p>{customers_df['customer_city'].nunique():,}</p>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <h3>Total State</h3>
        <p>{customers_df['customer_state'].nunique():,}</p>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <h3>Customer Unik</h3>
        <p>{customers_df['customer_unique_id'].nunique():,}</p>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Pertanyaan 1 ──────────────────────────────────────────────────────────────
st.markdown('<p class="section-title">Pertanyaan 1 — Distribusi Customer per State</p>', unsafe_allow_html=True)
st.markdown("*State mana yang memiliki jumlah customer terdaftar terbanyak dan bagaimana distribusinya terhadap total keseluruhan customer?*")

fig1, ax1 = plt.subplots(figsize=(14, 5))
top_state_all = customers_df['customer_state'].value_counts()
ax1.bar(top_state_all.index, top_state_all.values, color='#c8773a', alpha=0.85)
ax1.axhline(y=top_state_all.mean(), color='#1a1a1a', linestyle='--', linewidth=1.5,
            label=f'Rata-rata ({top_state_all.mean():.0f})')
ax1.set_title('Distribusi Jumlah Customer per State', fontsize=14, fontweight='bold', pad=15)
ax1.set_xlabel('State', fontsize=11)
ax1.set_ylabel('Jumlah Customer', fontsize=11)
ax1.legend()
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
plt.tight_layout()
st.pyplot(fig1)

st.markdown("""
<div class="insight-box">
    <h4>📌 Insight</h4>
    <ul>
        <li>State <b>SP (São Paulo)</b> mendominasi dengan 41.746 customer, jauh melampaui state lainnya.</li>
        <li>Hanya <b>4 state</b> yang berada di atas rata-rata (3.683): SP, RJ, MG, dan RS.</li>
        <li>State wilayah Utara seperti AC, AP, dan RR memiliki customer paling sedikit — potensi pasar belum tergarap.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Pertanyaan 2 ──────────────────────────────────────────────────────────────
st.markdown('<p class="section-title">Pertanyaan 2 — Potensi Kota di Luar São Paulo</p>', unsafe_allow_html=True)
st.markdown("*Kota mana di luar São Paulo yang memiliki potensi pertumbuhan customer terbesar?*")

fig2, ax2 = plt.subplots(figsize=(12, 6))
top_city_no_sp = customers_df[customers_df['customer_city'] != 'Sao Paulo']['customer_city'].value_counts().head(10)
ax2.barh(top_city_no_sp.index[::-1], top_city_no_sp.values[::-1], color='#c8773a', alpha=0.85)
ax2.set_title('Top 10 Kota dengan Customer Terbanyak (Exclude São Paulo)', fontsize=14, fontweight='bold', pad=15)
ax2.set_xlabel('Jumlah Customer', fontsize=11)
ax2.set_ylabel('Kota', fontsize=11)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
plt.tight_layout()
st.pyplot(fig2)

st.markdown("""
<div class="insight-box">
    <h4>📌 Insight</h4>
    <ul>
        <li><b>Rio de Janeiro</b> menjadi kota paling potensial di luar São Paulo dengan 6.882 customer.</li>
        <li><b>Belo Horizonte</b> (2.773) dan <b>Brasilia</b> (2.131) berada di posisi kedua dan ketiga.</li>
        <li>Kota Curitiba, Campinas, dan Porto Alegre memiliki jumlah customer serupa (1.300–1.500), sebagai target ekspansi jangka menengah.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Conclusion & Recommendation ───────────────────────────────────────────────
st.markdown('<p class="section-title">Conclusion & Recommendation</p>', unsafe_allow_html=True)

col_c, col_r = st.columns(2)

with col_c:
    st.markdown("""
    <div class="insight-box">
        <h4>✅ Conclusion</h4>
        <ul>
            <li><b>Pertanyaan 1:</b> SP mendominasi dengan 42% total customer. Hanya 4 state di atas rata-rata, sementara 23 state lainnya masih jauh di bawah rata-rata.</li>
            <li><b>Pertanyaan 2:</b> Rio de Janeiro adalah kota paling potensial di luar SP, diikuti Belo Horizonte dan Brasilia. Mayoritas kota masih dalam kategori Low Potential.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col_r:
    st.markdown("""
    <div class="insight-box">
        <h4>🚀 Rekomendasi Action Item</h4>
        <ul>
            <li>Fokuskan 40% anggaran marketing di state SP, RJ, dan MG sebagai wilayah dengan customer terbesar.</li>
            <li>Jadikan <b>Rio de Janeiro</b> sebagai prioritas ekspansi pertama dengan layanan same-day delivery.</li>
            <li>Luncurkan campaign awareness di 23 state yang berada di bawah rata-rata, khususnya wilayah Utara.</li>
            <li>Evaluasi kota Medium Potential (Curitiba, Campinas) setiap kuartal untuk memantau pertumbuhan.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>")
st.markdown("<center><small>© 2026 Olist Customer Analysis Dashboard</small></center>", unsafe_allow_html=True)
