# baederland_hh Project

## Ziel des Projekts
Für viele Eltern und Kinder in Hamburg ist es eine große Herausforderung, freie Plätze in Schwimmkursen bei Bäderland Hamburg zu finden. Oft sind die Kurse innerhalb weniger Minuten ausgebucht.

Ziel dieses Projekts ist es, einen kleinen Zeitvorteil bei der Platzsuche zu gewinnen.

Das Skript durchsucht automatisch eine bestimmte Seite von Bäderland Hamburg und überprüft, ob ausgewählte Schwimmkurse verfügbar sind. Sobald freie Plätze gefunden werden, verschickt es eine E-Mail an eine definierte Empfängerliste. Diese enthält wichtige Informationen wie:

- Kursname

- Datum

- Anzahl freier Plätze

- Kursgebühr

- Direktlink zur Buchungsseite

## Programmstart  

Das Projekt ist in **Python** entwickelt. Bevor das Skript korrekt ausgeführt werden kann, müssen einige Informationen hinterlegt werden:  

- Im Ordner **`credentials`** muss eine Datei **`creds.json`** abgelegt sein.  
  - In der Entwicklung wurde mit **Gmail** und App-Passwörtern gearbeitet.  
  - Eine Vorlage befindet sich unter **`example_credentials/creds.json`**.  
  - Bitte diese Datei anpassen und in den genannten Ordner kopieren.  

- Im Ordner **`steering`** liegt die Datei **`controls.json`**.  
  - Hier werden der gewünschte **Schwimmkursname**, das **Schwimmbad** und die **Wochentage** konfiguriert.  

Anschließend kann das Programm regelmäßig gestartet werden – z. B. über einen **Cron-Job**, einen **Airflow-DAG** oder ein anderes Scheduling-Tool – mit folgendem Skript:  

```bash
python src/baederland_hh/crawler.py
```

## Technische Informationen  

Dieses Python-Projekt basiert auf:  

- Python 3.12.10  
- poetry  
- python = ">=3.10"  
- requests = "^2.31.0"  
- beautifulsoup4 = "^4.12.2"  
- aiohttp = "^3.8.5"  
- isort = "^6.0.1"  
- datetime = "^5.5"  
- google-auth = "^2.23.0"  
- google-auth-oauthlib = "^1.1.0"  
- google-auth-httplib2 = "^0.1.1"  
- google-api-python-client = "^2.97.0"  
- sendgrid = "^6.12.4"  
- sqlalchemy = "^2.0.43"  

Beim Start des Skripts wird eine spezifische Seite besucht. Das konfigurierte Schwimmbad  
wird in der Datei **`src/baederland_hh/constants.py`** in eine interne ID übersetzt, die für den  
Seitenaufruf benötigt wird.  

Die Inhalte werden anschließend mit **requests** und **BeautifulSoup** analysiert und in eine strukturierte Form gebracht.  
Sofern relevante Informationen gefunden werden, erfolgt eine zusätzliche Filterung.  

Im nächsten Schritt wird der gefundene Kurs mit einer **SQLite3-Datenbank** abgeglichen:  
- Ist der Kurs dort bereits bekannt, wird er verworfen.  
- Ist er neu, wird er in eine Übergabeliste aufgenommen.  

Ziel dieser Logik ist es, zu verhindern, dass bereits bekannte Kurse mehrfach an die Empfängerliste gesendet werden.


## Installation  

1. Repository klonen  
```bash
git clone https://github.com/deinname/baederland_hh.git
cd baederland_hh
```
2. bhängigkeiten installieren
```bash
poetry install
```

## Beschreibung der JSON Files
Kurzer Auszug für creds.json und controls.json.

```json
// creds.json
{
  "email": "dein.name@gmail.com",
  "app_password": "xyz123..."
}

// controls.json
{
  "course_name": "Seepferdchen",
  "location": "Alsterbad",
  "days": ["Monday", "Wednesday"]
}
```

## Lizenz  

Dieses Projekt steht unter der [MIT-Lizenz](./LICENSE).
