#!/usr/bin/env bash
# Entrypoint for the optional live-Moodle container.
#
# It never touches the tester's original Moodle folder: the code is taken either
# from a prepared tarball (fast) or from a read-only mount of the folder (slow),
# placed in a writable container volume, and a fresh config.php is generated so
# Moodle points at the demo database.
set -e

SRC=/opt/moodle-src            # read-only mount of the Moodle code folder
DIST=/opt/moodle-dist          # may contain a prepared moodle-src.tar.gz
DATA_SRC=/opt/moodledata-src   # read-only mount of moodledata (optional)
HTML=/var/www/html
DATA=/var/www/moodledata

# ---------------------------------------------------------------------------
# First run only: populate the served code directory.
#
# Copying ~29k individual files across a Windows/macOS bind mount is very slow
# (tens of minutes). Extracting one prepared tarball instead takes a couple of
# minutes, so that path is strongly preferred. Create the tarball with
# docker/prepare-moodle.ps1 (Windows) or docker/prepare-moodle.sh (macOS/Linux).
# ---------------------------------------------------------------------------
if [ ! -f "$HTML/version.php" ]; then
  if [ -f "$DIST/moodle-src.tar.gz" ]; then
    echo "[moodle-entrypoint] Extracting Moodle code from prepared tarball..."
    tar xzf "$DIST/moodle-src.tar.gz" -C "$HTML"
  elif [ -f "$SRC/version.php" ]; then
    echo "[moodle-entrypoint] WARNING: no prepared tarball found, copying the"
    echo "[moodle-entrypoint] mounted folder file-by-file. This can take 30+"
    echo "[moodle-entrypoint] minutes. Run docker/prepare-moodle.ps1 (Windows)"
    echo "[moodle-entrypoint] or docker/prepare-moodle.sh to make this fast."
    cp -a "$SRC/." "$HTML/"
  else
    echo "[moodle-entrypoint] ERROR: no Moodle source found." >&2
    echo "[moodle-entrypoint] Set MOODLE_SRC in .env to your Moodle code folder" >&2
    echo "[moodle-entrypoint] (the one containing version.php), or prepare a" >&2
    echo "[moodle-entrypoint] tarball with docker/prepare-moodle.*" >&2
    exit 1
  fi

  rm -rf "$HTML/.git"
  chown -R www-data:www-data "$HTML"
  echo "[moodle-entrypoint] Moodle code ready ($(find "$HTML" -type f | wc -l) files)."
fi

# ---------------------------------------------------------------------------
# Always regenerate config.php from environment variables so the database host
# and web address are correct for the container, regardless of what the source
# folder's own config.php contained.
# ---------------------------------------------------------------------------
cat > "$HTML/config.php" <<PHP
<?php
unset(\$CFG);
global \$CFG;
\$CFG = new stdClass();

\$CFG->dbtype    = '${MOODLE_DBTYPE:-mariadb}';
\$CFG->dblibrary = 'native';
\$CFG->dbhost    = '${MOODLE_DB_HOST:-db}';
\$CFG->dbname    = '${MOODLE_DB_NAME:-moodle}';
\$CFG->dbuser    = '${MOODLE_DB_USER:-pm4moodle}';
\$CFG->dbpass    = '${MOODLE_DB_PASS:-pm4moodle}';
\$CFG->prefix    = 'mdl_';
\$CFG->dboptions = array(
    'dbpersist'   => 0,
    'dbport'      => ${MOODLE_DB_PORT:-3306},
    'dbsocket'    => '',
    'dbcollation' => 'utf8mb4_unicode_ci',
);

\$CFG->wwwroot  = '${MOODLE_WWWROOT:-http://localhost:8081}';
\$CFG->dataroot = '$DATA';
\$CFG->admin    = 'admin';
\$CFG->directorypermissions = 02777;

require_once(__DIR__ . '/lib/setup.php');
PHP

chown www-data:www-data "$HTML/config.php"

# ---------------------------------------------------------------------------
# Moodle's data directory must exist and be writable by the web server user.
# ---------------------------------------------------------------------------
mkdir -p "$DATA"

# First run only: seed uploaded file contents (moodledata/filedir) if a source
# moodledata folder was provided. Only filedir is copied — Moodle regenerates
# its own caches, sessions and temp dirs, avoiding stale-cache problems.
if [ ! -f "$DATA/.pm4moodle_seeded" ]; then
  if [ -d "$DATA_SRC/filedir" ]; then
    echo "[moodle-entrypoint] Seeding uploaded files from provided moodledata..."
    cp -a "$DATA_SRC/filedir" "$DATA/"
  else
    echo "[moodle-entrypoint] No moodledata provided; starting with empty file storage."
  fi
  touch "$DATA/.pm4moodle_seeded"
fi

chown -R www-data:www-data "$DATA"

# ---------------------------------------------------------------------------
# Optional: set the admin password so testers can actually log in. The dataset's
# original password is unknown, so without this the demo is read-only-by-browsing.
# Set MOODLE_ADMIN_PASSWORD in .env to enable. Local demo use only.
# ---------------------------------------------------------------------------
if [ -n "${MOODLE_ADMIN_PASSWORD:-}" ]; then
  cat > /tmp/pm4moodle-set-admin-password.php <<'PHP'
<?php
define('CLI_SCRIPT', true);
require('/var/www/html/config.php');
global $DB;
$username = getenv('MOODLE_ADMIN_USER') ?: 'admin';
$password = getenv('MOODLE_ADMIN_PASSWORD');
$user = $DB->get_record('user', array('username' => $username));
if (!$user) {
    fwrite(STDERR, "[set-admin-password] user '$username' not found\n");
    exit(1);
}
update_internal_user_password($user, $password);
echo "[set-admin-password] password set for '$username'\n";
PHP
  php /tmp/pm4moodle-set-admin-password.php \
    || echo "[moodle-entrypoint] WARNING: could not set the admin password."
  rm -f /tmp/pm4moodle-set-admin-password.php
fi

echo "[moodle-entrypoint] Starting Apache. Moodle will be available at ${MOODLE_WWWROOT:-http://localhost:8081}"
exec apache2-foreground
