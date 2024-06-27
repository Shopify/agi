from agi.db.neo4j import Neo4jConnection
import json
import math
from datetime import datetime
from agi.config.settings import settings

class Concept:
    def __init__(self, type, name):
        self.type = type.lower()
        self.name = name.lower()
        self.neo4j = Neo4jConnection()
        self.node = self._get_node()
    
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

    def _calculate_weight(self, weight_map):
        # fix this, my brain isn't working
        weight_map = [{**entry, 'timestamp': datetime.fromisoformat(entry['timestamp'])} for entry in weight_map]
        most_recent_date = max(entry['timestamp'] for entry in weight_map)
        
        weighted_sum = 0
        total_weight = 0
        decay_factor = 0.1

        for entry in weight_map:
            days_diff = (most_recent_date - entry['timestamp']).total_days()
            time_weight = math.exp(-decay_factor * days_diff)
            effective_trust = (1 - settings.GULLIBLITY) * (entry['trust'] ** 3) * time_weight
            
            combined_weight = entry['confidence'] * (1 - effective_trust) + effective_trust * entry['confidence']
            weighted_value = combined_weight * time_weight
            weighted_sum += weighted_value
            total_weight += time_weight

        if total_weight == 0:
            return 0
        return round(weighted_sum / total_weight, 3)

    def upsert_relationship(self, relationship_type, target, confidence, trust):
        existing_relationships_query = f"""
            MATCH (a:{self.type} {{name: '{self.name}'}})-[r:{relationship_type}]->(b:{target.type} {{name: '{target.name}'}})
            RETURN r
        """
        existing_relationships = self.neo4j.query(existing_relationships_query)

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
            update_rel_query = f"""
                MATCH (a:{self.type} {{name: '{self.name}'}}), (b:{target.type} {{name: '{target.name}'}})
                MERGE (a)-[r:{relationship_type}]->(b)
                ON CREATE SET r.weight = {weight}, r.weight_map = '{serialized_weight_map}'
                ON MATCH SET r.weight = {weight}, r.weight_map = '{serialized_weight_map}'
                RETURN r
            """
            self.neo4j.query(update_rel_query)
        else:
            weight = self._calculate_weight(weight_map)
            serialized_weight_map = json.dumps(weight_map)
            
            create_rel_query = f"""
                MATCH (a:{self.type} {{name: '{self.name}'}}), (b:{target.type} {{name: '{target.name}'}})
                CREATE (a)-[r:{relationship_type} {{weight: {weight}, weight_map: '{serialized_weight_map}'}}]->(b)
                RETURN r
            """
            self.neo4j.query(create_rel_query)

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
