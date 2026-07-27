# PM4Moodle — Docker Demo

Run the whole PM4Moodle tool with **one command** — no Moodle install, no manual
database restore. A database container automatically loads the bundled test
dataset, and PM4Moodle comes pre-connected to it.

There are two levels — start with the basic one:

| Level | What you get | Extra setup |
|-------|--------------|-------------|
| **Basic** | PM4Moodle only: extract OCEL 2.0 logs from the bundled test dataset | none |
| **Full** | The above **plus a live, editable Moodle** sharing the same database, so you can change a course and see it appear in a new extraction | one 70 MB download |

**Contents**

1. [Install Docker Desktop](#step-1--install-docker-desktop)
2. [Get the project](#step-2--get-the-project)
3. [Basic demo](#basic-demo)
4. [Full demo (with live Moodle)](#full-demo-with-live-moodle)
5. [Ports used](#ports-used)
6. [Troubleshooting](#troubleshooting)

---

## Step 1 — Install Docker Desktop

Docker Desktop is free and is the **only** thing you need to install. It runs
everything else (database, backend, frontend, and optionally Moodle).

1. Download it: <https://www.docker.com/products/docker-desktop/>
   - On **Windows**, pick the **AMD64** build unless you have an ARM device
     (Intel and AMD processors are both "AMD64").
2. Install with the default options.
3. Launch Docker Desktop and wait until it reports **"Engine running"**
   (bottom-left, or hover the whale icon in the system tray). The first launch
   takes a minute or two.

You do **not** need to create a Docker account — if a sign-in screen appears,
skip it.

> **Windows: if Docker warns that WSL2 is missing**
>
> Docker needs WSL2 (a lightweight Linux layer built into Windows). If you see
> that warning, open **PowerShell as Administrator** and run:
>
> ```powershell
> wsl --install
> ```
>
> Let it finish, then restart your computer if prompted and open Docker Desktop
> again. If Ubuntu asks you to create a username/password you may either fill it
> in or just close the window — Docker does not need that account.

## Step 2 — Get the project

```bash
git clone https://github.com/MiriNajme/PM4Moodle.git
cd PM4Moodle
```

No `git`? Download the ZIP from the
[repository page](https://github.com/MiriNajme/PM4Moodle) (**Code → Download
ZIP**), unpack it, and open a terminal in the unpacked folder.

**Run every command below from this project folder.**

---

## Basic demo

```bash
docker compose up --build
```

⏳ **The first run takes about 5–10 minutes** — it downloads the base images,
builds the backend and frontend, and imports the test dataset. Later starts take
only seconds.

The terminal keeps printing log messages and stays busy — that is normal, leave
it running. Once you see lines mentioning `pm4moodle-frontend` and
`pm4moodle-backend` having *started*, the demo is up.

> Prefer a free terminal? Add `-d` to run it in the background:
> `docker compose up --build -d`

Then open:

- **PM4Moodle:** <http://localhost:8080>

Click **Run Extraction**.

⏳ **Extraction takes about 40–50 seconds** — most of that is rendering the
OC-DFG diagram, so the page will look busy for a while. That is normal, not a
freeze.

When it finishes you should see download cards for:

- the **OCEL 2.0 log** (JSON, ~2 MB)
- the **OC-DFG** diagram (PNG)

and the **Verification Matrix** and **State Chart** tabs become usable.

PM4Moodle only *reads* the database, so you cannot break anything here.

### Stopping and resetting

Stop it with `Ctrl+C`, or from another terminal:

```bash
docker compose down
```

To also wipe the database and start completely fresh next time:

```bash
docker compose down -v
```

---

## Full demo (with live Moodle)

This adds a real Moodle you can log into and edit. Because Moodle and PM4Moodle
share the same database, you can **change a course in Moodle, re-run the
extraction in PM4Moodle, and immediately see the change** in the OCEL log.

### Step A — Get the Moodle code

The test dataset was built with **Moodle 5.1dev (Build: 20250711)** and Moodle
must run that exact version, otherwise it would try to upgrade (and thereby
alter) the dataset on first boot. Choose **one** of the options below.

#### Option A — download the prepared archive (recommended)

**You do not need to install Moodle.** Download the prepared `moodle-src.tar.gz`
into `docker/moodle-dist/`, keeping the file name.

From the project folder — **Windows PowerShell**:

```powershell
Invoke-WebRequest -Uri https://github.com/MiriNajme/PM4Moodle/releases/download/v1.0-demo/moodle-src.tar.gz -OutFile docker/moodle-dist/moodle-src.tar.gz
```

**macOS / Linux**:

```bash
curl -L -o docker/moodle-dist/moodle-src.tar.gz https://github.com/MiriNajme/PM4Moodle/releases/download/v1.0-demo/moodle-src.tar.gz
```

⏳ It is ~70 MB and can take a few minutes.

Or download it by hand from the
[releases page](https://github.com/MiriNajme/PM4Moodle/releases) and save it as
`docker/moodle-dist/moodle-src.tar.gz`.

Check it arrived in the right place — the file must be exactly here:

```
PM4Moodle/docker/moodle-dist/moodle-src.tar.gz
```

That is the complete, unmodified Moodle 5.1dev source (~70 MB), so the version
matches the dataset exactly. Moodle is licensed under the GPLv3, which permits
this redistribution.

> That specific development build is no longer downloadable from moodle.org
> (dev snapshots are replaced continuously), which is why the archive is provided
> here.

#### Option B — pack it from a local Moodle install

*Skip this if you used Option A.*

If you already have the matching Moodle source on disk, point `MOODLE_SRC` at it
in `.env` (Step B below) and pack it yourself:

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

### Step B — Create your `.env`

Copy the example file:

```bash
cp .env.example .env
```

On **Windows Command Prompt** use `copy .env.example .env` instead
(PowerShell accepts `cp`).

`.env.example` ships with working defaults, so **for Option A you do not need to
edit anything**. The settings it contains:

| Variable | Purpose |
|----------|---------|
| `MOODLE_ADMIN_USER` / `MOODLE_ADMIN_PASSWORD` | Your Moodle login, applied when the container starts. Defaults to `admin` / `Pm4Moodle!Demo1`. The dataset's original password is not published, which is why this is set here. |
| `MOODLE_SRC` | Only for **Option B** — path to your Moodle code folder. Commented out by default. |
| `MOODLE_DATA_SRC` | Optional. Path to a `moodledata` folder so previously-uploaded files appear. Mounted read-only; only uploaded file contents are copied, and Moodle regenerates its own caches. Commented out by default. |

### Step C — Start the full stack

```bash
docker compose -f docker-compose.yml -f docker-compose.moodle.yml up --build
```

⏳ First run: about **5–10 minutes** (or seconds if you already ran the basic
demo, since the images are reused).

Then open:

| | |
|---|---|
| **Moodle** | <http://localhost:8081> — log in with `admin` / `Pm4Moodle!Demo1` (or whatever you set in `.env`) |
| **PM4Moodle** | <http://localhost:8080> — run the extraction to see your edits |

Stop / reset the same way as the basic demo, but pass both files:

```bash
docker compose -f docker-compose.yml -f docker-compose.moodle.yml down
```

Add `-v` to wipe all data, including Moodle's.

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

**Docker Desktop won't start / "WSL2 is not installed" (Windows)**
Open PowerShell **as Administrator**, run `wsl --install`, restart if prompted,
then open Docker Desktop again.

**"docker: command not found" / "not recognized"**
Docker Desktop is not running, or your terminal was open before you installed it.
Start Docker Desktop, wait for "Engine running", then open a **new** terminal.

**"port is already allocated"**
Another program is using that port. Either stop it, or change the left-hand
number in the relevant `ports:` mapping in `docker-compose.yml` /
`docker-compose.moodle.yml` and re-run.

**The page at localhost:8080 doesn't load**
The containers may still be building or starting. Check with:

```bash
docker compose ps
```

Wait until `pm4moodle-db` shows `healthy` and the other containers show
`running`.

**Empty course list, or extraction errors**
The database may still be importing on first start. Wait until `pm4moodle-db` is
`healthy`, then reload the page.

**Extraction seems stuck**
It normally takes 40–50 seconds, most of it rendering the OC-DFG. Give it a
minute before assuming a problem. To watch what the backend is doing:

```bash
docker compose logs -f backend
```

**Moodle shows "403 Forbidden" or an error page**
Make sure `moodle-src.tar.gz` is at `docker/moodle-dist/moodle-src.tar.gz`, then
recreate the Moodle container:

```bash
docker compose -f docker-compose.yml -f docker-compose.moodle.yml up -d --force-recreate moodle
```

**Moodle start is extremely slow (many minutes)**
That happens when no archive was found and it fell back to copying ~29,000 files
one by one. Check the logs for a warning:

```bash
docker compose logs moodle
```

Place the archive (Step A) and recreate the container as shown above.

**Start completely fresh**

```bash
docker compose -f docker-compose.yml -f docker-compose.moodle.yml down -v
```

This removes all containers and data volumes, so the next `up` re-imports the
dataset from scratch.

---

## What to expect (summary of timings)

| Step | Time |
|------|------|
| Install Docker Desktop | one-off, a few minutes |
| Download `moodle-src.tar.gz` (full demo only) | ~70 MB, a few minutes |
| First `docker compose up --build` | **5–10 minutes** |
| Later starts | seconds |
| Each extraction | **40–50 seconds** |
