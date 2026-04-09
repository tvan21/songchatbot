# Song Chatbot

Ein interaktiver Chatbot zur Song-Empfehlung mit Web-Interface, entwickelt mit Python und FastAPI.

## Beschreibung

Der Song Chatbot hilft Nutzern, passende Songs basierend auf ihren Vorlieben zu finden. Durch eine natürliche Konversation können Nutzer nach Genre, Tempo, Stimmung und Keywords suchen. Gefundene Songs können in personalisierten Playlists gespeichert werden.

## Features

- **Intelligente Song-Suche** basierend auf Keywords, Genre, Tempo und Stimmung
- **Conversational Interface** mit Schritt-für-Schritt-Dialogen
- **Playlist-Verwaltung** zum Speichern favorisierter Songs
- **Web-Interface** für einfache Bedienung
- **SQLite-Datenbank** für persistente Datenspeicherung
- **REST API** für flexible Integration

## Technologie-Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML/JavaScript
- **Datenbank**: SQLite3
- **Server**: Uvicorn (ASGI)
- **Validierung**: Pydantic
- **Testing**: pytest
- **Linting**: flake8
- **CI/CD**: GitHub Actions

## Projektstruktur

.
├── chatbot.py          # Chatbot-Logik und Konversationssteuerung
├── song.py             # Song-Datenmodell
├── songlibrary.py      # Song-Verwaltung und Datenbankzugriff
├── songchatbot.py      # FastAPI-Anwendung mit REST-Endpoints
├── songs.db            # SQLite-Datenbank (wird automatisch erstellt)
├── static/
│   └── index.html      # Web-Interface
├── test/               # Unit-Tests
└── requirements.txt    # Python-Abhängigkeiten


### Voraussetzungen

- Python 3.13.0 oder höher
- pip (Python Package Manager)

### Setup

1. **Repository klonen:**

   git clone <repository-url>
   cd song-chatbot


2. **Virtuelle Umgebung erstellen (empfohlen):**
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # oder
   venv\Scripts\activate     # Windows


3. **Abhängigkeiten installieren:**

   pip install -r requirements.txt


## Verwendung

### Web-Anwendung starten

python songchatbot.py


Der Browser öffnet sich automatisch unter `http://localhost:8000`

### Interaktion mit dem Chatbot

1. **Song suchen:**

   User: love pop fast happy
   Bot: Blinding Lights von The Weeknd (Score: 5)
        Gefällt dir der Song? (ja/nein)


2. **Song zur Playlist hinzufügen:**

   User: ja
   Bot: Super! Soll ich 'Blinding Lights' in eine Playlist speichern?


3. **Neue Suche starten:**
   
   User: neu
   Bot: Neue Suche gestartet! Beschreibe einfach, was du hören möchtest.
   

### Beispiel-Suchanfragen

- `love pop fast happy` - Fröhliche Pop-Songs über Liebe
- `party edm energetic` - Energiegeladene Party-Musik
- `ruhiger jazz song` - Ruhige Jazz-Stücke
- `dark metal aggressive` - Aggressive Metal-Songs

## REST API

### Endpoints

#### Chat
- `POST /chat` - Nachricht an Chatbot senden
- `POST /reset` - Chatbot zurücksetzen

#### Songs
- `GET /songs` - Alle Songs abrufen
- `POST /songs` - Neuen Song hinzufügen

#### Playlists
- `GET /playlists` - Alle Playlists anzeigen
- `POST /playlists` - Neue Playlist erstellen
- `GET /playlists/{name}` - Songs einer Playlist abrufen
- `POST /playlists/{name}/songs` - Song zu Playlist hinzufügen

### API-Dokumentation

Automatische API-Dokumentation verfügbar unter:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing

### Tests ausführen

# Alle Tests
pytest test/

# Mit Coverage-Report
pytest test/ --cov=. --cov-report=term

# Mit Doctests
pytest test/ --doctest-modules

### Linting


# Code-Qualität prüfen
flake8 .

# Nur kritische Fehler
flake8 . --select=E9,F63,F7,F82

## Architektur

Das Projekt folgt einer **3-Tier-Architektur**:

┌─────────────────────────────┐
│  Presentation Layer         │
│  (HTML/JavaScript)          │
└─────────────┬───────────────┘
              │
┌─────────────▼───────────────┐
│  Application Layer          │
│  (FastAPI REST API)         │
└─────────────┬───────────────┘
              │
┌─────────────▼───────────────┐
│  Business Logic Layer       │
│  (Chatbot, SongLibrary)     │
└─────────────┬───────────────┘
              │
┌─────────────▼───────────────┐
│  Data Layer                 │
│  (SQLite Database)          │
└─────────────────────────────┘

### Datenbank-Schema

- **artists** - Künstlerinformationen
- **genres** - Musikgenres (Pop, Rock, EDM, etc.)
- **tempos** - Tempoangaben (slow, medium, fast)
- **moods** - Stimmungen (happy, sad, energetic, etc.)
- **keywords** - Suchbegriffe
- **songs** - Song-Haupttabelle
- **song_keywords** - Verknüpfung Songs ↔ Keywords
- **playlists** - Playlist-Verwaltung
- **playlist_songs** - Verknüpfung Playlists ↔ Songs

## CI/CD

GitHub Actions Workflow führt automatisch aus:

- Dependency Installation
- Linting mit flake8
- Unit-Tests mit pytest

Trigger: Push/Pull Request auf `master` oder `stage` Branch

## Lizenz

Dieses Projekt wurde für akademische Zwecke entwickelt.

## Autoren

[Teresa, Jessica, HÜmeyra, Leon]

## Bekannte Probleme

- Globale Chatbot-Instanz ist nicht thread-safe
- Keine Session-Verwaltung für mehrere gleichzeitige Nutzer
- Empfohlen für Single-User-Nutzung

## Zukünftige Erweiterungen

- Session-Management für Multi-User-Support
- Authentifizierung und Nutzerkonten
- Spotify/YouTube-Integration
- Erweiterte Such-Algorithmen
- Song-Vorschau-Player
- Export/Import von Playlists
