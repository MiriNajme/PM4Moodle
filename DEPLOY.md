# PM4Moodle — server deployment

Deployment notes for hosting PM4Moodle and the demo Moodle on one public
hostname. For running the demo locally on a laptop, see `DOCKER_DEMO.md`
instead — that setup is unchanged.

Everything is served from a single container port, under two paths:

| Path | Service |
|------|---------|
| `/pm4moodle` | PM4Moodle UI (its API lives under `/pm4moodle/api`) |
| `/moodle` | the live Moodle sharing the same database |
| `/` | redirects to `/pm4moodle/` |

All path routing happens inside the stack, in an nginx container defined in
`docker-compose.prod.yml`. **The outer, TLS-terminating proxy needs no path
rewriting** — it forwards everything, unchanged, to one port.

## 1. Prerequisites

- Docker Engine with the Compose plugin
- Roughly 4 vCPU, 8 GB RAM, 40 GB disk. The CPU matters: one extraction spends
  about a minute rendering the OC-DFG diagram with graphviz.

## 2. Get the code and the Moodle archive

```bash
git clone https://github.com/MiriNajme/PM4Moodle.git
cd PM4Moodle
curl -L -o docker/moodle-dist/moodle-src.tar.gz \
  https://github.com/MiriNajme/PM4Moodle/releases/download/v1.0-demo/moodle-src.tar.gz
```

The ~70 MB archive is Moodle 5.1dev (Build: 20250711), the exact version the
test dataset was created with. It is gitignored, so it is not in the clone, and
a different Moodle version would try to upgrade — and thereby alter — the
dataset on first boot.

## 3. Configure

```bash
cp .env.prod.example .env.prod
```

Then edit `.env.prod` and replace every `CHANGE_ME`. `PUBLIC_BASE_URL` must be
the address testers will use, with no trailing slash:

```
PUBLIC_BASE_URL=https://pm4moodle.dsv.su.se
PUBLIC_PORT=8080
DB_ROOT_PASSWORD=...
DB_PASSWORD=...
MOODLE_ADMIN_USER=admin
MOODLE_ADMIN_PASSWORD=...
```

The Moodle admin password is applied to the `admin` account on every container
start. The dataset's own admin password is unknown, so this is the only way in.
Please do not keep the value from `.env.example` — that one is public in the
repository.

## 4. Start

```bash
docker compose -f docker-compose.prod.yml --env-file .env.prod up -d --build
```

The first run takes about 5 minutes: it pulls the base images, builds the
backend and frontend, imports the test dataset, and unpacks Moodle. Check
progress with `docker compose -f docker-compose.prod.yml logs -f` and wait
until `pm4moodle-prod-db` reports `healthy`.

## 5. Front it with the outer proxy

The stack publishes `127.0.0.1:8080`. Forward everything to it, preserving the
original path and Host, and declaring the terminated scheme. For nginx:

```nginx
location / {
    proxy_pass http://127.0.0.1:8080;
    proxy_set_header Host              $host;
    proxy_set_header X-Real-IP         $remote_addr;
    proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;

    # An extraction takes about a minute, occasionally two.
    proxy_read_timeout 600s;
    proxy_send_timeout 600s;
}
```

For Apache:

```apache
ProxyPreserveHost On
RequestHeader set X-Forwarded-Proto "https"
ProxyPass        / http://127.0.0.1:8080/ timeout=600
ProxyPassReverse / http://127.0.0.1:8080/
```

Two details in those snippets carry more weight than they look:

- **No `rewrite` or path manipulation.** `/pm4moodle` and `/moodle` must arrive
  at the stack exactly as the browser sent them.
- **The original `Host` must be preserved** (`proxy_set_header Host $host` /
  `ProxyPreserveHost On`). Moodle compares the request's host against its
  configured `wwwroot` and redirects to `wwwroot` when they differ, so a proxy
  that replaces `Host` with `127.0.0.1:8080` puts Moodle in an endless redirect
  loop. See Troubleshooting below.

If access should be restricted to invited testers, HTTP basic authentication on
this outer proxy is the simplest place to add it.

## 6. Verify

- `https://<host>/` redirects to `/pm4moodle/`
- the tool loads, the course list is populated (that proves the database
  connection), and **Run Extraction** returns two download cards after about a
  minute
- both download links open — this is what proves the proxy headers are right;
  if they point at `http://` or at a path without `/pm4moodle`, the
  `X-Forwarded-Proto` / `X-Forwarded-Prefix` headers are not reaching Flask
- `https://<host>/moodle/` shows the Moodle login and the admin password works
- editing a course in Moodle and re-running the extraction shows the new events

## Troubleshooting

**`/moodle` redirects to itself forever, and/or `/` sends the browser to
`localhost:8080`**

Both mean the outer proxy is not passing the original `Host` header through, so
the stack sees `Host: localhost:8080` (or `127.0.0.1:8080`) instead of the real
hostname. Confirm it from the server:

```bash
curl -sI -H 'Host: pm4moodle.dsv.su.se' http://127.0.0.1:8080/
```

Sent with the correct `Host`, that returns `302` with `Location: /pm4moodle/`
and `/moodle/` loads normally. If the site misbehaves only when reached through
the outer proxy, the header is being lost there — add `proxy_set_header Host
$host;` (nginx) or `ProxyPreserveHost On` (Apache).

If preserving `Host` is not possible in your setup, set
`MOODLE_REVERSEPROXY=true` in `.env.prod` and recreate the Moodle container.
Moodle then trusts `wwwroot` rather than comparing it with the incoming request:

```bash
docker compose -f docker-compose.prod.yml --env-file .env.prod up -d moodle
```

**The download links after an extraction point at `http://` or omit
`/pm4moodle`**

`X-Forwarded-Proto` or `X-Forwarded-Prefix` is not reaching Flask. The internal
proxy sets `X-Forwarded-Prefix` itself, so this is normally the outer proxy
dropping `X-Forwarded-Proto`.

**Moodle shows "Incorrect access detected"**

The same `Host` mismatch as above, on a Moodle version that reports it rather
than redirecting. The same two fixes apply.

## What differs from the local demo

`docker-compose.prod.yml` is standalone — it does not layer on
`docker-compose.yml` — and differs from the laptop setup in four ways:

1. **No published database port.** MariaDB is reachable only from the other
   containers. The local demo publishes 3307 for inspection with a SQL client.
2. **All passwords come from `.env.prod`** rather than being hardcoded.
3. **The frontend is built for a subpath**: `VITE_BASE_PATH=/pm4moodle/` and a
   relative `VITE_API_BASE_URL=/pm4moodle/api`, so no CORS is involved.
4. **Moodle is installed in a subdirectory** (`MOODLE_SUBDIR=/moodle`) with
   `sslproxy` enabled, so the path the browser requests matches `$CFG->wwwroot`
   and Moodle does not redirect-loop behind TLS termination.

## Maintenance

Restart after a reboot is automatic (`restart: unless-stopped`).

The test dataset is imported **only when the database volume is created**. To
reload it after changing `test_dataset/backup.sql`:

```bash
docker compose -f docker-compose.prod.yml --env-file .env.prod down -v
docker compose -f docker-compose.prod.yml --env-file .env.prod up -d --build
```

`down -v` also wipes everything testers have done in Moodle, which is the
intended way to reset the demo to a clean state.

To remove the demo entirely, `down -v` and delete the clone.
