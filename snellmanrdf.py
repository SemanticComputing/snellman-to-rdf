import xml.etree.ElementTree as ET
import csv
import re
from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef
from bs4 import BeautifulSoup

# The target graph and some bindings
g = Graph()
snellman = Namespace('http://ldf.fi/snellman/')
g.bind('', snellman)
g.bind('skos', namespace.SKOS)
dc = Namespace('http://purl.org/dc/elements/1.1/')
g.bind('dc', dc)
g.bind('foaf', namespace.FOAF)
#dbo = Namespace('http://dbpedia.org/resource/classes#')
dbo = Namespace('http://dbpedia.org/ontology/')
g.bind('dbo', dbo)

# loadind YSO-paikat graph
yso_g = Graph()
yso_g.parse('graphs/yso-paikat-skos.rdf')


# Methods for the csv-files

def add_aiheet_csv():
    g.add((snellman.Subject, namespace.RDF.type, namespace.RDFS.Class))
    g.add((snellman.Subject, namespace.SKOS.prefLabel, Literal('Aihe, Subject')))
    csv_reader = csv.reader(open('taxonomy/taxocsv_5.csv', 'r'))
    for row in csv_reader:
        s = snellman[row[0]]
        g.add((s, namespace.RDF.type, snellman.Subject))
        g.add((s, namespace.SKOS.prefLabel, Literal(row[1], lang='fi')))

def add_henkilot_csv():
    add_snellman()
    csv_reader = csv.reader(open('taxonomy/taxocsv_10.csv', 'r'))
    for row in csv_reader:
        add_personal_info(row)

def add_personal_info(row):        
    s = snellman[row[0]]
    g.add((s, namespace.RDF.type, namespace.FOAF.Person))
    g.add((s, namespace.SKOS.prefLabel, Literal(row[1], lang='fi')))
    if row[9]:
        g.add((s, namespace.SKOS.altLabel, Literal(row[9], lang='fi')))
        # Following adds family name, but not correctly in every case.
        words = row[9].split(' ')
        g.add((s, namespace.FOAF.familyName, Literal(words[len(words)-1], lang='fi')))
    cleanr = re.compile('<.*?>')
    bio = re.sub(cleanr, '', row[12])
    if len(list(bio)):
        add_bio(s, bio)

def add_bio(s, bio):
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

def add_snellman():
    s = snellman['1']
    g.add((s, namespace.RDF.type, namespace.FOAF.Person))
    g.add((s, namespace.SKOS.prefLabel, Literal('J. V. Snellman', lang='fi')))
    g.add((s, namespace.RDFS.comment, Literal('Poliitikko, filosofi, kirjailija, sanomalehtimies ja valtiomies. Suomen kansallisfilosofi.', lang='fi')))
    g.add((s, namespace.FOAF.familyName, Literal('Snellman', lang='fi')))
    g.add((s, dbo.birthyear, Literal('1806', datatype=XSD.gyear)))
    g.add((s, dbo.deathyear, Literal('1881', datatype=XSD.gyear)))
          
def add_paikat_csv():
    g.add((snellman.Place, namespace.RDF.type, namespace.RDFS.Class))
    g.add((snellman.Place, namespace.SKOS.prefLabel, Literal('Paikka, place')))
    g.add((snellman.Place, namespace.SKOS.exactMatch, dbo.Place))
    csv_reader = csv.reader(open('taxonomy/taxocsv_4.csv', 'r'))
    for row in csv_reader:
        s = snellman[row[0]]
        g.add((s, namespace.RDF.type, snellman.Place))
        g.add((s, namespace.SKOS.prefLabel, Literal(row[1], lang='fi')))
#   add_links_to_paikka(s, row[1])
        
def add_links_to_paikka(s, place):
    location = Literal(place, lang='fi')
    q = yso_g.query("""
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            SELECT ?s
            WHERE { ?s skos:prefLabel ?label . }
            """, initBindings={'label': location})
    for row in q:
        g.add((s, namespace.SKOS.exactMatch, URIRef(row[0])))
    # some places need to be linked by hand...
    
def add_kirjeenvaihto_csv():
    g.add((snellman.Correspondence, namespace.RDF.type, namespace.RDFS.Class))
    g.add((snellman.Correspondence, namespace.SKOS.prefLabel, Literal('Kirjeenvaihto, Correspondence')))
    csv_reader = csv.reader(open('taxonomy/taxocsv_8.csv', 'r'))
    for row in csv_reader:
        s = snellman[row[0]]
        g.add((s, namespace.RDF.type, snellman.Correspondence))
        g.add((s, namespace.SKOS.prefLabel, Literal(row[1], lang='fi')))

def add_tyypit_csv():
    g.add((snellman.Doctype, namespace.RDF.type, namespace.RDFS.Class))
    g.add((snellman.Doctype, namespace.SKOS.prefLabel, Literal('Dokumentin tyyppi, document type')))
    csv_reader = csv.reader(open('taxonomy/taxocsv_9.csv', 'r'))
    for row in csv_reader:
        s = snellman[row[0]]
        g.add((s, namespace.RDF.type, snellman.Doctype))
        g.add((s, namespace.SKOS.prefLabel, Literal(row[1], lang='fi')))




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

# Adding some extra properties to the letters. Unfinished...   

def add_creator(elem, s):

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


def add_content(elem, s):
    content = elem.find('field_suomi')
    if len(list(content)):
        g.add((s, snellman.hasText, Literal((BeautifulSoup(content[0][0][3].text,'lxml').text))))

def add_to_graph(elem):
    s = snellman[elem.find('nid').text]
    g.add((s, namespace.RDF.type, snellman.Document))
    g.add((s, namespace.SKOS.prefLabel, Literal(elem.find('title').text)))
    path = elem.find('path')
    g.add((s, namespace.RDFS.comment, Literal('http://snellman.kootutteokset.fi/fi/{}'.format(path.find('alias').text))))
    add_people(elem, s)
    add_places(elem, s)
    add_concepts(elem, s)
    add_type(elem, s)
    add_time(elem, s)
    add_creator(elem, s)
    add_content(elem, s)

def add_export():
    g.add((snellman.Document, namespace.RDF.type, namespace.RDFS.Class))
    g.add((snellman.Document, namespace.RDFS.label, Literal('Document')))
    g.add((snellman.Document, namespace.OWL.equivalentClass, dc.Document))
    g.add((snellman.hasText, namespace.RDF.type, namespace.RDF.Property))
    g.add((snellman.hasText, namespace.RDFS.label, Literal('Text property')))
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


########

g.serialize('snellman.ttl', format='turtle')


# To do: Adding the actual texts(?), more sensible classes etc...
