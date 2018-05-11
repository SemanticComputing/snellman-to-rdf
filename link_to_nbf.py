from rdflib import Graph,namespace, URIRef
import requests



def link_nbf(g):
    q = '''
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>  
    PREFIX snell: <hhtp://ldf.fi/snellman>
    PREFIX fo: <http://www.w3.org/1999/XSL/Format#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
    PREFIX gvp:	<http://vocab.getty.edu/ontology#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX nbf:	<http://ldf.fi/nbf/>
    PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#>
    PREFIX schema: <http://schema.org/>

    SELECT DISTINCT ?sperson ?nbfperson
    WHERE { 
        ?sperson a foaf:Person .
        ?sperson foaf:familyName ?familyName .
        ?sperson foaf:givenName ?firstName .
        ?sperson dbo:birthYear ?sbirth .
        ?nbfperson a nbf:PersonConcept .
        ?nbfperson skosxl:prefLabel ?label .
        ?label schema:familyName ?familyName .
        ?label schema:givenName ?firstName .        
        ?nbfperson foaf:focus ?actor .
        ?birth crm:P98_brought_into_life ?actor .
        ?birth nbf:time ?btime .
        ?btime gvp:estStart ?birthtime .
        BIND(xsd:integer(?sbirth) as ?s_birth_year) .
        BIND(year(xsd:date(?birthtime)) as ?birthyear) .
        FILTER(?s_birth_year = ?birthyear)
        }
        '''
        
    response = requests.post('http://localhost:3030/ds/query',
                          data={'query': q})
    
    for row in response.json()['results']['bindings']:
        g.add((URIRef(row['sperson']['value']), namespace.SKOS.exactMatch, URIRef(row['nbfperson']['value'])))
        
g = Graph()
g.parse('snellman.ttl', format='turtle')
link_nbf(g)
g.serialize('snellman.ttl', format='turtle')
