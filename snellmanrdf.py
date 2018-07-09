from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef
import taxonomy
import documents
import corrections_to_places
import correspondence

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
    g.add((snellman.document, namespace.SKOS.prefLabel, Literal('Document', lang='en')))

    g.add((snellman.content, namespace.RDF.type, namespace.RDFS.Class))
    g.add((snellman.content, namespace.SKOS.prefLabel, Literal('Resource for document content', lang='en')))

    g.add((snellman.hasContent, namespace.RDF.type, namespace.RDF.Property))
    g.add((snellman.hasContent, namespace.SKOS.prefLabel, Literal('Link to content resource', lang='en')))

    g.add((snellman.hasText, namespace.RDF.type, namespace.RDF.Property))
    g.add((snellman.hasText, namespace.SKOS.prefLabel, Literal('Content as text', lang='en')))

    g.add((snellman.hasHTML, namespace.RDF.type, namespace.RDF.Property))
    g.add((snellman.hasHTML, namespace.SKOS.prefLabel, Literal('Content in HTML-format', lang='en')))

    g.add((snellman.material, namespace.RDF.type, namespace.RDFS.Class))
    g.add((snellman.material, namespace.SKOS.prefLabel, Literal('Biographic material', lang='en')))

    g.add((snellman.materialType, namespace.RDF.type, namespace.RDF.Property))

    g.add((snellman.actor, namespace.RDF.type, namespace.RDFS.Class))
    g.add((snellman.actor, namespace.SKOS.prefLabel, Literal('Actor, toimija')))

    #g.add((snellman.letterSender, namespace.RDF.type, namespace.RDF.Property))
    #g.add((snellman.letterSender, namespace.SKOS.prefLabel, Literal('Sender of the letter, kirjeen lahettaja')))

    g.add((snellman.dateComment, namespace.RDF.type, namespace.RDF.Property))
    g.add((snellman.dateComment, namespace.SKOS.prefLabel, Literal('Comment regarding the accuracy of the date', lang='en')))

    g.add((snellman.birthYear, namespace.RDF.type, namespace.RDF.Property))
    g.add((snellman.birthYear, namespace.SKOS.prefLabel, Literal('Syntymävuosi', lang='fi')))

    g.add((snellman.deathYear, namespace.RDF.type, namespace.RDF.Property))
    g.add((snellman.deathYear, namespace.SKOS.prefLabel, Literal('Kuolinvuosi', lang='fi')))

    g.add((snellman.correspondent, namespace.RDF.type, namespace.RDF.Property))
    g.add((snellman.correspondent, namespace.SKOS.prefLabel, Literal('Person or organisation related to the correspondence resource', lang='en')))

    g.add((snellman.writtenIn, namespace.RDF.type, namespace.RDF.Property))
    g.add((snellman.writtenIn, namespace.SKOS.prefLabel, Literal('Place where the text was propably written', lang='en')))

    #g.add((snellman.relation, namespace.RDF.type, namespace.RDF.Property))
    #g.add((snellman.relation, namespace.SKOS.prefLabel, Literal('A resource related to the text')))

    g.add((snellman.nbf, namespace.RDF.type, namespace.RDF.Property))
    g.add((snellman.nbf, namespace.RDFS.subPropertyOf, namespace.SKOS.exactMatch))
    g.add((snellman.nbf, namespace.SKOS.prefLabel, Literal('Link to nbf resource', lang='en')))

    g.add((snellman.wikidata, namespace.RDF.type, namespace.RDF.Property))
    g.add((snellman.wikidata, namespace.RDFS.subPropertyOf, namespace.SKOS.exactMatch))
    g.add((snellman.wikidata, namespace.SKOS.prefLabel, Literal('Link to Wikidata resource', lang='en')))

    g.add((snellman.yso, namespace.RDF.type, namespace.RDF.Property))
    g.add((snellman.yso, namespace.RDFS.subPropertyOf, namespace.SKOS.closeMatch))
    g.add((snellman.yso, namespace.SKOS.prefLabel, Literal('Link to YSO resource', lang='en')))

    g.add((snellman.relatedPlace, namespace.RDF.type, namespace.RDF.Property))
    g.add((snellman.relatedPlace, namespace.RDFS.subPropertyOf, dc.Relation))
    g.add((snellman.relatedPlace, namespace.SKOS.prefLabel, Literal('Dokumenttiin liittyvä paikka', lang='fi')))

    g.add((snellman.relatedPerson, namespace.RDF.type, namespace.RDF.Property))
    g.add((snellman.relatedPerson, namespace.RDFS.subPropertyOf, dc.Relation))
    g.add((snellman.relatedPerson, namespace.SKOS.prefLabel, Literal('Dokumenttiin liittyvä henkilö', lang='fi')))

    g.add((snellman.relatedCorrespondence, namespace.RDF.type, namespace.RDF.Property))
    g.add((snellman.relatedCorrespondence, namespace.RDFS.subPropertyOf, dc.Relation))
    g.add((snellman.relatedCorrespondence, namespace.SKOS.prefLabel, Literal('Dokumenttiin liittyvä kiirjeenvaihto', lang='fi')))




add_basic_schema(graph)
taxonomy.add_aiheet_csv(graph)
taxonomy.add_henkilot_csv(graph)
taxonomy.add_paikat_csv(graph)
#taxonomy.add_kirjeenvaihto_csv(graph)
correspondence.add_kirjeenvaihto_csv(graph)
taxonomy.add_tyypit_csv(graph)
taxonomy.add_kirjat_csv(graph)
taxonomy.add_luvut_csv(graph)
taxonomy.add_termit_csv(graph)
documents.add_export(graph, content_graph)
corrections_to_places.correct_places_on_letters(graph)

graph.serialize('turtle/snellman.ttl', format='turtle')
content_graph.serialize('turtle/snellman_content.ttl', format='turtle')
