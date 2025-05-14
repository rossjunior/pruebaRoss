import json

def crear_departamento_test_item(client, nombre="Departamento Test"):
    payload = {"nombre": nombre}
    response = client.post("/api/departamentos/", json=payload)
    assert response.status_code == 200 # Endpoint returns 200 on creation
    return response.json()

def test_get_departamentos(client):
    crear_departamento_test_item(client, "Departamento para Listar")
    response = client.get("/api/departamentos/")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "items" in data
    assert isinstance(data["items"], list)
    if data["total"] > 0:
        assert len(data["items"]) > 0
        assert "nombre" in data["items"][0]

def test_get_departamento_by_id(client):
    created_dept = crear_departamento_test_item(client, "Departamento Específico")
    departamento_id = created_dept["id"]

    response = client.get(f"/api/departamentos/{departamento_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Departamento Específico"
    assert data["id"] == departamento_id

def test_post_departamento_valido(client):
    payload = {
        "nombre": "Nuevo Departamento Creado"
    }
    response = client.post("/api/departamentos/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Nuevo Departamento Creado"
    assert "id" in data

def test_post_departamento_duplicado(client):
    nombre_departamento = "Departamento Duplicado Test"
    crear_departamento_test_item(client, nombre_departamento)

    payload = {"nombre": nombre_departamento}
    response = client.post("/api/departamentos/", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Departamento ya existe"


def test_post_departamento_invalido_sin_nombre(client):
    payload = {
        # Falta el campo nombre que es obligatorio
    }
    response = client.post("/api/departamentos/", json=payload)
    assert response.status_code == 422

def test_update_departamento(client):
    created_dept = crear_departamento_test_item(client, "Departamento Original Para Actualizar")
    departamento_id = created_dept["id"]

    payload = {
        "nombre": "Departamento Actualizado Correctamente"
    }
    response = client.put(f"/api/departamentos/{departamento_id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Departamento Actualizado Correctamente"
    assert data["id"] == departamento_id

def test_update_departamento_nombre_existente(client):
    dept1 = crear_departamento_test_item(client, "Nombre Unico 1")
    dept2 = crear_departamento_test_item(client, "Nombre Unico 2")

    payload = {"nombre": dept1["nombre"]}
    response = client.put(f"/api/departamentos/{dept2['id']}", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Ya existe un departamento con ese nombre"


def test_update_departamento_no_encontrado(client):
    payload = {"nombre": "No Importa"}
    response = client.put("/api/departamentos/99999", json=payload)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Departamento no encontrado"


def test_delete_departamento(client):
    created_dept = crear_departamento_test_item(client, "Departamento Para Eliminar")
    departamento_id = created_dept["id"]

    response = client.delete(f"/api/departamentos/{departamento_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True
    assert data["message"] == "Departamento eliminado correctamente"

    get_response = client.get(f"/api/departamentos/{departamento_id}")
    assert get_response.status_code == 404

def test_delete_departamento_no_encontrado(client):
    response = client.delete("/api/departamentos/99999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Departamento no encontrado"


