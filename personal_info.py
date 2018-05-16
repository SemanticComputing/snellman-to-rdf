from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef
import re

snellman = Namespace('http://ldf.fi/snellman/')
dbo = Namespace('http://dbpedia.org/ontology/')
dc = Namespace('http://purl.org/dc/elements/1.1/')


def add_personal_info(g, person):
    s = snellman[person[0]]
    g.add((s, namespace.RDF.type, snellman.Actor))
    g.add((s, namespace.RDF.type, namespace.FOAF.Person))
    g.add((s, namespace.SKOS.prefLabel, Literal(person[1], lang='fi')))
    name_split = person[1].split(',')
    bracket_remover = re.compile('\(.*?\)')
    if len(name_split) > 1:
        family_name = re.sub(bracket_remover, '', name_split[0]).strip()
        g.add((s, namespace.FOAF.familyName, Literal(family_name, lang='fi')))
        first_name = re.sub(bracket_remover, '', name_split[1]).strip()
        g.add((s, namespace.FOAF.givenName, Literal(first_name, lang='fi')))
    if person[9]:
        g.add((s, namespace.SKOS.altLabel, Literal(person[9], lang='fi')))
    cleanr = re.compile('<.*?>')
    bio = re.sub(cleanr, '', person[12])
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