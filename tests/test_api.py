from fastapi.testclient import TestClient
from .fixtures import setup_api, generate_simple_input, simple_output, assert_output_equal

from softhouse.api import app



def test_root(setup_api, generate_simple_input, simple_output):    
    """Tests the API with simple input data."""
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert_output_equal(response.json(), simple_output)