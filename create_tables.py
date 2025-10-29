from models.base import Base, engine
from models.user import User
from models.video import Video

Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
