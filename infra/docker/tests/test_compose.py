from pathlib import Path

import yaml


COMPOSE_PATH = Path(__file__).parents[1] / "compose.yaml"


def load_compose() -> dict:
    with COMPOSE_PATH.open(encoding="utf-8") as compose_file:
        return yaml.safe_load(compose_file)


def test_compose_defines_api_and_postgres_healthchecks() -> None:
    compose = load_compose()
    services = compose["services"]

    assert set(services) == {"api", "postgres"}
    assert services["api"]["healthcheck"]
    assert services["postgres"]["healthcheck"]
    assert services["api"]["depends_on"]["postgres"]["condition"] == "service_healthy"


def test_postgres_is_loopback_only_and_persistent() -> None:
    postgres = load_compose()["services"]["postgres"]

    assert postgres["ports"] == ["127.0.0.1:${POSTGRES_PORT:-5432}:5432"]
    assert "postgres_data:/var/lib/postgresql/data" in postgres["volumes"]


def test_services_use_internal_backend_network() -> None:
    compose = load_compose()

    assert compose["networks"]["backend"]["internal"] is True
    assert all("backend" in service["networks"] for service in compose["services"].values())

