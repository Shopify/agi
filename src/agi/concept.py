from agi.db.neo4j import Neo4jConnection

class Concept:
    def __init__(self, type, name):
        self.type = type.lower()
        self.name = name.lower()
        self.neo4j = Neo4jConnection()
        self.node = self._get_node()
    
    @property
    def relationships(self):
        query = f"""
            MATCH (n:{self.type} {{name: $name}})-[r]->()
            RETURN r
        """
        result = self.neo4j.query(query, parameters={'name': self.name})

        return [record['r'] for record in result] if result else []

    def add_relationship(self, type, target, confidence, trust):
        create_rel_query = f"""
            MATCH (a:{self.type} {{name: $source_name}}), (b:{target.type} {{name: $target_name}})
            MERGE (a)-[r:{type} {{confidence: $confidence}}]->(b)
            RETURN r
        """

        parameters = {
            'source_name': self.name,
            'target_name': target.name,
            'confidence': confidence
        }

        result = self.neo4j.query(create_rel_query, parameters=parameters)
        return result[0]['r'] if result else None

    def _get_node(self, **properties):
        merge_query = f"""
            MERGE (n:{self.type} {{name: $name}})
            ON CREATE SET n += $properties
            ON MATCH SET n += $properties
            RETURN n
        """
        properties_with_name = {"name": self.name, "properties": properties}
        result = self.neo4j.query(merge_query, parameters=properties_with_name)

        if result:
            return result[0]["n"]
        else:
            return None

    def __str__(self):
        return f"Concept name: '{self.name}', type: '{self.type}'"
    
    def __repr__(self):
        return f"Concept(name={self.name}, type={self.type})"
