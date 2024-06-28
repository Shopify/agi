from agi.extractors import interaction_classifier, semantic_extractor
from agi.config.settings import settings
from agi.concept import Concept


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

    def interact(self, message):
        message_classification = interaction_classifier(message)
        message_semantics = semantic_extractor(message)

        if message_classification["interaction_type"] == "factual":
            print(
                f"Agent is {message_classification['confidence']} confident",
                "that this is a factual message"
            )

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
                        print(concept.relationships)
    
            # to do
            # do a look up to determine if this new infromation contridicts existing knowledge
        elif message_classification["interaction_type"] == "interrogative":
            print(
                f"Agent is {message_classification['confidence']}",
                "confident that this is an interrogative message",
                "This hasn't been implemented yet"
            )
        return message_classification, message_semantics
