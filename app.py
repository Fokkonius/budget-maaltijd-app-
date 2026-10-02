import streamlit as st

# Pagina configuratie
st.set_page_config(
    page_title="Mijn Slimme Budget & Bulk Assistent",
    page_icon="🛒",
    layout="wide",
)

st.title("🛒 Slimme Maaltijd-, Bulk- & Prijsvergelijker")
st.markdown("Jouw private app met profielen voor aan boord en thuis.")

# --- SESSION STATE VOOR PROFIELEN ---
if "profielen" not in st.session_state:
  st.session_state.profielen = {
      "⚓ Aan Boord": {
          "personen": 2,
          "budget": 50,
          "keuken": "Snel, makkelijk & praktisch",
          "exclusies": "rauwe eidooiers, asperges, feta, olijven, geitenkaas",
      },
      "🏠 Thuis (Gezin)": {
          "personen": 4,
          "budget": 110,
          "keuken": "Kindvriendelijk & Gezond",
          "exclusies": (
              "rauwe eidooiers, asperges, feta, olijven, geitenkaas, te sterk"
              " gekruid / pikant"
          ),
      },
  }

if "favorieten" not in st.session_state:
  st.session_state.favorieten = [
      {
          "naam": "Page Kussen Zacht Wc-papier",
          "eenheid": "Per rol",
          "doel_prijs": 0.22,
          "winkels": ["Bol.com", "Amazon.nl", "Albert Heijn"],
      }
  ]

# --- ZIJBANK: PROFIEL SELECTIE ---
st.sidebar.header("👤 Situatie / Profiel")
geselecteerd_profiel = st.sidebar.selectbox(
    "Kies waar je bent", list(st.session_state.profielen.keys())
)

# Laad de instellingen van het gekozen profiel
profiel_data = st.session_state.profielen[geselecteerd_profiel]

st.sidebar.markdown(f"**Actieve instellingen voor {geselecteerd_profiel}:**")
huidige_personen = st.sidebar.slider(
    "Aantal personen", 1, 8, profiel_data["personen"], key="p_aantal"
)
huidig_budget = st.sidebar.number_input(
    "Totaal weekbudget (€)",
    min_value=20,
    max_value=400,
    value=profiel_data["budget"],
    step=5,
    key="p_bud",
)
huidige_exclusies = st.sidebar.text_input(
    "Wat wordt er niet gelust (uitsluiten):",
    value=profiel_data["exclusies"],
    key="p_exc",
)

# Sla aanpassingen op in de state
st.session_state.profielen[geselecteerd_profiel]["personen"] = huidige_personen
st.session_state.profielen[geselecteerd_profiel]["budget"] = huidig_budget
st.session_state.profielen[geselecteerd_profiel]["exclusies"] = huidige_exclusies

st.sidebar.divider()

# --- TABS VOOR NAVIGATIE ---
tab_menu, tab_bulk, tab_favorieten, tab_alerts = st.tabs(
    [
        "🍳 Weekmenu",
        "📦 Bulk & Non-Food",
        "⭐ Favorieten",
        "🔔 Prijs-Alerts",
    ]
)

# --- TAB 1: WEEKMENU ---
with tab_menu:
  st.subheader(
      f"Plan je weekmenu voor: *{geselecteerd_profiel}* ({huidige_personen}"
      f" personen)"
  )

  geselecteerde_supermarkten = st.multiselect(
      "Actieve supermarkten in deze omgeving:",
      [
          "Albert Heijn",
          "Jumbo",
          "Lidl",
          "PLUS",
          "Dirk",
          "Hoogvliet",
          "Bol.com",
          "Amazon.nl",
      ],
      default=["Albert Heijn", "Jumbo", "Lidl", "PLUS"],
  )

  keuken_stijl = st.selectbox(
      "Keukenstijl / Focus",
      [
          "Geen voorkeur / Mix",
          "Mediterraans",
          "Hollandse pot",
          "Thais",
          "Chinees / Aziatisch",
          "Kindvriendelijk / Simpel",
      ],
  )

  if st.button("🚀 Genereer Weekmenu & Boodschappenlijst", type="primary"):
    st.success(
        f"Menu gegenereerd voor **{geselecteerd_profiel}** met een budget van"
        f" €{huidig_budget}!"
    )
    if "Thuis" in geselecteerd_profiel:
      st.info(
          "💡 *Rekening gehouden met de smaken van de kinderen (geen verrassende"
          " structuren of scherpe smaken).*️️"
      )
    else:
      st.info(
          "💡 *Gerechten geoptimaliseerd voor snelle bereiding aan boord.*"
      )

    st.markdown(
        """
        * **Maandag:** Kindvriendelijke milde pastaschotel met verborgen groenten.
        * **Dinsdag:** Hollandse kookpot / stamppot.
        """
    )

# --- TAB 2: BULK & NON-FOOD ---
with tab_bulk:
  st.subheader("📦 Bulk-inkoop & Vergelijken")
  zoek_item = st.text_input(
      "Zoek product voor bulk:", value="Page kussen zacht wc papier"
  )
  if st.button("🔍 Vergelijk Bulk-opties"):
    st.markdown("""
        | Aanbieder | Totaalprijs | Verzendkosten | Prijs per eenheid | Status |
        | :--- | :--- | :--- | :--- | :--- |
        | **Amazon.nl** | € 24,99 | € 0,00 (Gratis) | **€ 0,22 per rol** | ⭐ **Beste keuze** |
        | **Bol.com** | € 27,50 | € 0,00 (Gratis) | € 0,24 per rol | Goed alternatief |
        """)

# --- TAB 3: MIJN FAVORIETE PRODUCTEN ---
with tab_favorieten:
  st.subheader("⭐ Jouw Vaste Huishoudelijke Producten")
  for fav in st.session_state.favorieten:
    st.markdown(
        f"**{fav['naam']}** – Doelprijs: €{fav['doel_prijs']:.2f}"
        f" ({fav['eenheid']})"
    )

# --- TAB 4: PRIJS-ALERTS ---
with tab_alerts:
  st.subheader("🔔 Actieve Prijs-Alerts")
  for fav in st.session_state.favorieten:
    st.markdown(
        f"✅ **{fav['naam']}** – Alert actief onder **€{fav['doel_prijs']:.2f}**"
    )
