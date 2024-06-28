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

    def _calculate_temporal_bais(self, start, end, event):
        start_epoch = start.timestamp()
        end_epoch = end.timestamp()
        event_epoch = event.timestamp()

        if end_epoch != start_epoch:
            relative_position = (event_epoch - start_epoch) / (end_epoch - start_epoch)
        else:
            return 0.95

        scale_min = 0.1
        scale_max = 0.95
        relative_position = max(0, min(1, relative_position))

        if relative_position > 0:
            log_scale = scale_min + (scale_max - scale_min) * math.log10(1 + 9 * relative_position)
        else:
            log_scale = scale_min

        return log_scale

    def _calculate_weighted_average_accuracy(self, weighted_averages):
        weighted_sum = 0
        total_weight = 0
        
        for weighted_average in weighted_averages:
            accuracy = weighted_average['accuracy']
            weight = weighted_average['weight']
            
            weighted_sum += accuracy * weight
            total_weight += weight
        
        if total_weight == 0:
            return 0
        return weighted_sum / total_weight

    def _calculate_weight(self, weight_map):
        weight_map = [{**entry, 'timestamp': datetime.fromisoformat(entry['timestamp'])} for entry in weight_map]
        earliest_weight = min(entry['timestamp'] for entry in weight_map)
        latest_weight = max(entry['timestamp'] for entry in weight_map)
              
        weighted_averages = []

        for entry in weight_map:
            temporal_bias_index = self._calculate_temporal_bais(earliest_weight, latest_weight, entry['timestamp'])
            trust_index = entry['trust'] ** 10
            gullibility_index = 1 - (settings.GULLIBLITY ** 1.5)
            accuracy = temporal_bias_index * trust_index * gullibility_index
            weighted_averages.append(
                {
                    "accuracy": accuracy,
                    "weight": entry['confidence']
                }
            )
            
        weighted_average = self._calculate_weighted_average_accuracy(weighted_averages)
        return weighted_average

    def upsert_relationship(self, relationship_type, target, confidence, trust):
        # this doesn't really work but yolo
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
