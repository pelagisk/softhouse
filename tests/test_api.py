from fastapi.testclient import TestClient
from .fixtures import generate_simple_input, simple_output, assert_output_equal

from softhouse.api import app


client = TestClient(app)


def test_root(generate_simple_input, simple_output):
    response = client.get("/")
    assert response.status_code == 200
    assert_output_equal(response.json(), simple_output)