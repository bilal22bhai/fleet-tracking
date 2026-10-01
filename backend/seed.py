from database import Base, engine, SessionLocal
from models import Company, User, Vehicle
from security import hash_password

Base.metadata.create_all(engine)
db = SessionLocal()

if db.query(Company).first():
    print("Seed already done, skipping.")
    db.close()
    raise SystemExit(0)

company = Company(name="Demo Transport Co")
db.add(company)
db.flush()

db.add(User(company_id=company.id, email="owner@demo.com",
            password_hash=hash_password("owner123"), role="owner"))

for i in range(1, 21):
    db.add(Vehicle(company_id=company.id, device_id=f"DEV{i:03d}",
                   plate_number=f"LEA-{1000+i}", name=f"Car {i}"))

db.commit()
db.close()
print("Seed done: owner@demo.com / owner123")
