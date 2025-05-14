import json

def crear_tipo_proceso_test_item(client, nombre="Tipo Proceso Test", descripcion="Descripción Test"):
    payload = {"nombre": nombre, "descripcion": descripcion}
    response = client.post("/api/tipos_proceso/", json=payload)
    assert response.status_code == 200
    return response.json()

def test_get_tipos_procesos(client):
    crear_tipo_proceso_test_item(client, "TP para Listar", "Desc Listar")
    response = client.get("/api/tipos_proceso/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    if len(data) > 0:
        assert "nombre" in data[0]
        assert "descripcion" in data[0]


def test_get_tipo_proceso_by_id(client):
    created_tp = crear_tipo_proceso_test_item(client, "TP Específico", "Desc Específico")
    tipo_proceso_id = created_tp["id"]

    response = client.get(f"/api/tipos_proceso/{tipo_proceso_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "TP Específico"
    assert data["descripcion"] == "Desc Específico"
    assert data["id"] == tipo_proceso_id

def test_post_tipo_proceso_valido(client):
    payload = {
        "nombre": "Nuevo Tipo Proceso",
        "descripcion": "Descripción del nuevo tipo de proceso"
    }
    response = client.post("/api/tipos_proceso/", json=payload)
    assert response.status_code == 200 # Assuming 200 OK
    data = response.json()
    assert data["nombre"] == "Nuevo Tipo Proceso"
    assert data["descripcion"] == "Descripción del nuevo tipo de proceso"
    assert "id" in data

def test_post_tipo_proceso_invalido_sin_nombre(client):
    payload = {
        # Falta el campo nombre que es obligatorio
        "descripcion": "Descripción sin nombre"
    }
    response = client.post("/api/tipos_proceso/", json=payload)
    assert response.status_code == 422  # Validation error

def test_update_tipo_proceso(client):
    created_tp = crear_tipo_proceso_test_item(client, "TP Original", "Desc Original")
    tipo_proceso_id = created_tp["id"]

    payload = {
        "nombre": "Tipo Proceso Actualizado",
        "descripcion": "Descripción actualizada"
    }
    response = client.put(f"/api/tipos_proceso/{tipo_proceso_id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Tipo Proceso Actualizado"
    assert data["descripcion"] == "Descripción actualizada"
    assert data["id"] == tipo_proceso_id

def test_delete_tipo_proceso(client):
    created_tp = crear_tipo_proceso_test_item(client, "TP Para Eliminar", "Desc Eliminar")
    tipo_proceso_id = created_tp["id"]

    response = client.delete(f"/api/tipos_proceso/{tipo_proceso_id}")
    assert response.status_code == 200
    data = response.json()
    assert data.get("ok", True) or "message" in data

    get_response = client.get(f"/api/tipos_proceso/{tipo_proceso_id}")
    assert get_response.status_code == 404
