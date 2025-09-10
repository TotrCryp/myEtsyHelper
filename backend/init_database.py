from database import Base, engine
import models  # імпортуємо щоб зареєструвати всі моделі

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
