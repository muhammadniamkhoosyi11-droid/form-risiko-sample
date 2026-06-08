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
st.set_page_config(page_title="Form Risiko Sample V10", page_icon="📝", layout="centered")

# Custom CSS untuk tampilan premium dan komunikatif
st.markdown("""
    <style>
    .main-title { text-align: center; color: #1e3c72; margin-bottom: 0; font-weight: 800; font-size: 26px; }
    .sub-title { text-align: center; font-size: 11px; color: #64748b; margin-bottom: 25px; font-weight: bold; letter-spacing: 1px; }
    .section-cutting { background: linear-gradient(135deg, #1e3c72, #2a5298); color: white; padding: 8px 15px; border-radius: 6px; font-size: 15px; font-weight: bold; margin-top: 15px; margin-bottom: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .section-sewing { background: linear-gradient(135deg, #d35400, #e67e22); color: white; padding: 8px 15px; border-radius: 6px; font-size: 15px; font-weight: bold; margin-top: 15px; margin-bottom: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .section-finishing { background: linear-gradient(135deg, #27ae60, #2ecc71); color: white; padding: 8px 15px; border-radius: 6px; font-size: 15px; font-weight: bold; margin-top: 15px; margin-bottom: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .item-box-fusing { background-color: #f0f4f8; border-left: 4px solid #2196f3; padding: 12px; border-radius: 4px; margin-bottom: 12px; }
    .item-box-sewing { background-color: #fff3e0; border-left: 4px solid #ff9800; padding: 12px; border-radius: 4px; margin-bottom: 12px; }
    .alert-box { background-color: #ffebee; border: 1px solid #ffcdd2; color: #b71c1c; padding: 10px; border-radius: 6px; font-size: 13px; font-weight: 500; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-title'>📋 FORM PARAMETER & RISIKO SAMPLE</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>VERSION 10.0 • INTEGRATED CLOUD DATABASE VIA GOOGLE PORTAL</div>", unsafe_allow_html=True)

st.markdown("""
    <div class='alert-box'>
        ⚠️ <b>PETUNJUK OPERATOR:</b> Pastikan data parameter diisi sesuai aktual trial mesin harian. 
        Setiap data yang diproses otomatis direkam langsung ke sistem pusat cloud office secara terintegrasi!
    </div>
    """, unsafe_allow_html=True)

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
    "SLEVEE AUTO": {"jarum": ["JARUM DP X 17", "JARUM DP X 17 (GB)"], "size": ["7", "8", "9", "11", "12", "13", "30", "34"]},
    "LABEL AUTO": {"jarum": ["JARUM DP X 17", "JARUM DP X 17 (GB)"], "size": ["7", "8", "9", "11", "12", "13", "31", "35"]},
    "BLINDSTITCH": {"jarum": ["JARUM LW X 5T", "JARUM LW X 6T", "JARUM LW X 251 EU", "JARUM LW X 251 EU (GB)"], "size": ["7", "8", "9", "11", "12", "13"]},
    "TN CHAINSTITCH (TNC)": {"jarum": ["JARUM TV X 7", "JARUM TV X 7 (GB)"], "size": ["7", "8", "9", "11", "12", "13"]},
    "DN CHAINSTITCH FRENCH SEAM": {"jarum": ["JARUM TV X 64"], "size": ["7", "8", "9", "11", "12", "13"]},
    "OVERDECK": {"jarum": ["JARUM UY X 128", "JARUM UY X 128 (GB)", "JARUM UY X 128 SAN 10 (GB)"], "size": ["7", "8", "9", "11", "12", "13"]},
    "LUBANG RISK": {"jarum": ["JARUM DO X 558"], "size": ["7", "8", "9", "11", "12", "13"]},
    "SNL_A DURKOPP": {"jarum": ["JARUM DO X 558"], "size": ["7", "8", "9", "11", "12", "13"]},
    "MESIN JAHIT SNAP / KANCING": {"jarum": ["JARUM TQ X 7"], "size": ["7", "8", "9", "11", "12", "13"]},
    "MESIN JAHIT KANSAY": {"jarum": ["JARUM UO X 113"], "size": ["7", "8", "9", "11", "12", "13"]},
    "MESIN BORDIR": {"jarum": ["JARUM DB X K5 (GB)"], "size": ["7", "8", "9", "11", "12", "13"]},
    "JAHIT TANGAN": {"jarum": ["JARUM HANDSEW"], "size": ["7", "8", "9", "11", "12", "13"]},
    "LAIN-LAIN_MANUAL": {"jarum": ["JARUM DB X 1", "JARUM DC X 27", "JARUM DP X 5", "JARUM DP X 17", "JARUM LW X 5T", "JARUM TV X 7", "JARUM UY X 128", "JARUM DO X 558", "JARUM HANDSEW"], "size": ["7", "8", "9", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36"]}
}

# 📝 Identitas Dokumen
artikel = st.text_input("✍️ NAMA ARTIKEL / BUYER", placeholder="CONTOH: DANJYO / CAKRA").upper()

# ==========================================
# A. AREA CUTTING & FUSING
# ==========================================
st.markdown("<div class='section-cutting'>A. AREA CUTTING & FUSING</div>", unsafe_allow_html=True)
op_cutting = st.text_input("👤 Operator Area Cutting", placeholder="Nama lengkap petugas cutting").upper()

col1, col2, col3 = st.columns(3)
with col1:
    jenis_fabric = st.text_input("🧵 Jenis Fabric / Konstruksi", placeholder="Cotton Combed 30s").upper()
with col2:
    metode_gelar = st.selectbox("📋 Metode Gelar Kain", ["GELAR MANUAL (SOLID)", "GELAR MANUAL (MATCHING)", "GELAR OTOMATIS", "LAIN - LAIN"])
with col3:
    metode_potong = st.selectbox("✂️ Metode Potong Kain", ["STRAIGHT KNIFE", "BAND KNIFE", "ROUND KNIFE", "LAIN-LAIN"])

critical_cutting = st.text_area("⚠️ CATATAN KRITIS: Proses Gelar & Potong", placeholder="Tulis instruksi khusus pemotongan di sini agar tidak keliru...").upper()

st.markdown("<p style='color: #2980b9; font-size: 13px; font-weight: bold; margin-bottom: 5px; margin-top: 10px;'>➕ SETTINGAN PARAMETER PROSES FUSING</p>", unsafe_allow_html=True)

if 'fusing_count' not in st.session_state:
    st.session_state.fusing_count = 1

fusing_data = []
for i in range(st.session_state.fusing_count):
    st.markdown(f"<div class='item-box-fusing'>", unsafe_allow_html=True)
    st.markdown(f"<span style='color:#1e3c72; font-weight:bold; font-size:12px;'>⚙️ ITEM FUSING KE-{i+1}</span>", unsafe_allow_html=True)
    
    fus_op = st.text_input(f"Nama Operator Fusing #{i+1}", key=f"fus_op_{i}").upper()
    fcol1, fcol2 = st.columns(2)
    with fcol1:
        fus_inter = st.text_input(f"Jenis Interlining #{i+1}", placeholder="Tricot / Cufner Kain", key=f"fus_inter_{i}").upper()
        fus_msn = st.text_input(f"Mesin Fusing #{i+1}", placeholder="Hashima Continuous", key=f"fus_msn_{i}").upper()
        fus_press = st.text_input(f"Tekanan (Pressure) #{i+1}", placeholder="Misal: 2.5 KG/CM2", key=f"fus_press_{i}").upper()
    with fcol2:
        fus_komp = st.text_input(f"Posisi Komponen #{i+1}", placeholder="Collar / Manset", key=f"fus_komp_{i}").upper()
        fus_suhu = st.number_input(f"Temperatur Fusing (°C) #{i+1}", min_value=0, value=130, key=f"fus_suhu_{i}")
        fus_spd = st.text_input(f"Speed / Waktu #{i+1}", placeholder="Misal: 12 Detik", key=f"fus_spd_{i}").upper()
        
    fus_defect = st.text_area(f"Potensi Cacat & Solusi Fusing #{i+1}", placeholder="CONTOH: Kain keras rawan GLASSING akibat tekanan tinggi", key=f"fus_def_{i}").upper()
    st.markdown("</div>", unsafe_allow_html=True)
    
    fusing_data.append(f"[{fus_komp}]: Op:{fus_op}, Interlining:{fus_inter}, Msn:{fus_msn}, Suhu:{fus_suhu}C, Press:{fus_press}, Speed:{fus_spd}, Defect Note:{fus_defect}")

if st.button("➕ Tambah Komponen Fusing", key="btn_add_fusing"):
    st.session_state.fusing_count += 1
    st.rerun()

# ==========================================
# B. AREA SEWING
# ==========================================
st.markdown("<div class='section-sewing'>B. AREA SEWING (PROSES JAHIT)</div>", unsafe_allow_html=True)
op_sewing = st.text_input("👤 Operator Area Sewing", placeholder="Nama lengkap penanggung jawab jahit").upper()

if 'mesin_count' not in st.session_state:
    st.session_state.mesin_count = 1

sewing_data = []
for i in range(st.session_state.mesin_count):
    st.markdown(f"<div class='item-box-sewing'>", unsafe_allow_html=True)
    st.markdown(f"<span style='color:#d35400; font-weight:bold; font-size:12px;'>🪡 SETTINGAN MESIN JAHIT KE-{i+1}</span>", unsafe_allow_html=True)
    
    sel_mesin = st.selectbox(f"Jenis / Fungsi Mesin #{i+1}", [""] + list(DATABASE_MESIN.keys()), key=f"msn_sel_{i}")
    nama_mesin_final = sel_mesin
    if sel_mesin == "LAIN-LAIN_MANUAL":
        nama_mesin_final = st.text_input(f"Ketik Nama Mesin Manual #{i+1}", key=f"msn_man_{i}").upper()

    jarum_options, size_options, default_size_idx = [""], [""], 0
    if sel_mesin and sel_mesin in DATABASE_MESIN:
        jarum_options = DATABASE_MESIN[sel_mesin]["jarum"] + ["JARUM_LAIN_MANUAL"]
        size_options = DATABASE_MESIN[sel_mesin]["size"]
        if "11" in size_options: default_size_idx = size_options.index("11")
            
    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        sel_jarum = st.selectbox(f"Jenis/Kode Jarum #{i+1}", jarum_options, key=f"jrm_sel_{i}")
        kode_jarum_final = sel_jarum
        if sel_jarum == "JARUM_LAIN_MANUAL":
            kode_jarum_final = st.text_input(f"Ketik Kode Jarum Manual #{i+1}", key=f"jrm_man_{i}").upper()
    with sc2:
        sel_size = st.selectbox(f"Ukuran Jarum #{i+1}", size_options, index=default_size_idx, key=f"size_sel_{i}")
    with sc3:
        inp_spi = st.text_input(f"SPI (Stitch Per Inch) #{i+1}", placeholder="Ex: 12 SPI", key=f"spi_{i}").upper()
    st.markdown("</div>", unsafe_allow_html=True)

    sewing_data.append(f"Msn:{nama_mesin_final}, Jarum:{kode_jarum_final}, Size:{sel_size}, SPI:{inp_spi}")

if st.button("➕ Tambah Pengaturan Mesin Jahit", key="btn_add_sewing"):
    st.session_state.mesin_count += 1
    st.rerun()

col_s1, col_s2 = st.columns(2)
with col_s1:
    song_song = st.text_input("📁 Penggunaan Song-Song (Folder)", placeholder="Contoh: Corong folder 2.5 CM / Tidak Ada").upper()
with col_s2:
    sepatu_spesial = st.text_input("👟 Penggunaan Sepatu Spesial", placeholder="Contoh: Sepatu kelim / Stitch kiri").upper()

critical_sewing = st.text_area("⚠️ CATATAN KRITIS: Alur Proses Jahitan", placeholder="Tulis deskripsi detail bagian rawan loncat, mengkerut, atau jebol di sini...").upper()

# ==========================================
# C. AREA FINISHING PACKING
# ==========================================
st.markdown("<div class='section-finishing'>C. AREA FINISHING & PACKING</div>", unsafe_allow_html=True)
op_finishing = st.text_input("👤 Operator Area Finishing", placeholder="Nama penanggung jawab gosok & packing").upper()

kain_options = [
    "",
    "POLYESTER (TC => COTTON) / ACETATE / ACRYLIC / LYCRA-SPANDEX / NYLON",
    "WOOL / POLYESTER (TC => TETRON) / SILK",
    "TRIACETATE / LINEN / COTTON / VISCOSE-RAYON",
    "JANGAN DIGOSOK (KAIN SENSITIF PANAS)",
    "KAIN LAIN-LAIN (KETIK MANUAL)"
]
jenis_kain = st.selectbox("🧣 Aturan Standar Steam Sesuai Jenis Kain", kain_options)
kain_final = jenis_kain
if jenis_kain == "KAIN LAIN-LAIN (KETIK MANUAL)":
    kain_final = st.text_input("Ketik Jenis Kain Manual").upper()

suhu_default, bar_default, ket_default = 0, "", ""
if "POLYESTER" in kain_final or "ACETATE" in kain_final or "NYLON" in kain_final:
    suhu_default, bar_default, ket_default = 115, "3-5 BAR", "LOW (•)"
elif "WOOL" in kain_final or "SILK" in kain_final:
    suhu_default, bar_default, ket_default = 140, "3-5 BAR", "MEDIUM (••)"
elif "LINEN" in kain_final or "COTTON" in kain_final or "VISCOSE" in kain_final:
    suhu_default, bar_default, ket_default = 170, "3-5 BAR", "HIGH (•••)"
elif "JANGAN DIGOSOK" in kain_final:
    suhu_default, bar_default, ket_default = 0, "NO STEAM", "JANGAN DIGOSOK (X)"

fcol_1, fcol_2 = st.columns(2)
with fcol_1:
    alat_gosok = st.selectbox("🎛️ Alat Gosok Akhir", ["SETRIKA UAP (STEAM IRON)", "HAND IRON BIASA"])
    bar_gosok = st.text_input("💨 Tekanan Steam Aktual (BAR)", value=bar_default).upper()
with fcol_2:
    suhu_gosok = st.number_input("🌡️ Suhu Gosok Aktual (°C)", value=suhu_default)
    st.text_input("🛡️ Rekomendasi Tingkat Panas Otomatis", value=ket_default, disabled=True)

critical_finishing = st.text_area("⚠️ CATATAN KRITIS: Proses Finishing Gosok", placeholder="Tulis instruksi agar kain tidak membekas/kilap/gosong...").upper()
metode_packing = st.text_area("📦 Metode Melipat & Packing", placeholder="Contoh: Lipat standar menggunakan boarding paper ukuran kemeja").upper()


# ==========================================
# PROSES GENERATE PDF
# ==========================================
def generate_pdf_report():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    story, styles = [], getSampleStyleSheet()
    
    title_style = ParagraphStyle('T1', parent=styles['Heading1'], fontSize=15, leading=18, textColor=colors.HexColor('#1e3c72'), alignment=1, spaceAfter=15)
    section_style = ParagraphStyle('S1', parent=styles['Heading2'], fontSize=11, leading=14, textColor=colors.white, backColor=colors.HexColor('#2c3e50'), borderPadding=5, spaceBefore=10, spaceAfter=6)
    label_style = ParagraphStyle('L1', parent=styles['Normal'], fontSize=9, fontName='Helvetica-Bold', textColor=colors.HexColor('#334155'))
    value_style = ParagraphStyle('V1', parent=styles['Normal'], fontSize=9, leading=12, textColor=colors.HexColor('#0f172a'))
    
    story.append(Paragraph("LAPORAN PARAMETER & RISIKO PROSES SAMPLE", title_style))
    master_data = [[Paragraph("ARTIKEL / BUYER :", label_style), Paragraph(artikel if artikel else "-", value_style)]]
    t_master = Table(master_data, colWidths=[120, 430])
    t_master.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 6)]))
    story.append(t_master)
    
    # PDF Section A
    story.append(Paragraph("A. AREA CUTTING & FUSING", section_style))
    cut_data = [
        [Paragraph("OPERATOR CUTTING", label_style), Paragraph(op_cutting if op_cutting else "-", value_style)],
        [Paragraph("FABRIC / KONSTRUKSI", label_style), Paragraph(jenis_fabric if jenis_fabric else "-", value_style)],
        [Paragraph("METODE GELAR / POTONG", label_style), Paragraph(f"{metode_gelar}  /  {metode_potong}", value_style)],
        [Paragraph("CRITICAL NOTE CUTTING", label_style), Paragraph(critical_cutting if critical_cutting else "-", value_style)],
    ]
    t_cut = Table(cut_data, colWidths=[140, 410])
    t_cut.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 4), ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0'))]))
    story.append(t_cut)

    # PDF Section B
    story.append(Paragraph("B. AREA SEWING", section_style))
    sew_f = [
        [Paragraph("OPERATOR SEWING", label_style), Paragraph(op_sewing if op_sewing else "-", value_style)],
        [Paragraph("SONG-SONG / SEPATU", label_style), Paragraph(f"{song_song}  /  {sepatu_spesial}", value_style)],
        [Paragraph("CRITICAL NOTE SEWING", label_style), Paragraph(critical_sewing if critical_sewing else "-", value_style)],
    ]
    t_sew_f = Table(sew_f, colWidths=[140, 410])
    t_sew_f.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 4), ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0'))]))
    story.append(t_sew_f)

    # PDF Section C
    story.append(Paragraph("C. AREA FINISHING PACKING", section_style))
    fin_data = [
        [Paragraph("OPERATOR FINISHING", label_style), Paragraph(op_finishing if op_finishing else "-", value_style)],
        [Paragraph("ATURAN KAIN STEAM", label_style), Paragraph(kain_final if kain_final else "-", value_style)],
        [Paragraph("PARAMETER MONITORING", label_style), Paragraph(f"ALAT: {alat_gosok} | SUHU: {suhu_gosok} °C | STEAM: {bar_gosok}", value_style)],
        [Paragraph("CRITICAL NOTE FINISHING", label_style), Paragraph(critical_finishing if critical_finishing else "-", value_style)],
        [Paragraph("METODE LIPAT & PACKING", label_style), Paragraph(metode_packing if metode_packing else "-", value_style)],
    ]
    t_fin = Table(fin_data, colWidths=[140, 410])
    t_fin.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 4)]))
    story.append(t_fin)
    
    doc.build(story)
    buffer.seek(0)
    return buffer

st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀 PROSES, KIRIM DATA CLOUD & UNDUH PDF", type="primary", use_container_width=True):
    if not artikel:
        st.error("❌ Gagal Simpan! Nama Artikel/Buyer wajib diisi agar tidak tertukar di database pusat.")
    else:
        with st.spinner("⏳ Menghubungkan ke server cloud & merekam data via Google Portal..."):
            try:
                # 🛠️ STRATEGI BYPASS VIA PINTU BELAKANG GOOGLE FORM MAS ANDREAS
                form_url = "https://docs.google.com/forms/d/e/1FAIpQLScZwJVgxBbwh0dVnIKvkU4qVsQ5g-2mQ2MthW83A1zOsEpotw/formResponse"
                
                # Mengemas seluruh laporan teknis pabrik menjadi teks narasi rapi
                teks_laporan_lengkap = f"""
=== A. CUTTING & FUSING ===
• Operator: {op_cutting}
• Jenis Fabric: {jenis_fabric}
• Metode Gelar/Potong: {metode_gelar} / {metode_potong}
• Catatan Kritis Cutting: {critical_cutting}
• Ringkasan Parameter Fusing: {" | ".join(fusing_data)}

=== B. SEWING (JAHIT) ===
• Operator Jahit: {op_sewing}
• Settingan Mesin & SPI: {" | ".join(sewing_data)}
• Perlengkapan (Song2/Sepatu): {song_song} / {sepatu_spesial}
• Catatan Kritis Sewing: {critical_sewing}

=== C. FINISHING & PACKING ===
• Operator Finishing: {op_finishing}
• Standar Kain Steam: {kain_final}
• Parameter Aktual: Alat={alat_gosok}, Suhu={suhu_gosok}°C, Tekanan={bar_gosok}
• Catatan Kritis Finishing: {critical_finishing}
• Metode Melipat & Packing: {metode_packing}
"""
                
                # Menyelaraskan dengan id entry link rahasia milik Mas Andreas
                payload = {
                    "entry.1189946018": artikel,
                    "entry.1323489576": teks_laporan_lengkap.strip()
                }
                
                # Tembak data langsung ke server Google Form (Bypass gembok)
                response = requests.post(form_url, data=payload)
                
                if response.status_code == 200 or response.ok:
                    st.success("✅ BERHASIL 100%! Data harian sukses direkam otomatis di Google Sheets pusat Mas Andreas.")
                else:
                    st.warning("⚠️ Data terkirim, namun server merespon dengan status berbeda. Sila cek berkala file Google Sheets Mas.")
                
                # Siapkan unduhan PDF lokal untuk operator lapangan
                pdf_data = generate_pdf_report()
                st.download_button(
                    label="📥 DOWNLOAD DOKUMEN PDF REKAPAN",
                    data=pdf_data,
                    file_name=f"RISIKO_SAMPLE_{artikel}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"❌ Terjadi gangguan portal: {e}")
                st.warning("Mas tetap bisa mengunduh file PDF lokalnya di bawah ini:")
                pdf_data = generate_pdf_report()
                st.download_button(label="📥 DOWNLOAD DOKUMEN PDF", data=pdf_data, file_name=f"RISIKO_SAMPLE_{artikel}.pdf", mime="application/pdf", use_container_width=True)
