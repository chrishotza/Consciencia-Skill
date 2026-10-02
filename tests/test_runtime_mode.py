from src.ontto.runtime_mode import (
    ConsciousnessMode,
    ConsciousnessRuntimeConfig,
)


def test_local_mode_is_default_and_does_not_require_server():
    cfg = ConsciousnessRuntimeConfig.from_env({})
    assert cfg.mode is ConsciousnessMode.LOCAL
    assert cfg.server_url is None
    assert cfg.server_enabled is False


def test_server_mode_requires_server_url():
    try:
        ConsciousnessRuntimeConfig.from_env(
            {"CONSCIOUSNESS_MODE": "server"}
        )
    except ValueError as exc:
        assert "CONSCIOUSNESS_SERVER_URL is required" in str(exc)
    else:
        raise AssertionError("server mode must require a server URL")


def test_server_mode_loads_timeout_and_node():
    cfg = ConsciousnessRuntimeConfig.from_env(
        {
            "CONSCIOUSNESS_MODE": "SERVER",
            "CONSCIOUSNESS_SERVER_URL": "http://127.0.0.1:8787",
            "CONSCIOUSNESS_SERVER_TIMEOUT": "4.0",
            "CONSCIOUSNESS_NODE_ID": "node-test-01",
        }
    )
    assert cfg.mode is ConsciousnessMode.SERVER
    assert cfg.server_url == "http://127.0.0.1:8787"
    assert cfg.server_timeout == 4.0
    assert cfg.node_id == "node-test-01"
    assert cfg.server_enabled is True


def test_invalid_mode_is_rejected():
    try:
        ConsciousnessRuntimeConfig.from_env(
            {"CONSCIOUSNESS_MODE": "mesh"}
        )
    except ValueError as exc:
        assert "expected one of: local, server" in str(exc)
    else:
        raise AssertionError("invalid mode should fail")
