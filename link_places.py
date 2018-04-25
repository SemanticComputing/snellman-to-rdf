from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef
import requests

snellman = Namespace('http://ldf.fi/snellman/')

# Links to both yso and ysa

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
        
g = Graph()
g.parse('snellman.ttl', format='turtle')
link_places_to_yso(g)

# Adding stuff by hand

g.add((snellman['13638'], namespace.SKOS.closeMatch, URIRef('http://finto.fi/yso-paikat/fi/page/p94466'))) #Nikolain kaupunki = Vaasa
g.add((snellman['13638'], namespace.SKOS.closeMatch, snellman['13228'])) # Nikoilainkaupunki -> Vaasa
g.add((snellman['13228'], namespace.SKOS.closeMatch, snellman['13638'])) # Vaasa -> Nikolainkaupunki
g.add((snellman['13221'], namespace.SKOS.closeMatch, URIRef('https://finto.fi/yso-paikat/fi/page/p94083'))) #Palo tässä ilmeisesti Alahärmän kylä (?)
g.add((snellman['13353'], namespace.SKOS.closeMatch, snellman['13221'])) # Palo -> Alahärmä
g.add((snellman['13221'], namespace.SKOS.closeMatch, snellman['13353'])) # Alahärmä -> Palo

g.serialize('snellman.ttl', format='turtle')