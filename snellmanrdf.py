import xml.etree.ElementTree as ET
import csv
import re
from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef
from bs4 import BeautifulSoup
import people_to_correspondence
from string import digits

snellman = Namespace('http://ldf.fi/snellman/')
dbo = Namespace('http://dbpedia.org/ontology/')
dc = Namespace('http://purl.org/dc/elements/1.1/')


# Methods for the csv-files

def add_luvut_csv(g):
    g.add((snellman.chapter, namespace.RDF.type, namespace.RDFS.Class))
    g.add((snellman.chapter, namespace.SKOS.prefLabel, Literal('Chapter, kirjan luku')))
    csv_reader = csv.reader(open('taxonomy/taxocsv_13.csv', 'r'))
    for row in csv_reader:
        resource = snellman[row[0]]
        g.add((resource, namespace.RDF.type, snellman.chapter))
        g.add((resource, namespace.SKOS.prefLabel, Literal(row[1], lang='fi')))
    return g


def add_kirjat_csv(g):
    g.add((snellman.bioBook, namespace.RDF.type, namespace.RDFS.Class))
    g.add((snellman.bioBook, namespace.SKOS.prefLabel, Literal('Biograhical book, elamankerrallinen kirja')))
    csv_reader = csv.reader(open('taxonomy/taxocsv_12.csv', 'r'))
    for row in csv_reader:
        resource = snellman[row[0]]
        g.add((resource, namespace.RDF.type, snellman.bioBook))
        g.add((resource, namespace.SKOS.prefLabel, Literal(row[1], lang='fi')))
    return g


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
    g.add((s, namespace.RDF.type, snellman.Actor))
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

def first_name(name):
    name_split = name.split(',')
    bracket_remover = re.compile('\(.*?\)')
    if len(name_split) > 1:
        return re.sub(bracket_remover, '', name_split[1]).strip()
    else:
        return ''

def family_name(name):
    name_split = name.split(',')
    bracket_remover = re.compile('\(.*?\)')
    if len(name_split) > 1:
        return re.sub(bracket_remover, '', name_split[0]).strip()
    else:
        return ''

def add_bio(g, s, bio):
    g.add((s, namespace.RDFS.comment, Literal(bio, lang='fi')))
    # Adding birth and death years. Death years sometimes problematic...
    bio = bio.replace("n.", "")
    bio = bio.replace("n. ", "")
    bio = bio.replace("synt. ", "")
    bio = bio.replace("synt.", "")
    bio = bio.replace("Synt.", "")
    bio = bio.replace("Synt.", "")
    bio = bio.strip()
    #print(bio)
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
    g.add((s, namespace.SKOS.prefLabel, Literal('Snellman, Johan Vilhelm', lang='fi')))
    g.add((s, namespace.SKOS.altLabel, Literal('J. V. Snellman', lang='fi')))
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
        link_correspondence_to_people(g, row, s)
    people_to_correspondence.connect(g)
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


def link_correspondence_to_people(g, correspondent, letter_resource):
    #print(surname)
    if link_by_label(g, correspondent[1], letter_resource):
        #print(correspondent)
        x=1
    elif link_by_name(g, correspondent[1], letter_resource):
        #print(correspondent)
        x=1
    else:
        #print(correspondent[1])
        x=1


def link_by_label(g, correspondent, letter_resource):
    csv_reader = csv.reader(open('taxonomy/taxocsv_10.csv', 'r'))
    for row in csv_reader:
        person_resource = snellman[row[0]]
        if row[9] == correspondent:
            g.add((letter_resource, dc.relation, person_resource))
            return True
        elif row[1] == correspondent:
            g.add((letter_resource, dc.relation, person_resource))
            return True


def link_by_name(g, correspondent, letter_resource):
    csv_reader = csv.reader(open('taxonomy/taxocsv_10.csv', 'r'))
    split_name = correspondent.split(' ')
    if len(split_name) > 1:
        surname = split_name[len(split_name)-1]
        first_names = return_first_names_from_split(split_name)
        for row in csv_reader:
            person_resource = snellman[row[0]]
            if (first_name(row[1]).split(' ')[0].strip() == first_names.strip()) and (family_name(row[1]) == surname):
                g.add((letter_resource, dc.relation, person_resource))
                return True
            if first_name(row[1]).strip() == first_names.strip() and family_name(row[1]) == surname:
                g.add((letter_resource, dc.relation, person_resource))
                return True
    return False


def return_first_names_from_split(name):
    first_names = ''
    x=0
    while x < len(name)-1:
        first_names = first_names + ' ' + name[x]
        x = x+1
    return first_names

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

def add_correspondence(g, elem, s):
    correspondent = elem.find('field_kirjeenvaihto')
    if len(list(correspondent)):
        g.add((s, dc.relation, snellman[correspondent[0][0][0].text]))
    return g


def add_relations(g, elem, s, field):
    for resource in field:
        g.add((s, dc.relation, snellman[resource[0].text]))
    return g


# Adding some extra properties to the letters. Unfinished...

def add_creator(g, elem, s):
    if len(list(elem.find('field_kirjeenvaihto'))):
        add_letter_sender(g, elem, s)
        places = elem.find('field_paikat')
        if len(list(places)):
            g.add((s, namespace.RDFS.seeAlso, snellman[places[0][0][0].text]))
    else:
        g.add((s, dc.creator, snellman['1']))
    return g


# vieläkin virheitä, ainakin "Johan Jakob Nervanderilta 1833"
def add_letter_sender(g, elem, s):
    full_title = elem.find('title').text
    title = full_title.split(",")[0]
    remove_digits = str.maketrans('', '', digits)
    no_dig_title = title.translate(remove_digits).strip()
    if (no_dig_title[len(no_dig_title) - 1] == 'a' or no_dig_title[len(no_dig_title) - 1] == 'ä') and no_dig_title[len(no_dig_title) - 2] == 't':
        #people = elem.find('field_henkilot')
        #if len(list(people)):
        #    g.add((s, dc.creator, snellman[people[0][0][0].text]))
        get_correspondent(g, elem, s)
    else:
        g.add((s, dc.creator, snellman['1']))

def get_correspondent(g, elem, s):
    correspondent = elem.find('field_kirjeenvaihto')[0][0][0].text
    q = g.query("""
            PREFIX snell: <http://ldf.fi/snellman/>
            PREFIX dc: <http://purl.org/dc/elements/1.1/>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            SELECT ?person
            WHERE {
                ?correspondent dc:relation ?person .
             }
            """, initBindings={'correspondent': snellman[correspondent]})
    if len(list(q)) > 0:
        for row in q:
            g.add((s, dc.creator, URIRef(row[0])))
    # Following adds creators for some letters in a risky way that may cause mistakes
    else:
        people = elem.find('field_henkilot')
        if len(list(people)):
            g.add((s, dc.creator, snellman[people[0][0][0].text]))

def add_content(g, elem, s, g_content, id):
    content = elem.find('field_suomi')
    c_resource = snellman['content/c' + id]
    if len(list(content)):
        g.add((s, snellman.hasContent, c_resource))
        g_content.add((c_resource, snellman.hasText, Literal(BeautifulSoup(content[0][0][3].text, 'lxml').text)))
        g_content.add((c_resource, snellman.hasHTML, Literal(content[0][0][3].text)))
    return g


def add_document_to_graph(g, elem, g_content):
    document_id = elem.find('nid').text
    s = snellman[document_id]
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
    g = add_content(g, elem, s, g_content, document_id)
    g = add_correspondence(g, elem, s)
    return g


def add_basic_terms(g):
    g.add((snellman.document, namespace.RDF.type, namespace.RDFS.Class))
    g.add((snellman.document, namespace.SKOS.prefLabel, Literal('Document')))
    g.add((snellman.content, namespace.RDF.type, namespace.RDFS.Class))
    g.add((snellman.content, namespace.SKOS.prefLabel, Literal('Resource for document content')))
    g.add((snellman.hasContent, namespace.RDF.type, namespace.RDF.Property))
    g.add((snellman.hasContent, namespace.SKOS.prefLabel, Literal('Link to content resource')))
    g.add((snellman.hasText, namespace.RDF.type, namespace.RDF.Property))
    g.add((snellman.hasText, namespace.SKOS.prefLabel, Literal('Content as text')))
    g.add((snellman.hasHTML, namespace.RDF.type, namespace.RDF.Property))
    g.add((snellman.hasHTML, namespace.SKOS.prefLabel, Literal('Content in HTML-format')))
    g.add((snellman.material, namespace.RDF.type, namespace.RDFS.Class))
    g.add((snellman.hasText, namespace.SKOS.prefLabel, Literal('Biographic material')))
    g.add((snellman.materialType, namespace.RDF.type, namespace.RDF.Property))
    g.add((snellman.actor, namespace.RDF.type, namespace.RDFS.Class))
    g.add((snellman.actor, namespace.SKOS.prefLabel, Literal('Actor, toimija')))
    g.add((snellman.letterSender, namespace.RDF.type, namespace.RDF.Property))
    g.add((snellman.letterSender, namespace.SKOS.prefLabel, Literal('Sender of the letter, kirjeen lahettaja')))


def add_matrikkeli(g_content, elem):
    resource = snellman['content/m' + elem.find('nid').text]
    g_content.add((resource, namespace.RDF.type, snellman.Material))
    g_content.add((resource, namespace.SKOS.prefLabel, Literal(elem.find('title').text)))
    content = elem.find('body')[0][0][0]
    g_content.add((resource, snellman.hasText, Literal(BeautifulSoup(content.text, 'lxml').text)))
    g_content.add((resource, snellman.hasHTML, Literal(content.text)))
    g_content.add((resource, dc.type, Literal('matrikkeli')))
    path = elem.find('path')
    g_content.add((resource, dc.source, URIRef('http://snellman.kootutteokset.fi/fi/{}'.format(path.find('alias').text))))
    time = elem.find('field_pvm_alkean')
    if len(list(time)):
        g_content.add((resource, dc.date, Literal(time[0][0][0].text[:10], datatype=XSD.date)))


def add_picture(g_content, elem):
    resource = snellman['content/pic' + elem.find('nid').text]
    g_content.add((resource, namespace.RDF.type, snellman.Material))
    g_content.add((resource, namespace.SKOS.prefLabel, Literal(elem.find('title').text)))
    g_content.add((resource, dc.type, Literal('kuvalahde')))
    path = elem.find('path')
    g_content.add((resource, dc.source, URIRef('http://snellman.kootutteokset.fi/fi/{}'.format(path.find('alias').text))))
    add_time(g_content, elem, resource)


def add_kirjallisuutta(g_content, elem):
    resource = snellman['content/m' + elem.find('nid').text]
    g_content.add((resource, namespace.RDF.type, snellman.Material))
    g_content.add((resource, namespace.SKOS.prefLabel, Literal(elem.find('title').text)))
    g_content.add((resource, dc.type, Literal('kirjallisuutta')))
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
def add_secondary_info(g_content,elem):
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
    add_basic_terms(g)
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


################

graph = Graph()
content_graph = Graph()
graph.bind('', snellman)
graph.bind('skos', namespace.SKOS)
graph.bind('dc', dc)
graph.bind('foaf', namespace.FOAF)
graph.bind('dbo', dbo)

content_graph.bind('snell', snellman)
content_graph.bind('skos', namespace.SKOS)
content_graph.bind('dc', dc)
content_graph.bind('foaf', namespace.FOAF)
content_graph.bind('dbo', dbo)

add_aiheet_csv(graph)
add_henkilot_csv(graph)
add_paikat_csv(graph)
add_kirjeenvaihto_csv(graph)
add_tyypit_csv(graph)
add_kirjat_csv(graph)
add_luvut_csv(graph)
add_export(graph, content_graph)

graph.serialize('turtle/snellman.ttl', format='turtle')
content_graph.serialize('turtle/snellman_content.ttl', format='turtle')
