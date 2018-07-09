import xml.etree.ElementTree as ET
import csv
import re
from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef
from bs4 import BeautifulSoup
from string import digits

snellman = Namespace('http://ldf.fi/snellman/')
dbo = Namespace('http://dbpedia.org/ontology/')
dc = Namespace('http://purl.org/dc/elements/1.1/')


# Methods for export.xml

def add_people(g, elem, s):
    people = elem.find('field_henkilot')
    if len(list(people)):
        for resource in people[0]:
            g.add((s, snellman.relatedPerson, snellman[resource[0].text]))
    return g


def add_places(g, elem, s):
    places = elem.find('field_paikat')
    if len(list(places)):
        for resource in places[0]:
            g.add((s, snellman.relatedPlace, snellman[resource[0].text]))
    return g


def add_concepts(g, elem, s):
    concepts = elem.find('field_asiat')
    if len(list(concepts)):
        for subject in concepts[0]:
            g.add((s, dc.subject, snellman[subject[0].text]))
    return g

def add_terms(g, elem, s):
    terms = elem.find('field_termit')
    if len(list(terms)):
        for term in terms[0]:
            g.add((s, dc.subject, snellman[term[0].text]))
    return g


def add_type(g, elem, s):
    doctype = elem.find('field_dokumentin_tyyppi')
    if len(list(doctype)):
        g.add((s, dc.type, snellman[doctype[0][0][0].text]))
    return g


def add_time(g, elem, s):
    time = elem.find('field_date')
    if len(list(time)):
        g.add((s, dc.date, Literal(time[0][0][0].text[:10], datatype=XSD.date)))
    return g

def add_correspondence(g, elem, s):
    correspondent = elem.find('field_kirjeenvaihto')
    if len(list(correspondent)):
        g.add((s, snellman.relatedCorrespondence, snellman[correspondent[0][0][0].text]))
    return g


# Adding some extra properties to the letters. Unfinished...

def remove_extra(s):
    answer = []
    for char in s:
        if (not char.isdigit()) and (char != '.'):
            answer.append(char)
    return ''.join(answer).replace('kesällä','').strip()

def add_creator(g, elem, s):
    no_dig_title = remove_extra(elem.find('title').text.split(',')[0])
    if len(list(elem.find('field_kirjeenvaihto'))):
        add_letter_sender(g, elem, s)
        places = elem.find('field_paikat')
        if len(list(places)):
            g.add((s, snellman.writtenIn, snellman[places[0][0][0].text]))
        return g
    elif get_type(g, s) == "Virkakirje" or "Yksityiskirje":
            if (no_dig_title[len(no_dig_title) - 1] == 'a' or no_dig_title[len(no_dig_title) - 1] == 'ä') \
                    and no_dig_title[len(no_dig_title) - 2] == 't':
                return g
    g.add((s, dc.creator, snellman['1']))
    return g


def add_letter_sender(g, elem, s):
    no_dig_title = remove_extra(elem.find('title').text.split(',')[0])
    if (no_dig_title[len(no_dig_title) - 1] == 'a' or no_dig_title[len(no_dig_title) - 1] == 'ä') and (no_dig_title[len(no_dig_title) - 2] == 't'):
        set_correspondent(g, elem, s)
    else:
        g.add((s, dc.creator, snellman['1']))

# type needs to be defined in graph before this is called...
def get_type(g, s):
    q = g.query("""
            PREFIX snell: <http://ldf.fi/snellman/>
            PREFIX dc: <http://purl.org/dc/elements/1.1/>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            SELECT ?stripped_label
            WHERE {
                ?s dc:type ?type .
  	            ?type skos:prefLabel ?type_label .
  	            BIND(STR(?type_label) As ?stripped_label) .
             }
            """, initBindings={'s': s})
    for row in q:
        return row[0]


def set_correspondent(g, elem, s):
    correspondent = elem.find('field_kirjeenvaihto')[0][0][0].text
    q = g.query("""
            PREFIX snell: <http://ldf.fi/snellman/>
            PREFIX dc: <http://purl.org/dc/elements/1.1/>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            SELECT ?person
            WHERE {
                ?correspondent snell:correspondent ?person .
             }
            """, initBindings={'correspondent': snellman[correspondent]})
    if len(list(q)) > 0:
        for row in q:
            g.add((s, dc.creator, URIRef(row[0])))
    # Following adds creators for some letters in a risky way that may cause mistakes
    # The first person in field_henkilöt is a likely creator of the letter, but this could be done better
    else:
        people = elem.find('field_henkilot')
        if len(list(people)):
            g.add((s, dc.creator, snellman[people[0][0][0].text]))

def add_content(g, elem, s, g_content, id):
    content = elem.find('field_suomi')
    c_resource = snellman['content/c' + id]
    if len(list(content)):
        g.add((s, snellman.hasContent, c_resource))
        g_content.add((c_resource, namespace.RDF.type, snellman.Content))
        g_content.add((c_resource, snellman.hasText, Literal(BeautifulSoup(content[0][0][3].text, 'lxml').text)))
        g_content.add((c_resource, snellman.hasHTML, Literal(content[0][0][3].text)))
    return g

def add_date_comment(g, elem, s):
    date_comment = elem.find('field_pvm_kommenti')
    if len(list(date_comment)):
        g.add((s, snellman.dateComment, Literal(date_comment[0][0][0].text)))
    return g


def add_document_to_graph(g, elem, g_content):
    document_id = elem.find('nid').text

    s = snellman[document_id]   # Bad naming, this is used a lot as subject in rdf, but it could be named better

    g.add((s, namespace.RDF.type, snellman.Material))
    g.add((s, snellman.materialType, Literal('tekstilahde')))

    g.add((s, namespace.RDF.type, snellman.Document))
    g.add((s, namespace.SKOS.prefLabel, Literal(elem.find('title').text)))

    path = elem.find('path')
    g.add((s, dc.source, URIRef('http://snellman.kootutteokset.fi/fi/{}'.format(path.find('alias').text))))
    g = add_people(g, elem, s)
    g = add_places(g, elem, s)
    g = add_concepts(g, elem, s)
    g = add_terms(g, elem, s)
    g = add_type(g, elem, s)
    g = add_time(g, elem, s)
    g = add_date_comment(g, elem, s)
    g = add_creator(g, elem, s)
    g = add_content(g, elem, s, g_content, document_id)
    g = add_correspondence(g, elem, s)
    return g



def add_matrikkeli(g_content, elem):
    resource = snellman['content/m' + elem.find('nid').text]
    g_content.add((resource, namespace.RDF.type, snellman.Material))
    g_content.add((resource, namespace.SKOS.prefLabel, Literal(elem.find('title').text)))
    content = elem.find('body')[0][0][0]
    g_content.add((resource, snellman.hasText, Literal(BeautifulSoup(content.text, 'lxml').text)))
    g_content.add((resource, snellman.hasHTML, Literal(content.text)))
    g_content.add((resource, snellman.materialType, Literal('matrikkeli')))
    path = elem.find('path')
    g_content.add((resource, dc.source, URIRef('http://snellman.kootutteokset.fi/fi/{}'.format(path.find('alias').text))))
    time = elem.find('field_pvm_alkean')
    if len(list(time)):
        g_content.add((resource, dc.date, Literal(time[0][0][0].text[:10], datatype=XSD.date)))


def add_picture(g_content, elem):
    resource = snellman['content/pic' + elem.find('nid').text]
    g_content.add((resource, namespace.RDF.type, snellman.Material))
    g_content.add((resource, namespace.SKOS.prefLabel, Literal(elem.find('title').text)))
    g_content.add((resource, snellman.materialType, Literal('kuvalahde')))
    path = elem.find('path')
    g_content.add((resource, dc.source, URIRef('http://snellman.kootutteokset.fi/fi/{}'.format(path.find('alias').text))))
    add_time(g_content, elem, resource)


def add_kirjallisuutta(g_content, elem):
    resource = snellman['content/m' + elem.find('nid').text]
    g_content.add((resource, namespace.RDF.type, snellman.Material))
    g_content.add((resource, namespace.SKOS.prefLabel, Literal(elem.find('title').text)))
    g_content.add((resource, snellman.materialType, Literal('kirjallisuutta')))
    try:
        content = elem.find('body')[0][0][0]
        g_content.add((resource, snellman.hasText, Literal(BeautifulSoup(content.text, 'lxml').text)))
        g_content.add((resource, snellman.hasHTML, Literal(content.text)))
        path = elem.find('path')
        g_content.add((resource, dc.source, URIRef('http://snellman.kootutteokset.fi/fi/{}'.format(path.find('alias').text))))
    except:
        pass


def add_kirjan_luku(g_content, elem):
    resource = snellman['content/m' + elem.find('nid').text]
    g_content.add((resource, namespace.RDF.type, snellman.Material))
    g_content.add((resource, namespace.SKOS.prefLabel, Literal(elem.find('title').text)))
    g_content.add((resource, dc.type, Literal('kirjan_luku')))
    try:
        content = elem.find('body')[0][0][0]
        g_content.add((resource, snellman.hasText, Literal(BeautifulSoup(content.text, 'lxml').text)))
        g_content.add((resource, snellman.hasHTML, Literal(content.text)))
        path = elem.find('path')
        g_content.add((resource, dc.source, URIRef('http://snellman.kootutteokset.fi/fi/{}'.format(path.find('alias').text))))
    except:
        pass
    kirja = elem.find('field_kirja')
    if len(list(kirja)):
        g_content.add((resource, dc.relation, snellman[kirja[0][0][0].text]))
    luku = elem.find('field_ylaluku')
    if len(list(luku)):
        g_content.add((resource, dc.relation, snellman[luku[0][0][0].text]))


# Adds this and some others: http://snellman.kootutteokset.fi/fi/node/6846
def add_secondary_info(g_content, elem):
    resource = snellman['content/m' + elem.find('nid').text]
    g_content.add((resource, namespace.RDF.type, snellman.Material))
    g_content.add((resource, namespace.SKOS.prefLabel, Literal(elem.find('title').text)))
    g_content.add((resource, dc.type, Literal('tietoa')))
    try:
        content = elem.find('body')[0][0][0]
        g_content.add((resource, snellman.hasText, Literal(BeautifulSoup(content.text, 'lxml').text)))
        g_content.add((resource, snellman.hasHTML, Literal(content.text)))
        g_content.add((resource, dc.source, URIRef('http://snellman.kootutteokset.fi/fi/node/{}'.format(elem.find('nid').text))))
    except:
        pass

def add_export(g, g_content):
    for event, elem in ET.iterparse('export.xml', events=("start", "end")):
        if event == 'end':
            if elem.tag == 'node':
                if elem.find('type').text == 'tekstilahde':
                    g = add_document_to_graph(g, elem, g_content)
                elif elem.find('type').text == 'matrikkeli':
                    add_matrikkeli(g_content, elem)
                elif elem.find('type').text == 'kuvalahde':
                    add_picture(g_content, elem)
                elif elem.find('type').text == 'kirjallisuutta':
                    add_kirjallisuutta(g_content, elem)
                elif elem.find('type').text == 'kirjan_luku':
                    add_kirjan_luku(g_content, elem)
                elif elem.find('type').text == 'secondary_highlights':
                    add_secondary_info(g_content, elem)
                    #print(ET.tostring(elem, encoding='utf8', method='xml'))
                #else:
                #    print(elem.find('type').text)
    return g

