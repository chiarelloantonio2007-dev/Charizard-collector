import streamlit as st
import pandas as pd
import requests

# Configurazione della pagina
st.set_page_config(page_title="Charizard Analytics App", page_icon="🔥", layout="wide")

st.title("🔥 Charizard Advanced Database & Analytics")
st.subheader("Foto in tempo reale, prezzi medi e storici di vendita")

# Funzione per scaricare TUTTE le immagini in un colpo solo e salvarle in memoria (Cache)
@st.cache_data(show_spinner="Caricamento database immagini...")
def fetch_all_images():
    images_dict = {}
    url = "https://api.pokemontcg.io/v2/cards?q=name:charizard&pageSize=250"
    try:
        response = requests.get(url).json()
        if 'data' in response:
            for card in response['data']:
                name_lower = card['name'].lower()
                images_dict[card['id']] = card['images']['small']
                if name_lower not in images_dict:
                    images_dict[name_lower] = card['images']['small']
    except:
        pass
    return images_dict

# Carichiamo il dizionario delle immagini globale
all_images = fetch_all_images()

# Database interno completo e aggiornato (Menzioni speciali e camei rimosse)
@st.cache_data
def load_data():
    data = [
        # L'Era Classica Wizards of the Coast (1996 - 2003)
        {"Anno": "1996-1997", "Era": "L'Era Classica WOTC", "Nome": "Charizard Topsun", "Info": "Retro Blu, Retro Verde, No Number", "Img_ID": "celestial-storm-topsun"},
        {"Anno": "1996-1997", "Era": "L'Era Classica WOTC", "Nome": "Charizard Carddass Bandai", "Info": "Prism e Regular per distributori automatici", "Img_ID": "carddass"},
        {"Anno": "1998", "Era": "L'Era Classica WOTC", "Nome": "Charizard CD Promo #6", "Info": "Esclusiva olografica giapponese (CD Promo)", "Img_ID": "jumbo-promo"},
        {"Anno": "1999", "Era": "L'Era Classica WOTC", "Nome": "Charizard Set Base #4/102", "Info": "1st Edition, Shadowless, Unlimited, 4th Print", "Img_ID": "base1-4"},
        {"Anno": "1999-2000", "Era": "L'Era Classica WOTC", "Nome": "Charizard Topps", "Info": "Serie Anime: Regular, Foil, Rainbow, Chrome", "Img_ID": "topps"},
        {"Anno": "2000", "Era": "L'Era Classica WOTC", "Nome": "Charizard Set Base 2 #4/130", "Info": "Ristampa celebrativa del set base originale", "Img_ID": "base2-4"},
        {"Anno": "2000", "Era": "L'Era Classica WOTC", "Nome": "Dark Charizard (Charizard Oscuro)", "Info": "Team Rocket #4/82 (Olo) e #21/82 (Non-Olo)", "Img_ID": "rocket1-4"},
        {"Anno": "2000", "Era": "L'Era Classica WOTC", "Nome": "Blaine's Charizard (Charizard di Blaine)", "Info": "Gym Challenge #2/132 (Variante Errata)", "Img_ID": "gym2-2"},
        {"Anno": "2000", "Era": "L'Era Classica WOTC", "Nome": "Charizard Intro Pack Neo", "Info": "Mazzo didattico giapponese, artwork unico non-olo", "Img_ID": "intro-neo"},
        {"Anno": "2002", "Era": "L'Era Classica WOTC", "Nome": "Shining Charizard (Charizard Lucente)", "Info": "Neo Destiny #107/105 - Cromatico", "Img_ID": "neo4-107"},
        {"Anno": "2002", "Era": "L'Era Classica WOTC", "Nome": "Charizard e-Card", "Info": "Expedition Base Set #6/165, #39/165 e Reverse", "Img_ID": "ecard1-6"},
        {"Anno": "2002", "Era": "L'Era Classica WOTC", "Nome": "Charizard McDonald's Promo", "Info": "Esclusiva e-Card per i fast food giapponesi", "Img_ID": "mcd"},
        {"Anno": "2002", "Era": "L'Era Classica WOTC", "Nome": "Charizard Legendary Collection #3/110", "Info": "Olo, Non-Olo e Reverse Holo a fuochi d'artificio", "Img_ID": "lc-3"},
        {"Anno": "2002", "Era": "L'Era Classica WOTC", "Nome": "Charizard Box Topper #S1/S4", "Info": "Versione gigante (Oversized) Legendary Collection", "Img_ID": "lc-s1"},
        {"Anno": "2003", "Era": "L'Era Classica WOTC", "Nome": "Crystal Charizard (Charizard Cristallino)", "Info": "Skyridge #146/144 - Tipo Incolore e Reverse", "Img_ID": "skyridge-146"},

        # L'Era EX, Diamante/Perla, Platino e i Sotto-Set (2003 - 2013)
        {"Anno": "2003", "Era": "L'Era EX", "Nome": "Charizard Segreto", "Info": "EX Dragon #100/97 (Variante National Promo)", "Img_ID": "ex3-100"},
        {"Anno": "2004", "Era": "L'Era EX", "Nome": "Charizard ex", "Info": "EX RossoFuoco & VerdeFoglia #105/112", "Img_ID": "ex6-105"},
        {"Anno": "2005", "Era": "L'Era EX", "Nome": "Ditto (Charizard)", "Info": "EX Specie Delta #36/113 - Sembianze di Charizard", "Img_ID": "ex11-36"},
        {"Anno": "2006", "Era": "L'Era EX", "Nome": "Charizard Delta Species", "Info": "EX Guardiani dei Cristalli #4/100 - Elettro/Metallo", "Img_ID": "ex14-4"},
        {"Anno": "2006", "Era": "L'Era EX", "Nome": "Charizard Star", "Info": "EX Dragon Frontiers #100/101 - Shiny Tipo Oscurità", "Img_ID": "ex15-100"},
        {"Anno": "2007", "Era": "L'Era EX", "Nome": "Charizard (Power Keepers)", "Info": "EX Power Keepers #6/108", "Img_ID": "ex16-6"},
        {"Anno": "2007", "Era": "L'Era EX", "Nome": "Charizard (Secret Wonders)", "Info": "Secret Wonders #3/132", "Img_ID": "dp3-3"},
        {"Anno": "2009", "Era": "L'Era EX", "Nome": "Charizard G / G LV.X", "Info": "Platino Re dei Supremi #20/127 e #143/147", "Img_ID": "pl3-143"},
        {"Anno": "2009", "Era": "L'Era EX", "Nome": "Charizard G LV.X Promo", "Info": "Diamond & Pearl Promo #DP45", "Img_ID": "dpp-DP45"},
        {"Anno": "2009", "Era": "L'Era EX", "Nome": "Charizard Base Set Reprint", "Info": "Platino Arceus #1/99", "Img_ID": "pl4-1"},
        {"Anno": "2012", "Era": "L'Era EX", "Nome": "Charizard (Ascesa Eroica)", "Info": "Boundaries Cross #20/149", "Img_ID": "bw7-20"},
        {"Anno": "2013", "Era": "L'Era EX", "Nome": "Charizard Shiny Segreto", "Info": "Uragano Plasma #136/135 - Rara segreta dorata", "Img_ID": "bw8-136"},
        {"Anno": "2013", "Era": "L'Era EX", "Nome": "Charizard Radiant Collection", "Info": "Tesori Leggendari #RC5/RC25", "Img_ID": "bw11rc-RC5"},

        # L'Era XY (2014 - 2016)
        {"Anno": "2014", "Era": "L'Era XY", "Nome": "Charizard-EX (Double Rare)", "Info": "XY Fuoco Infernale #11/106", "Img_ID": "xy2-11"},
        {"Anno": "2014", "Era": "L'Era XY", "Nome": "Charizard-EX (Full Art)", "Info": "XY Fuoco Infernale #100/106", "Img_ID": "xy2-100"},
        {"Anno": "2014", "Era": "L'Era XY", "Nome": "M Charizard-EX Y (Ultra Rare)", "Info": "Fuoco Infernale #13/106", "Img_ID": "xy2-13"},
        {"Anno": "2014", "Era": "L'Era XY", "Nome": "M Charizard-EX Y (Secret Rare Oro)", "Info": "Fuoco Infernale #107/106", "Img_ID": "xy2-107"},
        {"Anno": "2014", "Era": "L'Era XY", "Nome": "M Charizard-EX X (Ultra Rare)", "Info": "Fuoco Infernale #69/106", "Img_ID": "xy2-69"},
        {"Anno": "2014", "Era": "L'Era XY", "Nome": "M Charizard-EX X (Secret Rare Oro)", "Info": "Fuoco Infernale #108/106", "Img_ID": "xy2-108"},
        {"Anno": "2014", "Era": "L'Era XY", "Nome": "Charizard-EX Promo", "Info": "XY Promo #XY17 e #XY29", "Img_ID": "xyp-XY17"},
        {"Anno": "2016", "Era": "L'Era XY", "Nome": "Charizard-EX & M Charizard-EX", "Info": "Generazioni #12/83 e #13/83", "Img_ID": "g1-12"},
        {"Anno": "2016", "Era": "L'Era XY", "Nome": "Charizard (XY Evoluzioni)", "Info": "XY Evoluzioni #11/108 - Remake Set Base", "Img_ID": "xy12-11"},
        {"Anno": "2016", "Era": "L'Era XY", "Nome": "Charizard Spirit Link", "Info": "XY Evoluzioni #81/108", "Img_ID": "xy12-81"},
        {"Anno": "2016", "Era": "L'Era XY", "Nome": "M Charizard-EX (Full Art Mega)", "Info": "XY Evoluzioni #101/108", "Img_ID": "xy12-101"},

        # L'Era Sole & Luna (2017 - 2019)
        {"Anno": "2017", "Era": "L'Era Sole & Luna", "Nome": "Charizard-GX (Double Rare)", "Info": "Ombre Infuocate #20/147", "Img_ID": "sm3-20"},
        {"Anno": "2017", "Era": "L'Era Sole & Luna", "Nome": "Charizard-GX (Full Art)", "Info": "Ombre Infuocate #150/147", "Img_ID": "sm3-150"},
        {"Anno": "2017", "Era": "L'Era Sole & Luna", "Nome": "Charizard-GX (Rainbow / Hyper Rare)", "Info": "Ombre Infuocate #150/147 (Secret)", "Img_ID": "sm3-150"},
        {"Anno": "2017", "Era": "L'Era Sole & Luna", "Nome": "Charizard-GX Full Art Promo", "Info": "SM Promo #SM60", "Img_ID": "smp-SM60"},
        {"Anno": "2018", "Era": "L'Era Sole & Luna", "Nome": "Charizard (Dragon Majesty)", "Info": "Dragon Majesty #3/70", "Img_ID": "sm75-3"},
        {"Anno": "2019", "Era": "L'Era Sole & Luna", "Nome": "Charizard (Gioco di Squadra)", "Info": "Gioco di Squadra #14/181", "Img_ID": "sm9-14"},
        {"Anno": "2019", "Era": "L'Era Sole & Luna", "Nome": "Charizard (Detective Pikachu)", "Info": "Detective Pikachu #5/18", "Img_ID": "det1-5"},
        {"Anno": "2019", "Era": "L'Era Sole & Luna", "Nome": "Reshiram e Charizard-GX ALLEATI", "Info": "Legami Inossidabili #20/214", "Img_ID": "sm10-20"},
        {"Anno": "2019", "Era": "L'Era Sole & Luna", "Nome": "Clone Charizard (Charizard Clone)", "Info": "Mewtwo Strikes Back Evolution Promo", "Img_ID": "smp-SM226"},
        {"Anno": "2019", "Era": "L'Era Sole & Luna", "Nome": "Charizard-GX Cromatico", "Info": "Destino Sfuggente #SV49/SV94", "Img_ID": "sm115sv-SV49"},
        {"Anno": "2019", "Era": "L'Era Sole & Luna", "Nome": "Charizard e Braixen-GX ALLEATI", "Info": "Eclissi Cosmica #22/236", "Img_ID": "sm12-22"},

        # L'Era Spada & Scudo (2020 - 2022)
        {"Anno": "2020", "Era": "L'Era Spada & Scudo", "Nome": "Charizard-V & Charizard-VMAX", "Info": "Fiamme Oscure #19/189 e #20/189", "Img_ID": "swsh3-19"},
        {"Anno": "2020", "Era": "L'Era Spada & Scudo", "Nome": "Charizard-VMAX Arcobaleno", "Info": "Futuro Campione #074/073", "Img_ID": "swsh35-074"},
        {"Anno": "2020", "Era": "L'Era Spada & Scudo", "Nome": "Charizard-V Cromatico (Shiny)", "Info": "Futuro Campione #079/073", "Img_ID": "swsh35-079"},
        {"Anno": "2020", "Era": "L'Era Spada & Scudo", "Nome": "Charizard (Leon)", "Info": "Voltaggio Sfolgorante #025/185", "Img_ID": "swsh4-025"},
        {"Anno": "2020", "Era": "L'Era Spada & Scudo", "Nome": "Special Delivery Charizard", "Info": "Promo Pokémon Center #SWSH075", "Img_ID": "swshp-SWSH075"},
        {"Anno": "2021", "Era": "L'Era Spada & Scudo", "Nome": "Charizard-VMAX Cromatico", "Info": "Destino Splendente #SV107/SV122", "Img_ID": "swsh45sv-SV107"},
        {"Anno": "2021", "Era": "L'Era Spada & Scudo", "Nome": "Charizard di Lance V", "Info": "Gran Festa Promo #SWSH261", "Img_ID": "swshp-SWSH261"},
        {"Anno": "2021", "Era": "L'Era Spada & Scudo", "Nome": "Charizard Gran Festa #4/102", "Info": "Ristampa 25° Anniversario", "Img_ID": "cel25-4"},
        {"Anno": "2022", "Era": "L'Era Spada & Scudo", "Nome": "Charizard-V Alternate Art", "Info": "Astri Lucenti Alt Art #154", "Img_ID": "swsh9-154"},
        {"Anno": "2022", "Era": "L'Era Spada & Scudo", "Nome": "Charizard-VSTAR (Arcobaleno)", "Info": "Astri Lucenti #174/172", "Img_ID": "swsh9-174"},
        {"Anno": "2022", "Era": "L'Era Spada & Scudo", "Nome": "Charizard (Leon) Trainer Gallery", "Info": "Astri Lucenti #TG03/TG30", "Img_ID": "swsh9tg-TG03"},
        {"Anno": "2022", "Era": "L'Era Spada & Scudo", "Nome": "Charizard Lucente (Radiant)", "Info": "Pokémon GO #11/78 e Zenit Regale #20/159", "Img_ID": "pgo-11"},
        
        # Le tre Promo UPC separate
        {"Anno": "2022", "Era": "L'Era Spada & Scudo", "Nome": "Charizard-V Promo UPC", "Info": "Special Illustration Promo #SWSH260", "Img_ID": "swshp-SWSH260"},
        {"Anno": "2022", "Era": "L'Era Spada & Scudo", "Nome": "Charizard-VMAX Promo UPC", "Info": "Special Illustration Promo #SWSH261", "Img_ID": "swshp-SWSH261"},
        {"Anno": "2022", "Era": "L'Era Spada & Scudo", "Nome": "Charizard-VSTAR Promo UPC", "Info": "Special Illustration Promo #SWSH262", "Img_ID": "swshp-SWSH262"},

        # L'Era Scarlatto & Violetto (2023 - 2026)
        {"Anno": "2023", "Era": "L'Era Scarlatto & Violetto", "Nome": "Charizard ex Teracristal (Double Rare)", "Info": "Ossidiana Infuocata #125/197", "Img_ID": "sv3-125"},
        {"Anno": "2023", "Era": "L'Era Scarlatto & Violetto", "Nome": "Charizard ex Teracristal (Ultra Rare Full Art)", "Info": "Ossidiana Infuocata #215/197", "Img_ID": "sv3-215"},
        {"Anno": "2023", "Era": "L'Era Scarlatto & Violetto", "Nome": "Charizard ex Teracristal (SIR)", "Info": "Ossidiana Infuocata #223/197", "Img_ID": "sv3-223"},
        {"Anno": "2023", "Era": "L'Era Scarlatto & Violetto", "Nome": "Charizard ex Teracristal (Hyper Rare Gold)", "Info": "Ossidiana Infuocata #228/197", "Img_ID": "sv3-228"},
        {"Anno": "2023", "Era": "L'Era Scarlatto & Violetto", "Nome": "Charizard ex Kanto (Double Rare)", "Info": "Scarlatto e Violetto 151 #006/165", "Img_ID": "sv3pt5-006"},
        {"Anno": "2023", "Era": "L'Era Scarlatto & Violetto", "Nome": "Charizard ex Kanto (Ultra Rare Full Art)", "Info": "Scarlatto e Violetto 151 #183/165", "Img_ID": "sv3pt5-183"},
        {"Anno": "2023", "Era": "L'Era Scarlatto & Violetto", "Nome": "Charizard ex Kanto (SIR)", "Info": "Scarlatto e Violetto 151 #199/165", "Img_ID": "sv3pt5-199"},
        {"Anno": "2023", "Era": "L'Era Scarlatto & Violetto", "Nome": "Charizard ex Promozionali", "Info": "Promo SV #056 e #074", "Img_ID": "svp-56"},
        {"Anno": "2024", "Era": "L'Era Scarlatto & Violetto", "Nome": "Charizard ex Teracristal Shiny (Shiny Rare)", "Info": "Destino di Paldea #054/091", "Img_ID": "sv4pt5-054"},
        {"Anno": "2024", "Era": "L'Era Scarlatto & Violetto", "Nome": "Charizard ex Teracristal Shiny (SIR)", "Info": "Destino di Paldea #234/091", "Img_ID": "sv4pt5-234"},

        # L'Era Megaevoluzioni (2025)
        {"Anno": "2025", "Era": "L'Era Megaevoluzioni", "Nome": "Mega Charizard X ex", "Info": "Espansione Megaevoluzione — Fiamme Spettrali #013/094", "Img_ID": "sv6-mega1"},
        {"Anno": "2025", "Era": "L'Era Megaevoluzioni", "Nome": "Mega Charizard X ex (Full Art)", "Info": "Espansione Megaevoluzione — Fiamme Spettrali #109/094", "Img_ID": "sv6-mega2"},
        {"Anno": "2025", "Era": "L'Era Megaevoluzioni", "Nome": "Mega Charizard X ex (SIR)", "Info": "Espansione Megaevoluzione — Fiamme Spettrali #125/094", "Img_ID": "sv6-mega3"},
        {"Anno": "2025", "Era": "L'Era Megaevoluzioni", "Nome": "Mega Charizard X ex (Gold)", "Info": "Espansione Megaevoluzione — Fiamme Spettrali #130/094", "Img_ID": "sv6-mega4"},
        {"Anno": "2025", "Era": "L'Era Megaevoluzioni", "Nome": "Mega Charizard Y ex", "Info": "Set d'accompagnamento / Mazzo Tematico speciale", "Img_ID": "sv6-mega5"},
        {"Anno": "2026", "Era": "L'Era Scarlatto & Violetto", "Nome": "Mega Charizard Y ex (Promo)", "Info": "Tin da Collezione / Prodotto speciale d'inizio anno", "Img_ID": "sv7-promo1"}
    ]
    return pd.DataFrame(data)

df = load_data()

# Inizializzazione dello stato della collezione (Binder)
if "binder" not in st.session_state:
    st.session_state.binder = {}

# Barra laterale per i Filtri di Ricerca
st.sidebar.header("🔍 Filtri di Ricerca")
search_query = st.sidebar.text_input("Cerca per nome:", "")
selected_era = st.sidebar.selectbox("Filtra per Era:", ["Tutte"] + list(df["Era"].unique()))

# Filtro Binder
mostra_solo_binder = st.sidebar.checkbox("📂 Mostra SOLO il mio Binder")

# Conteggio carte nel Binder
carte_possedute = sum(1 for v in st.session_state.binder.values() if v)
st.sidebar.metric(label="📊 Carte nel tuo Binder", value=f"{carte_possedute} / {len(df)}")

# Applicazione dei filtri sui dati
filtered_df = df.copy()
if search_query:
    filtered_df = filtered_df[filtered_df["Nome"].str.contains(search_query, case=False)]
if selected_era != "Tutte":
    filtered_df = filtered_df[filtered_df["Era"] == selected_era]
if muestra_solo_binder:
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
                img_url = all_images.get(row["Img_ID"], all_images.get(row["Nome"].lower(), "https://via.placeholder.com/150x210?text=Charizard"))
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