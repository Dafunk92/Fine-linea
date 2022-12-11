import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import datetime as datetime
from PIL import Image
from plotly.subplots import make_subplots
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

st.set_page_config(page_title='Linea P2',
                   page_icon=':bar_chart:',
                   layout='wide')

df = pd.read_excel(
    io = os.path.join(__location__,'Fine_linea_streamlit.xlsx'),
    engine = 'openpyxl',
    sheet_name = 'Worksheet',
    skiprows = 0,
    usecols = 'A:F',
    nrows = 334,

)
df['data'] = pd.to_datetime(df['data'])

# -- Sidebar --
logo_trigano_path= os.path.join(__location__, '.streamlit\Triganovanlogo.png')
logo_trigano = Image.open(logo_trigano_path)
st.sidebar.image(logo_trigano, use_column_width=True)
df['autocontrollo'] = df['autocontrollo'].fillna('no')




st.sidebar.header('Filtri selezionati:')

#modello = st.radio('Seleziona modelli da analizzare', ('Tutti', 'Entry', 'Easy'))
#    
#    
#if modello == 'Tutti':
#        st.write(df)
#elif modello == 'Entry':
#        st.write(df[df['modello'].str.endswith('entry')])
#elif modello == 'Easy':
#        st.write(df[df['modello'].str.endswith('easy')])

    





with st.sidebar:
   container= st.container()
   


   tutti_modelli = st.checkbox('Seleziona tutti')
   modelli_entry = st.checkbox('Modelli entry')
   modelli_easy = st.checkbox('Modelli easy')
   if tutti_modelli:
    modello = container.multiselect('Seleziona uno o più modelli:',
        ['V2 entry', 'V5 entry','Tw entry','K2 entry', 'V2 easy','V5 easy','Tw easy','K2 easy','V4 easy'],
        ['V2 entry', 'V5 entry','Tw entry','K2 entry', 'V2 easy','V5 easy','Tw easy','K2 easy','V4 easy'])

   elif modelli_entry:
    modello = container.multiselect('Seleziona uno o più modelli:',
        ['V2 entry', 'V5 entry','Tw entry','K2 entry'],['V2 entry', 'V5 entry','Tw entry','K2 entry'])
    
   elif modelli_easy:
    modello = container.multiselect('Seleziona uno o più modelli:',
        ['V2 easy','V5 easy','Tw easy','K2 easy','V4 easy'],['V2 easy','V5 easy','Tw easy','K2 easy','V4 easy'] )


   else:
        modello = container.multiselect('Seleziona uno o più modelli:', ['V2 entry', 'V5 entry','Tw entry','K2 entry', 'V2 easy','V5 easy','Tw easy','K2 easy','V4 easy'])














#modello = st.sidebar.multiselect(
#    'Seleziona modello:',
#    options=df['modello'].unique(),
#    default=df['modello'].unique()
#)

autocontrollo = st.sidebar.multiselect(
    'Veicolo in autocontrollo?',
    options=df['autocontrollo'].unique(),
    default=df['autocontrollo'].unique()
             
)

#giorno_produzione = st.sidebar.multiselect(
#    'Giorno di produzione',
#    options=df['data'].sort_values().unique(),
#   default=df['data'].sort_values().unique()
#)

data_min_side = df['data'].min()
data_max_side = df['data'].max()


#calendario_inizio = st.sidebar.date_input(
#    "Giorno inizio",
#    data_min_side,
#    min_value=data_min_side,
#)
#
#calendario_fine = st.sidebar.date_input(
#    "Giorno Fine",
#    data_max_side,
#    max_value=data_max_side
#)
min_date = df['data'].min()
max_date = df['data'].max()
coppia_date = st.sidebar.date_input('Seleziona range di date', (min_date, max_date), min_value=min_date , max_value=max_date)
inizio_intervallo = coppia_date[0]
fine_intervallo = coppia_date[1]


#date_slider = df['data'].sort_values().unique()
#with st.sidebar:
#   data_slider_inizio, data_slider_fine = st.select_slider('Seleziona range di date:', options=date_slider, value=(data_min_side, data_max_side))


df_selection = df.query(
    'modello == @modello & autocontrollo == @autocontrollo & data >= @inizio_intervallo & data <= @fine_intervallo' , 
)


if len(df_selection) > 0:
    data_min_df_selection = df_selection['data'].min()
    data_max_df_selection = df_selection['data'].max()
    if str(data_min_df_selection) != 'NaT' and str(data_max_df_selection) != 'NaT':
    
        
        data_min = datetime.datetime.strftime(data_min_df_selection, format = '%d/%m/%Y')
        data_max = datetime.datetime.strftime(data_max_df_selection, format = '%d/%m/%Y')
        st.title(':bar_chart:' f'Dashboard produzione P2 Linea Verde dal {data_min} al {data_max}')
    
    
    
    
    
    
    
  
    # ---- MainPage ----
    
    #st.title(':bar_chart:' f'Dashboard produzione P2 Linea Verde dal {data_min} al {data_max}')
    st.markdown('##')
    
    
    # ----- Modelli -----
    V2_entry = df_selection[df_selection['modello'] == 'V2 entry']
    V5_entry = df_selection[df_selection['modello'] == 'V5 entry']
    V5_easy = df_selection[df_selection['modello'] == 'V5 easy']
    Tw_entry = df_selection[df_selection['modello'] == 'Tw entry']
    V2_easy = df_selection[df_selection['modello'] == 'V2 easy']
    Tw_easy = df_selection[df_selection['modello'] == 'Tw easy']
    K2_entry = df_selection[df_selection['modello'] == 'K2 entry']
    V4_easy = df_selection[df_selection['modello'] == 'V4 easy']
    K2_easy = df_selection[df_selection['modello'] == 'K2 easy']
    
    #--- Autocontrollo ---
    
    veicoli_autocontrollo = df_selection['autocontrollo'].value_counts().get('si',0)
    totale_veicoli = df_selection['telaio'].count()
    
    #---Pre-ripristino---
    
    
    df_veicoli_prerip = df_selection[~df_selection['min_rip_linea'].isnull()]
    
    
    # TOP KPI's
    
    
    media_tempo_ripristino_V2_entry = V2_entry['min_prev_rip'].mean()
    media_tempo_ripristino_V5_entry = V5_entry['min_prev_rip'].mean()
    media_tempo_ripristino_V5_easy = V5_easy['min_prev_rip'].mean()
    media_tempo_ripristino_Tw_entry = Tw_entry['min_prev_rip'].mean()
    media_tempo_ripristino_V2_easy = V2_easy['min_prev_rip'].mean()
    media_tempo_ripristino_Tw_easy = Tw_easy['min_prev_rip'].mean()
    media_tempo_ripristino_K2_entry = K2_entry['min_prev_rip'].mean()
    media_tempo_ripristino_V4_easy = V4_easy['min_prev_rip'].mean()
    media_tempo_ripristino_K2_easy = K2_easy['min_prev_rip'].mean()
    
    
    quanti_V2_entry = V2_entry['modello'].count()
    quanti_V5_entry = V5_entry['modello'].count()
    quanti_V5_easy = V5_easy['modello'].count()
    quanti_Tw_entry = Tw_entry['modello'].count()
    quanti_V2_easy = V2_easy['modello'].count()
    quanti_Tw_easy = Tw_easy['modello'].count()
    quanti_K2_entry = K2_entry['modello'].count()
    quanti_V4_easy = V4_easy['modello'].count()
    quanti_K2_easy = K2_easy['modello'].count()
    
    quanti_V2_entry_auto = V2_entry['autocontrollo'].count()
    quanti_V5_entry_auto = V5_entry['autocontrollo'].count()
    quanti_V5_easy_auto = V5_easy['autocontrollo'].count()
    quanti_Tw_entry_auto = Tw_entry['autocontrollo'].count()
    quanti_V2_easy_auto = V2_easy['autocontrollo'].count()
    quanti_Tw_easy_auto = Tw_easy['autocontrollo'].count()
    quanti_K2_entry_auto = K2_entry['autocontrollo'].count()
    quanti_V4_easy_auto = V4_easy['autocontrollo'].count()
    quanti_K2_easy_auto = K2_easy['autocontrollo'].count()
    
    
    #--- Colonne ---
    
    # --- Bar chart tempo medio per modello ---
    
    tempo_medio_ripristino_per_modello = df_selection.groupby('modello')['min_prev_rip'].mean().sort_values()
    
    grafico = px.bar(tempo_medio_ripristino_per_modello,
         x=tempo_medio_ripristino_per_modello.index, 
         y='min_prev_rip',
         title = '<b> Tempo medio preventivato per modello </b>',
         color_discrete_sequence=['#0083B8'] * len(tempo_medio_ripristino_per_modello),
         template='plotly_white',
    )
    
    grafico.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False)
    
    )
    
    
    ordine_media_rip_prev_marca = df_selection.groupby('modello')['min_prev_rip'].mean().sort_values().index
    boxplot = px.box(data_frame=df_selection,
         x='modello',
         y='min_prev_rip', 
         title='<b> Boxplot </b>', 
         color_discrete_sequence=['#0083B8'] * len(tempo_medio_ripristino_per_modello),
         template='plotly_white'
    )
    
    boxplot.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False)
    )
    boxplot.update_xaxes(categoryorder='array', categoryarray=ordine_media_rip_prev_marca)
    
    
    
    df_rip_medio = df_selection.groupby('data')["min_prev_rip"].mean()
    linechart = px.line(df_rip_medio, x=df_rip_medio.index, y='min_prev_rip', title="Tempo di ripristino medio per giorno", markers=True)
    linechart.add_hline(y=60, annotation_text='target', line_dash='dash', line_color='red')
    linechart.update_traces(textposition='top center')
    linechart.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False),
        yaxis_range=[0, 160]
    )
    linechart.update_traces(textposition='top center')
    
    
    
    # ---Hide streamlit style ---
    hide_st_style = '''
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                '''
    st.markdown(hide_st_style, unsafe_allow_html=True) 
    
    
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([' Dataframe','Media ripristino preventivato', 'Grafico', 'Vista generale', "Tempo ripristino medio per giorno", 'Pre-ripristino in Linea'])
    
    with tab1:
        st.header(':page_facing_up: Dataframe produzione P2 Linea Verde')
        st.dataframe(df_selection)
    
    
    with tab2:
        st.header(':bar_chart: Media tempo di ripristino preventivato per modello:')
        st.subheader(f'V2 entry {media_tempo_ripristino_V2_entry:.2f} Minuti')
        st.subheader(f'V5 entry {media_tempo_ripristino_V5_entry:.2f} Minuti')
        st.subheader(f'V5 easy {media_tempo_ripristino_V5_easy:.2f} Minuti')
        st.subheader(f'Tw entry {media_tempo_ripristino_Tw_entry:.2f} Minuti')
        st.subheader(f'V2 easy {media_tempo_ripristino_V2_easy:.2f} Minuti')
        st.subheader(f'Tw easy {media_tempo_ripristino_Tw_easy:.2f} Minuti')
        st.subheader(f'K2 entry {media_tempo_ripristino_K2_entry:.2f} Minuti')
        st.subheader(f'V4 easy {media_tempo_ripristino_V4_easy:.2f} Minuti')
        st.subheader(f'K2 easy {media_tempo_ripristino_K2_easy:.2f} Minuti')
    
    with tab3:
        st.header(':chart_with_upwards_trend: Analisi tempo di ripristino per modello')
        st.plotly_chart(boxplot)
    
    
    with tab4:
        st.header(' :notebook: Vista generale')
        left_column, middle_column, right_column = st.columns(3)
        with left_column:
            st.subheader('Media tempo di ripristino preventivato per modello:')
            st.subheader(f'V2 entry {media_tempo_ripristino_V2_entry:.2f} Minuti')
            st.subheader(f'V5 entry {media_tempo_ripristino_V5_entry:.2f} Minuti')
            st.subheader(f'V5 easy {media_tempo_ripristino_V5_easy:.2f} Minuti')
            st.subheader(f'Tw entry {media_tempo_ripristino_Tw_entry:.2f} Minuti')
            st.subheader(f'V2 easy {media_tempo_ripristino_V2_easy:.2f} Minuti')
            st.subheader(f'Tw easy {media_tempo_ripristino_Tw_easy:.2f} Minuti')
            st.subheader(f'K2 entry {media_tempo_ripristino_K2_entry:.2f} Minuti')
            st.subheader(f'V4 easy {media_tempo_ripristino_V4_easy:.2f} Minuti')
            st.subheader(f'K2 easy {media_tempo_ripristino_K2_easy:.2f} Minuti')
    
        with middle_column:
            st.subheader('Quanti telai per modello sono stati prodotti:')
            st.subheader(f'{quanti_V2_entry}')
            st.subheader(f'{quanti_V5_entry}')
            st.subheader(f'{quanti_V5_easy}')
            st.subheader(f'{quanti_Tw_entry}')
            st.subheader(f'{quanti_V2_easy}')
            st.subheader(f'{quanti_Tw_easy}')
            st.subheader(f'{quanti_K2_entry}')
            st.subheader(f'{quanti_V4_easy}')
            st.subheader(f'{quanti_K2_easy}')
    
        with right_column:
            st.subheader('Quanti veicoli prodotti in autocontrollo per modello')
            st.subheader(f'{quanti_V2_entry_auto}')
            st.subheader(f'{quanti_V5_entry_auto}')
            st.subheader(f'{quanti_V5_easy_auto}')
            st.subheader(f'{quanti_Tw_entry_auto}')
            st.subheader(f'{quanti_V2_easy_auto}')
            st.subheader(f'{quanti_Tw_easy_auto}')
            st.subheader(f'{quanti_K2_entry_auto}')
            st.subheader(f'{quanti_V4_easy_auto}')
            st.subheader(f'{quanti_K2_easy_auto}')
    
    
        st.markdown('---')
        st.subheader(f'Nel periodo selezionato sono stati prodotti {totale_veicoli} veicoli di cui {veicoli_autocontrollo} in autocontrollo ')
        st.subheader(f'quindi il {veicoli_autocontrollo / totale_veicoli * 100 :.2f}%')
        
    
    with tab5:
        st.subheader(" :put_litter_in_its_place:Tempo di ripristino medio per giorno")
        st.plotly_chart(linechart)
    
    with tab6:
        st.header(':small_red_triangle: Analisi pre-ripristino fine linea')
        left_column, right_column = st.columns(2)
        with left_column:
           df_rip_medio_prerip = df_selection.groupby('data')["min_rip_linea"].median()
           linechart2 = px.line(df_rip_medio_prerip, x=df_rip_medio_prerip.index, y='min_rip_linea', title="Tempo di ripristino medio preripristino", markers=True)
           linechart2.add_hline(y=60, annotation_text='target', line_dash='dash', line_color='red')
           linechart2.update_traces(textposition='top center')
           linechart2.update_layout(
               plot_bgcolor='rgba(0,0,0,0)',
               xaxis=dict(showgrid=False),
               yaxis_range=[0, 160])
           linechart2.update_traces(textposition='top center')
           st.plotly_chart(linechart2)
        
        with right_column:
            media_minuti_abbattimento = (df_veicoli_prerip['min_prev_rip'] - df_veicoli_prerip['min_rip_linea']).median()
            st.subheader(f'Mediamente il pre-ripristino riduce il tempo di rip di {media_minuti_abbattimento : .1f} minuti')

else:
    st.title('Utilizza la Sidebar per applicare i filtri desiderati.')

    
    
    

    







