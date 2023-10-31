from fastapi.testclient import TestClient
from .fixtures import *

from softhouse.api import app


def test_root(setup_api, generate_multiline_input, multiline_expected_output):    
    """Tests the API with simple input data."""
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert_output_equal(response.json(), multiline_expected_output)