from app.db.database import SessionLocal
from app.models.models import TipoProceso, Departamento

def seed():
    db = SessionLocal()
    for nombre in ["preventivo", "sancionatorio"]:
        if not db.query(TipoProceso).filter_by(nombre=nombre).first():
            db.add(TipoProceso(nombre=nombre))
    for nombre in ["Amazonas", "Caquetá"]:
        if not db.query(Departamento).filter_by(nombre=nombre).first():
            db.add(Departamento(nombre=nombre))
    db.commit()
    db.close()

if __name__ == "__main__":
    seed()