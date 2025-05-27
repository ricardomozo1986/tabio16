
import streamlit as st
import pandas as pd

st.set_page_config(layout='wide')
st.title("📊 Plataforma Estratégica Predial Municipal")

# --- Cargar archivo ---
uploaded_file = st.file_uploader("Sube tu base de datos predial", type=["xlsx"])

# Verificar que el archivo se haya cargado correctamente
if uploaded_file:
    try:
        
# Verificar que el archivo se haya cargado correctamente
if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        # Validar que las columnas esenciales existen
        columnas_necesarias = ['codigo_igac', 'sector_urbano', 'vereda', 'area_de_terreno', 'area_construida', 'propiedad_horizontal', 'sector', 'destino_economico_predio', 'condicion_predio', 'avaluo_catastral', 'rango_avaluos_predios', 'rango_areas_lote_predios', 'rangos_impuestos_a_pagar', 'valor_impuesto_a_pagar', 'descuentos_impuesto_predial', 'pago_impuesto_predial', 'financiacion_impuesto_predial', 'recaudo_predial', 'latitud', 'longitud']
        columnas_faltantes = [col for col in columnas_necesarias if col not in df.columns]
        if columnas_faltantes:
            st.error("⚠️ El archivo cargado no contiene todas las columnas necesarias.\n\nFaltan: " + ", ".join(columnas_faltantes))
            st.stop()
    except Exception as e:
        st.error(f"⚠️ Error al procesar el archivo: {e}")
        st.stop()
else:
    st.warning("📁 Por favor, carga un archivo Excel (.xlsx) para comenzar.")
    st.stop()


        # Validar que las columnas esenciales existen
        columnas_necesarias = ['codigo_igac', 'vereda', 'sector', 'sector_urbano', 'avaluo_catastral',
                               'valor_impuesto_a_pagar', 'recaudo_predial', 'descuentos_impuesto_predial',
                               'area_construida', 'pago_impuesto_predial', 'financiacion_impuesto_predial',
                               'latitud', 'longitud']
        if all(col in df.columns for col in columnas_necesarias):
            pass  # OK
        else:
            st.error("⚠️ El archivo cargado no contiene todas las columnas necesarias.")
            st.stop()

    except Exception as e:
        st.error(f"⚠️ Error al procesar el archivo: {e}")
        st.stop()
else:
    st.warning("📁 Por favor, carga un archivo Excel (.xlsx) para comenzar.")
    st.stop()


    # --- Normalizar columnas ---
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("á", "a")
        .str.replace("é", "e")
        .str.replace("í", "i")
        .str.replace("ó", "o")
        .str.replace("ú", "u")
    )

    st.sidebar.header("Filtros globales")
    veredas = ['Todas'] + sorted(df['vereda'].dropna().unique().tolist())
    sectores_urb = ['Todos'] + sorted(df['sector_urbano'].dropna().unique().tolist())
    ph_vals = ['Todos'] + sorted(df['propiedad_horizontal'].dropna().unique().tolist())

    filtro_vereda = st.sidebar.selectbox("Vereda", veredas)
    filtro_sector_urbano = st.sidebar.selectbox("Sector urbano", sectores_urb)
    filtro_ph = st.sidebar.selectbox("Propiedad horizontal", ph_vals)

    df_filtrado = df.copy()
    if filtro_vereda != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['vereda'] == filtro_vereda]
    if filtro_sector_urbano != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['sector_urbano'] == filtro_sector_urbano]
    if filtro_ph != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['propiedad_horizontal'] == filtro_ph]

    
    # Información General del Municipio
    st.title("🏛️ Información General del Municipio")
    st.markdown("Este panel muestra indicadores clave extraídos de la base de datos predial.")

    total_predios = len(df)
    total_avaluo = df['avaluo_catastral'].sum()
    total_impuesto = df['valor_impuesto_a_pagar'].sum()
    total_recaudo = df['recaudo_predial'].sum()
    cumplimiento = df['pago_impuesto_predial'].str.lower().eq('si').mean() * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Total predios", f"{total_predios:,}")
    col2.metric("Avalúo total", f"${total_avaluo:,.0f}")
    col3.metric("Impuesto total", f"${total_impuesto:,.0f}")

    col4, col5 = st.columns(2)
    col4.metric("Recaudo total", f"${total_recaudo:,.0f}")
    col5.metric("Cumplimiento (%)", f"{cumplimiento:.2f}%")


    tabs = st.tabs([
        "📊 0. Información General",
        "📌 1. Cumplimiento tributario",
        "📉 2. Segmentación cartera morosa",
        "🏗️ 3. Oportunidades catastrales",
        "💰 4. Estrategias de cobro",
        "🔮 5. Simulación de escenarios",
        "🗺️ 6. Riesgo geoespacial"
    ])

    
    
    with tabs[0]:
        st.header("0. Información General del Municipio")
        st.markdown("Este panel muestra un tablero resumen de indicadores clave, desagregado por sector.")

        veredas = ['Todas'] + sorted(df['vereda'].dropna().unique().tolist())
        sectores = ['Todos', 'URBANO', 'RURAL']

        filtro_vereda = st.selectbox("Filtrar por vereda", veredas, key="info_vereda")
        filtro_sector = st.selectbox("Filtrar por sector", sectores, key="info_sector")

        df_info = df.copy()
        if filtro_vereda != 'Todas':
            df_info = df_info[df_info['vereda'] == filtro_vereda]
        if filtro_sector != 'Todos':
            df_info = df_info[df_info['sector'] == filtro_sector]

        df_info['saldo'] = df_info['valor_impuesto_a_pagar'] - df_info['recaudo_predial']

        def resumen(df):
            return {
                'Predios': len(df),
                'Avalúo': df['avaluo_catastral'].sum(),
                'Impuesto': df['valor_impuesto_a_pagar'].sum(),
                'Recaudo': df['recaudo_predial'].sum(),
                'Descuento': df['descuentos_impuesto_predial'].sum(),
                'Saldo': df['saldo'].sum()
            }

        totales = resumen(df_info)
        urbanos = resumen(df_info[df_info['sector'] == 'URBANO'])
        rurales = resumen(df_info[df_info['sector'] == 'RURAL'])

        st.markdown("### Indicadores Clave (KPI)")
        kpi_data = pd.DataFrame([totales, urbanos, rurales], index=['Total', 'Urbano', 'Rural']).T
        st.dataframe(kpi_data.style.format("${:,.0f}", na_rep="-", subset=["Avalúo", "Impuesto", "Recaudo", "Descuento", "Saldo"]))


    with tabs[1]:
        st.header("1. Análisis de cumplimiento tributario")
        st.markdown("Este módulo permite analizar el cumplimiento tributario con indicadores clave y un mapa interactivo.")

        # Crear campo de cumplimiento (1 = pagó, 0 = no pagó)
        df_filtrado['cumplimiento'] = df_filtrado['pago_impuesto_predial'].apply(lambda x: 1 if str(x).lower() == 'si' else 0)

        # KPI globales
        total_predios = len(df_filtrado)
        total_facturado = df_filtrado['valor_impuesto_a_pagar'].sum()
        total_recaudo = df_filtrado['recaudo_predial'].sum()
        tasa_predios_cumplen = df_filtrado['cumplimiento'].mean() * 100
        tasa_recaudo = (total_recaudo / total_facturado * 100) if total_facturado > 0 else 0

        col1, col2, col3 = st.columns(3)
        col1.metric("Predios que pagan (%)", f"{tasa_predios_cumplen:.2f}%")
        col2.metric("Recaudo / Facturado", f"{tasa_recaudo:.2f}%")
        col3.metric("Total predios", f"{total_predios:,}")

        # Agrupar por vereda y calcular cumplimiento
        df_agrupado = df_filtrado.groupby('vereda').agg({
            'cumplimiento': 'mean',
            'valor_impuesto_a_pagar': 'sum',
            'recaudo_predial': 'sum',
            'latitud': 'mean',
            'longitud': 'mean'
        }).reset_index()

        df_agrupado['tasa_recaudo'] = (df_agrupado['recaudo_predial'] / df_agrupado['valor_impuesto_a_pagar']) * 100
        df_agrupado['cumplimiento_pct'] = df_agrupado['cumplimiento'] * 100

        # Mapa con datos individuales (sin quintiles)
        # Eliminado agrupamiento por quintiles pd.qcut(df_agrupado['cumplimiento_pct'], 5, labels=False)
        df_agrupado['quintil_cumplimiento'] += 1

        # Mapa interactivo
        import folium
        from folium.plugins import MarkerCluster
        from streamlit_folium import st_folium

        mapa = folium.Map(location=[df_agrupado['latitud'].mean(), df_agrupado['longitud'].mean()], zoom_start=12)
        cluster = MarkerCluster().add_to(mapa)

        for _, row in df_filtrado[df_filtrado['cumplimiento'] == 1].iterrows():
            folium.CircleMarker(
                location=[row['latitud'], row['longitud']],
                radius=10,
                color='blue',
                fill=True,
                fill_color='green' if row['cumplimiento_pct'] > 75 else 'orange' if row['cumplimiento_pct'] > 50 else 'red',
                fill_opacity=0.6,
                popup=(f"Vereda: {row['vereda']}<br>"
                       f"Cumplimiento: {row['cumplimiento_pct']:.2f}%<br>"
                       f"Recaudo: ${row['recaudo_predial']:,.0f}<br>"
                       f"Facturado: ${row['valor_impuesto_a_pagar']:,.0f}")
            ).add_to(cluster)

        st.markdown("### Mapa de cumplimiento por vereda (quintiles)")
        st_folium(mapa, width=700, height=500)


    
    with tabs[1]:
        st.header("2. Segmentación de cartera morosa")
        st.markdown("Este módulo permite visualizar los predios en mora y segmentarlos por quintiles de avalúo, impuesto y tipo de uso.")

        # Filtrar morosos
        morosos = df_filtrado[df_filtrado['pago_impuesto_predial'].str.lower() == 'no']

        # Crear quintiles
        morosos['quintil_avaluo'] = pd.qcut(morosos['avaluo_catastral'], 5, labels=False) + 1
        morosos['quintil_impuesto'] = pd.qcut(morosos['valor_impuesto_a_pagar'], 5, labels=False) + 1
        morosos['quintil_area_construida'] = pd.qcut(morosos['area_construida'], 5, labels=False, duplicates='drop') + 1

        # Indicador: predios morosos con alto avalúo o área construida
        alto_avaluo = morosos['avaluo_catastral'] > morosos['avaluo_catastral'].median()
        alta_area = morosos['area_construida'] > morosos['area_construida'].median()
        morosos_criticos = morosos[alto_avaluo | alta_area]

        st.markdown(f"**Total predios morosos:** {len(morosos):,}")
        st.markdown(f"**Morosos con alto avalúo o área construida:** {len(morosos_criticos):,}")

        # Gráfico: Morosos por tipo de uso
        st.markdown("#### Morosos por destino económico")
        uso_counts = morosos['destino_economico_predio'].value_counts()
        st.bar_chart(uso_counts)

        # Mapa interactivo
        import folium
        from folium.plugins import MarkerCluster
        from streamlit_folium import st_folium

        mapa_mora = folium.Map(location=[morosos['latitud'].mean(), morosos['longitud'].mean()], zoom_start=12)
        cluster = MarkerCluster().add_to(mapa_mora)

        for _, row in morosos.iterrows():
            folium.CircleMarker(
                location=[row['latitud'], row['longitud']],
                radius=8,
                color='crimson',
                fill=True,
                fill_color='crimson',
                fill_opacity=0.6,
                popup=(f"Vereda: {row['vereda']}<br>"
                       f"Uso: {row['destino_economico_predio']}<br>"
                       f"Avalúo: ${row['avaluo_catastral']:,.0f}<br>"
                       f"Impuesto: ${row['valor_impuesto_a_pagar']:,.0f}<br>"
                       f"Área construida: {row['area_construida']}")
            ).add_to(cluster)

        st.markdown("### Mapa de predios en mora")
        st_folium(mapa_mora, width=700, height=500)

        # Tabla de predios morosos
        st.markdown("### 🧾 Lista de predios en mora")
        st.dataframe(morosos[['codigo_igac', 'vereda', 'destino_economico_predio', 'avaluo_catastral', 'valor_impuesto_a_pagar', 'area_construida']].reset_index(drop=True))



    
    with tabs[2]:
        st.header("3. Oportunidades de actualización catastral")
        st.markdown("Este módulo identifica predios con posibles inconsistencias entre el área construida y el avalúo o el pago.")

        # Predios con área construida igual a cero y alto avalúo
        sin_construccion = df_filtrado[(df_filtrado['area_construida'] == 0)]
        sin_construccion_alto_avaluo = sin_construccion[sin_construccion['avaluo_catastral'] > sin_construccion['avaluo_catastral'].median()]

        # Predios sin pago y alto valor de impuesto
        sin_pago_alto_valor = df_filtrado[
            (df_filtrado['pago_impuesto_predial'].str.lower() == 'no') &
            (df_filtrado['valor_impuesto_a_pagar'] > df_filtrado['valor_impuesto_a_pagar'].median())
        ]

        # Mostrar totales
        st.markdown(f"**Predios con 0 área construida:** {len(sin_construccion):,}")
        st.markdown(f"**De ellos, con alto avalúo:** {len(sin_construccion_alto_avaluo):,}")
        st.markdown(f"**Predios sin pago con alto impuesto:** {len(sin_pago_alto_valor):,}")

        # Mapa combinado
        import folium
        from folium.plugins import MarkerCluster
        from streamlit_folium import st_folium

        mapa_op = folium.Map(location=[df_filtrado['latitud'].mean(), df_filtrado['longitud'].mean()], zoom_start=12)
        cluster = MarkerCluster().add_to(mapa_op)

        for _, row in sin_construccion_alto_avaluo.iterrows():
            folium.Marker(
                location=[row['latitud'], row['longitud']],
                icon=folium.Icon(color='orange'),
                popup=(f"<b>Oportunidad catastral</b><br>"
                       f"Vereda: {row['vereda']}<br>"
                       f"Avalúo: ${row['avaluo_catastral']:,.0f}<br>"
                       f"Área construida: {row['area_construida']} m²")
            ).add_to(cluster)

        for _, row in sin_pago_alto_valor.iterrows():
            folium.Marker(
                location=[row['latitud'], row['longitud']],
                icon=folium.Icon(color='red'),
                popup=(f"<b>Alto impuesto sin pago</b><br>"
                       f"Vereda: {row['vereda']}<br>"
                       f"Impuesto: ${row['valor_impuesto_a_pagar']:,.0f}")
            ).add_to(cluster)

        st.markdown("### Mapa de oportunidades de gestión catastral")
        st_folium(mapa_op, width=700, height=500)

        # Tabla de oportunidades
        st.markdown("### 🧾 Lista de predios con oportunidades catastrales")
        oportunidades = pd.concat([sin_construccion_alto_avaluo, sin_pago_alto_valor]).drop_duplicates()
        st.dataframe(oportunidades[['codigo_igac', 'vereda', 'avaluo_catastral', 'area_construida', 'valor_impuesto_a_pagar']].reset_index(drop=True))



    
    with tabs[3]:
        st.header("4. Estrategias de cobro")
        st.markdown("Este módulo presenta una lista priorizada de predios en mora y un mapa para focalizar acciones de cobro.")

        # Filtrar predios en mora
        en_mora = df_filtrado[df_filtrado['pago_impuesto_predial'].str.lower() == 'no'].copy()
        en_mora = en_mora.sort_values(by='valor_impuesto_a_pagar', ascending=False)

        # Tabla priorizada
        st.markdown("### 🔢 Top predios con mayor impuesto en mora")
        st.dataframe(en_mora[['vereda', 'sector', 'destino_economico_predio', 'avaluo_catastral', 'valor_impuesto_a_pagar', 'recaudo_predial']].head(10))

        # Mapa de predios en mora ordenados
        import folium
        from folium.plugins import MarkerCluster
        from streamlit_folium import st_folium

        mapa_cobro = folium.Map(location=[en_mora['latitud'].mean(), en_mora['longitud'].mean()], zoom_start=12)
        cluster = MarkerCluster().add_to(mapa_cobro)

        for _, row in en_mora.iterrows():
            folium.Marker(
                location=[row['latitud'], row['longitud']],
                icon=folium.Icon(color='purple'),
                popup=(f"<b>Predio en mora</b><br>"
                       f"Vereda: {row['vereda']}<br>"
                       f"Avalúo: ${row['avaluo_catastral']:,.0f}<br>"
                       f"Impuesto: ${row['valor_impuesto_a_pagar']:,.0f}")
            ).add_to(cluster)

        st.markdown("### 🗺️ Mapa de predios con mayor impuesto en mora")
        st_folium(mapa_cobro, width=700, height=500)

        # Propuestas de campañas
        st.markdown("### 🧠 Propuestas de campañas de cobro persuasivo")
        st.markdown("""
        1. **Campaña de acuerdos de pago flexibles**: contacto directo con los 50 predios de mayor deuda.
        2. **Condonación parcial de intereses por pago anticipado** en los próximos 30 días.
        3. **Publicación de ranking positivo de cumplimiento tributario** por vereda.
        4. **Envío masivo de notificaciones personalizadas** (correo, físico y WhatsApp).
        5. **Jornadas de conciliación y atención personalizada** en barrios con alta morosidad.
        """)


    
    with tabs[4]:
        st.header("5. Simulación de escenarios de recaudo")
        st.markdown("Este módulo permite visualizar cuánto se podría recaudar si aumentara la cobertura de pago en diferentes niveles.")

        # Predios en mora
        morosos = df_filtrado[df_filtrado['pago_impuesto_predial'].str.lower() == 'no'].copy()
        total_morosidad = morosos['valor_impuesto_a_pagar'].sum()

        st.markdown(f"**Total en mora (actual):** ${total_morosidad:,.0f}")

        # Escenarios simulados
        niveles = [10, 30, 50, 100]
        simulaciones = {n: total_morosidad * (n / 100) for n in niveles}

        st.markdown("### 💰 Posibles incrementos en recaudo")
        for n in niveles:
            st.markdown(f"- {n}% de cobertura adicional: **${simulaciones[n]:,.0f}**")

        # Mapa interactivo de escenarios (colores por escenario teórico)
        import folium
        from streamlit_folium import st_folium

        mapa_sim = folium.Map(location=[morosos['latitud'].mean(), morosos['longitud'].mean()], zoom_start=12)

        color_map = {
            10: 'lightblue',
            30: 'blue',
            50: 'darkblue',
            100: 'navy'
        }

        for nivel in niveles:
            top_n = int(len(morosos) * (nivel / 100))
            subset = morosos.sort_values(by='valor_impuesto_a_pagar', ascending=False).head(top_n)

            for _, row in subset.iterrows():
                folium.CircleMarker(
                    location=[row['latitud'], row['longitud']],
                    radius=6,
                    color=color_map[nivel],
                    fill=True,
                    fill_color=color_map[nivel],
                    fill_opacity=0.5,
                    popup=(f"<b>Simulación {nivel}%</b><br>"
                           f"Impuesto: ${row['valor_impuesto_a_pagar']:,.0f}")
                ).add_to(mapa_sim)

        st.markdown("### 🗺️ Mapa de escenarios simulados de recaudo")
        st_folium(mapa_sim, width=700, height=500)

        # Tabla de predios por escenario
        st.markdown("### 🧾 Lista de predios en escenarios simulados")
        simulados = pd.concat([
            morosos.sort_values(by='valor_impuesto_a_pagar', ascending=False).head(int(len(morosos) * (nivel / 100)))
            for nivel in niveles
        ]).drop_duplicates()
        st.dataframe(simulados[['codigo_igac', 'vereda', 'valor_impuesto_a_pagar', 'latitud', 'longitud']].reset_index(drop=True))



    
    with tabs[5]:
        st.header("6. Mapa geoespacial por niveles de riesgo tributario")
        st.markdown("Este módulo calcula y visualiza el riesgo tributario compuesto por predio, considerando aspectos fiscales, catastrales y de comportamiento.")

        df_riesgo = df_filtrado.copy()

        # Riesgo fiscal
        df_riesgo['riesgo_fiscal'] = pd.qcut(df_riesgo['valor_impuesto_a_pagar'], 5, labels=False, duplicates='drop') + 1
        df_riesgo.loc[df_riesgo['pago_impuesto_predial'].str.lower() == 'si', 'riesgo_fiscal'] = 1

        # Riesgo catastral
        df_riesgo['riesgo_catastral'] = 1
        sin_construccion = (df_riesgo['area_construida'] == 0) & (df_riesgo['avaluo_catastral'] > df_riesgo['avaluo_catastral'].median())
        bajo_construido_alto_avaluo = (df_riesgo['area_construida'] < df_riesgo['area_construida'].quantile(0.2)) & (df_riesgo['avaluo_catastral'] > df_riesgo['avaluo_catastral'].quantile(0.6))
        df_riesgo.loc[sin_construccion, 'riesgo_catastral'] = 5
        df_riesgo.loc[bajo_construido_alto_avaluo, 'riesgo_catastral'] = 3

        # Riesgo comportamental
        df_riesgo['riesgo_comportamental'] = 1
        df_riesgo.loc[
            (df_riesgo['pago_impuesto_predial'].str.lower() == 'no') & (df_riesgo['financiacion_impuesto_predial'].str.lower() == 'no'),
            'riesgo_comportamental'
        ] = 5
        df_riesgo.loc[
            (df_riesgo['pago_impuesto_predial'].str.lower() == 'no') & (df_riesgo['financiacion_impuesto_predial'].str.lower() == 'si'),
            'riesgo_comportamental'
        ] = 3

        # Puntaje compuesto (promedio ponderado)
        df_riesgo['riesgo_total'] = (
            0.5 * df_riesgo['riesgo_fiscal'] +
            0.3 * df_riesgo['riesgo_catastral'] +
            0.2 * df_riesgo['riesgo_comportamental']
        )

        # Clasificar en quintiles de riesgo total
        df_riesgo['nivel_riesgo'] = pd.qcut(df_riesgo['riesgo_total'], 5, labels=['Muy bajo', 'Bajo', 'Medio', 'Alto', 'Muy alto'], duplicates='drop')

        # Mapa
        import folium
        from streamlit_folium import st_folium

        mapa_riesgo = folium.Map(location=[df_riesgo['latitud'].mean(), df_riesgo['longitud'].mean()], zoom_start=12)
        color_map = {
            'Muy bajo': 'green',
            'Bajo': 'lightgreen',
            'Medio': 'orange',
            'Alto': 'red',
            'Muy alto': 'darkred'
        }

        for _, row in df_riesgo.iterrows():
            folium.CircleMarker(
                location=[row['latitud'], row['longitud']],
                radius=7,
                color=color_map[row['nivel_riesgo']],
                fill=True,
                fill_color=color_map[row['nivel_riesgo']],
                fill_opacity=0.6,
                popup=(f"<b>Riesgo: {row['nivel_riesgo']}</b><br>"
                       f"Avalúo: ${row['avaluo_catastral']:,.0f}<br>"
                       f"Impuesto: ${row['valor_impuesto_a_pagar']:,.0f}")
            ).add_to(mapa_riesgo)

        st.markdown("### 🗺️ Mapa de riesgo tributario compuesto")
        st_folium(mapa_riesgo, width=700, height=500)

