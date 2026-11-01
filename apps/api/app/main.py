"""FastAPI application entry point."""

from fastapi import FastAPI

app = FastAPI(
    title="AI Automation Platform API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url=None,
)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    """Return process liveness without requiring external dependencies."""

    return {"status": "ok", "service": "api"}

