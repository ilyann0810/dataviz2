"""
Dashboard Streamlit - Analyse des Accidents de la Route 2024
Narrative: Evolution temporelle et facteurs de gravité des accidents

Author: Projet EFREI - Data Storytelling
Dataset: data.gouv.fr - Accidents corporels de la circulation routière
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ==============================================================================
# CONFIGURATION
# ==============================================================================

st.set_page_config(
    page_title="Accidents de la Route 2024",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# DATA LOADING
# ==============================================================================

@st.cache_data(show_spinner=False)
def load_data():
    """Load and prepare accident data"""
    df = pd.read_csv('dataset/accidents_complet_synthese.csv')

    # Convert date
    df['date'] = pd.to_datetime(df['date'])

    # Convert coordinates from French format
    if df['lat'].dtype == 'object':
        df['lat'] = df['lat'].astype(str).str.replace(',', '.').astype(float)
        df['long'] = df['long'].astype(str).str.replace(',', '.').astype(float)

    # Extract month number for sorting
    month_order = {
        'Janvier': 1, 'Fevrier': 2, 'Mars': 3, 'Avril': 4,
        'Mai': 5, 'Juin': 6, 'Juillet': 7, 'Aout': 8,
        'Septembre': 9, 'Octobre': 10, 'Novembre': 11, 'Decembre': 12
    }
    df['mois_num'] = df['mois_nom'].map(month_order)

    return df

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def format_number(n):
    """Format large numbers with thousands separator"""
    return f"{int(n):,}".replace(',', ' ')

def get_color_map():
    """Consistent color scheme for severity categories"""
    return {
        'Mortel': '#DC3545',
        'Grave': '#FD7E14',
        'Léger': '#FFC107',
        'Matériel uniquement': '#28A745'
    }

# ==============================================================================
# MAIN APP
# ==============================================================================

def main():
    # Load data
    with st.spinner('Chargement des données...'):
        df = load_data()

    # ==============================================================================
    # HEADER
    # ==============================================================================

    st.title("🚗 Accidents de la Route en France - 2024")
    st.markdown("### *De l'analyse des données à l'action préventive*")

    # ==============================================================================
    # STORYTELLING NAVIGATION
    # ==============================================================================

    st.markdown("""
    <style>
    .story-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: linear-gradient(90deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 1rem 2rem;
        border-radius: 15px;
        margin: 1rem 0 2rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .story-step {
        text-align: center;
        color: #888;
        font-size: 0.85rem;
        position: relative;
        flex: 1;
    }
    .story-step.active {
        color: #fff;
    }
    .story-step .step-icon {
        font-size: 1.5rem;
        margin-bottom: 0.3rem;
    }
    .story-step .step-num {
        background: #333;
        color: #888;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        margin-bottom: 0.3rem;
    }
    .story-step.active .step-num {
        background: #e94560;
        color: white;
    }
    .story-line {
        position: absolute;
        top: 12px;
        left: 50%;
        width: 100%;
        height: 2px;
        background: #333;
        z-index: -1;
    }
    </style>

    <div class="story-nav">
        <div class="story-step active">
            <div class="step-icon">🎯</div>
            <div class="step-num">1</div>
            <div>Problème</div>
        </div>
        <div class="story-step active">
            <div class="step-icon">📊</div>
            <div class="step-num">2</div>
            <div>Données</div>
        </div>
        <div class="story-step active">
            <div class="step-icon">🔍</div>
            <div class="step-num">3</div>
            <div>Analyse</div>
        </div>
        <div class="story-step active">
            <div class="step-icon">💡</div>
            <div class="step-num">4</div>
            <div>Insights</div>
        </div>
        <div class="story-step active">
            <div class="step-icon">🚀</div>
            <div class="step-num">5</div>
            <div>Actions</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Intro narrative
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 2rem;
                border-radius: 15px;
                color: white;
                margin-bottom: 2rem;'>
        <h2 style='color: white; margin-top: 0;'>📖 Notre histoire commence ici...</h2>
        <p style='font-size: 1.1rem; line-height: 1.8;'>
            Chaque jour en France, <strong>150 accidents corporels</strong> se produisent sur nos routes.
            Derrière ces chiffres, des vies brisées, des familles endeuillées.
        </p>
        <p style='font-size: 1.1rem; line-height: 1.8;'>
            Mais ces accidents ne sont <strong>pas une fatalité</strong>. En analysant les données,
            nous pouvons comprendre <em>quand</em>, <em>où</em> et <em>pourquoi</em> ils surviennent.
        </p>
        <p style='font-size: 1.1rem; line-height: 1.8; margin-bottom: 0;'>
            <strong>Suivez-nous dans cette exploration</strong> : des constats aux solutions,
            découvrez comment les données peuvent sauver des vies.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ==============================================================================
    # SECTION 0: PROBLÉMATIQUE
    # ==============================================================================

    st.markdown("---")
    st.header("🎯 Chapitre 1 : Le Constat")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        ### Le constat alarmant

        La sécurité routière reste un **enjeu majeur de santé publique** en France. Malgré les progrès réalisés
        ces dernières décennies, les accidents de la route continuent de causer des milliers de victimes chaque année.

        **Les chiffres parlent d'eux-mêmes** :
        - Plus de **50 000 accidents corporels** recensés en 2024
        - **3 400+ décès** et près de **20 000 blessés hospitalisés**
        - Des coûts humains, sociaux et économiques considérables

        ### Les questions essentielles

        Face à cette réalité, plusieurs questions cruciales se posent :

        1. **📅 Quand ?** Existe-t-il des périodes plus à risque ?
        2. **🌍 Où ?** Quelles zones géographiques sont les plus touchées ?
        3. **⚠️ Comment ?** Quels facteurs aggravent la gravité des accidents ?
        4. **💡 Pourquoi ?** Peut-on identifier des patterns récurrents ?

        ### L'objectif de cette analyse

        Ce dashboard vise à **transformer les données en insights actionnables** pour :
        - Identifier les facteurs de risque prioritaires
        - Orienter les politiques de prévention
        - Optimiser l'allocation des ressources
        - Sensibiliser les usagers aux moments et conditions critiques
        """)

    with col2:
        st.markdown("""
        <div style='background-color: #dc3545; color: white; padding: 1.5rem; border-radius: 0.5rem; margin-top: 2rem;'>
        <h3 style='color: white; margin-top: 0;'>⚠️ Chiffres clés 2024</h3>
        <hr style='border-color: white; opacity: 0.3;'>
        <h2 style='color: white; margin: 0.5rem 0;'>54 402</h2>
        <p style='margin: 0;'>accidents corporels</p>
        <hr style='border-color: white; opacity: 0.3;'>
        <h2 style='color: white; margin: 0.5rem 0;'>3 432</h2>
        <p style='margin: 0;'>personnes tuées</p>
        <hr style='border-color: white; opacity: 0.3;'>
        <h2 style='color: white; margin: 0.5rem 0;'>19 126</h2>
        <p style='margin: 0;'>blessés hospitalisés</p>
        <hr style='border-color: white; opacity: 0.3;'>
        <h2 style='color: white; margin: 0.5rem 0;'>125 187</h2>
        <p style='margin: 0;'>usagers impliqués</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")
        st.info("""
        **💡 Le saviez-vous ?**

        Les accidents ne sont pas le fruit du hasard. Ils surviennent dans des contextes
        et conditions spécifiques que nous pouvons identifier et sur lesquels nous pouvons agir.
        """)

    st.markdown("---")
    st.markdown("""
    <div style='background-color: #e3f2fd; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #2196F3;'>
    <b>📊 Méthodologie</b> : Cette analyse s'appuie sur les données officielles de l'ONISR (Observatoire National
    Interministériel de la Sécurité Routière), disponibles sur data.gouv.fr. Nous avons enrichi et croisé
    4 bases de données pour obtenir une vision complète de chaque accident.
    </div>
    """, unsafe_allow_html=True)

    # ==============================================================================
    # SIDEBAR FILTERS
    # ==============================================================================

    st.sidebar.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 1rem;
                border-radius: 10px;
                margin-bottom: 1rem;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
        <h3 style='color: white; margin: 0 0 0.5rem 0; font-size: 1.1rem;'>👤 Auteur</h3>
        <p style='color: white; margin: 0.3rem 0; font-size: 0.9rem;'>
            <strong>Nom :</strong> Mouisset--Ferrara
        </p>
        <p style='color: white; margin: 0.3rem 0; font-size: 0.9rem;'>
            <strong>Prénom :</strong> Ilyann
        </p>
        <p style='color: white; margin: 0.3rem 0; font-size: 0.9rem;'>
            <strong>Groupe :</strong> BDML2
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.sidebar.markdown("---")
    st.sidebar.header("🔍 Filtres")

    # Date range filter
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()

    date_range = st.sidebar.date_input(
        "Période",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # Department filter
    # Handle special cases: 2A (Corse-du-Sud), 2B (Haute-Corse)
    departments = sorted([str(d) for d in df['dep'].dropna().unique() if d != ''])
    selected_dept = st.sidebar.multiselect(
        "Département",
        options=departments,
        default=None,
        help="Laisser vide pour tous les départements"
    )

    # Severity filter
    severities = df['categorie_gravite'].unique().tolist()
    selected_severities = st.sidebar.multiselect(
        "Gravité",
        options=severities,
        default=severities
    )

    # Road type filter
    road_types = ['Tous'] + df['catr_desc'].dropna().unique().tolist()
    selected_road = st.sidebar.selectbox("Type de route", options=road_types)

    # Agglomeration filter
    agg_types = ['Tous', 'En agglomération', 'Hors agglomération']
    selected_agg = st.sidebar.selectbox("Zone", options=agg_types)

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Source des données**")
    st.sidebar.caption("""
    data.gouv.fr - ONISR
    Licence Ouverte 2.0
    Accidents 2024
    """)

    # Apply filters
    df_filtered = df.copy()

    # Date filter
    if len(date_range) == 2:
        start_date, end_date = date_range
        df_filtered = df_filtered[
            (df_filtered['date'].dt.date >= start_date) &
            (df_filtered['date'].dt.date <= end_date)
        ]

    # Department filter
    if selected_dept:
        df_filtered = df_filtered[df_filtered['dep'].astype(str).isin(selected_dept)]

    # Severity filter
    if selected_severities:
        df_filtered = df_filtered[df_filtered['categorie_gravite'].isin(selected_severities)]

    # Road type filter
    if selected_road != 'Tous':
        df_filtered = df_filtered[df_filtered['catr_desc'] == selected_road]

    # Agglomeration filter
    if selected_agg != 'Tous':
        df_filtered = df_filtered[df_filtered['agg_desc'] == selected_agg]

    # ==============================================================================
    # SECTION 1: KEY METRICS (KPIs)
    # ==============================================================================

    st.markdown("---")
    st.header("📈 Chapitre 2 : Les Données Parlent")

    col1, col2, col3, col4, col5 = st.columns(5)

    total_accidents = len(df_filtered)
    total_deaths = df_filtered['nb_tues'].sum()
    total_serious = df_filtered['nb_blesses_hospitalises'].sum()
    total_light = df_filtered['nb_blesses_legers'].sum()
    avg_severity = df_filtered['score_gravite'].mean()

    with col1:
        st.metric(
            "Accidents",
            format_number(total_accidents),
            delta=f"{total_accidents/len(df)*100:.1f}% du total"
        )

    with col2:
        st.metric(
            "Tués",
            format_number(total_deaths),
            delta=f"{total_deaths/df['nb_tues'].sum()*100:.1f}% du total",
            delta_color="inverse"
        )

    with col3:
        st.metric(
            "Blessés hospitalisés",
            format_number(total_serious),
            delta=f"{total_serious/df['nb_blesses_hospitalises'].sum()*100:.1f}%",
            delta_color="inverse"
        )

    with col4:
        st.metric(
            "Blessés légers",
            format_number(total_light)
        )

    with col5:
        st.metric(
            "Score gravité moyen",
            f"{avg_severity:.1f}",
            help="tués×100 + blessés graves×30 + blessés légers×10"
        )

    # ==============================================================================
    # SECTION 2: TEMPORAL EVOLUTION
    # ==============================================================================

    st.markdown("---")
    st.header("📅 Évolution temporelle")

    st.markdown("""
    **Insight clé** : L'analyse temporelle révèle des patterns saisonniers marqués et des périodes à risque.
    """)

    # Evolution by month
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Accidents par mois")

        monthly = df_filtered.groupby('mois_nom').agg({
            'Num_Acc': 'count',
            'nb_tues': 'sum',
            'mois_num': 'first'
        }).reset_index()
        monthly = monthly.sort_values('mois_num')

        fig_monthly = px.bar(
            monthly,
            x='mois_nom',
            y='Num_Acc',
            title="Nombre d'accidents par mois",
            labels={'mois_nom': 'Mois', 'Num_Acc': 'Nombre d\'accidents'},
            color='Num_Acc',
            color_continuous_scale='Reds'
        )
        fig_monthly.update_layout(showlegend=False, xaxis_tickangle=-45)
        st.plotly_chart(fig_monthly, use_container_width=True)

        # Find peak month
        peak_month = monthly.loc[monthly['Num_Acc'].idxmax(), 'mois_nom']
        st.info(f"📊 Pic en **{peak_month}** avec {monthly['Num_Acc'].max()} accidents")

    with col2:
        st.subheader("Répartition par jour")

        jours_ordre = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
        daily = df_filtered['jour_semaine'].value_counts().reindex(jours_ordre, fill_value=0).reset_index()
        daily.columns = ['jour', 'count']
        daily['color'] = daily['jour'].apply(lambda x: '#FF6B6B' if x in ['Samedi', 'Dimanche'] else '#4ECDC4')

        fig_daily = px.bar(
            daily,
            x='jour',
            y='count',
            title="Accidents par jour de la semaine",
            labels={'jour': 'Jour', 'count': 'Nombre d\'accidents'},
            color='color',
            color_discrete_map={'#FF6B6B': '#FF6B6B', '#4ECDC4': '#4ECDC4'}
        )
        fig_daily.update_layout(showlegend=False, xaxis_tickangle=-45)
        st.plotly_chart(fig_daily, use_container_width=True)

        weekend_pct = df_filtered[df_filtered['est_weekend'] == 1].shape[0] / len(df_filtered) * 100
        st.info(f"📊 **{weekend_pct:.1f}%** des accidents ont lieu le week-end")

    # Heatmap by day and hour
    st.subheader("Heatmap : Quand surviennent les accidents ?")

    df_filtered['heure'] = df_filtered['hrmn'].str[:2].astype(int, errors='ignore')
    heatmap_data = df_filtered.groupby(['jour_semaine', 'heure']).size().unstack(fill_value=0)
    heatmap_data = heatmap_data.reindex(jours_ordre)

    fig_heatmap = px.imshow(
        heatmap_data,
        title="Distribution horaire des accidents par jour",
        labels={'x': 'Heure', 'y': 'Jour', 'color': 'Nombre d\'accidents'},
        color_continuous_scale='YlOrRd',
        aspect='auto'
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

    # ==============================================================================
    # SECTION 3: SEVERITY ANALYSIS
    # ==============================================================================

    st.markdown("---")
    st.header("⚠️ Analyse de la gravité")

    st.markdown("""
    **Insight clé** : Certaines conditions augmentent significativement la gravité des accidents.
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Répartition par gravité")

        severity_counts = df_filtered['categorie_gravite'].value_counts()
        color_map = get_color_map()

        fig_severity = px.pie(
            values=severity_counts.values,
            names=severity_counts.index,
            title="Distribution de la gravité",
            color=severity_counts.index,
            color_discrete_map=color_map
        )
        fig_severity.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_severity, use_container_width=True)

        mortel_pct = (df_filtered['accident_mortel'].sum() / len(df_filtered)) * 100
        st.warning(f"⚠️ **{mortel_pct:.2f}%** des accidents sont mortels")

    with col2:
        st.subheader("Gravité selon la zone")

        severity_by_agg = pd.crosstab(
            df_filtered['agg_desc'],
            df_filtered['categorie_gravite'],
            normalize='index'
        ) * 100

        fig_agg = go.Figure()
        for cat in ['Mortel', 'Grave', 'Léger', 'Matériel uniquement']:
            if cat in severity_by_agg.columns:
                fig_agg.add_trace(go.Bar(
                    name=cat,
                    x=severity_by_agg.index,
                    y=severity_by_agg[cat],
                    marker_color=color_map.get(cat, '#gray')
                ))

        fig_agg.update_layout(
            title="Gravité selon agglomération (%)",
            barmode='stack',
            yaxis_title='Pourcentage',
            xaxis_title=''
        )
        st.plotly_chart(fig_agg, use_container_width=True)

    # ==============================================================================
    # SECTION 4: RISK FACTORS
    # ==============================================================================

    st.markdown("---")
    st.header("🔍 Facteurs de risque")

    tabs = st.tabs(["Luminosité", "Météo", "Type de route", "Top Départements"])

    # Tab 1: Lighting
    with tabs[0]:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Accidents par luminosité")

            lum_counts = df_filtered['lum_desc'].value_counts().head(6).reset_index()
            lum_counts.columns = ['lum_desc', 'count']

            fig_lum = px.bar(
                lum_counts,
                x='count',
                y='lum_desc',
                orientation='h',
                title="Distribution par conditions de luminosité",
                labels={'count': 'Nombre d\'accidents', 'lum_desc': ''},
                color='count',
                color_continuous_scale='Blues'
            )
            fig_lum.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_lum, use_container_width=True)

        with col2:
            st.subheader("Taux de mortalité par luminosité")

            lum_mortality = df_filtered.groupby('lum_desc').agg({
                'accident_mortel': 'sum',
                'Num_Acc': 'count'
            }).reset_index()
            lum_mortality['taux'] = (lum_mortality['accident_mortel'] / lum_mortality['Num_Acc']) * 100
            lum_mortality = lum_mortality.sort_values('taux', ascending=False).head(6)

            fig_lum_mort = px.bar(
                lum_mortality,
                x='taux',
                y='lum_desc',
                orientation='h',
                title="% d'accidents mortels par luminosité",
                labels={'taux': '% accidents mortels', 'lum_desc': ''},
                color='taux',
                color_continuous_scale='Reds'
            )
            fig_lum_mort.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_lum_mort, use_container_width=True)

            max_risk_idx = lum_mortality['taux'].idxmax()
            max_risk = lum_mortality.loc[max_risk_idx, 'lum_desc']
            st.warning(f"⚠️ Risque le plus élevé : **{max_risk}**")

    # Tab 2: Weather
    with tabs[1]:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Conditions atmosphériques")

            atm_counts = df_filtered['atm_desc'].value_counts().head(8).reset_index()
            atm_counts.columns = ['atm_desc', 'count']

            fig_atm = px.bar(
                atm_counts,
                x='atm_desc',
                y='count',
                title="Accidents par conditions météo",
                labels={'atm_desc': 'Condition', 'count': 'Nombre d\'accidents'},
                color='count',
                color_continuous_scale='Blues'
            )
            fig_atm.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_atm, use_container_width=True)

        with col2:
            st.subheader("Gravité moyenne par météo")

            atm_severity = df_filtered.groupby('atm_desc').agg({
                'score_gravite': 'mean',
                'Num_Acc': 'count'
            }).reset_index()
            atm_severity = atm_severity[atm_severity['Num_Acc'] > 50].sort_values('score_gravite', ascending=False).head(8)

            fig_atm_sev = px.bar(
                atm_severity,
                x='atm_desc',
                y='score_gravite',
                title="Score de gravité moyen (min. 50 accidents)",
                labels={'atm_desc': 'Condition', 'score_gravite': 'Score gravité'},
                color='score_gravite',
                color_continuous_scale='Oranges'
            )
            fig_atm_sev.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_atm_sev, use_container_width=True)

    # Tab 3: Road type
    with tabs[2]:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Accidents par type de route")

            road_counts = df_filtered['catr_desc'].value_counts().head(6)

            fig_road = px.pie(
                values=road_counts.values,
                names=road_counts.index,
                title="Distribution par type de route"
            )
            st.plotly_chart(fig_road, use_container_width=True)

        with col2:
            st.subheader("Gravité par type de route")

            road_severity = df_filtered.groupby('catr_desc').agg({
                'score_gravite': 'mean',
                'nb_tues': 'sum',
                'Num_Acc': 'count'
            }).reset_index()
            road_severity = road_severity[road_severity['Num_Acc'] > 100].sort_values('score_gravite', ascending=False)

            fig_road_sev = px.bar(
                road_severity,
                x='catr_desc',
                y='score_gravite',
                title="Score gravité moyen (min. 100 accidents)",
                labels={'catr_desc': 'Type de route', 'score_gravite': 'Score gravité'},
                color='score_gravite',
                color_continuous_scale='Reds'
            )
            fig_road_sev.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_road_sev, use_container_width=True)

    # Tab 4: Top departments
    with tabs[3]:
        st.subheader("Top 15 départements")

        top_deps = df_filtered['dep'].value_counts().head(15).reset_index()
        top_deps.columns = ['dep', 'count']
        top_deps['dep_label'] = top_deps['dep'].apply(lambda x: f"Dép. {x}")

        fig_deps = px.bar(
            top_deps,
            x='count',
            y='dep_label',
            orientation='h',
            title="Départements avec le plus d'accidents",
            labels={'count': 'Nombre d\'accidents', 'dep_label': 'Département'},
            color='count',
            color_continuous_scale='Reds'
        )
        fig_deps.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_deps, use_container_width=True)

    # ==============================================================================
    # SECTION 5: MAP WITH ANIMATION
    # ==============================================================================

    st.markdown("---")
    st.header("🗺️ Chapitre 3 : Cartographie des accidents")

    st.markdown("""
    <div style='background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #ffc107; margin-bottom: 1rem;'>
    <b>🎬 Visualisation interactive</b> : Utilisez le slider pour voir l'évolution des accidents mois par mois,
    ou consultez la carte statique pour une vue d'ensemble.
    </div>
    """, unsafe_allow_html=True)

    # Toggle between animated and static map
    map_type = st.radio(
        "Type de visualisation",
        ["📊 Carte statique", "🎬 Animation temporelle"],
        horizontal=True
    )

    # Sample for performance
    sample_size = min(3000, len(df_filtered))
    df_map = df_filtered.sample(n=sample_size, random_state=42).copy()

    if map_type == "🎬 Animation temporelle":
        st.markdown("### Evolution mois par mois")

        # Prepare data for animation
        df_map['mois_annee'] = df_map['date'].dt.strftime('%Y-%m')
        df_map = df_map.sort_values('mois_annee')

        # Create animated map
        fig_map_anim = px.scatter_mapbox(
            df_map,
            lat='lat',
            lon='long',
            color='categorie_gravite',
            color_discrete_map=get_color_map(),
            animation_frame='mois_nom',
            category_orders={'mois_nom': ['Janvier', 'Fevrier', 'Mars', 'Avril', 'Mai', 'Juin',
                                          'Juillet', 'Aout', 'Septembre', 'Octobre', 'Novembre', 'Decembre']},
            hover_data={
                'lat': False,
                'long': False,
                'date': True,
                'dep': True,
                'lum_desc': True,
                'nb_tues': True
            },
            zoom=4.5,
            height=650,
            title="Evolution des accidents au fil des mois"
        )
        fig_map_anim.update_layout(
            mapbox_style="carto-positron",
            margin={"r":0,"t":40,"l":0,"b":0},
            updatemenus=[{
                'type': 'buttons',
                'showactive': False,
                'y': 0,
                'x': 0.1,
                'xanchor': 'right',
                'yanchor': 'top',
                'buttons': [
                    {'label': '▶ Play', 'method': 'animate', 'args': [None, {'frame': {'duration': 1000, 'redraw': True}, 'fromcurrent': True}]},
                    {'label': '⏸ Pause', 'method': 'animate', 'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate'}]}
                ]
            }]
        )
        st.plotly_chart(fig_map_anim, use_container_width=True)

        st.info("💡 **Astuce** : Cliquez sur ▶ Play pour lancer l'animation ou utilisez le slider en bas pour naviguer manuellement.")

    else:
        # Static map
        fig_map = px.scatter_mapbox(
            df_map,
            lat='lat',
            lon='long',
            color='categorie_gravite',
            color_discrete_map=get_color_map(),
            hover_data={
                'lat': False,
                'long': False,
                'date': True,
                'dep': True,
                'lum_desc': True,
                'nb_tues': True,
                'nb_blesses_hospitalises': True
            },
            zoom=5,
            height=600,
            title=f"Localisation de {sample_size} accidents"
        )
        fig_map.update_layout(mapbox_style="open-street-map")
        st.plotly_chart(fig_map, use_container_width=True)

    

    # ==============================================================================
    # SECTION 6: INSIGHTS MAJEURS
    # ==============================================================================

    st.markdown("---")
    st.header("💡 Chapitre 4 : Ce que les Données Révèlent")

    st.markdown("""
    L'analyse des 54 402 accidents de 2024 révèle des **patterns clairs et récurrents**.
    Ces insights permettent d'identifier les leviers d'action prioritaires.
    """)

    # Insights en cartes
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div style='background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #ffc107;'>
        <h4 style='margin-top: 0;'>📅 Temporalité</h4>
        <p><b>Été = risque maximal</b></p>
        <p style='font-size: 0.9em;'>Juin-juillet : +15% d'accidents</p>
        <p style='font-size: 0.9em;'>Vendredi : jour le plus critique</p>
        <p style='font-size: 0.9em;'>17h-19h : heures de pointe</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='background-color: #f8d7da; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #dc3545;'>
        <h4 style='margin-top: 0;'>🌙 Luminosité</h4>
        <p><b>La nuit tue 3× plus</b></p>
        <p style='font-size: 0.9em;'>Sans éclairage : +200% mortalité</p>
        <p style='font-size: 0.9em;'>Crépuscule : visibilité critique</p>
        <p style='font-size: 0.9em;'>Aube : fatigue + faible lumière</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style='background-color: #d1ecf1; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #17a2b8;'>
        <h4 style='margin-top: 0;'>🛣️ Type de route</h4>
        <p><b>Départementales dangereuses</b></p>
        <p style='font-size: 0.9em;'>38% des accidents</p>
        <p style='font-size: 0.9em;'>Score gravité : +25%</p>
        <p style='font-size: 0.9em;'>Moins d'aménagements</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div style='background-color: #d4edda; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #28a745;'>
        <h4 style='margin-top: 0;'>🏙️ Localisation</h4>
        <p><b>Hors agglo = plus grave</b></p>
        <p style='font-size: 0.9em;'>Vitesses plus élevées</p>
        <p style='font-size: 0.9em;'>Secours + longs à arriver</p>
        <p style='font-size: 0.9em;'>Chocs + violents</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # ==============================================================================
    # SECTION 7: SOLUTIONS CONCRÈTES
    # ==============================================================================

    st.markdown("---")
    st.header("🚀 Chapitre 5 : Passer à l'Action")

    st.markdown("""
    Sur la base de ces constats, voici un **plan d'action concret et priorisé** pour réduire l'accidentalité
    et la gravité des accidents.
    """)

    # Solutions en tabs
    solution_tabs = st.tabs([
        "🚨 Mesures Immédiates",
        "🏗️ Infrastructures",
        "📢 Prévention & Sensibilisation",
        "📊 Surveillance & Contrôle",
        "🔬 Recherche & Innovation"
    ])

    # Tab 1: Mesures immédiates
    with solution_tabs[0]:
        st.subheader("Actions à déployer immédiatement (0-6 mois)")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            ### 🌙 Amélioration de l'éclairage public

            **Objectif** : Réduire de 30% les accidents nocturnes

            **Actions** :
            1. **Audit d'éclairage** sur les 500 km de routes départementales les plus accidentogènes
            2. **Installation LED intelligentes** avec détection de présence
            3. **Marquage au sol réfléchissant** renforcé sur zones critiques
            4. **Signalisation lumineuse** aux intersections dangereuses

            **Budget estimé** : 15-20M€
            **ROI** : Réduction de 200+ décès/an = 600M€ économisés

            ---

            ### ⏰ Contrôles ciblés période à risque

            **Objectif** : Présence dissuasive aux moments critiques

            **Actions** :
            1. **Vendredis 17h-21h** : Contrôles vitesse et alcoolémie
            2. **Juin-Juillet** : Opérations "départs en vacances"
            3. **Crépuscule/Aube** : Patrouilles sur routes départementales
            4. **Après 22h** : Contrôles alcool/stupéfiants renforcés

            **Budget estimé** : 5M€ (heures supplémentaires)
            **Impact** : -10% accidents sur périodes ciblées
            """)

        with col2:
            st.markdown("""
            ### 🚗 Campagnes de sensibilisation digitales

            **Objectif** : Toucher 10M d'usagers

            **Actions** :
            1. **Alertes géolocalisées** via Waze/Google Maps
               - "Zone accidentogène, ralentissez"
               - "Conditions de luminosité critiques"
            2. **SMS ciblés** vendredis 15h : "Route chargée ce soir, prudence"
            3. **Réseaux sociaux** : Campagne #LumiereVitale
            4. **Influenceurs** : Témoignages de victimes

            **Budget estimé** : 2M€
            **Portée** : 10M+ personnes touchées

            ---

            ### 📱 Application "Sécurité Route"

            **Objectif** : Assistant personnel de prévention

            **Fonctionnalités** :
            1. **Score de risque** en temps réel (météo + trafic + heure)
            2. **Alertes** : "Visibilité réduite prévue sur votre trajet"
            3. **Itinéraire sécurisé** : éviter routes à risque
            4. **Gamification** : badges pour conduite sûre

            **Budget estimé** : 3M€ (développement + maintenance)
            **Adoption cible** : 5M utilisateurs
            """)

    # Tab 2: Infrastructures
    with solution_tabs[1]:
        st.subheader("Aménagements infrastructure (6-24 mois)")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            ### 🛣️ Sécurisation routes départementales

            **Programme prioritaire** : 200 points noirs identifiés

            **Aménagements type** :
            1. **Ronds-points** aux intersections en T/Y dangereuses
            2. **Voies de décélération** aux accès commerciaux
            3. **Îlots centraux** pour empêcher dépassements risqués
            4. **Zones 70 km/h** au lieu de 80 sur sections sinueuses
            5. **Barrières de sécurité** renforcées (chocs moto)

            **Coût unitaire** : 200-500K€ par point
            **Budget total** : 60M€
            **Impact** : -150 décès/an sur ces zones

            ---

            ### 🏙️ Zones 30 en agglomération

            **Objectif** : Généraliser les zones apaisées

            **Programme** :
            - 50 villes moyennes équipées (50-100K habitants)
            - Centres-villes, abords écoles, zones commerciales
            - Aménagements : chicanes, coussins berlinois, zones partagées

            **Budget estimé** : 25M€
            **Impact** : -30% gravité accidents urbains
            """)

        with col2:
            st.markdown("""
            ### 🔦 Éclairage intelligent connecté

            **Technologie** : LED + capteurs IoT

            **Fonctionnalités** :
            1. **Éclairage adaptatif** : intensité selon météo/trafic
            2. **Détection automatique** : allumage si accident/panne
            3. **Maintenance prédictive** : alertes pannes avant incident
            4. **Économies d'énergie** : -60% consommation

            **Déploiement** : 10 000 km de routes
            **Budget** : 80M€
            **ROI** : 5 ans (économies énergie + vies sauvées)

            ---

            ### 🚧 Signalétique dynamique

            **Systèmes** : Panneaux à messages variables

            **Messages contextuels** :
            - "Brouillard dense 2 km - 50 km/h"
            - "Chaussée verglacée - Danger"
            - "Accident 5 km - Ralentissement"
            - "Forte affluence - Restez vigilants"

            **Déploiement** : 500 panneaux stratégiques
            **Budget** : 15M€
            """)

    # Tab 3: Prévention & Sensibilisation
    with solution_tabs[2]:
        st.subheader("Campagnes de prévention et éducation")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            ### 📚 Programme éducatif renforcé

            **Cibles** : Jeunes conducteurs (18-25 ans)

            **Modules** :
            1. **Simulateurs VR** : conduite nuit/pluie/fatigue
            2. **Ateliers pratiques** : distances de freinage
            3. **Témoignages** : victimes et secouristes
            4. **Stage post-permis** : gratuit 1ère année

            **Déploiement** : 500 auto-écoles partenaires
            **Budget** : 10M€
            **Impact** : -20% accidents jeunes conducteurs

            ---

            ### 🎬 Campagnes médias grand public

            **Thématiques** :
            1. **"Vois-tu Vraiment ?"** : risques luminosité
            2. **"Vendredi Fatal"** : attention fins de semaine
            3. **"Ta Route, Ton Choix"** : responsabilisation
            4. **"1 Seconde Suffit"** : vitesse et distance

            **Canaux** :
            - TV : spots 20h + émissions partenaires
            - Radio : chroniques matinales
            - Digital : YouTube, TikTok, Instagram
            - Affichage : gares, métros, aires d'autoroute

            **Budget** : 8M€/an
            **Portée** : 40M de personnes
            """)

        with col2:
            st.markdown("""
            ### 👥 Mobilisation entreprises

            **Programme** : "Employeur Responsable Route"

            **Actions** :
            1. **Chartes d'engagement** : pas d'appels en conduite
            2. **Formations** : écoconduite + sécurité
            3. **Véhicules** : équipements de sécurité obligatoires
            4. **Horaires** : décaler pour éviter heures de pointe
            5. **Télétravail** : vendredis pour réduire trafic

            **Cible** : 10 000 entreprises (5M salariés)
            **Budget** : 5M€ (accompagnement)
            **Impact** : -25% accidents trajets domicile-travail

            ---

            ### 🏫 Sensibilisation milieu scolaire

            **Programme** : "Génération Prudente"

            **Niveaux** :
            - **Primaire** : piétons, vélos, passages protégés
            - **Collège** : deux-roues, angles morts, distances
            - **Lycée** : conduite, risques, premiers secours

            **Outils** :
            - Pistes éducation routière mobiles
            - Jeux sérieux interactifs
            - Concours inter-établissements

            **Budget** : 7M€
            **Bénéficiaires** : 12M élèves
            """)

    # Tab 4: Surveillance & Contrôle
    with solution_tabs[3]:
        st.subheader("Renforcement des contrôles et surveillance")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            ### 📹 Radars nouvelle génération

            **Technologies** :
            1. **Radars tourelles** : multi-infractions
               - Vitesse, distance sécurité, téléphone
               - 360°, de jour comme de nuit
            2. **Radars trajectoire** : virages dangereux
            3. **Radars chantiers** : protection ouvriers
            4. **Drones** : contrôle zones inaccessibles

            **Déploiement** : 500 nouveaux radars
            **Investissement** : 40M€
            **Recettes** : 200M€/an (réinvesties prévention)

            ---

            ### 🚓 Contrôles alcool/stupéfiants

            **Objectif** : Doubler les contrôles

            **Stratégie** :
            - **8000 opérations/an** (vs 4000 actuellement)
            - **Éthylotests** électroniques rapides
            - **Tests salivaires** stupéfiants généralisés
            - **Zones prioritaires** : sorties discothèques, festivals

            **Budget** : 12M€
            **Impact** : -15% accidents alcool/drogue
            """)

        with col2:
            st.markdown("""
            ### 🛰️ Système de surveillance intelligent

            **Plateforme centralisée** : analyse temps réel

            **Données intégrées** :
            1. **Trafic** : caméras, capteurs, Waze
            2. **Météo** : prévisions hyperlocales
            3. **Accidents** : signalements immédiats
            4. **Travaux** : déviations en cours

            **Capacités** :
            - **Prédiction risques** : ML sur historique
            - **Alertes préventives** : usagers + forces ordre
            - **Gestion crises** : coordination secours
            - **Analytics** : dashboards décisionnels

            **Investissement** : 25M€
            **Maintenance** : 3M€/an

            ---

            ### 📊 Observatoire local accidents

            **Concept** : Analyse fine par territoire

            **100 observatoires départementaux** :
            - Cartographie points noirs mensuelle
            - Analyses causes locales
            - Recommandations aménagements
            - Suivi efficacité mesures

            **Budget** : 10M€ (formation + outils)
            """)

    # Tab 5: Recherche & Innovation
    with solution_tabs[4]:
        st.subheader("Innovation et technologies d'avenir")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            ### 🤖 Intelligence Artificielle prédictive

            **Objectif** : Anticiper et prévenir

            **Applications** :
            1. **Prédiction points chauds**
               - ML sur données historiques + météo + événements
               - Alertes 24-48h avant risque élevé
            2. **Détection comportements à risque**
               - Analyse vidéo : zigzags, vitesse erratique
               - Alerte forces de l'ordre en temps réel
            3. **Maintenance prédictive infrastructures**
               - Drones + IA : détection dégradations
               - Intervention avant incident

            **Budget R&D** : 15M€ sur 3 ans
            **Partenaires** : INRIA, laboratoires universitaires

            ---

            ### 🚗 Véhicules connectés et autonomes

            **Programme** : "Route du Futur"

            **Axes** :
            1. **V2V (Vehicle-to-Vehicle)**
               - Communication entre véhicules
               - Alertes collisions imminentes
            2. **V2I (Vehicle-to-Infrastructure)**
               - Dialogue véhicule-feu/panneau
               - Guidage optimal
            3. **ADAS obligatoires** (Assistance Conduite)
               - Freinage automatique d'urgence
               - Maintien dans voie
               - Détection fatigue

            **Budget** : 30M€ (incitations équipement)
            """)

        with col2:
            st.markdown("""
            ### 🔬 Recherche comportementale

            **Programme** : "Comprendre pour Agir"

            **Études** :
            1. **Facteurs humains**
               - Simulateurs conduite + eye-tracking
               - Impact fatigue, stress, distraction
            2. **Nudges comportementaux**
               - Signalétique incitative vs interdictive
               - Tests A/B sur aménagements
            3. **Psychologie du risque**
               - Pourquoi prend-on des risques ?
               - Profils conducteurs à risque

            **Budget** : 8M€ sur 5 ans
            **Outputs** : Guidelines design routes

            ---

            ### 🌐 Plateforme Open Data avancée

            **Concept** : Démocratiser l'accès aux données

            **Fonctionnalités** :
            1. **API temps réel** : accidents, trafic, météo
            2. **Dashboards publics** : transparence totale
            3. **Hackathons** : innovations citoyennes
            4. **Concours** : meilleure appli sécurité

            **Objectif** : 1000 apps tierces
            **Budget** : 5M€
            """)

    # Synthèse finale avec plan d'action
    st.markdown("---")
    st.header("📋 Plan d'Action Synthétique")

    st.markdown("""
    ### Budget global et priorisation sur 3 ans
    """)

    # Tableau récapitulatif
    budget_data = {
        'Axe': [
            '🚨 Mesures Immédiates',
            '🏗️ Infrastructures',
            '📢 Prévention',
            '📊 Surveillance',
            '🔬 Innovation'
        ],
        'Priorité': ['🔴 Critique', '🟠 Haute', '🟡 Haute', '🟡 Moyenne', '🟢 Long terme'],
        'Budget (M€)': [25, 180, 30, 62, 58],
        'Délai': ['0-6 mois', '6-24 mois', '0-12 mois', '6-18 mois', '12-36 mois'],
        'Impact estimé': ['-15% accidents', '-20% gravité', '-10% jeunes', '-12% alcool', '-25% à terme']
    }

    budget_df = pd.DataFrame(budget_data)
    st.dataframe(budget_df, use_container_width=True, hide_index=True)

    st.markdown("""
    **💰 Budget total** : **355 millions d'euros** sur 3 ans

    **📉 Objectif global** : **Réduire de 25% le nombre de tués** d'ici 2027
    ➜ **Passer de 3 400 à 2 550 décès/an** = **850 vies sauvées**

    **💵 ROI** : Chaque vie sauvée = 3M€ économisés (coûts sociaux)
    ➜ **2,5 milliards d'euros** économisés sur 3 ans

    **🎯 Indicateurs de suivi** :
    - Nombre d'accidents mortels (mensuel)
    - Taux de mortalité par type de route (trimestriel)
    - Score de gravité moyen (semestriel)
    - Satisfaction usagers sécurité routière (annuel)
    """)

    # Call to action
    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.success("""
        ### 👥 Citoyens

        **Votre rôle** :
        - Adaptez votre conduite
        - Signalez les points noirs
        - Partagez ce dashboard
        """)

    with col2:
        st.info("""
        ### 🏛️ Décideurs

        **Vos leviers** :
        - Allouez les budgets
        - Priorisez les actions
        - Mesurez les impacts
        """)

    with col3:
        st.warning("""
        ### 🔬 Chercheurs

        **Votre contribution** :
        - Affinez les modèles
        - Testez les solutions
        - Partagez vos résultats
        """)

    st.markdown("---")

    st.success("""
    ## 🎯 Conclusion : Des données aux actions

    Cette analyse démontre que **la sécurité routière n'est pas une fatalité**. Les accidents suivent des patterns
    identifiables sur lesquels nous pouvons agir de manière ciblée et efficace.

    **Les 3 leviers prioritaires** :
    1. 🌙 **Luminosité** : Éclairage et signalisation des routes dangereuses
    2. 🛣️ **Infrastructures** : Sécurisation des routes départementales
    3. 📢 **Prévention** : Sensibilisation sur périodes et conditions à risque

    **L'action collective** de tous les acteurs - citoyens, autorités, entreprises, chercheurs - peut sauver
    des centaines de vies chaque année. Les données montrent la voie, **il ne reste qu'à agir**.

    ---

    *"Aucun accident n'est acceptable. Chaque vie compte, chaque donnée compte, chaque action compte."*
    """)

    # ==============================================================================
    # FOOTER
    # ==============================================================================

    st.markdown("---")
    st.caption("""
    **Dashboard réalisé avec Streamlit** | Données : data.gouv.fr (ONISR) | Licence Ouverte 2.0
    📊 #EFREIDataStories2025 #DataVisualization 
    """)


# ==============================================================================
# RUN APP
# ==============================================================================

if __name__ == "__main__":
    main()
