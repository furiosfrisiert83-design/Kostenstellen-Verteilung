import streamlit as st
import pandas as pd
from io import BytesIO

# ============================================================================
# 1. SEITENEINSTELLUNGEN
# ============================================================================
st.set_page_config(
    page_title="Kostenstellen-Verteilung",
    layout="wide",
    page_icon="💰",
)

st.title("💰 Kostenstellen-Verteilungstool")
st.caption("Rechnungspositionen auf Kostenstellen verteilen – mit MwSt.-Option")

# ============================================================================
# 2. SESSION STATE INITIALISIERUNG
# ============================================================================
if "kostenstellen_df" not in st.session_state:
    st.session_state.kostenstellen_df = None

if "rechnungspositionen" not in st.session_state:
    st.session_state.rechnungspositionen = []

if "mwst_modus" not in st.session_state:
    st.session_state.mwst_modus = "brutto"  # "brutto" oder "netto"

# ============================================================================
# 3. SIDEBAR – EINSTELLUNGEN
# ============================================================================
st.sidebar.header("⚙️ Einstellungen")

# Eingabemodus: Was gibt der Benutzer ein?
if "eingabe_modus" not in st.session_state:
    st.session_state.eingabe_modus = "netto"

eingabe_modus = st.sidebar.radio(
    "Eingabewerte sind:",
    options=["Netto (ohne MwSt.)", "Brutto (mit 19% MwSt.)"],
    index=0 if st.session_state.eingabe_modus == "netto" else 1,
    help="Was steht auf deiner Rechnung? Normalerweise Netto.",
)
st.session_state.eingabe_modus = "netto" if "Netto" in eingabe_modus else "brutto"

# Anzeigemodus: Was soll angezeigt werden?
if "anzeige_modus" not in st.session_state:
    st.session_state.anzeige_modus = "netto"

anzeige_modus = st.sidebar.radio(
    "Anzeige als:",
    options=["Netto", "Brutto"],
    index=0 if st.session_state.anzeige_modus == "netto" else 1,
    help="Soll das Ergebnis als Netto oder Brutto angezeigt werden?",
)
st.session_state.anzeige_modus = "netto" if anzeige_modus == "Netto" else "brutto"

# Info-Box bei unterschiedlichen Modi
if st.session_state.eingabe_modus != st.session_state.anzeige_modus:
    if st.session_state.eingabe_modus == "netto" and st.session_state.anzeige_modus == "brutto":
        st.sidebar.info("💡 Rechne Netto → Brutto (×1,19)")
    else:
        st.sidebar.info("💡 Rechne Brutto → Netto (÷1,19)")

st.sidebar.markdown("---")
st.sidebar.header("🧮 Brutto/Netto-Rechner")

# Unabhängiger Rechner (ohne Formular, damit es sich automatisch aktualisiert)
st.caption("Schnellumrechnung zwischen Netto und Brutto")

rechner_modus = st.sidebar.radio(
    "Modus:",
    options=["Netto → Brutto", "Brutto → Netto"],
    horizontal=True,
)

if rechner_modus == "Netto → Brutto":
    netto_wert = st.sidebar.number_input("Netto-Betrag (€)", min_value=0.0, step=0.01, format="%.2f", key="rechner_netto")
    brutto_wert = netto_wert * 1.19
    st.sidebar.success(f"**Brutto: {brutto_wert:,.2f} €**")
else:
    brutto_wert = st.sidebar.number_input("Brutto-Betrag (€)", min_value=0.0, step=0.01, format="%.2f", key="rechner_brutto")
    netto_wert = brutto_wert / 1.19
    st.sidebar.success(f"**Netto: {netto_wert:,.2f} €**")

st.sidebar.markdown("---")
st.sidebar.header("📋 Kostenstellenliste")

# Feste Kostenstellenliste (20 Stück, anonymisiert)
kostenstellen_liste = [
    (i, f"Kostenstelle {i}") for i in range(1, 21)
]
df_ks = pd.DataFrame(kostenstellen_liste, columns=["Kostenstelle", "Bezeichnung"])
st.session_state.kostenstellen_df = df_ks
st.sidebar.success(f"✅ {len(df_ks)} Kostenstellen geladen (fest integriert)")

# Kostenstellenliste anzeigen
with st.sidebar.expander("📄 Geladene Kostenstellen"):
    st.dataframe(st.session_state.kostenstellen_df, hide_index=True, use_container_width=True)

# ============================================================================
# 4. HAUPTBEREICH – RECHNUNGSEINGABE
# ============================================================================
if st.session_state.kostenstellen_df is None:
    st.warning("⚠️ Bitte zuerst eine Kostenstellenliste in der Sidebar hochladen.")
    st.stop()

df_ks = st.session_state.kostenstellen_df
liste_ks_nummern = df_ks["Kostenstelle"].tolist()
liste_ks_bezeichnungen = [f"{row.Kostenstelle} – {row.Bezeichnung}" for row in df_ks.itertuples()]

st.markdown("---")
st.subheader("📝 Rechnungspositionen eingeben")

# Eingabeformular für eine neue Position
with st.form("neue_position", clear_on_submit=True):
    col1, col2, col3 = st.columns([2, 1, 2])

    with col1:
        pos_name = st.text_input("Positionsbezeichnung", placeholder="z.B. Portokosten, Beratung, ...")

    with col2:
        pos_betrag = st.number_input("Betrag (€)", min_value=0.0, step=0.01, format="%.2f")

    with col3:
        verteilungs_art = st.selectbox(
            "Verteilung auf:",
            options=[
                "Einzelne Kostenstelle",
                "Gleichmäßig auf alle Kostenstellen",
                "Gleichmäßig auf verwendete Kostenstellen",
            ],
        )

    # Bereits verwendete Kostenstellen sammeln (für "Gleichmäßig auf verwendete")
    verwendete_kostenstellen = set()
    for pos in st.session_state.rechnungspositionen:
        verwendete_kostenstellen.update(pos["Ziel_Kostenstellen"])

    # Dynamische Auswahl je nach Verteilungsart
    ziel_kostenstellen = []
    if verteilungs_art == "Einzelne Kostenstelle":
        auswahl = st.multiselect(
            "Ziel-Kostenstelle(n):",
            options=liste_ks_nummern,
            format_func=lambda x: f"{x} – {df_ks.loc[df_ks['Kostenstelle']==x, 'Bezeichnung'].values[0]}",
        )
        ziel_kostenstellen = auswahl
    elif verteilungs_art == "Gleichmäßig auf alle Kostenstellen":
        ziel_kostenstellen = liste_ks_nummern
        st.info(f"ℹ️ Verteile auf alle {len(liste_ks_nummern)} Kostenstellen")
    elif verteilungs_art == "Gleichmäßig auf verwendete Kostenstellen":
        if verwendete_kostenstellen:
            # Zeige Info über verwendete KS, aber keine Auswahl – verteile auf ALLE verwendeten
            st.info(f"ℹ️ Verteile auf alle {len(verwendete_kostenstellen)} verwendeten Kostenstellen: {', '.join(map(str, sorted(verwendete_kostenstellen)))}")
            ziel_kostenstellen = list(verwendete_kostenstellen)
        else:
            ziel_kostenstellen = liste_ks_nummern
            st.warning("⚠️ Noch keine Kostenstellen verwendet – verteile auf alle.")

    submitted = st.form_submit_button("➕ Position hinzufügen", use_container_width=True)

    if submitted:
        if not pos_name or pos_betrag <= 0:
            st.error("Bitte Bezeichnung und positiven Betrag eingeben.")
        elif verteilungs_art == "Einzelne Kostenstelle" and not ziel_kostenstellen:
            st.error("Bitte mindestens eine Kostenstelle auswählen (Strg+Klick für mehrere).")
        else:
            # Fallback-Logik: Nur bei "Gleichmäßig auf alle/verwendete" erlauben
            if verteilungs_art == "Einzelne Kostenstelle":
                finale_ziel_ks = ziel_kostenstellen  # Muss ausgewählt sein, kein Fallback!
            else:
                finale_ziel_ks = ziel_kostenstellen if ziel_kostenstellen else liste_ks_nummern

            neue_position = {
                "Positionsname": pos_name,
                "Betrag": pos_betrag,
                "Verteilungsart": verteilungs_art,
                "Ziel_Kostenstellen": finale_ziel_ks,
            }
            st.session_state.rechnungspositionen.append(neue_position)
            st.success(f"✅ Position '{pos_name}' hinzugefügt")
            st.rerun()

# ============================================================================
# 5. EINGEGEBENE POSITIONEN ANZEIGEN & LÖSCHEN
# ============================================================================
if st.session_state.rechnungspositionen:
    st.markdown("### 📋 Eingegebene Positionen")

    df_pos = pd.DataFrame(st.session_state.rechnungspositionen)
    df_pos["Ziel_Kostenstellen_Anzeige"] = df_pos["Ziel_Kostenstellen"].apply(
        lambda ks_list: ", ".join([f"{k} ({df_ks.loc[df_ks['Kostenstelle']==k, 'Bezeichnung'].values[0]})" for k in ks_list])
    )

    anzeige_df = df_pos[["Positionsname", "Betrag", "Verteilungsart", "Ziel_Kostenstellen_Anzeige"]].copy()
    anzeige_df.columns = ["Position", "Betrag (€)", "Verteilung", "Ziel-Kostenstellen"]

    # Beträge im Eingabemodus anzeigen (nicht immer Netto!)
    if st.session_state.eingabe_modus == "brutto":
        # Eingaben sind Brutto → zeige Brutto-Werte
        anzeige_df["Betrag (€)"] = anzeige_df["Betrag (€)"].apply(lambda x: f"{x:,.2f} €")
    else:
        # Eingaben sind Netto → zeige Netto-Werte
        anzeige_df["Betrag (€)"] = anzeige_df["Betrag (€)"].apply(lambda x: f"{x:,.2f} €")

    # Summenzeile hinzufügen (im Eingabemodus)
    summe_positionen = df_pos["Betrag"].sum()
    summen_zeile = pd.DataFrame({
        "Position": [f"SUMME ({st.session_state.eingabe_modus.upper()})"],
        "Betrag (€)": [f"{summe_positionen:,.2f} €"],
        "Verteilung": [""],
        "Ziel-Kostenstellen": [""],
    })
    anzeige_df = pd.concat([anzeige_df, summen_zeile], ignore_index=True)

    st.dataframe(anzeige_df, hide_index=True, use_container_width=True)

    # Löschen-Button pro Position
    col_del1, col_del2 = st.columns([4, 1])
    with col_del2:
        if st.button("🗑️ Letzte Position löschen", use_container_width=True):
            st.session_state.rechnungspositionen.pop()
            st.rerun()

    with col_del1:
        if st.button("🔄 Alle Positionen löschen", use_container_width=True):
            st.session_state.rechnungspositionen = []
            st.rerun()

# ============================================================================
# 6. VERTEILUNG BERECHNEN
# ============================================================================
st.markdown("---")

if st.button("🧮 Verteilung berechnen", use_container_width=True, type="primary"):
    if not st.session_state.rechnungspositionen:
        st.warning("Bitte zuerst Positionen eingeben.")
    else:
        # Ergebnis-DataFrame vorbereiten
        ergebnis = {ks: {"Netto": 0.0, "Brutto": 0.0, "Anteil_Positionen": []} for ks in liste_ks_nummern}

        for pos in st.session_state.rechnungspositionen:
            betrag = pos["Betrag"]
            ziel_ks = pos["Ziel_Kostenstellen"]

            # Wenn Eingabe Brutto war, zuerst in Netto umrechnen für die Verteilung
            if st.session_state.eingabe_modus == "brutto":
                betrag = betrag / 1.19

            if pos["Verteilungsart"] == "Einzelne Kostenstelle":
                # Betrag bleibt ungeteilt auf die ausgewählten Kostenstellen
                anteil = betrag / len(ziel_ks) if len(ziel_ks) > 0 else 0
                for ks in ziel_ks:
                    if ks in ergebnis:
                        ergebnis[ks]["Netto"] += anteil
                        ergebnis[ks]["Brutto"] += anteil * 1.19
                        ergebnis[ks]["Anteil_Positionen"].append(pos["Positionsname"])
            else:
                # Gleichmäßig auf alle oder verwendete
                anteil = betrag / len(ziel_ks) if len(ziel_ks) > 0 else 0
                for ks in ziel_ks:
                    if ks in ergebnis:
                        ergebnis[ks]["Netto"] += anteil
                        ergebnis[ks]["Brutto"] += anteil * 1.19
                        ergebnis[ks]["Anteil_Positionen"].append(pos["Positionsname"])

        # DataFrame bauen – nur Kostenstellen mit Betrag > 0 anzeigen
        ergebnis_zeilen = []
        for ks in liste_ks_nummern:
            netto = ergebnis[ks]["Netto"]
            brutto = ergebnis[ks]["Brutto"]
            # Nur anzeigen, wenn die Kostenstelle tatsächlich einen Betrag erhalten hat
            if netto > 0.01 or brutto > 0.01:
                bez = df_ks.loc[df_ks["Kostenstelle"] == ks, "Bezeichnung"].values[0]
                anteil_pos = "; ".join(sorted(set(ergebnis[ks]["Anteil_Positionen"])))
                ergebnis_zeilen.append({
                    "Kostenstelle": ks,
                    "Bezeichnung": bez,
                    "Netto (€)": netto,
                    "Brutto (€)": brutto,
                    "Zugewiesene Positionen": anteil_pos,
                })

        df_ergebnis = pd.DataFrame(ergebnis_zeilen)

        # Gesamtsumme
        summe_netto = df_ergebnis["Netto (€)"].sum()
        summe_brutto = df_ergebnis["Brutto (€)"].sum()

        # ============================================================================
        # 7. AUSGABE
        # ============================================================================
        st.markdown("## 📊 Ergebnis")

        # Auswahlspalte und Summe je nach Anzeigemodus
        if st.session_state.anzeige_modus == "brutto":
            betrag_spalte = "Brutto (€)"
            summe = summe_brutto
            spalten_anzeige = ["Kostenstelle", "Bezeichnung", "Brutto (€)", "Zugewiesene Positionen"]
        else:
            betrag_spalte = "Netto (€)"
            summe = summe_netto
            spalten_anzeige = ["Kostenstelle", "Bezeichnung", "Netto (€)", "Zugewiesene Positionen"]

        # Formatierung
        df_anzeige = df_ergebnis[spalten_anzeige].copy()
        betrag_col_name = "Brutto (€)" if st.session_state.anzeige_modus == "brutto" else "Netto (€)"
        df_anzeige[betrag_col_name] = df_anzeige[betrag_col_name].apply(lambda x: f"{x:,.2f} €")

        st.dataframe(df_anzeige, hide_index=True, use_container_width=True)

        # Gesamtsumme hervorheben (im Anzeigemodus)
        st.markdown(f"### 💵 Gesamtsumme ({st.session_state.anzeige_modus.upper()}): **{summe:,.2f} €**")

        # Kontrolle: Summe der Rechnungspositionen (im EINGABEMODUS!)
        summe_positionen = sum(p["Betrag"] for p in st.session_state.rechnungspositionen)
        st.caption(f"Kontrolle: Summe aller Rechnungspositionen ({st.session_state.eingabe_modus.upper()}) = {summe_positionen:,.2f} €")

        # Warnung bei Abweichung (rundungsbedingt)
        # Die Verteilung wurde aus den EINGABEWERTEN berechnet, also muss die Kontrollsumme
        # im EINGABEMODUS mit der Verteilungssumme im EINGABEMODUS übereinstimmen
        if st.session_state.eingabe_modus == "netto":
            # Eingaben waren Netto → vergleiche Netto-Summe der Verteilung mit Originalsumme
            summe_verteilung_eingabe = summe_netto
            if abs(summe_verteilung_eingabe - summe_positionen) > 0.01:
                st.warning(f"⚠️ Abweichung: Verteilung {summe_verteilung_eingabe:,.2f} € vs. Original {summe_positionen:,.2f} €")
            else:
                st.success("✅ Verteilung stimmt mit Originalsumme überein")
        else:
            # Eingaben waren Brutto → vergleiche Brutto-Summe der Verteilung mit Originalsumme
            summe_verteilung_eingabe = summe_brutto
            if abs(summe_verteilung_eingabe - summe_positionen) > 0.01:
                st.warning(f"⚠️ Abweichung: Verteilung {summe_verteilung_eingabe:,.2f} € vs. Original {summe_positionen:,.2f} €")
            else:
                st.success("✅ Verteilung stimmt mit Originalsumme überein")

        # ============================================================================
        # 8. EXPORT
        # ============================================================================
        st.markdown("---")
        st.subheader("📤 Export")

        # Excel-Export vorbereiten
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            # Sheet 1: Ergebnis
            df_export = df_ergebnis.copy()
            df_export["Netto (€)"] = df_export["Netto (€)"].apply(lambda x: round(x, 2))
            df_export["Brutto (€)"] = df_export["Brutto (€)"].apply(lambda x: round(x, 2))
            df_export.to_excel(writer, sheet_name="Verteilung", index=False)

            # Sheet 2: Positionen
            df_pos_export = pd.DataFrame(st.session_state.rechnungspositionen)
            df_pos_export["Ziel_Kostenstellen"] = df_pos_export["Ziel_Kostenstellen"].apply(
                lambda x: ", ".join(map(str, x))
            )
            df_pos_export.to_excel(writer, sheet_name="Positionen", index=False)

        excel_bytes = output.getvalue()

        st.download_button(
            label="📥 Als Excel herunterladen",
            data=excel_bytes,
            file_name="kostenstellen_verteilung.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

        # CSV-Export
        csv_bytes = df_ergebnis.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Als CSV herunterladen",
            data=csv_bytes,
            file_name="kostenstellen_verteilung.csv",
            mime="text/csv",
            use_container_width=True,
        )