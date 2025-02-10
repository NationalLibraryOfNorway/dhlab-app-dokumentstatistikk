import pandas as pd
import dhlab.nbtext as nb
import streamlit as st
import datetime
import matplotlib.pyplot as plt
from PIL import Image
import requests

@st.cache_data(show_spinner = False)
def get_df(frases, title='aftenposten', media='aviser', aggs='year'):

    querystring = " + ".join(['"'+frase+'"' for frase in frases])
    query = {
        'q':querystring,
        'size':1,
        'aggs':aggs,
        'filter':[f'mediatype:{media}', f'title:{title}']
    }
    r = requests.get("https://api.nb.no/catalog/v1/items", params = query)
    aggs = r.json()['_embedded']['aggregations'][0]['buckets']
    return {x['key']:x['count'] for x in aggs}

@st.cache_data( show_spinner = False)
def phrase_plots(phrase_sets, title='aftenposten', media = 'aviser', aggs='year', fra = 1960, til = 2020, step=5):
    df_all = []
    for f in phrase_sets:
        df_all.append(nb.frame(get_df(f, title= title, media=media, aggs=aggs), ', '.join(f)))
    df = pd.concat(df_all, sort=False)
    df.index = df.index.astype(int)
    df = df.sort_index()
    df['bins'] = pd.cut(df.index, range(fra, til, step), precision=0)
    a = df.groupby('bins', observed=False).sum()
    return a



st.set_page_config(layout="wide")

image = Image.open("DHlab_logo_web_en_black.png")
st.sidebar.image(image)

## Sidebar ###################
st.sidebar.markdown("""Les mer om DH ved Nasjonalbiblioteket på [DHLAB-siden](https://nb.no/dh-lab)""")

this_year = datetime.date.today().year

st.sidebar.markdown("""## Parametre""")
st.sidebar.markdown("""### Utvalg""")
title = st.sidebar.text_input("Tittel på dokument, skriv * for å søke i alt", '*', help = "Tittel på avis, bok eller tidsskrift")
steps = st.sidebar.number_input('Antall år for gruppering', min_value = 1, max_value = 20, value = 10, help="Angi et tall mellom 1  og 20")
from_year, to_year = st.sidebar.slider(
    'Angi periode',
    min_value = 1800,
    max_value = datetime.date.today().year,
    value = (1950, this_year),
    help="Årene det søkes i")
mediatype = st.sidebar.selectbox("Velg medietype", ["aviser", "bøker", "tidsskrift"], index=0)



st.sidebar.markdown("""### Visning""")
hor = int(st.sidebar.number_input("Angi bredde  på figur 5 til 50", min_value=5, max_value=50, value=15))
ver = int(st.sidebar.number_input("Angi høyde på figur 2 til 20", min_value = 2, max_value = 20, value = 5))
rot = int(st.sidebar.number_input("Skråstill årstall - 0 til 90", min_value = 0, max_value=90, value = 20, help="0 er ingen skråstilling og 90 er vinkelrett"))



## Main page #######################
st.title("Hvor mange dokument inneholder en frase eller et ord?")
frases = st.text_input("List opp enkeltord eller fraser skilt med komma", "i alle dager, i forhold til")
frases = [[x.strip()] for x in frases.split(',')]

## Plot the results
try:
    fig, ax = plt.subplots()
    a = phrase_plots(frases, title =title, fra=int(from_year), til= int(to_year), media=mediatype, step= int(steps), aggs= 'year')
    a.plot(ax = ax, kind='bar', figsize=(hor,ver), rot=rot)
    st.pyplot(fig)

except KeyError:
    st.write("Ingen data")
