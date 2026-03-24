from auth_database import engine, Base
from auth.models import User


print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Done.")