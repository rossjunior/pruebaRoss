import json

def test_post_zona_valida(client):
    payload = {
        "nombre_zona": "ZonaTest",
        "tipo_proceso": "preventivo",
        "departamento": "Amazonas",
        "geom": "POLYGON((-74.1 4.5, -74.2 4.5, -74.2 4.6, -74.1 4.6, -74.1 4.5))"
    }

    response = client.post("/zonas-deforestadas/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["nombre_zona"] == "ZonaTest"

def test_post_zona_geom_invalido(client):
    payload = {
        "nombre_zona": "ZonaInvalida",
        "tipo_proceso": "preventivo",
        "departamento": "Amazonas",
        "geom": "INVALID_STRING"
    }

    response = client.post("/zonas-deforestadas/", json=payload)
    assert response.status_code == 400
    assert "Geometría inválida" in response.json()["detail"]
