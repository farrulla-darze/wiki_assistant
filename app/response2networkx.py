import os
import networkx as nx
import matplotlib.pyplot as plt
from neo4j import GraphDatabase
from neo4j.graph import Node, Relationship
from dotenv import load_dotenv


load_dotenv()

host = os.environ.get('NEO4J_URL')
user = os.environ.get('NEO4J_USER')
password = os.environ.get('NEO4J_PASS')

# Connect to Neo4j database
driver = GraphDatabase.driver(host, auth=(user, password))

# Query to retrieve Felipe and his relationships
query = """
MATCH (p:Person {name:"Keanu Reeves"})-[r:ACTED_IN]->(movie)
RETURN {movie: movie.title, role: r.role} AS result
"""

# Execute the query
with driver.session() as session:
    result = session.run(query, {})
    response = [r.values()[0] for r in result]

print(response)
# for record in response:
#     print(record["movie"])
def graph_from_response(data):
    # # Create a NetworkX graph
    """Constructs a networkx graph from the results of a neo4j cypher query.
    Example of use:
    >>> result = session.run(query)
    >>> G = graph_from_cypher(result.data())

    Nodes have fields 'labels' (frozenset) and 'properties' (dicts). Node IDs correspond to the neo4j graph.
    Edges have fields 'type_' (string) denoting the type of relation, and 'properties' (dict)."""

    G = nx.MultiDiGraph()
    def add_node(node):
        # Adds node id it hasn't already been added
        u = node.id
        if G.has_node(u):
            return
        G.add_node(u, labels=node._labels, properties=dict(node))

    def add_edge(relation):
        # Adds edge if it hasn't already been added.
        # Make sure the nodes at both ends are created
        for node in (relation.start_node, relation.end_node):
            add_node(node)
        # Check if edge already exists
        u = relation.start_node.id
        v = relation.end_node.id
        eid = relation.id
        if G.has_edge(u, v, key=eid):
            return
        # If not, create it
        G.add_edge(u, v, key=eid, type_=relation.type, properties=dict(relation))

    for d in data:
        for entry in d.values():
            # Parse node
            if isinstance(entry, Node):
                add_node(entry)

            # Parse link
            elif isinstance(entry, Relationship):
                add_edge(entry)
            else:
                raise TypeError("Unrecognized object")
    return G

G = graph_from_response(response)
    
# G = nx.Graph()  # or DiGraph, MultiGraph, MultiDiGraph, etc
# e = (1, 2)
# G.add_edge(1, 2)  # explicit two-node form
# G.add_edge(*e)  # single edge as tuple of two nodes
# G.add_edges_from([(1, 2)])  # add edges from iterable container

# Now, G contains the NetworkX graph with  and his relationships
# plot the graph
    

nx.draw(G, with_labels=True)
plt.show()