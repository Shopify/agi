import pytest
from agi.extractors import semantic_extractor
from deepdiff import DeepDiff
from helper import get_vcr_cassette_filename, vcr_cassette

def test_extract_simple_concepts(request):
    input_text = "France is a county in Europe"
    with vcr_cassette.use_cassette(get_vcr_cassette_filename(request)):
        actual_response = semantic_extractor(input_text)

    expected_response = {
        'concepts': [
            'France',
            'Country',
            'Europe'
        ],
        'relationships': [
            {
                'source': 'France',
                'relationship': 'type_of',
                'target': 'Country',
                'strength': 0.9
            }, {
                'source': 'France',
                'relationship': 'part_of',
                'target': 'Europe',
                'strength': 1.0
            }
        ]
    }

    differences = DeepDiff(actual_response, expected_response, ignore_order=True)

    assert not differences, differences

def test_extract_complex_concepts(request):
    input_text = "The Seven Lively Arts was a series of seven paintings created by the Spanish surrealist painter Salvador Dalí in 1944 and, after they were lost in a fire in 1956, recreated in an updated form by Dalí in 1957. The paintings depicted the seven arts of dancing, opera, ballet, music, cinema, radio/television and theatre."
    with vcr_cassette.use_cassette(get_vcr_cassette_filename(request)):
        actual_response = semantic_extractor(input_text)
    
    expected_response = {'concepts': ['The Seven Lively Arts', 'Painting', 'Series', 'Seven', 'Salvador Dalí', 'Spanish surrealist painter', 'year: 1944', 'date: 1944-01-01', 'year: 1956', 'date: 1956-01-01', 'year: 1957', 'date: 1957-01-01', 'Fire', 'Dancing', 'Opera', 'Ballet', 'Music', 'Cinema', 'Radio/Television', 'Theatre'], 'relationships': [{'source': 'The Seven Lively Arts', 'relationship': 'type_of', 'target': 'Series', 'strength': 1.0}, {'source': 'The Seven Lively Arts', 'relationship': 'part_of', 'target': 'Painting', 'strength': 1.0}, {'source': 'Series', 'relationship': 'attribute', 'target': 'Seven', 'strength': 1.0}, {'source': 'The Seven Lively Arts', 'relationship': 'created_by', 'target': 'Salvador Dalí', 'strength': 1.0}, {'source': 'Salvador Dalí', 'relationship': 'type_of', 'target': 'Spanish surrealist painter', 'strength': 1.0}, {'source': 'The Seven Lively Arts', 'relationship': 'began', 'target': 'year: 1944', 'strength': 1.0}, {'source': 'year: 1944', 'relationship': 'connected_to', 'target': 'date: 1944-01-01', 'strength': 1.0}, {'source': 'Fire', 'relationship': 'has', 'target': 'year: 1956', 'strength': 1.0}, {'source': 'Fire', 'relationship': 'connected_to', 'target': 'date: 1956-01-01', 'strength': 1.0}, {'source': 'The Seven Lively Arts', 'relationship': 'recreated', 'target': 'year: 1957', 'strength': 1.0}, {'source': 'year: 1957', 'relationship': 'connected_to', 'target': 'date: 1957-01-01', 'strength': 1.0}, {'source': 'The Seven Lively Arts', 'relationship': 'depicts', 'target': 'Dancing', 'strength': 1.0}, {'source': 'The Seven Lively Arts', 'relationship': 'depicts', 'target': 'Opera', 'strength': 1.0}, {'source': 'The Seven Lively Arts', 'relationship': 'depicts', 'target': 'Ballet', 'strength': 1.0}, {'source': 'The Seven Lively Arts', 'relationship': 'depicts', 'target': 'Music', 'strength': 1.0}, {'source': 'The Seven Lively Arts', 'relationship': 'depicts', 'target': 'Cinema', 'strength': 1.0}, {'source': 'The Seven Lively Arts', 'relationship': 'depicts', 'target': 'Radio/Television', 'strength': 1.0}, {'source': 'The Seven Lively Arts', 'relationship': 'depicts', 'target': 'Theatre', 'strength': 1.0}]}
    differences = DeepDiff(actual_response, expected_response, ignore_order=True)

    assert not differences, differences
