# Connecting some people to their correct correspondence resource by hand
from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef

snellman = Namespace('http://ldf.fi/snellman/')
dbo = Namespace('http://dbpedia.org/ontology/')
dc = Namespace('http://purl.org/dc/elements/1.1/')

def connect(g):
    #   g.add((snellman[''], snellman.correspondent, snellman['']))

    # Anton von Schiefner
    g.add((snellman['13550'], snellman.correspondent, snellman['12257']))

    # Borgström, Henrik nuorempi -> Borgström, Henrik vanhempi
    g.remove((snellman['13476'], snellman.correspondent, snellman['9392']))
    g.add((snellman['13476'], snellman.correspondent, snellman['9393']))

    # Robert Tengström
    g.add((snellman['13289'], snellman.correspondent, snellman['12722']))

    # Herman Kellgren
    g.add((snellman['13290'], snellman.correspondent, snellman['10888']))

    # Johanna Lovisa Snellman
    g.add((snellman['13295'], snellman.correspondent, snellman['12469']))
    g.add((snellman['13324'], snellman.correspondent, snellman['12469']))

    # Essen, Anna Christina von (o. s. Snellman) / Anna Christina Snellman
    g.add((snellman['13336'], snellman.correspondent, snellman['10024']))

    # Johan Hugo Emmerik Nervander
    g.add((snellman['13360'], snellman.correspondent, snellman['11620']))

    # Anders Gustav Simelius
    g.add((snellman['13362'], snellman.correspondent, snellman['12389']))

    # Wilhelm Gabriel Lagus
    g.add((snellman['13372'], snellman.correspondent, snellman['11111']))

    # Bernhard Elis Malmström
    g.add((snellman['13400'], snellman.correspondent, snellman['11368']))

    # Mathias Aleksander Castrén
    g.add((snellman['13413'], snellman.correspondent, snellman['9617']))

    # Carl Robert Ehrström
    g.add((snellman['13268'], snellman.correspondent, snellman['9934']))
