from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef
import csv

snellman = Namespace('http://ldf.fi/snellman/')

def map_from_old(g_source, g_write):
    q = g_source.query("""
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            PREFIX snellman: <http://ldf.fi/snellman/>
            SELECT ?person ?wdPerson
            WHERE { 
                ?person a foaf:Person .
                ?person snellman:wikidata ?wdPerson .
            }
            """)

    for row in q:
        g_write.add((URIRef(row[0]), snellman.wikidata, URIRef(row[1])))


graph_source = Graph()
graph_write = Graph()
graph_source.parse('graphs/snellman_links.ttl', format='turtle')
graph_write.parse('turtle/snellman.ttl', format='turtle')
map_from_old(graph_source, graph_write)
graph_write.serialize('turtle/snellman.ttl', format='turtle')