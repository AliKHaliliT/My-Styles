# Base Image
FROM python:3.13-slim

# Working Directory
WORKDIR /app

# System Dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    wireguard-tools \
    nftables \
    iproute2 \
    iptables \
    net-tools \
    sqlite3 \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

# Copy Project Files
COPY . .

# Make the scripts executable
RUN chmod +x /app/entrypoint.sh
RUN chmod +x /app/scripts/backup.sh
RUN dos2unix /app/entrypoint.sh /app/scripts/backup.sh

# Install Python Dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose API Port
EXPOSE 8000

# Entrypoint (production-friendly)
ENTRYPOINT ["/app/entrypoint.sh"]