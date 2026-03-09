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




# ORM 

Câu này nhiều người mới học **SQLAlchemy ORM** cũng thắc mắc. Thực ra dòng này không phải “viết cho đúng syntax”, mà nó tạo **một thuộc tính Python để truy cập dữ liệu liên quan**.

Ta phân tích từng phần:

```python
insights = relationship(
    "DatasetInsights",
    back_populates="dataset",
    cascade="all, delete"
)
```

---

# 1️⃣ `insights =` là gì?

Đây là **tên thuộc tính Python** mà ORM tạo ra cho object.

Ví dụ:

```python
dataset = db.query(DatasetMetadata).first()
```

bạn có thể gọi:

```python
dataset.insights
```

và ORM sẽ trả về:

```python
[
  DatasetInsights(...),
  DatasetInsights(...)
]
```

Nghĩa là:

```text
dataset.insights = list các insight thuộc dataset đó
```

Tên này **bạn tự đặt**, miễn là dễ hiểu.

Ví dụ cũng hợp lệ:

```python
dataset_insights = relationship(...)
```

hoặc

```python
analysis = relationship(...)
```

Nhưng convention thường đặt:

```text
one-to-many → plural
many-to-one → singular
```

Nên:

```text
DatasetMetadata.insights   (plural)
DatasetInsights.dataset    (singular)
```

---

# 2️⃣ `"DatasetInsights"` là gì?

```python
relationship("DatasetInsights")
```

Đây là **tên class ORM** của bảng liên kết.

SQLAlchemy sẽ hiểu:

```text
DatasetMetadata liên kết với DatasetInsights
```

Bạn viết string thay vì class trực tiếp để tránh lỗi **circular import**.

Ví dụ:

```python
relationship(DatasetInsights)  ❌ đôi khi lỗi import
relationship("DatasetInsights") ✅ safe
```

---

# 3️⃣ `back_populates="dataset"` là gì?

Đây là **liên kết 2 chiều**.

Bạn có:

### Table 1

```python
class DatasetMetadata(Base):

    insights = relationship(
        "DatasetInsights",
        back_populates="dataset"
    )
```

### Table 2

```python
class DatasetInsights(Base):

    dataset = relationship(
        "DatasetMetadata",
        back_populates="insights"
    )
```

Hai dòng này **trỏ vào nhau**.

Quan hệ:

```text
DatasetMetadata.insights
        ↕
DatasetInsights.dataset
```

---

## Ví dụ truy cập

### từ dataset → insights

```python
dataset = db.query(DatasetMetadata).first()

dataset.insights
```

---

### từ insight → dataset

```python
insight = db.query(DatasetInsights).first()

insight.dataset
```

---

# 4️⃣ `cascade="all, delete"` là gì?

Cascade nghĩa là **lan truyền hành động**.

```python
cascade="all, delete"
```

Nghĩa là nếu bạn xóa dataset:

```python
db.delete(dataset)
db.commit()
```

thì ORM sẽ **tự động xóa insights liên quan**.

Ví dụ:

```text
datasets
-------
id = 1
filename = sales.csv
```

```text
datasets_insights
-------
dataset_id = 1
summary = ...
```

Sau khi delete dataset:

```text
datasets → row removed
datasets_insights → rows removed automatically
```

---

# 5️⃣ Quan hệ thực sự nằm ở đâu?

Nhiều người nghĩ `relationship()` tạo relation trong database.

❌ Không phải.

Quan hệ database nằm ở:

```python
dataset_id = Column(
    Integer,
    ForeignKey("datasets.id")
)
```

`relationship()` chỉ giúp **ORM truy cập object dễ hơn**.

---

# 6️⃣ Mental model rất quan trọng

Hãy nhớ:

```
ForeignKey → database level relation
relationship → python object relation
```

---

## Ví dụ

Database:

```
datasets
-------
id
filename
```

```
datasets_insights
-------
id
dataset_id
summary
```

ORM:

```
dataset.insights
insight.dataset
```

---

# 7️⃣ Ví dụ trực quan

Giả sử database có:

```
Dataset
-------
id = 1
filename = sales.csv
```

```
Insights
-------
id = 1
dataset_id = 1
summary = Europe dominates sales
```

Python:

```python
dataset = db.query(DatasetMetadata).first()
```

```python
dataset.insights
```

→ ORM chạy SQL:

```sql
SELECT * 
FROM datasets_insights
WHERE dataset_id = 1
```

---

# 8️⃣ Vì sao phải viết `relationship()`?

Nếu không có:

```python
relationship()
```

bạn sẽ phải query thủ công:

```python
db.query(DatasetInsights).filter(
    DatasetInsights.dataset_id == dataset.id
)
```

ORM giúp bạn viết đơn giản:

```python
dataset.insights
```

---

# 9️⃣ Tóm tắt

```python
insights = relationship(
    "DatasetInsights",
    back_populates="dataset",
    cascade="all, delete"
)
```

ý nghĩa:

| Phần              | Ý nghĩa               |
| ----------------- | --------------------- |
| insights          | tên thuộc tính Python |
| "DatasetInsights" | bảng liên kết         |
| back_populates    | liên kết 2 chiều      |
| cascade           | delete liên quan      |

---

