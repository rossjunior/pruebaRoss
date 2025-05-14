import json

from uuid import uuid4

def crear_departamento_test_item(client, auth_header, nombre=None):
    if not nombre:
        nombre = f"Departamento Test {uuid4().hex[:6]}"
    payload = {"nombre": nombre}
    response = client.post("/api/departamentos/", json=payload, headers=auth_header)

    if response.status_code == 400 and "ya existe" in response.text.lower():
        lista = client.get("/api/departamentos/", headers=auth_header).json()["items"]
        existente = next((d for d in lista if d["nombre"] == nombre), None)
        assert existente is not None
        return existente

    assert response.status_code == 200
    return response.json()

def test_get_departamentos(client, auth_header):
    crear_departamento_test_item(client, auth_header, "Departamento para Listar")
    response = client.get("/api/departamentos/", headers=auth_header)
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "items" in data
    assert isinstance(data["items"], list)
    if data["total"] > 0:
        assert len(data["items"]) > 0
        assert "nombre" in data["items"][0]

def test_get_departamento_by_id(client, auth_header):
    created_dept = crear_departamento_test_item(client, auth_header, "Departamento Específico")
    departamento_id = created_dept["id"]

    response = client.get(f"/api/departamentos/{departamento_id}", headers=auth_header)
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Departamento Específico"
    assert data["id"] == departamento_id

def test_post_departamento_valido(client, auth_header):
    nombre_unico = f"Departamento {uuid4().hex[:6]}"
    payload = {"nombre": nombre_unico}
    response = client.post("/api/departamentos/", json=payload, headers=auth_header)
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == nombre_unico

def test_post_departamento_duplicado(client, auth_header):
    nombre_departamento = "Departamento Duplicado Test"
    crear_departamento_test_item(client, auth_header, nombre_departamento)

    payload = {"nombre": nombre_departamento}
    response = client.post("/api/departamentos/", json=payload, headers=auth_header)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "400: Departamento ya existe"


def test_post_departamento_invalido_sin_nombre(client, auth_header):
    payload = {
        # Falta el campo nombre que es obligatorio
    }
    response = client.post("/api/departamentos/", json=payload, headers=auth_header)
    assert response.status_code == 422

def test_update_departamento(client, auth_header):
    from uuid import uuid4
    created_dept = crear_departamento_test_item(client, auth_header, "Departamento Original Para Actualizar")
    departamento_id = created_dept["id"]
    nuevo_nombre = f"Departamento Actualizado {uuid4().hex[:6]}"

    payload = {"nombre": nuevo_nombre}
    response = client.put(f"/api/departamentos/{departamento_id}", json=payload, headers=auth_header)
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == nuevo_nombre
    assert data["id"] == departamento_id

def test_update_departamento_nombre_existente(client, auth_header):
    dept1 = crear_departamento_test_item(client, auth_header, "Nombre Unico 1")
    dept2 = crear_departamento_test_item(client, auth_header, "Nombre Unico 2")

    payload = {"nombre": dept1["nombre"]}
    response = client.put(f"/api/departamentos/{dept2['id']}", json=payload, headers=auth_header)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "400: Ya existe un departamento con ese nombre"


def test_update_departamento_no_encontrado(client, auth_header):
    payload = {"nombre": "No Importa"}
    response = client.put("/api/departamentos/99999", json=payload, headers=auth_header)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Departamento no encontrado"


def test_delete_departamento(client, auth_header):
    created_dept = crear_departamento_test_item(client, auth_header, "Departamento Para Eliminar")
    departamento_id = created_dept["id"]

    response = client.delete(f"/api/departamentos/{departamento_id}", headers=auth_header)
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True
    assert data["message"] == "Departamento eliminado correctamente"

    get_response = client.get(f"/api/departamentos/{departamento_id}", headers=auth_header)
    assert get_response.status_code == 404

def test_delete_departamento_no_encontrado(client, auth_header):
    response = client.delete("/api/departamentos/99999", headers=auth_header)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Departamento no encontrado"


