from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef
import personal_info
import csv
import people_to_correspondence_manually

snellman = Namespace('http://ldf.fi/snellman/')

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
            try:
                if (personal_info.first_name(row[1]).split(' ')[1].strip() == first_names.strip()) and (personal_info.family_name(row[1]) == surname):
                    g.add((letter_resource, snellman.correspondent, person_resource))
                    return True
            except IndexError:
                pass
            try:
                if (personal_info.first_name(row[1]).split(' ')[2].strip() == first_names.strip()) and (personal_info.family_name(row[1]) == surname):
                    g.add((letter_resource, snellman.correspondent, person_resource))
                    return True
            except IndexError:
                pass
    return False


def return_first_names_from_split(name):
    first_names = ''
    x=0
    while x < len(name)-1:
        first_names = first_names + ' ' + name[x]
        x = x+1
    return first_names

# graph = Graph()
# add_kirjeenvaihto_csv(graph)
# graph.serialize('graphs/test.ttl', format='turtle')