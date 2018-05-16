# Linking subjects / asiat

from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef
import requests
import csv

snellman = Namespace('http://ldf.fi/snellman/')

def link_to_yso(g, concept_g, s, concept):
    concept = Literal(concept.lower(), lang='fi')
    q = concept_g.query("""
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            SELECT ?s
            WHERE { ?s skos:prefLabel ?label . }
            """, initBindings={'label': concept})
    if len(list(q)) > 0:
        for row in q:
            g.add((s, namespace.SKOS.exactMatch, URIRef(row[0])))
        return True
    else:
        return False

def link_to_yso_alt(g, concept_g, s, concept):
    concept = Literal(concept.lower(), lang='fi')
    q = concept_g.query("""
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            SELECT ?s
            WHERE { ?s skos:altLabel ?label . }
            """, initBindings={'label': concept})
    if len(list(q)) > 0:
        for row in q:
            g.add((s, namespace.SKOS.exactMatch, URIRef(row[0])))
        return True
    else:
        return False


def link_concepts(g):
    csv_reader = csv.reader(open('taxonomy/taxocsv_5.csv', 'r'))
    yso_g = Graph()
    yso_g.parse('graphs/yso-skos.ttl', format='turtle')

    for row in csv_reader:
        resource_id = snellman[row[0]]
        if link_to_yso(g, yso_g, resource_id, row[1]):
            pass
        elif link_to_yso(g, yso_g, resource_id, row[1] + 't'):
            pass
        elif link_to_yso_alt(g, yso_g, resource_id, row[1]):
            pass
        elif link_to_yso(g, yso_g, resource_id, row[1] + ' (tapahtumat)'):
            pass
        elif link_to_yso(g, yso_g, resource_id, row[1] + ' (ilmiöt)'):
            pass
        philosophy(g, resource_id, row[1])
    #manual_links(g)

def philosophy(g, s, concept):
    if 'filosofia' in concept:
        g.add((s, namespace.SKOS.broader, snellman['13418']))

graph = Graph()
graph.parse('turtle/snellman.ttl', format='turtle')
link_concepts(graph)
graph.serialize('turtle/snellman.ttl', format='turtle')