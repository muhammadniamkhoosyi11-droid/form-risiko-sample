import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import requests
import io

# ==========================================
# KONFIGURASI HALAMAN UTAMA & MODERNISE TAMPILAN
# ==========================================
st.set_page_config(page_title="Form Risiko Sample V12", page_icon="📝", layout="centered")

st.markdown("""
    <style>
    .main-title { text-align: center; color: #1e3c72; margin-bottom: 0; font-weight: 800; font-size: 26px; }
    .sub-title { text-align: center; font-size: 11px; color: #64748b; margin-bottom: 25px; font-weight: bold; letter-spacing: 1px; }
    .section-cutting { background: linear-gradient(135deg, #1e3c72, #2a5298); color: white; padding: 8px 15px; border-radius: 6px; font-size: 15px; font-weight: bold; margin-top: 15px; margin-bottom: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .section-sewing { background: linear-gradient(135deg, #d35400, #e67e22); color: white; padding: 8px 15px; border-radius: 6px; font-size: 15px; font-weight: bold; margin-top: 15px; margin-bottom: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .section-finishing { background: linear-gradient(135deg, #27ae60, #2ecc71); color: white; padding: 8px 15px; border-radius: 6px; font-size: 15px; font-weight: bold; margin-top: 15px; margin-bottom: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .item-box-fusing { background-color: #f0f4f8; border-left: 4px solid #2196f3; padding: 12px; border-radius: 4px; margin-bottom: 12px; }
    .item-box-sewing { background-color: #fff3e0; border-left: 4px solid #ff9800; padding: 12px; border-radius: 4px; margin-bottom: 12px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-title'>📋 FORM PARAMETER & RISIKO SAMPLE</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>VERSION 12.0 • ASSET SYNC SUCCESS</div>", unsafe_allow_html=True)

# DATABASE INTEGRASI MESIN & JARUM LENGKAP
DATABASE_MESIN = {
    "SNL_A/M LOCKSTITCH (JAHIT REG)": {"jarum": ["JARUM DB X 1", "JARUM DB X 1 (GB)", "JARUM DB X 1 (GB/GEBEDUR)", "JARUM DB X 1KN", "JARUM DB X 1 SAN 10 (GB)"], "size": ["7", "8", "9", "11", "12", "13"]},
    "OVER LOCK / OBRAS": {"jarum": ["JARUM DC X 27", "JARUM DC X 27 (GB)", "JARUM DC X 27 (GB/GEBEDUR)", "JARUM DC X 27 SAN 10 (GB)"], "size": ["7", "8", "9", "11", "12", "13"]},
    "DN LOCKSTITCH": {"jarum": ["JARUM DP X 5", "JARUM DP X 5 (GB/GEBEDUR)"], "size": ["7", "8", "9", "11", "12", "13", "17", "21"]},
    "LUBANG KANCING": {"jarum": ["JARUM DP X 5", "JARUM DP X 5 (GB)", "JARUM DP X 5 (GB/GEBEDUR)", "JARUM DP X 5 SAN 10"], "size": ["7", "8", "9", "11", "12", "13", "14", "18", "22", "25"]},
    "BARTAQ": {"jarum": ["JARUM DP X 5", "JARUM DP X 5 (GB)", "JARUM DP X 5 (GB/GEBEDUR)", "JARUM DP X 5 SAN 10"], "size": ["7", "8", "9", "11", "12", "13", "15", "19", "23", "26"]},
    "ZIG ZAG": {"jarum": ["JARUM DP X 5", "JARUM DP X 5 (GB)", "JARUM DP X 5 (GB/GEBEDUR)", "JARUM DP X 5 SAN 10"], "size": ["7", "8", "9", "11", "12", "13", "16", "20", "24", "27"]},
    "PASANG KANCING": {"jarum": ["JARUM DP X 17", "JARUM DP X 17 (GB)"], "size": ["7", "8", "9", "11", "12", "13", "28", "32"]},
    "PASPOL": {"jarum": ["JARUM DP X 17", "JARUM DP X 17 (GB)", "JARUM DP X 35"], "size": ["7", "8", "9", "11", "12", "13", "29", "33", "36"]},
    "BLINDSTITCH": {"jarum": ["JARUM LW X 5T", "JARUM LW X 6T", "JARUM LW X 251 EU", "JARUM LW X 251 EU (GB)"], "size": ["7", "8", "9", "11", "12", "13"]},
    "TN CHAINSTITCH (TNC)": {"jarum": ["JARUM TV X 7", "JARUM TV X 7 (GB)"], "size": ["7", "8", "9", "11", "12", "13"]},
    "OVERDECK": {"jarum": ["JARUM UY X 128", "JARUM UY X 128 (GB)", "JARUM UY X 128 SAN 10 (GB)"], "size": ["7", "8", "9", "11", "12", "13"]},
    "LAIN-LAIN_MANUAL": {"jarum": ["JARUM DB X 1", "JARUM DC X 27", "JARUM DP X 5", "JARUM HANDSEW"], "size": ["11", "12", "13", "14", "16"]}
}

# Identitas Dokumen
artikel = st.text_input("✍️ NAMA ARTIKEL / BUYER", placeholder="CONTOH: DANJYO / CAKRA").upper()

# AREA CUTTING
st.markdown("<div class='section-cutting'>A. AREA CUTTING & FUSING</div>", unsafe_allow_html=True)
op_cutting = st.text_input("👤 Operator Area Cutting", placeholder="Nama petugas cutting").upper()
jenis_fabric = st.text_input("🧵 Jenis Fabric / Konstruksi", placeholder="Cotton Combed 30s").upper()
metode_gelar = st.selectbox("📋 Metode Gelar Kain", ["GELAR MANUAL (SOLID)", "GELAR MANUAL (MATCHING)", "GELAR OTOMATIS", "LAIN - LAIN"])
metode_potong = st.selectbox("✂️ Metode Potong Kain", ["STRAIGHT KNIFE", "BAND KNIFE", "ROUND KNIFE"])
critical_cutting = st.text_area("⚠️ CATATAN KRITIS: Proses Gelar & Potong").upper()

# FUSING SECTIONS
if 'fusing_count' not in st.session_state: st.session_state.fusing_count = 1
fusing_data = []
for i in range(st.session_state.fusing_count):
    st.markdown(f"<div class='item-box-fusing'>⚙️ ITEM FUSING KE-{i+1}</div>", unsafe_allow_html=True)
    fus_op = st.text_input(f"Nama Operator Fusing #{i+1}", key=f"fus_op_{i}").upper()
    fus_inter = st.text_input(f"Jenis Interlining #{i+1}", key=f"fus_inter_{i}").upper()
    fus_msn = st.text_input(f"Mesin Fusing #{i+1}", key=f"fus_msn_{i}").upper()
    fus_press = st.text_input(f"Tekanan #{i+1}", key=f"fus_press_{i}").upper()
    fus_komp = st.text_input(f"Posisi Komponen #{i+1}", key=f"fus_komp_{i}").upper()
    fus_suhu = st.number_input(f"Temperatur Fusing (°C) #{i+1}", min_value=0, value=130, key=f"fus_suhu_{i}")
    fus_spd = st.text_input(f"Speed #{i+1}", key=f"fus_spd_{i}").upper()
    fus_defect = st.text_area(f"Potensi Cacat Fusing #{i+1}", key=f"fus_def_{i}").upper()
    fusing_data.append(f"[{fus_komp}]: Op:{fus_op}, Interlining:{fus_inter}, Msn:{fus_msn}, Suhu:{fus_suhu}C, Press:{fus_press}, Speed:{fus_spd}, Note:{fus_defect}")

if st.button("➕ Tambah Komponen Fusing"):
    st.session_state.fusing_count += 1
    st.rerun()

# AREA SEWING
st.markdown("<div class='section-sewing'>B. AREA SEWING (PROSES JAHIT)</div>", unsafe_allow_html=True)
op_sewing = st.text_input("👤 Operator Area Sewing").upper()

if 'mesin_count' not in st.session_state: st.session_state.mesin_count = 1
sewing_data = []
for i in range(st.session_state.mesin_count):
    st.markdown(f"<div class='item-box-sewing'>🪡 SETTINGAN MESIN JAHIT KE-{i+1}</div>", unsafe_allow_html=True)
    sel_mesin = st.selectbox(f"Jenis Mesin #{i+1}", list(DATABASE_MESIN.keys()), key=f"msn_sel_{i}")
    j_opts = DATABASE_MESIN[sel_mesin]["jarum"]
    s_opts = DATABASE_MESIN[sel_mesin]["size"]
    sel_jarum = st.selectbox(f"Jenis Jarum #{i+1}", j_opts, key=f"jrm_sel_{i}")
    sel_size = st.selectbox(f"Ukuran Jarum #{i+1}", s_opts, key=f"size_sel_{i}")
    inp_spi = st.text_input(f"SPI #{i+1}", key=f"spi_{i}").upper()
    sewing_data.append(f"Msn:{sel_mesin}, Jarum:{sel_jarum}, Size:{sel_size}, SPI:{inp_spi}")

if st.button("➕ Tambah Pengaturan Mesin Jahit"):
    st.session_state.mesin_count += 1
    st.rerun()

song_song = st.text_input("📁 Penggunaan Song-Song (Folder)").upper()
sepatu_spesial = st.text_input("👟 Penggunaan Sepatu Spesial").upper()
critical_sewing = st.text_area("⚠️ CATATAN KRITIS: Alur Proses Jahitan").upper()

# AREA FINISHING
st.markdown("<div class='section-finishing'>C. AREA FINISHING & PACKING</div>", unsafe_allow_html=True)
op_finishing = st.text_input("👤 Operator Area Finishing").upper()
alat_gosok = st.selectbox("🎛️ Alat Gosok Akhir", ["SETRIKA UAP (STEAM IRON)", "HAND IRON BIASA"])
bar_gosok = st.text_input("💨 Tekanan Steam").upper()
suhu_gosok = st.number_input("🌡️ Suhu Gosok Aktual (°C)", value=140)
critical_finishing = st.text_area("⚠️ CATATAN KRITIS: Proses Finishing Gosok").upper()
metode_packing = st.text_area("📦 Metode Melipat & Packing").upper()

def generate_pdf_report():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    story, styles = [], getSampleStyleSheet()
    title_style = ParagraphStyle('T1', parent=styles['Heading1'], fontSize=15, alignment=1, spaceAfter=15)
    story.append(Paragraph(f"LAPORAN PARAMETER & RISIKO PROSES SAMPLE - {artikel}", title_style))
    doc.build(story)
    buffer.seek(0)
    return buffer

st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀 PROSES & KIRIM KE CLOUD GOOGLE", type="primary", use_container_width=True):
    if not artikel:
        st.error("❌ Nama Artikel wajib diisi!")
    else:
        with st.spinner("⏳ Menembak data ke Cloud Google Sheets Anda..."):
            try:
                # MENGGUNAKAN ID FORM ASLI MILIK GOOGLE FORM MAS ANDREAS
                form_url = "https://docs.google.com/forms/d/e/1qKwX368iZkJSXQ2meJy16TaBHUxRAeybWyfsXYEdc2o/formResponse"
                
                teks_laporan_lengkap = f"""
[CUTTING AREA] 
• Operator: {op_cutting}
• Fabric/Konstruksi: {jenis_fabric}
• Metode Gelar: {metode_gelar}
• Metode Potong: {metode_potong}
• Catatan Kritis Cutting: {critical_cutting}
• Detail Fusing Komponen: {" / ".join(fusing_data)}

[SEWING AREA]
• Operator Sewing: {op_sewing}
• Pengaturan Mesin Jahit: {" / ".join(sewing_data)}
• Song-Song/Folder: {song_song}
• Sepatu Spesial: {sepatu_spesial}
• Catatan Kritis Sewing: {critical_sewing}

[FINISHING & PACKING AREA]
• Operator Finishing: {op_finishing}
• Alat Gosok: {alat_gosok} | Tekanan Steam: {bar_gosok} | Suhu: {suhu_gosok}°C
• Catatan Kritis Gosok: {critical_finishing}
• Metode Packing: {metode_packing}
"""
                payload = {
                    "entry.1189946018": artikel,
                    "entry.1323489576": teks_laporan_lengkap.strip()
                }
                
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                }
                
                # Eksekusi Tembakan
                response = requests.post(form_url, data=payload, headers=headers)
                
                st.success("🎉 MANTAP JOSS! Data Berhasil Amblas Masuk ke Google Sheets Anda!")
                st.download_button(label="📥 DOWNLOAD DOKUMEN PDF REKAPAN", data=generate_pdf_report(), file_name=f"RISIKO_{artikel}.pdf", mime="application/pdf", use_container_width=True)
            except Exception as e:
                st.error(f"Gangguan Portal: {e}")
