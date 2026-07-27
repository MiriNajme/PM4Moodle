# PM4Moodle — Docker Demo

Run the whole PM4Moodle tool with **one command** — no Moodle install, no manual
database restore. A database container automatically loads the bundled test
dataset, and PM4Moodle comes pre-connected to it.

There are two levels:

| Level | What you get | Command |
|-------|--------------|---------|
| **Basic** | PM4Moodle only (extract OCEL 2.0 logs from the test dataset) | `docker compose up --build` |
| **Full** | The above **plus a live, editable Moodle** sharing the same database | see [With live Moodle](#full-demo-with-live-moodle) |

---

## Prerequisites (everyone)

Install **Docker Desktop** (free) and make sure it is running:

- Download: <https://www.docker.com/products/docker-desktop/>
- Install with the default options (on Windows, allow the "WSL2" step if prompted).
- Launch Docker Desktop once so the engine is running.

That is the only thing you need to install. Docker runs everything else.

---

## Basic demo

From the project folder:

```bash
docker compose up --build
```

The first run downloads images and imports the dataset (a few minutes). When it
settles, open:

- **PM4Moodle:** <http://localhost:8080>

Click **Run Extraction** to generate the OCEL 2.0 log and the OC-DFG diagram.
The tool is read-only against the database, so you cannot break anything.

Stop it with `Ctrl+C`, or from another terminal:

```bash
docker compose down
```

To also wipe the database and start fresh next time:

```bash
docker compose down -v
```

---

## Full demo (with live Moodle)

This adds a real Moodle you can log into and edit. Because Moodle and PM4Moodle
share the same database, you can **change a course in Moodle, re-run the
extraction in PM4Moodle, and immediately see the change** in the OCEL log.

### 1. Get the Moodle code

The test dataset was built with **Moodle 5.1dev (Build: 20250711)** and Moodle
must run that exact version, otherwise it would try to upgrade (and thereby
alter) the dataset on first boot. Choose **one** of the options below.

#### Option A — download the prepared archive (recommended)

**You do not need to install Moodle.** Download the prepared `moodle-src.tar.gz`
into `docker/moodle-dist/`, keeping the file name.

From the project root — Windows PowerShell:

```powershell
Invoke-WebRequest -Uri https://github.com/MiriNajme/PM4Moodle/releases/download/v1.0-demo/moodle-src.tar.gz -OutFile docker/moodle-dist/moodle-src.tar.gz
```

macOS / Linux:

```bash
curl -L -o docker/moodle-dist/moodle-src.tar.gz https://github.com/MiriNajme/PM4Moodle/releases/download/v1.0-demo/moodle-src.tar.gz
```

Or download it by hand from the
[releases page](https://github.com/MiriNajme/PM4Moodle/releases) and save it as
`docker/moodle-dist/moodle-src.tar.gz` (~70 MB).

That is the complete, unmodified Moodle 5.1dev source (~70 MB), so the version
matches the dataset exactly. Moodle is licensed under the GPLv3, which permits
this redistribution.

> That specific development build is no longer downloadable from moodle.org
> (dev snapshots are replaced continuously), which is why the archive is provided
> here.

#### Option B — pack it from a local Moodle install

If you already have the matching Moodle source on disk, point `MOODLE_SRC` at it
in `.env` (step 2) and pack it yourself:

```bash
powershell -ExecutionPolicy Bypass -File docker\prepare-moodle.ps1
```

On macOS/Linux:

```bash
bash docker/prepare-moodle.sh
```

This writes `docker/moodle-dist/moodle-src.tar.gz` (~10 seconds). Packing matters:
the folder holds ~29,000 files, and letting the container copy them individually
through Docker's file sharing takes **30+ minutes**, versus seconds for the
archive. Your folder is mounted **read-only** and is never modified.

> If no archive is present, the demo still works — it falls back to the slow
> file-by-file copy and warns you.

### 2. Configure `.env`

```bash
cp .env.example .env
```

`.env.example` ships with working defaults. The settings that matter:

| Variable | Purpose |
|----------|---------|
| `MOODLE_ADMIN_USER` / `MOODLE_ADMIN_PASSWORD` | Your Moodle login. Applied on container start — the dataset's original password is not published. |
| `MOODLE_SRC` | Only needed for **Option B** (path to your Moodle code folder). |
| `MOODLE_DATA_SRC` | Optional. Path to a `moodledata` folder so previously-uploaded files appear. Mounted read-only; only uploaded file contents are copied, and Moodle regenerates its own caches. Omit for empty file storage. |

### 3. Start the full stack

```bash
docker compose -f docker-compose.yml -f docker-compose.moodle.yml up --build
```

Then open:

- **Moodle:** <http://localhost:8081>  (log in with the credentials from your `.env` and edit courses)
- **PM4Moodle:** <http://localhost:8080>  (run the extraction to see your edits reflected)

Stop / reset the same way as the basic demo (`docker compose ... down`, add `-v`
to wipe all data including Moodle's).

### Try the round trip

1. In **Moodle** (<http://localhost:8081>), log in and change something — add a
   forum post, edit a choice activity, or view an activity as a student.
2. In **PM4Moodle** (<http://localhost:8080>), click **Run Extraction** again.
3. The new events appear in the freshly extracted OCEL 2.0 log.

Both applications read and write the same database, so changes show up
immediately — no export/import step.

### Notes

- **Uploaded files:** file *contents* (e.g. uploaded resources) live in Moodle's
  `moodledata` folder, not in the database. Provide it via `MOODLE_DATA_SRC` (see
  step 1) and those files appear. If you omit it, course structure and all
  activities still work and are editable — only previously-uploaded files show as
  missing links. Either way, it does not affect PM4Moodle extraction.
- **Isolation:** each person who runs this gets their own private copy, so
  editing courses never affects anyone else.

---

## Ports used

| Service | URL / Port |
|---------|------------|
| PM4Moodle frontend | http://localhost:8080 |
| PM4Moodle backend (API) | http://localhost:5000 |
| Database (MariaDB) | localhost:3307 |
| Moodle (full demo only) | http://localhost:8081 |

If a port is already in use on your machine, edit the `ports:` lines in
`docker-compose.yml` / `docker-compose.moodle.yml`.

---

## Troubleshooting

- **"port is already allocated"** — another program uses that port. Change the
  left-hand number in the relevant `ports:` mapping and re-run.
- **Backend can't connect / empty course list** — the database may still be
  importing on first start. Wait until the `db` container is healthy, then reload.
- **Start completely fresh** — `docker compose down -v` removes all containers
  and data volumes so the next `up` re-imports the dataset from scratch.
