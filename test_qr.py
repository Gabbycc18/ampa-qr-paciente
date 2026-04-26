import streamlit as st
import qrcode
from io import BytesIO

st.title("Sistema de Registro AMPA con QR")
st.write("Hola!. Bienvenido al sistema AMPA. Porfavor, introduce las mediciones de varios días y genera un QR para consulta.")

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

    fila = f"D{dia}:{m1_sis}/{m1_dia},{m2_sis}/{m2_dia},{n1_sis}/{n1_dia},{n2_sis}/{n2_dia}"
    datos.append(fila)

if st.button("Generar QR completo"):
    texto_qr = ";".join(datos)

    st.subheader("Datos codificados")
    st.text_area("Resumen AMPA codificado", texto_qr, height=150)

    qr = qrcode.QRCode(box_size=7, border=2)
    qr.add_data(texto_qr)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")

    st.subheader("QR generado")
    st.image(buffer.getvalue(), caption="QR AMPA completo")

    st.download_button(
        label="Descargar QR",
        data=buffer.getvalue(),
        file_name="qr_ampa_completo.png",
        mime="image/png"
    )