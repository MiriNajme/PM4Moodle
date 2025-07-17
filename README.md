# Moodle OCEL 2.0 Extractor

**Moodle OCEL 2.0 Extractor** is a specialized tool for extracting [OCEL 2.0](https://www.ocel-standard.org/) event logs from Moodle, covering the most common and important Moodle modules. It offers an intuitive interface for users to connect directly to their Moodle database and extract OCEL 2.0 logs effortlessly.

Key features include:

- **Database Connection Interface:** Simple UI to connect to your Moodle database.
- **OCEL 2.0 Extraction:** Seamlessly extract OCEL 2.0 event logs from supported Moodle modules.
- **Object-Centric Directly-Follows Graph (OC-DFG):** Automatically generate OC-DFG visualizations for extracted logs.
- **Verification Matrix:** Allows teachers to verify the extracted logs with a matrix showing the number of objects per event, supporting log quality checks.
- **Lifecycle Diagrams:** For each supported module, generates a state chart (lifecycle diagram) based on the actual events for that module in the extracted file.

This tool streamlines the extraction, validation, and analysis of object-centric event logs from Moodle, supporting object-centric process mining and educational analytics.


---

## Table of Contents

- [Project Structure](#project-structure)
- [Cloning the Repository](#Cloning-the-Repository)
- [Backend Setup](#backend-setup)
- [Frontend Setup](#frontend-setup)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Project Structure

```
root/
├── backend/
│   ├── app.py
│   └── ...
└── frontend/
    └── ...
```

---

## Cloning the Repository

To get started, you need to clone this repository to your local machine.

1. Open your terminal or command prompt.
2. Navigate to the directory where you want to place the project.
3. Run the following command:

   ```bash
   git clone https://github.com/MiriNajme/Ocpm2-extension.git

4. Change into the project directory:

    ```bash
   cd Ocpm2-extension

You are now ready to set up the backend and frontend.

## Backend Setup

The backend is built with **Python** and **Flask**.

### 1. Install Python

Make sure you have Python 3.8+ installed.  
[Download Python here](https://www.python.org/downloads/)

### 2. Open the Project in Your Code Editor

We recommend using [Visual Studio Code (VS Code)](https://code.visualstudio.com/) for the best experience.

1. Launch VS Code (or your preferred editor).
2. Open the cloned project folder (`Ocpm2-extension`).


### 3. Create and Activate a Virtual Environment

In your terminal go to your `backend/` folder by the command:

```bash
cd backend
```
Then run:

```bash
python -m venv venv
```

Activate the virtual environment:

- **Windows:**
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

### 5. Set Environment Variables

- **Windows PowerShell:**
  ```powershell
  $env:FLASK_APP = "app.py"
  $env:FLASK_DEBUG = "1"   # Optional for debug mode
  ```
- **macOS/Linux:**
  ```bash
  export FLASK_APP=app.py
  export FLASK_DEBUG=1     # Optional for debug mode
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

The frontend requires **Node.js**.

### 1. Install Node.js

Download and install Node.js from the [official website](https://nodejs.org/en/download).

### 2. Install Frontend Dependencies

Navigate to the `frontend/` folder and run:

```bash
npm install
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


---

## License

 
[MIT](LICENSE)

---

