import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime

# --- CONFIGURASI HALAMAN STREAMLIT ---
st.set_page_config(
    page_title="Form Analisis Risiko Sampel",
    page_icon="📋",
    layout="centered"
)

# --- DATABASE PARAMETER DEFAULT (Berdasarkan Tipe Mesin) ---
DATABASE_MESIN = {
    "Mesin Jahit (Sewing)": {
        "Defect Potensial": "Jahitan Lompat (Skipped Stitch)",
        "Penyebab": "Jarum tumpul atau pemasangan benang kurang tepat.",
        "Tindakan Pencegahan": "Ganti jarum secara berkala dan cek jalur benang sebelum rump up."
    },
    "Mesin Obras (Overlock)": {
        "Defect Potensial": "Kain Terpotong Berlebih (Uneven Cutting)",
        "Penyebab": "Pisau pemotong obras tumpul atau setelan meleset.",
        "Tindakan Pencegahan": "Asah atau ganti pisau obras dan lakukan tes potongan pada kain perca."
    },
    "Collar Fusing Machine": {
        "Defect Potensial": "Glassing / Bubbling",
        "Penyebab": "Tekanan (pressure) atau suhu terlalu tinggi pada proses fusing kerah.",
        "Tindakan Pencegahan": "Kalibrasi suhu dan tekanan mesin sebelum proses fusing sampel dimulai."
    },
    "Mesin Potong (Cutting)": {
        "Defect Potensial": "Pola Bergeser (Fraying / Misalignment)",
        "Penyebab": "Penjepitan kain kurang kuat saat mesin potong bergerak.",
        "Tindakan Pencegahan": "Pastikan klem kain terpasang kencang sebelum cutting dimulai."
    }
}

# --- FUNGSI GENERATE PDF ---
def buat_pdf(data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Styles
    style_judul = ParagraphStyle(
        'JudulPDF',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1E3A8A'),
        alignment=1, # Center
        spaceAfter=20
    )
    
    style_label = ParagraphStyle(
        'LabelKiri',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#374151')
    )
    
    style_isi = ParagraphStyle(
        'IsiKanan',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#1F2937')
    )
    
    cerita = []
    
    # 1. Judul Dokumen
    cerita.append(Paragraph("LAPORAN ANALISIS RISIKO PROSES SAMPEL", style_judul))
    cerita.append(Spacer(1, 10))
    
    # 2. Tabel Konten
    data_tabel = []
    for key, value in data.items():
        # Bungkus teks ke dalam Paragraph agar otomatis ganti baris (wrap text)
        p_key = Paragraph(f"<b>{key}</b>", style_label)
        p_val = Paragraph(str(value), style_isi)
        data_tabel.append([p_key, p_val])
        
    tabel_input = Table(data_tabel, colWidths=[150, 380])
    tabel_input.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F3F4F6')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1F2937')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#D1D5DB')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    
    cerita.append(tabel_input)
    cerita.append(Spacer(1, 40))
    
    # 3. Kolom Tanda Tangan
    data_ttd = [
        [Paragraph("<b>Dibuat Oleh:</b>", style_isi), Paragraph("<b>Diperiksa Oleh:</b>", style_isi)],
        [Spacer(1, 40), Spacer(1, 40)], # Ruang kosong tanda tangan
        [Paragraph("___________________<br/>Staf Engineering / Penanggung Jawab", style_isi), 
         Paragraph("___________________<br/>Manager / Supervisor", style_isi)]
    ]
    tabel_ttd = Table(data_ttd, colWidths=[265, 265])
    tabel_ttd.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    cerita.append(tabel_ttd)
    
    # Build PDF
    doc.build(cerita)
    buffer.seek(0)
    return buffer

# --- TAMPILAN APLIKASI WEB ---
st.title("📋 Form Analisis Risiko Proses Sampel")
st.write("Isi detail parameter di bawah ini untuk mengidentifikasi risiko dan mengunduh laporan PDF.")
st.markdown("---")

# Input Identitas Utama
kolom1, kolom2 = st.columns(2)
with kolom1:
    nama_petugas = st.text_input("Nama Penanggung Jawab / Staff", placeholder="Contoh: Andreas Eko")
    tanggal_input = st.date_input("Tanggal Analisis", datetime.today())
with kolom2:
    nama_style = st.text_input("Nama / Kode Style Sampel", placeholder="Contoh: Summer26-Drop2")
    buyer = st.text_input("Nama Buyer", placeholder="Contoh: Brand-A")

st.markdown("### 🛠️ Detail Teknis & Mesin")

# Pilihan Tipe Mesin
pilihan_mesin = st.selectbox(
    "Pilih Tipe Mesin yang Digunakan:",
    list(DATABASE_MESIN.keys())
)

# Ambil data bawaan berdasarkan tipe mesin yang dipilih
data_bawaan = DATABASE_MESIN[pilihan_mesin]

# Input parameter risiko (bisa diedit jika di lapangan ada temuan berbeda)
defect_potensial = st.text_area(
    "Potensi Cacat Produksi (Defect)", 
    value=data_bawaan["Defect Potensial"],
    help="Bisa disesuaikan jika ada potensi cacat spesifik lainnya."
)

analisa_penyebab = st.text_area(
    "Analisa Penyebab Masalah", 
    value=data_bawaan["Penyebab"]
)

tindakan_pencegahan = st.text_area(
    "Tindakan Pencegahan (Preventive Action)", 
    value=data_bawaan["Tindakan Pencegahan"]
)

st.markdown("---")

# Tombol Proses & Unduh
if st.button("Proses Data & Siapkan Dokumen", type="primary"):
    if not nama_petugas or not nama_style:
        st.error("❌ Nama Penanggung Jawab dan Kode Style wajib diisi terlebih dahulu!")
    else:
        # Susun data untuk dimasukkan ke PDF
        payload_data = {
            "Tanggal Analisis": tanggal_input.strftime('%d %B %Y'),
            "Penanggung Jawab": nama_petugas,
            "Kode Style Sampel": nama_style,
            "Buyer": buyer if buyer else "-",
            "Tipe Mesin Utama": pilihan_mesin,
            "Potensi Defect": defect_potensial,
            "Penyebab Masalah": analisa_penyebab,
            "Tindakan Pencegahan": tindakan_pencegahan
        }
        
        # Buat file PDF-nya
        file_pdf = buat_pdf(payload_data)
        
        st.success("✅ Dokumen PDF Berhasil Dibuat!")
        
        # Tombol Download PDF resmi dari Streamlit
        st.download_button(
            label="📥 Unduh Laporan PDF Risiko",
            data=file_pdf,
            file_name=f"Laporan_Risiko_{nama_style}_{tanggal_input.strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
