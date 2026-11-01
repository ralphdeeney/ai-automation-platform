# Docker Infrastructure

## Local configuration

Copy the repository `.env.example` to `.env`, replace the placeholder password, then run from the repository root:

```powershell
docker compose --env-file .env -f infra/docker/compose.yaml up --build
```

The API is exposed on `http://localhost:8000` by default. PostgreSQL binds only to loopback. The private `backend` network prevents direct external access between service containers and the public network.

Do not use development credentials in production. Production deployment requires approval, TLS/reverse-proxy configuration, VPS-managed secrets, resource limits based on measured capacity, backups, and a tested restore procedure.

