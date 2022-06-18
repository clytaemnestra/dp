def test_get_homepage(test_client):
    """Check valid response when the "/" page is requested."""
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"Measures" in response.data


def test_post_homepage(test_client):
    """Checks response for POST request."""
    response = test_client.post("/")
    assert response.status_code == 302
    assert b"results" in response.data


def test_get_results(test_client):
    """Check valid response when the "/results" page is requested."""
    response = test_client.get("/results")
    assert response.status_code == 200
    assert b"Results" in response.data


def test_post_results(test_client):
    """Checks if status code 405 is returned for POST request."""
    response = test_client.post("/results")
    assert response.status_code == 405


def test_get_non_existent_page(test_client):
    """Check response when non-existed page is called."""
    response = test_client.get("/non-existent-page")
    assert response.status_code == 404
    assert b'<a href="#">COVID measures</a>' in response.data
