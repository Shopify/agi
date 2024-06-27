import os
import vcr


def get_vcr_cassette_filename(request):
    full_path = request.fspath
    file_name = os.path.basename(full_path)
    file_name_no_ext, _ = os.path.splitext(file_name)
    return f"{file_name_no_ext}[{request.node.name}].yaml"


vcr_cassette = vcr.VCR(
    serializer="yaml",
    cassette_library_dir="tests/fixtures/vcr_cassettes",
    record_mode=os.getenv("VCR_RECORD_MODE", "once"),
    match_on=["uri", "method"],
    filter_post_data_parameters=["client_id", "client_secret", "refresh_token"],
    filter_headers=["authorization"],
)
