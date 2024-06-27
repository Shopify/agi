import pytest
from unittest.mock import patch
from agi.agent import Agent
from deepdiff import DeepDiff


@pytest.fixture
def interaction_classifier_response():
    return {"interaction_type": "factual", "confidence": 0.9}

@pytest.fixture
def semantic_extractor_response():
    return {
        "concepts": [
            "Monarch butterfly",
            "Butterfly",
            "Orange",
            "Black"
        ],
        "relationships": [
            {
                "source": "Monarch butterfly",
                "relationship": "type_of",
                "target": "Butterfly",
                "strength": 0.9
            }, {
                "source": "Monarch butterfly",
                "relationship": "attribute",
                "target": "Orange",
                "strength": 1.0
            }, {
                "source": "Monarch butterfly",
                "relationship": "attribute",
                "target": "Black",
                "strength": 1.0
            }
        ]
    }

@patch('agi.agent.interaction_classifier')
@patch('agi.agent.semantic_extractor')
def test_foo(mock_semantic_extractor, mock_interaction_classifier, interaction_classifier_response, semantic_extractor_response):
    agent = Agent()
    mock_interaction_classifier.return_value = interaction_classifier_response
    mock_semantic_extractor.return_value = semantic_extractor_response

    message = "Where is France located?"
    message_classification, message_semantics = agent.interact(message=message)

    differences = DeepDiff(message_classification, interaction_classifier_response, ignore_order=True)
    assert not differences, differences

    differences = DeepDiff(message_semantics, semantic_extractor_response, ignore_order=True)
    assert not differences, differences
    