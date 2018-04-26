import xml.etree.ElementTree as ET
import csv
import re
from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef
from bs4 import BeautifulSoup


snellman = Namespace('http://ldf.fi/snellman/')
dbo = Namespace('http://dbpedia.org/ontology/')
dc = Namespace('http://purl.org/dc/elements/1.1/')


# Methods for the csv-files

def add_aiheet_csv(g):
    g.add((snellman.Subject, namespace.RDF.type, namespace.RDFS.Class))
    g.add((snellman.Subject, namespace.SKOS.prefLabel, Literal('Aihe, Subject')))
    csv_reader = csv.reader(open('taxonomy/taxocsv_5.csv', 'r'))
    for row in csv_reader:
        s = snellman[row[0]]
        g.add((s, namespace.RDF.type, snellman.Subject))
        g.add((s, namespace.SKOS.prefLabel, Literal(row[1], lang='fi')))
    return g

def add_henkilot_csv(g):
    add_snellman(g)
    csv_reader = csv.reader(open('taxonomy/taxocsv_10.csv', 'r'))
    for row in csv_reader:
        add_personal_info(g, row)
    return g

def add_personal_info(g, row):
    s = snellman[row[0]]
    g.add((s, namespace.RDF.type, namespace.FOAF.Person))
    g.add((s, namespace.SKOS.prefLabel, Literal(row[1], lang='fi')))
    name_split = row[1].split(',')
    bracket_remover = re.compile('\(.*?\)')  
    if len(name_split) > 1:
        family_name = re.sub(bracket_remover, '', name_split[0]).strip()
        g.add((s, namespace.FOAF.familyName, Literal(family_name, lang='fi')))
        first_name = re.sub(bracket_remover, '', name_split[1]).strip()
        g.add((s, namespace.FOAF.givenName, Literal(first_name, lang='fi')))
    if row[9]:
        g.add((s, namespace.SKOS.altLabel, Literal(row[9], lang='fi')))
    cleanr = re.compile('<.*?>')
    bio = re.sub(cleanr, '', row[12])
    if len(list(bio)):
        add_bio(g, s, bio)
    return g

def add_bio(g, s, bio):
    g.add((s, namespace.RDFS.comment, Literal(bio, lang='fi')))
    # Adding birth and death years. Death years sometimes problematic...
    if bio[0].isdigit():
        biosplit = bio.split('–')
        if len(list(biosplit)):
            if len(biosplit[0]) == 4:
                g.add((s, dbo.birthYear, Literal(biosplit[0], datatype=XSD.gyear)))
                death = biosplit[1].split('.')[0].split(',')[0].split(' ')[0].split('/')[0].split('?')[0].split('e')[0]
                if len(list(death)):
                    if len(death) == 4:
                        g.add((s, dbo.deathYear, Literal(death, datatype=XSD.gyear)))
    return g

def add_snellman(g):
    s = snellman['1']
    g.add((s, namespace.RDF.type, namespace.FOAF.Person))
    g.add((s, namespace.SKOS.prefLabel, Literal('J. V. Snellman', lang='fi')))
    g.add((s, namespace.RDFS.comment, Literal('Poliitikko, kirjailija, sanomalehtimies, valtiomies ja Suomen kansallisfilosofi.', lang='fi')))
    g.add((s, namespace.FOAF.familyName, Literal('Snellman', lang='fi')))
    g.add((s, namespace.FOAF.givenName, Literal('Johan Vilhelm', lang='fi')))
    g.add((s, dbo.birthyear, Literal('1806', datatype=XSD.gyear)))
    g.add((s, dbo.deathyear, Literal('1881', datatype=XSD.gyear)))
    return g
          
def add_paikat_csv(g):
    g.add((snellman.Place, namespace.RDF.type, namespace.RDFS.Class))
    g.add((snellman.Place, namespace.SKOS.prefLabel, Literal('Paikka, place')))
    g.add((snellman.Place, namespace.SKOS.exactMatch, dbo.Place))
    csv_reader = csv.reader(open('taxonomy/taxocsv_4.csv', 'r'))
    for row in csv_reader:
        s = snellman[row[0]]
        g.add((s, namespace.RDF.type, snellman.Place))
        g.add((s, namespace.SKOS.prefLabel, Literal(row[1], lang='fi')))
    return g
#   add_links_to_paikka(s, row[1])
        
def add_links_to_paikka(g, s, place):
    yso_g = Graph()
    yso_g.parse('graphs/yso-paikat-skos.rdf')
    location = Literal(place, lang='fi')
    q = yso_g.query("""
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            SELECT ?s
            WHERE { ?s skos:prefLabel ?label . }
            """, initBindings={'label': location})
    for row in q:
        g.add((s, namespace.SKOS.exactMatch, URIRef(row[0])))
    return g
    # some places need to be linked by hand...
    
def add_kirjeenvaihto_csv(g):
    g.add((snellman.Correspondence, namespace.RDF.type, namespace.RDFS.Class))
    g.add((snellman.Correspondence, namespace.SKOS.prefLabel, Literal('Kirjeenvaihto, Correspondence')))
    csv_reader = csv.reader(open('taxonomy/taxocsv_8.csv', 'r'))
    for row in csv_reader:
        s = snellman[row[0]]
        g.add((s, namespace.RDF.type, snellman.Correspondence))
        g.add((s, namespace.SKOS.prefLabel, Literal(row[1], lang='fi')))
    return g

def add_tyypit_csv(g):
    g.add((snellman.Doctype, namespace.RDF.type, namespace.RDFS.Class))
    g.add((snellman.Doctype, namespace.SKOS.prefLabel, Literal('Dokumentin tyyppi, document type')))
    csv_reader = csv.reader(open('taxonomy/taxocsv_9.csv', 'r'))
    for row in csv_reader:
        s = snellman[row[0]]
        g.add((s, namespace.RDF.type, snellman.Doctype))
        g.add((s, namespace.SKOS.prefLabel, Literal(row[1], lang='fi')))
    return g



# Methods for export.xml

def add_people(g, elem, s):
    people = elem.find('field_henkilot')
    if len(list(people)):
        add_relations(g, elem, s, people[0])
    return g
              
def add_places(g, elem, s):
    places = elem.find('field_paikat')
    if len(list(places)):
        add_relations(g, elem, s, places[0])
    return g
        
def add_concepts(g, elem, s):
    concepts = elem.find('field_asiat')
    if len(list(concepts)):
        add_relations(g, elem, s, concepts[0])
    return g
        
def add_type(g, elem, s):
    doctype = elem.find('field_dokumentin_tyyppi')
    if len(list(doctype)):
        g.add((s, namespace.RDF.type, snellman[doctype[0][0][0].text]))
    return g
    
def add_time(g, elem, s):
    time = elem.find('field_date')
    if len(list(time)):
        g.add((s, dc.date, Literal(time[0][0][0].text[:10], datatype=XSD.date)))
    return g

def add_relations(g, elem, s, field):
    for resource in field:
        g.add((s, dc.relation, snellman[resource[0].text]))
    return g

# Adding some extra properties to the letters. Unfinished...   

def add_creator(g, elem, s):

    if len(list(elem.find('field_kirjeenvaihto'))):
        full_title = elem.find('title').text
        title = full_title.split(",")[0]
        if title[len(title)-1] == 'a' or title[len(title)-1] == 'ä':
            people = elem.find('field_henkilot')
            if len(list(people)):
                g.add((s, dc.creator, snellman[people[0][0][0].text]))
            places = elem.find('field_paikat')
            if len(list(places)):
                g.add((s, namespace.RDFS.seeAlso, snellman[places[0][0][0].text]))
        else:
            g.add((s, dc.creator, snellman['1']))
            places = elem.find('field_paikat')
            if len(list(places)):
                g.add((s, namespace.RDFS.seeAlso, snellman[places[0][0][0].text]))
    else:
        g.add((s, dc.creator, snellman['1']))
    return g

def add_content(g, elem, s):
    content = elem.find('field_suomi')
    if len(list(content)):
        g.add((s, snellman.hasText, Literal((BeautifulSoup(content[0][0][3].text,'lxml').text))))
    return g

def add_document_to_graph(g, elem):
    s = snellman[elem.find('nid').text]
    g.add((s, namespace.RDF.type, snellman.Document))
    g.add((s, namespace.SKOS.prefLabel, Literal(elem.find('title').text)))
    path = elem.find('path')
    g.add((s, dc.source, URIRef('http://snellman.kootutteokset.fi/fi/{}'.format(path.find('alias').text))))
    g = add_people(g, elem, s)
    g = add_places(g, elem, s)
    g = add_concepts(g, elem, s)
    g = add_type(g, elem, s)
    g = add_time(g, elem, s)
    g = add_creator(g, elem, s)
    g = add_content(g, elem, s)
    return g

def add_export(g):
    g.add((snellman.Document, namespace.RDF.type, namespace.RDFS.Class))
    g.add((snellman.Document, namespace.RDFS.label, Literal('Document')))
    g.add((snellman.Document, namespace.OWL.equivalentClass, dc.Document))
    g.add((snellman.hasText, namespace.RDF.type, namespace.RDF.Property))
    g.add((snellman.hasText, namespace.RDFS.label, Literal('Text property')))
    for event, elem in ET.iterparse('export.xml', events=("start", "end")):
        if event == 'end':
            if elem.tag == 'node':
                if elem.find('type').text == 'tekstilahde':
                    g = add_document_to_graph(g, elem)
    return g


################

g = Graph()
g.bind('', snellman)
g.bind('skos', namespace.SKOS)
g.bind('dc', dc)
g.bind('foaf', namespace.FOAF)
g.bind('dbo', dbo)

g = add_aiheet_csv(g)
g = add_henkilot_csv(g)
g = add_paikat_csv(g)
g = add_kirjeenvaihto_csv(g)
g = add_tyypit_csv(g)
g = add_export(g)

g.serialize('snellman.ttl', format='turtle')


# To do: Adding the actual texts(?), more sensible classes etc...
