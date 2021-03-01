import rdflib

def ontology_queries(file, query):
    g=rdflib.Graph()
    g.parse(file, format="nt")
    result=g.query(query)
    return list(result)

print("--------------query 1:----------------")
query1="select ?p ?t \
            where{ ?p <http://example.org/birthPlace> ?c . \
                    ?c <http://example.org/locatedIn> <http://example.org/Brazil> .\
                     ?p <http://example.org/playsFor> ?t.}" 
res=ontology_queries("ontology.nt",query1)
for item in res:
    print("player: " + str(item[0]) +", team: " + str(item[1]))

print("--------------query 2:----------------")
query2="select ?p ?t \
            where{?p <http://example.org/birthDate> ?d . \
                    filter (?d>='1996-01-01'^^xsd:date). \
                    ?p <http://example.org/playsFor> ?t}" 
res=ontology_queries("ontology.nt",query2)
for item in res:
    print("player: " + str(item[0]) +", team: " + str(item[1]))

print("--------------query 3:----------------")
query3="select ?p \
            where{?p <http://example.org/birthPlace> ?c1 . \
                   ?p <http://example.org/playsFor> ?t. \
                    ?t <http://example.org/homeCity> ?c2 . \
                    filter ( ?c1=?c2)}" 
res=ontology_queries("ontology.nt",query3)
for item in res:
    print("player: " + str(item[0]))
    
print("--------------query 4:----------------")
query4="select ?t1 ?t2 \
            where{?t1 <http://example.org/homeCity> ?c1 . \
                   ?t2 <http://example.org/homeCity> ?c2. \
                    filter ( ?c1=?c2 && ?t1!=?t2)}" 
res=ontology_queries("ontology.nt",query4)
for item in res:
    print("team1: " + str(item[0]) +", team2: " + str(item[1]))
