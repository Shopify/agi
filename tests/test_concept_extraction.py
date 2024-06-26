import pytest
import agi.concepts
import vcr
import os

vcr_cassette = vcr.VCR(
    serializer="yaml",
    cassette_library_dir="tests/fixtures/vcr_cassettes",
    record_mode="once",
    match_on=["uri", "method"],
    filter_post_data_parameters=["client_id", "client_secret", "refresh_token"],
    filter_headers=["authorization"],
)

def _get_vcr_cassette_filename(request):
    full_path = request.fspath
    file_name = os.path.basename(full_path)
    file_name_no_ext, _ = os.path.splitext(file_name)
    return f"{ file_name_no_ext }[{ request.node.name }].yaml"


def test_extract_simple_concepts(request):
    input_text = "France is a county in Europe"
    with vcr_cassette.use_cassette(_get_vcr_cassette_filename(request)):
        response = agi.concepts.extract_concepts(input_text)
        concepts = response['concepts']

    assert "France" in concepts
    assert "Country" in concepts
    assert "Europe" in concepts

def test_extract_complex_concepts(request):
    input_text = """The Seven Lively Arts was a series of seven paintings created by the Spanish surrealist painter Salvador Dalí in 1944 and, after they were lost in a fire in 1956, recreated in an updated form by Dalí in 1957. The paintings depicted the seven arts of dancing, opera, ballet, music, cinema, radio/television and theatre."""
    with vcr_cassette.use_cassette(_get_vcr_cassette_filename(request)):
        response = agi.concepts.extract_concepts(input_text)
        concepts = response['concepts']

    assert "Seven Lively Arts" in concepts
    assert "Painting" in concepts
    assert "Spanish" in concepts
    assert "Surrealist" in concepts
    assert "Salvador Dalí" in concepts
    assert "year: 1944" in concepts
    assert "Fire" in concepts
    assert "year: 1956" in concepts
    assert "year: 1957" in concepts
    assert "Dancing" in concepts
    assert "Opera" in concepts
    assert "Ballet" in concepts
    assert "Music" in concepts
    assert "Cinema" in concepts
    assert "Radio/Television" in concepts


