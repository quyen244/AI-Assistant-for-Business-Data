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


Bạn đang viết gần đúng rồi, chỉ **thiếu phần ForeignKey và relationship ở bảng `DatasetInsights`**. Mình sẽ giải thích từng dòng để bạn hiểu **cơ chế ORM relation** thay vì chỉ nhớ syntax.

---

# 1️⃣ Bảng `DatasetMetadata`

```python
class DatasetMetadata(Base):
    __tablename__ = "datasets"
```

→ tạo table trong database:

```
datasets
```

---

## Các cột dữ liệu

```python
id = Column(Integer, primary_key=True, index=True)
```

Primary key của bảng.

Database sẽ tạo:

```
id SERIAL PRIMARY KEY
```

---

```python
filename = Column(String(255), nullable=False)
```

Tên file CSV user upload.

Ví dụ:

```
sales.csv
hospital_data.csv
```

---

```python
columns = Column(JSON, nullable=False)
```

Bạn lưu danh sách column.

Ví dụ:

```json
["Region","Country","Item Type","Sales"]
```

---

```python
statistics = Column(JSON, nullable=False)
```

Bạn lưu statistics của dataset.

Ví dụ:

```json
{
 "numeric":{
   "sales":{
     "mean":200,
     "std":40
   }
 }
}
```

---

```python
sample_data = Column(JSON, nullable=False)
```

Ví dụ:

```json
[
  {
    "Region": "Asia",
    "Country": "Vietnam",
    "Sales": 200
  }
]
```

---

```python
created_at = Column(DateTime, default=datetime.now)
```

Tự động lưu thời gian dataset được upload.

---

# 2️⃣ Relationship quan trọng nhất

```python
insights = relationship(
    "DatasetInsights",
    back_populates="dataset",
    cascade="all, delete"
)
```

Ý nghĩa:

```
DatasetMetadata 1 ---- N DatasetInsights
```

Một dataset có thể có nhiều insights.

Ví dụ:

```
Dataset: sales.csv
```

Insights:

```
1. Europe has highest revenue
2. Cosmetics dominate sales
3. Seasonal trend detected
```

---

## ORM sẽ tạo property Python

Sau khi query dataset:

```python
dataset = db.query(DatasetMetadata).first()
```

Bạn có thể gọi:

```python
dataset.insights
```

# 7️⃣ ORM magic (rất mạnh)

Bạn cũng có thể viết:

```python
dataset = DatasetMetadata(...)

insight = DatasetInsights(
    summary="Europe dominates sales",
    insights=[...]
)

dataset.insights.append(insight)

db.add(dataset)
db.commit()
```

ORM sẽ **tự động set**

```
dataset_id = dataset.id
```

---

# 8️⃣ `back_populates` hoạt động thế nào

```
DatasetMetadata.insights
          ↕

DatasetInsights.dataset
```

Ví dụ:

### từ dataset → insights

```python
dataset.insights
```

### từ insight → dataset

```python
insight.dataset
```

---

# 9️⃣ `cascade="all, delete"`

Nếu bạn xóa dataset:

```python
db.delete(dataset)
db.commit()
```

ORM sẽ **xóa luôn insights**.

Database:

```
datasets_insights rows removed
```

---

# 🔟 Mental model (quan trọng)

SQLAlchemy có **2 layer relationship**

### Database level

```
ForeignKey("datasets.id")
```

đảm bảo dữ liệu hợp lệ.

---

### Python ORM level

```
relationship()
```

để truy cập object.

---

