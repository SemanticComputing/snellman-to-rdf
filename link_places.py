from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef
import requests
import csv

snellman = Namespace('http://ldf.fi/snellman/')

# Links to both yso and ysa, not used currently

def link_places_to_yso(g):
    q = '''
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    
        SELECT DISTINCT ?splace ?ysoplace
        WHERE { 
            ?place skos:prefLabel "Paikka, place" .
            ?splace a ?place .
            ?splace skos:prefLabel ?placename_snellman .
            SERVICE <http://api.finto.fi/sparql> {
                ?ysoplace skos:prefLabel ?placename_snellman .
                }
        }
        '''

    response = requests.post('http://localhost:3030/ds/query',
                          data={'query': q})
    
    with open('graphs/placelinking.json','w') as f:
        f.write(response.text) 
    
    for row in response.json()['results']['bindings']:
        g.add((URIRef(row['splace']['value']), namespace.SKOS.exactMatch, URIRef(row['ysoplace']['value'])))
        
def link_places_to_wd(g):
    q = '''
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>  
        PREFIX yso: <http://www.yso.fi/onto/yso> 
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        PREFIX wd: <http://www.wikidata.org/entity/>
        SELECT DISTINCT ?splace ?wdtown
        WHERE { 
        ?place skos:prefLabel "Paikka, place" .
        ?splace a ?place .
        ?splace skos:prefLabel ?nimi .
        SERVICE <https://query.wikidata.org/sparql> {
 			{ ?wdtown	wdt:P31 wd:Q3957 .
                ?wdtown rdfs:label ?nimi . }
                UNION
                { ?wdtown wdt:P31 wd:Q515 .
                ?wdtown rdfs:label ?nimi . }
  		}
        }
        '''
    response = requests.post('http://localhost:3030/ds/query',
                             data={'query': q})
                          
    for row in response.json()['results']['bindings']:
        g.add((URIRef(row['splace']['value']), namespace.SKOS.exactMatch, URIRef(row['wdtown']['value'])))
    
    g.remove((snellman['13370'], namespace.SKOS.exactMatch, URIRef('http://www.wikidata.org/entity/Q30990')))
    g.remove((snellman['13799'], namespace.SKOS.exactMatch, URIRef('http://www.wikidata.org/entity/Q145717')))
    g.remove((snellman['13729'], namespace.SKOS.exactMatch, URIRef('http://www.wikidata.org/entity/Q48370')))


def link_to_yso(g, place_g, s, place, language):
        location = Literal(place, lang=language)
        q = place_g.query("""
                PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                SELECT ?s
                WHERE { ?s skos:prefLabel ?label . }
                """, initBindings={'label': location})
        if len(list(q)) > 0:
            for row in q:
                g.add((s, namespace.SKOS.exactMatch, URIRef(row[0])))
            return True
        else:
            return False

def link_by_altLabel(g, place_g, s, place, language):
    location = Literal(place, lang=language)
    q = place_g.query("""
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            SELECT ?s
            WHERE { ?s skos:altLabel ?label . }
            """, initBindings={'label': location})
    if len(list(q)) > 0:
        for row in q:
            g.add((s, namespace.SKOS.exactMatch, URIRef(row[0])))
        return True
    else:
        return False



def manual_links(g):
    g.add((snellman['13221'], namespace.SKOS.broader, snellman['13353'])) # Palo -> Alahärmä
    g.add((snellman['13638'], namespace.SKOS.broader, snellman['13228'])) # Nikolain -> Vaasa
    # g.add((snellman['13397'], namespace.SKOS.exactMatch, URIRef('http://www.yso.fi/onto/yso/p94148')))
    g.add((snellman['13709'], namespace.SKOS.broader, snellman['13397'])) # Kaksi Hämeenlinnaa ???
    g.add((snellman['13721'], namespace.SKOS.broader, snellman['13722'])) # Mustiala -> Tammela ????
    g.add((snellman['13330'], namespace.SKOS.broader, snellman['13326'])) # Kuusilahti -> Siilinjärvi
    g.add((snellman['13325'], namespace.SKOS.broader, snellman['13326'])) # Kuuslahti -> Siilinjärvi
    g.add((snellman['13701'], namespace.SKOS.broader, snellman['13261'])) # Bosgård -> Porvoo
    g.add((snellman['13531'], namespace.SKOS.exactMatch, URIRef('https://www.wikidata.org/wiki/Q748559'))) #Strömstad
    g.add((snellman['13581'], namespace.SKOS.exactMatch, URIRef('https://www.wikidata.org/wiki/Q2966'))) # Heidelberg
    g.add((snellman['13478'], namespace.SKOS.exactMatch, URIRef('https://www.wikidata.org/wiki/Q25413'))) # Linköping
    g.add((snellman['13642'], namespace.SKOS.broader, snellman['13643'])) # Ratula -> Artjärvi
    g.add((snellman['13318'], namespace.SKOS.exactMatch, URIRef('https://www.wikidata.org/wiki/Q146342'))) # Teplitz
    g.add((snellman['13333'], namespace.SKOS.exactMatch, URIRef('https://www.wikidata.org/wiki/Q21885987'))) # Hull
    g.add((snellman['13447'], namespace.SKOS.exactMatch, URIRef('http://www.yso.fi/onto/yso/p94109'))) # Vuojoki -> Eurajoki
    g.add((snellman['13860'], namespace.SKOS.exactMatch, URIRef('https://www.wikidata.org/wiki/Q3852'))) # Worms
    g.add((snellman['13559'], namespace.SKOS.exactMatch, URIRef('https://www.wikidata.org/wiki/Q3806'))) # Tübingen
    g.add((snellman['13303'], namespace.SKOS.exactMatch, URIRef('https://www.wikidata.org/wiki/Q167668'))) # Libau
    g.add((snellman['13804'], namespace.SKOS.broader, URIRef('http://www.yso.fi/onto/yso/p94210'))) # Danskarby -> Kirkkonummi
    g.add((snellman['13655'], namespace.SKOS.broader, snellman['13261'])) # kroksnäs -> Porvoo
    # Vjasnik kaupunki Vladimirin kuvermentissä ei löydy
    # Mattila ???
    # Skålltorp ?
    # Ḱimo ?
    # Keppo / Kepoo ?

    # g.add((snellman['13638'], namespace.SKOS.closeMatch, URIRef('http://finto.fi/yso-paikat/fi/page/p94466'))) #Nikolain kaupunki = Vaasa
    # g.add((snellman['13638'], namespace.SKOS.closeMatch, snellman['13228'])) # Nikoilainkaupunki -> Vaasa
    # g.add((snellman['13228'], namespace.SKOS.closeMatch, snellman['13638'])) # Vaasa -> Nikolainkaupunki
    # g.add((snellman['13221'], namespace.SKOS.closeMatch, URIRef('https://finto.fi/yso-paikat/fi/page/p94083'))) #Palo tässä ilmeisesti Alahärmän kylä (?)
    # g.add((snellman['13353'], namespace.SKOS.closeMatch, snellman['13221'])) # Alahärmä -> Palo
    # g.add((snellman['13221'], namespace.SKOS.closeMatch, snellman['13353'])) # Palo -> Alahärmä

def link_places(g):
    csv_reader = csv.reader(open('taxonomy/taxocsv_4.csv', 'r'))
    yso_g = Graph()
    yso_g.parse('graphs/yso-paikat-skos.rdf')
    for row in csv_reader:
        s = snellman[row[0]]
        if link_to_yso(g, yso_g, s, row[1], 'fi'):
            pass
        elif link_to_yso(g, yso_g, s, row[1], 'en'):
            pass
        elif link_to_yso(g, yso_g, s, row[1], 'sv'):
            pass
        else:
            link_by_altLabel(g, yso_g, s, row[1], 'fi')
    link_places_to_wd(g)
    manual_links(g)


g = Graph()
g.parse('turtle/snellman.ttl', format='turtle')
link_places(g)
g.serialize('turtle/snellman.ttl', format='turtle')