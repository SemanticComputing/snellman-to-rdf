from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef
import taxonomy
import documents
import corrections_to_places

snellman = Namespace('http://ldf.fi/snellman/')
dbo = Namespace('http://dbpedia.org/ontology/')
dc = Namespace('http://purl.org/dc/elements/1.1/')

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


def add_basic_schema(g):
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
    g.add((snellman.material, namespace.SKOS.prefLabel, Literal('Biographic material')))

    g.add((snellman.materialType, namespace.RDF.type, namespace.RDF.Property))

    g.add((snellman.actor, namespace.RDF.type, namespace.RDFS.Class))
    g.add((snellman.actor, namespace.SKOS.prefLabel, Literal('Actor, toimija')))

    #g.add((snellman.letterSender, namespace.RDF.type, namespace.RDF.Property))
    #g.add((snellman.letterSender, namespace.SKOS.prefLabel, Literal('Sender of the letter, kirjeen lahettaja')))

    g.add((snellman.dateComment, namespace.RDF.type, namespace.RDF.Property))
    g.add((snellman.dateComment, namespace.SKOS.prefLabel, Literal('Comment regarding the accuracy of the date')))

    g.add((snellman.birthYear, namespace.RDF.type, namespace.RDF.Property))

    g.add((snellman.deathYear, namespace.RDF.type, namespace.RDF.Property))

    g.add((snellman.correspondent, namespace.RDF.type, namespace.RDF.Property))
    g.add((snellman.correspondent, namespace.SKOS.prefLabel, Literal('Person or organisation related to the correspondence resource')))

    g.add((snellman.writtenIn, namespace.RDF.type, namespace.RDF.Property))
    g.add((snellman.writtenIn, namespace.SKOS.prefLabel, Literal('Place where the text was propably written')))

    #g.add((snellman.relation, namespace.RDF.type, namespace.RDF.Property))
    #g.add((snellman.relation, namespace.SKOS.prefLabel, Literal('A resource related to the text')))

    g.add((snellman.nbf, namespace.RDF.type, namespace.RDF.Property))
    g.add((snellman.nbf, namespace.SKOS.prefLabel, Literal('Link to nbf resource')))


add_basic_schema(graph)
taxonomy.add_aiheet_csv(graph)
taxonomy.add_henkilot_csv(graph)
taxonomy.add_paikat_csv(graph)
taxonomy.add_kirjeenvaihto_csv(graph)
taxonomy.add_tyypit_csv(graph)
taxonomy.add_kirjat_csv(graph)
taxonomy.add_luvut_csv(graph)
taxonomy.add_termit_csv(graph)
documents.add_export(graph, content_graph)
corrections_to_places.correct_places_on_letters(graph)

graph.serialize('turtle/snellman.ttl', format='turtle')
content_graph.serialize('turtle/snellman_content.ttl', format='turtle')
