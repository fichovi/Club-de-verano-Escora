import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, datetime
import json
import os

# --- 1. CONFIGURACIÓN DE PÁGINA (MARCA BLANCA MOBILE-FIRST) ---
st.set_page_config(
    page_title="Control Club de Verano", 
    page_icon="🏆", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- 2. INYECCIÓN DE CSS AVANZADO (INTERFAZ ULTRA-COMPACTA ADAPTADA A MÓVILES) ---
st.markdown("""
    <style>
        /* Ocultar menús nativos y logos de Streamlit / GitHub */
        header {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        div[data-testid="stDecoration"] {display: none !important;}
        div[data-testid="stSidebar"] {display: none !important;}
        
        /* Reducir drásticamente tamaños de letra de títulos para pantallas móviles */
        h1 { font-size: 1.15rem !important; margin-bottom: 2px !important; padding-top: 0px !important; font-weight: bold; }
        h2 { font-size: 1.0rem !important; margin-bottom: 2px !important; font-weight: bold; }
        h3 { font-size: 0.9rem !important; margin-bottom: 2px !important; font-weight: bold; }
        p, span, label, .stMarkdown { font-size: 0.8rem !important; }
        
        /* Eliminar márgenes y paddings excesivos para pegar el contenido */
        .block-container { padding-top: 0.4rem !important; padding-bottom: 0.4rem !important; padding-left: 0.5rem !important; padding-right: 0.5rem !important; }
        .element-container { margin-bottom: 0.2rem !important; }
        div[data-testid="stVerticalBlock"] { gap: 0.2rem !important; }
        
        /* Barra de navegación superior (Elementos súper pegados y deslizables) */
        div[data-testid="stHorizontalBlock"] {
            overflow-x: auto !important;
            flex-wrap: nowrap !important;
            white-space: nowrap !important;
            padding: 1px 0px !important;
            gap: 2px !important; 
        }
        
        /* Botones del menú principal */
        div[data-testid="stHorizontalBlock"] button {
            background-color: #f0f2f6 !important;
            color: #31333F !important;
            border-radius: 8px !important;
            padding: 3px 8px !important;
            border: 1px solid #cbd5e1 !important;
            font-size: 12px !important;
            font-weight: bold !important;
        }
        
        /* Reducir altura de las cajas de opciones de selección (Radios de puntuación) */
        div[data-testid="stWidgetLabel"] { margin-bottom: 0px !important; padding-bottom: 0px !important; }
        div[data-row-items] { gap: 4px !important; }
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
    with open("local_cancelaciones.json", "w", encoding="utf-8") as f:
        json.dump({
            "no_deporte": list(st.session_state.dates_no_deporte),
            "no_taller": list(st.session_state.dates_no_taller)
        }, f)

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
    if os.path.exists("local_cancelaciones.json"):
        with open("local_cancelaciones.json", "r") as f:
            data = json.load(f)
            st.session_state.dates_no_deporte = set(data.get("no_deporte", []))
            st.session_state.dates_no_taller = set(data.get("no_taller", []))
    else:
        st.session_state.dates_no_deporte = set()
        st.session_state.dates_no_taller = set()

if 'alumnos_master' not in st.session_state:
    cargar_datos_locales()

LISTA_ORACIONES = ["Señal Sta Cruz", "Padrenuestro", "Ave María", "Gloria", "5 pasos confesion", "Visita", "Angelus", "Oh Sra mía", "Angel Guarda", "10 mandamientos", "Empezar oracion", "Acabar oracion", "Bendicion mesa", "Acc gracias dp comer", "5 mand Sta Mad Igl", "Salve", "Bend sea pureza", "Señor mio Xto", "Acordaos", "Sacramentos"]
LISTA_ENCARGOS_OFICIALES = ["ORDEN SALA DE ESTUDIO", "ORDEN COMEDOR", "ORDEN TALLERES", "ORDEN ZONA ALMUERZO", "ORDEN VESTUARIOS", "ORDEN PISCINA", "MATERIAL DE DEPORTE", "MATERIAL DE PISCINA", "NEVERA", "VASOS", "CUBIERTOS", "TUPPERS", "AGUA COMIDA", "PLAN TARDE", "ORATORIO"]

if 'menu_actual' not in st.session_state:
    st.session_state.menu_actual = "🏠 Inicio"

# --- 4. CONFIGURACIÓN COMPACTA DE CABECERA ---
c_conf1, c_conf2 = st.columns(2)
semana_act = c_conf1.selectbox("Bloque:", ["Semana 1", "Semana 2", "Semana 3", "Semana 4"], label_visibility="collapsed")
fecha_hoy = c_conf2.date_input("Fecha:", date.today(), label_visibility="collapsed")

alumnos_activos = [al for al in st.session_state.alumnos_master if st.session_state.asistencia.get(semana_act, {}).get(al, True)]

# --- 5. MENÚ SUPERIOR DE BOTONES PEGADOS ---
items_menu = ["🏠 Inicio", "👥 Asistencia", "📊 Clasificación", "📚 Estudio", "🙏 Oraciones", "⚽ Deporte", "🙌 Deportividad", "🎨 Taller", "🧹 Encargos", "🍽️ Comedor", "💪 Extras", "🎥 Vídeo", "⚠️ Multas", "🛠️ Admin"]
nav_cols = st.columns(len(items_menu))
for idx, item in enumerate(items_menu):
    if st.session_state.menu_actual == item:
        st.markdown(f"<style>div[data-testid='stHorizontalBlock'] > div:nth-of-type({idx+1}) button {{ background-color: #1e3a8a !important; color: white !important; border: 1px solid #1e3a8a !important; }}</style>", unsafe_allow_html=True)
    if nav_cols[idx].button(item, key=f"nav_top_{item}"):
        st.session_state.menu_actual = item
        st.rerun()
st.write("---")

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
        nueva_fila = pd.DataFrame([{'Fecha': str(fecha_hoy), 'Alumno': alumno, 'Actividad': actividad, 'Puntos': puntos, 'Detalle': detalle, 'Semana': semana_act}])
        st.session_state.historico_puntos = pd.concat([st.session_state.historico_puntos, nueva_fila], ignore_index=True)
    guardar_datos_locales()

# --- PANTALLA: INICIO & HORARIO REAL ADAPTADO AL CALENDARIO ---
if st.session_state.menu_actual == "🏠 Inicio":
    st.subheader("📆 Horario Oficial del Campus")
    st.markdown(f"👦 **Asistentes esta semana:** `{len(alumnos_activos)} de {len(st.session_state.alumnos_master)}`")
    
    # MEJORA: Calcular la hora comparándola dinámicamente con la fecha elegida en el selector
    es_dia_actual = (str(fecha_hoy) == str(date.today()))
    hora_ahora = datetime.now().time()
    
    cronograma = [
        {"inicio": "09:00", "fin": "10:00", "tarea": "🎒 Tareas de Verano"},
        {"inicio": "10:00", "fin": "11:00", "tarea": "🥪 Almuerzo y Charla"},
        {"inicio": "11:00", "fin": "12:30", "tarea": "Torneo de Tenis y Pádel"},
        {"inicio": "12:30", "fin": "14:00", "tarea": "🏊 Piscina Refrescante"},
        {"inicio": "14:00", "fin": "15:00", "tarea": "🍽️ Comedor y Servicio"},
        {"inicio": "15:00", "fin": "17:00", "tarea": "⚽ Pachanga + Piscina de Tarde"},
        {"inicio": "17:00", "fin": "17:15", "tarea": "🏁 Fin de la Jornada"}
    ]
    
    # Traducir fecha elegida a nombre de día para dar claridad al monitor
    dias_semana_es = {"Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles", "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"}
    nombre_dia_elegido = dias_semana_es.get(fecha_hoy.strftime("%A"), str(fecha_hoy))
    st.info(f"📅 Mostrando planificación programada para el **{nombre_dia_elegido} {fecha_hoy.strftime('%d/%m/%Y')}**")
    
    for c in cronograma:
        t_ini = datetime.strptime(c["inicio"], "%H:%M").time()
        t_fin = datetime.strptime(c["fin"], "%H:%M").time()
        
        # El resaltado verde brillante (AHORA) solo se activa si estás visualizando el día de hoy real en el calendario
        if es_dia_actual and (t_ini <= hora_ahora <= t_fin):
            st.markdown(f'<div style="background-color: #d1fae5; border-left: 4px solid #10b981; padding: 6px; border-radius: 4px; margin-bottom: 3px; font-size:13px;"><strong>⚡ AHORA MISMO ({c["inicio"]} - {c["fin"]}):</strong> {c["tarea"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="background-color: #f3f4f6; border-left: 4px solid #9ca3af; padding: 5px; border-radius: 4px; margin-bottom: 3px; color: #6b7280; font-size:12px;">⏳ {c["inicio"]} - {c["fin"]}: {c["tarea"]}</div>', unsafe_allow_html=True)

# --- PANTALLA: ASISTENCIA SEMANAL ---
elif st.session_state.menu_actual == "👥 Asistencia":
    st.subheader("👥 Control de Asistencia Semanal")
    st.markdown(f"👦 **Total Presentes:** `{len(alumnos_activos)} de {len(st.session_state.alumnos_master)}`")
    st.caption("Desmarca a los niños que no asistan durante esta semana:")
    if semana_act not in st.session_state.asistencia: st.session_state.asistencia[semana_act] = {}
    for al in sorted(st.session_state.alumnos_master):
        if al not in st.session_state.asistencia[semana_act]: st.session_state.asistencia[semana_act][al] = True
        val_ch = st.checkbox(al, value=st.session_state.asistencia[semana_act][al], key=f"asist_tab_{al}")
        if val_ch != st.session_state.asistencia[semana_act][al]:
            st.session_state.asistencia[semana_act][al] = val_ch
            guardar_datos_locales()
            st.rerun()

# --- PANTALLA: CLASIFICACIÓN ---
elif st.session_state.menu_actual == "📊 Clasificación":
    st.subheader("📊 Resultados de Clasificación")
    tab_s, tab_g = st.tabs(["📆 Clasificación Semanal", "🏆 Acumulado General"])
    df_hist = st.session_state.historico_puntos.copy()
    
    def procesar_ranking_con_defaults(filtrar_semana=None):
        df_base = df_hist[df_hist['Semana'] == filtrar_semana].copy() if filtrar_semana else df_hist.copy()
        if not df_base.empty:
            df_grouped = df_base.groupby('Alumno')['Puntos'].sum().reset_index()
            dict_totales = dict(zip(df_grouped['Alumno'], df_grouped['Puntos']))
        else:
            dict_totales = {}
        lista_ninos = alumnos_activos if filtrar_semana else st.session_state.alumnos_master
        for al in lista_ninos:
            if al not in dict_totales: dict_totales[al] = 0
            fechas_evaluadas = df_hist['Fecha'].unique() if not df_hist.empty else [str(fecha_hoy)]
            for f in fechas_evaluadas:
                sem_f = df_hist[df_hist['Fecha'] == f]['Semana'].values[0] if not df_hist.empty and f in df_hist['Fecha'].values else  semana_act
                if not st.session_state.asistencia.get(sem_f, {}).get(al, True): continue
                if filtrar_semana and sem_f != filtrar_semana: continue
                
                has_explicit_dep = not df_hist[(df_hist['Fecha'] == f) & (df_hist['Alumno'] == al) & (df_hist['Actividad'] == "Deportividad")].empty
                if not has_explicit_dep and f not in st.session_state.dates_no_deporte: dict_totales[al] += 5
                
                has_explicit_tal = not df_hist[(df_hist['Fecha'] == f) & (df_hist['Alumno'] == al) & (df_hist['Actividad'] == "Taller")].empty
                if not has_explicit_tal and f not in st.session_state.dates_no_taller: dict_totales[al] += 5
        df_res = pd.DataFrame(list(dict_totales.items()), columns=['Alumno', 'Puntos'])
        return df_res.sort_values(by="Puntos", ascending=True)

    with tab_s:
        df_tot_sem = procesar_ranking_con_defaults(semana_act)
        fig_s = px.bar(df_tot_sem, x='Puntos', y='Alumno', orientation='h', color='Puntos', color_continuous_scale='Mint', text_auto=True)
        fig_s.update_traces(textposition='outside')
        fig_s.update_layout(height=550, xaxis=dict(fixedrange=True), yaxis=dict(fixedrange=True), margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(fig_s, width='stretch', config={'displayModeBar': False})

    with tab_g:
        df_tot_gen = procesar_ranking_con_defaults(None)
        fig_g = px.bar(df_tot_gen, x='Puntos', y='Alumno', orientation='h', color='Puntos', color_continuous_scale='Blues', text_auto=True)
        fig_g.update_traces(textposition='outside')
        fig_g.update_layout(height=650, xaxis=dict(fixedrange=True), yaxis=dict(fixedrange=True), margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(fig_g, width='stretch', config={'displayModeBar': False})
        
    st.markdown("---")
    st.subheader("🔍 Historial Técnico Completo")
    st.dataframe(st.session_state.historico_puntos.iloc[::-1], width='stretch')

# --- PANTALLA: ESTUDIO ---
elif st.session_state.menu_actual == "📚 Estudio":
    st.subheader("📚 Puntuación: Hora de Estudio")
    opciones_estudio = {"No evaluado": None, "❌ 0 Puntos": 0, "⚠️ 2 Puntos": 2, "✅ 5 Puntos": 5}
    for al in sorted(alumnos_activos):
        pts_actuales = get_puntos_hoy(al, "Estudio", None)
        index_def = list(opciones_estudio.values()).index(pts_actuales)
        st.markdown(f"**🧑 {al}**")
        seleccion = st.radio(f"Est_{al}", options=list(opciones_estudio.keys()), index=index_def, key=f"rad_est_{al}", horizontal=True, label_visibility="collapsed")
        pts_seleccionados = opciones_estudio[seleccion]
        if pts_seleccionados is not None and pts_seleccionados != pts_actuales:
            set_puntos_hoy(al, "Estudio", pts_seleccionados, "Evaluación de estudio")
            st.toast(f"✅ {al} actualizado", icon="📝")
        st.markdown("<div style='border-bottom:1px solid #f1f5f9; margin-bottom:4px;'></div>", unsafe_allow_html=True)

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
        st.markdown(f'<div style="background-color:{b["color"]}; padding:4px; border-radius:4px; font-weight:bold; margin-top:4px; font-size:11px; color:#333;">{b["nombre"]}</div>', unsafe_allow_html=True)
        for item in b["items"]:
            if st.checkbox(item, value=(item in oraciones_actuales), key=f"or_m_{al_sel}_{item}"): nuevas_oraciones.append(item)
    if nuevas_oraciones != oraciones_actuales:
        st.session_state.oraciones_aprendidas[al_sel] = nuevas_oraciones
        st.session_state.historico_puntos = st.session_state.historico_puntos[~((st.session_state.historico_puntos['Alumno'] == al_sel) & (st.session_state.historico_puntos['Actividad'] == "Oración"))]
        for o in nuevas_oraciones: set_puntos_hoy(al_sel, "Oración", 5, f"Sabe: {o}")
        st.rerun()

# --- PANTALLA: DEPORTE ---
elif st.session_state.menu_actual == "⚽ Deporte":
    st.subheader("⚽ Gestión de Deporte del Día")
    is_cancelled = str(fecha_hoy) in st.session_state.dates_no_deporte
    t_toggle = "🟢 DEPORTE ACTIVO (Pulsar para suspender)" if not is_cancelled else "🚫 HOY NO HAY DEPORTE (Puntos anulados)"
    if st.button(t_toggle, key="toggle_dep_day"):
        if is_cancelled: st.session_state.dates_no_deporte.remove(str(fecha_hoy))
        else: st.session_state.dates_no_deporte.add(str(fecha_hoy))
        guardar_datos_locales(); st.rerun()
    if not is_cancelled:
        modalidad = st.radio("Formato de hoy:", ["👥 Por Equipos", "🎾 Por Parejas (Dobles)", "🏃 Individual"], label_visibility="collapsed")
        if "Equipos" in modalidad:
            num_equipos = st.slider("Equipos:", 2, 4, 2)
            nombres_base = ["Alfa", "Beta", "Gamma", "Delta"][:num_equipos]
            for eq in nombres_base:
                st.markdown(f"##### Equipo {eq}")
                st.session_state[f"c_dep_{eq}"] = st.selectbox(f"👑 Capitán de {eq}:", [""] + alumnos_activos, key=f"c_{eq}")
                st.session_state[f"m_dep_{eq}"] = st.multiselect(f"Jugadores {eq}:", [al for al in alumnos_activos if al != st.session_state[f"c_dep_{eq}"]], key=f"j_{eq}")
            mapa_pts = {5: "1º Lugar (5 Pts)", 3: "2º Lugar (3 Pts)", 2: "3º Lugar (2 Pts)", 0: "4º Lugar (0 Pts)"}
            res = {eq: st.selectbox(f"Posición {eq}:", [5, 3, 2, 0], format_func=lambda x: mapa_pts[x], key=f"r_eq_{eq}") for eq in nombres_base}
            if st.button("💾 Registrar Torneo"):
                for eq in nombres_base:
                    pts = res[eq]
                    if st.session_state[f"c_dep_{eq}"]: set_puntos_hoy(st.session_state[f"c_dep_{eq}"], "Deporte", pts, f"Capitán {eq}")
                    for j in st.session_state[f"m_dep_{eq}"]: set_puntos_hoy(j, "Deporte", pts, f"Miembro {eq}")
                st.success("Torneo guardado.")

# --- PANTALLA: DEPORTIVIDAD ---
elif st.session_state.menu_actual == "🙌 Deportividad":
    st.subheader("🙌 Control de Deportividad")
    is_cancelled_dep = str(fecha_hoy) in st.session_state.dates_no_deporte
    if is_cancelled_dep:
        st.warning("Deporte suspendido hoy. Los 5 puntos base están desactivados.")
    else:
        opciones_dep = {"✅ Excelente (5 Pts)": 5, "⚠️ Quejas/Faltas (2 Pts)": 2, "❌ Falta Grave (0 Pts)": 0}
        for al in sorted(alumnos_activos):
            st.markdown(f"**🙌 {al}**")
            pts_act = get_puntos_hoy(al, "Deportividad", 5)
            idx_def = list(opciones_dep.values()).index(pts_act)
            sel = st.radio(f"Dep_{al}", options=list(opciones_dep.keys()), index=idx_def, key=f"rad_dep_{al}", label_visibility="collapsed")
            if opciones_dep[sel] != pts_act:
                set_puntos_hoy(al, "Deportividad", opciones_dep[sel], "Nota deportividad")
                st.toast(f"🙌 {al} actualizado", icon="🙌")
            st.markdown("<div style='border-bottom:1px solid #f1f5f9; margin-bottom:4px;'></div>", unsafe_allow_html=True)

# --- PANTALLA: TALLER ---
elif st.session_state.menu_actual == "🎨 Taller":
    st.subheader("🎨 Trabajo en los Talleres")
    is_cancelled_tal = str(fecha_hoy) in st.session_state.dates_no_taller
    t_toggle_tal = "🟢 TALLER ACTIVO (Pulsar para suspender)" if not is_cancelled_tal else "🚫 HOY NO HAY TALLER (Puntos anulados)"
    if st.button(t_toggle_tal, key="toggle_tal_day"):
        if is_cancelled_tal: st.session_state.dates_no_taller.remove(str(fecha_hoy))
        else: st.session_state.dates_no_taller.add(str(fecha_hoy))
        guardar_datos_locales(); st.rerun()
    if is_cancelled_tal:
        st.warning("Talleres suspendidos hoy. Se eliminan los 5 puntos base.")
    else:
        opciones_tal = {"✅ Trabajador (5 Pts)": 5, "⚠️ Distraído (2 Pts)": 2, "❌ Indisciplina (0 Pts)": 0}
        for al in sorted(alumnos_activos):
            st.markdown(f"**🎨 {al}**")
            pts_act = get_puntos_hoy(al, "Taller", 5)
            idx_def = list(opciones_tal.values()).index(pts_act)
            sel = st.radio(f"Tal_{al}", options=list(opciones_tal.keys()), index=idx_def, key=f"rad_tal_{al}", label_visibility="collapsed")
            if opciones_tal[sel] != pts_act:
                set_puntos_hoy(al, "Taller", opciones_tal[sel], "Nota taller")
                st.toast(f"🎨 {al} actualizado", icon="🎨")
            st.markdown("<div style='border-bottom:1px solid #f1f5f9; margin-bottom:4px;'></div>", unsafe_allow_html=True)

# --- PANTALLA: ENCARGOS ---
elif st.session_state.menu_actual == "🧹 Encargos":
    st.subheader("🧹 Distribución de Encargos")
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
            if sel_t != def_t: st.session_state.estar_de_turno[semana_act][d] = sel_t if sel_t != "--- Sin asignar ---" else ""; guardar_datos_locales()

# --- PANTALLA: LIMPIEZA COMEDOR ---
elif st.session_state.menu_actual == "🍽️ Comedor":
    st.subheader("🍽️ Tareas de Limpieza (10 Puntos)")
    if st.button("🤖 Calcular Sugerencia Justa del Día"):
        al_ordenados = sorted(alumnos_activos, key=lambda x: st.session_state.contador_comedor.get(x, 0))
        st.session_state.limpieza_propuesta = {"Fregar Vasos y Cubiertos (2)": [al_ordenados[0], al_ordenados[1]], "Barrer Comedor (2)": [al_ordenados[2], al_ordenados[3]], "Pasar Bayetas por Mesas (2)": [al_ordenados[4], al_ordenados[5]], "Basura Envases (1)": [al_ordenados[6]], "Basura Orgánico (1)": [al_ordenados[7]], "Basura Papel y Cartón (1)": [al_ordenados[8]]}
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

# --- PANTALLA: EXTRAS EN VIVO ---
elif st.session_state.menu_actual == "💪 Extras":
    st.subheader("💪 Marcador de Encargos Extra")
    motivo_live = st.text_input("Trabajo Extra Actual:", "Ayudar a ordenar materiales")
    for al in sorted(alumnos_activos):
        c_name, c_btn = st.columns([3, 1])
        c_name.write(f"🏃 **{al}**")
        if c_btn.button(f"➕ 1 Pt", key=f"b_ex_v_{al}"):
            nueva_f = pd.DataFrame([{'Fecha': str(fecha_hoy), 'Alumno': al, 'Actividad': "Extra", 'Puntos': 1, 'Detalle': motivo_live, 'Semana': semana_act}])
            st.session_state.historico_puntos = pd.concat([st.session_state.historico_puntos, nueva_f], ignore_index=True)
            guardar_datos_locales()
            st.toast(f"💪 +1 Pt Extra a {al}", icon="💪")
            st.rerun()
    st.markdown("---")
    st.subheader("🔍 Historial de Extras Añadidos Hoy")
    if not st.session_state.historico_puntos.empty:
        df_ex_hoy = st.session_state.historico_puntos[(st.session_state.historico_puntos['Fecha'].astype(str) == str(fecha_hoy)) & (st.session_state.historico_puntos['Actividad'] == "Extra")]
        st.dataframe(df_ex_hoy[['Alumno', 'Puntos', 'Detalle']], width='stretch')

# --- PANTALLA: JUEGOS ---
elif st.session_state.menu_actual == "🧠 Juegos":
    st.subheader("🧠 Puntuación de Juegos del Día")
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
    st.subheader("🎥 Preguntas del Vídeo (2 Pts)")
    if 'vid_preg_num' not in st.session_state: st.session_state.vid_preg_num = 1
    conteo_v = {al: len(st.session_state.historico_puntos[(st.session_state.historico_puntos['Alumno'] == al) & (st.session_state.historico_puntos['Actividad'] == "Video Formación")]) if not st.session_state.historico_puntos.empty else 0 for al in alumnos_activos}
    if st.button("🔄 Generar / Congelar Fila del Día"):
        st.session_state.fixed_queue = sorted(alumnos_activos, key=lambda x: conteo_v[x])
        st.session_state.vid_pointer = 0
        st.success("¡Fila fijada!")
    if 'fixed_queue' not in st.session_state:
        st.session_state.fixed_queue = sorted(alumnos_activos, key=lambda x: conteo_v[x])
        st.session_state.vid_pointer = 0
    cola_fija = st.session_state.fixed_queue
    total_cola = len(cola_fija)
    p = st.session_state.vid_pointer
    if p >= total_cola: p = 0; st.session_state.vid_pointer = 0
    st.write(f"❓ **Pregunta N° {st.session_state.vid_preg_num}**")
    titular = cola_fija[p] if total_cola > 0 else "Nadie"
    st.info(f"🎯 **Pregunta para:** {titular}")
    c_t1, c_t2 = st.columns([3, 1])
    c_t1.write(f"🔹 Principal: **{titular}**")
    if c_t2.button("✅ Acertó", key="v_tit_b"):
        set_puntos_hoy(titular, "Video Formación", 2, f"Pregunta {st.session_state.vid_preg_num}")
        st.session_state.vid_pointer = (cola_fija.index(titular) + 1) % total_cola
        st.session_state.vid_preg_num += 1
        st.rerun()
    st.markdown("---")
    for idx in range(1, 6):
        if total_cola > idx:
            reb_alumno = cola_fija[(p + idx) % total_cola]
            cr_n, cr_b = st.columns([3, 1])
            cr_n.write(f"↪️ Rebote {idx}: {reb_alumno}")
            if cr_b.button(f"💥 Acertó Rebote {idx}", key=f"v_r_b_{idx}"):
                set_puntos_hoy(reb_alumno, "Video Formación", 2, f"Preg {st.session_state.vid_preg_num} - Reb {idx}")
                st.session_state.vid_pointer = (cola_fija.index(reb_alumno) + 1) % total_cola
                st.session_state.vid_preg_num += 1
                st.rerun()
    if st.button("⏭️ Saltar Pregunta"): st.session_state.vid_pointer = (st.session_state.vid_pointer + 1) % total_cola; st.session_state.vid_preg_num += 1; st.rerun()

# --- PANTALLA: MULTAS ---
elif st.session_state.menu_actual == "⚠️ Multas":
    st.subheader("⚠️ Registro de Penalizaciones Especiales")
    ninos_a_penalizar = st.multiselect("Selecciona los alumnos implicados:", sorted(alumnos_activos))
    motivo_p = st.text_input("Motivo de la infracción:", placeholder="Ej. Hablar alto o levantarse")
    st.write("Elige los puntos a restar (Se guardará al hacer clic):")
    c1, c2, c3, c4, c5 = st.columns(5)
    puntos_a_quitar = None
    if c1.button("📉 -1"): puntos_a_quitar = -1
    if c2.button("📉 -2"): puntos_a_quitar = -2
    if c3.button("📉 -3"): puntos_a_quitar = -3
    if c4.button("📉 -4"): puntos_a_quitar = -4
    if c5.button("📉 -5"): puntos_a_quitar = -5
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
        if not df_pen_hoy.empty: st.dataframe(df_pen_hoy[['Alumno', 'Puntos', 'Detalle']], width='stretch')

# --- PANTALLA: ADMIN (MÓDULO LIMPIO SIN TEXTOS ROTOS) ---
elif st.session_state.menu_actual == "🛠️ Admin":
    st.subheader("🛠️ Panel de Administración")
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
            st.toast(f"🗑️ Eliminado: {alumno_a_borrar}")
            st.rerun()
    st.markdown("---")
    st.subheader("📥 Carga a Granel (Semana 1)")
    with st.form("form_granel"):
        alumno_g = st.selectbox("Alumno:", sorted(st.session_state.alumnos_master))
        puntos_g = st.number_input("Puntos:", min_value=0, max_value=500, value=0)
        motivo_g = st.text_input("Motivo:", "Volcado masivo Excel Semana 1")
        if st.form_submit_button("🚀 Inyectar"):
            if puntos_g > 0:
                nueva_fila = pd.DataFrame([{'Fecha': str(fecha_hoy), 'Alumno': alumno_g, 'Actividad': "Volcado Inicial", 'Puntos': puntos_g, 'Detalle': motivo_g, 'Semana': "Semana 1"}])
                st.session_state.historico_puntos = pd.concat([st.session_state.historico_puntos, nueva_fila], ignore_index=True)
                guardar_datos_locales()
                st.success("Puntos inyectados.")
            else: st.error("Introduce una puntuación válida.")