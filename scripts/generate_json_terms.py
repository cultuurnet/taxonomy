#!/usr/bin/env python3

import json
from nis import cat
from xml import dom
import xml.etree.ElementTree as ET

def check_scope(domain, id):
    if domain == 'facility' and id not in event_facilities:
        return ['events', 'places']
    if domain == 'theme':
        return ['events']
    if id in place_types:
        return ['places']
    return ['events']

event_facilities = [
    'H28fcfRKFQAQs00K9NF9hh', # Prikkelarm aanbod
    '4Vz9eZf0cnQmtfqcGGnNMF', # Afspraken en voorspelbaarheid
]
theme_list = []
terms_list = []
place_types = [
    '0.14.0.0.0',             # Monument       
    '0.15.0.0.0',             # Natuur, park of tuin
    '0.41.0.0.0',             # Thema of pretpark
    '0.53.0.0.0',             # Recreatiedomein of centrum
    '0.8.0.0.0',              # Openbare ruimte
    '3CuHvenJ+EGkcvhXLg9Ykg', # Archeologische Site
    '8.70.0.0.0',             # Theater
    'BtVNd33sR0WntjALVbyp3w', # Bioscoop
    'GnPFp9uvOUyqhOckIFMKmg', # Museum of galerij
    'JCjA0i5COUmdjMwcyjNAFA', # Jeugdhuis of jeugdcentrum
    'OyaPaf64AEmEAYXHeLMAtA', # Zaal of expohal
    'VRC6HX0Wa063sq98G5ciqw', # Winkel
    'YVBc8KVdrU6XfTNvhMYUpg', # Discotheek
    'Yf4aZBfsUEu2NsQqsprngw', # Cultuur- of ontmoetingscentrum
    'eBwaUAAhw0ur0Z02i5ttnw', # Sportcentrum
    'ekdc4ATGoUitCa0e6me6xA', # Horeca
    'kI7uAyn2uUu9VV6Z3uWZTA', # Bibliotheek of documentatiecentrum
    'rJRFUqmd6EiqTD4c7HS90w', # School of onderwijscentrum
    'wwjRVmExI0w6xfQwT1KWpx', # Speeltuin
]

suggestions = {
    # Begeleide uitstap of rondleiding
    '0.7.0.0.0': [
        '1.2.1.0.0',  # Architectuur
        '1.40.0.0.0', # Erfgoed
        '1.11.0.0.0', # Geschiedenis
        '1.41.0.0.0', # Kunst en kunsteducatie
        '1.63.0.0.0', # Landbouw en platteland
        '1.0.9.0.0',  # Meerdere kunstvormen
        '1.64.0.0.0', # Milieu en natuur
        '1.37.2.0.0', # Samenleving
        '1.25.0.0.0', # Wetenschap
        '1.44.0.0.0', # Zingeving, filosofie en religie
    ],
    # Beurs
    '0.6.0.0.0': [
        '1.17.0.0.0', # Antiek en brocante
        '1.7.2.0.0',  # Erfgoed
        '1.62.0.0.0', # Gezondheid en wellness
        '1.10.0.0.0', # Literatuur
        '1.0.9.0.0',  # Meerdere kunstvormen
        '1.64.0.0.0', # Milieu en natuur
        '1.37.2.0.0', # Samenleving
        '1.10.8.0.0', # Strips
        '1.65.0.0.0', # Voeding
        '1.25.0.0.0', # Wetenschap
    ],
    # Concert
    '0.50.4.0.0': [
        '1.8.3.5.0', # Amusementsmuziek
        '1.8.3.3.0', # Dance muziek
        '1.8.4.0.0', # Folk en wereldmuziek
        '1.8.3.2.0', # Hiphop, r&b en rap
        '1.8.2.0.0', # Jazz en blues
        '1.8.1.0.0', # Klassieke muziek
        '1.8.3.1.0', # Pop en rock
    ],
    # Lessenreeks
    '0.3.1.0.0': [
        '1.9.1.0.0',   # Ballet en klassieke dans - Dans
        '1.9.2.0.0',   # Moderne dans - Dans
        '1.9.5.0.0',   # Stijl en salondansen - Dans
        '1.9.3.0.0',   # Volksdans en werelddans - Dans
        '1.1.0.0.0',   # Audiovisuele kunst - Kunst en erfgoed
        '1.0.2.0.0',   # Beeldhouwkunst - Kunst en erfgoed
        '0.52.0.0.0',  # Circus - Kunst en erfgoed
        '1.42.0.0.0',  # Creativiteit - Kunst en erfgoed
        '1.0.5.0.0',   # Decoratieve kunst - Kunst en erfgoed
        '1.2.2.0.0',   # Design - Kunst en erfgoed
        '1.40.0.0.0',  # Erfgoed - Kunst en erfgoed
        '1.0.6.0.0',   # Fotografie - Kunst en erfgoed
        '1.0.4.0.0',   # Grafiek - Kunst en erfgoed
        '1.10.0.0.0',  # Literatuur - Kunst en erfgoed
        '1.0.9.0.0',   # Meerdere kunstvormen - Kunst en erfgoed
        '1.49.0.0.0',  # Mode - Kunst en erfgoed
        '1.10.5.0.0',  # Poëzie - Kunst en erfgoed
        '1.0.1.0.0',   # Schilderkunst - Kunst en erfgoed
        '1.3.1.0.0',   # Tekst- en muziektheater - Kunst en erfgoed
        '1.8.3.5.0',   # Amusementsmuziek - Muziek
        '1.8.3.3.0',   # Dance muziek - Muziek
        '1.8.4.0.0',   # Folk en wereldmuziek - Muziek
        '1.8.3.2.0',   # Hiphop, r&b en rap - Muziek
        '1.8.2.0.0',   # Jazz en blues - Muziek
        '1.8.1.0.0',   # Klassieke muziek - Muziek
        '1.8.3.1.0',   # Pop en rock - Muziek
        '1.51.14.0.0', # Atletiek, wandelen en fietsen - Sport
        '1.51.13.0.0', # Bal en racketsport - Sport
        '1.51.6.0.0',  # Fitness, gymnastiek, dans en vechtsport - Sport
        '1.58.8.0.0',  # Lucht en motorsport - Sport
        '1.51.12.0.0', # Omnisport en andere - Sport
        '1.51.11.0.0', # Outdoor en Adventure sport - Sport
        '1.51.10.0.0', # Volkssporten - Sport
        '1.51.3.0.0',  # Zwemmen en watersport - Sport
        '1.37.1.0.0',  # Gezondheid en wellness - Varia
        '1.43.0.0.0',  # Interculturele vorming - Varia
        '1.64.0.0.0',  # Milieu en natuur - Varia
        '1.37.0.0.0',  # Opvoeding - Varia
        '1.61.0.0.0',  # Persoon en relaties - Varia
        '1.37.2.0.0',  # Samenleving - Varia
        '1.65.0.0.0',  # Voeding - Varia
        '1.25.0.0.0',  # Wetenschap - Varia
        '1.44.0.0.0',  # Zingeving, filosofie en religie - Varia
    ],
    # Cursus met open sessies
    '0.3.1.0.1': [
        '1.9.1.0.0',   # Ballet en klassieke dans - Dans
        '1.9.2.0.0',   # Moderne dans - Dans
        '1.9.5.0.0',   # Stijl en salondansen - Dans
        '1.9.3.0.0',   # Volksdans en werelddans - Dans
        '1.1.0.0.0',   # Audiovisuele kunst - Kunst en erfgoed
        '1.0.2.0.0',   # Beeldhouwkunst - Kunst en erfgoed
        '0.52.0.0.0',  # Circus - Kunst en erfgoed
        '1.42.0.0.0',  # Creativiteit - Kunst en erfgoed
        '1.0.5.0.0',   # Decoratieve kunst - Kunst en erfgoed
        '1.2.2.0.0',   # Design - Kunst en erfgoed
        '1.40.0.0.0',  # Erfgoed - Kunst en erfgoed
        '1.0.6.0.0',   # Fotografie - Kunst en erfgoed
        '1.0.4.0.0',   # Grafiek - Kunst en erfgoed
        '1.10.0.0.0',  # Literatuur - Kunst en erfgoed
        '1.0.9.0.0',   # Meerdere kunstvormen - Kunst en erfgoed
        '1.49.0.0.0',  # Mode - Kunst en erfgoed
        '1.10.5.0.0',  # Poëzie - Kunst en erfgoed
        '1.0.1.0.0',   # Schilderkunst - Kunst en erfgoed
        '1.3.1.0.0',   # Tekst- en muziektheater - Kunst en erfgoed
        '1.8.3.5.0',   # Amusementsmuziek - Muziek
        '1.8.3.3.0',   # Dance muziek - Muziek
        '1.8.4.0.0',   # Folk en wereldmuziek - Muziek
        '1.8.3.2.0',   # Hiphop, r&b en rap - Muziek
        '1.8.2.0.0',   # Jazz en blues - Muziek
        '1.8.1.0.0',   # Klassieke muziek - Muziek
        '1.8.3.1.0',   # Pop en rock - Muziek
        '1.51.14.0.0', # Atletiek, wandelen en fietsen - Sport
        '1.51.13.0.0', # Bal en racketsport - Sport
        '1.51.6.0.0',  # Fitness, gymnastiek, dans en vechtsport - Sport
        '1.58.8.0.0',  # Lucht en motorsport - Sport
        '1.51.12.0.0', # Omnisport en andere - Sport
        '1.51.11.0.0', # Outdoor en Adventure sport - Sport
        '1.51.10.0.0', # Volkssporten - Sport
        '1.51.3.0.0',  # Zwemmen en watersport - Sport
        '1.37.1.0.0',  # Gezondheid en wellness - Varia
        '1.43.0.0.0',  # Interculturele vorming - Varia
        '1.64.0.0.0',  # Milieu en natuur - Varia
        '1.37.0.0.0',  # Opvoeding - Varia
        '1.61.0.0.0',  # Persoon en relaties - Varia
        '1.37.2.0.0',  # Samenleving - Varia
        '1.65.0.0.0',  # Voeding - Varia
        '1.25.0.0.0',  # Wetenschap - Varia
        '1.44.0.0.0',  # Zingeving, filosofie en religie - Varia
    ],
    # Dansvoorstelling
    '0.54.0.0.0': [
        '1.9.1.0.0', # Ballet en klassieke dans
        '1.9.2.0.0', # Moderne dans
        '1.9.5.0.0', # Stijl en salondansen
        '1.9.3.0.0', # Volksdans en werelddans
    ],
    # Eet- of drankfestijn
    # '1.50.0.0.0': [],
    # Festival
    '0.5.0.0.0': [
        '1.8.3.5.0',  # Amusementsmuziek
        '0.52.0.0.0', # Circus
        '1.8.3.3.0',  # Dance muziek
        '1.8.4.0.0',  # Folk en wereldmuziek
        '1.3.10.0.0', # Humor en comedy
        '1.8.2.0.0',  # Jazz en blues
        '1.8.1.0.0',  # Klassieke muziek
        '1.41.0.0.0', # Kunst en kunsteducatie
        '1.10.0.0.0', # Literatuur
        '1.7.14.0.0', # Meerdere filmgenres
        '1.0.9.0.0',  # Meerdere kunstvormen
        '1.8.3.1.0',  # Pop en rock
        '1.37.2.0.0', # Samenleving
        '1.3.1.0.0',  # Tekst- en muziektheater
        '1.25.0.0.0', # Wetenschap
    ],
    # Film
    '0.50.6.0.0': [
        '1.7.2.0.0',  # Actie- en avonturenfilm
        '1.7.12.0.0', # Animatie en kinderfilms
        '1.7.11.0.0', # Cinefiel
        '1.7.1.0.0',  # Documentaires en reportages
        '1.7.4.0.0',  # Drama
        '1.7.10.0.0', # Filmmusical
        '1.7.6.0.0',  # Griezelfilm of horror
        '1.7.8.0.0',  # Historische film
        '1.7.3.0.0',  # Komedie
        '1.7.13.0.0', # Kortfilm
        '1.7.7.0.0',  # Science fiction
        '1.7.15.0.0', # Thriller
    ],
    # Kamp of vakantie
    '0.57.0.0.0': [
        '1.51.11.0.0', # Avontuur
        '1.42.0.0.0',  # Creativiteit
        '1.65.0.0.0',  # Koken
        '1.64.0.0.0',  # Natuur
        '1.51.12.0.0', # Sport
        '1.21.0.0.0',  # Technologie
        '1.11.2.0.0',  # Themakamp
        '1.11.1.0.0',  # Taal en communicatie
    ],
    # Festiviteit
    # '0.28.0.0.0': [],
    # Lezing of congres
    '0.3.2.0.0': [
        '1.21.0.0.0', # Computer en techniek
        '1.42.0.0.0', # Creativiteit
        '1.40.0.0.0', # Erfgoed
        '1.11.0.0.0', # Geschiedenis
        '1.37.1.0.0', # Gezondheid en zorg
        '1.41.0.0.0', # Kunst en kunsteducatie
        '1.10.0.0.0', # Literatuur
        '1.64.0.0.0', # Milieu en natuur
        '1.37.0.0.0', # Opvoeding
        '1.61.0.0.0', # Persoon en relaties
        '1.10.5.0.0', # Poëzie
        '1.37.2.0.0', # Samenleving
        '1.25.0.0.0', # Wetenschap
        '1.44.0.0.0', # Zingeving, filosofie en religie
    ],
    # Markt, braderie of kermis
    '0.37.0.0.0': [
        '1.17.0.0.0', # Antiek en brocante
        '1.66.0.0.0', # Economie
        '1.62.0.0.0', # Gezondheid en wellness
        '1.63.0.0.0', # Landbouw en platteland
        '1.10.0.0.0', # Literatuur
        '1.0.9.0.0',  # Meerdere kunstvormen
        '1.64.0.0.0', # Milieu en natuur
        '1.37.2.0.0', # Samenleving
    ],
    # Opendeurdag
    '0.12.0.0.0': [
        '1.2.1.0.0',  # Architectuur
        '1.21.0.0.0', # Computer en techniek
        '1.40.0.0.0', # Erfgoed
        '1.41.0.0.0', # Kunst en kunsteducatie
        '1.63.0.0.0', # Landbouw en platteland
        '1.10.0.0.0', # Literatuur
        '1.0.9.0.0',  # Meerdere kunstvormen
        '1.37.2.0.0', # Samenleving
        '1.25.0.0.0', # Wetenschap
    ],
    # Party of fuif
    # '0.49.0.0.0': [],
    # Route
    # '0.17.0.0.0': [],
    # Spel of quiz
    # '0.50.21.0.0': [],
    # Sport en beweging
    '0.59.0.0.0': [
        '1.51.14.0.0', # Atletiek, wandelen en fietsen
        '1.51.13.0.0', # Bal en racketsport
        '1.51.6.0.0',  # Fitness, gymnastiek, dans en vechtsport
        '1.58.8.0.0',  # Lucht en motorsport
        '1.51.12.0.0', # Omnisport en andere
        '1.51.11.0.0', # Outdoor en Adventure sport
        '1.51.10.0.0', # Volkssporten
        '1.51.3.0.0',  # Zwemmen en watersport
    ],
    # Sportwedstrijd bekijken
    '0.19.0.0.0': [
        '1.51.14.0.0', # Atletiek, wandelen en fietsen
        '1.51.13.0.0', # Bal en racketsport
        '1.51.6.0.0',  # Fitness, gymnastiek, dans en vechtsport
        '1.58.8.0.0',  # Lucht en motorsport
        '1.51.12.0.0', # Omnisport en andere
        '1.51.11.0.0', # Outdoor en Adventure sport
        '1.51.10.0.0', # Volkssporten
        '1.51.3.0.0',  # Zwemmen en watersport
    ],
    # Tentoonstelling
    '0.0.0.0.0': [
        '1.2.1.0.0',  # Architectuur
        '1.1.0.0.0',  # Audiovisuele kunst
        '1.0.2.0.0',  # Beeldhouwkunst
        '1.0.5.0.0',  # Decoratieve kunst
        '1.2.2.0.0',  # Design
        '1.40.0.0.0', # Erfgoed
        '1.0.6.0.0',  # Fotografie
        '1.11.0.0.0', # Geschiedenis
        '1.0.4.0.0',  # Grafiek
        '1.0.3.0.0',  # Installatiekunst
        '1.10.0.0.0', # Literatuur
        '1.0.9.0.0',  # Meerdere kunstvormen
        '1.64.0.0.0', # Milieu en natuur
        '1.49.0.0.0', # Mode
        '1.37.2.0.0', # Samenleving
        '1.0.1.0.0',  # Schilderkunst
        '1.25.0.0.0', # Wetenschap
    ],
    # Theatervoorstelling
    '0.55.0.0.0': [
        '0.52.0.0.0', # Circus
        '1.3.5.0.0',  # Figuren en poppentheater
        '1.3.10.0.0', # Humor en comedy
        '1.3.4.0.0',  # Mime en bewegingstheater
        '1.4.0.0.0',  # Musical
        '1.5.0.0.0',  # Opera en operette
        '1.3.1.0.0',  # Tekst- en muziektheater
    ],
}

tree = ET.parse('../xml/term.xml')
root = tree.getroot()

for categorisation in root.findall('{http://www.cultuurdatabank.com/XMLSchema/CdbXSD/3.2/FINAL}categorisation'):
    for term in categorisation:
        domain = term.get('domain')
        id = term.get('id')
        enabled = term.get('enabled')

        if enabled == 'false':
            continue

        if domain == 'eventtype' or domain == 'theme' or domain == 'facility':
            term_info = {}
            term_info['id'] = id
            term_info['domain'] = domain
            term_info['name'] = {
                'nl': term.get('labelnl'),
                'fr': term.get('labelfr'),
                'de': term.get('labelde'),
                'en': term.get('labelen'),
            }
            term_info['scope'] = check_scope(domain, id)

            if domain == 'theme':
                theme_list.append(term_info)
            
            terms_list.append(term_info)

for term in terms_list:
    if term['id'] in suggestions.keys():
        suggestions_list = []
        for other_term in suggestions[term['id']]:
            theme = next(t for t in theme_list if t['id'] == other_term)
            suggestions_list.append(theme)
            term['otherSuggestedTerms'] = suggestions_list

terms_dict = { 'terms': terms_list}

with open('terms.json', 'w') as pretty_file:
    json.dump(terms_dict, pretty_file, indent = 4)
    
with open('../json/terms.json', 'w') as dump_file:
    json.dump(terms_dict, dump_file)
