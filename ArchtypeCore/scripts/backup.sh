#!/bin/bash

# ---------------- Configuration ----------------
BACKUP_DIR="backup"
DB_FILE="test.db"
WG_CONFIG_FILE="/etc/wireguard/archetype0.conf"
RETENTION_DAYS=7   # How many days of backups to keep
LOG_FILE="$BACKUP_DIR/backup.log"
# ---------------- End Configuration ----------------

# Ensure backup directory exists
mkdir -p "$BACKUP_DIR"

# Create timestamp
TIMESTAMP=$(date +%F_%H-%M-%S)

# Function to log messages
log() {
    echo "[$(date '+%F %T')] $1" | tee -a "$LOG_FILE"
}

log "Starting backup process..."

# Backup SQLite database
DB_BACKUP="$BACKUP_DIR/archetype_$TIMESTAMP.db"
log "Backing up database to $DB_BACKUP..."
if sqlite3 "$DB_FILE" ".backup '$DB_BACKUP'"; then
    log "Database backup successful."
else
    log "Database backup FAILED!"
    exit 1
fi

# Backup Network Provider configuration (Example: WireGuard)
WG_BACKUP="$BACKUP_DIR/archetype0_$TIMESTAMP.conf"
if [ -f "$WG_CONFIG_FILE" ]; then
    log "Backing up network config to $WG_BACKUP..."
    cp "$WG_CONFIG_FILE" "$WG_BACKUP" && log "Network configuration backup successful."
else
    log "Network configuration file $WG_CONFIG_FILE not found. Skipping."
fi

# Remove old backups
log "Cleaning up backups older than $RETENTION_DAYS days..."
find "$BACKUP_DIR" -type f -mtime +$RETENTION_DAYS -name "*.db" -or -name "*.conf" -exec rm -f {} \;
log "Old backups cleanup complete."

log "Backup process completed successfully."
exit 0
