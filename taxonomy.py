import xml.etree.ElementTree as ET
import csv
import re
from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef
from bs4 import BeautifulSoup
import people_to_correspondence_manually
from string import digits
import personal_info

snellman = Namespace('http://ldf.fi/snellman/')
dbo = Namespace('http://dbpedia.org/ontology/')
dc = Namespace('http://purl.org/dc/elements/1.1/')
schema = Namespace('http://schema.org/')


# Methods for the csv-files

def add_termit_csv(g):
    g.add((snellman.subjectTerm, namespace.RDF.type, namespace.RDFS.Class))
    g.add((snellman.subjectTerm, namespace.SKOS.prefLabel, Literal('Termi', lang='fi')))
    csv_reader = csv.reader(open('taxonomy/taxocsv_11.csv', 'r'))
    for row in csv_reader:
        resource = snellman[row[0]]
        g.add((resource, namespace.RDF.type, snellman.SubjectTerm))
        g.add((resource, namespace.SKOS.prefLabel, Literal(row[1], lang='fi')))
    return g

def add_luvut_csv(g):
    g.add((snellman.chapter, namespace.RDF.type, namespace.RDFS.Class))
    g.add((snellman.chapter, namespace.SKOS.prefLabel, Literal('Luku', lang='fi')))
    csv_reader = csv.reader(open('taxonomy/taxocsv_13.csv', 'r'))
    for row in csv_reader:
        resource = snellman[row[0]]
        g.add((resource, namespace.RDF.type, snellman.Chapter))
        g.add((resource, namespace.SKOS.prefLabel, Literal(row[1], lang='fi')))
    return g


def add_kirjat_csv(g):
    g.add((snellman.bioBook, namespace.RDF.type, namespace.RDFS.Class))
    g.add((snellman.bioBook, namespace.SKOS.prefLabel, Literal('Elamänkerrallinen kirja', lang='fi')))
    csv_reader = csv.reader(open('taxonomy/taxocsv_12.csv', 'r'))
    for row in csv_reader:
        resource = snellman[row[0]]
        g.add((resource, namespace.RDF.type, snellman.BioBook))
        g.add((resource, namespace.SKOS.prefLabel, Literal(row[1], lang='fi')))
    return g


def add_asiat_csv(g):
    g.add((snellman.abstractConcept, namespace.RDF.type, namespace.RDFS.Class))
    g.add((snellman.abstractConcept, namespace.SKOS.prefLabel, Literal('Asia', lang='fi')))
    csv_reader = csv.reader(open('taxonomy/taxocsv_5.csv', 'r'))
    for row in csv_reader:
        s = snellman[row[0]]
        g.add((s, namespace.RDF.type, snellman.AbstractConcept))
        g.add((s, namespace.SKOS.prefLabel, Literal(row[1], lang='fi')))
    return g


def add_henkilot_csv(g):
    add_snellman(g)
    csv_reader = csv.reader(open('taxonomy/taxocsv_10.csv', 'r'))
    for row in csv_reader:
        personal_info.add_personal_info(g, row)
    return g


def add_snellman(g):
    s = snellman['1']
    g.add((s, namespace.RDF.type, namespace.FOAF.Person))
    g.add((s, namespace.SKOS.prefLabel, Literal('Snellman, Johan Vilhelm', lang='fi')))
    g.add((s, namespace.SKOS.altLabel, Literal('J. V. Snellman', lang='fi')))
    g.add((s, namespace.RDFS.comment, Literal('1806-1881 Poliitikko, kirjailija, sanomalehtimies, valtiomies ja Suomen kansallisfilosofi.', lang='fi')))
    g.add((s, namespace.FOAF.familyName, Literal('Snellman', lang='fi')))
    g.add((s, namespace.FOAF.givenName, Literal('Johan Vilhelm', lang='fi')))
    g.add((s, snellman.nbf, URIRef('http://ldf.fi/nbf/p996')))
    #g.add((s, dbo.birthYear, '"1806"^^xsd:gYear')) # RDFlib does not suppport gYear
    #g.add((s, dbo.deathYear, '"1881"^^xsd:gYear'))
    g.add((s, snellman.birthYear, Literal('1806', datatype=XSD.integer)))
    g.add((s, snellman.deathYear, Literal('1881', datatype=XSD.integer)))
    return g


def add_paikat_csv(g):
    g.add((snellman.place, namespace.RDF.type, namespace.RDFS.Class))
    g.add((snellman.place, namespace.SKOS.prefLabel, Literal('Paikka', lang='fi')))
    g.add((snellman.place, namespace.RDFS.subClassOf, schema.Place))
    csv_reader = csv.reader(open('taxonomy/taxocsv_4.csv', 'r'))
    for row in csv_reader:
        s = snellman[row[0]]
        g.add((s, namespace.RDF.type, snellman.Place))
        g.add((s, namespace.SKOS.prefLabel, Literal(row[1], lang='fi')))
    return g

'''
def add_kirjeenvaihto_csv(g):
    g.add((snellman.correspondence, namespace.RDF.type, namespace.RDFS.Class))
    g.add((snellman.correspondence, namespace.SKOS.prefLabel, Literal('Kirjeenvaihto', lang='fi')))
    csv_reader = csv.reader(open('taxonomy/taxocsv_8.csv', 'r'))
    for row in csv_reader:
        s = snellman[row[0]]
        g.add((s, namespace.RDF.type, snellman.Correspondence))
        g.add((s, namespace.SKOS.prefLabel, Literal(row[1], lang='fi')))
        link_correspondence_to_people(g, row, s)
    people_to_correspondence_manually.connect(g)
    return g
'''

def add_tyypit_csv(g):
    g.add((snellman.doctype, namespace.RDF.type, namespace.RDFS.Class))
    g.add((snellman.doctype, namespace.SKOS.prefLabel, Literal('Dokumentin tyyppi', lang='fi')))
    csv_reader = csv.reader(open('taxonomy/taxocsv_9.csv', 'r'))
    for row in csv_reader:
        s = snellman[row[0]]
        g.add((s, namespace.RDF.type, snellman.Doctype))
        g.add((s, namespace.SKOS.prefLabel, Literal(row[1], lang='fi')))
    return g

'''

# Linkkejä kirjeenvaihdon ja henkilöiden välille

def link_correspondence_to_people(g, correspondent, letter_resource):
    #print(surname)
    if link_by_label(g, correspondent[1], letter_resource):
        pass
    elif link_by_name(g, correspondent[1], letter_resource):
        pass
    else:
        pass


def link_by_label(g, correspondent, letter_resource):
    csv_reader = csv.reader(open('taxonomy/taxocsv_10.csv', 'r'))
    for row in csv_reader:
        person_resource = snellman[row[0]]
        if row[9] == correspondent:
            g.add((letter_resource, snellman.correspondent, person_resource))
            return True
        elif row[1] == correspondent:
            g.add((letter_resource, snellman.correspondent, person_resource))
            return True


def link_by_name(g, correspondent, letter_resource):
    csv_reader = csv.reader(open('taxonomy/taxocsv_10.csv', 'r'))
    split_name = correspondent.split(' ')
    if len(split_name) > 1:
        surname = split_name[len(split_name)-1]
        first_names = return_first_names_from_split(split_name)
        for row in csv_reader:
            person_resource = snellman[row[0]]
            if (personal_info.first_name(row[1]).split(' ')[0].strip() == first_names.strip()) and (personal_info.family_name(row[1]) == surname):
                g.add((letter_resource, snellman.correspondent, person_resource))
                return True
            if personal_info.first_name(row[1]).strip() == first_names.strip() and personal_info.family_name(row[1]) == surname:
                g.add((letter_resource, snellman.correspondent, person_resource))
                return True
    return False


def return_first_names_from_split(name):
    first_names = ''
    x=0
    while x < len(name)-1:
        first_names = first_names + ' ' + name[x]
        x = x+1
    return first_names
    '''
