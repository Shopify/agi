from agi.db.neo4j import Neo4jConnection
import json
import math
from datetime import datetime
from agi.config.settings import settings

class Concept:
    def __init__(self, type, name):
        self.type = self._neo4j_safe(type)
        self.name = self._neo4j_safe(name)
        self.neo4j = Neo4jConnection()
        self.node = self._get_node()

    def _neo4j_safe(self, string):
        return string.lower().replace(' ', '_')
    
    @property
    def relationships(self):
        query = f"""
            MATCH (n:{self.type} {{name: $name}})-[r]->(m)
            RETURN r, labels(m) AS node_labels, m.name AS node_name
        """
        result = self.neo4j.query(query, parameters={'name': self.name})

        relationships = []
        if result:
            for record in result:
                relationships.append(
                    {
                        "source": {
                            "name": self.name,
                            "type": self.type
                        },
                        "type": record['r'].type,
                        "target": {
                            "type": record['node_labels'][0],
                            "name": record['node_name']
                        },
                        "weight": record['r']._properties['weight'],
                        "weight_map": record['r']._properties['weight_map']
                    }
                )
        return relationships

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

    def _calculate_weight(self, weight_map):
        return weight_map[-1]['confidence'] * weight_map[-1]['trust']

    def upsert_relationship(self, relationship_type, target, confidence, trust):
        existing_relationships_query = f"""
            MATCH (a:`{self.type}` {{name: $name_a}})-[r:`{relationship_type}`]->(b:`{target.type}` {{name: $name_b}})
            RETURN r
        """

        parameters = {
            'name_a': self.name,
            'name_b': target.name
        }

        existing_relationships = self.neo4j.query(existing_relationships_query, parameters)

        weight_map = [
            {
                'confidence': confidence,
                'trust': trust,
                'timestamp': datetime.now().isoformat()
            }
        ]

        if existing_relationships:
            weight_map = weight_map + json.loads(existing_relationships[0]['r']._properties['weight_map'])
            weight = self._calculate_weight(weight_map)
            serialized_weight_map = json.dumps(weight_map)

            # Format labels and relationship type directly in the query string using f-strings
            update_rel_query = f"""
                MATCH (a:`{self.type}` {{name: $name_a}}), (b:`{target.type}` {{name: $name_b}})
                MERGE (a)-[r:`{relationship_type}`]->(b)
                ON CREATE SET r.weight = $weight, r.weight_map = $weight_map
                ON MATCH SET r.weight = $weight, r.weight_map = $weight_map
                RETURN r
            """

            parameters = {
                'name_a': self.name,
                'name_b': target.name,
                'weight': weight,
                'weight_map': serialized_weight_map
            }

            print(update_rel_query)
            self.neo4j.query(update_rel_query, parameters)
        else:
            weight = self._calculate_weight(weight_map)
            serialized_weight_map = json.dumps(weight_map)

            create_rel_query = f"""
                MATCH (a:{self.type} {{name: $name_a}}), (b:{target.type} {{name: $name_b}})
                CREATE (a)-[r:{relationship_type} {{weight: $weight, weight_map: $weight_map}}]->(b)
                RETURN r
            """

            parameters = {
                'name_a': self.name,
                'name_b': target.name,
                'weight': weight,
                'weight_map': serialized_weight_map
            }

            self.neo4j.query(create_rel_query, parameters)

    def __str__(self):
        return f"Concept name: '{self.name}', type: '{self.type}'"
    
    def __repr__(self):
        return f"Concept(name={self.name}, type={self.type})"
