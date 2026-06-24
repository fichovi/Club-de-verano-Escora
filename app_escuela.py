import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, datetime
import json
import os

# --- 1. CONFIGURACIÓN DE PÁGINA (MARCA BLANCA NATIVA) ---
st.set_page_config(
    page_title="Control Club de Verano", 
    page_icon="🏆", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- 2. INYECCIÓN DE CSS AVANZADO (OCULTAR LOGOS DE STREAMLIT Y DISEÑO MÓVIL AUTOMÁTICO) ---
st.markdown("""
    <style>
        /* Ocultar elementos oficiales de Streamlit y GitHub */
        header {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        div[data-testid="stDecoration"] {display: none !important;}
        div[data-testid="stSidebar"] {display: none !important;}
        
        /* Forzar que las columnas superiores se comporten como una barra corredera horizontal */
        div[data-testid="stHorizontalBlock"] {
            overflow-x: auto !important;
            flex-wrap: nowrap !important;
            white-space: nowrap !important;
            padding: 5px 0px !important;
            gap: 8px !important;
        }
        
        /* Estilizar los botones de navegación superiores (Menú gris permanente) */
        div[data-testid="stHorizontalBlock"] button {
            background-color: #f0f2f6 !important;
            color: #31333F !important;
            border-radius: 20px !important;
            padding: 6px 16px !important;
            border: 1px solid #d1d5db !important;
            font-weight: bold !important;
        }
        
        /* --- DISEÑO DE MACRO-BOTONES TÁCTILES GRANDES EN VERTICAL --- */
        .stButton > button {
            width: 100% !important;
            height: 55px !important;
            font-size: 18px !important;
            font-weight: bold !important;
            border-radius: 12px !important;
            margin-bottom: 8px !important;
        }
        
        /* LÓGICA DE DETECCIÓN: Si la fila tiene exactamente 3 columnas, aplicamos semáforo de color */
        /* Columna 1 de 3 -> Verde */
        div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-of-type(1):nth-last-of-type(3) .stButton > button {
            background-color: #22c55e !important;
            color: white !important;
            border: 1px solid #16a34a !important;
        }
        /* Columna 2 de 3 -> Naranja */
        div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-of-type(2):nth-last-of-type(2) .stButton > button {
            background-color: #f97316 !important;
            color: white !important;
            border: 1px solid #ea580c !important;
        }
        /* Columna 3 de 3 -> Rojo */
        div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-of-type(3):nth-last-of-type(1) .stButton > button {
            background-color: #ef4444 !important;
            color: white !important;
            border: 1px solid #dc2626 !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. CARGA Y PERSISTENCIA DE ARCHIVOS LOCALES ---
LISTA_ALUM_INICIAL = [
    "Aitor Abarca Lillo", "Alex Martinez Sanfelix", "Álvaro Sancho Arnau", "Carles Sancho Toldos",
    "David Amoros Moreno", "Gorka Gramaje Flor", "Iñaki Tomás Espinilla", "Isaac Martínez Diago",
    "Jaume Navarro Pla", "Jaume Sancho", "Jordi Biosca Lera", "Juan Carlos Mayans Arandiga",
    "Manu Magdaleno Micó", "Mario Soriano Rovira", "Martín Bordera Carbó", "Martin Martinez Borras",
    "Mauro Ballester perucho", "Miguel Daries Nacher", "Miguel Navalón Fuentes", "Norberto Sala Úbeda",
    "Pablo Sancho Arnau", "Rafael Micó Cuallado", "Robert Ibáñez Gozalbes", "Salva Martinez Beltrán",
    "Santiago Berrio Aguado", "Santiago Pinter Aparicio", "Santiago Sala Úbeda", "Sergi Cervero Paz",
    "Toni Melo Gras", "Vicent Ferrer Díaz", "Yago Munera Martinez", "Nico Aznar Gisbert"
]

def guardar_datos_locales():
    st.session_state.historico_puntos.to_csv("local_historico_puntos.csv", index=False)
    with open("local_alumnos_master.json", "w", encoding="utf-8") as f:
        json.dump(st.session_state.alumnos_master, f, ensure_ascii=False)
    with open("local_oraciones.json", "w", encoding="utf-8") as f:
        json.dump(st.session_state.oraciones_aprendidas, f, ensure_ascii=False)
    with open("local_comedor.json", "w", encoding="utf-8") as f:
        json.dump(st.session_state.contador_comedor, f, ensure_ascii=False)
    with open("local_encargos.json", "w", encoding="utf-8") as f:
        json.dump(st.session_state.encargos_semanales, f, ensure_ascii=False)
    with open("local_asistencia.json", "w", encoding="utf-8") as f:
        json.dump(st.session_state.asistencia, f, ensure_ascii=False)
    with open("local_turno.json", "w", encoding="utf-8") as f:
        json.dump(st.session_state.estar_de_turno, f, ensure_ascii=False)

def cargar_datos_locales():
    if os.path.exists("local_alumnos_master.json"):
        with open("local_alumnos_master.json", "r", encoding="utf-8") as f:
            st.session_state.alumnos_master = json.load(f)
    else:
        st.session_state.alumnos_master = LISTA_ALUM_INICIAL.copy()
    if os.path.exists("local_historico_puntos.csv"):
        st.session_state.historico_puntos = pd.read_csv("local_historico_puntos.csv")
    else:
        st.session_state.historico_puntos = pd.DataFrame(columns=['Fecha', 'Alumno', 'Actividad', 'Puntos', 'Detalle', 'Semana'])
    if os.path.exists("local_oraciones.json"):
        with open("local_oraciones.json", "r", encoding="utf-8") as f:
            st.session_state.oraciones_aprendidas = json.load(f)
    else:
        st.session_state.oraciones_aprendidas = {al: [] for al in st.session_state.alumnos_master}
    if os.path.exists("local_comedor.json"):
        with open("local_comedor.json", "r", encoding="utf-8") as f:
            st.session_state.contador_comedor = json.load(f)
    else:
        st.session_state.contador_comedor = {al: 0 for al in st.session_state.alumnos_master}
    if os.path.exists("local_encargos.json"):
        with open("local_encargos.json", "r", encoding="utf-8") as f:
            st.session_state.encargos_semanales = json.load(f)
    else:
        st.session_state.encargos_semanales = {f"Semana {i}": {} for i in range(1, 5)}
    if os.path.exists("local_asistencia.json"):
        with open("local_asistencia.json", "r", encoding="utf-8") as f:
            st.session_state.asistencia = json.load(f)
    else:
        st.session_state.asistencia = {f"Semana {i}": {al: True for al in st.session_state.alumnos_master} for i in range(1, 5)}
    if os.path.exists("local_turno.json"):
        with open("local_turno.json", "r", encoding="utf-8") as f:
            st.session_state.estar_de_turno = json.load(f)
    else:
        st.session_state.estar_de_turno = {f"Semana {i}": {"Lunes": "", "Martes": "", "Miércoles": "", "Jueves": "", "Viernes": ""} for i in range(1, 5)}

if 'alumnos_master' not in st.session_state:
    cargar_datos_locales()

LISTA_ORACIONES = ["Señal Sta Cruz", "Padrenuestro", "Ave María", "Gloria", "5 pasos confesion", "Visita", "Angelus", "Oh Sra mía", "Angel Guarda", "10 mandamientos", "Empezar oracion", "Acabar oracion", "Bendicion mesa", "Acc gracias dp comer", "5 mand Sta Mad Igl", "Salve", "Bend sea pureza", "Señor mio Xto", "Acordaos", "Sacramentos"]
LISTA_ENCARGOS_OFICIALES = ["ORDEN SALA DE ESTUDIO", "ORDEN COMEDOR", "ORDEN TALLERES", "ORDEN ZONA ALMUERZO", "ORDEN VESTUARIOS", "ORDEN PISCINA", "MATERIAL DE DEPORTE", "MATERIAL DE PISCINA", "NEVERA", "VASOS", "CUBIERTOS", "TUPPERS", "AGUA COMIDA", "PLAN TARDE", "ORATORIO"]

if 'menu_actual' not in st.session_state:
    st.session_state.menu_actual = "🏠 Inicio"

# --- 4. BARRA DE CONFIGURACIÓN SUPERIOR COMPACTA ---
c_conf1, c_conf2, c_conf3 = st.columns([1, 1, 1])
semana_act = c_conf1.selectbox("📅 Bloque:", ["Semana 1", "Semana 2", "Semana 3", "Semana 4"], label_visibility="collapsed")
fecha_hoy = c_conf2.date_input("📆 Fecha:", date.today(), label_visibility="collapsed")

# --- 5. MENÚ HORIZONTAL DE BOTONES CORREDEROS AUTOMÁTICO ---
st.write("---")
items_menu = ["🏠 Inicio", "📊 Clasificación", "📚 Estudio", "🙏 Oraciones", "⚽ Deporte", "🙌 Deportividad", "🎨 Taller", "🧹 Encargos", "🍽️ Comedor", "💪 Extras", "🎥 Vídeo", "⚠️ Multas", "🛠️ Admin"]
nav_cols = st.columns(len(items_menu))

for idx, item in enumerate(items_menu):
    if nav_cols[idx].button(item, key=f"nav_top_{item}"):
        st.session_state.menu_actual = item
        st.rerun()
st.write("---")

alumnos_activos = [al for al in st.session_state.alumnos_master if st.session_state.asistencia.get(semana_act, {}).get(al, True)]

def get_puntos_hoy(alumno, actividad, default_val=None):
    df = st.session_state.historico_puntos
    if df.empty: return default_val
    cond = (df['Fecha'].astype(str) == str(fecha_hoy)) & (df['Alumno'] == alumno) & (df['Actividad'] == actividad)
    if cond.any(): return df.loc[cond, 'Puntos'].values[0]
    return default_val

def set_puntos_hoy(alumno, actividad, puntos, detalle=""):
    df = st.session_state.historico_puntos
    cond = (df['Fecha'].astype(str) == str(fecha_hoy)) & (df['Alumno'] == alumno) & (df['Actividad'] == actividad)
    if cond.any():
        st.session_state.historico_puntos.loc[cond, 'Puntos'] = puntos
        st.session_state.historico_puntos.loc[cond, 'Detalle'] = detalle
    else:
        nueva_fila = pd.DataFrame([{
            'Fecha': str(fecha_hoy), 'Alumno': alumno, 'Actividad': actividad, 
            'Puntos': puntos, 'Detalle': detalle, 'Semana': semana_act
        }])
        st.session_state.historico_puntos = pd.concat([st.session_state.historico_puntos, nueva_fila], ignore_index=True)
    guardar_datos_locales()

# --- PANTALLA: INICIO & AGENDA ---
if st.session_state.menu_actual == "🏠 Inicio":
    st.subheader("📆 Horario y Agenda del Día")
    hora_ahora = datetime.now().time()
    cronograma = [
        {"inicio": "09:00", "fin": "10:00", "tarea": "🙏 Acogida y Oración de la mañana"},
        {"inicio": "10:00", "fin": "11:30", "tarea": "📚 Hora de Estudio Silencioso"},
        {"inicio": "11:30", "fin": "12:00", "tarea": " Sandwich y Almuerzo de Compañeros"},
        {"inicio": "12:00", "fin": "13:30", "tarea": "🎨 Talleres Creativos Manuales"},
        {"inicio": "13:30", "fin": "15:00", "tarea": "🍽️ Almuerzo, Comedor y Turno de Limpieza"},
        {"inicio": "15:00", "fin": "15:30", "tarea": "🎥 Vídeo de Formación y Preguntas Masivas"},
        {"inicio": "15:30", "fin": "17:00", "tarea": " Torneo de Deportes y Juegos de Grupo"}
    ]
    for c in cronograma:
        t_ini = datetime.strptime(c["inicio"], "%H:%M").time()
        t_fin = datetime.strptime(c["fin"], "%H:%M").time()
        if t_ini <= hora_ahora <= t_fin:
            st.markdown(f'<div style="background-color: #d1fae5; border-left: 5px solid #10b981; padding: 12px; border-radius: 6px; margin-bottom: 8px;"><strong>⚡ AHORA MISMO ({c["inicio"]} - {c["fin"]}):</strong> {c["tarea"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="background-color: #f3f4f6; border-left: 5px solid #9ca3af; padding: 10px; border-radius: 6px; margin-bottom: 8px; color: #6b7280;">⏳ {c["inicio"]} - {c["fin"]}: {c["tarea"]}</div>', unsafe_allow_html=True)

# --- PANTALLA: CLASIFICACIÓN ---
elif st.session_state.menu_actual == "📊 Clasificación":
    st.subheader("📊 Resultados de Clasificación")
    tab_s, tab_g = st.tabs(["📆 Clasificación Semanal", "🏆 Acumulado General"])
    df_hist = st.session_state.historico_puntos
    
    with tab_s:
        df_tot_sem = df_hist[df_hist['Semana'] == semana_act].groupby('Alumno')['Puntos'].sum().reset_index() if not df_hist.empty else pd.DataFrame(columns=['Alumno', 'Puntos'])
        for al in alumnos_activos:
            if al not in df_tot_sem['Alumno'].values: df_tot_sem = pd.concat([df_tot_sem, pd.DataFrame([{'Alumno': al, 'Puntos': 0}])], ignore_index=True)
        df_tot_sem = df_tot_sem[df_tot_sem['Alumno'].isin(alumnos_activos)].sort_values(by="Puntos", ascending=True)
        fig_s = px.bar(df_tot_sem, x='Puntos', y='Alumno', orientation='h', color='Puntos', color_continuous_scale='Mint', text_auto=True)
        fig_s.update_traces(textposition='outside')
        fig_s.update_layout(height=600, xaxis=dict(fixedrange=True), yaxis=dict(fixedrange=True))
        st.plotly_chart(fig_s, width='stretch', config={'scrollZoom': False, 'displayModeBar': False})

    with tab_g:
        df_tot_gen = df_hist.groupby('Alumno')['Puntos'].sum().reset_index() if not df_hist.empty else pd.DataFrame(columns=['Alumno', 'Puntos'])
        for al in st.session_state.alumnos_master:
            if al not in df_tot_gen['Alumno'].values: df_tot_gen = pd.concat([df_tot_gen, pd.DataFrame([{'Alumno': al, 'Puntos': 0}])], ignore_index=True)
        df_tot_gen = df_tot_gen.sort_values(by="Puntos", ascending=True)
        fig_g = px.bar(df_tot_gen, x='Puntos', y='Alumno', orientation='h', color='Puntos', color_continuous_scale='Blues', text_auto=True)
        fig_g.update_traces(textposition='outside')
        fig_g.update_layout(height=700, xaxis=dict(fixedrange=True), yaxis=dict(fixedrange=True))
        st.plotly_chart(fig_g, width='stretch', config={'scrollZoom': False, 'displayModeBar': False})
        
    st.markdown("---")
    st.subheader("🔍 Historial Técnico Completo")
    st.dataframe(st.session_state.historico_puntos.iloc[::-1], width='stretch')

# --- PANTALLA: ESTUDIO (CORREGIDA) ---
elif st.session_state.menu_actual == "📚 Estudio":
    st.subheader("📚 Puntuación: Hora de Estudio")
    for al in sorted(alumnos_activos):
        st.markdown(f"### 🧑 {al}")
        cb1, cb2, cb3 = st.columns(3)
        # CORRECCIÓN: Eliminados los argumentos 'class_name', ahora el CSS pinta por posición
        if cb1.button("✅ +5 Puntos", key=f"est_g_{al}"):
            set_puntos_hoy(al, "Estudio", 5, "Estudio Excelente")
            st.toast(f"🎉 ¡+5 Puntos asignados a {al}!", icon="✅")
        if cb2.button("⚠️ +2 Puntos", key=f"est_o_{al}"):
            set_puntos_hoy(al, "Estudio", 2, "Estudio Regular")
            st.toast(f"⚠️ ¡+2 Puntos asignados a {al}!", icon="⚠️")
        if cb3.button("❌ 0 Puntos", key=f"est_r_{al}"):
            set_puntos_hoy(al, "Estudio", 0, "No aprovechado")
            st.toast(f"🛑 0 Puntos anotados a {al}", icon="❌")
        st.markdown("<hr style='border:1px dashed #ccc;' />", unsafe_allow_html=True)

# --- PANTALLA: ORACIONES ---
elif st.session_state.menu_actual == "🙏 Oraciones":
    st.subheader("🙏 Matriz de Oraciones Aprendidas")
    al_sel = st.selectbox("Selecciona un alumno:", sorted(alumnos_activos))
    oraciones_actuales = st.session_state.oraciones_aprendidas.get(al_sel, [])
    nuevas_oraciones = []
    bloques_semanales = [
        {"nombre": "🟢 SEMANA 1", "items": LISTA_ORACIONES[0:5], "color": "#e2f0cb"},
        {"nombre": "🔵 SEMANA 2", "items": LISTA_ORACIONES[5:10], "color": "#b5ead7"},
        {"nombre": "🟡 SEMANA 3", "items": LISTA_ORACIONES[10:15], "color": "#ffdac1"},
        {"nombre": "🟠 SEMANA 4", "items": LISTA_ORACIONES[15:20], "color": "#ffb7b2"}
    ]
    for b in bloques_semanales:
        st.markdown(f'<div style="background-color:{b["color"]}; padding:8px; border-radius:4px; font-weight:bold; margin-top:10px;">{b["nombre"]}</div>', unsafe_allow_html=True)
        for item in b["items"]:
            if st.checkbox(item, value=(item in oraciones_actuales), key=f"or_mob_{al_sel}_{item}"): nuevas_oraciones.append(item)
    if nuevas_oraciones != oraciones_actuales:
        st.session_state.oraciones_aprendidas[al_sel] = nuevas_oraciones
        st.session_state.historico_puntos = st.session_state.historico_puntos[~((st.session_state.historico_puntos['Alumno'] == al_sel) & (st.session_state.historico_puntos['Actividad'] == "Oración"))]
        for o in nuevas_oraciones: set_puntos_hoy(al_sel, "Oración", 5, f"Sabe: {o}")
        st.success("Cambios en oraciones guardados.")

# --- PANTALLA: DEPORTE ---
elif st.session_state.menu_actual == "⚽ Deporte":
    st.subheader("⚽ Gestión de Deporte del Día")
    modalidad = st.radio("Selecciona el formato de la competición de hoy:", ["👥 Por Equipos (Por defecto)", "🎾 Por Parejas (Dobles Tenis/Pádel)", "🏃 Individual (Carreras / Atletismo)"])
    
    if "Equipos" in modalidad:
        num_equipos = st.slider("¿Cuántos equipos compiten?", 2, 4, 2)
        nombres_base = ["Alfa", "Beta", "Gamma", "Delta"][:num_equipos]
        for eq in nombres_base:
            if f"m_dep_{eq}" not in st.session_state: st.session_state[f"m_dep_{eq}"] = []
            if f"c_dep_{eq}" not in st.session_state: st.session_state[f"c_dep_{eq}"] = ""
        for eq in nombres_base:
            st.markdown(f"##### Equipo {eq}")
            st.session_state[f"c_dep_{eq}"] = st.selectbox(f"👑 Capitán de {eq}:", [""] + alumnos_activos, key=f"cap_sel_{eq}")
            st.session_state[f"m_dep_{eq}"] = st.multiselect(f"Jugadores de {eq}:", [al for al in alumnos_activos if al != st.session_state[f"c_dep_{eq}"]], key=f"jug_sel_{eq}")
        st.markdown("---")
        mapa_pts = {5: "1º Lugar (5 Pts)", 3: "2º Lugar (3 Pts)", 2: "3º Lugar (2 Pts)", 0: "4º Lugar (0 Pts)"}
        res = {eq: st.selectbox(f"Posición de Equipo {eq}:", [5, 3, 2, 0], format_func=lambda x: mapa_pts[x], key=f"res_eq_{eq}") for eq in nombres_base}
        if st.button("💾 Guardar Torneo por Equipos"):
            for eq in nombres_base:
                pts = res[eq]
                if st.session_state[f"c_dep_{eq}"]: set_puntos_hoy(st.session_state[f"c_dep_{eq}"], "Deporte", pts, f"Capitán de {eq}")
                for j in st.session_state[f"m_dep_{eq}"]: set_puntos_hoy(j, "Deporte", pts, f"Miembro de {eq}")
            st.success("Puntos de equipo guardados.")
            
    elif "Parejas" in modalidad:
        p1 = st.multiselect("Pareja A:", alumnos_activos, max_selections=2, key="par_a")
        p2 = st.multiselect("Pareja B:", [al for al in alumnos_activos if al not in p1], max_selections=2, key="par_b")
        pts_pa = st.selectbox("Puntos Pareja A:", [5, 3, 2, 0], key="pts_pa")
        pts_pb = st.selectbox("Puntos Pareja B:", [5, 3, 2, 0], key="pts_pb")
        if st.button("💾 Registrar Puntos de Parejas"):
            for al in p1: set_puntos_hoy(al, "Deporte", pts_pa, "Torneo Parejas A")
            for al in p2: set_puntos_hoy(al, "Deporte", pts_pb, "Torneo Parejas B")
            st.success("Puntos de dobles guardados.")
            
    elif "Individual" in modalidad:
        al_ganador = st.selectbox("1º Clasificado (+5 Pts):", alumnos_activos, key="ind_1")
        al_2do = st.selectbox("2º Clasificado (+3 Pts):", [al for al in alumnos_activos if al != al_ganador], key="ind_2")
        al_3ro = st.selectbox("3º Clasificado (+2 Pts):", [al for al in alumnos_activos if al not in [al_ganador, al_2do]], key="ind_3")
        if st.button("💾 Registrar Deporte Individual"):
            set_puntos_hoy(al_ganador, "Deporte", 5, "1º Lugar Individual")
            set_puntos_hoy(al_2do, "Deporte", 3, "2º Lugar Individual")
            set_puntos_hoy(al_3ro, "Deporte", 2, "3º Lugar Individual")
            st.success("Puntos individuales guardados.")

# --- PANTALLA: DEPORTIVIDAD (CORREGIDA) ---
elif st.session_state.menu_actual == "🙌 Deportividad":
    st.header("🙌 Control de Deportividad")
    for al in sorted(alumnos_activos):
        st.markdown(f"### 🙌 {al}")
        cb1, cb2, cb3 = st.columns(3)
        # CORRECCIÓN: Eliminados los argumentos 'class_name'
        if cb1.button("✅ Excelente (+5)", key=f"dep_g_{al}"):
            set_puntos_hoy(al, "Deportividad", 5, "Deportividad Excelente")
            st.toast(f"🙌 Deportividad de {al} fijada en 5 Pts", icon="🙌")
        if cb2.button("⚠️ Quejas (+2)", key=f"dep_o_{al}"):
            set_puntos_hoy(al, "Deportividad", 2, "Protestas leves")
            st.toast(f"⚠️ Deportividad reducida a 2 Pts para {al}", icon="⚠️")
        if cb3.button("❌ Grave (0)", key=f"dep_r_{al}"):
            set_puntos_hoy(al, "Deportividad", 0, "Falta grave de respeto")
            st.toast(f"🛑 0 Pts en Deportividad para {al}", icon="❌")
        st.markdown("<hr style='border:1px dashed #ccc;' />", unsafe_allow_html=True)

# --- PANTALLA: TALLER (CORREGIDA) ---
elif st.session_state.menu_actual == "🎨 Taller":
    st.header("🎨 Trabajo en los Talleres")
    for al in sorted(alumnos_activos):
        st.markdown(f"### 🎨 {al}")
        cb1, cb2, cb3 = st.columns(3)
        # CORRECCIÓN: Eliminados los argumentos 'class_name'
        if cb1.button("✅ Trabajador (+5)", key=f"tal_g_{al}"):
            set_puntos_hoy(al, "Taller", 5, "Trabajo Completo")
            st.toast(f"🎨 Taller de {al} -> 5 Pts", icon="🎨")
        if cb2.button("⚠️ Distraído (+2)", key=f"tal_o_{al}"):
            set_puntos_hoy(al, "Taller", 2, "Poco participativo")
            st.toast(f"⚠️ Taller de {al} -> 2 Pts", icon="⚠️")
        if cb3.button("❌ Malo (0)", key=f"tal_r_{al}"):
            set_puntos_hoy(al, "Taller", 0, "Mal comportamiento en sala")
            st.toast(f"🛑 Taller de {al} -> 0 Pts", icon="❌")
        st.markdown("<hr style='border:1px dashed #ccc;' />", unsafe_allow_html=True)

# --- PANTALLA: ENCARGOS ---
elif st.session_state.menu_actual == "🧹 Encargos":
    st.header("🧹 Distribución de Encargos Oficiales")
    tab_f, tab_t = st.tabs(["📌 Tareas Fijas", "🙏 Estar de Turno"])
    if semana_act not in st.session_state.encargos_semanales: st.session_state.encargos_semanales[semana_act] = {e: [] for e in LISTA_ENCARGOS_OFICIALES}
    
    with tab_f:
        for enc in LISTA_ENCARGOS_OFICIALES:
            ocupados = []
            for o_enc, elegidos in st.session_state.encargos_semanales[semana_act].items():
                if o_enc != enc: ocupados.extend(elegidos)
            dispo = [al for al in alumnos_activos if al not in ocupados]
            def_e = [al for al in st.session_state.encargos_semanales[semana_act].get(enc, []) if al in dispo]
            st.session_state.encargos_semanales[semana_act][enc] = st.multiselect(f"🛠️ {enc}:", options=dispo, default=def_e, max_selections=2, key=f"box_enc_{enc}")
        st.markdown("---")
        op_e = {"5 Pts (Bien)": 5, "2 Pts (Regular)": 2, "0 Pts (Mal)": 0}
        for enc, encargados in st.session_state.encargos_semanales[semana_act].items():
            if encargados:
                st.markdown(f"**{enc}**")
                for nino in encargados:
                    c_n, c_r = st.columns([2, 2])
                    c_n.write(f"└─ {nino}")
                    pts_a = get_puntos_hoy(nino, f"Encargo_{enc}", None)
                    idx_e = list(op_e.values()).index(pts_a) if pts_a in op_e.values() else 0
                    sel_e = c_r.radio(f"r_{enc}_{nino}", list(op_e.keys()), index=idx_e, key=f"rd_{enc}_{nino}", label_visibility="collapsed")
                    if op_e[sel_e] != pts_a: set_puntos_hoy(nino, f"Encargo_{enc}", op_e[sel_e], f"Hizo {enc}")

    with tab_t:
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
        for d in dias:
            if semana_act not in st.session_state.estar_de_turno: st.session_state.estar_de_turno[semana_act] = {}
            def_t = st.session_state.estar_de_turno[semana_act].get(d, "")
            idx_t = alumnos_activos.index(def_t) + 1 if def_t in alumnos_activos else 0
            sel_t = st.selectbox(f"Encargado del {d}:", ["--- Sin asignar ---"] + alumnos_activos, index=idx_t, key=f"t_or_{d}")
            if sel_t != def_t:
                st.session_state.estar_de_turno[semana_act][d] = sel_t if sel_t != "--- Sin asignar ---" else ""
                guardar_datos_locales()

# --- PANTALLA: LIMPIEZA COMEDOR ---
elif st.session_state.menu_actual == "🍽️ Comedor":
    st.header("🍽️ Tareas de Limpieza (10 Puntos)")
    if st.button("🤖 Calcular Sugerencia Justa del Día"):
        al_ordenados = sorted(alumnos_activos, key=lambda x: st.session_state.contador_comedor.get(x, 0))
        st.session_state.limpieza_propuesta = {
            "Fregar Vasos y Cubiertos (2)": [al_ordenados[0], al_ordenados[1]],
            "Barrer Comedor (2)": [al_ordenados[2], al_ordenados[3]],
            "Pasar Bayetas por Mesas (2)": [al_ordenados[4], al_ordenados[5]],
            "Basura Envases (1)": [al_ordenados[6]],
            "Basura Orgánico (1)": [al_ordenados[7]],
            "Basura Papel y Cartón (1)": [al_ordenados[8]]
        }
    if "limpieza_propuesta" in st.session_state:
        roles_f = {}
        for rol, sugeridos in st.session_state.limpieza_propuesta.items():
            max_s = 2 if "(2)" in rol else 1
            roles_f[rol] = st.multiselect(f"Responsables para {rol}:", alumnos_activos, default=sugeridos, max_selections=max_s, key=f"l_rol_{rol}")
        if st.button("💾 Validar Limpieza y Asignar +10 Puntos"):
            for rol, elegidos in roles_f.items():
                for el in elegidos:
                    set_puntos_hoy(el, "Limpieza Comedor", 10, f"Rol diario: {rol}")
                    st.session_state.contador_comedor[el] += 1
            st.success("¡Cuadrante guardado!")

# --- PANTALLA: EXTRAS ---
elif st.session_state.menu_actual == "💪 Extras":
    st.header("💪 Marcador de Encargos Extra en Vivo")
    motivo_live = st.text_input("Trabajo Extra Actual:", "Ayudar a ordenar el pabellón")
    st.markdown("---")
    for al in sorted(alumnos_activos):
        c_name, c_btn = st.columns([3, 1])
        c_name.write(f"🏃 **{al}**")
        if c_btn.button(f"➕ 1 Pt Extra", key=f"b_ex_v_{al}"):
            set_puntos_hoy(al, "Extra", 1, motivo_live)
            st.toast(f"💪 +1 Punto Extra añadido a {al} por '{motivo_live}'", icon="💪")
            st.rerun()
    st.markdown("---")
    st.subheader("🔍 Historial de Extras Añadidos Hoy")
    if not st.session_state.historico_puntos.empty:
        df_ex_hoy = st.session_state.historico_puntos[(st.session_state.historico_puntos['Fecha'].astype(str) == str(fecha_hoy)) & (st.session_state.historico_puntos['Actividad'] == "Extra")]
        st.dataframe(df_ex_hoy[['Alumno', 'Puntos', 'Detalle']], width='stretch')

# --- PANTALLA: JUEGOS ---
elif st.session_state.menu_actual == "🧠 Juegos":
    st.header("🧠 Puntuación de Juegos del Día")
    nombres_j = ["Alfa", "Beta", "Gamma", "Delta"]
    mapa_j = {5: "5 Puntos", 3: "3 Puntos", 2: "2 Puntos", 0: "0 Puntos"}
    motivo_juego = st.text_input("Nombre del juego de hoy:", "Gran Gymkhana")
    for eq in nombres_j:
        cap_name = st.session_state.get(f"c_dep_{eq}", "")
        tag_j = f"Equipo {eq} (Capitán: {cap_name})" if cap_name else f"Equipo {eq}"
        st.markdown(f"##### {tag_j}")
        pts_juego = st.selectbox(f"Puntos para {tag_j}:", [5, 3, 2, 0], format_func=lambda x: mapa_j[x], key=f"pts_j_s_{eq}")
        if st.button(f"Confirmar puntos de {tag_j}", key=f"b_j_s_{eq}"):
            miembros_eq = st.session_state.get(f"m_dep_{eq}", [])
            if cap_name: set_puntos_hoy(cap_name, "Juegos", pts_juego, f"Juego: {motivo_juego} ({eq})")
            for m in miembros_eq: set_puntos_hoy(m, "Juegos", pts_juego, f"Juego: {motivo_juego} ({eq})")
            st.success(f"Puntos asignados a {tag_j}")

# --- PANTALLA: VÍDEO FORMACIÓN ---
elif st.session_state.menu_actual == "🎥 Vídeo":
    st.header("🎥 Preguntas del Vídeo de Formación (2 Pts por Acierto)")
    if 'vid_preg_num' not in st.session_state: st.session_state.vid_preg_num = 1
    conteo_v = {al: len(st.session_state.historico_puntos[(st.session_state.historico_puntos['Alumno'] == al) & (st.session_state.historico_puntos['Actividad'] == "Video Formación")]) if not st.session_state.historico_puntos.empty else 0 for al in alumnos_activos}

    if st.button("🔄 Generar / Congelar Fila del Día"):
        st.session_state.fixed_queue = sorted(alumnos_activos, key=lambda x: conteo_v[x])
        st.session_state.vid_pointer = 0
        st.success("¡Fila fijada correctamente!")

    if 'fixed_queue' not in st.session_state:
        st.session_state.fixed_queue = sorted(alumnos_activos, key=lambda x: conteo_v[x])
        st.session_state.vid_pointer = 0

    cola_fija = st.session_state.fixed_queue
    total_cola = len(cola_fija)
    p = st.session_state.vid_pointer
    if p >= total_cola: p = 0; st.session_state.vid_pointer = 0
    
    st.subheader(f"❓ Pregunta Actual N° {st.session_state.vid_preg_num}")
    titular = cola_fija[p] if total_cola > 0 else "Nadie"
    st.info(f"🎯 **Pregunta dirigida a:** {titular}")
    
    c_t1, c_t2 = st.columns([3, 1])
    c_t1.write(f"🔹 Principal: **{titular}**")
    if c_t2.button("✅ Acertó Principal (+2 Pts)", key="v_tit_b"):
        set_puntos_hoy(titular, "Video Formación", 2, f"Pregunta {st.session_state.vid_preg_num}")
        st.session_state.vid_pointer = (cola_fija.index(titular) + 1) % total_cola
        st.session_state.vid_preg_num += 1
        st.rerun()
        
    st.markdown("---")
    st.write("**Cadena de Rebotes:**")
    for idx in range(1, 6):
        if total_cola > idx:
            reb_alumno = cola_fija[(p + idx) % total_cola]
            cr_n, cr_b = st.columns([3, 1])
            cr_n.write(f"↪️ Rebote {idx}: {reb_alumno}")
            if cr_b.button(f"💥 Acertó Rebote {idx} (+2)", key=f"v_r_b_{idx}"):
                set_puntos_hoy(reb_alumno, "Video Formación", 2, f"Pregunta {st.session_state.vid_preg_num} - Rebote {idx}")
                st.session_state.vid_pointer = (cola_fija.index(reb_alumno) + 1) % total_cola
                st.session_state.vid_preg_num += 1
                st.rerun()
                
    if st.button("⏭️ Saltar Pregunta (Nadie sumó)"):
        st.session_state.vid_pointer = (st.session_state.vid_pointer + 1) % total_cola
        st.session_state.vid_preg_num += 1
        st.rerun()

# --- PANTALLA: MULTAS ---
elif st.session_state.menu_actual == "⚠️ Multas":
    st.header("⚠️ Registro de Penalizaciones Especiales")
    ninos_a_penalizar = st.multiselect("Selecciona los alumnos implicados:", sorted(alumnos_activos))
    motivo_p = st.text_input("Motivo de la infracción:", placeholder="Estar de pie gritando")
    
    c1, c2, c3, c4, c5 = st.columns(5)
    puntos_a_quitar = None
    if c1.button("📉 -1 Pt"): puntos_a_quitar = -1
    if c2.button("📉 -2 Pts"): puntos_a_quitar = -2
    if c3.button("📉 -3 Pts"): puntos_a_quitar = -3
    if c4.button("📉 -4 Pts"): puntos_a_quitar = -4
    if c5.button("📉 -5 Pts"): puntos_a_quitar = -5
        
    if puntos_a_quitar is not None and ninos_a_penalizar and motivo_p:
        for al_p in ninos_a_penalizar:
            nueva_fila = pd.DataFrame([{'Fecha': str(fecha_hoy), 'Alumno': al_p, 'Actividad': "Penalizacion", 'Puntos': puntos_a_quitar, 'Detalle': motivo_p, 'Semana': semana_act}])
            st.session_state.historico_puntos = pd.concat([st.session_state.historico_puntos, nueva_fila], ignore_index=True)
            st.toast(f"📉 Penalización de {puntos_a_quitar} Pts aplicada a {al_p}", icon="⚠️")
        guardar_datos_locales()
        st.rerun()
    st.markdown("---")
    st.subheader("🔍 Historial de Penalizaciones de Hoy")
    if not st.session_state.historico_puntos.empty:
        df_pen_hoy = st.session_state.historico_puntos[(st.session_state.historico_puntos['Fecha'].astype(str) == str(fecha_hoy)) & (st.session_state.historico_puntos['Actividad'] == "Penalizacion")]
        st.dataframe(df_pen_hoy[['Alumno', 'Puntos', 'Detalle']], width='stretch')

# --- PANTALLA: ADMIN ---
elif st.session_state.menu_actual == "🛠️ Admin":
    st.header("🛠️ Configuración e Inicialización")
    st.subheader("🚨 Eliminar Alumno de los Registros")
    alumno_a_borrar = st.selectbox("Selecciona el alumno a eliminar:", ["--- Selecciona ---"] + sorted(st.session_state.alumnos_master))
    
    if st.button("❌ Eliminar Alumno Definitivamente", type="primary"):
        if alumno_a_borrar != "--- Selecciona ---":
            st.session_state.alumnos_master.remove(alumno_a_borrar)
            if alumno_a_borrar in st.session_state.oraciones_aprendidas: del st.session_state.oraciones_aprendidas[alumno_a_borrar]
            if alumno_a_borrar in st.session_state.contador_comedor: del st.session_state.contador_comedor[alumno_a_borrar]
            for s in st.session_state.asistencia:
                if alumno_a_borrar in st.session_state.asistencia[s]: del st.session_state.asistencia[s][alumno_a_borrar]
            guardar_datos_locales()
            st.toast(f"🔥 {alumno_a_borrar} ha sido eliminado del sistema", icon="🗑️")
            st.rerun()
            
    st.markdown("---")
    st.subheader("📥 Carga de Puntos a Granel (Histórico de Semana 1)")
    with st.form("form_granel"):
        alumno_g = st.selectbox("Selecciona al Alumno:", sorted(st.session_state.alumnos_master))
        puntos_g = st.number_input("Puntos Totales Acumulados:", min_value=0, max_value=500, value=0)
        motivo_g = st.text_input("Origen o motivo del volcado:", "Volcado masivo Excel Semana 1 de pruebas")
        if st.form_submit_button("🚀 Inyectar Puntos a Granel"):
            if puntos_g > 0:
                nueva_fila = pd.DataFrame([{'Fecha': str(fecha_hoy), 'Alumno': alumno_g, 'Actividad': "Volcado Inicial", 'Puntos': puntos_g, 'Detalle': motivo_g, 'Semana': "Semana 1"}])
                st.session_state.historico_puntos = pd.concat([st.session_state.historico_puntos, nueva_fila], ignore_index=True)
                guardar_datos_locales()
                st.success(f"¡Inyectados {puntos_g} puntos con éxito!")
            else: st.error("Introduce una puntuación mayor que cero.")

    st.markdown("---")
    st.subheader("🆕 Alta de Alumnos Nuevos")
    nuevo_nombre = st.text_input("Nombre completo del nuevo alumno:")
    if st.button("➕ Dar de alta Alumno"):
        if nuevo_nombre and nuevo_nombre not in st.session_state.alumnos_master:
            st.session_state.alumnos_master.append(nuevo_nombre)
            guardar_datos_locales()
            st.success(f"¡{nuevo_nombre} dado de alta con éxito!")
            st.rerun()