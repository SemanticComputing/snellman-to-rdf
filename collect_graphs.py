from rdflib import Graph

g = Graph()
g.parse('turtle/snellman.ttl', format='turtle')
g.parse('turtle/snellman_content.ttl', format='turtle')
g.serialize('turtle/snellman_collected_works.ttl', format='turtle')