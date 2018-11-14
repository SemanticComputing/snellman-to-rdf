from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef
import taxonomy
import documents
import corrections_to_places
import correspondence

snellman = Namespace('http://ldf.fi/snellman/')
dbo = Namespace('http://dbpedia.org/ontology/')
dc = Namespace('http://purl.org/dc/elements/1.1/')
schema = Namespace('http://schema.org/')

graph = Graph()
content_graph = Graph()
extra_graph = Graph()

graph.bind('', snellman)
graph.bind('skos', namespace.SKOS)
graph.bind('dc', dc)
graph.bind('foaf', namespace.FOAF)
graph.bind('dbo', dbo)

content_graph.bind('', snellman)
content_graph.bind('skos', namespace.SKOS)
content_graph.bind('dc', dc)
content_graph.bind('foaf', namespace.FOAF)
content_graph.bind('dbo', dbo)

extra_graph.bind('', snellman)
extra_graph.bind('skos', namespace.SKOS)
extra_graph.bind('dc', dc)


def add_basic_schema(g):
    g.add((snellman.document, namespace.RDF.type, namespace.RDFS.Class))
    g.add((snellman.document, namespace.SKOS.prefLabel, Literal('Document', lang='en')))
    g.add((snellman.document, namespace.SKOS.prefLabel, Literal('J. V. Snellmanin teosten tekstilähde', lang='fi')))
    g.add((snellman.document, namespace.RDFS.subClassOf, schema.CreativeWork))

    g.add((snellman.content, namespace.RDF.type, namespace.RDFS.Class))
    g.add((snellman.content, namespace.SKOS.prefLabel, Literal('Resource for document content', lang='en')))
    g.add((snellman.content, namespace.SKOS.prefLabel, Literal('Sisällön resurssi', lang='fi')))

    g.add((snellman.hasContent, namespace.RDF.type, namespace.RDF.Property))
    g.add((snellman.hasContent, namespace.SKOS.prefLabel, Literal('Link to content resource', lang='en')))
    g.add((snellman.hasContent, namespace.SKOS.prefLabel, Literal('Dokumenttiin liittyvä sisältö', lang='fi')))

    g.add((snellman.hasText, namespace.RDF.type, namespace.RDF.Property))
    g.add((snellman.hasText, namespace.SKOS.prefLabel, Literal('Content as text', lang='en')))
    g.add((snellman.hasText, namespace.SKOS.prefLabel, Literal('Sisältö muotoilemattomana tekstinä', lang='fi')))

    g.add((snellman.hasHTML, namespace.RDF.type, namespace.RDF.Property))
    g.add((snellman.hasHTML, namespace.SKOS.prefLabel, Literal('Content in HTML-format', lang='en')))
    g.add((snellman.hasHTML, namespace.SKOS.prefLabel, Literal('Sisältö HTML-muodossa', lang='fi')))

    g.add((snellman.material, namespace.RDF.type, namespace.RDFS.Class))
    g.add((snellman.material, namespace.SKOS.prefLabel, Literal('A document related to Snellman-portal', lang='en')))
    g.add((snellman.material, namespace.SKOS.prefLabel, Literal('Mikä tahansa Snellman-portaaliin liittyvä dokumentti', lang='fi')))

    g.add((snellman.materialType, namespace.RDF.type, namespace.RDF.Property))
    g.add((snellman.materialType, namespace.SKOS.prefLabel, Literal('Materiaalin tyyppi', lang='fi')))

    g.add((snellman.actor, namespace.RDF.type, namespace.RDFS.Class))
    g.add((snellman.actor, namespace.SKOS.prefLabel, Literal('Actor, toimija', lang='fi')))

    g.add((snellman.dateComment, namespace.RDF.type, namespace.RDF.Property))
    g.add((snellman.dateComment, namespace.SKOS.prefLabel, Literal('Comment regarding the accuracy of the date', lang='en')))
    g.add((snellman.dateComment, namespace.SKOS.prefLabel, Literal('Päivämäärän tarkkuuteen liittyvä kommentti', lang='fi')))

    g.add((snellman.birthYear, namespace.RDF.type, namespace.RDF.Property))
    g.add((snellman.birthYear, namespace.SKOS.prefLabel, Literal('Syntymävuosi', lang='fi')))

    g.add((snellman.deathYear, namespace.RDF.type, namespace.RDF.Property))
    g.add((snellman.deathYear, namespace.SKOS.prefLabel, Literal('Kuolinvuosi', lang='fi')))

    g.add((snellman.correspondent, namespace.RDF.type, namespace.RDF.Property))
    g.add((snellman.correspondent, namespace.SKOS.prefLabel, Literal('Person or organisation related to the correspondence resource', lang='en')))
    g.add((snellman.correspondent, namespace.SKOS.prefLabel,
           Literal('Henkilö, organisaatio tai vastaava, joka liittyy kirjeenvaihto-resurssiin', lang='fi')))

    g.add((snellman.writtenIn, namespace.RDF.type, namespace.RDF.Property))
    g.add((snellman.writtenIn, namespace.SKOS.prefLabel, Literal('Place where the text was propably written', lang='en')))
    g.add((snellman.writtenIn, namespace.SKOS.prefLabel, Literal('Tekstin todennäköinen kirjoituspaikka', lang='fi')))
    g.add((snellman.writtenIn, namespace.RDFS.subPropertyOf, dc.relation))

    g.add((snellman.letterReceiver, namespace.RDF.type, namespace.RDF.Property))
    g.add((snellman.letterReceiver, namespace.SKOS.prefLabel, Literal('Kirjeen vastaanottaja', lang='fi')))
    g.add((snellman.letterReceiver, namespace.RDFS.subPropertyOf, dc.relation))

    g.add((snellman.nbf, namespace.RDF.type, namespace.RDF.Property))
    g.add((snellman.nbf, namespace.RDFS.subPropertyOf, namespace.SKOS.exactMatch))
    g.add((snellman.nbf, namespace.SKOS.prefLabel, Literal('Link to nbf resource', lang='en')))
    g.add((snellman.nbf, namespace.SKOS.prefLabel, Literal('Siltaus Kansallisbiografiaan', lang='fi')))

    g.add((snellman.wikidata, namespace.RDF.type, namespace.RDF.Property))
    g.add((snellman.wikidata, namespace.RDFS.subPropertyOf, namespace.SKOS.exactMatch))
    g.add((snellman.wikidata, namespace.SKOS.prefLabel, Literal('Link to Wikidata resource', lang='en')))
    g.add((snellman.wikidata, namespace.SKOS.prefLabel, Literal('Siltaus Wikidataan', lang='fi')))

    g.add((snellman.yso, namespace.RDF.type, namespace.RDF.Property))
    g.add((snellman.yso, namespace.RDFS.subPropertyOf, namespace.SKOS.closeMatch))
    g.add((snellman.yso, namespace.SKOS.prefLabel, Literal('Link to YSO resource', lang='en')))
    g.add((snellman.yso, namespace.SKOS.prefLabel, Literal('Siltaus YSO-ontologiaan', lang='fi')))


    #g.add((snellman.relatedPlace, namespace.RDF.type, namespace.RDF.Property))
    #g.add((snellman.relatedPlace, namespace.RDFS.subPropertyOf, dc.relation))
    #g.add((snellman.relatedPlace, namespace.SKOS.prefLabel, Literal('Dokumenttiin liittyvä paikka', lang='fi')))

    #g.add((snellman.relatedPerson, namespace.RDF.type, namespace.RDF.Property))
    #g.add((snellman.relatedPerson, namespace.RDFS.subPropertyOf, dc.relation))
    #g.add((snellman.relatedPerson, namespace.SKOS.prefLabel, Literal('Dokumenttiin liittyvä henkilö', lang='fi')))

    #g.add((snellman.relatedCorrespondence, namespace.RDF.type, namespace.RDF.Property))
    #g.add((snellman.relatedCorrespondence, namespace.RDFS.subPropertyOf, dc.relation))
    #g.add((snellman.relatedCorrespondence, namespace.SKOS.prefLabel, Literal('Dokumenttiin liittyvä kiirjeenvaihto', lang='fi')))




add_basic_schema(graph)
taxonomy.add_asiat_csv(graph)
taxonomy.add_henkilot_csv(graph)
taxonomy.add_paikat_csv(graph)
#taxonomy.add_kirjeenvaihto_csv(graph)
correspondence.add_kirjeenvaihto_csv(graph)
taxonomy.add_tyypit_csv(graph)
taxonomy.add_kirjat_csv(graph)
taxonomy.add_luvut_csv(graph)
taxonomy.add_termit_csv(graph)
documents.add_export(graph, content_graph, extra_graph)
corrections_to_places.correct_places_on_letters(graph)

graph.serialize('turtle/snellman.ttl', format='turtle')
content_graph.serialize('turtle/snellman_content.ttl', format='turtle')
extra_graph.serialize('turtle/snellman_extras.ttl', format='turtle')

#full_graph = Graph()
#full_graph.parse('turtle/snellman.ttl', format='turtle')
#full_graph.parse('turtle/snellman_content.ttl', format='turtle')
#full_graph.serialize('turtle/snellman_works_full.ttl', format='turtle')
