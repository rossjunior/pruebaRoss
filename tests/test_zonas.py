import json

def test_get_zonas(client):
    response = client.get("/zonas-deforestadas/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_zona_by_id(client):
    payload = {
        "nombre_zona": "ZonaTest",
        "tipo_proceso": "preventivo",
        "departamento": "Amazonas",
        "geom": "POLYGON((-74.1 4.5, -74.2 4.5, -74.2 4.6, -74.1 4.6, -74.1 4.5))"
    }
    create_response = client.post("/zonas-deforestadas/", json=payload)
    zona_id = create_response.json()["id"]

    response = client.get(f"/zonas-deforestadas/{zona_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["nombre_zona"] == "ZonaTest"
    assert data["tipo_proceso"] == "preventivo"
    assert data["departamento"] == "Amazonas"

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

def test_post_zona_campos_faltantes(client):
    payload = {
        "nombre_zona": "ZonaIncompleta",
        "departamento": "Amazonas",
        "geom": "POLYGON((-74.1 4.5, -74.2 4.5, -74.2 4.6, -74.1 4.6, -74.1 4.5))"
    }

    response = client.post("/zonas-deforestadas/", json=payload)
    assert response.status_code == 422  # Validation error

def test_update_zona(client):
    payload = {
        "nombre_zona": "ZonaParaActualizar",
        "tipo_proceso": "preventivo",
        "departamento": "Amazonas",
        "geom": "POLYGON((-74.1 4.5, -74.2 4.5, -74.2 4.6, -74.1 4.6, -74.1 4.5))"
    }
    create_response = client.post("/zonas-deforestadas/", json=payload)
    zona_id = create_response.json()["id"]

    update_payload = {
        "nombre_zona": "ZonaActualizada",
        "tipo_proceso": "correctivo",
        "departamento": "Amazonas",
        "geom": "POLYGON((-74.1 4.5, -74.2 4.5, -74.2 4.6, -74.1 4.6, -74.1 4.5))"
    }

    response = client.put(f"/zonas-deforestadas/{zona_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["nombre_zona"] == "ZonaActualizada"
    assert data["tipo_proceso"] == "correctivo"

def test_delete_zona(client):
    payload = {
        "nombre_zona": "ZonaParaEliminar",
        "tipo_proceso": "preventivo",
        "departamento": "Amazonas",
        "geom": "POLYGON((-74.1 4.5, -74.2 4.5, -74.2 4.6, -74.1 4.6, -74.1 4.5))"
    }
    create_response = client.post("/zonas-deforestadas/", json=payload)
    zona_id = create_response.json()["id"]

    response = client.delete(f"/zonas-deforestadas/{zona_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Zona deforestada eliminada correctamente"
