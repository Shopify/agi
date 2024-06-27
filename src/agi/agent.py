from agi.extractors import interaction_classifier, semantic_extractor
from agi.config.settings import settings


class Agent:
    def __init__(self, trust=settings.TRUST):
        self.trust = trust

    def interact(self, message):
        message_classification = interaction_classifier(message)
        message_semantics = semantic_extractor(message)
        print(message_semantics)

        if message_classification["interaction_type"] == "factual":
            print(
                f"""
                    Agent is {message_classification['confidence']} confident
                    that this is a factual message
                """
            )
            # look up identified concepts
            # for each concept check if it aligns with existing concept relationships
            # if trust is 1.0, update concept relationships to match new fact
            # if trust is less than 1.0, use a prompt to determine the trustworthiness of the fact
            # given the existing knowledge. Use the trustworthiness and trust level to inform the
            # confidence and if the new fact should be added
            # determine if the interaction warrents a response
        elif message_classification["interaction_type"] == "interrogative":
            print(
                f"""
                Agent is {message_classification['confidence']}
                confident that this is an interrogative message
                """
            )
            pass
            # look up identified concepts
            # Use the relationships of that concept as context for the question
            # respond to the question
        return message_classification, message_semantics
