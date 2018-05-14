# Connecting some people to their correct correspondence resource by hand
from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef

snellman = Namespace('http://ldf.fi/snellman/')
dbo = Namespace('http://dbpedia.org/ontology/')
dc = Namespace('http://purl.org/dc/elements/1.1/')

def connect(g):
    #   g.add((snellman[''], dc.relation, snellman['']))

    # Borgström, Henrik nuorempi -> Borgström, Henrik vanhempi
    g.remove((snellman['13476'], dc.relation, snellman['9392']))
    g.add((snellman['13476'], dc.relation, snellman['9393']))

    # Robert Tengström
    g.add((snellman['13289'], dc.relation, snellman['12722']))

    # Herman Kellgren
    g.add((snellman['13290'], dc.relation, snellman['10888']))

    # Johanna Lovisa Snellman
    g.add((snellman['13295'], dc.relation, snellman['12469']))
    g.add((snellman['13324'], dc.relation, snellman['12469']))

    # Essen, Anna Christina von (o. s. Snellman) / Anna Christina Snellman
    g.add((snellman['13336'], dc.relation, snellman['10024']))

    # Johan Hugo Emmerik Nervander
    g.add((snellman['13360'], dc.relation, snellman['11620']))

    # Anders Gustav Simelius
    g.add((snellman['13362'], dc.relation, snellman['12389']))

    # Wilhelm Gabriel Lagus
    g.add((snellman['13372'], dc.relation, snellman['11111']))

    # Bernhard Elis Malmström
    g.add((snellman['13400'], dc.relation, snellman['11368']))

    # Mathias Aleksander Castrén
    g.add((snellman['13413'], dc.relation, snellman['9617']))
