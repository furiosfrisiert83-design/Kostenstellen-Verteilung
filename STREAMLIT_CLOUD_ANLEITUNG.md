# 🚀 Anleitung: Veröffentlichung auf Streamlit Cloud

Diese Anleitung zeigt dir, wie du deine Kostenstellen-Verteilungs-App kostenlos auf Streamlit Cloud hostest.

## 📋 Voraussetzungen

- GitHub-Konto (kostenlos)
- Dein Code ist in einem GitHub-Repository

## 🎯 Schritt 1: GitHub Repository erstellen

### 1.1 Auf GitHub anmelden
- Gehe zu [github.com](https://github.com)
- Melde dich an (oder erstelle einen Account)

### 1.2 Neues Repository erstellen
1. Klicke oben rechts auf **"+"** → **"New repository"**
2. Repository-Name: `kostenstellen-verteilung` (oder ähnlich)
3. Beschreibung: `Tool zur Verteilung von Rechnungspositionen auf Kostenstellen`
4. Wähle **"Public"** (öffentlich) oder **"Private"** (privat)
5. Hake **"Add a README file"** an
6. Klicke **"Create repository"**

### 1.3 Code hochladen

**Option A: Mit VS Code (einfach)**
1. Öffne VS Code in deinem Projektordner
2. Klicke auf das Source-Control-Symbol (links, 3. Symbol von oben)
3. Klicke **"Publish to GitHub"**
4. Wähle dein Repository aus
5. Klicke **"OK"**

**Option B: Mit Git-Befehlen**
```bash
# Git initialisieren
git init

# Alle Dateien hinzufügen
git add .

# Commit erstellen
git commit -m "Initial commit: Kostenstellen-Verteilungstool"

# Mit GitHub verbinden (ersetze die URL durch deine!)
git remote add origin https://github.com/dein-benutzername/kostenstellen-verteilung.git

# Hochladen
git branch -M main
git push -u origin main
```

## 🎯 Schritt 2: Streamlit Cloud verbinden

### 2.1 Auf Streamlit Cloud anmelden
1. Gehe zu [streamlit.io/cloud](https://streamlit.io/cloud)
2. Klicke **"Sign up"** oder **"Log in"**
3. Melde dich mit deinem **GitHub-Account** an

### 2.2 Neue App erstellen
1. Klicke auf **"New app"**
2. Fülle die Felder aus:
   - **Repository:** Wähle dein Repository aus (`dein-benutzername/kostenstellen-verteilung`)
   - **Branch:** `main` (oder `master`)
   - **Main file path:** `app.py`
   - **App URL:** `kostenstellen-verteilung` (wird zu `kostenstellen-verteilung.streamlit.app`)
3. Klicke **"Deploy"**

### 2.3 Warten
- Streamlit Cloud lädt jetzt deine App hoch
- Das dauert ca. 2-5 Minuten
- Du siehst den Fortschritt

## ✅ Schritt 3: Fertig!

Deine App ist jetzt online unter:
**`https://kostenstellen-verteilung.streamlit.app`**

## 🔄 Automatische Updates

Wenn du Änderungen an deinem Code machst:

1. Änderungen in VS Code speichern
2. Mit Git committen und pushen:
   ```bash
   git add .
   git commit -m "Update: Neue Funktion"
   git push
   ```
3. Streamlit Cloud aktualisiert die App **automatisch** innerhalb von 1-2 Minuten

## ⚙️ Einstellungen in Streamlit Cloud

### App-Einstellungen ändern:
1. Gehe zu [share.streamlit.io](https://share.streamlit.io)
2. Klicke auf deine App
3. Klicke auf **"Settings"** (Zahnrad-Symbol)

### Mögliche Einstellungen:
- **Python version:** 3.8, 3.9, 3.10, 3.11, 3.12
- **Secrets:** API-Keys oder Passwörter (verschlüsselt)
- **Custom domain:** Eigene Domain (nur in paid plans)

## 📊 Kosten

**Streamlit Cloud Free Tier:**
- ✅ 1 öffentliche App
- ✅ Unbegrenzte private Apps (seit 2024)
- ✅ Automatische SSL-Verschlüsselung
- ✅ 1 GB RAM pro App
- ✅ Shared CPU

**Limits:**
- Apps schlafen nach 1 Woche Inaktivität ein
- Max. 3 Apps im Free-Tier (kann angehoben werden)

## 🐛 Troubleshooting

### App startet nicht?
1. Prüfe die **Logs** in Streamlit Cloud (Settings → Logs)
2. Häufige Fehler:
   - `requirements.txt` fehlt oder ist falsch
   - `app.py` hat einen Syntaxfehler
   - Fehlende Abhängigkeiten

### App ist langsam?
- Streamlit Cloud Free Tier hat begrenzte Ressourcen
- Für produktive Nutzung: Streamlit Cloud Team Plan oder selbst hosten

### Daten werden nicht gespeichert?
- Streamlit Cloud Apps sind **zustandslos** (stateless)
- Bei jedem Neuladen wird die App zurückgesetzt
- Für dauerhafte Speicherung: Externe Datenbank (z.B. SQLite, PostgreSQL)

## 🔒 Sicherheit

### Was NICHT in GitHub/Streamlit Cloud gehört:
- ❌ Echte Kostenstellennamen
- ❌ Passwörter oder API-Keys
- ❌ Vertrauliche Geschäftsdaten

### Was sicher ist:
- ✅ Der Code (Logik)
- ✅ Die Struktur
- ✅ Beispiel-Daten

### Secrets verwalten:
Für echte Daten nutze **Streamlit Secrets**:
1. In Streamlit Cloud: Settings → Secrets
2. Füge sensible Daten hinzu:
   ```toml
   [database]
   host = "dein-db-server"
   password = "dein-passwort"
   ```
3. In der App zugreifen:
   ```python
   import streamlit as st
   password = st.secrets["database"]["password"]
   ```

## 📝 Checkliste vor Veröffentlichung

- [ ] `.gitignore` enthält keine sensiblen Daten
- [ ] `requirements.txt` ist aktuell
- [ ] `README.md` ist vollständig
- [ ] Keine echten Kostenstellennamen im Code
- [ ] Keine Passwörter/API-Keys im Code
- [ ] App funktioniert lokal
- [ ] Lizenz hinzugefügt (z.B. MIT)

## 🎉 Nächste Schritte

1. **GitHub Repository** erstellen
2. **Code hochladen**
3. **Streamlit Cloud** verbinden
4. **App teilen** mit Kollegen

## 📚 Weiterführende Links

- [Streamlit Cloud Dokumentation](https://docs.streamlit.io/streamlit-community-cloud)
- [GitHub Dokumentation](https://docs.github.com/)
- [Streamlit Sharing Best Practices](https://docs.streamlit.io/streamlit-community-cloud/share-your-app)

---

**Viel Erfolg mit deiner veröffentlichten App!** 🚀