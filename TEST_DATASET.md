# Using the Test Dataset

This page explains how to download, set up, and use the provided test dataset for PM4Moodle.

---

## About the Test Dataset

The test dataset is a complete backup (`backup.sql`) from a Moodle database, created specifically for testing PM4Moodle.  
It includes data for 9 of the most common and pedagogically important Moodle modules, as identified by instructor interviews.

---

## Downloading the Test Dataset

You can find the test dataset in the repository under:
test_dataset/backup.sql

Or [download it directly here](test_dataset/backup.sql) (right-click and “Save link as...” if needed).

---

## Setting Up the Test Dataset

## How to Restore the Provided Test Dataset

You can use the `moodle_backup_restore.py` script to restore the provided test Moodle database backup into a new database.  
Below are step-by-step instructions for using the tool interactively.

---

### 1. Run the Backup/Restore Script

Open your terminal and navigate to the folder containing the script (PM4Moodle/test_dataset), then run:

```bash
python moodle_backup_restore.py
```
### 2. Respond to the Prompts

- **Default Configuration:**  
  The tool will display default settings (host, username, password, source database, backup path, destination database, etc.).
  - When asked:  
    `Would you like to use the default configuration? [Y/n]:`  
    - Type `n` to enter your own details, or just press `Enter` (or type `y`) to use the defaults.

- **For Each Prompt:**  
  For each of the following, either press `Enter` to accept the default value in brackets, or type your custom value:
  - **Enter host [localhost]:**  
  Database server address. Press `Enter` for local computer or type another address if needed.
- **Enter username [root]:**  
  MySQL username. Press `Enter` for `root` or type your username.
- **Enter password [empty]:**  
  MySQL password. Press `Enter` if none, or type your password.
- **Enter source database [moodle]:**  
  Name of your original Moodle database. *(Not needed for restoring an existing backup—just press `Enter` to continue.)*
- **Destination database:**  
  Enter the name you want for your new test database (e.g., `test_moodle`), or press `Enter` to use the default name.
- **Backup file path:**  
  Enter the full path to where you stored the `backup.sql` file (default is `PM4Moodle/test_dataset/backup.sql` inside your project folder).
- **MySQL binary folder:**  
  Enter the path to the `bin` folder of your MySQL installation (e.g., ` C:\Moodle5.1\server\mysql\bin` or as shown by your Moodle installer).

- **Backup Step:**  
  When prompted:  
  `Would you like to create a backup from 'moodle' database? [y/n]:`  
  - Type `n` (because you already have the backup file provided).

- **Restore Step:**  
  When prompted:  
  `Would you like to restore backup to 'your_database_name' database? [y/n]:`  
  - Type `y` to proceed with restoring your backup file into the specified database.

**The Figure below shows an example of restoring the backup file.** 
<p align='center'>
<img src="figures/backup-restore.png" alt="Restoring the backup file" width="450"/>
</p>

## Testing Extraction with PM4Moodle – A Walkthrough

### 1. Start the PM4Moodle tool.  
  For setup details, see the [Setup Guide](SETUP.md).
  
Once the tool is running, as a tester you will see the main extraction interface (see the figure below). 
<p align='center'>
<img src="figures/main-page1.png" alt="Restoring the backup file" width="450"/>
</p>
Here’s what you should check and how to validate the extraction against the test dataset:

### 2. Connect to the test database you just restored. (see the figure below)
<p align='center'>
<img src="figures/database-connection.png" alt="Test DB connection" width="450"/>
</p>

### 3. Select courses, modules, and event types as needed. 
  The first combo box ("Select Courses:") lists the available courses (e.g., the two simulated test courses).  
  The second ("Select Modules:") shows the 9 common Moodle modules in your test set.  
  The third ("Select Events:") displays event types for the selected module(s).  
  _Leaving any field unselected will extract logs for all of that type._

### 4. Run the extraction.
  Click “Run Extraction” to generate the OCEL 2.0 event log and DFG visualization.  
  Download links will be provided for the log and its OC-DFG. You see:

<p align='center'>
<img src="figures/main-page2.png" alt="Test DB connection" width="450"/>
</p>

- **Validate the extraction results.**  
  Use the Verification Matrix and State Chart Diagram tabs to confirm that all required relationships and lifecycles are present in the extracted log, enabling you to answer Q1–Q5.  
  (See screenshots and details in the [Usage Guide](USAGE_GUIDE.md).)

---


## 6. Troubleshooting

- If you cannot connect, double-check the username, password, and database name in your config.
- Make sure your MySQL server is running and accessible.
- For further help, see the [Troubleshooting section in the User Guide](USER_GUIDE.md#troubleshooting).

---

