#!/bin/sh
set -e

# Generate the backend config from environment variables so the demo works with
# zero manual setup: PM4Moodle is pointed at the bundled database container that
# already has the test dataset loaded. Overriding via the connection dialog in
# the UI still works — this just provides sensible, ready-to-run defaults.
CONFIG_PATH="/app/logic/config.cfg"

cat > "$CONFIG_PATH" <<EOF
[database]
host = ${DB_HOST:-db}
port = ${DB_PORT:-3306}
user = ${DB_USER:-pm4moodle}
password = ${DB_PASSWORD:-pm4moodle}
db_name = ${DB_NAME:-moodle}

[output]
file_path = output
file_name_prefix = ocel2
EOF

echo "[entrypoint] Backend config written to $CONFIG_PATH"

exec flask run --host=0.0.0.0 --port=5000
