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