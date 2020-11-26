from models import db
from app import app

# Create all table
db.drop_all()
db.create_all()
