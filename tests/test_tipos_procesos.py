import pytest
from uuid import uuid4

@pytest.fixture(scope="module")
def auth_header():
    from app.core.security import crear_token
    token = crear_token("admin")
    return {"Authorization": f"Bearer {token}"}

def crear_tipo_proceso_test_item(client, auth_header, nombre=None, descripcion="Descripción Test"):
    if not nombre:
        nombre = f"Tipo Proceso {uuid4().hex[:6]}"
    payload = {"nombre": nombre, "descripcion": descripcion}
    response = client.post("/api/tipos_proceso/", json=payload, headers=auth_header)

    if response.status_code == 400 and "ya existe" in response.text.lower():
        lista_response = client.get("/api/tipos_proceso/", headers=auth_header)
        if lista_response.status_code == 200:
            data = lista_response.json()
            items = data.get("items", [])
            existente = next((tp for tp in items if tp["nombre"] == nombre), None)
            assert existente is not None
            return existente
        else:
            raise Exception(f"Fallo al obtener lista: {lista_response.status_code} {lista_response.text}")

    if response.status_code != 200:
        print("DEBUG:", response.status_code, response.text)

    assert response.status_code == 200
    return response.json()



def test_get_tipos_procesos(client, auth_header):
    crear_tipo_proceso_test_item(client, auth_header, "TP para Listar", "Desc Listar")
    response = client.get("/api/tipos_proceso/", headers=auth_header)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)  # Verifica que la respuesta es un diccionario
    assert "items" in data  # Confirma que la clave 'items' existe en el diccionario
    assert isinstance(data["items"], list)  # Ahora valida que 'items' es una lista

    if len(data["items"]) > 0:
        assert "nombre" in data["items"][0]

def test_get_tipo_proceso_by_id(client, auth_header):
    created_tp = crear_tipo_proceso_test_item(client, auth_header, "TP Específico", "Desc Específico")
    tipo_proceso_id = created_tp["id"]

    response = client.get(f"/api/tipos_proceso/{tipo_proceso_id}", headers=auth_header)
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "TP Específico"
    assert data["id"] == tipo_proceso_id

def test_post_tipo_proceso_valido(client, auth_header):
    nombre = f"Tipo Proceso {uuid4().hex[:6]}"
    payload = {
        "nombre": nombre
    }
    response = client.post("/api/tipos_proceso/", json=payload, headers=auth_header)
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == nombre
    assert "id" in data

def test_post_tipo_proceso_invalido_sin_nombre(client, auth_header):
    payload = {
        "descripcion": "Descripción sin nombre"
    }
    response = client.post("/api/tipos_proceso/", json=payload, headers=auth_header)
    assert response.status_code == 422

def test_update_tipo_proceso(client, auth_header):
    created_tp = crear_tipo_proceso_test_item(client, auth_header, "TP Original", "Desc Original")
    tipo_proceso_id = created_tp["id"]
    nuevo_nombre = f"TP Actualizado {uuid4().hex[:6]}"

    payload = {
        "nombre": nuevo_nombre
    }
    response = client.put(f"/api/tipos_proceso/{tipo_proceso_id}", json=payload, headers=auth_header)
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == nuevo_nombre
    assert data["id"] == tipo_proceso_id

def test_delete_tipo_proceso(client, auth_header):
    created_tp = crear_tipo_proceso_test_item(client, auth_header, "TP Para Eliminar", "Desc Eliminar")
    tipo_proceso_id = created_tp["id"]

    response = client.delete(f"/api/tipos_proceso/{tipo_proceso_id}", headers=auth_header)
    assert response.status_code == 200
    data = response.json()
    assert data.get("ok", True) or "message" in data

    get_response = client.get(f"/api/tipos_proceso/{tipo_proceso_id}", headers=auth_header)
    assert get_response.status_code == 404