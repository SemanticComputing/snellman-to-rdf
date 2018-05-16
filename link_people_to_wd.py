from rdflib import Graph,namespace, URIRef
import requests



def link_people_wd(g):
    q = '''
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX dc: <http://purl.org/dc/elements/1.1/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX fo: <http://www.w3.org/1999/XSL/Format#>
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        PREFIX snell: <http://ldf.fi/snellman/>
        
        SELECT DISTINCT ?henkilo ?human
        WHERE { 
            ?henkilo a foaf:Person .
            ?henkilo skos:altLabel ?nimi .
            ?henkilo snell:birthYear ?sbyear .
            SERVICE <https://query.wikidata.org/sparql> {
                ?human wdt:P31 wd:Q5 .
                ?human rdfs:label ?nimi .
                ?human wdt:P569 ?wdbdate .
                }
        BIND(xsd:integer(?sbyear) as ?s_birth_year) .
        BIND(year(xsd:date(?wdbdate)) as ?wd_birth_year) .
        FILTER(?s_birth_year = ?wd_birth_year) .
        }
        '''

    response = requests.post('http://localhost:3030/ds/query',
                          data={'query': q})
    
    for row in response.json()['results']['bindings']:
        g.add((URIRef(row['henkilo']['value']), namespace.SKOS.exactMatch, URIRef(row['human']['value'])))

              
def link_people_wd_prefLabel(g):
    q = '''
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX dc: <http://purl.org/dc/elements/1.1/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX fo: <http://www.w3.org/1999/XSL/Format#>
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        PREFIX snell: <http://ldf.fi/snellman/>
        
        SELECT DISTINCT ?henkilo ?human
        WHERE { 
            ?henkilo a foaf:Person .
            ?henkilo skos:prefLabel ?nimi .
            ?henkilo snell:birthYear ?sbyear .
            SERVICE <https://query.wikidata.org/sparql> {
                ?human wdt:P31 wd:Q5 .
                ?human rdfs:label ?nimi .
                ?human wdt:P569 ?wdbdate .
                }
        BIND(xsd:integer(?sbyear) as ?s_birth_year) .
        BIND(year(xsd:date(?wdbdate)) as ?wd_birth_year) .
        FILTER(?s_birth_year = ?wd_birth_year) .
        }
        '''

    response = requests.post('http://localhost:3030/ds/query',
                          data={'query': q})
    
    for row in response.json()['results']['bindings']:
        g.add((URIRef(row['henkilo']['value']), namespace.SKOS.exactMatch, URIRef(row['human']['value'])))

g = Graph()
g.parse('turtle/snellman.ttl', format='turtle')
link_people_wd(g)
link_people_wd_prefLabel(g)
g.serialize('turtle/snellman.ttl', format='turtle')