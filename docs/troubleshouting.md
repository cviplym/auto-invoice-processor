# Troubleshooting

## Uvicorn using wrong Python version

If `uvicorn --version` shows Python 3.8:

```bash
python -m uvicorn server.app:app --reload
```

This ensures uvicorn uses the active Python environment.
