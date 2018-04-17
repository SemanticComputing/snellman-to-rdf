import xml.etree.ElementTree as ET
import csv
import re
from rdflib import Graph, Literal, namespace, Namespace, XSD

g = Graph()
snellman = Namespace('http://ldf.fi/snellman/')
g.bind('skos', namespace.SKOS)
dc = Namespace('http://purl.org/dc/elements/1.1/')
g.bind('dc', dc)
g.bind('foaf', namespace.FOAF)


# Methods for the csv-files

def add_aiheet_csv():
    g.add((snellman.Aihe, namespace.RDF.type, namespace.RDFS.Class))
    g.add((snellman.Aihe, namespace.SKOS.prefLabel, Literal('Aihe, Subject')))
    csv_reader = csv.reader(open('taxonomy/taxocsv_5.csv', 'r'))
    for row in csv_reader:
        s = snellman[row[0]]
        g.add((s, namespace.RDF.type, snellman.Aihe))
        g.add((s, namespace.SKOS.prefLabel, Literal(row[1])))
        
def add_henkilot_csv():
    csv_reader = csv.reader(open('taxonomy/taxocsv_10.csv', 'r'))
    for row in csv_reader:
        s = snellman[row[0]]
        g.add((s, namespace.RDF.type, namespace.FOAF.Person))
        g.add((s, namespace.SKOS.prefLabel, Literal(row[1])))
        if row[9]:
            g.add((s, namespace.SKOS.altLabel, Literal(row[9])))
            # Following adds family name, but not correctly in every case.
            words = row[9].split(' ')
            g.add((s, namespace.FOAF.familyName, Literal(words[len(words)-1])))
        cleanr = re.compile('<.*?>')
        g.add((s, namespace.RDFS.comment, Literal(re.sub(cleanr, '', row[12]))))

def add_paikat_csv():
    g.add((snellman.Paikka, namespace.RDF.type, namespace.RDFS.Class))
    g.add((snellman.Paikka, namespace.SKOS.prefLabel, Literal('Paikka')))
    csv_reader = csv.reader(open('taxonomy/taxocsv_4.csv', 'r'))
    for row in csv_reader:
        s = snellman[row[0]]
        g.add((s, namespace.RDF.type, snellman.Paikka))
        g.add((s, namespace.SKOS.prefLabel, Literal(row[1])))
        
def add_kirjeenvaihto_csv():
    g.add((snellman.Kirjeenvaihto, namespace.RDF.type, namespace.RDFS.Class))
    g.add((snellman.Kirjeenvaihto, namespace.SKOS.prefLabel, Literal('Kirjeenvaihto')))
    csv_reader = csv.reader(open('taxonomy/taxocsv_8.csv', 'r'))
    for row in csv_reader:
        s = snellman[row[0]]
        g.add((s, namespace.RDF.type, snellman.Kirjeenvaihto))
        g.add((s, namespace.SKOS.prefLabel, Literal(row[1])))

def add_tyypit_csv():
    g.add((snellman.Dokumenttityyppi, namespace.RDF.type, namespace.RDFS.Class))
    g.add((snellman.Dokumenttityyppi, namespace.SKOS.prefLabel, Literal('Dokumentin tyyppi')))
    csv_reader = csv.reader(open('taxonomy/taxocsv_9.csv', 'r'))
    for row in csv_reader:
        s = snellman[row[0]]
        g.add((s, namespace.RDF.type, snellman.Dokumenttityyppi))
        g.add((s, namespace.SKOS.prefLabel, Literal(row[1])))


# Methods for export.xml

def add_people(elem, s):
    people = elem.find('field_henkilot')
    if len(list(people)):
        add_relations(elem, s, people[0])
              
def add_places(elem, s):
    places = elem.find('field_paikat')
    if len(list(places)):
        add_relations(elem, s, places[0])
        
def add_concepts(elem, s):
    concepts = elem.find('field_asiat')
    if len(list(concepts)):
        add_relations(elem, s, concepts[0])
        
def add_type(elem, s):
    doctype = elem.find('field_dokumentin_tyyppi')
    if len(list(doctype)):
        g.add((s, namespace.RDF.type, snellman[doctype[0][0][0].text]))
    
def add_time(elem, s):
    time = elem.find('field_date')
    if len(list(time)):
        g.add((s, dc.date, Literal(time[0][0][0].text[:10], datatype=XSD.date)))

def add_relations(elem, s, field):
    for resource in field:
        g.add((s, dc.relation, snellman[resource[0].text]))

def add_to_graph(elem):
    document = snellman[elem.find('nid').text]
    g.add((document, namespace.RDF.type, snellman.SnellmanTeksti))
    g.add((document, namespace.SKOS.prefLabel, Literal(elem.find('title').text)))
    path = elem.find('path')
    g.add((document, namespace.RDFS.comment, Literal('http://snellman.kootutteokset.fi/fi/{}'.format(path.find('alias').text))))
    add_people(elem, document)
    add_places(elem, document)
    add_concepts(elem, document)
    add_type(elem, document)
    add_time(elem, document)

def add_export():
    g.add((snellman.SnellmanTeksti, namespace.RDF.type, namespace.RDFS.Class))
    for event, elem in ET.iterparse('export.xml', events=("start", "end")):
        if event == 'end':
            if elem.tag == 'node':
                if elem.find('type').text == 'tekstilahde':
                    add_to_graph(elem)

################

add_aiheet_csv()
add_henkilot_csv()
add_paikat_csv()
add_kirjeenvaihto_csv()
add_tyypit_csv()
add_export()
g.serialize('snellman.ttl', format='turtle')


# To do: Adding the actual texts(?), more sensible classes etc...
