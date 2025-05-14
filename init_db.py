from app.db.database import Base, engine
from app.models import models

Base.metadata.create_all(bind=engine)