# --- Imports ---
import datetime
import json
import os
import time
import sys
import re
# Add colorama imports
import colorama
from colorama import Fore, Back, Style, init

# --- Initialize Colorama ---
# init(autoreset=True) automatically resets the style after each print
init(autoreset=True)

# --- Configuration ---
POMODORO_WORK_MINUTES = 25
POMODORO_SHORT_BREAK_MINUTES = 5
POMODORO_LONG_BREAK_MINUTES = 15
POMODOROS_BEFORE_LONG_BREAK = 4
POINTS_PER_TASK = 10  # Points awarded for completing a task

# --- Leveling System ---
LEVEL_THRESHOLDS = [
    (1, 0), (2, 100), (3, 250), (4, 500), (5, 1000),
    (6, 2000), (7, 3500), (8, 5500), (9, 8000), (10, 11000),
    (11, 15000), (12, 20000),
]

# --- [Helper functions: clean_filename, load_tasks, save_tasks] ---
# (These functions remain unchanged from the previous version)
# --- Paste them here ---
def clean_filename(userid):
    """Cleans the userid to create a safe filename."""
    userid = userid.lower()
    userid = re.sub(r'[^\w\-]+', '', userid)
    if not userid:
        userid = "default_user"
    return f"tasks_{userid}.json"

def load_tasks(userid):
    """
    Loads tasks and user info from a user-specific JSON file.
    Returns a tuple: (tasks_list, user_info_dict)
    """
    filename = clean_filename(userid)
    print(f"--- Loading data for user '{userid}' from {filename} ---")

    default_user_info = {"userid": userid, "points": 0} # Default structure

    if not os.path.exists(filename):
        print("No existing data file found for this user. Starting fresh.")
        return [], default_user_info # Return empty tasks list and default info

    try:
        with open(filename, 'r') as f:
            data = json.load(f)

            # Check if data is in the new dictionary format or old list format
            if isinstance(data, dict) and "tasks" in data and "user_info" in data:
                tasks_data = data.get("tasks", [])
                user_info = data.get("user_info", default_user_info)
                # Ensure points key exists in loaded user_info
                if "points" not in user_info:
                    user_info["points"] = 0
                if "userid" not in user_info: # Add userid if somehow missing
                    user_info["userid"] = userid
            elif isinstance(data, list):
                # Handle old format: tasks are the list, user_info is default
                print("Old tasks format detected. Converting and initializing points to 0.")
                tasks_data = data
                user_info = default_user_info
            else:
                 # Unknown format
                 print("Warning: Unknown data format in file. Starting fresh.")
                 return [], default_user_info

            # Process tasks data (same as before)
            processed_tasks = []
            for task in tasks_data:
                if task.get('due_datetime_str'):
                    task['due_datetime'] = datetime.datetime.fromisoformat(task['due_datetime_str'])
                else:
                    task['due_datetime'] = None
                if 'completed' not in task:
                    task['completed'] = False
                if 'pomodoros_completed' not in task:
                    task['pomodoros_completed'] = 0
                processed_tasks.append(task) # Append processed task

            print(f"Loaded {len(processed_tasks)} tasks. Current points: {user_info.get('points', 0)}")
            return processed_tasks, user_info

    except (json.JSONDecodeError, IOError, TypeError) as e:
        print(f"Error loading data from {filename}: {e}. Starting with an empty list and 0 points.")
        return [], default_user_info # Return defaults on error

def save_tasks(tasks, user_info, userid):
    """Saves tasks and user info to a user-specific JSON file."""
    filename = clean_filename(userid)
    print(f"--- Saving data for user '{userid}' to {filename} ---")

    try:
        # Prepare tasks for JSON serialization
        tasks_to_save = []
        for task in tasks:
            task_copy = task.copy()
            if task_copy.get('due_datetime'):
                task_copy['due_datetime_str'] = task_copy['due_datetime'].isoformat()
            task_copy.pop('due_datetime', None)
            if 'pomodoros_completed' not in task_copy:
                 task_copy['pomodoros_completed'] = 0
            tasks_to_save.append(task_copy)

        # Create the combined data structure
        data_to_save = {
            "user_info": user_info,
            "tasks": tasks_to_save
        }

        with open(filename, 'w') as f:
            json.dump(data_to_save, f, indent=4)
        print(f"Saved {len(tasks_to_save)} tasks. Points: {user_info.get('points', 0)}")

    except IOError as e:
        print(f"Error saving data to {filename}: {e}")


# --- [Core logic functions: display_agenda, add_task, complete_task, Pomodoro funcs, calculate_level] ---
# (These functions remain unchanged internally, only the print in complete_task gets color via autoreset)
# --- Paste them here ---
def display_agenda(tasks):
    """Sorts tasks and displays them grouped by day, including Pomodoro count."""
    if not tasks:
        print("\nNo tasks in your agenda!")
        return

    timed_tasks = [t for t in tasks if t.get('due_datetime')]
    all_day_tasks = [t for t in tasks if not t.get('due_datetime')]
    timed_tasks.sort(key=lambda x: x['due_datetime'])
    tasks_by_day = {}
    today = datetime.date.today()
    for task in timed_tasks:
        task_date = task['due_datetime'].date()
        if task_date not in tasks_by_day:
            tasks_by_day[task_date] = []
        tasks_by_day[task_date].append(task)

    print("\n--- Your Agenda ---")
    sorted_dates = sorted(tasks_by_day.keys())

    for display_date in sorted_dates:
        header_str = display_date.strftime('%A, %B %d, %Y') # e.g., Saturday, April 12, 2025
        if display_date == today:
            header_str = f"TODAY - {header_str}"
        elif display_date == today + datetime.timedelta(days=1):
            header_str = f"TOMORROW - {header_str}"
        # Make Date headers bold (example of using Style)
        print(Style.BRIGHT + f"\n--- {header_str} ---") # Style.BRIGHT + Style.RESET_ALL (autoreset handles reset)

        for i, task in enumerate(tasks_by_day[display_date]):
            completed = task.get('completed', False)
            status = Fore.LIGHTBLACK_EX + "[X]" if completed else "[ ]" # Dim completed tasks slightly
            time_str = task['due_datetime'].strftime('%I:%M %p') if task.get('due_datetime') else "All Day"
            title = task.get('title', 'No Title')
            project = f" ({task['project']})" if task.get('project') else ""
            priority = f" [P{task['priority']}]" if task.get('priority') else ""
            pomos = f" (Pomos: {task.get('pomodoros_completed', 0)})"
            # Add strikethrough for completed tasks if terminal supports it (often doesn't)
            # title_display = f"\u0336{title}\u0336" if completed else title # Strikethrough approximation
            title_display = title # Keep it simple
            task_line = f"  {status} {time_str.ljust(9)} {title_display}{project}{priority}{pomos}"
            print(Fore.LIGHTBLACK_EX + task_line if completed else task_line) # Dim completed tasks

    if all_day_tasks:
        print(Style.BRIGHT + "\n--- Unscheduled / All Day Tasks ---") # Bold header
        for i, task in enumerate(all_day_tasks):
             completed = task.get('completed', False)
             status = Fore.LIGHTBLACK_EX + "[X]" if completed else "[ ]"
             title = task.get('title', 'No Title')
             project = f" ({task['project']})" if task.get('project') else ""
             priority = f" [P{task['priority']}]" if task.get('priority') else ""
             pomos = f" (Pomos: {task.get('pomodoros_completed', 0)})"
             # title_display = f"\u0336{title}\u0336" if completed else title
             title_display = title
             task_line = f"  {status} {'No Date'.ljust(9)} {title_display}{project}{priority}{pomos}"
             print(Fore.LIGHTBLACK_EX + task_line if completed else task_line)


def add_task(tasks):
    """Prompts user for task details and adds it, initializing pomodoro count."""
    print("\n--- Add New Task ---")
    title = input("Task Title: ")
    if not title:
        print(Fore.RED + "Task title cannot be empty.")
        return
    due_date_str = input("Due Date (YYYY-MM-DD) or leave blank: ")
    due_time_str = input("Due Time (HH:MM) or leave blank: ")
    project = input("Project/Category (optional): ")
    priority_str = input("Priority (1=High, 2=Med, 3=Low - optional): ")

    due_datetime = None
    if due_date_str:
        try:
            date_part = datetime.datetime.strptime(due_date_str, "%Y-%m-%d").date()
            if due_time_str:
                time_part = datetime.datetime.strptime(due_time_str, "%H:%M").time()
                due_datetime = datetime.datetime.combine(date_part, time_part)
            else:
                 print(Fore.YELLOW + "Info: Date specified without time. Task treated as 'All Day'/Unscheduled.")
                 due_datetime = None # Set to None if only date provided
        except ValueError:
            print(Fore.RED + "Invalid date or time format. Task treated as unscheduled.")
            due_datetime = None

    priority = None
    if priority_str.isdigit():
        priority = int(priority_str)

    new_task = {
        # Generate a more robust ID later if needed (e.g., UUID)
        "id": int(time.time() * 1000), # Simple timestamp-based ID for now
        "title": title,
        "due_datetime": due_datetime,
        "project": project if project else None,
        "priority": priority,
        "completed": False,
        "pomodoros_completed": 0
    }
    tasks.append(new_task)
    print(Fore.GREEN + "Task added successfully!")

def complete_task(tasks, user_info):
    """Lists incomplete tasks, marks the selected one as complete, and handles points/leveling."""
    print("\n--- Mark Task as Complete ---")
    incomplete_tasks = [(i, task) for i, task in enumerate(tasks) if not task.get('completed', False)]

    if not incomplete_tasks:
        print(Fore.YELLOW + "No tasks to complete!")
        return

    incomplete_tasks.sort(key=lambda item: item[1].get('due_datetime') or datetime.datetime.max)

    print("Select task to mark as complete:")
    display_map = {}
    for display_index, (original_index, task) in enumerate(incomplete_tasks):
        display_map[display_index] = original_index
        due_str = task['due_datetime'].strftime('%Y-%m-%d %H:%M') if task.get('due_datetime') else "No date"
        pomos = task.get('pomodoros_completed', 0)
        print(f"  {display_index}: {task['title']} ({due_str}) [Pomos: {pomos}]")

    try:
        choice = int(input("Enter task number: "))
        if choice in display_map:
            original_task_index = display_map[choice]

            if not tasks[original_task_index].get('completed', False):
                tasks[original_task_index]['completed'] = True
                points_earned = POINTS_PER_TASK
                old_points = user_info.get('points', 0)
                old_level = calculate_level(old_points)  # Get level *before* adding points

                user_info['points'] = old_points + points_earned # Add the points
                new_points = user_info['points']
                new_level = calculate_level(new_points)      # Get level *after* adding points

                print(Fore.GREEN + f"\nTask '{tasks[original_task_index]['title']}' marked as complete.")
                print(Fore.CYAN + f"Congratulations! You earned {points_earned} points.")
                print(f"Total points: {new_points}")

                if new_level > old_level:
                    # Use Bright Green for Level Up message
                    print(Fore.GREEN + Style.BRIGHT + f"\n🎉🎉🎉 Level Up! 🎉🎉🎉")
                    print(Fore.GREEN + Style.BRIGHT + f"You are now Level {new_level}!")
            else:
                print(Fore.YELLOW + f"Task '{tasks[original_task_index]['title']}' was already complete.")

        else:
            print(Fore.RED + "Invalid choice.")
    except ValueError:
        print(Fore.RED + "Invalid input. Please enter a number.")

def run_timer(minutes, session_type="Work"):
    """Runs a countdown timer for the specified minutes."""
    total_seconds = minutes * 60
    cancelled = False
    # Use Cyan for Work, Magenta for Breaks
    color = Fore.CYAN if session_type == "Work" else Fore.MAGENTA
    print(color + f"\nStarting {session_type} session ({minutes} minutes). Press Ctrl+C to cancel.")
    try:
        while total_seconds > 0:
            mins, secs = divmod(total_seconds, 60)
            timer_display = f"{session_type}: {mins:02d}:{secs:02d}".ljust(25)
            # Print timer in specific color
            print(color + f"\r{timer_display}", end="")
            sys.stdout.flush()
            time.sleep(1)
            total_seconds -= 1
        # Clear timer line with spaces and print completion message in color
        print(color + "\r" + f"{session_type} session finished!".ljust(25))
    except KeyboardInterrupt:
        # Clear timer line and print cancellation message in Yellow
        print(Fore.YELLOW + "\r" + f"{session_type} session cancelled.".ljust(25))
        cancelled = True
    if not cancelled:
        # Use system bell for alert
        print("\a", end="") # \a is the ASCII Bell character
    return not cancelled

def select_task_for_pomodoro(tasks):
    """Lists incomplete tasks and lets the user choose one to work on."""
    print("\n--- Start Pomodoro Session ---")
    incomplete_tasks = [(i, task) for i, task in enumerate(tasks) if not task.get('completed', False)]
    if not incomplete_tasks:
        print(Fore.YELLOW + "No incomplete tasks to start a Pomodoro for!")
        return None
    incomplete_tasks.sort(key=lambda item: item[1].get('due_datetime') or datetime.datetime.max)
    print("Select task to work on:")
    display_map = {}
    for display_index, (original_index, task) in enumerate(incomplete_tasks):
        display_map[display_index] = original_index
        due_str = task['due_datetime'].strftime('%Y-%m-%d %H:%M') if task.get('due_datetime') else "No date"
        pomos = task.get('pomodoros_completed', 0)
        print(f"  {display_index}: {task['title']} ({due_str}) [Pomos: {pomos}]")
    try:
        choice = int(input("Enter task number: "))
        if choice in display_map:
            original_task_index = display_map[choice]
            return tasks[original_task_index]
        else:
            print(Fore.RED + "Invalid choice.")
            return None
    except ValueError:
        print(Fore.RED + "Invalid input. Please enter a number.")
        return None

def start_pomodoro_cycle(task):
    """Manages a full Pomodoro cycle (work/break) for the selected task."""
    if not task:
        return
    print(f"\nSelected Task: {task['title']}")
    pomodoro_count_session = 0
    while True:
        work_completed = run_timer(POMODORO_WORK_MINUTES, "Work")
        if work_completed:
            task['pomodoros_completed'] = task.get('pomodoros_completed', 0) + 1
            pomodoro_count_session += 1
            print(f"Pomodoro #{pomodoro_count_session} for '{task['title']}' completed! Total: {task['pomodoros_completed']}")
            if pomodoro_count_session % POMODOROS_BEFORE_LONG_BREAK == 0:
                print("\nTime for a long break!")
                run_timer(POMODORO_LONG_BREAK_MINUTES, "Long Break")
            else:
                print("\nTime for a short break!")
                run_timer(POMODORO_SHORT_BREAK_MINUTES, "Short Break")
            # Ask user if they want to continue
            try:
                 cont = input("\nStart next Pomodoro session for this task? (y/n): ").lower()
                 if cont != 'y':
                    break # Exit the cycle loop if user doesn't input 'y'
            except EOFError: # Handle cases where input stream is closed unexpectedly
                 break
        else:
            print("Pomodoro cycle interrupted.")
            break # Exit the cycle loop if work session was cancelled

def calculate_level(points):
    """Calculates the user's level based on their points and the level thresholds."""
    current_level = 1 # Default level
    for level, min_points in LEVEL_THRESHOLDS:
        if points >= min_points:
            current_level = level
        else:
            break # Since thresholds are sorted, no need to check further
    return current_level

# --- Main Application Loop ---
if __name__ == "__main__":
    user_id = ""
    while not user_id:
        user_id_raw = input("Enter your User ID (letters/numbers recommended): ").strip()
        if not user_id_raw:
            print(Fore.RED + "User ID cannot be empty.")
        else:
            # Use the raw ID for display, but cleaned version for filename
            user_id = user_id_raw

    all_tasks, user_data = load_tasks(user_id)

    while True:
        current_points = user_data.get('points', 0)
        current_level = calculate_level(current_points)
        # --- Apply Green color to the header ---
        header_string = f"\n===== Task Agenda Menu [User: {user_id}] [Level: {current_level}] [Points: {current_points}] ====="
        print(Fore.GREEN + Style.BRIGHT + header_string) # Use Bright Green
        # --- Options remain the same ---
        print("1. View Agenda")
        print("2. Add Task")
        print("3. Complete Task")
        print("4. Start Pomodoro for Task")
        print("5. Save & Exit")
        print("6. Exit Without Saving")

        choice = input("Enter your choice: ")

        if choice == '1':
            display_agenda(all_tasks)
        elif choice == '2':
            add_task(all_tasks)
        elif choice == '3':
            complete_task(all_tasks, user_data)
        elif choice == '4':
            selected_task = select_task_for_pomodoro(all_tasks)
            if selected_task:
                start_pomodoro_cycle(selected_task)
        elif choice == '5':
            # Use cleaned ID for saving
            save_tasks(all_tasks, user_data, user_id)
            print("Data saved. Exiting.")
            break
        elif choice == '6':
            print("Exiting without saving changes.")
            break
        else:
            print(Fore.RED + "Invalid choice, please try again.")