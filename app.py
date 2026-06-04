import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import io

# 1. DATABASE INTEGRASI MESIN & JARUM LENGKAP
DATABASE_MESIN = {
    "SNL_A/M LOCKSTITCH (JAHIT REG)": {
        "jarum": ["JARUM DB X 1", "JARUM DB X 1 (GB)", "JARUM DB X 1 (GB/GEBEDUR)", "JARUM DB X 1KN", "JARUM DB X 1 SAN 10 (GB)"],
        "size": ["7", "8", "9", "11", "12", "13"]
    },
    "OVER LOCK / OBRAS": {
        "jarum": ["JARUM DC X 27", "JARUM DC X 27 (GB)", "JARUM DC X 27 (GB/GEBEDUR)", "JARUM DC X 27 SAN 10 (GB)"],
        "size": ["7", "8", "9", "11", "12", "13"]
    },
    "DN LOCKSTITCH": {
        "jarum": ["JARUM DP X 5", "JARUM DP X 5 (GB/GEBEDUR)"],
        "size": ["7", "8", "9", "11", "12", "13", "17", "21"]
    },
    "LUBANG KANCING": {
        "jarum": ["JARUM DP X 5", "JARUM DP X 5 (GB)", "JARUM DP X 5 (GB/GEBEDUR)", "JARUM DP X 5 SAN 10"],
        "size": ["7", "8", "9", "11", "12", "13", "14", "18", "22", "25"]
    },
    "BARTAQ": {
        "jarum": ["JARUM DP X 5", "JARUM DP X 5 (GB)", "JARUM DP X 5 (GB/GEBEDUR)", "JARUM DP X 5 SAN 10"],
        "size": ["7", "8", "9", "11", "12", "13", "15", "19", "23", "26"]
    },
    "ZIG ZAG": {
        "jarum": ["JARUM DP X 5", "JARUM DP X 5 (GB)", "JARUM DP X 5 (GB/GEBEDUR)", "JARUM DP X 5 SAN 10"],
        "size": ["7", "8", "9", "11", "12", "13", "16", "20", "24", "27"]
    },
    "PASANG KANCING": {
        "jarum": ["JARUM DP X 17", "JARUM DP X 17 (GB)"],
        "size": ["7", "8", "9", "11", "12", "13", "28", "32"]
    },
    "PASPOL": {
        "jarum": ["JARUM DP X 17", "JARUM DP X 17 (GB)", "JARUM DP X 35"],
        "size": ["7", "8", "9", "11", "12", "13", "29", "33", "36"]
    },
    "SLEVEE AUTO": {
        "jarum": ["JARUM DP X 17", "JARUM DP X 17 (GB)"],
        "size": ["7", "8", "9", "11", "12", "13", "30", "34"]
    },
    "LABEL AUTO": {
        "jarum": ["JARUM DP X 17", "JARUM DP X 17 (GB)"],
        "size": ["7", "8", "9", "11", "12", "13", "31", "35"]
    },
    "BLINDSTITCH": {
        "jarum": ["JARUM LW X 5T", "JARUM LW X 6T", "JARUM LW X 251 EU", "JARUM LW X 251 EU (GB)"],
        "size": ["7", "8", "9", "11", "12", "13"]
    },
    "TN CHAINSTITCH (TNC)": {
        "jarum": ["JARUM TV X 7", "JARUM TV X 7 (GB)"],
        "size": ["7", "8", "9", "11", "12", "13"]
    },
    "DN CHAINSTITCH FRENCH SEAM": {
        "jarum": ["JARUM TV X 64"],
        "size": ["7", "8", "9", "11", "12", "13"]
    },
    "OVERDECK": {
        "jarum": ["JARUM UY X 128", "JARUM UY X 128 (GB)", "JARUM UY X 128 SAN 10 (GB)"],
        "size": ["7", "8", "9", "11", "12", "13"]
    },
    "LUBANG RISK": {
        "jarum": ["JARUM DO X 558"],
        "size": ["7", "8", "9", "11", "12", "13"]
    },
    "SNL_A DURKOPP": {
        "jarum": ["JARUM DO X 558"],
        "size": ["7", "8", "9", "11", "12", "13"]
    },
    "MESIN JAHIT SNAP / KANCING": {
        "jarum": ["JARUM TQ X 7"],
        "size": ["7", "8", "9", "11", "12", "13"]
    },
    "MESIN JAHIT KANSAY": {
        "jarum": ["JARUM UO X 113"],
        "size": ["7", "8", "9", "11", "12", "13"]
    },
    "MESIN BORDIR": {
        "jarum": ["JARUM DB X K5 (GB)"],
        "size": ["7", "8", "9", "11", "12", "13"]
    },
    "JAHIT TANGAN": {
        "jarum": ["JARUM HANDSEW"],
        "size": ["7", "8", "9", "11", "12", "13"]
    },
    "LAIN-LAIN_MANUAL": {
        "jarum": ["JARUM DB X 1", "JARUM DC X 27", "JARUM DP X 5", "JARUM DP X 17", "JARUM LW X 5T", "JARUM TV X 7", "JARUM UY X 128", "JARUM DO X 558", "JARUM HANDSEW"],
        "size": ["7", "8", "9", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36"]
    }
}

# Konfigurasi Halaman Utama
st.markdown("<h2 style='text-align: center; color: #1e3c72; margin-bottom: 0;'>FORM PARAMETER & RISIKO SAMPLE</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 12px; color: #64748b; margin-bottom: 25px;'>VERSION 9.7 - STANDALONE LIVE WEB APP</p>", unsafe_allow_html=True)

# Identitas Utama
artikel = st.text_input("ARTIKEL / BUYER", placeholder="CONTOH: DANJYO / CAKRA").upper()

# ==========================================
# A. AREA CUTTING & FUSING
# ==========================================
st.markdown("<h3 style='background-color: #1e3c72; color: white; padding: 6px 12px; border-radius: 4px; font-size: 14px;'>A. AREA CUTTING</h3>", unsafe_allow_html=True)

op_cutting = st.text_input("NAMA OPERATOR AREA CUTTING", placeholder="INPUT NAMA OPERATOR CUTTING").upper()

col1, col2, col3 = st.columns(3)
with col1:
    jenis_fabric = st.text_input("JENIS FABRIC / KONSTRUKSI", placeholder="CONTOH: COTTON COMBED 30S").upper()
with col2:
    metode_gelar = st.selectbox("METODE GELAR", ["GELAR MANUAL (SOLID)", "GELAR MANUAL (MATCHING)", "GELAR OTOMATIS", "LAIN - LAIN"])
with col3:
    metode_potong = st.selectbox("METODE POTONG", ["STRAIGHT KNIFE", "BAND KNIFE", "ROUND KNIFE", "LAIN-LAIN"])

critical_cutting = st.text_area("CRITICAL PROSES GELAR & POTONG (NOTE PERINTAH)", placeholder="INPUT MANUAL CATATAN PROSES CUTTING DI SINI...").upper()

st.markdown("<h4 style='color: #2980b9; font-size: 13px; border-bottom: 1px dashed #3498db; padding-bottom: 3px;'>PROSES FUSING (INTERLINING)</h4>", unsafe_allow_html=True)

if 'fusing_count' not in st.session_state:
    st.session_state.fusing_count = 1

fusing_data = []
for i in range(st.session_state.fusing_count):
    st.markdown(f"<div style='font-weight:bold; font-size:12px; color:#2563eb;'>ITEM FUSING #{i+1}</div>", unsafe_allow_html=True)
    fus_op = st.text_input(f"NAMA OPERATOR AREA FUSING #{i+1}", key=f"fus_op_{i}").upper()
    
    fcol1, fcol2 = st.columns(2)
    with fcol1:
        fus_inter = st.text_input(f"JENIS INTERLINING #{i+1}", placeholder="CONTOH: TRICOT / CUFNER KAIN", key=f"fus_inter_{i}").upper()
        fus_msn = st.text_input(f"MESIN YANG DIPAKAI #{i+1}", placeholder="CONTOH: HASHIMA CONTINUOUS", key=f"fus_msn_{i}").upper()
        fus_press = st.text_input(f"TEKANAN (PRESSURE) #{i+1}", placeholder="MISAL: 2.5 KG/CM2", key=f"fus_press_{i}").upper()
    with fcol2:
        fus_komp = st.text_input(f"POSISI KOMPONEN YANG DI-FUSING #{i+1}", placeholder="CONTOH: COLLAR / MANSET", key=f"fus_komp_{i}").upper()
        fus_suhu = st.number_input(f"TEMPERATUR (°C) #{i+1}", min_value=0, value=130, key=f"fus_suhu_{i}")
        fus_spd = st.text_input(f"SPEED / WAKTU #{i+1}", placeholder="MISAL: 12 DETIK", key=f"fus_spd_{i}").upper()
        
    fus_defect = st.text_area(f"POTENSI DEFECT / CACAT FUSING #{i+1}", placeholder="CONTOH: KAIN KERAS RAWAN GLASSING AKIBAT TEKANAN TINGGI", key=f"fus_def_{i}").upper()
    fusing_data.append({
        "op": fus_op, "interlining": fus_inter, "komponen": fus_komp,
        "mesin": fus_msn, "suhu": fus_suhu, "pressure": fus_press, "speed": fus_spd, "defect": fus_defect
    })

if st.button("+ TAMBAH ITEM FUSING"):
    st.session_state.fusing_count += 1
    st.rerun()

# ==========================================
# B. AREA SEWING
# ==========================================
st.markdown("<br><h3 style='background-color: #d35400; color: white; padding: 6px 12px; border-radius: 4px; font-size: 14px;'>B. AREA SEWING</h3>", unsafe_allow_html=True)

op_sewing = st.text_input("NAMA OPERATOR AREA SEWING", placeholder="INPUT NAMA OPERATOR SEWING").upper()

if 'mesin_count' not in st.session_state:
    st.session_state.mesin_count = 1

sewing_data = []
for i in range(st.session_state.mesin_count):
    st.markdown(f"<div style='font-weight:bold; font-size:12px; color:#ea580c;'>SETTINGAN MESIN SEWING #{i+1}</div>", unsafe_allow_html=True)
    
    mesin_options = [""] + list(DATABASE_MESIN.keys())
    sel_mesin = st.selectbox(f"JENIS / FUNGSI MESIN #{i+1}", mesin_options, key=f"msn_sel_{i}")
    
    nama_mesin_final = sel_mesin
    if sel_mesin == "LAIN-LAIN_MANUAL":
        nama_mesin_final = st.text_input(f"KETIK NAMA FUNGSI MESIN #{i+1}", key=f"msn_man_{i}").upper()

    jarum_options = [""]
    size_options = [""]
    default_size_idx = 0
    
    if sel_mesin and sel_mesin in DATABASE_MESIN:
        jarum_options = DATABASE_MESIN[sel_mesin]["jarum"] + ["JARUM_LAIN_MANUAL"]
        size_options = DATABASE_MESIN[sel_mesin]["size"]
        if "11" in size_options:
            default_size_idx = size_options.index("11")
            
    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        sel_jarum = st.selectbox(f"JENIS/KODE JARUM #{i+1}", jarum_options, key=f"jrm_sel_{i}")
        kode_jarum_final = sel_jarum
        if sel_jarum == "JARUM_LAIN_MANUAL":
            kode_jarum_final = st.text_input(f"KETIK KODE JARUM MANUAL #{i+1}", key=f"jrm_man_{i}").upper()
    with sc2:
        sel_size = st.selectbox(f"UKURAN JARUM #{i+1}", size_options, index=default_size_idx, key=f"size_sel_{i}")
    with sc3:
        inp_spi = st.text_input(f"SPI / STITCHING #{i+1}", placeholder="EX: 12 SPI", key=f"spi_{i}").upper()

    sewing_data.append({
        "mesin": nama_mesin_final, "jarum": kode_jarum_final, "size": sel_size, "spi": inp_spi
    })

if st.button("+ TAMBAH SETTINGAN MESIN"):
    st.session_state.mesin_count += 1
    st.rerun()

col_s1, col_s2 = st.columns(2)
with col_s1:
    song_song = st.text_input("PENGGUNAAN SONG-SONG", placeholder="CONTOH: CORONG FOLDER 2.5 CM / TIDAK ADA").upper()
with col_s2:
    sepatu_spesial = st.text_input("PENGGUNAAN SEPATU SPESIAL", placeholder="CONTOH: SEPATU KELIM / STITCH KIRI").upper()

critical_sewing = st.text_area("CRITICAL PROSES JAHITAN (NOTE DESKRIPSI)", placeholder="INPUT MANUAL CATATAN PROSES SEWING DI SINI...").upper()

# ==========================================
# C. AREA FINISHING PACKING
# ==========================================
st.markdown("<br><h3 style='background-color: #27ae60; color: white; padding: 6px 12px; border-radius: 4px; font-size: 14px;'>C. AREA FINISHING PACKING</h3>", unsafe_allow_html=True)

op_finishing = st.text_input("NAMA OPERATOR AREA FINISHING", placeholder="INPUT NAMA OPERATOR FINISHING").upper()

kain_options = [
    "",
    "POLYESTER (TC => COTTON) / ACETATE / ACRYLIC / LYCRA-SPANDEX / NYLON",
    "WOOL / POLYESTER (TC => TETRON) / SILK",
    "TRIACETATE / LINEN / COTTON / VISCOSE-RAYON",
    "JANGAN DIGOSOK (KAIN SENSITIF PANAS)",
    "KAIN LAIN-LAIN (KETIK MANUAL)"
]
jenis_kain = st.selectbox("JENIS KAIN UTAMA (ATURAN STEAM VALID)", kain_options)

kain_final = jenis_kain
if jenis_kain == "KAIN LAIN-LAIN (KETIK MANUAL)":
    kain_final = st.text_input("KETIK JENIS KAIN MANUAL DISINI").upper()

suhu_default = 0
bar_default = ""
ket_default = ""

if jenis_kain == "POLYESTER (TC => COTTON) / ACETATE / ACRYLIC / LYCRA-SPANDEX / NYLON":
    suhu_default = 115
    bar_default = "3-5 BAR"
    ket_default = "LOW (•)"
elif jenis_kain == "WOOL / POLYESTER (TC => TETRON) / SILK":
    suhu_default = 140
    bar_default = "3-5 BAR"
    ket_default = "MEDIUM (••)"
elif jenis_kain == "TRIACETATE / LINEN / COTTON / VISCOSE-RAYON":
    suhu_default = 170
    bar_default = "3-5 BAR"
    ket_default = "HIGH (•••)"
elif jenis_kain == "JANGAN DIGOSOK (KAIN SENSITIF PANAS)":
    suhu_default = 0
    bar_default = "NO STEAM"
    ket_default = "JANGAN DIGOSOK (X)"

fcol_1, fcol_2 = st.columns(2)
with fcol_1:
    alat_gosok = st.selectbox("ALAT GOSOK AKHIR", ["SETRIKA UAP (STEAM IRON)", "HAND IRON BIASA"])
    bar_gosok = st.text_input("SETTINGAN TEKANAN STEAM (BAR)", value=bar_default).upper()
with fcol_2:
    suhu_gosok = st.number_input("SUHU GOSOK AKTUAL (°C)", value=suhu_default)
    st.text_input("KETERANGAN TINGKAT PANAS AUTOMATIC", value=ket_default, disabled=True)

critical_finishing = st.text_area("CRITICAL PROSES FINISHING (NOTE DESKRIPSI)", placeholder="INPUT MANUAL CATATAN PROSES FINISHING DI SINI...").upper()
metode_packing = st.text_area("METHODE LIPAT DAN PACKING", placeholder="CONTOH: LIPAT STANDAR PAKAI BOARDING PAPER").upper()

# ==========================================
# PROSES GENERATE PDF
# ==========================================
def generate_pdf_report():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('T1', parent=styles['Heading1'], fontSize=15, leading=18, textColor=colors.HexColor('#1e3c72'), alignment=1, spaceAfter=15)
    section_style = ParagraphStyle('S1', parent=styles['Heading2'], fontSize=11, leading=14, textColor=colors.white, backColor=colors.HexColor('#2c3e50'), borderPadding=5, spaceBefore=10, spaceAfter=6)
    label_style = ParagraphStyle('L1', parent=styles['Normal'], fontSize=9, fontName='Helvetica-Bold', textColor=colors.HexColor('#334155'))
    value_style = ParagraphStyle('V1', parent=styles['Normal'], fontSize=9, leading=12, textColor=colors.HexColor('#0f172a'))
    
    story.append(Paragraph("LAPORAN PARAMETER & RISIKO PROSES SAMPLE", title_style))
    
    master_data = [[Paragraph("ARTIKEL / BUYER :", label_style), Paragraph(artikel if artikel else "-", value_style)]]
    t_master = Table(master_data, colWidths=[120, 430])
    t_master.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 6)]))
    story.append(t_master)
    
    # Section A
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
    
    for idx, f in enumerate(fusing_data):
        story.append(Spacer(1, 4))
        story.append(Paragraph(f"<b>• ITEM FUSING #{idx+1}</b>", label_style))
        f_data = [
            [Paragraph("Operator / Komponen", label_style), Paragraph(f"{f['op']} / {f['komponen']}", value_style)],
            [Paragraph("Interlining / Mesin", label_style), Paragraph(f"{f['interlining']} / {f['mesin']}", value_style)],
            [Paragraph("Suhu / Press / Speed", label_style), Paragraph(f"{f['suhu']} °C / {f['pressure']} / {f['speed']}", value_style)],
            [Paragraph("Potensi Defect Note", label_style), Paragraph(f['defect'] if f['defect'] else "AMAN", value_style)],
        ]
        t_f = Table(f_data, colWidths=[140, 410])
        t_f.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('LEFTPADDING', (0,0), (-1,-1), 10), ('BOTTOMPADDING', (0,0), (-1,-1), 3)]))
        story.append(t_f)

    # Section B
    story.append(Paragraph("B. AREA SEWING", section_style))
    sew_master = [[Paragraph("OPERATOR SEWING", label_style), Paragraph(op_sewing if op_sewing else "-", value_style)]]
    t_sew_m = Table(sew_master, colWidths=[140, 410])
    t_sew_m.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 4)]))
    story.append(t_sew_m)
    
    for idx, s in enumerate(sewing_data):
        story.append(Spacer(1, 4))
        story.append(Paragraph(f"<b>• SETTINGAN MESIN #{idx+1}</b>", label_style))
        s_data = [
            [Paragraph("Jenis Mesin / SPI", label_style), Paragraph(f"{s['mesin']} / {s['spi']}", value_style)],
            [Paragraph("Spesifikasi Jarum", label_style), Paragraph(f"KODE: {s['jarum']}  |  SIZE: {s['size']}", value_style)],
        ]
        t_s = Table(s_data, colWidths=[140, 410])
        t_s.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('LEFTPADDING', (0,0), (-1,-1), 10), ('BOTTOMPADDING', (0,0), (-1,-1), 3)]))
        story.append(t_s)
        
    sew_f = [
        [Paragraph("SONG-SONG / SEPATU", label_style), Paragraph(f"{song_song}  /  {sepatu_spesial}", value_style)],
        [Paragraph("CRITICAL NOTE SEWING", label_style), Paragraph(critical_sewing if critical_sewing else "-", value_style)],
    ]
    t_sew_f = Table(sew_f, colWidths=[140, 410])
    t_sew_f.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 4), ('LINEABOVE', (0,0), (-1,0), 0.5, colors.HexColor('#e2e8f0'))]))
    story.append(t_sew_f)

    # Section C
    story.append(Paragraph("C. AREA FINISHING PACKING", section_style))
    fin_data = [
        [Paragraph("OPERATOR FINISHING", label_style), Paragraph(op_finishing if op_finishing else "-", value_style)],
        [Paragraph("ATURAN KAIN STEAM", label_style), Paragraph(kain_final if kain_final else "-", value_style)],
        [Paragraph("PARAMETER MONITORING", label_style), Paragraph(f"ALAT: {alat_gosok} | SUHU: {suhu_gosok} °C | STEAM: {bar_gosok} | LEVEL: {ket_default}", value_style)],
        [Paragraph("CRITICAL NOTE FINISHING", label_style), Paragraph(critical_finishing if critical_finishing else "-", value_style)],
        [Paragraph("METODE LIPAT & PACKING", label_style), Paragraph(metode_packing if metode_packing else "-", value_style)],
    ]
    t_fin = Table(fin_data, colWidths=[140, 410])
    t_fin.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 4), ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0'))]))
    story.append(t_fin)
    
    doc.build(story)
    buffer.seek(0)
    return buffer

st.markdown("<br>", unsafe_allow_html=True)
if st.button("PROSES & UNDUH LAPORAN PDF", type="primary"):
    pdf_data = generate_pdf_report()
    st.download_button(
        label="📥 KLIK DISINI UNTUK UNDUH FILE PDF",
        data=pdf_data,
        file_name=f"LAPORAN_RISIKO_SAMPLE_{artikel if artikel else 'BARU'}.pdf",
        mime="application/pdf",
        use_container_width=True
    )
