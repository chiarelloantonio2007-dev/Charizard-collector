import streamlit as st
import pandas as pd
import requests

# Configurazione della pagina
st.set_page_config(page_title="Charizard Analytics App", page_icon="🔥", layout="wide")

st.title("🔥 Charizard Advanced Database & Analytics")
st.subheader("Foto in tempo reale, prezzi medi e storici di vendita")

# --- FUNZIONE PER RECUPERARE I PREZZI REALI DA CARDMARKET ---
@st.cache_data(ttl=3600, show_spinner=False)  # Cache di 1 ora, nasconde lo spinner nativo per fluidità
def fetch_cardmarket_prices(img_id):
    """
    Interroga l'API pubblica di Pokémon TCG usando l'ID della carta.
    Evita le chiamate per gli ID speciali non presenti nel database standard.
    """
    # Elenco di ID che sappiamo NON essere presenti nell'API ufficiale internazionale
    id_non_supportati = [
        "topsun", "carddass", "cd_promo", "topps", "intro-neo", 
        "sv6-mega1", "sv6-mega2", "sv6-mega3", "sv6-mega4", "sv6-mega5"
    ]
    
    if img_id in id_non_supportati:
        return {"Stato": "Non Standard", "Prezzo_Trend": 0.00, "Prezzo_Low": 0.00, "Prezzo_Avg1": 0.00, "Prezzo_Avg30": 0.00, "Link_Cardmarket": ""}

    try:
        url = f"https://api.pokemontcg.io/v2/cards/{img_id}"
        # Timeout a 2 secondi per non bloccare l'app se l'API è lenta
        response = requests.get(url, timeout=2.0)
        
        if response.status_code == 200:
            card_data = response.json().get('data', {})
            cardmarket = card_data.get('cardmarket', {})
            
            if cardmarket:
                prices = cardmarket.get('prices', {})
                return {
                    "Stato": "Successo",
                    "Prezzo_Trend": prices.get('trendPrice', 0.00),
                    "Prezzo_Low": prices.get('lowPrice', 0.00),
                    "Prezzo_Avg1": prices.get('avg1', 0.00),
                    "Prezzo_Avg30": prices.get('avg30', 0.00),
                    "Link_Cardmarket": cardmarket.get('url', 'https://www.cardmarket.com')
                }
        return {"Stato": "Nessun dato", "Prezzo_Trend": 0.00, "Prezzo_Low": 0.00, "Prezzo_Avg1": 0.00, "Prezzo_Avg30": 0.00, "Link_Cardmarket": ""}
    except Exception:
        # In caso di timeout o errore di rete, restituisce uno stato di errore senza rompere l'app
        return {"Stato": "Errore API", "Prezzo_Trend": 0.00, "Prezzo_Low": 0.00, "Prezzo_Avg1": 0.00, "Prezzo_Avg30": 0.00, "Link_Cardmarket": ""}


# Dizionario statico delle immagini con i tuoi link esatti e verificati
@st.cache_data
def load_all_images():
    return {
        "topsun": "https://storage.googleapis.com/images.pricecharting.com/7e0e90a3886cc364f32ae16c0e1e281c5efe4190a04bc2d0062582beeef7eab9/1600.jpg",
        "carddass": "https://storage.googleapis.com/images.pricecharting.com/4583c416d1b36c6a5a13a08b34d191b5d3696d10586d16a5c9d5864daed1dfe1/240.jpg",
        "cd_promo": "https://images.scrydex.com/pokemon/miscp_ja-39/medium",
        "base1-4": "https://images.scrydex.com/pokemon/base1-4/medium",
        "topps": "https://i.ebayimg.com/images/g/IcAAAeSwAZNpuq7S/s-l1600.webp",
        "base2-4": "https://images.scrydex.com/pokemon/base4-4/medium",
        "rocket1-4": "https://images.scrydex.com/pokemon/base5-4/medium",
        "gym2-2": "https://images.scrydex.com/pokemon/gym2-2/medium",
        "intro-neo": "https://images.scrydex.com/pokemon/neo2pf_ja-6/medium",
        "neo4-107": "https://images.scrydex.com/pokemon/neo4-107/medium",
        "ecard1-6": "https://images.scrydex.com/pokemon/ecard1-6/medium",
        "lc-3": "https://images.scrydex.com/pokemon/base6-3/medium",
        "skyridge-146": "https://images.scrydex.com/pokemon/ecard3-146/medium",
        "ex3-100": "https://images.pokemontcg.io/ex3/100.png",
        "ex6-105": "https://images.pokemontcg.io/ex6/105.png",
        "ex14-4": "https://images.pokemontcg.io/ex14/4.png",
        "ex15-100": "https://images.pokemontcg.io/ex15/100.png",
        "ex16-6": "https://images.pokemontcg.io/ex16/6.png",
        "dp3-3": "https://images.pokemontcg.io/dp3/3.png",
        "pl3-143": "https://images.pokemontcg.io/pl3/143.png",
        "dpp-DP45": "https://images.pokemontcg.io/dpp/DP45.png",
        "pl4-1": "https://images.pokemontcg.io/pl4/1.png",
        "bw7-20": "https://images.pokemontcg.io/bw7/20.png",
        "bw8-136": "https://images.pokemontcg.io/bw8/136.png",
        "xy2-11": "https://images.pokemontcg.io/xy2/11.png",
        "xy2-100": "https://images.pokemontcg.io/xy2/100.png",
        "xy2-13": "https://images.pokemontcg.io/xy2/13.png",
        "xy2-107": "https://images.pokemontcg.io/xy2/107.png",
        "xy2-69": "https://images.pokemontcg.io/xy2/69.png",
        "xy2-108": "https://images.pokemontcg.io/xy2/108.png",
        "xyp-XY17": "https://images.pokemontcg.io/xyp/XY17.png",
        "g1-12": "https://images.pokemontcg.io/g1/12.png",
        "xy12-11": "https://www.cardtrader.com/uploads/blueprints/image/118329/show_charizard-rare-holo-11-108-evolutions.jpg",
        "xy12-81": "https://images.scrydex.com/pokemon/xy12-75/medium",
        "xy12-101": "https://images.pokemontcg.io/xy12/101.png",
        "sm3-20": "https://images.pokemontcg.io/sm3/20.png",
        "sm3-150-rb": "https://images.pokemontcg.io/sm3/150.png",
        "smp-SM60": "https://images.pokemontcg.io/smp/SM60.png",
        "sm75-3": "https://images.pokemontcg.io/sm75/3.png",
        "sm9-14": "https://images.pokemontcg.io/sm9/14.png",
        "det1-5": "https://images.pokemontcg.io/det1/5.png",
        "sm10-20": "https://images.pokemontcg.io/sm10/20.png",
        "smp-SM226": "https://images.scrydex.com/pokemon/smp-SM226/medium",
        "sm115sv-SV49": "https://images.scrydex.com/pokemon/sma-SV49/medium",
        "sm12-22": "https://images.pokemontcg.io/sm12/22.png",
        "swsh3-20": "https://images.pokemontcg.io/swsh3/20.png",
        "swsh35-074": "https://images.scrydex.com/pokemon/swsh35-74/medium",
        "swsh35-079": "https://images.scrydex.com/pokemon/swsh35-79/medium",
        "swsh4-025": "https://images.scrydex.com/pokemon/swsh4-25/medium",
        "swshp-SWSH075": "https://images.scrydex.com/pokemon/swshp-SWSH075/medium",
        "swsh45sv-SV107": "https://images.pokemontcg.io/swsh45sv/SV107.png",
        "swshp-SWSH261": "https://images.scrydex.com/pokemon/swshp-SWSH133/medium",  # <-- Immagine corretta inserita qui
        "cel25-4": "https://images.scrydex.com/pokemon/cel25c-4_A/medium",
        "swsh9-154": "https://images.pokemontcg.io/swsh9/154.png",
        "swsh9-174": "https://images.pokemontcg.io/swsh9/174.png",
        "swsh9tg-TG03": "https://images.scrydex.com/pokemon/swsh11tg-TG03/medium",
        "pgo-11": "https://images.pokemontcg.io/pgo/11.png",
        "swshp-SWSH260": "https://images.pokemontcg.io/swshp/SWSH260.png",
        "swshp-SWSH261-upc": "https://images.pokemontcg.io/swshp/SWSH261.png",
        "swshp-SWSH262": "https://images.pokemontcg.io/swshp/SWSH262.png",
        "sv3-125": "https://images.pokemontcg.io/sv3/125.png",
        "sv3-215": "https://images.pokemontcg.io/sv3/215.png",
        "sv3-223": "https://images.pokemontcg.io/sv3/223.png",
        "sv3-228": "https://images.pokemontcg.io/sv3/228.png",
        "sv3pt5-006": "https://images.scrydex.com/pokemon/sv3pt5-6/medium",
        "sv3pt5-183": "https://images.scrydex.com/pokemon/sv3pt5-183/medium",
        "sv3pt5-199": "https://images.pokemontcg.io/sv3pt5/199.png",
        "svp-56": "https://images.pokemontcg.io/svp/56.png",
        "sv4pt5-234": "https://images.pokemontcg.io/sv4pt5/234.png",
        "sv6-mega1": "https://images.scrydex.com/pokemon/me2-13/medium",
        "sv6-mega2": "https://images.scrydex.com/pokemon/me2-109/medium",
        "sv6-mega3": "https://images.scrydex.com/pokemon/me2-125/medium",
        "sv6-mega4": "https://images.scrydex.com/pokemon/me2-130/medium",
        "sv6-mega5": "https://images.scrydex.com/pokemon/mep-30/medium"
    }

all_images = load_all_images()

# Database delle carte
@st.cache_data
def load_data():
    data = [
        {"Anno": "1996-1997", "Era": "L'Era Classica WOTC", "Nome": "Charizard Topsun", "Info": "Retro Blu, Retro Verde, No Number", "Img_ID": "topsun"},
        {"Anno": "1996-1997", "Era": "L'Era Classica WOTC", "Nome": "Charizard Carddass Bandai", "Info": "Prism e Regular per distributori automatici", "Img_ID": "carddass"},
        {"Anno": "1998", "Era": "L'Era Classica WOTC", "Nome": "Charizard CD Promo #6", "Info": "Esclusiva olografica giapponese (CD Promo)", "Img_ID": "cd_promo"},
        {"Anno": "1999", "Era": "L'Era Classica WOTC", "Nome": "Charizard Set Base #4/102", "Info": "1st Edition, Shadowless, Unlimited, 4th Print", "Img_ID": "base1-4"},
        {"Anno": "1999-2000", "Era": "L'Era Classica WOTC", "Nome": "Charizard Topps Anime", "Info": "Serie Anime: Regular, Foil, Rainbow, Chrome", "Img_ID": "topps"},
        {"Anno": "2000", "Era": "L'Era Classica WOTC", "Nome": "Charizard Set Base 2 #4/130", "Info": "Ristampa celebrativa del set base originale", "Img_ID": "base2-4"},
        {"Anno": "2000", "Era": "L'Era Classica WOTC", "Nome": "Dark Charizard (Charizard Oscuro) #4/82", "Info": "Team Rocket #4/82 (Olo)", "Img_ID": "rocket1-4"},
        {"Anno": "2000", "Era": "L'Era Classica WOTC", "Nome": "Blaine's Charizard #2/132", "Info": "Gym Challenge #2/132 (Variante Errata)", "Img_ID": "gym2-2"},
        {"Anno": "2000", "Era": "L'Era Classica WOTC", "Nome": "Charizard Intro Pack Neo", "Info": "Mazzo didattico giapponese, artwork unico non-olo", "Img_ID": "intro-neo"},
        {"Anno": "2002", "Era": "L'Era Classica WOTC", "Nome": "Shining Charizard (Lucente) #107/105", "Info": "Neo Destiny #107/105 - Cromatico", "Img_ID": "neo4-107"},
        {"Anno": "2002", "Era": "L'Era Classica WOTC", "Nome": "Charizard e-Card Expedition #6/165", "Info": "Expedition Base Set #6/165 e Reverse", "Img_ID": "ecard1-6"},
        {"Anno": "2002", "Era": "L'Era Classica WOTC", "Nome": "Charizard Legendary Collection #3/110", "Info": "Olo, Non-Olo e Reverse Holo a fuochi d'artificio", "Img_ID": "lc-3"},
        {"Anno": "2003", "Era": "L'Era Classica WOTC", "Nome": "Crystal Charizard (Cristallino) #146/144", "Info": "Skyridge #146/144 - Tipo Incolore e Reverse", "Img_ID": "skyridge-146"},
        {"Anno": "2003", "Era": "L'Era EX", "Nome": "Charizard Segreto EX Dragon #100/97", "Info": "EX Dragon #100/97 Secret Rare", "Img_ID": "ex3-100"},
        {"Anno": "2004", "Era": "L'Era EX", "Nome": "Charizard ex RossoFuoco/VerdeFoglia #105/112", "Info": "EX RossoFuoco & VerdeFoglia #105/112", "Img_ID": "ex6-105"},
        {"Anno": "2006", "Era": "L'Era EX", "Nome": "Charizard Delta Species #4/100", "Info": "EX Guardiani dei Cristalli #4/100 - Elettro/Metallo", "Img_ID": "ex14-4"},
        {"Anno": "2006", "Era": "L'Era EX", "Nome": "Charizard Star Shiny #100/101", "Info": "EX Dragon Frontiers #100/101 - Shiny Tipo Oscurità", "Img_ID": "ex15-100"},
        {"Anno": "2007", "Era": "L'Era EX", "Nome": "Charizard EX Power Keepers #6/108", "Info": "EX Power Keepers #6/108", "Img_ID": "ex16-6"},
        {"Anno": "2007", "Era": "L'Era EX", "Nome": "Charizard Secret Wonders #3/132", "Info": "Secret Wonders #3/132", "Img_ID": "dp3-3"},
        {"Anno": "2009", "Era": "L'Era EX", "Nome": "Charizard G LV.X #143/147", "Info": "Platino Re dei Supremi #143/147", "Img_ID": "pl3-143"},
        {"Anno": "2009", "Era": "L'Era EX", "Nome": "Charizard G LV.X Promo #DP45", "Info": "Diamond & Pearl Promo #DP45", "Img_ID": "dpp-DP45"},
        {"Anno": "2009", "Era": "L'Era EX", "Nome": "Charizard Base Set Reprint Platino #1/99", "Info": "Platino Arceus #1/99", "Img_ID": "pl4-1"},
        {"Anno": "2012", "Era": "L'Era EX", "Nome": "Charizard Ascesa Eroica #20/149", "Info": "Boundaries Cross #20/149", "Img_ID": "bw7-20"},
        {"Anno": "2013", "Era": "L'Era EX", "Nome": "Charizard Shiny Segreto Uragano Plasma #136/135", "Info": "Uragano Plasma #136/135 - Rara segreta dorata", "Img_ID": "bw8-136"},
        {"Anno": "2014", "Era": "L'Era XY", "Nome": "Charizard-EX Fuoco Infernale #11/106", "Info": "XY Fuoco Infernale #11/106", "Img_ID": "xy2-11"},
        {"Anno": "2014", "Era": "L'Era XY", "Nome": "Charizard-EX Full Art Fuoco Infernale #100/106", "Info": "XY Fuoco Infernale #100/106", "Img_ID": "xy2-100"},
        {"Anno": "2014", "Era": "L'Era XY", "Nome": "M Charizard-EX Y #13/106", "Info": "Fuoco Infernale #13/106", "Img_ID": "xy2-13"},
        {"Anno": "2014", "Era": "L'Era XY", "Nome": "M Charizard-EX Y Secret Oro #107/106", "Info": "Fuoco Infernale #107/106", "Img_ID": "xy2-107"},
        {"Anno": "2014", "Era": "L'Era XY", "Nome": "M Charizard-EX X #69/106", "Info": "Fuoco Infernale #69/106", "Img_ID": "xy2-69"},
        {"Anno": "2014", "Era": "L'Era XY", "Nome": "M Charizard-EX X Secret Oro #108/106", "Info": "Fuoco Infernale #108/106", "Img_ID": "xy2-108"},
        {"Anno": "2014", "Era": "L'Era XY", "Nome": "Charizard-EX Promo #XY17", "Info": "XY Promo #XY17", "Img_ID": "xyp-XY17"},
        {"Anno": "2016", "Era": "L'Era XY", "Nome": "Charizard-EX Generazioni #12/83", "Info": "Generazioni #12/83 EX", "Img_ID": "g1-12"},
        {"Anno": "2016", "Era": "L'Era XY", "Nome": "Charizard XY Evoluzioni #11/108", "Info": "XY Evoluzioni #11/108 - Remake Set Base", "Img_ID": "xy12-11"},
        {"Anno": "2016", "Era": "L'Era XY", "Nome": "Charizard Spirit Link XY Evoluzioni #75/108", "Info": "XY Evoluzioni #75/108 Spirit Link", "Img_ID": "xy12-81"},
        {"Anno": "2016", "Era": "L'Era XY", "Nome": "M Charizard-EX Full Art XY Evoluzioni #101/108", "Info": "XY Evoluzioni #101/108", "Img_ID": "xy12-101"},
        {"Anno": "2017", "Era": "L'Era Sole & Luna", "Nome": "Charizard-GX Ombre Infuocate #20/147", "Info": "Ombre Infuocate #20/147", "Img_ID": "sm3-20"},
        {"Anno": "2017", "Era": "L'Era Sole & Luna", "Nome": "Charizard-GX Rainbow Secret #150/147", "Info": "Ombre Infuocate #150/147 (Secret Rainbow)", "Img_ID": "sm3-150-rb"},
        {"Anno": "2017", "Era": "L'Era Sole & Luna", "Nome": "Charizard-GX Full Art Promo #SM60", "Info": "SM Promo #SM60 Premium Collection", "Img_ID": "smp-SM60"},
        {"Anno": "2018", "Era": "L'Era Sole & Luna", "Nome": "Charizard Dragon Majesty #3/70", "Info": "Dragon Majesty #3/70", "Img_ID": "sm75-3"},
        {"Anno": "2019", "Era": "L'Era Sole & Luna", "Nome": "Charizard Gioco di Squadra #14/181", "Info": "Gioco di Squadra #14/181", "Img_ID": "sm9-14"},
        {"Anno": "2019", "Era": "L'Era Sole & Luna", "Nome": "Charizard Detective Pikachu #5/18", "Info": "Detective Pikachu #5/18 Special Set", "Img_ID": "det1-5"},
        {"Anno": "2019", "Era": "L'Era Sole & Luna", "Nome": "Reshiram & Charizard-GX ALLEATI #20/214", "Info": "Legami Inossidabili #20/214 Tag Team", "Img_ID": "sm10-20"},
        {"Anno": "2019", "Era": "L'Era Sole & Luna", "Nome": "Clone Charizard Mewtwo Strikes Back Promo (2019)", "Info": "Mewtwo Strikes Back Evolution Special Promo", "Img_ID": "smp-SM226"},
        {"Anno": "2019", "Era": "L'Era Sole & Luna", "Nome": "Charizard-GX Shiny Destino Sfuggente #SV49", "Info": "Destino Sfuggente #SV49 Shiny Vault", "Img_ID": "sm115sv-SV49"},
        {"Anno": "2019", "Era": "L'Era Sole & Luna", "Nome": "Charizard & Braixen-GX ALLEATI #22/236", "Info": "Eclissi Cosmica #22/236 Tag Team", "Img_ID": "sm12-22"},
        {"Anno": "2020", "Era": "L'Era Spada & Scudo", "Nome": "Charizard-VMAX Fiamme Oscure #20/189", "Info": "Fiamme Oscure #20/189 VMAX", "Img_ID": "swsh3-20"},
        {"Anno": "2020", "Era": "L'Era Spada & Scudo", "Nome": "Charizard-VMAX Arcobaleno Futuro Campione #074", "Info": "Futuro Campione #074 Arcobaleno", "Img_ID": "swsh35-074"},
        {"Anno": "2020", "Era": "L'Era Spada & Scudo", "Nome": "Charizard-V Shiny Futuro Campione #079", "Info": "Futuro Campione #079 Cromatico", "Img_ID": "swsh35-079"},
        {"Anno": "2020", "Era": "L'Era Spada & Scudo", "Nome": "Charizard (Leon) Voltaggio Sfolgorante #025/185", "Info": "Voltaggio Sfolgorante #025/185", "Img_ID": "swsh4-025"},
        {"Anno": "2020", "Era": "L'Era Spada & Scudo", "Nome": "Special Delivery Charizard Promo #SWSH075", "Info": "Promo Pokémon Center #SWSH075", "Img_ID": "swshp-SWSH075"},
        {"Anno": "2021", "Era": "L'Era Spada & Scudo", "Nome": "Charizard-VMAX Cromatico Destino Splendente #SV107", "Info": "Destino Splendente #SV107 Shiny VMAX", "Img_ID": "swsh45sv-SV107"},
        {"Anno": "2021", "Era": "L'Era Spada & Scudo", "Nome": "Charizard di Lance V Promo Gran Festa #SWSH261", "Info": "Gran Festa Promo Special V", "Img_ID": "swshp-SWSH261"},
        {"Anno": "2021", "Era": "L'Era Spada & Scudo", "Nome": "Charizard Ristampa Set Base Gran Festa #4/102", "Info": "Ristampa Classica 25° Anniversario", "Img_ID": "cel25-4"},
        {"Anno": "2022", "Era": "L'Era Spada & Scudo", "Nome": "Charizard-V Alternate Art Astri Lucenti #154/172", "Info": "Astri Lucenti Alt Art #154/172", "Img_ID": "swsh9-154"},
        {"Anno": "2022", "Era": "L'Era Spada & Scudo", "Nome": "Charizard-VSTAR Rainbow Astri Lucenti #174/172", "Info": "Astri Lucenti #174/172 Rainbow", "Img_ID": "swsh9-174"},
        {"Anno": "2022", "Era": "L'Era Spada & Scudo", "Nome": "Charizard (Leon) Trainer Gallery Astri Lucenti #TG03", "Info": "Astri Lucenti #TG03 Trainer Gallery", "Img_ID": "swsh9tg-TG03"},
        {"Anno": "2022", "Era": "L'Era Spada & Scudo", "Nome": "Charizard Lucente (Radiant) Pokémon GO #11/78", "Info": "Pokémon GO #11/78 Radiant Shiny", "Img_ID": "pgo-11"},
        {"Anno": "2022", "Era": "L'Era Spada & Scudo", "Nome": "Charizard-V Promo UPC #SWSH260", "Info": "Special Illustration Promo UPC #SWSH260", "Img_ID": "swshp-SWSH260"},
        {"Anno": "2022", "Era": "L'Era Spada & Scudo", "Nome": "Charizard-VMAX Promo UPC #SWSH261", "Info": "Special Illustration Promo UPC #SWSH261", "Img_ID": "swshp-SWSH261-upc"},
        {"Anno": "2022", "Era": "L'Era Spada & Scudo", "Nome": "Charizard-VSTAR Promo UPC #SWSH262", "Info": "Special Illustration Promo UPC #SWSH262", "Img_ID": "swshp-SWSH262"},
        {"Anno": "2023", "Era": "L'Era Scarlatto & Violetto", "Nome": "Charizard ex Teracristal Ossidiana Infuocata #125/197", "Info": "Ossidiana Infuocata #125/197 ex Double Rare", "Img_ID": "sv3-125"},
        {"Anno": "2023", "Era": "L'Era Scarlatto & Violetto", "Nome": "Charizard ex Tera Full Art Ossidiana Infuocata #215/197", "Info": "Ossidiana Infuocata #215/197 Full Art", "Img_ID": "sv3-215"},
        {"Anno": "2023", "Era": "L'Era Scarlatto & Violetto", "Nome": "Charizard ex Teracristal SIR Ossidiana Infuocata #223/197", "Info": "Ossidiana Infuocata #223/197 Special Illustration Rare", "Img_ID": "sv3-223"},
        {"Anno": "2023", "Era": "L'Era Scarlatto & Violetto", "Nome": "Charizard ex Tera Gold Secret Ossidiana Infuocata #228/197", "Info": "Ossidiana Infuocata #228/197 Hyper Rare Gold", "Img_ID": "sv3-228"},
        {"Anno": "2023", "Era": "L'Era Scarlatto & Violetto", "Nome": "Charizard ex Kanto SV 151 #006/165", "Info": "Scarlatto e Violetto 151 #006/165", "Img_ID": "sv3pt5-006"},
        {"Anno": "2023", "Era": "L'Era Scarlatto & Violetto", "Nome": "Charizard ex Kanto Full Art SV 151 #183/165", "Info": "Scarlatto e Violetto 151 #183/165 Full Art", "Img_ID": "sv3pt5-183"},
        {"Anno": "2023", "Era": "L'Era Scarlatto & Violetto", "Nome": "Charizard ex Kanto SIR SV 151 #199/165", "Info": "Scarlatto e Violetto 151 #199/165 Special Illustration Rare", "Img_ID": "sv3pt5-199"},
        {"Anno": "2023", "Era": "L'Era Scarlatto & Violetto", "Nome": "Charizard ex Tin Promo #SV056", "Info": "Promo SV #056 Tin ex Product", "Img_ID": "svp-56"},
        {"Anno": "2024", "Era": "L'Era Scarlatto & Violetto", "Nome": "Charizard ex Tera Shiny SIR Destino di Paldea #234/091", "Info": "Destino di Paldea #234/091 Special Illustration Rare", "Img_ID": "sv4pt5-234"},
        {"Anno": "2025", "Era": "L'Era Megaevoluzioni", "Nome": "Mega Charizard X ex Fiamme Spettrali #013", "Info": "Espansione Megaevoluzione — Fiamme Spettrali #013/094", "Img_ID": "sv6-mega1"},
        {"Anno": "2025", "Era": "L'Era Megaevoluzioni", "Nome": "Mega Charizard X ex Full Art #109", "Info": "Espansione Megaevoluzione — Fiamme Spettrali #109/094", "Img_ID": "sv6-mega2"},
        {"Anno": "2025", "Era": "L'Era Megaevoluzioni", "Nome": "Mega Charizard X ex SIR #125", "Info": "Espansione Megaevoluzione — Fiamme Spettrali #125/094", "Img_ID": "sv6-mega3"},
        {"Anno": "2025", "Era": "L'Era Megaevoluzioni", "Nome": "Mega Charizard X ex Gold #228", "Info": "Espansione Megaevoluzione — Fiamme Spettrali #130/094", "Img_ID": "sv6-mega4"},
        {"Anno": "2025", "Era": "L'Era Megaevoluzioni", "Nome": "Mega Charizard Y ex Mazzo Speciale (2025)", "Info": "Set d'accompagnamento / Mazzo Tematico speciale", "Img_ID": "sv6-mega5"}
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
                img_url = all_images.get(row["Img_ID"], "https://via.placeholder.com/150x210?text=Charizard")
                st.image(img_url, width=160)
            with col2:
                st.markdown(f"### {row['Nome']}")
                st.caption(f"📅 **Anno:** {row['Anno']} | 🏛️ **Era:** {row['Era']}")
                st.write(f"📝 *{row['Info']}*")
                
                owned = st.checkbox("Ce l'ho in collezione", key=key_id, value=st.session_state.binder.get(key_id, False))
                st.session_state.binder[key_id] = owned
                
                if owned:
                    st.success("✅ Aggiunto al tuo Binder!")
            
            # --- SEZIONE PREZZI ---
            with col3:
                st.markdown("📊 **Market Analytics (Cardmarket Real-time)**")
                
                dati_cm = fetch_cardmarket_prices(row["Img_ID"])
                
                if dati_cm["Stato"] == "Successo" and dati_cm["Prezzo_Trend"] > 0:
                    st.metric(
                        label="Prezzo Trend Cardmarket", 
                        value=f"€ {dati_cm['Prezzo_Trend']:.2f}", 
                        delta=f"Minimo: € {dati_cm['Prezzo_Low']:.2f}",
                        delta_color="off"
                    )
                    st.markdown("**Andamento storico vendite:**")
                    st.text(f"🔸 Media odierna: € {dati_cm['Prezzo_Avg1']:.2f}")
                    st.text(f"🔸 Media ultimi 30 giorni: € {dati_cm['Prezzo_Avg30']:.2f}")
                    st.markdown(f"[🛒 Vedi su Cardmarket]({dati_cm['Link_Cardmarket']})")
                
                else:
                    if "Base" in row["Nome"] or "Shining" in row["Nome"] or "Crystal" in row["Nome"] or "Star" in row["Nome"]:
                        prezzo_stimato = 650.00
                    elif "ex" in row["Nome"].lower() and "2004" in row["Anno"]:
                        prezzo_stimato = 250.00
                    elif "Topsun" in row["Nome"] or "Carddass" in row["Nome"]:
                        prezzo_stimato = 400.00
                    else:
                        prezzo_stimato = 45.00
                    
                    st.metric(label="Prezzo di Mercato (Stima)", value=f"€ {prezzo_stimato:.2f}")
                    st.caption("⚠️ *Dati Cardmarket live non disponibili per questo ID specifico o server temporaneamente occupati.*")
                    st.markdown("**Stime condizioni:**")
                    st.text(f"🔸 Mint (Perfetta): € {prezzo_stimato * 1.6:.2f}")
                    st.text(f"🔸 Near Mint (Ottima): € {prezzo_stimato:.2f}")
            st.divider()