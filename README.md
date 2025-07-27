# PM4Moodle

**PM4Moodle** is a specialized tool for extracting [OCEL 2.0](https://www.ocel-standard.org/) event logs from Moodle, covering the most common and important Moodle modules. It offers an intuitive interface for users to connect directly to their Moodle database and extract OCEL 2.0 logs effortlessly.

Key features include:

- **Database Connection Interface:** Simple UI to connect to your Moodle database.
- **OCEL 2.0 Extraction:** Seamlessly extract OCEL 2.0 event logs from supported Moodle modules.
- **Object-Centric Directly-Follows Graph (OC-DFG):** Automatically generate OC-DFG visualizations for extracted logs.
- **Verification Matrix:** Allows teachers to verify the extracted logs with a matrix showing the number of objects per event, supporting log quality checks.
- **Lifecycle Diagrams:** For each supported module, generates a state chart (lifecycle diagram) based on the actual events for that module in the extracted file.
- **Downloadable Outputs:** Download both the OCEL 2.0 JSON log and generated visualizations directly from the interface.


This tool streamlines the extraction, validation, and analysis of object-centric event logs from Moodle, supporting object-centric process mining and educational analytics.


---

## Table of Contents

- [Project Structure](#project-structure)
- [Cloning the Repository](#Cloning-the-Repository)
- [Backend Setup](#backend-setup)
- [Frontend Setup](#frontend-setup)
- [Troubleshooting](#troubleshooting)
- [How to Use PM4Moodle](#how-to-use-pm4moodle)
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
   git clone https://github.com/MiriNajme/PM4Moodle.git

4. Change into the project directory:

    ```bash
   cd PM4Moodle

You are now ready to set up the backend and frontend.

## Backend Setup

The backend is built with **Python** and **Flask**.

### 1. Install Python

Make sure you have Python 3.8+ installed.  
[Download Python here](https://www.python.org/downloads/)

### 2. Open the Project in Your Code Editor

We recommend using [Visual Studio Code (VS Code)](https://code.visualstudio.com/) for the best experience.

1. Launch VS Code (or your preferred editor).
2. Open the cloned project folder (`PM4Moodle`).


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


---

## How to Use PM4Moodle
PM4Moodle’s interface is organized into three main tabs.
Here’s how to extract logs and generate visualizations:

### Set Up Database Connection

- Click the **Settings** button in the top-right corner of the page.
- Enter your Moodle database credentials (host, port, user, password, database name).
- Save your settings.

<img src="screenshots/Database_Settings.png" alt="Screenshot: Database Settings Dialog" width="500"/>

### Extraction Tab

#### **Step 1: Select Modules and Events**

- You can **extract logs for all supported modules and their events by simply clicking on "Run Extraction"** without selecting any modules or events.
- Alternatively, **choose one or more Moodle module types** (e.g., Assignment, File, Folder, URL) to extract logs only for those modules. If you select modules but no events, all events for the selected modules will be extracted.
- For more fine-grained control, you can **select specific events for any chosen module** to extract only those events.

#### **Step 2: Extract and Download the Log**

- Click the **Run Extraction** button.
- The tool connects to your database and processes the data to extract the OCEL 2.0 log based on your selection.
- When finished, download the OCEL 2.0 log in JSON format and the Directly-Follows Graph (DFG) as an image, if desired. You can also view these files in full size without downloading them.

<img src="screenshots/Extraction_Tab.png" alt="Screenshot: Extraction and Download" width="500"/>

### Verification Matrix Tab
- After you extract a log, navigate to the **Verification Matrix** tab to see the matrix automatically generated for your extracted OCEL 2.0 log.
- The verification matrix displays the number of objects per event in the extracted log, allowing you to inspect and verify log quality and completeness at a glance.
- This feature helps teachers and analysts confirm that the log includes the expected level of detail and correct object-event relationships.
- Use the matrix to identify potential data issues before proceeding with further analysis or visualization.

<img src="screenshots/Verification_Tab.png" alt="Screenshot: Verification Matrix" width="500"/>

### Statechart Diagram Tab

- Upon extracting an OCEL 2.0 log, users can navigate to the **Statechart Diagram** tab to automatically view statechart lifecycle diagrams for each Moodle module included in the extraction.
- These diagrams are dynamically generated based on the events present in the extracted log, visually depicting the actual lifecycle transitions (such as creation, update, view, and deletion) observed for each module instance.
- It is important to note that the completeness of a statechart diagram directly depends on the event coverage within the extracted log. If certain lifecycle events are absent from the data—for instance, if a module instance was never deleted or updated—those transitions will not appear in the statechart, and the full lifecycle cannot be reconstructed.
- This feature enables users to gain an object-centric understanding of process behavior at the module level, and to assess which lifecycle transitions are supported by empirical evidence in the dataset.

As an example, the figure below illustrates the statechart diagram generated for the **Assignment** module:

<img src="screenshots/StateChart_Tab.png" alt="Screenshot: Assignment Statechart Diagram" width="500"/>


---
## License

 
[MIT](LICENSE)

---

