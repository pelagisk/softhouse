from fastapi.testclient import TestClient
from .fixtures import *

from softhouse.api import app


def test_root(setup_api, multiline_io, setup_input_file):    
    """Tests the API with simple input data."""
    input_str, expected = multiline_io
    setup_input_file(input_str)
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert_output_equal(response.json(), expected)