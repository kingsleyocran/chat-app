from api.v1.router import __version__


def test_app_version() -> None:
    assert __version__ == "0.1.0"
