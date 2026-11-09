# Back-End-Development-Songs

Flask/PyMongo API completed from the IBM Skills Network starter. MongoDB stores song IDs, titles and lyrics. The initial fixture is seeded only when the collection is empty; application startup does not drop existing data.

## Environment Setup
- Repository created from the provided template; original course bootstrap: bin/setup.sh.
- Verified in capstone-env (Python 3.10) in IBM Skills Network Labs.
- Install: python -m pip install -r requirements.txt
- Configure MONGODB_SERVICE=host:27017, MONGODB_USERNAME and MONGODB_PASSWORD in the environment. An optional MONGODB_URI overrides these. Never commit credentials.
- Run: flask --app backend run --host 0.0.0.0 --port 3000
- Unit checks: SONGS_TEST_MOCK=1 python -m pytest -v (mongomock test double).
- Live check: python -m pytest tests/test_api.py -v against an actual configured MongoDB.

Endpoints: GET /health (database ping), GET /count, GET/POST /song, GET/PUT/DELETE /song/<id>.
Dockerfile runs gunicorn on port 3000.
