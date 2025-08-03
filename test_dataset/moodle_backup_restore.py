import subprocess
import sys
from colorama import Fore, Style


def print_default_config(
    host, user, password, backup_from_db, restore_to_db, backup_file, mysql_bin_folder
):
    """Print the default configuration parameters"""
    print(
        f"\n{Style.BRIGHT}{Fore.CYAN}=== DEFAULT CONFIGURATION ==={Style.RESET_ALL}\n\n"
    )
    print(f"Host: {Fore.YELLOW}{host}{Style.RESET_ALL}")
    print(f"User: {Fore.YELLOW}{user}{Style.RESET_ALL}")
    print(
        f"Password: {Fore.YELLOW}{'*' * len(password) if password else '(empty)'}{Style.RESET_ALL}"
    )
    print(f"Backup from database: {Fore.YELLOW}{backup_from_db}{Style.RESET_ALL}")
    print(f"Restore to database: {Fore.YELLOW}{restore_to_db}{Style.RESET_ALL}")
    print(f"Backup file path: {Fore.YELLOW}{backup_file}{Style.RESET_ALL}")
    print(f"MySQL binary folder: {Fore.YELLOW}{mysql_bin_folder}{Style.RESET_ALL}")
    print(
        f"\n{Style.BRIGHT}{Fore.CYAN}================================{Style.RESET_ALL}\n"
    )


def get_user_config():
    """Get database configuration from user input"""
    print(f"\n{Style.BRIGHT}{Fore.GREEN}=== ENTER CONFIGURATION ==={Style.RESET_ALL}")
    host = (
        input(f"Enter host [{Fore.YELLOW}localhost{Style.RESET_ALL}]: ").strip()
        or "localhost"
    )
    user = (
        input(f"Enter username [{Fore.YELLOW}root{Style.RESET_ALL}]: ").strip()
        or "root"
    )
    password = input(f"Enter password [{Fore.YELLOW}empty{Style.RESET_ALL}]: ").strip()
    backup_from_db = (
        input(f"Enter source database [{Fore.YELLOW}moodle{Style.RESET_ALL}]: ").strip()
        or "moodle"
    )
    restore_to_db = (
        input(
            f"Enter destination database [{Fore.YELLOW}moodle_backup{Style.RESET_ALL}]: "
        ).strip()
        or "moodle_backup"
    )
    backup_file = (
        input(
            f"Enter backup file path [{Fore.YELLOW}C:\\DbBackup\\backup.sql{Style.RESET_ALL}]: "
        ).strip()
        or r"C:\DbBackup\backup.sql"
    )
    mysql_bin_folder = (
        input(
            f"Enter MySQL binary folder [{Fore.YELLOW}C:\\Moodle5.1\\server\\mysql\\bin{Style.RESET_ALL}]: "
        ).strip()
        or r"C:\Moodle5.1\server\mysql\bin"
    )
    print(
        f"{Style.BRIGHT}{Fore.GREEN}==============================={Style.RESET_ALL}\n"
    )

    return (
        host,
        user,
        password,
        backup_from_db,
        restore_to_db,
        backup_file,
        mysql_bin_folder,
    )


def get_yes_no_input(prompt, default="y"):
    """Get yes/no input from user"""
    while True:
        response = (
            input(
                f"{prompt} [{Fore.YELLOW}{'Y/n' if default == 'y' else 'y/N'}{Style.RESET_ALL}]: "
            )
            .strip()
            .lower()
        )
        if not response:
            return default == "y"
        if response in ["y", "yes"]:
            return True
        elif response in ["n", "no"]:
            return False
        else:
            print(f"{Fore.RED}Please enter 'y' for yes or 'n' for no.{Style.RESET_ALL}")


def backup_database(host, user, password, database, output_file, mysql_bin_folder):
    # Construct the mysqldump command
    command = [
        f"{mysql_bin_folder}\\mysqldump",
        f"--host={host}",
        f"--user={user}",
        f"--password={password}",
        f"{database}",
        f"--result-file={output_file}",
    ]

    # Run the mysqldump command
    print(
        f"\nRunning {Fore.YELLOW}{Style.BRIGHT}BACKUP{Style.RESET_ALL} command on {database}"
    )
    subprocess.run(command, shell=True)
    print(f"{Fore.LIGHTGREEN_EX}--DONE{Style.RESET_ALL}\n")


def clear_and_restore_database(
    host, user, password, database, input_file, mysql_bin_folder
):
    base_command = [
        f"{mysql_bin_folder}\\mysql",
        f"--host={host}",
        f"--user={user}",
        f"--password={password}",
    ]

    # Construct the mysql clear command
    clear_command = ["-e", f"DROP DATABASE IF EXISTS {database};"]

    # Run the mysql clear command
    print(
        f"\nStart to {Style.BRIGHT}{Fore.RED}CLEARING{Style.RESET_ALL} backup database ({database}).\nIt will take time, please wait!!"
    )
    subprocess.run(base_command + clear_command, shell=True)
    print(f"{Fore.LIGHTGREEN_EX}--DONE{Style.RESET_ALL}\n")

    # Construct the mysql create database command
    create_database_command = ["-e", f"CREATE DATABASE {database};"]

    # Run the mysql create database command
    print(
        f"\n{Style.BRIGHT}{Fore.BLUE}Creating{Style.RESET_ALL} new backup database ({database})"
    )
    subprocess.run(base_command + create_database_command, shell=True)
    print(f"{Fore.LIGHTGREEN_EX}--DONE{Style.RESET_ALL}\n")

    # Construct the mysql restore command
    restore_command = [f"{database}", f"< {input_file}"]

    # Run the mysql restore command
    print(
        f"\n{Style.BRIGHT}{Fore.MAGENTA}Restoring{Style.RESET_ALL} backup file.\nIt will take time, please wait!!"
    )
    subprocess.run(" ".join(base_command + restore_command), shell=True)
    print(f"{Fore.LIGHTGREEN_EX}--DONE{Style.RESET_ALL}\n")


if __name__ == "__main__":
    print(
        f"\n{Style.BRIGHT}{Fore.MAGENTA}=== MOODLE DATABASE BACKUP & RESTORE TOOL ==={Style.RESET_ALL}\n"
    )

    # Default configuration
    host = "localhost"
    user = "root"
    password = ""
    backup_from_database = "moodle"
    restore_to_database = "moodle_backup"
    backup_file = r"C:\DbBackup\backup.sql"
    mysql_bin_folder = r"C:\Moodle5.1\server\mysql\bin"

    # Print default configuration and ask if user wants to change it
    print_default_config(
        host,
        user,
        password,
        backup_from_database,
        restore_to_database,
        backup_file,
        mysql_bin_folder,
    )

    use_default = get_yes_no_input(
        "Would you like to use the default configuration?", "y"
    )

    if not use_default:
        (
            host,
            user,
            password,
            backup_from_database,
            restore_to_database,
            backup_file,
            mysql_bin_folder,
        ) = get_user_config()

    # Ask about backup operation
    should_backup = get_yes_no_input(
        f"\nWould you like to create a backup from '{backup_from_database}' database?",
        "y",
    )

    if should_backup:
        backup_database(
            host, user, password, backup_from_database, backup_file, mysql_bin_folder
        )
    else:
        print(f"{Fore.YELLOW}Skipping backup operation.{Style.RESET_ALL}")

    # Ask about restore operation
    should_restore = get_yes_no_input(
        f"\nWould you like to restore backup to '{restore_to_database}' database?", "y"
    )

    if should_restore:
        if not should_backup:
            # If no backup was created, check if backup file exists
            import os

            if not os.path.exists(backup_file):
                print(
                    f"{Fore.RED}Error: Backup file '{backup_file}' does not exist!{Style.RESET_ALL}"
                )
                print(
                    f"{Fore.YELLOW}Please create a backup first or specify an existing backup file.{Style.RESET_ALL}"
                )
                sys.exit(1)

        clear_and_restore_database(
            host, user, password, restore_to_database, backup_file, mysql_bin_folder
        )
    else:
        print(f"{Fore.YELLOW}Skipping restore operation.{Style.RESET_ALL}")

    if should_backup or should_restore:
        print(
            f"\n🎉🎉🎉\tMISSION {Style.BRIGHT}{Fore.CYAN}COMPLETED{Style.RESET_ALL} SUCCESSFULLY.\t🎆🎆🎆\n"
        )
    else:
        print(f"\n{Fore.YELLOW}No operations were performed.{Style.RESET_ALL}\n")
