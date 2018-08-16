from rdflib import Graph,namespace, Namespace, URIRef
import requests
import json
import csv
import re

snellman = Namespace('http://ldf.fi/snellman/')

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
    ORDER BY ASC(?birthyear)
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
        ORDER BY ASC(?birthYear)
        '''

    response = requests.post('http://localhost:3030/ds/query',
                             data={'query': q})

    with open('graphs/people.csv', 'w') as csvfile:
        for row in response.json()['results']['bindings']:
            csvfile.write(row['person']['value'] + ',' + row['birthYear']['value'] + ',' \
                          + row['familyName']['value'] + ',' + row['firstName']['value'] + '\n')


def binary_search(values, target):
    low = 0
    high = len(values) - 1
    while low <= high:
        mid = (high + low) // 2
        if values[mid] == target:
            return mid
        elif target < values[mid]:
            high = mid - 1
        else:
            low = mid + 1
    return -1

def make_birth_list(csv):
    birth_list = []
    x=0
    for row in csv:
        birth_list.append(int(row[1]))
        x = x+1
    return birth_list

#previous index actually :)
def find_index_of_year(year, list):
    index = binary_search(list, year)
    if index < 0:
        return index
    else:
        while list[index] >= year and index > 0:
            index = index - 1
    return index

def make_list(csv, index):
    list = []
    x=0
    for row in csv:
        list.append(row[index])
        x = x+1
    return list


def nbf_from_csv(g):

    csv_snell = csv.reader(open('graphs/people.csv', 'r'))

    csv_nbf = csv.reader(open('graphs/nbf.csv', 'r'))
    nbf_birth_list = make_birth_list(csv_nbf)

    csv_nbf = csv.reader(open('graphs/nbf.csv', 'r'))
    nbf_first_name_list = make_list(csv_nbf, 3)

    csv_nbf = csv.reader(open('graphs/nbf.csv', 'r'))
    nbf_family_name_list = make_list(csv_nbf, 2)

    csv_nbf = csv.reader(open('graphs/nbf.csv', 'r'))
    nbf_uri_list = make_list(csv_nbf, 0)

    for row in csv_snell:
        index = find_index_of_year(int(row[1]), nbf_birth_list)
        #print(nbindex)
        if index >= 0:
            x=0
            while nbf_birth_list[index] <= int(row[1]):
                snellman_name = re.sub('(.*?)', '', (row[3] + row[2])).strip().replace(" ", "")
                nbf_name = re.sub('(.*?)', '', (nbf_first_name_list[index] + nbf_family_name_list[index])).strip().replace(" ", "")
                print(nbf_name + '   ' + snellman_name)
                if (row[2] == nbf_family_name_list[index] and row[3] == nbf_first_name_list[index]) \
                        or (nbf_name == snellman_name):
                    g.add((URIRef(row[0]), snellman.nbf, URIRef(nbf_uri_list[index])))

                index = index + 1

def link_places(g):
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

        SELECT DISTINCT ?place ?nbfPlace
        WHERE {
            ?place a snell:Place .
            ?place skos:prefLabel ?placeLabel .
            ?nbfPlace a nbf:Place .
            ?nbfPlace skos:prefLabel ?placeLabel .
        }
        '''

    response = requests.post('http://localhost:3030/ds/query',
                                     data={'query': q})

    for row in response.json()['results']['bindings']:
        g.add((URIRef(row['place']['value']), snellman.nbf, URIRef(row['nbfPlace']['value'])))

g = Graph()
g.parse('turtle/snellman.ttl', format='turtle')
#link_nbf(g)
#find_nbf_people()
#find_snellman_people()

nbf_from_csv(g)
#link_places(g)

g.serialize('turtle/snellman.ttl', format='turtle')