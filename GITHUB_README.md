# 💰 Kostenstellen-Verteilungstool

Ein einfaches Tool zur Verteilung von Rechnungspositionen auf verschiedene Kostenstellen – mit MwSt.-Unterstützung.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.58%2B-red)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features

- 📊 **Einfache Eingabe** von Rechnungspositionen
- 🎯 **3 Verteilungsarten:**
  - Einzelne Kostenstelle (frei wählbar)
  - Gleichmäßig auf alle Kostenstellen
  - Gleichmäßig auf verwendete Kostenstellen
- 💶 **MwSt.-Unterstützung** (Netto/Brutto-Umrechnung)
- 📥 **Export** als Excel oder CSV
- 🎨 **Modernes Theme** (Orange/Weiß)

## 🚀 Live Demo

**Hier wird deine Streamlit Cloud URL stehen, nachdem du es veröffentlicht hast!**

## 📦 Installation

### Voraussetzungen
- Python 3.8 oder höher
- pip (Python-Paketverwaltung)

### Lokale Installation

```bash
# Repository klonen
git clone https://github.com/dein-benutzername/kostenstellen-verteilung.git
cd kostenstellen-verteilung

# Virtuelle Umgebung erstellen (empfohlen)
python -m venv venv

# Windows:
.\venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

# Abhängigkeiten installieren
pip install -r requirements.txt

# App starten
streamlit run app.py
```

## 📖 Anleitung

### 1. Kostenstellenliste hochladen
- Erstelle eine Excel/CSV-Datei mit deinen Kostenstellen
- Spalte A: Kostenstellennummer (z.B. 900000)
- Spalte B: Bezeichnung (z.B. "Kostenstelle 1")
- Lade die Datei in der Sidebar hoch

### 2. Rechnungspositionen eingeben
- Positionsbezeichnung (z.B. "Portokosten")
- Betrag in Euro
- Verteilungsart wählen
- Ziel-Kostenstellen auswählen

### 3. MwSt.-Modus wählen
- **Eingabewerte:** Stehen auf deiner Rechnung? (Netto/Brutto)
- **Anzeige als:** Wie soll das Ergebnis angezeigt werden?

### 4. Berechnen und Export
- Klicke "Verteilung berechnen"
- Prüfe das Ergebnis
- Exportiere als Excel oder CSV

## 🛠️ Verwendete Technologien

- **[Streamlit](https://streamlit.io/)** – Web-Framework für Python
- **[Pandas](https://pandas.pydata.org/)** – Datenverarbeitung
- **[OpenPyXL](https://openpyxl.readthedocs.io/)** – Excel-Export
- **[Plotly](https://plotly.com/)** – Visualisierung (optional)

## 📁 Projektstruktur

```
kostenstellen-verteilung/
├── app.py                      # Hauptanwendung
├── requirements.txt            # Python-Abhängigkeiten
├── .streamlit/
│   └── config.toml            # Theme-Konfiguration
├── .gitignore                 # Git-Ausschlussliste
├── README.md                  # Diese Datei
├── erstelle_excel_vorlage.py  # Excel-Vorlage erstellen
├── vba_makro.bas              # VBA-Makro für Excel
└── kostenstellen_verteilung_excel_vorlage.xlsx  # Excel-Vorlage
```

## 🎯 Verwendungszweck

Dieses Tool hilft dir:
- Rechnungsbeträge auf mehrere Kostenstellen zu verteilen
- Verschiedene Verteilungslogiken anzuwenden
- MwSt.-Beträge automatisch umzurechnen
- Ergebnisse zu exportieren und weiterzuverarbeiten

## 🤝 Beitrag leisten

Beiträge sind willkommen! Bitte beachte:

1. Fork das Repository
2. Erstelle einen Feature-Branch (`git checkout -b feature/NeueFunktion`)
3. Committe deine Änderungen (`git commit -m 'Add: Neue Funktion'`)
4. Push zum Branch (`git push origin feature/NeueFunktion`)
5. Öffne einen Pull Request

## 📝 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert – siehe [LICENSE](LICENSE) Datei für Details.

## 👨‍💻 Autor

Erstellt mit ❤️ für die einfache Kostenstellenverteilung

## 🙏 Danksagungen

- [Streamlit](https://streamlit.io/) für das großartige Framework
- Alle Tester und Feedback-Geber

---

**Hinweis:** Dies ist ein Open-Source-Projekt. Nutzung auf eigene Gefahr. Prüfe die Berechnungen immer nach!