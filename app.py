import streamlit as st
import pandas as pd
import pickle

# ── Configuración de página ──
st.set_page_config(page_title="Predictor de Depósito", page_icon="🏦", layout="wide")

# ── Carga del modelo ──
@st.cache_resource
def load_model():
    with open("bank_ALL/bank_12.pkl", "rb") as f:
        return pickle.load(f)

try:
    modelo = load_model()
    model_loaded = True
except FileNotFoundError:
    model_loaded = False

# ── Funciones de transformación ──
def pdays_transform(x): return 0 if x == -1 else 1

def bin_pdays(x):
    if x == -1: return 0
    if x < 100: return 1
    if x < 200: return 2
    if x < 400: return 3
    return 4

# ── Interfaz web ──
st.title("Predictor de Suscripción a Depósito Bancario")

if not model_loaded:
    st.error("No se encontró el modelo 'bank_12.pkl' en esta carpeta.")
    st.stop()

col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input("Edad", 18, 95, 40)
    job = st.selectbox("Ocupación", ["admin.", "blue-collar", "entrepreneur", "housemaid", "management", "retired", "self-employed", "services", "student", "technician", "unemployed", "unknown"])
    marital = st.selectbox("Estado civil", ["married", "single", "divorced"])
    education = st.selectbox("Nivel educativo", ["primary", "secondary", "tertiary", "unknown"])
    default = st.selectbox("¿Tiene crédito en mora?", ["no", "yes"])
    balance = st.number_input("Saldo medio anual (€)", -10000, 100000, 1500)

with col2:
    housing = st.selectbox("¿Tiene hipoteca?", ["yes", "no"])
    loan = st.selectbox("¿Tiene préstamo personal?", ["no", "yes"])
    contact = st.selectbox("Tipo de contacto", ["cellular", "telephone", "unknown"])
    day = st.number_input("Día del último contacto", 1, 31, 15)
    month = st.selectbox("Mes del último contacto", ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"])
    duration = st.number_input("Duración llamada (s)", 0, 5000, 200)

with col3:
    campaign = st.number_input("Contactos esta campaña", 1, 50, 2)
    pdays = st.number_input("Días desde último contacto (-1 si no hubo)", -1, 900, -1)
    previous = st.number_input("Contactos antes de campaña", 0, 60, 0)
    poutcome = st.selectbox("Resultado campaña anterior", ["unknown", "failure", "other", "success"])

if st.button("🔮 Realizar Predicción", type="primary", use_container_width=True):
    input_data = pd.DataFrame([{
        "age": age, "job": job, "marital": marital, "education": education,
        "default": default, "balance": balance, "housing": housing, "loan": loan,
        "contact": contact, "day": day, "month": month, "duration": duration,
        "campaign": campaign, "previous": previous, "poutcome": poutcome,
        "wasContacted": pdays_transform(pdays), "contactedLabel": bin_pdays(pdays),
    }])

    prediccion = modelo.predict(input_data)
    
    st.divider()
    if prediccion == "yes":
        st.success("**Es MUY PROBABLE que el cliente SUSCRIBA el depósito**")
    else:
        st.error("**Es POCO PROBABLE que el cliente suscriba el depósito**")