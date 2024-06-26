import pytest
import agi.concepts

# def test_extract_simple_concepts():
#     input_text = "France is a county in Europe"
#     response = agi.concepts.extract_concepts(input_text)
#     concepts = response['concepts']

#     assert "France" in concepts
#     assert "Country" in concepts
#     assert "Europe" in concepts

def test_extract_complex_concepts():
    input_text = "The Seven Lively Arts was a series of seven paintings created by the Spanish surrealist painter Salvador Dalí in 1944 and, after they were lost in a fire in 1956, recreated in an updated form by Dalí in 1957. The paintings depicted the seven arts of dancing, opera, ballet, music, cinema, radio/television and theatre."
    response = agi.concepts.extract_concepts(input_text)
    concepts = response['concepts']
    breakpoint()

    assert "France" in concepts
    assert "country" in concepts
    assert "Europe" in concepts
