import os

# The settings module builds its Settings instance at import time and four values carry no
# default, so the suite supplies them before any application module loads. They are
# deliberately fake, and they are assigned rather than defaulted so that a real environment
# on the machine running the tests can never leak into a run.
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["SERVER_IP"] = "127.0.0.1"
os.environ["SERVER_PUBKEY"] = "test-only-server-public-key"
os.environ["SECRET_KEY"] = "test-only-secret-key-of-sufficient-length"
