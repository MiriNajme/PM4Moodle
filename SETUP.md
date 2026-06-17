# PM4Moodle Setup Guide

Welcome to the **PM4Moodle Setup Guide**. This document will walk you through the process of cloning the repository, setting up the backend and frontend environments, and troubleshooting common installation issues.

---

## Table of Contents

- [Cloning the Repository](#cloning-the-repository)
- [Backend Setup](#backend-setup)
- [Frontend Setup](#frontend-setup)
- [Troubleshooting](#troubleshooting)

---


## Cloning the Repository

> ⚠️ **Shell Compatibility Note**  
> Please make sure to use the correct terminal **for all the steps below**:  
> - On **Windows**, use **PowerShell** (instead of Command Prompt or Git Bash), as some commands may not work properly in other shells.  
> - On **macOS** and **Linux**, the default **Terminal** is fully supported.


To get started, you need to clone this repository to your local machine.

1. Open your terminal or command prompt.
2. Navigate to the directory where you want to place the project.
3. Run the following command:

   ```bash
   git clone https://github.com/MiriNajme/PM4Moodle.git

4. Change into the project directory:

    ```bash
   cd PM4Moodle

You are now ready to set up the backend and frontend.

## Backend Setup

The backend is built with **Python** and **Flask**.

### 1. Install Python

Use **Python 3.11–3.14** (**3.12 recommended**).  
[Download Python here](https://www.python.org/downloads/)

> ⚠️ **Pick a supported version.** The scientific packages this tool depends on
> (`numpy`, `scipy`, `pm4py`, `lxml`, `cvxopt`, …) ship prebuilt binaries only
> for specific Python versions. If you install on a Python version that is too
> new (or too old), `pip` may try to build these from source and produce a
> broken environment. If unsure, install **Python 3.12**.

You can check your version with:

```bash
python --version
```

### 2. Open the Project in Your Code Editor

We recommend using [Visual Studio Code (VS Code)](https://code.visualstudio.com/) for the best experience.

1. Launch VS Code (or your preferred editor).
2. Open the cloned project folder (`PM4Moodle`).


### 3. Create and Activate a Virtual Environment

In your terminal or powershell go to your `backend/` folder with the command:

```bash
cd backend
```
Then run:

```bash
python -m venv venv
```

Activate the virtual environment:

- **Windows PowerShell:**
  ```
  .\venv\Scripts\Activate
  ```
- **macOS/Linux:**
  ```
  source venv/bin/activate
  ```

You should now see your prompt prefixed with `(venv)`.

### 4. Install Dependencies

Inside your virtual environment, run:

```bash
pip install -r requirements.txt
```

### 5. Set Environment Variables (This is optional for debug mode)

- **Windows PowerShell:**
  ```powershell
  $env:FLASK_APP = "app.py"
  $env:FLASK_DEBUG = "1"   
  ```
- **macOS/Linux:**
  ```bash
  export FLASK_APP=app.py
  export FLASK_DEBUG=1     
  ```

### 6. Run the Flask Application

```bash
flask run
```

You should see something like:
```
* Running on http://127.0.0.1:5000/
```

**Pro Tip:**  
If `flask run` does not work, use:
```bash
python -m flask run
```

---

## Frontend Setup

The frontend requires **Node.js version 22.x**.

### 1. Install Node.js version 22.x

Download and install Node.js from the [official website](https://nodejs.org/en/download).

### 2. Install Frontend Dependencies

Open another terminal or PowerShell and navigate to the `frontend/` folder and run:

```bash
npm install --legacy-peer-deps
```

### 3. Start the Frontend Development Server

```bash
npm run dev
```

The frontend should now be running, typically on [[http://localhost:5173](http://localhost:5173/)].

---

## Troubleshooting

- Make sure Python and Node.js are correctly installed and added to your system PATH.
- Ensure your virtual environment is activated before installing Python packages or running the Flask app.
- If you encounter errors when running `flask run`, make sure you have activated your virtual environment first by running `.\venv\Scripts\Activate` (on Windows) or `source venv/bin/activate` (on macOS/Linux), and then try `flask run` again.

### "No module named ..." / "broken install" errors on `flask run`

If `flask run` fails with a `ModuleNotFoundError` or "broken install" coming from
a compiled package, for example:

```
ModuleNotFoundError: No module named 'rpds.rpds'
ModuleNotFoundError: No module named 'numpy._core._multiarray_umath'
ImportError: The `scipy` install you are using seems to be broken
ImportError: cannot import name 'etree' from 'lxml'
```

your Python version installed some packages from source as broken C extensions.
This almost always means **your Python version is unsupported** (typically too
new). Fix it by recreating the environment on a supported Python (**3.11–3.14,
3.12 recommended**):

```bash
# from the backend/ folder, with the old venv deactivated
rm -rf venv            # Windows PowerShell: Remove-Item -Recurse -Force venv
py -3.12 -m venv venv  # or: python3.12 -m venv venv
.\venv\Scripts\Activate            # Windows
# source venv/bin/activate         # macOS/Linux
pip install --upgrade pip
pip install -r requirements.txt
```

`requirements.txt` is configured to install these packages from prebuilt
wheels only, so if your Python version is unsupported the install will **fail
immediately with a clear message** instead of producing a broken environment.


