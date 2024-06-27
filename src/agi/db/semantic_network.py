from agi.config.settings import settings
from py2neo import Graph, Node, Relationship, NodeMatcher
from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self):
        self._driver = None

    @property
    def driver(self):
        if self._driver is None:
            self._driver = GraphDatabase.driver(
                settings.NEO4J_URI, auth=(settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD)
            )
        return self._driver

    def query(self, query, parameters=None, **kwargs):
        with self._driver.session() as session:
            result = session.run(query, parameters, **kwargs)
            return [record for record in result]


class SemanticNetwork:
    def __init__(self):
        self._graph = None
        
    @property
    def graph(self):
        if self._graph is None:
            self._graph = Graph(settings.NEO4J_URI, auth=(settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD))
        return self._graph

    def run(self, query):
        return self.graph.run(query)

class Concept:
    def __init__(self, type, name):
        self.type = type.lower()
        self.name = name.lower()
        self.neo4j = Neo4jConnection()
        self.semantic_network = SemanticNetwork()
        self.graph = self.semantic_network.graph
        self.node = self._get_node()
    
    @property
    def relationships(self):
        return [rel for rel in self.graph.relationships.match(nodes=(self.node,))]

    def add_relationship(self, type, target, confidence):
        relationship = Relationship(self.node, type, target.node, confidence=confidence)
        self.graph.create(relationship)

    def _get_node(self, **properties):
        concept_node = Node(self.type, name=self.name, **properties)
        
        merged_node = self.graph.nodes.match(self.type, name=self.name).first()
        if not merged_node:
            self.graph.create(concept_node)
            merged_node = concept_node
        else:
            merged_node.update(**properties)
            self.graph.push(merged_node)
        
        return merged_node


    def __str__(self):
        return f"Concept name: '{self.name}', type: '{self.type}'"
    
    def __repr__(self):
        return f"Concept(name={self.name}, type={self.type})"
