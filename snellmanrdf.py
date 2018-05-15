from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef
import people_to_correspondence
import taxonomy
import documents

snellman = Namespace('http://ldf.fi/snellman/')
dbo = Namespace('http://dbpedia.org/ontology/')
dc = Namespace('http://purl.org/dc/elements/1.1/')


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

taxonomy.add_aiheet_csv(graph)
taxonomy.add_henkilot_csv(graph)
taxonomy.add_paikat_csv(graph)
taxonomy.add_kirjeenvaihto_csv(graph)
taxonomy.add_tyypit_csv(graph)
taxonomy.add_kirjat_csv(graph)
taxonomy.add_luvut_csv(graph)
documents.add_export(graph, content_graph)

graph.serialize('turtle/snellman.ttl', format='turtle')
content_graph.serialize('turtle/snellman_content.ttl', format='turtle')
