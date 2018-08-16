# Linking AbstractConcepts / asiat

from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef
import requests
import csv

snellman = Namespace('http://ldf.fi/snellman/')
koko = Namespace('http://www.yso.fi/onto/koko/')

def link_to_yso(g, concept_g, s, concept):
    concept = Literal(concept.lower(), lang='fi')
    q = concept_g.query("""
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            SELECT ?s
            WHERE { ?s concept skos:prefLabel|skos:hiddenLabel|skos:altLabel ?label . }
            """, initBindings={'label': concept})
    if len(list(q)) > 0:
        for row in q:
            g.add((s, snellman.yso, URIRef(row[0])))
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
        elif link_to_yso(g, yso_g, resource_id, row[1] + ' (tapahtumat)'):
            pass
        elif link_to_yso(g, yso_g, resource_id, row[1] + ' (ilmiöt)'):
            pass
        philosophy(g, resource_id, row[1])
    #manual_links(g)

def philosophy(g, s, concept):
    if 'filosofia' in concept:
        g.add((s, namespace.SKOS.broader, snellman['13418']))


def link_to_koko(g, concept_g, s, concept):
    concept = Literal(concept.lower(), lang='fi')
    q = concept_g.query("""
        SELECT DISTINCT ?concept
        WHERE { 
          ?concept a ?conceptScheme .
          ?concept skos:prefLabel|skos:hiddenLabel|skos:altLabel ?label .
        }
            """, initBindings={'label': concept})
    if len(list(q)) > 0:
        for row in q:
            g.add((s, namespace.SKOS.closeMatch, URIRef(row[0])))
        return True
    else:
        return False

def link_concepts_to_koko(g):
    csv_reader = csv.reader(open('taxonomy/taxocsv_5.csv', 'r'))
    koko_g = Graph()
    koko_g.parse('graphs/koko-skos.ttl', format='turtle')
    print("parsed koko-skos.ttl succesfully, mapping...")
    for row in csv_reader:
        resource_id = snellman[row[0]]
        if link_to_koko(g, koko_g, resource_id, row[1]):
            pass
        if 'filosofia' in row[1]:
            g.add((resource_id, namespace.SKOS.broadMatch, koko.p34913))
    manual_mapping(g)


def manual_mapping(g):
    g.add((snellman['13839'], namespace.SKOS.broadMatch, koko['p67602'])) # hypoteekki -> asuntolainoitus
    # g.add((snellman['13859'], namespace.SKOS.broadMatch, koko['p2246'])) # suomenkieli -> kielikysymys
    g.add((snellman['13270'], namespace.SKOS.closeMatch, koko['p1234'])) # ulkomaanmatkailu -> ulkomaanmatka
    g.add((snellman['13312'], namespace.SKOS.closeMatch, koko['p50183'])) # ystäväpiiri -> ystävät
    g.add((snellman['13245'], namespace.SKOS.broadMatch, koko['p35181'])) # sanomalehtimies -> toimittajat
    g.add((snellman['13637'], namespace.SKOS.broadMatch, koko['p6367'])) # rahauudistus -> rahapolitiika
    g.add((snellman['13541'], namespace.SKOS.closeMatch, koko['p18782'])) # edustuslaitos -> kansanedustuslaitokset
    g.add((snellman['13520'], namespace.SKOS.closeMatch, koko['p64653'])) # pankkilaitos -> pankki- ja rahoitustoiminta

    # removing dublicates, leaving best match
    g.remove((snellman['13222'], namespace.SKOS.closeMatch, koko['p48206'])) # perhe

    g.remove((snellman['13251'], namespace.SKOS.closeMatch, koko['p34538'])) # kirjallisuus, little unclear which is correct one
    g.remove((snellman['13251'], namespace.SKOS.closeMatch, koko['p37095'])) # left kaunokirjallisuus
    g.remove((snellman['13251'], namespace.SKOS.closeMatch, koko['p25991']))


graph = Graph()
graph.parse('turtle/snellman.ttl', format='turtle')
#link_concepts(graph)
link_concepts_to_koko(graph)
graph.serialize('turtle/snellman.ttl', format='turtle')