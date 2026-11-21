
VALID = {"name": "Ivan", "email": "ivan@test.com", "phone_number": "", "company": "ACME"}

def test_list_page_loads(client):
    response = client.get("/customers")
    assert response.status_code == 200

def test_post_to_customer_returns_303(client):
    response = client.post("/customers", data=VALID, follow_redirects=False)
    assert response.status_code == 303

def test_invalid_email_returns_400(client):
    bad = {**VALID, "email": "not-an-rmail"}
    response = client.post("/customers", data=bad)
    assert response.status_code == 400
    assert "error" in response.text

def test_duplicate_email_returns_400(client):
    client.post("/customers", data=VALID)
    response = client.post("/customers", data=VALID)
    assert response.status_code == 400
    assert "Email already exists" in response.text

def test_missing_customer_edit_returns_404(client):
    response = client.get("/customers/999/edit")
    assert response.status_code == 404
