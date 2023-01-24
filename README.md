# hide-my-email

# Migration

```python
alembic revision --autogenerate -m "<message>"
```

```python
alembic upgrade head
```


# Run

```python
uvicorn src.main:app --port 8000
```