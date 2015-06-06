# Doel

Dit is een scraper voor de website van de Groene Amsterdammer. Met behulp van deze scraper kan een abonnee automatisch de PDF downloaden van de Groene Amsterdammer van deze week.

# Gebruik in het kort

## Installatie

```
$ git clone 
$ cd GroeneScrapy
$ sudo pip install -r requirements.txt
```

## Configuratie

Stel de volgende dingen in in `GroeneScrapy/settings.py`:
* `GROENE_USERNAME` is je gebruikersnaam (e-mailadres);
* `GROENE_PASSWORD` is je wachtwoord;
* `GROENE_PDF_PATH` is de directory waar de PDF's worden opgeslagen (standaard: `GroenePDF`).

## Gebruik

Gebruik dit in de root van de repository.

```
$ scrapy crawl pdfspider
```
