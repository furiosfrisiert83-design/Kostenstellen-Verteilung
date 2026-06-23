# 💰 Kostenstellen-Verteilungstool

## Kurzbeschreibung

Ein Tool zur Verteilung von Rechnungspositionen auf verschiedene Kostenstellen mit MwSt.-Unterstützung.

## Features

- ✅ 20 fest integrierte Kostenstellen (Kostenstelle 1-20)
- ✅ 3 Verteilungsarten:
  - Einzelne Kostenstelle (frei wählbar)
  - Gleichmäßig auf alle Kostenstellen
  - Gleichmäßig auf verwendete Kostenstellen
- ✅ MwSt.-Unterstützung (Netto/Brutto-Umrechnung)
- ✅ **Brutto/Netto-Rechner** in der Sidebar
- ✅ Export als Excel oder CSV
- ✅ Modernes Orange-Theme

## Schnellstart

```powershell
# Virtuelle Umgebung aktivieren
.\.venv\Scripts\activate

# App starten
streamlit run app.py
```

App öffnet sich unter: `http://localhost:8501`

## Projektstruktur

```
mein-neues-projekt/
├── app.py                           # Hauptanwendung (Streamlit)
├── requirements.txt                 # Python-Abhängigkeiten
├── .streamlit/
│   └── config.toml                  # Theme (Orange #FF8C00)
├── .gitignore
├── README.md                        # Diese Datei
├── GITHUB_README.md                 # GitHub-Beschreibung
├── STREAMLIT_CLOUD_ANLEITUNG.md     # Anleitung für Streamlit Cloud
├── erstelle_excel_vorlage.py        # Excel-Vorlage erstellen
├── vba_makro.bas                    # VBA-Makro für Excel
└── kostenstellen_verteilung_excel_vorlage_anonymisiert.xlsx  # Excel-Vorlage
```

## Verwendung

### 1. Rechnungspositionen eingeben
- Positionsbezeichnung (z.B. "Portokosten")
- Betrag in Euro
- Verteilungsart wählen
- Ziel-Kostenstellen auswählen

### 2. MwSt.-Modus wählen
- **Eingabewerte:** Was steht auf der Rechnung? (Netto/Brutto)
- **Anzeige als:** Wie soll das Ergebnis angezeigt werden?

### 3. Berechnen und Export
- "Verteilung berechnen" klicken
- Ergebnis prüfen
- Als Excel oder CSV exportieren

## Brutto/Netto-Rechner

In der Sidebar findest du einen schnellen Rechner:
- Modus wählen: "Netto → Brutto" oder "Brutto → Netto"
- Wert eingeben
- Ergebnis wird sofort angezeigt

## Online-Version

Die App ist veröffentlicht auf:
- **GitHub:** https://github.com/furiosfrisiert83-design/Kostenstellen-Verteilung
- **Streamlit Cloud:** https://kostenstellen-verteilung.streamlit.app

## Technologien

- Python 3.14
- Streamlit 1.58
- Pandas 3.0
- OpenPyXL (Excel-Export)

## Autor

Erstellt von: furiosfrisiert83-design

## Lizenz

MIT License
