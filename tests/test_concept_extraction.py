import pytest
import agi.concepts

def test_extract_concepts():
    input_text = "France is a county in Europe"
    response = agi.concepts.extract_concepts(input_text)
    concepts = response['concepts']

    assert "France" in concepts
    assert "country" in concepts
    assert "Europe" in concepts
