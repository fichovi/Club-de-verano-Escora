import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, datetime
import json
import os

# --- 1. CONFIGURACIÓN DE PÁGINA (MARCA BLANCA MOBILE-FIRST) ---
st.set_page_config(
    page_title="Club Escora Panel", 
    page_icon="🏆", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- 2. INYECCIÓN DE CSS MAESTRO (DISEÑO ULTRA-COMPACTO ADAPTADO A MÓVILES) ---
st.markdown("""
    <style>
        /* Ocultar menús nativos y logos de Streamlit / GitHub */
        header {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        div[data-testid="stDecoration"] {display: none !important;}
        div[data-testid="stSidebar"] {display: none !important;}
        
        /* Reducir drásticamente tamaños de letra de títulos para pantallas móviles */
        h1 { font-size: 1.1rem !important; margin-bottom: 2px !important; padding-top: 0px !important; font-weight: bold; }
        h2 { font-size: 0.95rem !important; margin-bottom: 2px !important; font-weight: bold; }
        h3 { font-size: 0.85rem !important; margin-bottom: 2px !important; font-weight: bold; }
        p, span, label, .stMarkdown { font-size: 0.78rem !important; }
        
        /* Eliminar márgenes y paddings excesivos para pegar el contenido */
        .block-container { padding-top: 0.4rem !important; padding-bottom: 0.4rem !important; padding-left: 0.5rem !important; padding-right: 0.5rem !important; }
        .element-container { margin-bottom: 0.15rem !important; }
        div[data-testid="stVerticalBlock"] { gap: 0.15rem !important; }
        
        /* Barra de navegación superior (Elementos súper pegados y deslizables) */
        div[data-testid="element-container"]:has(#nav-marker) + div[data-testid="element-container"] div[role="radiogroup"] {
            overflow-x: auto !important;
            flex-wrap: nowrap !important;
            white-space: nowrap !important;
            display: flex !important;
            gap: 1px !important; 
            padding: 3px 0px !important;
        }
        
        div[data-testid="element-container"]:has(#nav-marker) + div[data-testid="element-container"] div[role="radiogroup"] label {
            background-color: #e2e8f0 !important;
            border-radius: 6px !important;
            padding: 4px 8px !important;
            border: 1px solid #cbd5e1 !important;
            margin: 0px !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
        }
        
        div[data-testid="element-container"]:has(#nav-marker) + div[data-testid="element-container"] div[role="radiogroup"] label p {
            color: #1e293b !important;
            font-weight: bold !important;
            font-size: 11px !important;
            margin: 0px !important;
            padding: 0px !important;
        }
        
        div[data-testid="element-container"]:has(#nav-marker) + div[data-testid="element-container"] div[role="radiogroup"] label[data-checked="true"] {
            background-color: #1e3a8a !important;
            border-color: #1e3a8a !important;
        }
        
        div[data-testid="element-container"]:has(#nav-marker) + div[data-testid="element-container"] div[role="radiogroup"] label[data-checked="true"] p {
            color: white !important;
        }
        
        div[data-testid="element-container"]:has(#nav-marker) + div[data-testid="element-container"] div[role="radiogroup"] label > div:first-child {
            width: 0px !important;
            height: 0px !important;
            overflow: hidden !important;
            visibility: hidden !important;
            margin: 0px !important;
            padding: 0px !important;
        }
        
        div[data-testid="stCheckbox"] { padding: 1px 0px !important; margin: 0px !important; }
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
    with open("local_perfiles.json", "w", encoding="utf-8") as f:
        json.dump(st.session_state.perfiles_alumnos, f, ensure_ascii=False)
    with open("local_cancelaciones.json", "w", encoding="utf-8") as f:
        json.dump({"no_deporte": list(st.session_state.dates_no_deporte), "no_taller": list(st.session_state.dates_no_taller)}, f)

def cargar_datos_locales():
    if os.path.exists("local_alumnos_master.json"):
        with open("local_alumnos_master.json", "r", encoding="utf-8") as f: st.session_state.alumnos_master = json.load(f)
    else: st.session_state.alumnos_master = LISTA_ALUM_INICIAL.copy()
    if os.path.exists("local_historico_puntos.csv"):
        st.session_state.historico_puntos = pd.read_csv("local_historico_puntos.csv")
    else:
        st.session_state.historico_puntos = pd.DataFrame(columns=['Fecha', 'Hora', 'Alumno', 'Actividad', 'Puntos', 'Detalle', 'Semana'])
    if os.path.exists("local_oraciones.json"):
        with open("local_oraciones.json", "r", encoding="utf-8") as f: st.session_state.oraciones_aprendidas = json.load(f)
    else: st.session_state.oraciones_aprendidas = {al: [] for al in st.session_state.alumnos_master}
    if os.path.exists("local_comedor.json"):
        with open("local_comedor.json", "r", encoding="utf-8") as f: st.session_state.contador_comedor = json.load(f)
    else: st.session_state.contador_comedor = {al: 0 for al in st.session_state.alumnos_master}
    if os.path.exists("local_encargos.json"):
        with open("local_encargos.json", "r", encoding="utf-8") as f: st.session_state.encargos_semanales = json.load(f)
    else:
        st.session_state.encargos_semanales = {f"Semana {i}": {} for i in range(1, 5)}
    if os.path.exists("local_asistencia.json"):
        with open("local_asistencia.json", "r", encoding="utf-8") as f: st.session_state.asistencia = json.load(f)
    else:
        st.session_state.asistencia = {f"Semana {i}": {al: True for al in st.session_state.alumnos_master} for i in range(1, 5)}
    if os.path.exists("local_turno.json"):
        with open("local_turno.json", "r", encoding="utf-8") as f: st.session_state.estar_de_turno = json.load(f)
    else:
        st.session_state.estar_de_turno = {f"Semana {i}": {"Lunes": "", "Martes": "", "Miércoles": "", "Jueves": "", "Viernes": ""} for i in range(1, 5)}
    if os.path.exists("local_perfiles.json"):
        with open("local_perfiles.json", "r", encoding="utf-8") as f: st.session_state.perfiles_alumnos = json.load(f)
    else: st.session_state.perfiles_alumnos = {}
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

if 'menu_actual' not in st.session_state: st.session_state.menu_actual = "🏠 Inicio"

LISTA_ORACIONES = ["Señal Sta Cruz", "Padrenuestro", "Ave María", "Gloria", "5 pasos confesion", "Visita", "Angelus", "Oh Sra mía", "Angel Guarda", "10 mandamientos", "Empezar oracion", "Acabar oracion", "Bendicion mesa", "Acc gracias dp comer", "5 mand Sta Mad Igl", "Salve", "Bend sea pureza", "Señor mio Xto", "Acordaos", "Sacramentos"]
LISTA_ENCARGOS_OFICIALES = ["ORDEN SALA DE ESTUDIO 📚", "ORDEN COMEDOR 🍽️", "ORDEN TALLERES 🎨", "ORDEN ZONA ALMUERZO 🥪", "ORDEN VESTUARIOS 👕", "ORDEN PISCINA 🏊", "MATERIAL DE DEPORTE ⚽", "MATERIAL DE PISCINA 🛟", "NEVERA ❄️", "VASOS 🥛", "CUBIERTOS 🍴", "TUPPERS 🍱", "AGUA COMIDA 💧", "PLAN TARDE 🌅", "ORATORIO ⛪"]

# --- 4. CONFIGURACIÓN COMPACTA DE CABECERA ---
c_conf1, c_conf2 = st.columns(2)
semana_act = c_conf1.selectbox("Bloque:", ["Semana 1", "Semana 2", "Semana 3", "Semana 4"], label_visibility="collapsed")
fecha_hoy = c_conf2.date_input("Fecha:", date.today(), label_visibility="collapsed")

alumnos_activos = [al for al in st.session_state.alumnos_master if st.session_state.asistencia.get(semana_act, {}).get(al, True)]

# --- 5. MENÚ DE NAVEGACIÓN SUPERIOR BLINDADO ---
st.markdown('<div id="nav-marker"></div>', unsafe_allow_html=True)
items_menu = ["🏠 Inicio", "👥 Asist", "📊 Rank", "📚 Est", "🙏 Orac", "⚽ Dep", "🙌 Depor", "🎨 Tal", "🧹 Enc", "🍽️ Com", "💪 Ext", "🎥 Vid", "⚠️ Mult", "🛠️ Admin"]

pestaña_recuperada = st.session_state.get('menu_actual', "🏠 Inicio")
idx_actual = items_menu.index(pestaña_recuperada) if pestaña_recuperada in items_menu else 0

menu_seleccionado = st.radio("Navegacion", options=items_menu, index=idx_actual, horizontal=True, label_visibility="collapsed")
if menu_seleccionado != st.session_state.menu_actual:
    st.session_state.menu_actual = menu_seleccionado
    st.rerun()
st.write("---")

def get_puntos_hoy(alumno, actividad, default_val=None):
    df = st.session_state.historico_puntos
    if df.empty: return default_val
    cond = (df['Fecha'].astype(str) == str(fecha_hoy)) & (df['Alumno'] == alumno) & (df['Actividad'] == actividad)
    if cond.any(): return df.loc[cond, 'Puntos'].values[0]
    return default_val

def registrar_puntos(alumno, actividad, puntos, detalle=""):
    df = st.session_state.historico_puntos
    hora_actual = datetime.now().strftime("%H:%M:%S")
    actividades_fijas = (actividad in ["Estudio", "Deportividad", "Taller"]) or actividad.startswith("Encargo_")
    
    if actividades_fijas:
        cond = (df['Fecha'].astype(str) == str(fecha_hoy)) & (df['Alumno'] == alumno) & (df['Actividad'] == actividad)
        if cond.any():
            st.session_state.historico_puntos.loc[cond, 'Puntos'] = puntos
            st.session_state.historico_puntos.loc[cond, 'Hora'] = hora_actual
            st.session_state.historico_puntos.loc[cond, 'Detalle'] = detalle
            guardar_datos_locales()
            return
            
    nueva_fila = pd.DataFrame([{'Fecha': str(fecha_hoy), 'Hora': hora_actual, 'Alumno': alumno, 'Actividad': actividad, 'Puntos': puntos, 'Detalle': detalle, 'Semana': semana_act}])
    st.session_state.historico_puntos = pd.concat([st.session_state.historico_puntos, nueva_fila], ignore_index=True)
    guardar_datos_locales()

# --- PANTALLA: INICIO & HORARIO CARGADO ---
if st.session_state.menu_actual == "🏠 Inicio":
    st.subheader("🏠 Panel de Inicio")
    st.markdown(f"👦 **Alumnos Asistentes:** `{len(alumnos_activos)} de {len(st.session_state.alumnos_master)}`")
    
    ruta_horario_imagen = f"horario_{semana_act}.png"
    if os.path.exists(ruta_horario_imagen):
        st.image(ruta_horario_imagen, caption=f"Horario Oficial Subido para la {semana_act}", use_container_width=True)
    else:
        st.info("💡 No hay ninguna imagen de horario cargada para esta semana. Mostrando horario de texto predeterminado:")
        hora_ahora = datetime.now().time()
        nombre_dia_eng = fecha_hoy.strftime("%A")
        horarios_oficiales = {
            "Monday": [{"inicio": "09:00", "fin": "10:00", "tarea": "🎒 Tareas de Verano"}, {"inicio": "10:00", "fin": "11:00", "tarea": "🥪 Almuerzo + Avisos"}, {"inicio": "11:00", "fin": "12:00", "tarea": "👑 Rey de la Pista F-Sala"}, {"inicio": "12:00", "fin": "13:00", "tarea": "🏊 Piscina Libre"}, {"inicio": "13:00", "fin": "14:00", "tarea": "🪙 Fútbol Chapas"}, {"inicio": "14:00", "fin": "15:00", "tarea": "🍽️ Comida"}, {"inicio": "15:00", "fin": "17:00", "tarea": " Torneos"}],
            "Tuesday": [{"inicio": "09:00", "fin": "10:00", "tarea": "🎒 Tareas de Verano"}, {"inicio": "10:00", "fin": "11:00", "tarea": "🗣️ Plática + Almuerzo"}, {"inicio": "11:00", "fin": "12:30", "tarea": "⚾ Béisbol"}, {"inicio": "12:30", "fin": "13:00", "tarea": "🏊 Piscina"}, {"inicio": "13:00", "fin": "14:00", "tarea": "🎨 Termorretractil / Cerámica"}, {"inicio": "14:00", "fin": "15:00", "tarea": "🍽️ Comida"}, {"inicio": "15:00", "fin": "17:00", "tarea": "🧠 Superquiz + Torneos"}],
            "Wednesday": [{"inicio": "09:00", "fin": "10:00", "tarea": "🎒 Tareas de Verano"}, {"inicio": "10:00", "fin": "11:00", "tarea": "💬 Almuerzo + Charla"}, {"inicio": "11:00", "fin": "12:30", "tarea": " Torneo de Tenis y Pádel"}, {"inicio": "12:30", "fin": "14:00", "tarea": "🏊 Piscina"}, {"inicio": "14:00", "fin": "15:00", "tarea": "🍽️ Comida"}, {"inicio": "15:00", "fin": "17:00", "tarea": "⚽ Pachanga + Piscina"}],
            "Thursday": [{"inicio": "09:00", "fin": "10:00", "tarea": "🎒 Tareas de Verano"}, {"inicio": "10:00", "fin": "17:00", "tarea": "🚌 EXCURSIÓN A XÀTIVA (Piscina + Barbacoa)"}],
            "Friday": [{"inicio": "09:00", "fin": "10:00", "tarea": "🎒 Tareas de Verano"}, {"inicio": "10:00", "fin": "11:00", "tarea": "🎥 Vídeo + Almuerzo"}, {"inicio": "11:00", "fin": "13:00", "tarea": "💦 Gymkhana Acuática"}, {"inicio": "13:00", "fin": "14:00", "tarea": "🎨 Termorretractil / Cerámica"}, {"inicio": "14:00", "fin": "15:00", "tarea": "🍽️ Comida"}, {"inicio": "15:00", "fin": "17:00", "tarea": "🍿 Peliculón"}]
        }
        cronograma_hoy = horarios_oficiales.get(nombre_dia_eng, [{"inicio": "09:00", "fin": "17:00", "tarea": "✨ Fin de semana / Libre"}])
        for c in cronograma_hoy:
            t_ini = datetime.strptime(c["inicio"], "%H:%M").time()
            t_fin = datetime.strptime(c["fin"], "%H:%M").time()
            if (str(fecha_hoy) == str(date.today())) and (t_ini <= hora_ahora <= t_fin):
                st.markdown(f'<div style="background-color: #d1fae5; border-left: 4px solid #10b981; padding: 5px; border-radius: 4px; margin-bottom: 2px; font-size:12px;"><strong>⚡ AHORA ({c["inicio"]} - {c["fin"]}):</strong> {c["tarea"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="background-color: #f3f4f6; border-left: 4px solid #9ca3af; padding: 4px; border-radius: 4px; margin-bottom: 2px; color:#6b7280; font-size:11px;">⏳ {c["inicio"]} - {c["fin"]}: {c["tarea"]}</div>', unsafe_allow_html=True)

# --- PANTALLA: GESTIÓN DE ASISTENCIA Y CONTACTOS ---
elif st.session_state.menu_actual == "👥 Asist":
    st.subheader("👥 Control de Asistencia y Fichas")
    tab_asist, tab_fichas = st.tabs(["📌 Asistencia de la Semana", "📇 Fichas de Contacto Completo"])
    
    with tab_asist:
        st.markdown(f"👦 **Total Asistentes:** `{len(alumnos_activos)} de {len(st.session_state.alumnos_master)}`")
        if semana_act not in st.session_state.asistencia: st.session_state.asistencia[semana_act] = {}
        for al in sorted(st.session_state.alumnos_master):
            if al not in st.session_state.asistencia[semana_act]: st.session_state.asistencia[semana_act][al] = True
            val_ch = st.checkbox(al, value=st.session_state.asistencia[semana_act][al], key=f"asist_tab_{al}")
            if val_ch != st.session_state.asistencia[semana_act][al]:
                st.session_state.asistencia[semana_act][al] = val_ch
                guardar_datos_locales(); st.rerun()
                
    with tab_fichas:
        st.markdown("### 📇 Consulta de Datos Familiares")
        if st.session_state.perfiles_alumnos:
            al_f = st.selectbox("Seleccionar Alumno para ver detalles:", sorted(st.session_state.alumnos_master), key="sb_fichas_view")
            perfil = st.session_state.perfiles_alumnos.get(al_f, {})
            if perfil:
                st.markdown(f"**📞 Teléfono Padre:** {perfil.get('Tel_Padre', 'No registrado')}")
                st.markdown(f"**📞 Teléfono Madre:** {perfil.get('Tel_Madre', 'No registrado')}")
                st.markdown(f"**👨 Nombre del Padre:** {perfil.get('Nombre_Padre', 'No registrado')}")
                st.markdown(f"**👩 Nombre de la Madre:** {perfil.get('Nombre_Madre', 'No registrado')}")
                st.markdown(f"**🏫 Colegio de Procedencia:** {perfil.get('Colegio', 'No registrado')}")
                st.markdown(f"**👕 Talla Camiseta:** {perfil.get('Camiseta', 'No registrado')}")
                st.markdown(f"**🎂 Nacimiento:** {perfil.get('Nacimiento', 'No registrado')}")
            else:
                st.info("Este alumno no tiene ficha detallada.")
        else:
            st.info("Aún no hay fichas registradas. Sube una hoja Excel en la pestaña Admin para sincronizarlas.")

# --- PANTALLA: CLASIFICACIONES ---
elif st.session_state.menu_actual == "📊 Rank":
    st.subheader("📊 Resultados de Clasificación")
    tab_s, tab_g, tab_d = st.tabs(["📆 Semanal", "🏆 General", "📅 Puntos de Hoy"])
    df_hist = st.session_state.historico_puntos.copy()
    
    def generar_tabla_desglosada(filtrar_semana=None, filtrar_fecha=None):
        df_base = df_hist.copy()
        if filtrar_semana: df_base = df_base[df_base['Semana'] == filtrar_semana]
        if filtrar_fecha: df_base = df_base[df_base['Fecha'].astype(str) == str(filtrar_fecha)]
        
        registros_puntos = []
        if not df_base.empty:
            for _, fila in df_base.iterrows():
                registros_puntos.append({'Alumno': fila['Alumno'], 'Actividad': fila['Actividad'], 'Puntos': float(fila['Puntos'])})
                
        if not filtrar_fecha:
            fechas_evaluadas = df_hist['Fecha'].unique() if not df_hist.empty else [str(fecha_hoy)]
            lista_ninos = alumnos_activos if filtrar_semana else st.session_state.alumnos_master
            for al in lista_ninos:
                for f in fechas_evaluadas:
                    sem_f = df_hist[df_hist['Fecha'] == f]['Semana'].values[0] if not df_hist.empty and f in df_hist['Fecha'].values else  semana_act
                    if not st.session_state.asistencia.get(sem_f, {}).get(al, True): continue
                    if filtrar_semana and sem_f != filtrar_semana: continue
                    
                    if f not in st.session_state.dates_no_deporte and df_hist[(df_hist['Fecha'] == f) & (df_hist['Alumno'] == al) & (df_hist['Actividad'] == "Deportividad")].empty:
                        registros_puntos.append({'Alumno': al, 'Actividad': 'Deportividad (Auto)', 'Puntos': 5.0})
                    if f not in st.session_state.dates_no_taller and df_hist[(df_hist['Fecha'] == f) & (df_hist['Alumno'] == al) & (df_hist['Actividad'] == "Taller")].empty:
                        registros_puntos.append({'Alumno': al, 'Actividad': 'Taller (Auto)', 'Puntos': 5.0})
        if not registros_puntos: return pd.DataFrame(columns=['Alumno', 'Actividad', 'Puntos'])
        return pd.DataFrame(registros_puntos)

    with tab_s:
        df_s = generar_tabla_desglosada(filtrar_semana=semana_act)
        if not df_s.empty:
            fig_s = px.bar(df_s, x='Puntos', y='Alumno', color='Actividad', orientation='h', title=f"Estadísticas: {semana_act}")
            fig_s.update_layout(height=500, barmode='stack', xaxis=dict(fixedrange=True), yaxis=dict(fixedrange=True, categoryorder='total ascending'), margin=dict(l=0,r=0,t=25,b=0))
            st.plotly_chart(fig_s, width='stretch', config={'displayModeBar': False})
            csv_data_s = df_s.groupby(['Alumno', 'Actividad'])['Puntos'].sum().reset_index().to_csv(index=False).encode('utf-8')
            st.download_button("📥 Descargar CSV Semanal", data=csv_data_s, file_name=f"Desglose_Semanal_{semana_act}.csv", mime='text/csv')
            
    with tab_g:
        df_g = generar_tabla_desglosada(None)
        if not df_g.empty:
            fig_g = px.bar(df_g, x='Puntos', y='Alumno', color='Actividad', orientation='h', title="Estadísticas Acumuladas")
            fig_g.update_layout(height=600, barmode='stack', xaxis=dict(fixedrange=True), yaxis=dict(fixedrange=True, categoryorder='total ascending'), margin=dict(l=0,r=0,t=25,b=0))
            st.plotly_chart(fig_g, width='stretch', config={'displayModeBar': False})
            csv_data_g = df_g.groupby(['Alumno', 'Actividad'])['Puntos'].sum().reset_index().to_csv(index=False).encode('utf-8')
            st.download_button("📥 Descargar CSV General", data=csv_data_g, file_name="Desglose_General_Campus.csv", mime='text/csv')
            
    with tab_d:
        df_d = generar_tabla_desglosada(None, filtrar_fecha=fecha_hoy)
        if not df_d.empty:
            df_d_sum = df_d.groupby('Alumno')['Puntos'].sum().reset_index().sort_values(by="Puntos", ascending=True)
            fig_d = px.bar(df_d_sum, x='Puntos', y='Alumno', orientation='h', title=f"Puntos Ganados Hoy ({fecha_hoy})", text_auto=True)
            fig_d.update_layout(height=500, xaxis=dict(fixedrange=True), yaxis=dict(fixedrange=True))
            st.plotly_chart(fig_d, width='stretch', config={'displayModeBar': False})
            csv_data_d = df_d.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Descargar CSV de Puntos de Hoy", data=csv_data_d, file_name=f"Puntos_Hoy_{fecha_hoy}.csv", mime='text/csv')
        else:
            st.info("No hay registros de puntos anotados en la fecha de hoy.")
            
    st.markdown("---")
    st.dataframe(st.session_state.historico_puntos.iloc[::-1], width='stretch')

# --- PANTALLA: ESTUDIO ---
elif st.session_state.menu_actual == "📚 Est":
    st.subheader("📚 Puntuación: Hora de Estudio")
    opciones_estudio = {"No evaluado": None, "❌ 0 Puntos": 0, "⚠️ 2 Puntos": 2, "✅ 5 Puntos": 5}
    for al in sorted(alumnos_activos):
        pts_actuales = get_puntos_hoy(al, "Estudio", None)
        index_def = list(opciones_estudio.values()).index(pts_actuales)
        
        st.markdown(f"**🧑 {al}**")
        seleccion = st.radio(f"Est_{al}", options=list(opciones_estudio.keys()), index=index_def, key=f"rad_est_{al}", horizontal=False, label_visibility="collapsed")
        pts_seleccionados = opciones_estudio[seleccion]
        if pts_seleccionados is not None and pts_seleccionados != pts_actuales:
            registrar_puntos(al, "Estudio", pts_seleccionados, "Nota estudio")
            st.toast(f"✅ {al} Guardado"); st.rerun()
        st.markdown("<div style='border-bottom:1px dashed #cbd5e1; margin:4px 0px;'></div>", unsafe_allow_html=True)

# --- PANTALLA: ORACIONES ---
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
        st.markdown(f'<div style="background-color:{b["color"]}; padding:5px; border-radius:4px; font-weight:bold; margin-top:14px; margin-bottom:8px; font-size:11px; color:#1e293b; clear:both;">{b["nombre"]}</div>', unsafe_allow_html=True)
        for item in b["items"]:
            if st.checkbox(item, value=(item in oraciones_actuales), key=f"or_mob_{al_sel}_{item}"): nuevas_oraciones.append(item)
            
    if nuevas_oraciones != oraciones_actuales:
        st.session_state.oraciones_aprendidas[al_sel] = nuevas_oraciones
        st.session_state.historico_puntos = st.session_state.historico_puntos[~((st.session_state.historico_puntos['Alumno'] == al_sel) & (st.session_state.historico_puntos['Actividad'] == "Oración"))]
        for o in nuevas_oraciones: registrar_puntos(al_sel, "Oración", 5, f"Sabe: {o}")
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
                    if st.session_state[f"c_dep_{eq}"]: registrar_puntos(st.session_state[f"c_dep_{eq}"], "Deporte", pts, f"Capitán {eq}")
                    for j in st.session_state[f"m_dep_{eq}"]: registrar_puntos(j, "Deporte", pts, f"Miembro {eq}")
                st.success("Torneo guardado.")
        elif "Parejas" in modalidad:
            p1 = st.multiselect("Pareja A:", alumnos_activos, max_selections=2, key="par_a")
            p2 = st.multiselect("Pareja B:", [al for al in alumnos_activos if al not in p1], max_selections=2, key="par_b")
            pts_pa = st.selectbox("Puntos Pareja A:", [5, 3, 2, 0], key="pts_pa")
            pts_pb = st.selectbox("Puntos Pareja B:", [5, 3, 2, 0], key="pts_pb")
            if st.button("💾 Registrar Puntos de Parejas"):
                for al in p1: registrar_puntos(al, "Deporte", pts_pa, "Torneo Parejas A")
                for al in p2: registrar_puntos(al, "Deporte", pts_pb, "Torneo Parejas B")
                st.success("Puntos guardados.")
        elif "Individual" in modalidad:
            al_ganador = st.selectbox("1º Clasificado (+5 Pts):", alumnos_activos, key="ind_1")
            al_2do = st.selectbox("2º Clasificado (+3 Pts):", [al for al in alumnos_activos if al != al_ganador], key="ind_2")
            al_3ro = st.selectbox("3º Clasificado (+2 Pts):", [al for al in alumnos_activos if al not in [al_ganador, al_2do]], key="ind_3")
            if st.button("💾 Registrar Deporte Individual"):
                registrar_puntos(al_ganador, "Deporte", 5, "1º Lugar Individual")
                registrar_puntos(al_2do, "Deporte", 3, "2º Lugar Individual")
                registrar_puntos(al_3ro, "Deporte", 2, "3º Lugar Individual")
                st.success("Puntos individuales guardados.")

# --- PANTALLA: DEPORTIVIDAD ---
elif st.session_state.menu_actual == "🙌 Depor":
    st.subheader("🙌 Control de Deportividad")
    is_cancelled_dep = str(fecha_hoy) in st.session_state.dates_no_deporte
    if is_cancelled_dep:
        st.warning("Deporte suspendido hoy. Se elimina la asignación por defecto.")
    else:
        opciones_dep = {"✅ Excelente (5 Pts)": 5, "⚠️ Quejas/Faltas (2 Pts)": 2, "❌ Falta Grave (0 Pts)": 0}
        for al in sorted(alumnos_activos):
            st.markdown(f"**🙌 {al}**")
            pts_act = get_puntos_hoy(al, "Deportividad", 5)
            idx_def = list(opciones_dep.values()).index(pts_act)
            
            sel = st.radio(f"Dep_{al}", options=list(opciones_dep.keys()), index=idx_def, key=f"rad_dep_{al}", horizontal=False, label_visibility="collapsed")
            if opciones_dep[sel] != pts_act:
                registrar_puntos(al, "Deportividad", opciones_dep[sel], "Nota deportividad")
                st.toast(f"🙌 {al} Guardado")
            st.markdown("<div style='border-bottom:1px dashed #cbd5e1; margin-bottom:5px; margin-top:5px;'></div>", unsafe_allow_html=True)

# --- PANTALLA: TALLER ---
elif st.session_state.menu_actual == "🎨 Tal":
    st.subheader("🎨 Trabajo en los Talleres")
    is_cancelled_tal = str(fecha_hoy) in st.session_state.dates_no_taller
    t_toggle_tal = "🟢 TALLER ACTIVO (Pulsar para suspender)" if not is_cancelled_tal else "🚫 HOY NO HAY TALLER (Puntos anulados)"
    if st.button(t_toggle_tal, key="toggle_tal_day"):
        if is_cancelled_tal: st.session_state.dates_no_taller.remove(str(fecha_hoy))
        else: st.session_state.dates_no_taller.add(str(fecha_hoy))
        guardar_datos_locales(); st.rerun()
        
    if is_cancelled_tal:
        st.warning("Talleres suspendidos hoy. No se aplican los 5 puntos automáticos.")
    else:
        opciones_tal = {"✅ Trabajador (5 Pts)": 5, "⚠️ Distraído (2 Pts)": 2, "❌ Indisciplina (0 Pts)": 0}
        for al in sorted(alumnos_activos):
            st.markdown(f"**🎨 {al}**")
            pts_act = get_puntos_hoy(al, "Taller", 5)
            idx_def = list(opciones_tal.values()).index(pts_act)
            
            sel = st.radio(f"Tal_{al}", options=list(opciones_tal.keys()), index=idx_def, key=f"rad_tal_{al}", horizontal=False, label_visibility="collapsed")
            if opciones_tal[sel] != pts_act:
                registrar_puntos(al, "Taller", opciones_tal[sel], "Nota taller")
                st.toast(f"🎨 {al} Guardado")
            st.markdown("<div style='border-bottom:1px dashed #cbd5e1; margin-bottom:5px; margin-top:5px;'></div>", unsafe_allow_html=True)

# --- PANTALLA: ENCARGOS ---
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
            st.session_state.encargos_semanales[semana_act][enc] = st.multiselect(f"{enc}:", options=dispo, default=def_e, max_selections=2, key=f"box_enc_{enc}")
        st.markdown("---")
        op_e = {"5 Pts (Bien)": 5, "2 Pts (Regular)": 2, "0 Pts (Mal)": 0}
        for enc, encargados in st.session_state.encargos_semanales[semana_act].items():
            if encargados:
                st.markdown(f"**{enc}**")
                for nino in encargados:
                    pts_a = get_puntos_hoy(nino, f"Encargo_{enc}", None)
                    idx_e = list(op_e.values()).index(pts_a) if pts_a in op_e.values() else 0
                    sel_e = st.radio(f"Nota para {nino}:", list(op_e.keys()), index=idx_e, key=f"rd_{enc}_{nino}")
                    if op_e[sel_e] != pts_a: registrar_puntos(nino, f"Encargo_{enc}", op_e[sel_e], f"Hizo {enc}")

    with tab_t:
        st.subheader("🙏 Fila para Rezar las Oraciones")
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
        for d in dias:
            if semana_act not in st.session_state.estar_de_turno: st.session_state.estar_de_turno[semana_act] = {}
            def_t = st.session_state.estar_de_turno[semana_act].get(d, "")
            
            opciones_turno = ["--- Sin asignar ---"] + alumnos_activos
            idx_t = opciones_turno.index(def_t) if def_t in opciones_turno else 0
            
            sel_t = st.selectbox(f"Encargado del {d}:", options=opciones_turno, index=idx_t, key=f"t_or_{d}")
            if sel_t != def_t:
                st.session_state.estar_de_turno[semana_act][d] = sel_t if sel_t != "--- Sin asignar ---" else ""
                guardar_datos_locales()

# --- PANTALLA: LIMPIEZA COMEDOR ---
elif st.session_state.menu_actual == "🍽️ Com":
    st.subheader("🍽️ Tareas de Limpieza (10 Puntos)")
    if st.button("🤖 Calcular Sugerencia Justa del Día"):
        al_ordenados = sorted(alumnos_activos, key=lambda x: st.session_state.contador_comedor.get(x, 0))
        st.session_state.limpieza_propuesta = {"Fregar Vasos y Cubiertos (2)": [al_ordenados[0], al_ordenados[1]], "Barrer Comedor (2)": [al_ordenados[2], al_ordenados[3]], "Pasar Bayetas por Mesas (2)": [al_ordenados[4], al_ordenados[5]], "Basura Envases (1)": [al_ordenados[6]], "Basura Orgánico (1)": [al_ordenados[7]], "Basura Papel y Cartón (1)": [al_ordenados[8]]}
    
    if "limpieza_propuesta" in st.session_state:
        roles_f = {}
        lista_roles = list(st.session_state.limpieza_propuesta.keys())
        
        for rol in lista_roles:
            sugeridos = st.session_state.limpieza_propuesta[rol]
            max_s = 2 if "(2)" in rol else 1
            
            ocupados_otros_roles = []
            for otro_rol in lista_roles:
                if otro_rol != rol:
                    key_widget = f"l_rol_{otro_rol}"
                    if key_widget in st.session_state:
                        ocupados_otros_roles.extend(st.session_state[key_widget])
            
            dispo_comedor = [al for al in alumnos_activos if al not in ocupados_otros_roles]
            def_comedor = [al for al in sugeridos if al in dispo_comedor]
            
            roles_f[rol] = st.multiselect(f"{rol}:", options=dispo_comedor, default=def_comedor, max_selections=max_s, key=f"l_rol_{rol}")
            
        if st.button("💾 Validar Limpieza y Asignar +10 Puntos"):
            for rol, elegidos in roles_f.items():
                for el in elegidos:
                    registrar_puntos(el, "Limpieza Comedor", 10, f"Rol diario: {rol}")
                    st.session_state.contador_comedor[el] += 1
            st.success("¡Cuadrante guardado con éxito!")

# --- PANTALLA: EXTRAS EN VIVO ACUMULATIVOS ---
elif st.session_state.menu_actual == "💪 Ext":
    st.subheader("💪 Marcador de Encargos Extra")
    motivo_live = st.text_input("Trabajo Extra Actual:", "Ayudar a ordenar materiales")
    
    for al in sorted(alumnos_activos):
        st.markdown(f"🏃 **{al}**")
        if st.button(f"➕ Añadir +1 Punto Extra", key=f"b_ex_v_{al}"):
            registrar_puntos(al, "Extra", 1, motivo_live)
            st.toast(f"💪 +1 Pt Extra cargado a {al}", icon="💪")
            st.rerun()
            
    st.markdown("---")
    st.subheader("🔍 Historial de Extras Añadidos Hoy")
    if not st.session_state.historico_puntos.empty:
        df_ex_hoy = st.session_state.historico_puntos[(st.session_state.historico_puntos['Fecha'].astype(str) == str(fecha_hoy)) & (st.session_state.historico_puntos['Actividad'] == "Extra")]
        st.dataframe(df_ex_hoy[['Alumno', 'Puntos', 'Detalle']], width='stretch')

# --- PANTALLA: JUEGOS ---
elif st.session_state.menu_actual == "🧠 Jue":
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
            if cap_name: registrar_puntos(cap_name, "Juegos", pts_juego, f"Juego: {motivo_juego} ({eq})")
            for m in miembros_eq: registrar_puntos(m, "Juegos", pts_juego, f"Juego: {motivo_juego} ({eq})")
            st.success(f"Puntos asignados a {tag_j}")

# --- PANTALLA: VÍDEO FORMACIÓN ---
elif st.session_state.menu_actual == "🎥 Vid":
    st.subheader("🎥 Preguntas del Vídeo (2 Pts)")
    if 'vid_preg_num' not in st.session_state: st.session_state.vid_preg_num = 1
    
    conteo_v = {al: len(st.session_state.historico_puntos[(st.session_state.historico_puntos['Alumno'] == al) & (st.session_state.historico_puntos['Actividad'] == "Video Formación")]) if not st.session_state.historico_puntos.empty else 0 for al in alumnos_activos}

    if st.button("🔄 Generar / Congelar Fila del Día"):
        st.session_state.fixed_queue = sorted(alumnos_activos, key=lambda x: conteo_v[x])
        st.session_state.vid_pointer = 0
        st.success("¡Fila de sesión fijada correctamente!")

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
        registrar_puntos(titular, "Video Formación", 2, f"Pregunta {st.session_state.vid_preg_num}")
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
                registrar_puntos(reb_alumno, "Video Formación", 2, f"Preg {st.session_state.vid_preg_num} - Reb {idx}")
                st.session_state.vid_pointer = (cola_fija.index(reb_alumno) + 1) % total_cola
                st.session_state.vid_preg_num += 1
                st.rerun()
                
    if st.button("⏭️ Saltar Pregunta"): 
        st.session_state.vid_pointer = (st.session_state.vid_pointer + 1) % total_cola
        st.session_state.vid_preg_num += 1
        st.rerun()
        
    st.markdown("---")
    st.write("**🙋 Respuesta por Mano Levantada:**")
    al_libre = st.selectbox("Asignar +2 puntos directos a:", ["--- Selecciona ---"] + alumnos_activos, key="sb_libre_vid")
    if st.button("💾 Guardar Punto Mano Levantada"):
        if al_libre != "--- Selecciona ---":
            registrar_puntos(al_libre, "Video Formación", 2, "Respuesta libre mano levantada")
            st.toast(f"🎥 +2 Pts a {al_libre}", icon="🎥")
            st.rerun()
            
    st.markdown("---")
    st.subheader("📊 Conteo de Aciertos en Vídeo Formación")
    listado_aciertos_video = []
    for al in sorted(alumnos_activos):
        listado_aciertos_video.append({'Alumno': al, 'Preguntas Acertadas': conteo_v.get(al, 0)})
    df_rank_video = pd.DataFrame(listado_aciertos_video).sort_values(by="Preguntas Acertadas", ascending=False)
    st.dataframe(df_rank_video, use_container_width=True, hide_index=True)

# --- PANTALLA: MULTAS ---
elif st.session_state.menu_actual == "⚠️ Mult":
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
            registrar_puntos(al_p, "Penalizacion", puntos_a_quitar, motivo_p)
            st.toast(f"📉 Penalización aplicada a {al_p}", icon="⚠️")
        st.rerun()
        
    st.markdown("---")
    st.subheader("🔍 Historial de Penalizaciones de Hoy")
    if not st.session_state.historico_puntos.empty:
        df_pen_hoy = st.session_state.historico_puntos[(st.session_state.historico_puntos['Fecha'].astype(str) == str(fecha_hoy)) & (st.session_state.historico_puntos['Actividad'] == "Penalizacion")]
        if not df_pen_hoy.empty: 
            st.dataframe(df_pen_hoy[['Alumno', 'Puntos', 'Detalle']], width='stretch')

# --- PANTALLA: ADMIN (PROTECCIÓN DE ACCIÓN POR BOTÓN DE CONFIRMACIÓN) ---
elif st.session_state.menu_actual == "🛠️ Admin":
    st.subheader("🛠️ Panel de Administración")
    
    st.markdown("### 📥 Inscripción Masiva y Sincronización de Respuestas de Google Forms")
    st.caption("Sube el archivo de respuestas descargado de vuestro formulario (.xlsx / .csv):")
    excel_file = st.file_uploader("Seleccionar Excel de Alumnos:", type=["xlsx", "xls", "csv"], key="excel_masivo_uploader")
    
    if excel_file is not None:
        # CORRECCIÓN: Botón explícito para lanzar la importación masiva solo cuando se pulsa, evitando el bucle infinito
        if st.button("📥 Confirmar e Importar Alumnos del Excel", key="btn_confirmar_excel", type="primary"):
            try:
                if excel_file.name.endswith('.csv'):
                    df_inscritos = pd.read_csv(excel_file)
                else:
                    df_inscritos = pd.read_excel(excel_file)
                    
                df_inscritos = df_inscritos.dropna(subset=[c for c in df_inscritos.columns if "Nombre y apellidos" in c or "Nombre" in c], how='all')
                
                col_nombre = [c for c in df_inscritos.columns if "Nombre y apellidos del niño" in c][0]
                col_tel_padre = [c for c in df_inscritos.columns if "Número de teléfono del Padre" in c or "teléfono del Padre" in c][0]
                col_tel_madre = [c for c in df_inscritos.columns if "Número de teléfono de la madre" in c or "teléfono de la madre" in c][0]
                col_padre_nom = [c for c in df_inscritos.columns if "Nombre del padre" in c][0]
                col_madre_nom = [c for c in df_inscritos.columns if "Nombre de la madre" in c][0]
                col_colegio = [c for c in df_inscritos.columns if "Colegio" in c][0]
                col_camiseta = [c for c in df_inscritos.columns if "Talla de camiseta" in c or "Camiseta" in c][0]
                col_nacimiento = [c for c in df_inscritos.columns if "Fecha de nacimiento" in c or "nacimiento" in c][0]
                
                conteo_nuevos = 0
                for _, fila in df_inscritos.iterrows():
                    nombre_completo = str(fila[col_nombre]).strip()
                    if nombre_completo and nombre_completo != "nan" and not nombre_completo.startswith("TOTAL"):
                        if nombre_completo not in st.session_state.alumnos_master:
                            st.session_state.alumnos_master.append(nombre_completo)
                            conteo_nuevos += 1
                        
                        st.session_state.perfiles_alumnos[nombre_completo] = {
                            "Tel_Padre": str(fila[col_tel_padre]).replace(".0", "").strip(),
                            "Tel_Madre": str(fila[col_tel_madre]).replace(".0", "").strip(),
                            "Nombre_Padre": str(fila[col_padre_nom]).strip(),
                            "Nombre_Madre": str(fila[col_madre_nom]).strip(),
                            "Colegio": str(fila[col_colegio]).strip(),
                            "Camiseta": str(fila[col_camiseta]).strip(),
                            "Nacimiento": str(fila[col_nacimiento]).strip()
                        }
                guardar_datos_locales()
                st.success(f"🚀 Sincronización completada. {conteo_nuevos} altas master. {len(df_inscritos)} fichas indexadas.")
                st.rerun()
            except Exception as e:
                st.error(f"Error procesando el formato de inscripciones: {str(e)}. Verifica que las columnas no estén movidas.")
                
    st.markdown("---")
    st.markdown("### 🖼️ Cargar Imagen de Horario del Campus")
    archivo_imagen = st.file_uploader("Seleccionar imagen de horario:", type=["png", "jpg", "jpeg"], key="upload_admin_horario")
    
    if archivo_imagen is not None:
        # CORRECCIÓN: Botón explícito para guardar la imagen, eliminando la congelación por bucle infinito
        if st.button("💾 Confirmar y Guardar Imagen de Horario", key="btn_confirmar_imagen"):
            with open(f"horario_{semana_act}.png", "wb") as f:
                f.write(archivo_imagen.getbuffer())
            st.success(f"¡Imagen de horario guardada correctamente para la {semana_act}!")
            st.rerun()
            
    st.markdown("---")
    st.subheader("🚨 Eliminar Alumno de los Registros")
    alumno_a_borrar = st.selectbox("Selecciona el alumno a eliminar:", ["--- Selecciona ---"] + sorted(st.session_state.alumnos_master))
    if st.button("❌ Eliminar Alumno Definitivamente", type="primary"):
        if alumno_a_borrar != "--- Selecciona ---":
            st.session_state.alumnos_master.remove(alumno_a_borrar)
            if alumno_a_borrar in st.session_state.oraciones_aprendidas: del st.session_state.oraciones_aprendidas[alumno_a_borrar]
            if alumno_a_borrar in st.session_state.contador_comedor: del st.session_state.contador_comedor[alumno_a_borrar]
            if alumno_a_borrar in st.session_state.perfiles_alumnos: del st.session_state.perfiles_alumnos[alumno_a_borrar]
            for s in st.session_state.asistencia:
                if alumno_a_borrar in st.session_state.asistencia[s]: del st.session_state.asistencia[s][alumno_a_borrar]
            guardar_datos_locales()
            st.toast(f"🗑️ Eliminado: {alumno_a_borrar}"); st.rerun()
            
    st.markdown("---")
    st.subheader("📥 Carga a Granel (Semana 1)")
    with st.form("form_granel"):
        alumno_g = st.selectbox("Alumno:", sorted(st.session_state.alumnos_master))
        puntos_g = st.number_input("Puntos:", min_value=0, max_value=500, value=0)
        motivo_g = st.text_input("Motivo:", "Volcado masivo Excel Semana 1")
        if st.form_submit_button("🚀 Inyectar"):
            if puntos_g > 0:
                registrar_puntos(alumno_g, "Volcado Inicial", puntos_g, motivo_g)
                st.success("Puntos inyectados.")
            else: st.error("Introduce una puntuación válida.")

    st.markdown("---")
    st.subheader("🆕 Alta de Alumnos Nuevos")
    nuevo_nombre = st.text_input("Nombre completo del nuevo alumno:")
    if st.button("➕ Dar de alta Alumno"):
        if nuevo_nombre and nuevo_nombre not in st.session_state.alumnos_master:
            st.session_state.alumnos_master.append(nuevo_nombre)
            guardar_datos_locales()
            st.success(f"¡{nuevo_nombre} dado de alta!"); st.rerun()