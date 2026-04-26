import streamlit as st
import qrcode
from io import BytesIO
import urllib.parse

st.set_page_config(page_title="Sistema AMPA con QR", layout="centered")

st.title("Sistema de Registro AMPA con QR")
st.write(
    "Introduce las mediciones de presión arterial de varios días y genera un QR "
    "para mostrar en consulta."
)

dias = st.number_input("Número de días registrados", min_value=3, max_value=7, value=7)

datos = []

for dia in range(1, dias + 1):
    st.subheader(f"Día {dia}")

    st.markdown("**Mañana**")
    m1_sis = st.number_input(f"Día {dia} mañana 1 sistólica", 50, 250, 135, key=f"m1s{dia}")
    m1_dia = st.number_input(f"Día {dia} mañana 1 diastólica", 30, 150, 85, key=f"m1d{dia}")

    m2_sis = st.number_input(f"Día {dia} mañana 2 sistólica", 50, 250, 135, key=f"m2s{dia}")
    m2_dia = st.number_input(f"Día {dia} mañana 2 diastólica", 30, 150, 85, key=f"m2d{dia}")

    st.markdown("**Noche**")
    n1_sis = st.number_input(f"Día {dia} noche 1 sistólica", 50, 250, 130, key=f"n1s{dia}")
    n1_dia = st.number_input(f"Día {dia} noche 1 diastólica", 30, 150, 80, key=f"n1d{dia}")

    n2_sis = st.number_input(f"Día {dia} noche 2 sistólica", 50, 250, 130, key=f"n2s{dia}")
    n2_dia = st.number_input(f"Día {dia} noche 2 diastólica", 30, 150, 80, key=f"n2d{dia}")

    fila = (
        f"D{dia}:"
        f"{m1_sis}/{m1_dia},"
        f"{m2_sis}/{m2_dia},"
        f"{n1_sis}/{n1_dia},"
        f"{n2_sis}/{n2_dia}"
    )
    datos.append(fila)

if st.button("Generar QR para consulta"):
    texto = ";".join(datos)

    texto_codificado = urllib.parse.quote(texto)

    link_medico = f"https://ampa-qr-medico.streamlit.app?data={texto_codificado}"

    st.subheader("Resumen AMPA generado")
    st.text_area("Datos codificados", texto, height=150)

    st.subheader("Enlace para consulta médica")
    st.write(link_medico)

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )

    qr.add_data(link_medico)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")

    st.subheader("QR generado")
    st.image(buffer.getvalue(), caption="QR para mostrar en consulta")

    st.download_button(
        label="Descargar QR",
        data=buffer.getvalue(),
        file_name="qr_ampa_consulta.png",
        mime="image/png"
    )
