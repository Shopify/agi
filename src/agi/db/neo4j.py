from agi.config.settings import settings
from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self):
        self.driver = GraphDatabase.driver(
                settings.NEO4J_URI, auth=(settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD)
            )

    def query(self, query, parameters=None, **kwargs):
        with self.driver.session() as session:
            result = session.run(query, parameters, **kwargs)
            return [record for record in result]

    def drop_all(self):
        delete_query = "MATCH (n) DETACH DELETE n"
        self.query(delete_query)
