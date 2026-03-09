#  PostgreSQL với SQLAlchemy

# 1. Kết nối PostgreSQL với SQLAlchemy

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:password@localhost:5432/mydb"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

session = SessionLocal()
```

---

# 2. Define Model (Table)

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
```

SQL table tương đương:

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR,
    age INTEGER
);
```

---

# 3. INSERT (Create)

```python
user = User(name="Alice", age=25)

session.add(user)
session.commit()
session.refresh(user)
```

SQL tương đương:

```sql
INSERT INTO users (name, age)
VALUES ('Alice', 25);
```

---

# 4. SELECT (Read)

## Lấy tất cả

```python
users = session.query(User).all()
```

SQL:

```sql
SELECT * FROM users;
```

---

## Lấy theo id

```python
user = session.query(User).filter(User.id == 1).first()
```

SQL:

```sql
SELECT * FROM users
WHERE id = 1
LIMIT 1;
```

---

## WHERE nhiều điều kiện

```python
users = session.query(User).filter(
    User.age > 20,
    User.name == "Alice"
).all()
```

SQL:

```sql
SELECT * FROM users
WHERE age > 20 AND name = 'Alice';
```

---

## LIKE search

```python
users = session.query(User).filter(User.name.like("%Ali%")).all()
```

SQL:

```sql
SELECT * FROM users
WHERE name LIKE '%Ali%';
```

---

# 5. UPDATE

```python
user = session.query(User).filter(User.id == 1).first()

user.age = 30

session.commit()
```

SQL:

```sql
UPDATE users
SET age = 30
WHERE id = 1;
```

---

# 6. DELETE

```python
user = session.query(User).filter(User.id == 1).first()

session.delete(user)
session.commit()
```

SQL:

```sql
DELETE FROM users
WHERE id = 1;
```

---

# 7. ORDER BY

```python
users = session.query(User).order_by(User.age.desc()).all()
```

SQL:

```sql
SELECT * FROM users
ORDER BY age DESC;
```

---

# 8. LIMIT

```python
users = session.query(User).limit(5).all()
```

SQL:

```sql
SELECT * FROM users
LIMIT 5;
```

---

# 9. COUNT

```python
from sqlalchemy import func

count = session.query(func.count(User.id)).scalar()
```

SQL:

```sql
SELECT COUNT(id) FROM users;
```

---

# 10. IN query

```python
users = session.query(User).filter(User.id.in_([1,2,3])).all()
```

SQL:

```sql
SELECT * FROM users
WHERE id IN (1,2,3);
```

---

# 11. JOIN (cơ bản)

Ví dụ:

```
users
orders
```

```python
session.query(User).join(Order).all()
```

SQL:

```sql
SELECT *
FROM users
JOIN orders ON users.id = orders.user_id;
```

---

# 12. Pattern chuẩn trong FastAPI

Thường viết:

```python
def get_users(db):
    return db.query(User).all()


def get_user(db, user_id):
    return db.query(User).filter(User.id == user_id).first()


def create_user(db, name, age):
    user = User(name=name, age=age)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
```

---

# 13. SQLAlchemy 2.0 style (modern hơn)

SQLAlchemy mới khuyên dùng:

```python
from sqlalchemy import select

stmt = select(User).where(User.age > 20)

result = session.execute(stmt)

users = result.scalars().all()
```

---

# 14. Debug xem SQL query

```python
engine = create_engine(DATABASE_URL, echo=True)
```

Terminal sẽ log:

```
SELECT users.id, users.name, users.age
FROM users
WHERE users.id = %s
```

---

💡 **Tip quan trọng cho backend**

Luồng chuẩn:

```
router -> service -> repository -> database
```

```
API
 ↓
Service
 ↓
SQLAlchemy Query
 ↓
PostgreSQL
```

---
