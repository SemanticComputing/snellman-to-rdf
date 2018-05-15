# correcting some mistakes that happen when reading the first place from letter as place where the letter was send

from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef


# g.remove((snellman[''], namespace.RDFS.seeAlso, snellman['']))
# g.add((snellman[''], namespace.RDFS.seeAlso, snellman['']))


snellman = Namespace('http://ldf.fi/snellman/')

def correct_places_on_letters(g):
    # Karl Ludwig Michelet’lle 9.5.1843, ote kirjeestä (julkaistu Der Gedanke -lehdessä, Berliini 1861)

    g.remove((snellman['4212'], namespace.RDFS.seeAlso, snellman['13254']))


    # johanna-lovisa-snellmanille-1

    g.remove((snellman['4697'], namespace.RDFS.seeAlso, snellman['13301']))
    g.add((snellman['4697'], namespace.RDFS.seeAlso, snellman['13303']))

    # emil-stjernvall-walleenilta-16

    g.remove((snellman['5889'], namespace.RDFS.seeAlso, snellman['13242']))
    g.add((snellman['5889'], namespace.RDFS.seeAlso, snellman['13502']))


    # fredrik-kristian-nybomilta-16

    g.remove((snellman['6358'], namespace.RDFS.seeAlso, snellman['13242']))
    g.add((snellman['6358'], namespace.RDFS.seeAlso, snellman['13344']))

    # alexander-armfeltiltä-1

    g.remove((snellman['5186'], namespace.RDFS.seeAlso, snellman['13242']))
    g.add((snellman['5186'], namespace.RDFS.seeAlso, snellman['13502']))

    # alexander-armfeltilta-konsepti

    g.remove((snellman['5565'], namespace.RDFS.seeAlso, snellman['13242']))
    g.add((snellman['5565'], namespace.RDFS.seeAlso, snellman['13502']))

    # frans-johan-rabbelle

    g.remove((snellman['4654'], namespace.RDFS.seeAlso, snellman['13252']))
    g.add((snellman['4654'], namespace.RDFS.seeAlso, snellman['13241']))