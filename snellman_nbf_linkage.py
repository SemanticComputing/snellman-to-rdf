from rdflib import Graph, Literal, namespace, Namespace, XSD, URIRef

snellman = Namespace('http://ldf.fi/snellman/')

def create_single_links(s_g, w_g):
    q = s_g.query('''
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            PREFIX snell: <http://ldf.fi/snellman/>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            
            select distinct ?person
            
            where {
              ?person a foaf:Person .
              ?person snell:nbf ?link .
            }
            ''')
    for row in q:
        singles(row[0], s_g, w_g)

def singles(person, s_g, w_g):
        q = s_g.query('''
                PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                PREFIX snell: <http://ldf.fi/snellman/>
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>

                select distinct ?link

                where {
                  ?person snell:nbf ?link .
                }
                ''', initBindings={'person': person})
        for row in q:
            w_g.add((URIRef(person), namespace.SKOS.exactMatch, URIRef(row[0])))
            return w_g


source_graph =  Graph()
source_graph.parse ('turtle/snellman.ttl', format='turtle')
write_graph = Graph()

create_single_links(source_graph, write_graph)

write_graph.serialize('graphs/snell_to_nbf.ttl', format='turtle')