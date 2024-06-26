from neo4j import GraphDatabase
from agi.config.settings import settings

class Neo4jConnection:
    def __init__(self):
        self._driver = GraphDatabase.driver(
            settings.NEO4J_URI, 
            auth=(
                settings.NEO4J_USERNAME, 
                settings.NEO4J_PASSWORD
            )
        )

    def close(self):
        self._driver.close()

    def query(self, query, parameters=None, **kwargs):
        with self._driver.session() as session:
            result = session.run(query, parameters, **kwargs)
            return [record for record in result]