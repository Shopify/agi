import pytest
from agi.extractors import interaction_classifier
from helper import get_vcr_cassette_filename, vcr_cassette

def test_interaction_classifier_question(request):
    input_text = "Where is France located?"
    with vcr_cassette.use_cassette(get_vcr_cassette_filename(request)):
        actual_response = interaction_classifier(input_text)
    expected_interaction_type = 'interrogative'

    assert actual_response['interaction_type'] == expected_interaction_type
    assert actual_response['confidence'] >= 0.9

def test_interaction_classifier_fact(request):
    input_text = "France is a county in Europe"
    with vcr_cassette.use_cassette(get_vcr_cassette_filename(request)):
        actual_response = interaction_classifier(input_text)
    expected_interaction_type = 'factual'

    assert actual_response['interaction_type'] == expected_interaction_type
    assert actual_response['confidence'] >= 0.9

def test_interaction_classifier_mixed(request):
    input_text = "Paris is in France. Where is New York?"
    with vcr_cassette.use_cassette(get_vcr_cassette_filename(request)):
        actual_response = interaction_classifier(input_text)
    expected_interaction_type = 'interrogative'

    assert actual_response['interaction_type'] == expected_interaction_type
    assert actual_response['confidence'] >= 0.7