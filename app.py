import streamlit as st
import pandas as pd
from fpdf import FPDF
import io
import zipfile
import os
import shutil
from PIL import Image  # ✅ Importación para convertir imágenes
from datetime import datetime  # Asegúrate de tener esto al inicio del archivo
from io import BytesIO
import re  # al inicio del archivo si no está ya
from num2words import num2words
import urllib.parse




# ✅ Cargar usuarios desde Excel
@st.cache_data
def cargar_usuarios():
    df = pd.read_excel("usuarios.xlsx")
    df["vencimiento"] = pd.to_datetime(df["vencimiento"])
    usuarios = {}
    for _, row in df.iterrows():
        usuarios[row["usuario"]] = {
            "password": str(row["password"]),
            "nombre_empresa": row["nombre_empresa"],
            "vencimiento": row["vencimiento"].to_pydatetime()
        }
    return usuarios

USUARIOS = cargar_usuarios()

# 🔒 Control de sesión
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False


if not st.session_state["autenticado"]:
    st.markdown("""
        <style>
        /* Imagen de fondo solo cuando no se ha autenticado */
        .stApp {
            background-image: url("https://i.postimg.cc/B6nPntCQ/Dise-o-sin-t-tulo-5.png");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }

        /* Color general del texto */
        html, body, [class*="css"] {
            color: white !important;
        }

        /* Estilo de los campos de entrada */
        input[type="text"], input[type="password"], textarea, select {
            background-color: #D3D3D3 !important;
            color: black !important;
            caret-color: black !important;
            border-radius: 5px;
            border: 1px solid #ccc;
            padding: 0.4rem;
        }

        /* Estilo del botón */
        .stButton>button {
            background-color: #000000 !important;
            color: white !important;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
        }
        </style>
    """, unsafe_allow_html=True)




# 🔐 Función de login
def login():

    st.title("Acceso a la Plataforma")

    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        if usuario in USUARIOS:
            user_data = USUARIOS[usuario]
            if user_data["password"] == password:
                if datetime.today().date() <= user_data["vencimiento"].date():
                    st.session_state["autenticado"] = True
                    st.session_state["usuario"] = usuario
                    st.session_state["vencimiento"] = user_data["vencimiento"]  # ✅ Aquí guardamos la fecha
                    st.rerun()
                else:
                    st.warning("⚠️ Tu cuenta ha expirado.")

                    numero_whatsapp = "573205283573"
                    mensaje = f"Hola, soy el usuario {usuario} y necesito reactivar mi cuenta."
                    mensaje_codificado = urllib.parse.quote(mensaje)
                    enlace = f"https://wa.me/{numero_whatsapp}?text={mensaje_codificado}"

                    st.markdown(
                        f"<p style='margin-top: 10px;'>"
                        f"<a href='{enlace}' target='_blank' style='color:#FFFFFF; font-weight:bold;'>"
                        f"Haz clic aquí para solicitar reactivación por WhatsApp</a></p>",
                        unsafe_allow_html=True
                    )

            else:
                st.error("❌ Contraseña incorrecta")
        else:
            st.error("❌ Usuario no encontrado")

    # 🔽 Pie de login con contacto
    st.markdown("---")
    col1, col2 = st.columns([1, 5])

    with col1:
        if os.path.exists("logo_creador.png"):
            st.image("logo_creador.png", width=80)

    with col2:
        st.markdown("""
        ### Desarrollado por Hazlo Fácil - Excel contable  
        📧 hazlofacil.contabilidad@gmail.com  
        📱 Whatsapp +57 320 528 3573  
        🌐 [YouTube](http://www.youtube.com/@HAZLOFACIL-EXCELCONTABLE)
        """)

    st.markdown(
        "<p style='text-align: center; font-size: 13px; color: white;'>"
        "© 2025 Hazlo Fácil - Excel contable. Todos los derechos reservados."
        "</p>",
        unsafe_allow_html=True
    )



if not st.session_state["autenticado"]:
    login()
    st.stop()

# ✅ Mostrar botón para cerrar sesión en la app principal
with st.sidebar:
    st.markdown(f"👤 Usuario: **{st.session_state['usuario']}**")

    # Mostrar días restantes
    hoy = datetime.today().date()
    vencimiento = st.session_state.get("vencimiento", hoy)

    # 👇 Convertimos vencimiento a date si es datetime
    if isinstance(vencimiento, datetime):
        vencimiento = vencimiento.date()

    dias_restantes = (vencimiento - hoy).days

    if dias_restantes >= 0:
        st.markdown(f"📅 **Días restantes de licencia:** {dias_restantes}")
    else:
        st.markdown("⚠️ **Licencia expirada**")

    if st.button("🔒 Cerrar sesión"):
        st.session_state["autenticado"] = False
        st.session_state["usuario"] = ""
        st.rerun()




st.set_page_config(page_title="Generador de Comprobantes de Nómina", layout="centered")
st.markdown("""
    <style>
    /* --- FONDO GENERAL --- */
    .stApp {
        background-color: #bfbfbf !important;  /* Gris claro */
        color: black !important;
    }
    html, body, [class*="css"] {
        color: black !important;
    }

    /* --- TITULOS --- */
    h1, h2, h3, h4, h5, h6 {
        color: black !important;
    }

    /* --- INPUTS / TEXTAREAS / SELECTS --- */
    input, textarea, select {
        background-color: #ffffff !important;
        color: black !important;
        border-radius: 5px;
        border: 1px solid #cccccc !important;
    }

    /* --- ETIQUETAS DE FORMULARIO --- */
    label, .stTextInput label, .stSelectbox label, .stNumberInput label,
    .stDateInput label, .stFileUploader label, .stTextArea label {
        color: black !important;
        font-weight: 500;
    }

    /* --- BOTONES GENERALES VERDES --- */
    .stButton > button {
        background-color: #198c19 !important;
        color: white !important;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 6px;
    }

    .stButton > button:hover {
        background-color: #166f16 !important;
    }

    /* --- ÚLTIMO BOTÓN (Cerrar sesión) ROJO --- */
    .stButton > button:last-child {
        background-color: #c62828 !important;
        color: white !important;
    }

    .stButton > button:last-child:hover {
        background-color: #b71c1c !important;
    }

    /* --- BOTÓN DE DESCARGA --- */
    .stDownloadButton > button {
        background-color: #2e7d32 !important;
        color: white !important;
        border-radius: 6px;
    }

    /* --- SIDEBAR (VERDE OSCURO) --- */
    section[data-testid="stSidebar"] {
        background-color: #0b3d0b !important;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    section[data-testid="stSidebar"]::before {
        background-color: #0b3d0b !important;
    }

    /* --- ALERTAS (mensajes como warning/info/success/error) --- */
    .stAlert > div {
        color: black !important;
    }

    /* --- UPLOADER Y TEXTO DE ARCHIVOS --- */
    section[data-testid="stFileUploader"] * {
        color: black !important;
    }

    .uploadedFileDetails,
    .uploadedFileDetails span {
        color: black !important;
    }

    /* --- BARRAS DE PROGRESO --- */
    .stProgress > div > div > div > div {
        background-color: #4caf50;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Generador de Comprobantes de Nómina")

# 🔹 Plantilla descargable
st.subheader("Descargar plantilla de Excel")
plantilla_df = pd.DataFrame({
    "Nombre": [],
    "Documento": [],
    "Valor Pagado": [],
    "Concepto": [],
    "Dias trabajados": [],
    "Sueldo": [],
    "Aux. Transporte": [],
    "Otros ingresos": [],
    "Salud": [],
    "Pensión": [],
    "Retefuente": [],
    "FSP": [],
    "Prestamos": [],
    "Otras deducciones": [],
    "Forma de pago": [],
    "Banco": [],
    "Observaciones": []
})

# Guardar plantilla en memoria
excel_buffer = BytesIO()
with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
    plantilla_df.to_excel(writer, index=False, sheet_name='Plantilla')

excel_buffer.seek(0)

# Botón de descarga
st.download_button(
    label="Descargar plantilla de Excel",
    data=excel_buffer,
    file_name="plantilla_nomina.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)


# 🔹 Datos del empleador
st.subheader("Información del Empleador")
nombre_empleador = st.text_input("Nombre del empleador")
nit = st.text_input("NIT del empleador")
anio = st.text_input("Año", value="2025")
logo = st.file_uploader("Sube el logo de la empresa (PNG o JPG)", type=["png", "jpg", "jpeg"])

archivo = st.file_uploader("Sube tu archivo Excel con los datos", type=["xlsx"])

if archivo:
    df = pd.read_excel(archivo)
    st.success("Archivo cargado correctamente ✅")
    st.write("Vista previa de los datos:", df.head())

    if st.button("🚀 Generar Recibos en ZIP"):
        os.makedirs("recibos_tmp", exist_ok=True)

        progress_bar = st.progress(0, text="Generando archivos PDF...")
        total_rows = len(df)


        # ✅ Convertir logo a PNG con PIL si fue subido
        logo_path = None
        if logo:
            logo_path = os.path.join("recibos_tmp", "logo_temp.png")
            img = Image.open(logo).convert("RGBA")
            img.save(logo_path, format="PNG")

        for i, row in df.iterrows():
            pdf = FPDF()
            pdf.add_page()

            # 🔹 Logo en la esquina superior izquierda
            if logo_path:
                pdf.image(logo_path, x=10, y=8, w=30)

            # 🔹 Datos del empleador (superior derecha)
            pdf.set_font("Arial", '', 10)
            pdf.set_text_color(100, 100, 100)
            pdf.set_xy(140, 10)
            pdf.multi_cell(60, 5, f"{nombre_empleador}\nNIT: {nit}\nAño: {anio}", align="R")

            # Título
            pdf.set_font("Arial", 'B', 16)
            pdf.set_text_color(100, 100, 100)
            pdf.cell(200, 10, "Comprobante de Nómina", ln=True, align="C")
            pdf.ln(6)

            # Subtítulo
            pdf.set_font("Arial", 'B', 12)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(200, 6, "Resumen", ln=True, align="C")

            # Primera línea
            pdf.set_draw_color(100, 100, 100)
            pdf.set_line_width(0.7)
            y_line = pdf.get_y()
            pdf.line(10, y_line, 200, y_line)

            # Segunda línea más delgada justo abajo
            pdf.set_line_width(0.3)
            pdf.line(10, y_line + 1.5, 200, y_line + 1.5)

            pdf.ln(4)

            # Datos básicos
            pdf.set_font("Arial", '', 12)
            pdf.set_text_color(0, 0, 0)
            pdf.set_fill_color(245, 245, 245)

            pdf.cell(50, 8, "Nombre:", border=0)
            pdf.cell(130, 8, row['Nombre'], ln=True, fill=True)

            pdf.cell(50, 8, "Documento:", border=0)
            pdf.cell(130, 8, str(row['Documento']), ln=True, fill=True)

            pdf.cell(50, 8, "Valor pagado:", border=0)
            pdf.cell(130, 8, f"${row['Valor Pagado']:,}", ln=True, fill=True)

            pdf.cell(50, 8, "Concepto:", border=0)
            pdf.multi_cell(130, 8, row['Concepto'], fill=True)

            pdf.cell(50, 8, "Dias trabajados:", border=0)
            pdf.cell(130, 8, str(row['Dias trabajados']), ln=True, fill=True)

            # --- Sección: Resumen de Ingresos y Deducciones ---
            pdf.ln(4)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(200, 6, "Detalle de Ingresos y Deducciones", ln=True, align="C")
            
            # Primera línea
            pdf.set_draw_color(100, 100, 100)
            pdf.set_line_width(0.7)
            y_line = pdf.get_y()
            pdf.line(10, y_line, 200, y_line)

            # Segunda línea más delgada justo abajo
            pdf.set_line_width(0.3)
            pdf.line(10, y_line + 1.5, 200, y_line + 1.5)

            pdf.ln(4)

            pdf.set_font("Arial", '', 11)
            pdf.set_fill_color(240, 240, 240)

            ingresos = [
                ("Sueldo", row["Sueldo"]),
                ("Aux. Transporte", row["Aux. Transporte"]),
                ("Otros ingresos", row["Otros ingresos"]),
            ]

            deducciones = [
                ("Salud", row["Salud"]),
                ("Pensión", row["Pensión"]),
                ("Retefuente", row["Retefuente"]),
                ("FSP", row["FSP"]),
                ("Préstamos", row["Prestamos"]),
                ("Otras Deducciones", row["Otras deducciones"]),
            ]

            total_ingresos = sum([v for _, v in ingresos if isinstance(v, (int, float))])
            total_deducciones = sum([v for _, v in deducciones if isinstance(v, (int, float))])

            # Ingresos (izquierda)
            y_start = pdf.get_y()
            pdf.set_x(10)
            for label, value in ingresos:
                pdf.cell(60, 6, f"{label}:", border=0)
                pdf.cell(30, 6, f"${value:,}" if isinstance(value, (int, float)) else str(value), ln=True, fill=True)

            pdf.set_font("Arial", 'B', 11)
            pdf.cell(60, 6, "Total ingresos:", border=0)
            pdf.cell(30, 6, f"${total_ingresos:,}", ln=True, fill=True)

            # Deducciones (derecha)
            pdf.set_font("Arial", '', 11)
            y_deducciones = y_start
            for label, value in deducciones:
                pdf.set_xy(120, y_deducciones)
                pdf.cell(45, 6, f"{label}:", border=0)
                pdf.cell(30, 6, f"${value:,}" if isinstance(value, (int, float)) else str(value), ln=True, fill=True)
                y_deducciones += 6

            pdf.set_font("Arial", 'B', 11)
            pdf.set_xy(120, y_deducciones)
            pdf.cell(45, 6, "Total deducciones:", border=0)
            pdf.cell(30, 6, f"${total_deducciones:,}", ln=True, fill=True)

           # Neto a pagar centrado
            neto = total_ingresos - total_deducciones
            neto_letras = num2words(neto, lang='es').capitalize() + " pesos M/te"

            pdf.ln(2)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(285, 8, f"Neto a pagar:              ${neto:,}", ln=True, align="C")

            # Valor en letras
            pdf.set_font("Arial", 'I', 8)
            pdf.set_x(120) 
            pdf.multi_cell(0, 4, f"Son: {neto_letras}", align="L")

            # Neto a forma de pago
            pdf.set_font("Arial", '', 10)
            pdf.cell(35, 8, "Forma de pago:", border=0)
            pdf.multi_cell(40, 8, row['Forma de pago'], fill=True)

            # Bancos
            pdf.set_font("Arial", '', 10)
            pdf.cell(35, 8, "Banco:", border=0)
            pdf.multi_cell(40, 8, row['Banco'], fill=True)

            # 🔹 Observaciones desde Excel
            if 'Observaciones' in row and pd.notna(row['Observaciones']):
               
                pdf.set_font("Arial", 'B', 11)
                pdf.cell(200, 8, "Observaciones:", ln=True)
                pdf.set_font("Arial", '', 11)
                pdf.multi_cell(190, 8, str(row['Observaciones']))

            # 🔻 Establecer posición fija en la parte inferior (sin crear nueva página)
                pdf.set_auto_page_break(auto=False)  # ⚠️ Importante: Desactiva salto automático de página
                pdf.set_y(-15)  # Mover el cursor 15 mm desde el borde inferior
                pdf.set_font("Arial", 'I', 9)
                pdf.set_text_color(100, 100, 100)
                fecha_generacion = datetime.now().strftime("%d/%m/%Y")
                pdf.cell(0, 10, f"Fecha de generación: {fecha_generacion}", 0, 0, 'R')

            # Guardar PDF con nombre, concepto y "recibo"
            nombre_limpio = re.sub(r'[\\/*?:"<>|]', "", str(row['Nombre'])).strip().replace(" ", "_")
            concepto_raw = str(row['Concepto'])[:40]  # Limita a 40 caracteres
            concepto_limpio = re.sub(r'[\\/*?:"<>|]', "", concepto_raw).strip().replace(" ", "_")

            filename = f"recibos_tmp/{nombre_limpio}_{concepto_limpio}_recibo_{i+1}.pdf"
            pdf.output(filename)


            # Actualiza la barra de progreso
            progress_bar.progress((i + 1) / total_rows, text=f"Procesando {i + 1} de {total_rows} archivos...")

        # Crear archivo ZIP
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zipf:
            for filename in os.listdir("recibos_tmp"):
                filepath = os.path.join("recibos_tmp", filename)
                zipf.write(filepath, arcname=filename)

        zip_buffer.seek(0)


        # Al finalizar, mostrar mensaje de éxito
        progress_bar.empty()
        st.success("✅ Archivos generados y listos para descargar.")
        
        # Botón de descarga
        st.download_button(
            label="📦 Descargar todos los recibos en un ZIP",
            data=zip_buffer,
            file_name="recibos_nomina.zip",
            mime="application/zip"
        )

        # Limpiar archivos temporales
        shutil.rmtree("recibos_tmp")
st.markdown("---")
col1, col2 = st.columns([1, 5])

with col1:
    st.image("logo_creador.png", width=80)  # o usa file_uploader

with col2:
    st.markdown("""
    ### Desarrollado por Hazlo Fácil - Excel contable  
    📧 hazlofacil.contabilidad@gmail.com  
    📱 Whatsapp +57 320 528 3573  
    🌐 http://www.youtube.com/@HAZLOFACIL-EXCELCONTABLE
    """)

# Derechos de autor al final
st.markdown(
    "<p style='text-align: center; font-size: 13px; color: Black;'>"
    "© 2025 Hazlo Fácil - Excel contable. Todos los derechos reservados."
    "</p>",
    unsafe_allow_html=True
)
