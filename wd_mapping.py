from rdflib import Graph,namespace, URIRef
import csv
import re
import requests

def get_wikidata_csv():
    q = '''
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT DISTINCT ?human ?nimiFI ?nimiSV (year(?wdbdate) as ?birthYear)
        WHERE { 
            ?human wdt:P31 wd:Q5 .
            ?human rdfs:label ?nimiFI .
            ?human rdfs:label ?nimiSV .
            ?human wdt:P569 ?wdbdate .
            FILTER(lang(?nimiFI) = 'fi') . 
            FILTER(lang(?nimiSV) = 'sv') .
        }
        '''

    response = requests.post('https://query.wikidata.org/sparql',
                             data={'query': q, 'format': 'json'})

    person_file = open('graphs/wd_people.csv', 'w')

    for row in response.json()['results']['bindings']:
        name_in_fi = re.sub("[\(].*?[\)]", "", row['nimiFI']['value']).strip()
        name_in_sv = re.sub("[\(].*?[\)]", "", row['nimiSV']['value']).strip()
        person_file.write('"' + row['human']['value'] + '","' + name_in_fi + '","' + name_in_sv + '","' + row['birthYear']['value'] + '"\n')


get_wikidata_csv()