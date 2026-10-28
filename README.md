# FastAPI with DB

API inicial em FastAPI.

## Preparar o ambiente

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Executar em desenvolvimento

```bash
uvicorn main:app --reload
```

A API fica disponível em <http://127.0.0.1:8000>. A documentação interativa
fica em <http://127.0.0.1:8000/docs>, e o endpoint de verificação em
<http://127.0.0.1:8000/health>.