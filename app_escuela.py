import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
import json
import os

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Escuela de Verano - Smart Panel", layout="wide", initial_sidebar_state="expanded")
st.title("🏆 Panel de Control - Escuela de Verano")

# --- 2. SISTEMA DE ARCHIVOS LOCALES (PERSISTENCIA ANTIF5) ---
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

for al in st.session_state.alumnos_master:
    if al not in st.session_state.oraciones_aprendidas: st.session_state.oraciones_aprendidas[al] = []
    if al not in st.session_state.contador_comedor: st.session_state.contador_comedor[al] = 0

if 'equipos_del_dia' not in st.session_state:
    st.session_state.equipos_del_dia = {"Alfa": [], "Beta": [], "Gamma": [], "Delta": []}
if 'capitanes_del_dia' not in st.session_state:
    st.session_state.capitanes_del_dia = {"Alfa": "", "Beta": "", "Gamma": "", "Delta": ""}

# --- LISTAS OFICIALES ---
LISTA_ORACIONES = [
    "Señal Sta Cruz", "Padrenuestro", "Ave María", "Gloria", "5 pasos confesion", 
    "Visita", "Angelus", "Oh Sra mía", "Angel Guarda", "10 mandamientos", 
    "Empezar oracion", "Acabar oracion", "Bendicion mesa", "Acc gracias dp comer", "5 mand Sta Mad Igl", 
    "Salve", "Bend sea pureza", "Señor mio Xto", "Acordaos", "Sacramentos"
]

LISTA_ENCARGOS_OFICIALES = [
    "ORDEN SALA DE ESTUDIO", "ORDEN COMEDOR", "ORDEN TALLERES", "ORDEN ZONA ALMUERZO", 
    "ORDEN VESTUARIOS", "ORDEN PISCINA", "MATERIAL DE DEPORTE", "MATERIAL DE PISCINA", 
    "NEVERA", "VASOS", "CUBIERTOS", "TUPPERS", "AGUA COMIDA", "PLAN TARDE", "ORATORIO"
]

# --- 3. BARRA LATERAL ---
st.sidebar.header("⚙️ Ajustes Diarios")
semana_act = st.sidebar.selectbox("📅 Semana del Campus:", ["Semana 1", "Semana 2", "Semana 3", "Semana 4"])
fecha_hoy = st.sidebar.date_input("📆 Fecha de Trabajo:", date.today())

with st.sidebar.expander("👥 Control de Asistencia Semanal"):
    st.caption("Desmarca a los niños ausentes esta semana:")
    for al in sorted(st.session_state.alumnos_master):
        if semana_act not in st.session_state.asistencia: st.session_state.asistencia[semana_act] = {}
        if al not in st.session_state.asistencia[semana_act]: st.session_state.asistencia[semana_act][al] = True
            
        val_check = st.checkbox(al, value=st.session_state.asistencia[semana_act][al], key=f"asist_sid_{al}")
        if val_check != st.session_state.asistencia[semana_act][al]:
            st.session_state.asistencia[semana_act][al] = val_check
            guardar_datos_locales()

alumnos_activos = [al for al in st.session_state.alumnos_master if st.session_state.asistencia[semana_act].get(al, True)]
st.sidebar.metric(label="👦 Niños Presentes", value=f"{len(alumnos_activos)} de {len(st.session_state.alumnos_master)}")

st.sidebar.markdown("---")
menu = st.sidebar.radio("📍 Actividades:", [
    "📊 Histórico & Ranking", "📚 Estudio", "🙏 Oraciones", "⚽ Deporte", 
    "🙌 Deportividad", "🎨 Taller", "🧹 Encargos Semanales", "🍽️ Limpieza Comedor", 
    "💪 Extras Activos", "🧠 Juegos", "🎥 Vídeo Formación", "⚠️ Penalizaciones", "🛠️ Administración"
])

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

# --- PANEL 1: HISTÓRICO, RANKINGS Y BUSCADOR GLOBAL REINCORPORADO ---
if menu == "📊 Histórico & Ranking":
    st.header("📊 Tablas de Clasificación Oficial")
    tab_semanal, tab_general = st.tabs(["📆 Premios Semanales (Esta Semana)", "🏆 Gran Premio General (Acumulado)"])
    df_hist = st.session_state.historico_puntos
    
    with tab_semanal:
        st.subheader(f"Clasificación Exclusiva: {semana_act}")
        if not df_hist.empty:
            df_sem = df_hist[df_hist['Semana'] == semana_act]
            df_tot_sem = df_sem.groupby('Alumno')['Puntos'].sum().reset_index() if not df_sem.empty else pd.DataFrame(columns=['Alumno', 'Puntos'])
        else:
            df_tot_sem = pd.DataFrame(columns=['Alumno', 'Puntos'])
            
        for al in alumnos_activos:
            if al not in df_tot_sem['Alumno'].values:
                df_tot_sem = pd.concat([df_tot_sem, pd.DataFrame([{'Alumno': al, 'Puntos': 0}])], ignore_index=True)
                
        df_tot_sem = df_tot_sem[df_tot_sem['Alumno'].isin(alumnos_activos)].sort_values(by="Puntos", ascending=True)
        fig_s = px.bar(df_tot_sem, x='Puntos', y='Alumno', orientation='h', color='Puntos', color_continuous_scale='Mint', text_auto=True)
        fig_s.update_traces(textposition='outside')
        fig_s.update_layout(height=650)
        st.plotly_chart(fig_s, width='stretch')
        
        csv_s = df_tot_sem.sort_values(by="Puntos", ascending=False).to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descargar CSV Semanal", data=csv_s, file_name=f"Ranking_{semana_act}.csv", mime='text/csv')

    with tab_general:
        st.subheader("Clasificación General Acumulada (Semanas 1 a 4)")
        df_tot_gen = df_hist.groupby('Alumno')['Puntos'].sum().reset_index() if not df_hist.empty else pd.DataFrame(columns=['Alumno', 'Puntos'])
            
        for al in st.session_state.alumnos_master:
            if al not in df_tot_gen['Alumno'].values:
                df_tot_gen = pd.concat([df_tot_gen, pd.DataFrame([{'Alumno': al, 'Puntos': 0}])], ignore_index=True)
                
        df_tot_gen = df_tot_gen.sort_values(by="Puntos", ascending=True)
        fig_g = px.bar(df_tot_gen, x='Puntos', y='Alumno', orientation='h', color='Puntos', color_continuous_scale='Blues', text_auto=True)
        fig_g.update_traces(textposition='outside')
        fig_g.update_layout(height=700)
        st.plotly_chart(fig_g, width='stretch')
        
        csv_g = df_tot_gen.sort_values(by="Puntos", ascending=False).to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descargar CSV General", data=csv_g, file_name="Ranking_General_Campus.csv", mime='text/csv')

    # --- CONSULTA DEL HISTORIAL GLOBAL SOLICITADA ---
    st.markdown("---")
    st.subheader("🔍 Historial Transaccional Completo (Auditoría en Vivo)")
    st.caption("A continuación se listan de forma cronológica todas las anotaciones de puntos y penalizaciones realizadas por los monitores.")
    if not st.session_state.historico_puntos.empty:
        # Mostramos el histórico ordenado de más nuevo a más antiguo
        st.dataframe(st.session_state.historico_puntos.iloc[::-1], width='stretch')
    else:
        st.info("Aún no se han registrado movimientos de puntos en el sistema.")

# --- PANEL 2: ESTUDIO (MEJORA: ALINEACIÓN VERTICAL ANTI-LINEWRAPPING EN MÓVIL) ---
elif menu == "📚 Estudio":
    st.header("📚 Control de la Hora de Estudio")
    opciones_estudio = {"No evaluado": None, "❌ 0 Puntos": 0, "⚠️ 2 Puntos": 2, "✅ 5 Puntos": 5}
    
    for al in sorted(alumnos_activos):
        st.markdown(f"**🧑 {al}**")
        pts_actuales = get_puntos_hoy(al, "Estudio", None)
        index_def = list(opciones_estudio.values()).index(pts_actuales)
        
        # Eliminamos horizontal=True para forzar que los botones de radio se apilen verticalmente en bloque grande
        seleccion = st.radio(f"Estudio_{al}", options=list(opciones_estudio.keys()), index=index_def, key=f"mob_est_{al}", label_visibility="collapsed")
        pts_seleccionados = opciones_estudio[seleccion]
        if pts_seleccionados is not None and pts_seleccionados != pts_actuales:
            set_puntos_hoy(al, "Estudio", pts_seleccionados, "Evaluación diaria de estudio")
            st.toast(f"Estudio {al} -> {seleccion}")
        st.markdown("<div style='border-bottom: 2px solid #f0f2f6; margin-bottom: 15px; margin-top: 10px;'></div>", unsafe_allow_html=True)

# --- PANEL 3: ORACIONES ---
elif menu == "🙏 Oraciones":
    st.header("🙏 Matriz de Oraciones Aprendidas")
    al_sel = st.selectbox("Selecciona un alumno para gestionar sus oraciones:", sorted(alumnos_activos))
    
    oraciones_actuales = st.session_state.oraciones_aprendidas.get(al_sel, [])
    nuevas_oraciones = []
    
    bloques_semanales = [
        {"nombre": "🟢 GRUPO 1 - SEMANA 1", "items": LISTA_ORACIONES[0:5], "color": "#e2f0cb"},
        {"nombre": "🔵 GRUPO 2 - SEMANA 2", "items": LISTA_ORACIONES[5:10], "color": "#b5ead7"},
        {"nombre": "🟡 GRUPO 3 - SEMANA 3", "items": LISTA_ORACIONES[10:15], "color": "#ffdac1"},
        {"nombre": "🟠 GRUPO 4 - SEMANA 4", "items": LISTA_ORACIONES[15:20], "color": "#ffb7b2"}
    ]
    
    for bloque in bloques_semanales:
        st.markdown(f'<div style="background-color: {bloque["color"]}; padding: 8px; border-radius: 4px; margin-top: 15px; font-weight: bold; color: #333;">{bloque["nombre"]}</div>', unsafe_allow_html=True)
        for oracion in bloque["items"]:
            marcado = oracion in oraciones_actuales
            if st.checkbox(oracion, value=marcado, key=f"chk_list_u_{al_sel}_{oracion}"):
                nuevas_oraciones.append(oracion)
                
    if nuevas_oraciones != oraciones_actuales:
        st.session_state.oraciones_aprendidas[al_sel] = nuevas_oraciones
        st.session_state.historico_puntos = st.session_state.historico_puntos[
            ~((st.session_state.historico_puntos['Alumno'] == al_sel) & (st.session_state.historico_puntos['Actividad'] == "Oración"))
        ]
        for o in nuevas_oraciones:
            registrar_puntos = pd.DataFrame([{
                'Fecha': str(fecha_hoy), 'Alumno': al_sel, 'Actividad': "Oración", 'Puntos': 5, 'Detalle': f"Sabe: {o}", 'Semana': semana_act
            }])
            st.session_state.historico_puntos = pd.concat([st.session_state.historico_puntos, registrar_puntos], ignore_index=True)
        guardar_datos_locales()
        st.success(f"Oraciones guardadas para {al_sel}.")

# --- PANEL 4: DEPORTE ---
elif menu == "⚽ Deporte":
    st.header("⚽ Torneo de Deportes del Día")
    num_equipos = st.slider("¿Cuántos equipos compiten hoy?", 2, 4, 2)
    nombres_base = ["Alfa", "Beta", "Gamma", "Delta"][:num_equipos]
    
    for eq in nombres_base:
        if f"m_dep_{eq}" not in st.session_state: st.session_state[f"m_dep_{eq}"] = []
        if f"c_dep_{eq}" not in st.session_state: st.session_state[f"c_dep_{eq}"] = ""
        
    st.subheader("👥 Configuración de Capitanes y Miembros Exclusivos")
    capitanes_elegidos = {}
    for eq in nombres_base:
        ocupados_caps = [v for k, v in capitanes_elegidos.items() if v != ""]
        dispo_cap = [al for al in alumnos_activos if al not in ocupados_caps]
        def_cap = st.session_state[f"c_dep_{eq}"]
        idx_c = dispo_cap.index(def_cap) if def_cap in dispo_cap else 0
        capitanes_elegidos[eq] = st.selectbox(f"👑 Selecciona Capitán para Equipo {eq}:", [""] + dispo_cap, index=idx_c, key=f"c_dep_sel_{eq}")
        st.session_state[f"c_dep_{eq}"] = capitanes_elegidos[eq]
        
    st.markdown("---")
    equipos_finales = {}
    for eq in nombres_base:
        cap_name = st.session_state[f"c_dep_{eq}"]
        label_equipo = f"Equipo {eq} (Capitán: {cap_name})" if cap_name else f"Equipo {eq}"
        st.markdown(f"##### {label_equipo}")
        
        ocupados_total = []
        for o_eq in nombres_base:
            if o_eq != eq:
                if st.session_state[f"c_dep_{o_eq}"]: ocupados_total.append(st.session_state[f"c_dep_{o_eq}"])
                ocupados_total.extend(st.session_state[f"m_dep_{o_eq}"])
                
        dispo_jugadores = [al for al in alumnos_activos if al not in ocupados_total and al != cap_name]
        def_j = [al for al in st.session_state[f"m_dep_{eq}"] if al in dispo_jugadores]
        equipos_finales[eq] = st.multiselect(f"Añadir jugadores a {label_equipo}:", options=dispo_jugadores, default=def_j, key=f"m_dep_sel_{eq}")
        st.session_state[f"m_dep_{eq}"] = equipos_finales[eq]

    st.subheader("🏆 Guardar Puntos del Deporte")
    mapa_pts = {5: "1º Lugar (5 Pts)", 3: "2º Lugar (3 Pts)", 2: "3º Lugar (2 Pts)", 0: "4º Lugar (0 Pts)"}
    res_deporte = {}
    for eq in nombres_base:
        cap_name = st.session_state[f"c_dep_{eq}"]
        tag = f"Equipo {eq} [{cap_name}]" if cap_name else f"Equipo {eq}"
        res_deporte[eq] = st.selectbox(f"Clasificación para {tag}:", [5, 3, 2, 0], format_func=lambda x: mapa_pts[x], key=f"res_dep_p_{eq}")
        
    motivo_dep = st.text_input("Deporte jugado hoy:", "Fútbol / Baloncesto")
    if st.button("💾 Registrar Deporte Hoy"):
        for eq in nombres_base:
            puntos = res_deporte[eq]
            cap_n = st.session_state[f"c_dep_{eq}"]
            if cap_n: set_puntos_hoy(cap_n, "Deporte", puntos, f"Torneo de {motivo_dep} - Cap {eq}")
            for jug in st.session_state[f"m_dep_{eq}"]:
                set_puntos_hoy(jug, "Deporte", puntos, f"Torneo de {motivo_dep} - Miembro {eq}")
        st.success("Puntuaciones de torneo asignadas.")

# --- PANEL 5: DEPORTIVIDAD (MEJORA: ALINEACIÓN VERTICAL EN MÓVIL) ---
elif menu == "🙌 Deportividad":
    st.header("🙌 Control de Deportividad")
    opciones_dep = {"5 Pts (Excelente)": 5, "2 Pts (Quejas/Faltas)": 2, "0 Pts (Falta Respeto)": 0}
    for al in sorted(alumnos_activos):
        st.markdown(f"**🙌 {al}**")
        pts_act = get_puntos_hoy(al, "Deportividad", 5)
        idx_def = list(opciones_dep.values()).index(pts_act)
        
        # Eliminamos horizontal=True para evitar el desborde y asegurar bloque vertical táctil
        sel = st.radio(f"Dep_{al}", options=list(opciones_dep.keys()), index=idx_def, key=f"mob_dep_{al}", label_visibility="collapsed")
        if opciones_dep[sel] != pts_act:
            set_puntos_hoy(al, "Deportividad", opciones_dep[sel], "Comportamiento en pista")
        st.markdown("<div style='border-bottom: 2px solid #f0f2f6; margin-bottom: 15px; margin-top: 10px;'></div>", unsafe_allow_html=True)

# --- PANEL 6: TALLER (MEJORA: ALINEACIÓN VERTICAL EN MÓVIL) ---
elif menu == "🎨 Taller":
    st.header("🎨 Trabajo en los Talleres")
    opciones_tal = {"5 Pts (Trabajador)": 5, "2 Pts (Despistado)": 2, "0 Pts (Mal Comportamiento)": 0}
    for al in sorted(alumnos_activos):
        st.markdown(f"**🎨 {al}**")
        pts_act = get_puntos_hoy(al, "Taller", 5)
        idx_def = list(opciones_tal.values()).index(pts_act)
        
        # Eliminamos horizontal=True para empujar las opciones en vertical
        sel = st.radio(f"Tal_{al}", options=list(opciones_tal.keys()), index=idx_def, key=f"mob_tal_{al}", label_visibility="collapsed")
        if opciones_tal[sel] != pts_act:
            set_puntos_hoy(al, "Taller", opciones_tal[sel], "Desempeño en taller")
        st.markdown("<div style='border-bottom: 2px solid #f0f2f6; margin-bottom: 15px; margin-top: 10px;'></div>", unsafe_allow_html=True)

# --- PANEL 7: ENCARGOS SEMANALES ---
elif menu == "🧹 Encargos Semanales":
    st.header("🧹 Distribución de Encargos Oficiales")
    tab_fijos, tab_turno = st.tabs(["📌 Encargos de la Semana", "🙏 Estar de Turno (Oración Diaria)"])
    
    if semana_act not in st.session_state.encargos_semanales:
        st.session_state.encargos_semanales[semana_act] = {e: [] for e in LISTA_ENCARGOS_OFICIALES}
        
    with tab_fijos:
        st.subheader("Asignación Semanal Exclusiva")
        for encargo in LISTA_ENCARGOS_OFICIALES:
            ocupados_otros = []
            for o_enc, elegidos in st.session_state.encargos_semanales[semana_act].items():
                if o_enc != encargo: ocupados_otros.extend(elegidos)
            
            dispo_encargo = [al for al in alumnos_activos if al not in ocupados_otros]
            def_enc = [al for al in st.session_state.encargos_semanales[semana_act].get(encargo, []) if al in dispo_encargo]
            
            sel_enc = st.multiselect(f"🛠️ {encargo}:", options=dispo_encargo, default=def_enc, max_selections=2, key=f"fij_box_mob_{encargo}")
            st.session_state.encargos_semanales[semana_act][encargo] = sel_enc
            
        st.markdown("---")
        st.subheader("📋 Puntuación Diaria")
        op_enc = {"5 Pts (Bien)": 5, "2 Pts (Regular)": 2, "0 Pts (Mal)": 0}
        
        for encargo, encargados in st.session_state.encargos_semanales[semana_act].items():
            if encargados:
                st.markdown(f"**{encargo}**")
                for nino in encargados:
                    c_n, c_r = st.columns([2, 2])
                    c_n.write(f"└─ {nino}")
                    pts_a = get_puntos_hoy(nino, f"Encargo_{encargo}", None)
                    idx_e = list(op_enc.values()).index(pts_a) if pts_a in op_enc.values() else 0
                    sel_e = c_r.radio(f"r_enc_{encargo}_{nino}", list(op_enc.keys()), index=idx_e, horizontal=True, key=f"rd_enc_{encargo}_{nino}", label_visibility="collapsed")
                    if op_enc[sel_e] != pts_a:
                        set_puntos_hoy(nino, f"Encargo_{encargo}", op_enc[sel_e], f"Cumplió: {encargo}")
                        
    with tab_turno:
        st.subheader("🙏 Turno de Oración de la Semana")
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
        for d in dias:
            if semana_act not in st.session_state.estar_de_turno: st.session_state.estar_de_turno[semana_act] = {}
            def_t = st.session_state.estar_de_turno[semana_act].get(d, "")
            idx_t = alumnos_activos.index(def_t) + 1 if def_t in alumnos_activos else 0
            
            sel_t = st.selectbox(f"Encargado del {d}:", ["--- Sin asignar ---"] + alumnos_activos, index=idx_t, key=f"turno_or_{d}")
            if sel_t != def_t:
                st.session_state.estar_de_turno[semana_act][d] = sel_t if sel_t != "--- Sin asignar ---" else ""
                guardar_datos_locales()

# --- PANEL 8: LIMPIEZA COMEDOR ---
elif menu == "🍽️ Limpieza Comedor":
    st.header("🍽️ Tareas de Limpieza después de Comer (10 Puntos)")
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
        st.subheader("Cuadrante de Limpieza")
        roles_f = {}
        for rol, sugeridos in st.session_state.limpieza_propuesta.items():
            max_s = 2 if "(2)" in rol else 1
            roles_f[rol] = st.multiselect(f"Responsables para {rol}:", alumnos_activos, default=sugeridos, max_selections=max_s, key=f"lim_{rol}")
        if st.button("💾 Validar Limpieza y Asignar +10 Puntos"):
            for rol, elegidos in roles_f.items():
                for el in elegidos:
                    set_puntos_hoy(el, "Limpieza Comedor", 10, f"Rol diario: {rol}")
                    st.session_state.contador_comedor[el] += 1
            st.success("¡Cuadrante guardado!")

# --- PANEL 9: EXTRAS EN VIVO ---
elif menu == "💪 Extras Activos":
    st.header("💪 Marcador de Encargos Extra en Vivo")
    
    motivo_live = st.text_input("Trabajo Extra Actual:", "Ayudar a ordenar el pabellón de deportes")
    st.markdown("---")
    
    for al in sorted(alumnos_activos):
        c_name, c_btn = st.columns([3, 1])
        c_name.write(f"🏃 **{al}**")
        if c_btn.button(f"➕ 1 Pt Extra", key=f"btn_live_ex_{al}"):
            nueva_f = pd.DataFrame([{
                'Fecha': str(fecha_hoy), 'Alumno': al, 'Actividad': "Extra", 
                'Puntos': 1, 'Detalle': motivo_live, 'Semana': semana_act
            }])
            st.session_state.historico_puntos = pd.concat([st.session_state.historico_puntos, nueva_f], ignore_index=True)
            guardar_datos_locales()
            st.toast(f"¡+1 Punto Extra a {al}!")
            st.rerun()
            
    st.markdown("---")
    st.subheader("🔍 Historial de Puntos Extra Añadidos Hoy")
    df_h = st.session_state.historico_puntos
    if not df_h.empty:
        df_extra_hoy = df_h[(df_h['Fecha'].astype(str) == str(fecha_hoy)) & (df_h['Actividad'] == "Extra")]
        if not df_extra_hoy.empty:
            st.dataframe(df_extra_hoy[['Alumno', 'Puntos', 'Detalle', 'Semana']], width='stretch')
        else:
            st.write("Aún no se han asignado puntos extra hoy.")
    else:
        st.write("Aún no se han asignado puntos extra hoy.")

# --- PANEL 10: JUEGOS ---
elif menu == "🧠 Juegos":
    st.header("🧠 Puntuación de Juegos de Mesa / Quizzes del Día")
    nombres_j = ["Alfa", "Beta", "Gamma", "Delta"]
    mapa_j = {5: "5 Puntos", 3: "3 Puntos", 2: "2 Puntos", 0: "0 Puntos"}
    motivo_juego = st.text_input("Nombre del juego de hoy:", "Gran Gymkhana / Superquiz")
    
    for eq in nombres_j:
        cap_name = st.session_state.get(f"c_dep_{eq}", "")
        tag_j = f"Equipo {eq} (Capitán: {cap_name})" if cap_name else f"Equipo {eq}"
        st.markdown(f"##### {tag_j}")
        pts_juego = st.selectbox(f"Puntos para {tag_j}:", [5, 3, 2, 0], format_func=lambda x: mapa_j[x], key=f"pts_jue_sl_{eq}")
        if st.button(f"Confirmar puntos de {tag_j}", key=f"btn_jue_save_{eq}"):
            miembros_eq = st.session_state.get(f"m_dep_{eq}", [])
            if cap_name: set_puntos_hoy(cap_name, "Juegos", pts_juego, f"Juego: {motivo_juego} ({eq})")
            for m in miembros_eq: set_puntos_hoy(m, "Juegos", pts_juego, f"Juego: {motivo_juego} ({eq})")
            st.success(f"Puntos asignados a {tag_j}")

# --- PANEL 11: VÍDEO FORMACIÓN (CON COLA DE PREFERENCIA FIJA ESTABLE) ---
elif menu == "🎥 Vídeo Formación":
    st.header("🎥 Preguntas del Vídeo de Formación (2 Pts por Acierto)")
    
    if 'vid_preg_num' not in st.session_state: st.session_state.vid_preg_num = 1
    
    conteo_v = {}
    for al in alumnos_activos:
        if not st.session_state.historico_puntos.empty:
            conteo_v[al] = len(st.session_state.historico_puntos[(st.session_state.historico_puntos['Alumno'] == al) & (st.session_state.historico_puntos['Actividad'] == "Video Formación")])
        else:
            conteo_v[al] = 0

    if st.button("🔄 Generar / Congelar Fila del Día (Evita saltos de bug)"):
        st.session_state.fixed_queue = sorted(alumnos_activos, key=lambda x: conteo_v[x])
        st.session_state.vid_pointer = 0
        st.success("¡Fila congelada con éxito para esta sesión!")

    if 'fixed_queue' not in st.session_state:
        st.session_state.fixed_queue = sorted(alumnos_activos, key=lambda x: conteo_v[x])
        st.session_state.vid_pointer = 0

    cola_fija = st.session_state.fixed_queue
    total_cola = len(cola_fija)
    p = st.session_state.vid_pointer
    
    if p >= total_cola: p = 0; st.session_state.vid_pointer = 0
    
    st.subheader(f"❓ Pregunta Actual N° {st.session_state.vid_preg_num}")
    titular = cola_fija[p] if total_cola > 0 else "Nadie"
    r1 = cola_fija[(p+1)%total_cola] if total_cola > 1 else "Nadie"
    r2 = cola_fija[(p+2)%total_cola] if total_cola > 2 else "Nadie"
    r3 = cola_fija[(p+3)%total_cola] if total_cola > 3 else "Nadie"
    r4 = cola_fija[(p+4)%total_cola] if total_cola > 4 else "Nadie"
    r5 = cola_fija[(p+5)%total_cola] if total_cola > 5 else "Nadie"
    
    st.info(f"🎯 **Pregunta dirigida a:** {titular}")
    
    c_t1, c_t2 = st.columns([3, 1])
    c_t1.write(f"🔹 Principal: **{titular}**")
    if c_t2.button("✅ Acertó Principal (+2 Pts)", key="v_btn_tit"):
        set_puntos_hoy(titular, "Video Formación", 2, f"Pregunta {st.session_state.vid_preg_num}")
        st.session_state.vid_pointer = (cola_fija.index(titular) + 1) % total_cola
        st.session_state.vid_preg_num += 1
        st.rerun()
        
    st.markdown("---")
    st.write("**Cadena de Rebotes Inalterable:**")
    
    rebotes = [r1, r2, r3, r4, r5]
    for idx, reb_alumno in enumerate(rebotes, start=1):
        cr_n, cr_b = st.columns([3, 1])
        cr_n.write(f"↪️ **Rebote {idx}:** {reb_alumno}")
        if cr_b.button(f"💥 Acertó Rebote {idx} (+2)", key=f"v_btn_r_{idx}"):
            set_puntos_hoy(reb_alumno, "Video Formación", 2, f"Preg {st.session_state.vid_preg_num} - Rebote {idx}")
            st.session_state.vid_pointer = (cola_fija.index(reb_alumno) + 1) % total_cola
            st.session_state.vid_preg_num += 1
            st.rerun()
            
    st.markdown("---")
    if st.button("⏭️ Saltar Pregunta (Avanzar la fila un puesto sin sumar)"):
        st.session_state.vid_pointer = (st.session_state.vid_pointer + 1) % total_cola
        st.session_state.vid_preg_num += 1
        st.rerun()
        
    st.markdown("---")
    st.write("**🙋 Mano Levantada Extra:**")
    al_libre = st.selectbox("Asignar acierto directo libre a:", ["--- Selecciona ---"] + alumnos_activos, key="sb_libre_vid")
    if st.button("💾 Dar +2 por mano levantada"):
        if al_libre != "--- Selecciona ---":
            set_puntos_hoy(al_libre, "Video Formación", 2, "Mano levantada libre")
            st.success("Cargado.")

# --- PANEL 12: PENALIZACIONES ---
elif menu == "⚠️ Penalizaciones":
    st.header("⚠️ Registro de Penalizaciones Especiales")
    
    ninos_a_penalizar = st.multiselect("Selecciona los alumnos a penalizar:", sorted(alumnos_activos))
    motivo_p = st.text_input("Motivo de la infracción (Obligatorio):", placeholder="Ej. Protestar de forma desconsiderada en el juego")
    
    c1, c2, c3, c4, c5 = st.columns(5)
    puntos_a_quitar = None
    
    if c1.button("📉 -1 Pt"): puntos_a_quitar = -1
    if c2.button("📉 -2 Pts"): puntos_a_quitar = -2
    if c3.button("📉 -3 Pts"): puntos_a_quitar = -3
    if c4.button("📉 -4 Pts"): puntos_a_quitar = -4
    if c5.button("📉 -5 Pts"): puntos_a_quitar = -5
        
    if puntos_a_quitar is not None:
        if ninos_a_penalizar and motivo_p:
            for al_p in ninos_a_penalizar:
                nueva_f = pd.DataFrame([{
                    'Fecha': str(fecha_hoy), 'Alumno': al_p, 'Actividad': "Penalizacion", 
                    'Puntos': puntos_a_quitar, 'Detalle': motivo_p, 'Semana': semana_act
                }])
                st.session_state.historico_puntos = pd.concat([st.session_state.historico_puntos, nueva_f], ignore_index=True)
            guardar_datos_locales()
            st.error(f"Se han restado {puntos_a_quitar} Pts.")
            st.rerun()
        else:
            st.warning("⚠️ Selecciona alumnos y escribe el motivo antes de asignar puntos negativos.")
            
    st.markdown("---")
    st.subheader("🔍 Historial de Penalizaciones Aplicadas Hoy")
    df_h = st.session_state.historico_puntos
    if not df_h.empty:
        df_pen_hoy = df_h[(df_h['Fecha'].astype(str) == str(fecha_hoy)) & (df_h['Actividad'] == "Penalizacion")]
        if not df_pen_hoy.empty:
            st.dataframe(df_pen_hoy[['Alumno', 'Puntos', 'Detalle', 'Semana']], width='stretch')
        else:
            st.write("No hay penalizaciones registradas hoy.")
    else:
        st.write("No hay penalizaciones registradas hoy.")

# --- PANEL 13: ADMINISTRACIÓN ---
elif menu == "🛠️ Administración":
    st.header("🛠️ Configuración e Inicialización")
    st.subheader("📥 Carga de Puntos a Granel (Histórico de Semana 1)")
    
    with st.form("form_granel"):
        alumno_g = st.selectbox("Selecciona al Alumno:", sorted(st.session_state.alumnos_master))
        puntos_g = st.number_input("Puntos Totales Acumulados:", min_value=0, max_value=500, value=0)
        motivo_g = st.text_input("Origen o motivo del volcado:", "Volcado masivo Excel Semana 1 de pruebas")
        
        if st.form_submit_button("🚀 Inyectar Puntos a Granel"):
            if puntos_g > 0:
                nueva_f = pd.DataFrame([{
                    'Fecha': str(fecha_hoy), 'Alumno': alumno_g, 'Actividad': "Volcado Inicial", 
                    'Puntos': puntos_g, 'Detalle': motivo_g, 'Semana': "Semana 1"
                }])
                st.session_state.historico_puntos = pd.concat([st.session_state.historico_puntos, nueva_f], ignore_index=True)
                guardar_datos_locales()
                st.success(f"¡Inyectados {puntos_g} puntos con éxito a {alumno_g}!")
            else:
                st.error("Introduce una puntuación mayor que cero.")

    st.markdown("---")
    st.subheader("🆕 Alta de Alumnos Nuevos")
    nuevo_nombre = st.text_input("Nombre completo del nuevo alumno:")
    if st.button("➕ Dar de alta Alumno"):
        if nuevo_nombre and nuevo_nombre not in st.session_state.alumnos_master:
            st.session_state.alumnos_master.append(nuevo_nombre)
            guardar_datos_locales()
            st.success(f"¡{nuevo_nombre} dado de alta con éxito!")
            st.rerun()
            
    st.markdown("---")
    if st.button("🚨 REINICIAR TODA LA ESCUELA DE VERANO"):
        for f in ["local_historico_puntos.csv", "local_alumnos_master.json", "local_oraciones.json", "local_comedor.json", "local_encargos.json", "local_asistencia.json", "local_turno.json"]:
            if os.path.exists(f): os.remove(f)
        st.session_state.clear()
        st.success("Datos reseteados. Refresca la web.")
        st.rerun()