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

# --- 2. INYECCIÓN DE CSS MAESTRO (DISEÑO COMPACTO ULTRA-AJUSTADO PARA SMARTPHONES) ---
st.markdown("""
    <style>
        /* Ocultar elementos oficiales de Streamlit y GitHub */
        header {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        div[data-testid="stDecoration"] {display: none !important;}
        div[data-testid="stSidebar"] {display: none !important;}
        
        /* Reducción drástica de fuentes para evitar renglones dobles en móviles */
        h1 { font-size: 1.1rem !important; margin-bottom: 2px !important; padding-top: 0px !important; font-weight: bold; }
        h2 { font-size: 0.95rem !important; margin-bottom: 2px !important; font-weight: bold; }
        h3 { font-size: 0.85rem !important; margin-bottom: 2px !important; font-weight: bold; }
        p, span, label, .stMarkdown { font-size: 0.78rem !important; }
        
        /* Compactación máxima de espacios y márgenes */
        .block-container { padding-top: 0.3rem !important; padding-bottom: 0.3rem !important; padding-left: 0.4rem !important; padding-right: 0.4rem !important; }
        .element-container { margin-bottom: 0.15rem !important; }
        div[data-testid="stVerticalBlock"] { gap: 0.15rem !important; }
        
        /* Barra de navegación superior ultra-pegada con scroll horizontal fluido */
        div[data-testid="stHorizontalBlock"] {
            overflow-x: auto !important;
            flex-wrap: nowrap !important;
            white-space: nowrap !important;
            padding: 1px 0px !important;
            gap: 1px !important; /* Espaciado mínimo absoluto entre pestañas */
        }
        
        /* Estilo súper compacto de los botones del menú principal */
        div[data-testid="stHorizontalBlock"] button {
            background-color: #f0f2f6 !important;
            color: #31333F !important;
            border-radius: 6px !important;
            padding: 2px 6px !important;
            border: 1px solid #cbd5e1 !important;
            font-size: 11px !important;
            font-weight: bold !important;
        }
        
        /* Corrección de solapamiento en Oraciones y selectores */
        div[data-testid="stCheckbox"] { padding: 2px 0px !important; margin: 0px !important; }
        .stRadio > div { gap: 2px !important; padding: 0px !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. CARGA Y PERSISTENCIA DE ARCHIVOS LOCALES CON AUDITORÍA ---
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
        # Asegurar retrocompatibilidad con la columna de Hora
        if 'Hora' not in st.session_state.historico_puntos.columns:
            st.session_state.historico_puntos['Hora'] = "12:00:00"
    else:
        st.session_state.historico_puntos = pd.DataFrame(columns=['Fecha', 'Hora', 'Alumno', 'Actividad', 'Puntos', 'Detalle', 'Semana'])
        
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
LISTA_ENCARGOS_OFICIALES = ["ORDEN SALA DE ESTUDIO 📚", "ORDEN COMEDOR 🍽️", "ORDEN TALLERES 🎨", "ORDEN ZONA ALMUERZO 🥪", "ORDEN VESTUARIOS 👕", "ORDEN PISCINA 🏊", "MATERIAL DE DEPORTE ⚽", "MATERIAL DE PISCINA 🛟", "NEVERA ❄️", "VASOS 🥛", "CUBIERTOS 🍴", "TUPPERS 🍱", "AGUA COMIDA 💧", "PLAN TARDE 🌅", "ORATORIO ⛪"]

if 'menu_actual' not in st.session_state:
    st.session_state.menu_actual = "🏠 Inicio"

# --- 4. CONFIGURACIÓN COMPACTA DE CABECERA ---
c_conf1, c_conf2 = st.columns(2)
semana_act = c_conf1.selectbox("Bloque:", ["Semana 1", "Semana 2", "Semana 3", "Semana 4"], label_visibility="collapsed")
fecha_hoy = c_conf2.date_input("Fecha:", date.today(), label_visibility="collapsed")

alumnos_activos = [al for al in st.session_state.alumnos_master if st.session_state.asistencia.get(semana_act, {}).get(al, True)]

# --- 5. MENÚ SUPERIOR DE BOTONES PEGADOS CON ICONOS COMPACTOS ---
items_menu = ["🏠 Inicio", "👥 Asist", "📊 Rank", "📚 Est", "🙏 Orac", "⚽ Dep", "🙌 Depor", "🎨 Tal", "🧹 Enc", "🍽️ Com", "💪 Ext", "🎥 Vid", "⚠️ Mult", "🛠️ Admin"]
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
    hora_actual = datetime.now().strftime("%H:%M:%S") # Inyectar marca de tiempo exacta hh:mm:ss solicitado
    if cond.any():
        st.session_state.historico_puntos.loc[cond, 'Puntos'] = puntos
        st.session_state.historico_puntos.loc[cond, 'Hora'] = hora_actual
        st.session_state.historico_puntos.loc[cond, 'Detalle'] = detalle
    else:
        nueva_fila = pd.DataFrame([{'Fecha': str(fecha_hoy), 'Hora': hora_actual, 'Alumno': alumno, 'Actividad': actividad, 'Puntos': puntos, 'Detalle': detalle, 'Semana': semana_act}])
        st.session_state.historico_puntos = pd.concat([st.session_state.historico_puntos, nueva_fila], ignore_index=True)
    guardar_datos_locales()

# --- PANTALLA: INICIO & HORARIO OFICIAL DINÁMICO POR DÍA DE LA SEMANA ---
if st.session_state.menu_actual == "🏠 Inicio":
    st.subheader("🏠 Inicio: Estado del Campus")
    st.markdown(f"👦 **Alumnos Asistentes esta Semana:** `{len(alumnos_activos)} de {len(st.session_state.alumnos_master)}`")
    
    # Lógica de detección automática del día seleccionado en el calendario
    es_dia_actual = (str(fecha_hoy) == str(date.today()))
    hora_ahora = datetime.now().time()
    nombre_dia_eng = fecha_hoy.strftime("%A")
    
    # Diccionario con vuestro horario oficial estricto (Imagen 1000257882.jpg)
    horarios_oficiales = {
        "Monday": [
            {"inicio": "09:00", "fin": "10:00", "tarea": "🎒 Tareas de Verano"},
            {"inicio": "10:00", "fin": "11:00", "tarea": "🥪 Almuerzo + Avisos"},
            {"inicio": "11:00", "fin": "12:00", "tarea": "👑 Rey de la Pista Fútbol-Sala"},
            {"inicio": "12:00", "fin": "13:00", "tarea": "🏊 Piscina Libre"},
            {"inicio": "13:00", "fin": "14:00", "tarea": "🪙 Fútbol Chapas"},
            {"inicio": "14:00", "fin": "15:00", "tarea": "🍽️ Comida"},
            {"inicio": "15:00", "fin": "17:00", "tarea": "🏆 Torneos de Tarde"}
        ],
        "Tuesday": [
            {"inicio": "09:00", "fin": "10:00", "tarea": "🎒 Tareas de Verano"},
            {"inicio": "10:00", "fin": "11:00", "tarea": "🗣️ Plática + Almuerzo"},
            {"inicio": "11:00", "fin": "12:30", "tarea": "⚾ Béisbol en Pista"},
            {"inicio": "12:30", "fin": "13:00", "tarea": "🏊 Piscina"},
            {"inicio": "13:00", "fin": "14:00", "tarea": "🎨 Termorretractil / Cerámica"},
            {"inicio": "14:00", "fin": "15:00", "tarea": "🍽️ Comida"},
            {"inicio": "15:00", "fin": "17:00", "tarea": "🧠 Superquiz + Torneos"}
        ],
        "Wednesday": [
            {"inicio": "09:00", "fin": "10:00", "tarea": "🎒 Tareas de Verano"},
            {"inicio": "10:00", "fin": "11:00", "tarea": "💬 Almuerzo + Charla"},
            {"inicio": "11:00", "fin": "12:30", "tarea": "🎾 Torneo de Tenis y Pádel"},
            {"inicio": "12:30", "fin": "14:00", "tarea": "🏊 Piscina"},
            {"inicio": "14:00", "fin": "15:00", "tarea": "🍽️ Comida"},
            {"inicio": "15:00", "fin": "17:00", "tarea": "🌊 Pachanga + Piscina de Tarde"}
        ],
        "Thursday": [
            {"inicio": "09:00", "fin": "10:00", "tarea": "🎒 Tareas de Verano"},
            {"inicio": "10:00", "fin": "17:00", "tarea": "🚌 EXCURSIÓN A XÀTIVA (Piscina + Barbacoa)"}
        ],
        "Friday": [
            {"inicio": "09:00", "fin": "10:00", "tarea": "🎒 Tareas de Verano"},
            {"inicio": "10:00", "fin": "11:00", "tarea": "🎥 Vídeo + Almuerzo"},
            {"inicio": "11:00", "fin": "13:00", "tarea": "💦 Gymkhana Acuática"},
            {"inicio": "13:00", "fin": "14:00", "tarea": "🎨 Termorretractil / Cerámica"},
            {"inicio": "14:00", "fin": "15:00", "tarea": "🍽️ Comida"},
            {"inicio": "15:00", "fin": "17:00", "tarea": "🍿 Peliculón de Viernes"}
        ]
    }
    
    dias_es = {"Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles", "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"}
    st.markdown(f"📅 Planificación Oficial: **{dias_es.get(nombre_day := nombre_dia_eng, nombre_day)}**")
    
    cronograma_hoy = horarios_oficiales.get(nombre_dia_eng, [{"inicio": "09:00", "fin": "17:00", "tarea": "✨ Descanso o Actividad Extraordinaria"}])
    
    for c in cronograma_hoy:
        t_ini = datetime.strptime(c["inicio"], "%H:%M").time()
        t_fin = datetime.strptime(c["fin"], "%H:%M").time()
        if es_dia_actual and (t_ini <= hora_ahora <= t_fin):
            st.markdown(f'<div style="background-color: #d1fae5; border-left: 4px solid #10b981; padding: 6px; border-radius: 4px; margin-bottom: 3px; font-size:12px;"><strong>⚡ AHORA ({c["inicio"]} - {c["fin"]}):</strong> {c["tarea"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="background-color: #f3f4f6; border-left: 4px solid #9ca3af; padding: 5px; border-radius: 4px; margin-bottom: 3px; color: #6b7280; font-size:11px;">⏳ {c["inicio"]} - {c["fin"]}: {c["tarea"]}</div>', unsafe_allow_html=True)

# --- PANTALLA: ASISTENCIA SEMANAL ---
elif st.session_state.menu_actual == "👥 Asist":
    st.subheader("👥 Control de Asistencia Semanal")
    st.markdown(f"👦 **Total Asistentes:** `{len(alumnos_activos)} de {len(st.session_state.alumnos_master)}`")
    if semana_act not in st.session_state.asistencia: st.session_state.asistencia[semana_act] = {}
    for al in sorted(st.session_state.alumnos_master):
        if al not in st.session_state.asistencia[semana_act]: st.session_state.asistencia[semana_act][al] = True
        val_ch = st.checkbox(al, value=st.session_state.asistencia[semana_act][al], key=f"asist_tab_{al}")
        if val_ch != st.session_state.asistencia[semana_act][al]:
            st.session_state.asistencia[semana_act][al] = val_ch
            guardar_datos_locales()
            st.rerun()

# --- PANTALLA: CLASIFICACIÓN CON GRÁFICOS APILADOS POR COLORES (ESTADÍSTICAS) ---
elif st.session_state.menu_actual == "📊 Rank":
    st.subheader("📊 Resultados de Clasificación")
    tab_s, tab_g = st.tabs(["📆 Clasificación Semanal", "🏆 Acumulado General"])
    df_hist = st.session_state.historico_puntos.copy()
    
    def generar_tabla_desglosada(filtrar_semana=None):
        df_base = df_hist[df_hist['Semana'] == filtrar_semana].copy() if filtrar_semana else df_hist.copy()
        lista_ninos = alumnos_activos if filtrar_semana else st.session_state.alumnos_master
        
        registros_puntos = []
        # Agregar los puntos manuales existentes en la base de datos
        if not df_base.empty:
            for _, fila in df_base.iterrows():
                registros_puntos.append({'Alumno': fila['Alumno'], 'Actividad': fila['Actividad'], 'Puntos': float(fila['Puntos'])})
                
        # Inyectar de modo automático los +5 predeterminados por día no cancelado
        fechas_evaluadas = df_hist['Fecha'].unique() if not df_hist.empty else [str(fecha_hoy)]
        for al in lista_ninos:
            for f in fechas_evaluadas:
                sem_f = df_hist[df_hist['Fecha'] == f]['Semana'].values[0] if not df_hist.empty and f in df_hist['Fecha'].values else semana_act
                if not st.session_state.asistencia.get(sem_f, {}).get(al, True): continue
                if filtrar_semana and sem_f != filtrar_semana: continue
                
                # Deportividad por defecto
                has_explicit_dep = not df_hist[(df_hist['Fecha'] == f) & (df_hist['Alumno'] == al) & (df_hist['Actividad'] == "Deportividad")].empty
                if not has_explicit_dep and f not in st.session_state.dates_no_deporte:
                    registros_puntos.append({'Alumno': al, 'Actividad': 'Deportividad (Auto)', 'Puntos': 5.0})
                    
                # Taller por defecto
                has_explicit_tal = not df_hist[(df_hist['Fecha'] == f) & (df_hist['Alumno'] == al) & (df_hist['Actividad'] == "Taller")].empty
                if not has_explicit_tal and f not in st.session_state.dates_no_taller:
                    registros_puntos.append({'Alumno': al, 'Actividad': 'Taller (Auto)', 'Puntos': 5.0})
                    
        if not registros_puntos:
            return pd.DataFrame(columns=['Alumno', 'Actividad', 'Puntos'])
        return pd.DataFrame(registros_puntos)

    with tab_s:
        df_sem_desglose = generar_tabla_desglosada(semana_act)
        if not df_sem_desglose.empty:
            # MEJORA SOLICITADA: Gráfico apilado por colores de actividad (Estadísticas en vivo)
            fig_s = px.bar(df_sem_desglose, x='Puntos', y='Alumno', color='Actividad', orientation='h', title="Origen de Puntos - Esta Semana", color_continuous_scale='Mint')
            fig_s.update_layout(height=550, barmode='stack', xaxis=dict(fixedrange=True), yaxis=dict(fixedrange=True, categoryorder='total ascending'))
            st.plotly_chart(fig_s, width='stretch', config={'displayModeBar': False})

    with tab_g:
        df_gen_desglose = generar_tabla_desglosada(None)
        if not df_gen_desglose.empty:
            fig_g = px.bar(df_gen_desglose, x='Puntos', y='Alumno', color='Actividad', orientation='h', title="Origen de Puntos - Historial General", color_continuous_scale='Blues')
            fig_g.update_layout(height=650, barmode='stack', xaxis=dict(fixedrange=True), yaxis=dict(fixedrange=True, categoryorder='total ascending'))
            st.plotly_chart(fig_g, width='stretch', config={'displayModeBar': False})
        
    st.markdown("---")
    st.subheader("🔍 Historial Técnico con Horas (hh:mm:ss)")
    st.dataframe(st.session_state.historico_puntos.iloc[::-1], width='stretch')

# --- PANTALLA: ESTUDIO (DISEÑO SELECTOR VERTICAL COMPACTO EXCLUSIVO) ---
elif st.session_state.menu_actual == "📚 Est":
    st.subheader("📚 Puntuación: Hora de Estudio")
    opciones_estudio = {"No evaluado": None, "❌ 0 Puntos": 0, "⚠️ 2 Puntos": 2, "✅ 5 Puntos": 5}
    for al in sorted(alumnos_activos):
        pts_actuales = get_puntos_hoy(al, "Estudio", None)
        index_def = list(opciones_estudio.values()).index(pts_actuales)
        
        # MEJORA SOLICITADA: Opciones verticales en lugar de columnas para evitar el salto feo
        st.markdown(f"**🧑 {al}**")
        seleccion = st.radio(f"Est_{al}", options=list(opciones_estudio.keys()), index=index_def, key=f"rad_est_{al}", horizontal=False)
        pts_seleccionados = opciones_estudio[seleccion]
        if pts_seleccionados is not None and pts_seleccionados != pts_actuales:
            set_puntos_hoy(al, "Estudio", pts_seleccionados, "Nota estudio")
            st.toast(f"✅ {al} Guardado", icon="📝")
        st.markdown("<div style='border-bottom:1px dashed #cbd5e1; margin-bottom:5px; margin-top:5px;'></div>", unsafe_allow_html=True)

# --- PANTALLA: ORACIONES (CORREGIDO SOLAPAMIENTO DE TÍTULOS DE SEMANA) ---
elif st.session_state.menu_actual == "🙏 Orac":
    st.subheader("🙏 Matriz de Oraciones Aprendidas")
    al_sel = st.selectbox("Selecciona un alumno:", sorted(alumnos_activos))
    oraciones_actuales = st.session_state.oraciones_aprendidas.get(al_sel, [])
    nuevas_oraciones = []
    
    bloques_semanales = [
        {"nombre": "🟢 SEMANA 1", "items": LISTA_ORACIONES[0:5], "color": "#d1fae5"},
        {"nombre": "🔵 SEMANA 2", "items": LISTA_ORACIONES[5:10], "color": "#e0f2fe"},
        {"nombre": "🟡 SEMANA 3", "items": LISTA_ORACIONES[10:15], "color": "#fef3c7"},
        {"nombre": "🟠 SEMANA 4", "items": LISTA_ORACIONES[15:20], "color": "#fee2e2"}
    ]
    for b in bloques_semanales:
        # CORRECCIÓN: Separación de bloque limpia con padding y sin float absoluto para evitar solapamientos
        st.markdown(f'<div style="background-color:{b["color"]}; padding:5px; border-radius:4px; font-weight:bold; margin-top:12px; margin-bottom:6px; font-size:11px; color:#1e293b;">{b["nombre"]}</div>', unsafe_allow_html=True)
        for item in b["items"]:
            if st.checkbox(item, value=(item in oraciones_actuales), key=f"or_m_{al_sel}_{item}"): nuevas_oraciones.append(item)
            
    if nuevas_oraciones != oraciones_actuales:
        st.session_state.oraciones_aprendidas[al_sel] = nuevas_oraciones
        st.session_state.historico_puntos = st.session_state.historico_puntos[~((st.session_state.historico_puntos['Alumno'] == al_sel) & (st.session_state.historico_puntos['Actividad'] == "Oración"))]
        for o in nuevas_oraciones: set_puntos_hoy(al_sel, "Oración", 5, f"Sabe: {o}")
        st.rerun()

# --- PANTALLA: DEPORTE ---
elif st.session_state.menu_actual == "⚽ Dep":
    st.subheader("⚽ Gestión de Deporte del Día")
    is_cancelled = str(fecha_hoy) in st.session_state.dates_no_deporte
    t_toggle = "🟢 DEPORTE ACTIVO (Pulsar para suspender)" if not is_cancelled else "🚫 HOY NO HAY DEPORTE (Puntos anulados)"
    if st.button(t_toggle, key="toggle_dep_day"):
        if is_cancelled: st.session_state.dates_no_deporte.remove(str(fecha_hoy))
        else: st.session_state.dates_no_deporte.add(str(fecha_hoy))
        guardar_datos_locales(); st.rerun()
        
    if not is_cancelled:
        modalidad = st.radio("Formato de hoy:", ["👥 Por Equipos", "🎾 Por Parejas (Dobles)", "🏃 Individual"])
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

# --- PANTALLA: DEPORTIVIDAD (PRE-MARCADOS EXCLUSIVAMENTE VERTICALES) ---
elif st.session_state.menu_actual == "🙌 Depor":
    st.subheader("🙌 Control de Deportividad")
    is_cancelled_dep = str(fecha_hoy) in st.session_state.dates_no_deporte
    if is_cancelled_dep:
        st.warning("Deporte suspendido hoy. Se elimina la asignación por defecto.")
    else:
        opciones_dep = {"✅ Excelente (5 Pts)": 5, "⚠️ Quejas/Faltas (2 Pts)": 2, "❌ Falta Grave (0 Pts)": 0}
        for al in sorted(alumnos_activos):
            st.markdown(f"**🙌 {al}**")
            pts_act = get_puntos_hoy(al, "Deportividad", 5) # 5 por defecto
            idx_def = list(opciones_dep.values()).index(pts_act)
            
            sel = st.radio(f"Dep_{al}", options=list(opciones_dep.keys()), index=idx_def, key=f"rad_dep_{al}", horizontal=False)
            if opciones_dep[sel] != pts_act:
                set_puntos_hoy(al, "Deportividad", opciones_dep[sel], "Nota deportividad")
                st.toast(f"🙌 {al} Guardado", icon="🙌")
            st.markdown("<div style='border-bottom:1px dashed #cbd5e1; margin-bottom:5px; margin-top:5px;'></div>", unsafe_allow_html=True)

# --- PANTALLA: TALLER (PRE-MARCADOS EXCLUSIVAMENTE VERTICALES) ---
elif st.session_state.menu_actual == "🎨 Tal":
    st.subheader("🎨 Trabajo en los Talleres")
    is_cancelled_tal = str(fecha_hoy) in st.session_state.dates_no_taller
    t_toggle_tal = "🟢 TALLER ACTIVO (Pulsar para suspender)" if not is_cancelled_tal else "🚫 HOY NO HAY TALLER (Puntos anulados)"
    if st.button(t_toggle_tal, key="toggle_tal_day"):
        if is_cancelled_tal: st.session_state.dates_no_taller.remove(str(fecha_hoy))
        else: st.session_state.dates_no_taller.add(str(fecha_hoy))
        guardar_datos_locales(); st.rerun()
        
    if is_cancelled_tal:
        st.warning("Talleres suspendidos hoy. No se inyectan puntos base.")
    else:
        opciones_tal = {"✅ Trabajador (5 Pts)": 5, "⚠️ Distraído (2 Pts)": 2, "❌ Indisciplina (0 Pts)": 0}
        for al in sorted(alumnos_activos):
            st.markdown(f"**🎨 {al}**")
            pts_act = get_puntos_hoy(al, "Taller", 5) # 5 por defecto
            idx_def = list(opciones_tal.values()).index(pts_act)
            
            sel = st.radio(f"Tal_{al}", options=list(opciones_tal.keys()), index=idx_def, key=f"rad_tal_{al}", horizontal=False)
            if opciones_tal[sel] != pts_act:
                set_puntos_hoy(al, "Taller", opciones_tal[sel], "Nota taller")
                st.toast(f"🎨 {al} Guardado", icon="🎨")
            st.markdown("<div style='border-bottom:1px dashed #cbd5e1; margin-bottom:5px; margin-top:5px;'></div>", unsafe_allow_html=True)

# --- PANTALLA: ENCARGOS CON ICONOS VISUALES ASIGNADOS ---
elif st.session_state.menu_actual == "🧹 Enc":
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
                    pts_a = get_puntos_hoy(nino, f"Encargo_{enc}", None)
                    idx_e = list(op_e.values()).index(pts_a) if pts_a in op_e.values() else 0
                    sel_e = st.radio(f"Nota para {nino} ({enc}):", list(op_e.keys()), index=idx_e, key=f"rd_{enc}_{nino}")
                    if op_e[sel_e] != pts_a: set_puntos_hoy(nino, f"Encargo_{enc}", op_e[sel_e], f"Cumplió {enc}")

# --- PANTALLA: LIMPIEZA COMEDOR ---
elif st.session_state.menu_actual == "🍽️ Com":
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

# --- PANTALLA: EXTRAS RE-ALINEADOS SIN DESBORDE ---
elif st.session_state.menu_actual == "💪 Ext":
    st.subheader("💪 Marcador de Encargos Extra")
    motivo_live = st.text_input("Trabajo Extra Actual:", "Ayudar a ordenar materiales")
    
    # MEJORA: Modificamos el layout para que el botón no se salga del margen lateral del teléfono
    for al in sorted(alumnos_activos):
        st.markdown(f"🏃 **{al}**")
        if st.button(f"➕ Asignar +1 Punto Extra", key=f"b_ex_v_{al}"):
            set_puntos_hoy(al, "Extra", 1, motivo_live)
            st.toast(f"💪 +1 Pt Extra a {al}", icon="💪")
            st.rerun()
            
    st.markdown("---")
    st.subheader("🔍 Historial de Extras Añadidos Hoy")
    if not st.session_state.historico_puntos.empty:
        df_ex_hoy = st.session_state.historico_puntos[(st.session_state.historico_puntos['Fecha'].astype(str) == str(fecha_hoy)) & (st.session_state.historico_puntos['Actividad'] == "Extra")]
        st.dataframe(df_ex_hoy[['Alumno', 'Puntos', 'Detalle']], width='stretch')

# --- PANTALLA: JUEGOS ---
elif st.session_state.menu_actual == "🧠 Jue":
    st.subheader("🧠 Puntuación de Juegos del Día")