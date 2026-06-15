#!/bin/sh
set -e

# --- Backup ---
echo "[Backup] Running pre-migration backup..."
if sh /app/scripts/backup.sh; then
    echo "[Backup] Backup completed successfully."
else
    echo "[Backup] Backup FAILED! Aborting startup."
    exit 1
fi

# --- Network Abstraction setup (Example: WireGuard) ---
if ! ip link show archetype0 >/dev/null 2>&1; then
    echo "[Network] Setting up interface..."
    ip link add dev archetype0 type wireguard
    ip addr add 10.0.0.1/24 dev archetype0
    ip link set up dev archetype0
else
    echo "[Network] Interface already exists, skipping setup."
fi

# --- Apply Alembic migrations safely ---
echo "[Migrations] Applying database migrations..."
if alembic upgrade head; then
    echo "[Migrations] Success."
else
    echo "[Migrations] Migration failed! Rolling back to previous version..."
    PREV_REV=$(alembic current | awk '{print $1}')
    if [ -n "$PREV_REV" ]; then
        alembic downgrade "$PREV_REV"
        echo "[Migrations] Rolled back to previous revision $PREV_REV."
    else
        echo "[Migrations] Could not determine previous revision. Exiting."
        exit 1
    fi
    exit 1
fi

# --- Start FastAPI ---
echo "[Server] Starting FastAPI..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload --log-level="$(echo "$UVICORN_LOG_LEVEL" | tr '[:upper:]' '[:lower:]')"
