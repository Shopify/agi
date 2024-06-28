from agi.extractors import interaction_classifier, semantic_extractor, answer_question_with_context, identify_missing_context
from agi.config.settings import settings
from agi.concept import Concept
from agi.extractors import load_template

class Agent:
    def __init__(
            self,
            trust=settings.TRUST,
            gullibilty=settings.GULLIBLITY,
            creativity=settings.GULLIBLITY,
            susceptibility=settings.GULLIBLITY,
        ):
        self.trust = trust
        self.gullibilty = gullibilty
        self.creativity = creativity
        self.susceptibility = susceptibility

    def _process_factual_interaction(self, message_semantics):
        # update this function so that it checks the incoming information with existing knowledge
        for concept_dict in message_semantics['concepts']:
            concept = Concept(concept_dict['type'], concept_dict['name'])
            for relationship in message_semantics['relationships']:
                if concept_dict == relationship['source']:
                    target = Concept(relationship['target']['type'], relationship['target']['name'])
                    concept.upsert_relationship(
                        relationship_type=relationship['type'],
                        target=target,
                        confidence=relationship['confidence'],
                        trust=1
                    )
    
    def _process_interrogative_interaction(self, question, message_semantics):
        concept_map = []
        for concept_dict in message_semantics['concepts']:
            concept = Concept(concept_dict['type'], concept_dict['name'])
            relationships = []
            for relationship in concept.relationships:
                if relationship['weight'] > 0.3:
                    relationships.append({
                        "concept_name": relationship['target']['name'],
                        "concept_type": relationship['target']['type'],
                        "relationship_type": relationship['type'],
                        "relationship_weight": relationship['weight']
                    })
            ordered_relationships = sorted(relationships, key=lambda x: x['relationship_weight'], reverse=True)
            concept_map.append({
                "concept_name": concept.name,
                "concept_type": concept.type,
                "related_concepts": ordered_relationships
            })

        # Add loop here to go deeper when there isn't enough context
        question_response = answer_question_with_context(question, concept_map)
        if question_response['answerable'] and question_response['confidence'] > 0.8:
            return question_response['answer']

        missing_context_response = identify_missing_context(question, concept_map)
        template = load_template("response_for_unanswerable_questions")
        response = template.render(
            suggested_wikipedia_articles=missing_context_response['suggested_wikipedia_articles']
        )
        return response

    def interact(self, message):
        message_classification = interaction_classifier(message)
        message_semantics = semantic_extractor(message)

        if message_classification["interaction_type"] == "factual":
            self._process_factual_interaction(message_semantics)
        elif message_classification["interaction_type"] == "interrogative":
            return self._process_interrogative_interaction(message, message_semantics)
