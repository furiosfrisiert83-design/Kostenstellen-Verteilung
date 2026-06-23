# Mein Streamlit-Projekt

Eine Streamlit-App mit der gleichen Umgebung wie das Hauptprojekt.

## Setup (bereits erledigt)

```powershell
# 1. Virtuelle Umgebung aktivieren (falls nicht schon aktiv)
.\.venv\Scripts\activate

# 2. Falls Pakete fehlen:
pip install -r requirements.txt
```

## App starten

```powershell
streamlit run app.py
```

Die App öffnet sich dann automatisch im Browser unter `http://localhost:8501`

## Projektstruktur

```
mein-neues-projekt/
├── .venv/                    # Virtuelle Umgebung (nicht committen!)
├── .streamlit/
│   └── config.toml           # Theme-Konfiguration
├── .gitignore
├── requirements.txt          # Abhängigkeiten
├── README.md
└── app.py                    # Deine Streamlit-App
```

## Nützliche Befehle

| Befehl | Beschreibung |
|--------|-------------|
| `streamlit run app.py` | App starten |
| `streamlit run app.py --server.port 8502` | App auf anderem Port starten |
| `pip freeze > requirements.txt` | Aktuelle Pakete speichern |
| `pip install -r requirements.txt` | Pakete aus Datei installieren |