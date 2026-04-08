import streamlit as st
import pandas as pd
import joblib

# 1. Configuración de la página
st.set_page_config(page_title="Predicción de subscripción", page_icon="🏦", layout="wide")
st.title("Simulador de subscripción a producto bancario")
st.markdown("Introduce los datos del cliente para predecir si contratará el producto bancario.")

# 2. Cargar el modelo guardado
@st.cache_resource
def load_model():
    return joblib.load('modelo_final.joblib')

modelo = load_model()

# 3. Crear el formulario de entrada organizado en 3 columnas
st.subheader("Datos del Cliente")
col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input("Edad (age)", min_value=18, max_value=100, value=38)
    job = st.selectbox("Trabajo (job)", ['management', 'technician', 'entrepreneur', 'blue-collar', 'unknown', 'retired', 'admin.', 'services', 'self-employed', 'unemployed', 'housemaid', 'student'])
    marital = st.selectbox("Estado Civil (marital)", ['married', 'single', 'divorced'])
    education = st.selectbox("Educación (education)", ['tertiary', 'secondary', 'primary', 'unknown'])
    default = st.selectbox("¿Tiene crédito en mora? (default)", ['no', 'yes'])
    balance = st.number_input("Saldo Medio Anual (balance)", value=119)
    

with col2:
    housing = st.selectbox("¿Tiene hipoteca? (housing)", ['yes', 'no'])
    loan = st.selectbox("¿Tiene préstamo personal? (loan)", ['no', 'yes'])
    contact = st.selectbox("Tipo de contacto (contact)", ['unknown', 'cellular', 'telephone'])
    day = st.number_input("Día del mes (day)", min_value=1, max_value=31, value=13)
    month = st.selectbox("Mes (month)", ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'])
    duration = st.number_input("Duración última llamada en seg. (duration)", min_value=0, value=568)

with col3:
    campaign = st.number_input("Contactos en esta campaña (campaign)", min_value=1, value=4)
    previous = st.number_input("Contactos antes de esta campaña (previous)", min_value=0, value=0)
    poutcome = st.selectbox("Resultado campaña anterior (poutcome)", ['unknown', 'failure', 'other', 'success'])
    wasContacted = st.selectbox("¿Fue contactado antes? (wasContacted)", [0, 1])
    contactedLabel = st.selectbox("Categoría de contacto previo (contactedLabel)", [0, 1, 2, 3, 4])

# 4. Botón de predicción
st.markdown("---")
if st.button("Predecir Contratación", type="primary", use_container_width=True):
    
    # Recopilar todos los datos en un DataFrame con UNA sola fila
    input_data = pd.DataFrame([{
        'age': age,
        'job': job,
        'marital': marital,
        'education': education,
        'balance': balance,
        'default': default,
        'housing': housing,
        'loan': loan,
        'contact': contact,
        'day': day,
        'month': month,
        'duration': duration,
        'campaign': campaign,
        'previous': previous,
        'poutcome': poutcome,
        'wasContacted': wasContacted,
        'contactedLabel': contactedLabel
    }])
    
    # Hacer la predicción
    prediccion = modelo.predict(input_data)[0]
    
    # Mostrar el resultado a lo grande
    st.subheader("Resultado de la Predicción:")
    if prediccion == 'yes':
        st.success("¡El cliente SÍ contratará el producto! (Predicción: 'yes')")
        st.balloons()
    else:
        st.error("El cliente NO contratará el producto. (Predicción: 'no')")