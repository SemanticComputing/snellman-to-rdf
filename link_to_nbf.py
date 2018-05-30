from rdflib import Graph,namespace, URIRef
import requests
import json
import csv


def link_nbf(g):
    q = '''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX snell: <http://ldf.fi/snellman/>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX place: <http://purl.org/ontology/places/>
PREFIX fo: <http://www.w3.org/1999/XSL/Format#>
PREFIX nbf:	<http://ldf.fi/nbf/>
PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#>
PREFIX schema: <http://schema.org/>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX gvp:	<http://vocab.getty.edu/ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT DISTINCT ?sperson ?nbfperson
    WHERE { 
        ?sperson a foaf:Person .
        ?sperson foaf:familyName ?familyName .
        ?sperson foaf:givenName ?firstName .
        ?sperson snell:birthYear ?sbirth .
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



def find_nbf_people():
    q = '''
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX snell: <http://ldf.fi/snellman/>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX place: <http://purl.org/ontology/places/>
    PREFIX fo: <http://www.w3.org/1999/XSL/Format#>
    PREFIX nbf:	<http://ldf.fi/nbf/>
    PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#>
    PREFIX schema: <http://schema.org/>
    PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
    PREFIX gvp:	<http://vocab.getty.edu/ontology#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT DISTINCT ?nbfperson ?familyName ?firstName ?birthyear
    WHERE { 
        ?nbfperson a nbf:PersonConcept .
        ?nbfperson skosxl:prefLabel ?label .
        ?label schema:familyName ?familyName .
        ?label schema:givenName ?firstName .        
        ?nbfperson foaf:focus ?actor .
        ?birth crm:P98_brought_into_life ?actor .
        ?birth nbf:time ?btime .
        ?btime gvp:estStart ?birthtime .
        BIND(year(xsd:date(?birthtime)) as ?birthyear) .
        FILTER(?birthyear < 1882)
    }
    ORDER BY DESC(?birthyear)
    '''
    response = requests.post('http://localhost:3030/ds/query',
                             data={'query': q})

    #with open('graphs/nbf.json', 'w') as nbf_people:
    #    json.dump(response.json(), nbf_people)
    with open('graphs/nbf.csv', 'w') as csvfile:
        for row in response.json()['results']['bindings']:
            csvfile.write(row['nbfperson']['value'] + ',' + row['birthyear']['value'] + ',' + \
                          row['familyName']['value'] + ',' + row['firstName']['value'] + '\n')
        #for row in response.json()['results']['bindings']:
         #   print(row['prefLabel']['value'])

def read_csv():
    csvreader = csv.reader(open('graphs/nbf.csv', 'r'))
    for row in csvreader:
        print(row[1])

def find_snellman_people():
    q = '''
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX snell: <http://ldf.fi/snellman/>

        SELECT DISTINCT ?person ?birthYear ?familyName ?firstName
        WHERE { 
            ?person a foaf:Person .
            ?person foaf:familyName ?familyName .
            ?person foaf:givenName ?firstName .
            ?person snell:birthYear ?birthYear .
        }
        ORDER BY DESC(?birthYear)
        '''

    response = requests.post('http://localhost:3030/ds/query',
                             data={'query': q})

    with open('graphs/people.csv', 'w') as csvfile:
        for row in response.json()['results']['bindings']:
            csvfile.write(row['person']['value'] + ',' + row['birthYear']['value'] + ',' \
                          + row['familyName']['value'] + ',' + row['firstName']['value'] + '\n')

#g = Graph()
#g.parse('turtle/snellman.ttl', format='turtle')
#link_nbf(g)
#g.serialize('turtle/snellman.ttl', format='turtle')
#find_nbf_people()
#find_snellman_people()

def previous_year(listcsv, x):
    idx0 = 0
    idxn = (len(listcsv) - 1)
    print(listcsv[idx0][1])
    print(listcsv[idxn][1])

    while idx0 <= idxn and x <= int(listcsv[idx0][1]) and x >= int(listcsv[idxn][1]):
        mid = idx0 + \
              int(((float(idxn - idx0) / 2)))
        print(mid)
        print(int(listcsv[mid][1]))
    # Compare the value at mid point with search value
        if int(listcsv[mid][1]) == x:
            while not x > int(listcsv[mid][1]):
                mid = mid - 1
            return mid

        if int(listcsv[mid][1]) > x:
            idxn = mid - 1

        if int(listcsv[mid][1]) < x:
            idx0 = mid + 1

    return -1

csv_reader = csv.reader(open('graphs/people.csv', 'r'))
#csv_reader = csv.reader(open('graphs/nbf.csv', 'r'))


print(previous_year(list(csv_reader), 1830))