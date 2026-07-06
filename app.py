import streamlit as st
import pandas as pd
import requests

# Configurazione della pagina
st.set_page_config(page_title="Charizard Analytics App", page_icon="🔥", layout="wide")

st.title("🔥 Charizard Advanced Database & Analytics")
st.subheader("Foto in tempo reale, prezzi medi e storici di vendita")

# Database interno completo e aggiornato
@st.cache_data
def load_data():
    data = [
        # L'Era Classica Wizards of the Coast (1996 - 2003)
        {"Anno": "1996-1997", "Era": "L'Era Classica WOTC", "Nome": "Charizard Topsun", "Info": "Retro Blu, Retro Verde, No Number"},
        {"Anno": "1996-1997", "Era": "L'Era Classica WOTC", "Nome": "Charizard Carddass Bandai", "Info": "Prism e Regular per distributori automatici"},
        {"Anno": "1998", "Era": "L'Era Classica WOTC", "Nome": "Charizard CD Promo #6", "Info": "Esclusiva olografica giapponese (CD Promo)"},
        {"Anno": "1999", "Era": "L'Era Classica WOTC", "Nome": "Charizard Set Base #4/102", "Info": "1st Edition, Shadowless, Unlimited, 4th Print"},
        {"Anno": "1999-2000", "Era": "L'Era Classica WOTC", "Nome": "Charizard Topps", "Info": "Serie Anime: Regular, Foil, Rainbow, Chrome"},
        {"Anno": "2000", "Era": "L'Era Classica WOTC", "Nome": "Charizard Set Base 2 #4/130", "Info": "Ristampa celebrativa del set base originale"},
        {"Anno": "2000", "Era": "L'Era Classica WOTC", "Nome": "Dark Charizard (Charizard Oscuro)", "Info": "Team Rocket #4/82 (Olo) e #21/82 (Non-Olo)"},
        {"Anno": "2000", "Era": "L'Era Classica WOTC", "Nome": "Blaine's Charizard (Charizard di Blaine)", "Info": "Gym Challenge #2/132 (Variante Errata)"},
        {"Anno": "2000", "Era": "L'Era Classica WOTC", "Nome": "Charizard Intro Pack Neo", "Info": "Mazzo didattico giapponese, artwork unico non-olo"},
        {"Anno": "2002", "Era": "L'Era Classica WOTC", "Nome": "Shining Charizard (Charizard Lucente)", "Info": "Neo Destiny #107/105 - Cromatico"},
        {"Anno": "2002", "Era": "L'Era Classica WOTC", "Nome": "Charizard e-Card", "Info": "Expedition Base Set #6/165, #39/165 e Reverse"},
        {"Anno": "2002", "Era": "L'Era Classica WOTC", "Nome": "Charizard McDonald's Promo", "Info": "Esclusiva e-Card per i fast food giapponesi"},
        {"Anno": "2002", "Era": "L'Era Classica WOTC", "Nome": "Charizard Legendary Collection #3/110", "Info": "Olo, Non-Olo e Reverse Holo a fuochi d'artificio"},
        {"Anno": "2002", "Era": "L'Era Classica WOTC", "Nome": "Charizard Box Topper #S1/S4", "Info": "Versione gigante (Oversized) Legendary Collection"},
        {"Anno": "2003", "Era": "L'Era Classica WOTC", "Nome": "Crystal Charizard (Charizard Cristallino)", "Info": "Skyridge #146/144 - Tipo Incolore e Reverse"},

        # L'Era EX, Diamante/Perla, Platino e i Sotto-Set (2003 - 2013)
        {"Anno": "2003", "Era": "L'Era EX", "Nome": "Charizard Segreto", "Info": "EX Dragon #100/97 (Variante National Promo)"},
        {"Anno": "2004", "Era": "L'Era EX", "Nome": "Charizard ex", "Info": "EX RossoFuoco & VerdeFoglia #105/112"},
        {"Anno": "2005", "Era": "L'Era EX", "Nome": "Ditto (Charizard)", "Info": "EX Specie Delta #36/113 - Sembianze di Charizard"},
        {"Anno": "2006", "Era": "L'Era EX", "Nome": "Charizard Delta Species", "Info": "EX Guardiani dei Cristalli #4/100 - Elettro/Metallo"},
        {"Anno": "2006", "Era": "L'Era EX", "Nome": "Charizard Star", "Info": "EX Dragon Frontiers #100/101 - Shiny Tipo Oscurità"},
        {"Anno": "2007", "Era": "L'Era EX", "Nome": "Charizard (Power Keepers)", "Info": "EX Power Keepers #6/108"},
        {"Anno": "2007", "Era": "L'Era EX", "Nome": "Charizard (Secret Wonders)", "Info": "Secret Wonders #3/132"},
        {"Anno": "2009", "Era": "L'Era EX", "Nome": "Charizard G / G LV.X", "Info": "Platino Re dei Supremi #20/127 e #143/147"},
        {"Anno": "2009", "Era": "L'Era EX", "Nome": "Charizard G LV.X Promo", "Info": "Diamond & Pearl Promo #DP45"},
        {"Anno": "2009", "Era": "L'Era EX", "Nome": "Charizard Base Set Reprint", "Info": "Platino Arceus #1/99"},
        {"Anno": "2012", "Era": "L'Era EX", "Nome": "Charizard (Ascesa Eroica)", "Info": "Boundaries Cross #20/149"},
        {"Anno": "2013", "Era": "L'Era EX", "Nome": "Charizard Shiny Segreto", "Info": "Uragano Plasma #136/135 - Rara segreta dorata"},
        {"Anno": "2013", "Era": "L'Era EX", "Nome": "Charizard Radiant Collection", "Info": "Tesori Leggendari #RC5/RC25"},

        # L'Era XY (2014 - 2016)
        {"Anno": "2014", "Era": "L'Era XY", "Nome": "Charizard-EX (Double Rare)", "Info": "XY Fuoco Infernale #11/106"},
        {"Anno": "2014", "Era": "L'Era XY", "Nome": "Charizard-EX (Full Art)", "Info": "XY Fuoco Infernale #100/106"},
        {"Anno": "2014", "Era": "L'Era XY", "Nome": "M Charizard-EX Y (Ultra Rare)", "Info": "Fuoco Infernale #13/106"},
        {"Anno": "2014", "Era": "L'Era XY", "Nome": "M Charizard-EX Y (Secret Rare Oro)", "Info": "Fuoco Infernale #107/106"},
        {"Anno": "2014", "Era": "L'Era XY", "Nome": "M Charizard-EX X (Ultra Rare)", "Info": "Fuoco Infernale #69/106"},
        {"Anno": "2014", "Era": "L'Era XY", "Nome": "M Charizard-EX X (Secret Rare Oro)", "Info": "Fuoco Infernale #108/106"},
        {"Anno": "2014", "Era": "L'Era XY", "Nome": "Charizard-EX Promo", "Info": "XY Promo #XY17 e #XY29"},
        {"Anno": "2016", "Era": "L'Era XY", "Nome": "Charizard-EX & M Charizard-EX", "Info": "Generazioni #12/83 e #13/83"},
        {"Anno": "2016", "Era": "L'Era XY", "Nome": "Charizard (XY Evoluzioni)", "Info": "XY Evoluzioni #11/108 - Remake Set Base"},
        {"Anno": "2016", "Era": "L'Era XY", "Nome": "Charizard Spirit Link", "Info": "XY Evoluzioni #81/108"},
        {"Anno": "2016", "Era": "L'Era XY", "Nome": "M Charizard-EX (Full Art Mega)", "Info": "XY Evoluzioni #101/108"},
        {"Anno": "2016", "Era": "L'Era XY", "Nome": "Charizard-EX Promo (Cameo)", "Info": "XY Promo #XY121 - Con Magmar e Flareon"},

        # L'Era Sole & Luna (2017 - 2019)
        {"Anno": "2017", "Era": "L'Era Sole & Luna", "Nome": "Charizard-GX (Double Rare)", "Info": "Ombre Infuocate #20/147"},
        {"Anno": "2017", "Era": "L'Era Sole & Luna", "Nome": "Charizard-GX (Full Art)", "Info": "Ombre Infuocate #150/147"},
        {"Anno": "2017", "Era": "L'Era Sole & Luna", "Nome": "Charizard-GX (Rainbow / Hyper Rare)", "Info": "Ombre Infuocate #150/147 (Secret)"},
        {"Anno": "2017", "Era": "L'Era Sole & Luna", "Nome": "Charizard-GX Full Art Promo", "Info": "SM Promo #SM60"},
        {"Anno": "2018", "Era": "L'Era Sole & Luna", "Nome": "Charizard (Dragon Majesty)", "Info": "Dragon Majesty #3/70"},
        {"Anno": "2019", "Era": "L'Era Sole & Luna", "Nome": "Charizard (Gioco di Squadra)", "Info": "Gioco di Squadra #14/181"},
        {"Anno": "2019", "Era": "L'Era Sole & Luna", "Nome": "Charizard (Detective Pikachu)", "Info": "Detective Pikachu #5/18"},
        {"Anno": "2019", "Era": "L'Era Sole & Luna", "Nome": "Reshiram e Charizard-GX ALLEATI", "Info": "Legami Inossidabili #20/214, Full Art #194, Alt Art #195, Arcobaleno #217"},
        {"Anno": "2019", "Era": "L'Era Sole & Luna", "Nome": "Clone Charizard (Charizard Clone)", "Info": "Mewtwo Strikes Back Evolution #366/SM-P"},
        {"Anno": "2019", "Era": "L'Era Sole & Luna", "Nome": "Charizard-GX Cromatico", "Info": "Destino Sfuggente #SV49/SV94"},
        {"Anno": "2019", "Era": "L'Era Sole & Luna", "Nome": "Charizard e Braixen-GX ALLEATI", "Info": "Eclissi Cosmica #22/236, Full Art #212, Arcobaleno #251"},

        # L'Era Spada & Scudo (2020 - 2022)
        {"Anno": "2020", "Era": "L'Era Spada & Scudo", "Nome": "Charizard-V & Charizard-VMAX", "Info": "Fiamme Oscure #19/189 e #20/189"},
        {"Anno": "2020", "Era": "L'Era Spada & Scudo", "Nome": "Charizard-VMAX Arcobaleno", "Info": "Futuro Campione #074/073"},
        {"Anno": "2020", "Era": "L'Era Spada & Scudo", "Nome": "Charizard-V Cromatico (Shiny)", "Info": "Futuro Campione #079/073"},
        {"Anno": "2020", "Era": "L'Era Spada & Scudo", "Nome": "Charizard (Leon)", "Info": "Voltaggio Sfolgorante #025/185"},
        {"Anno": "2020", "Era": "L'Era Spada & Scudo", "Nome": "Special Delivery Charizard", "Info": "Promo Pokémon Center #SWSH075"},
        {"Anno": "2021", "Era": "L'Era Spada & Scudo", "Nome": "Charizard-VMAX Cromatico", "Info": "Destino Splendente #SV107/SV122"},
        {"Anno": "2021", "Era": "L'Era Spada & Scudo", "Nome": "Charizard di Lance V", "Info": "Gran Festa Promo #SWSH261"},
        {"Anno": "2021", "Era": "L'Era Spada & Scudo", "Nome": "Charizard Gran Festa #4/102", "Info": "Ristampa 25° Anniversario"},
        {"Anno": "2022", "Era": "L'Era Spada & Scudo", "Nome": "Charizard-V Alternate Art", "Info": "Astri Lucenti Alt Art #154"},
        {"Anno": "2022", "Era": "L'Era Spada & Scudo", "Nome": "Charizard-VSTAR (Arcobaleno)", "Info": "Astri Lucenti #174/172"},
        {"Anno": "2022", "Era": "L'Era Spada & Scudo", "Nome": "Charizard (Leon) Trainer Gallery", "Info": "Astri Lucenti #TG03/TG30"},
        {"Anno": "2022", "Era": "L'Era Spada & Scudo", "Nome": "Charizard Lucente (Radiant)", "Info": "Pokémon GO #11/78 e Zenit Regale #20/159"},
        
        # SEPARATE: Le tre Promo UPC separate come richiesto
        {"Anno": "2022", "Era": "L'Era Spada & Scudo", "Nome": "Charizard-V Promo UPC", "Info": "Special Illustration Promo #SWSH260"},
        {"Anno": "2022", "Era": "L'Era Spada & Scudo", "Nome": "Charizard-VMAX Promo UPC", "Info": "Special Illustration Promo #SWSH261"},
        {"Anno": "2022", "Era": "L'Era Spada & Scudo", "Nome": "Charizard-VSTAR Promo UPC", "Info": "Special Illustration Promo #SWSH262"},

        # L'Era Scarlatto & Violetto (2023 - 2024-2026)
        {"Anno": "2023", "Era": "L'Era Scarlatto & Violetto", "Nome": "Charizard ex Teracristal (Double Rare)", "Info": "Ossidiana Infuocata #125/197 - Tipo Buio Regolare"},
        {"Anno": "2023", "Era": "L'Era Scarlatto & Violetto", "Nome": "Charizard ex Teracristal (Ultra Rare Full Art)", "Info": "Ossidiana Infuocata #215/197"},
        {"Anno": "2023", "Era": "L'Era Scarlatto & Violetto", "Nome": "Charizard ex Teracristal (SIR)", "Info": "Ossidiana Infuocata #223/197 - Special Illustration Rare"},
        {"Anno": "2023", "Era": "L'Era Scarlatto & Violetto", "Nome": "Charizard ex Teracristal (Hyper Rare Gold)", "Info": "Ossidiana Infuocata #228/197"},
        {"Anno": "2023", "Era": "L'Era Scarlatto & Violetto", "Nome": "Charizard ex Kanto (Double Rare)", "Info": "Scarlatto e Violetto 151 #006/165"},
        {"Anno": "2023", "Era": "L'Era Scarlatto & Violetto", "Nome": "Charizard ex Kanto (Ultra Rare Full Art)", "Info": "Scarlatto e Violetto 151 #183/165"},
        {"Anno": "2023", "Era": "L'Era Scarlatto & Violetto", "Nome": "Charizard ex Kanto (SIR)", "Info": "Scarlatto e Violetto 151 #199/165 - Canyon"},
        {"Anno": "2023", "Era": "L'Era Scarlatto & Violetto", "Nome": "Charizard ex Promozionali", "Info": "Promo SV #056 e #074"},
        {"Anno": "2024", "Era": "L'Era Scarlatto & Violetto", "Nome": "Charizard ex Teracristal Shiny (Shiny Rare)", "Info": "Destino di Paldea #054/091"},
        {"Anno": "2024", "Era": "L'Era Scarlatto & Violetto", "Nome": "Charizard ex Teracristal Shiny (SIR)", "Info": "Destino di Paldea #234/091 - Cromatico artistico"},
        {"Anno": "2024", "Era": "L'Era Scarlatto & Violetto", "Nome": "Charizard McDonald's Promo", "Info": "Dragon Discovery #001/015"},

        # MODIFICATE: Le carte del 2025 spostate sotto "L'Era Megaevoluzioni" come richiesto
        {"Anno": "2025", "Era": "L'Era Megaevoluzioni", "Nome": "Mega Charizard X ex", "Info": "Espansione Megaevoluzione — Fiamme Spettrali #013/094"},
        {"Anno": "2025", "Era": "L'Era Megaevoluzioni", "Nome": "Mega Charizard X ex (Full Art)", "Info": "Espansione Megaevoluzione — Fiamme Spettrali #109/094"},
        {"Anno": "2025", "Era": "L'Era Megaevoluzioni", "Nome": "Mega Charizard X ex (SIR)", "Info": "Espansione Megaevoluzione — Fiamme Spettrali #125/094"},
        {"Anno": "2025", "Era": "L'Era Megaevoluzioni", "Nome": "Mega Charizard X ex (Gold)", "Info": "Espansione Megaevoluzione — Fiamme Spettrali #130/094"},
        {"Anno": "2025", "Era": "L'Era Megaevoluzioni", "Nome": "Mega Charizard Y ex", "Info": "Set d'accompagnamento / Mazzo Tematico speciale"},
        {"Anno": "2026", "Era": "L'Era Scarlatto & Violetto", "Nome": "Mega Charizard Y ex (Promo)", "Info": "Tin da Collezione / Prodotto speciale d'inizio anno"},

        # Menzioni Speciali e Camei Ufficiali
        {"Anno": "2023", "Era": "Menzioni Speciali e Camei", "Nome": "Mewtwo GG (Cameo)", "Info": "Crown Zenith Galarian Gallery #GG44"},
        {"Anno": "2023", "Era": "Menzioni Speciali e Camei", "Nome": "Pikachu Promo SV (Cameo)", "Info": "Scarlatto e Violetto Promo #005"},
        {"Anno": "2019", "Era": "Menzioni Speciali e Camei", "Nome": "Greninja (Cameo)", "Info": "Greninja Unbroken Bonds 117"},
        {"Anno": "2023", "Era": "Menzioni Speciali e Camei", "Nome": "Charmander IR (Cameo)", "Info": "Scarlatto e Violetto 151 #168/165"},
        {"Anno": "Vintage", "Era": "Menzioni Speciali e Camei", "Nome": "Team Rocket's Meowth Promo (Cameo)", "Info": "WOTC Promo"}
    ]
    return pd.DataFrame(data)

df = load_data()

# Inizializzazione dello stato della collezione (per salvare i check)
if "binder" not in st.session_state:
    st.session_state.binder = {}

def get_pokemon_image(card_name):
    clean_name = card_name.replace(" (Cameo)", "").replace(" (Charizard Oscuro)", "").replace(" (Charizard di Blaine)", "").replace(" (Charizard Lucente)", "").replace(" (Charizard Cristallino)", "")
    # Piccolo trucco per far cercare bene le promo UPC separate
    if "Promo UPC" in clean_name:
        clean_name = "Charizard SWSH"
    url = f"https://api.pokemontcg.io/v2/cards?q=name:\"{clean_name}\""
    try:
        response = requests.get(url).json()
        if response['data']:
            return response['data'][0]['images']['small']
    except:
        pass
    return "https://via.placeholder.com/150x210?text=Immagine+Non+Disponibile"

# Barra laterale per i Filtri di Ricerca
st.sidebar.header("🔍 Filtri di Ricerca")
search_query = st.sidebar.text_input("Cerca per nome:", "")
selected_era = st.sidebar.selectbox("Filtra per Era:", ["Tutte"] + list(df["Era"].unique()))

# Mostra solo il Binder
mostra_solo_binder = st.sidebar.checkbox("📂 Mostra SOLO il mio Binder")

# Conteggio carte nel Binder
carte_possedute = sum(1 for v in st.session_state.binder.values() if v)
st.sidebar.metric(label="📊 Carte nel tuo Binder", value=f"{carte_possedute} / {len(df)}")

# Applicazione dei filtri
filtered_df = df.copy()

if search_query:
    filtered_df = filtered_df[filtered_df["Nome"].str.contains(search_query, case=False)]
if selected_era != "Tutte":
    filtered_df = filtered_df[filtered_df["Era"] == selected_era]
if mostra_solo_binder:
    filtered_df = filtered_df[filtered_df.index.map(lambda idx: st.session_state.binder.get(f"check_{idx}", False))]

# Visualizzazione delle carte
if filtered_df.empty:
    st.warning("Nessun Charizard corrisponde ai criteri selezionati.")
else:
    for index, row in filtered_df.iterrows():
        key_id = f"check_{index}"
        with st.container():
            col1, col2, col3 = st.columns([1, 2, 2])
            with col1:
                img_url = get_pokemon_image(row["Nome"])
                st.image(img_url, width=160)
            with col2:
                st.markdown(f"### {row['Nome']}")
                st.caption(f"📅 **Anno:** {row['Anno']} | 🏛️ **Era:** {row['Era']}")
                st.write(f"📝 *{row['Info']}*")
                
                owned = st.checkbox("Ce l'ho in collezione", key=key_id, value=st.session_state.binder.get(key_id, False))
                st.session_state.binder[key_id] = owned
                
                if owned:
                    st.success("✅ Aggiunto al tuo Binder!")
            with col3:
                st.markdown("📊 **Market Analytics (Simulazione Cardmarket)**")
                if "Base" in row["Nome"] or "Shining" in row["Nome"] or "Crystal" in row["Nome"] or "Star" in row["Nome"]:
                    prezzo_medio = 650.00
                elif "ex" in row["Nome"].lower() and row["Anno"] == "2004":
                    prezzo_medio = 250.00
                elif "SIR" in row["Nome"] or "Alternate Art" in row["Nome"] or "Promo UPC" in row["Nome"]:
                    prezzo_medio = 180.00
                else:
                    prezzo_medio = 45.00
                    
                st.metric(label="Prezzo Medio di Vendita", value=f"€ {prezzo_medio:.2f}", delta="+5.4% nell'ultimo mese")
                st.markdown("**Migliori vendite recenti:**")
                st.text(f"🔸 Mint (Copia perfetta): € {prezzo_medio * 1.6:.2f}")
                st.text(f"🔸 Near Mint (Ottima copia): € {prezzo_medio:.2f}")
                st.text(f"🔸 Played (Copia rovinata): € {prezzo_medio * 0.35:.2f}")
            st.divider()