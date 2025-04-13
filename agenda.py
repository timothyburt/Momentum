import datetime
import json
import os
import time
import sys
import re

# --- Configuration ---
POMODORO_WORK_MINUTES = 25
POMODORO_SHORT_BREAK_MINUTES = 5
POMODORO_LONG_BREAK_MINUTES = 15
POMODOROS_BEFORE_LONG_BREAK = 4
POINTS_PER_TASK = 10  # Points awarded for completing a task

# --- Leveling System ---
# Tiered level thresholds: (level, minimum_points)
LEVEL_THRESHOLDS = [
    (1, 0),
    (2, 100),
    (3, 250),
    (4, 500),
    (5, 1000),
    (6, 2000),
    (7, 3500),
    (8, 5500),
    (9, 8000),
    (10, 11000),
    (11, 15000),
    (12, 20000),
]  # Add more levels as desired, ensure they are sorted by points

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

    default_user_info = {"userid": userid, "points": 0}

    if not os.path.exists(filename):
        print("No existing data file found for this user. Starting fresh.")
        return [], default_user_info

    try:
        with open(filename, 'r') as f:
            data = json.load(f)

            if isinstance(data, dict) and "tasks" in data and "user_info" in data:
                tasks_data = data.get("tasks", [])
                user_info = data.get("user_info", default_user_info)
                if "points" not in user_info:
                    user_info["points"] = 0
                if "userid" not in user_info:
                    user_info["userid"] = userid
            elif isinstance(data, list):
                print("Old tasks format detected. Converting and initializing points to 0.")
                tasks_data = data
                user_info = default_user_info
            else:
                print("Warning: Unknown data format in file. Starting fresh.")
                return [], default_user_info

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
                processed_tasks.append(task)

            print(f"Loaded {len(processed_tasks)} tasks. Current points: {user_info.get('points', 0)}")
            return processed_tasks, user_info

    except (json.JSONDecodeError, IOError, TypeError) as e:
        print(f"Error loading data from {filename}: {e}. Starting with an empty list and 0 points.")
        return [], default_user_info

def save_tasks(tasks, user_info, userid):
    """Saves tasks and user info to a user-specific JSON file."""
    filename = clean_filename(userid)
    print(f"--- Saving data for user '{userid}' to {filename} ---")

    try:
        tasks_to_save = []
        for task in tasks:
            task_copy = task.copy()
            if task_copy.get('due_datetime'):
                task_copy['due_datetime_str'] = task_copy['due_datetime'].isoformat()
            task_copy.pop('due_datetime', None)
            if 'pomodoros_completed' not in task_copy:
                 task_copy['pomodoros_completed'] = 0
            tasks_to_save.append(task_copy)

        data_to_save = {
            "user_info": user_info,
            "tasks": tasks_to_save
        }

        with open(filename, 'w') as f:
            json.dump(data_to_save, f, indent=4)
        print(f"Saved {len(tasks_to_save)} tasks. Points: {user_info.get('points', 0)}")

    except IOError as e:
        print(f"Error saving data to {filename}: {e}")

# --- display_agenda, add_task ---
# (These functions remain unchanged)
# --- [Paste unchanged display_agenda and add_task here] ---
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
        header = display_date.strftime('%A, %B %d, %Y') # e.g., Saturday, April 12, 2025
        if display_date == today:
            header = f"TODAY - {header}"
        elif display_date == today + datetime.timedelta(days=1):
            header = f"TOMORROW - {header}"
        print(f"\n--- {header} ---")

        for i, task in enumerate(tasks_by_day[display_date]):
            status = "[X]" if task.get('completed', False) else "[ ]"
            time_str = task['due_datetime'].strftime('%I:%M %p') if task.get('due_datetime') else "All Day" # Handle All Day display
            title = task.get('title', 'No Title')
            project = f" ({task['project']})" if task.get('project') else ""
            priority = f" [P{task['priority']}]" if task.get('priority') else ""
            pomos = f" (Pomos: {task.get('pomodoros_completed', 0)})"
            print(f"  {status} {time_str.ljust(9)} {title}{project}{priority}{pomos}") # Adjusted ljust slightly

    if all_day_tasks:
        print("\n--- Unscheduled / All Day Tasks ---")
        for i, task in enumerate(all_day_tasks):
             status = "[X]" if task.get('completed', False) else "[ ]"
             title = task.get('title', 'No Title')
             project = f" ({task['project']})" if task.get('project') else ""
             priority = f" [P{task['priority']}]" if task.get('priority') else ""
             pomos = f" (Pomos: {task.get('pomodoros_completed', 0)})"
             # Use a placeholder for time alignment or adjust formatting
             print(f"  {status} {'No Date'.ljust(9)} {title}{project}{priority}{pomos}")


def add_task(tasks):
    """Prompts user for task details and adds it, initializing pomodoro count."""
    print("\n--- Add New Task ---")
    title = input("Task Title: ")
    if not title:
        print("Task title cannot be empty.")
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
                 # Task has a date but no specific time - treat as 'All Day' conceptually
                 # We store None for due_datetime here to group it with unscheduled/all day
                 # Alternatively, store date with min time: datetime.datetime.combine(date_part, datetime.time.min)
                 # For simplicity with current display logic, let's keep it None if time is missing
                 print("Info: Date specified without time. Task treated as 'All Day'/Unscheduled.")
                 due_datetime = None # Set to None if only date provided
        except ValueError:
            print("Invalid date or time format. Task treated as unscheduled.")
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
    print("Task added successfully!")

# --- complete_task (Modified for Points and Leveling) ---
def complete_task(tasks, user_info):
    """Lists incomplete tasks, marks the selected one as complete, and handles points/leveling."""
    print("\n--- Mark Task as Complete ---")
    incomplete_tasks = [(i, task) for i, task in enumerate(tasks) if not task.get('completed', False)]

    if not incomplete_tasks:
        print("No tasks to complete!")
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

                print(f"\nTask '{tasks[original_task_index]['title']}' marked as complete.")
                print(f"Congratulations! You earned {points_earned} points.")
                print(f"Total points: {new_points}")

                if new_level > old_level:
                    print(f"🎉🎉🎉 Level Up! 🎉🎉🎉  You are now Level {new_level}!")
            else:
                print(f"Task '{tasks[original_task_index]['title']}' was already complete.")

        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input. Please enter a number.")

# --- run_timer, select_task_for_pomodoro, start_pomodoro_cycle ---
# (These functions remain unchanged)
# --- [Paste unchanged Pomodoro functions here] ---
def run_timer(minutes, session_type="Work"):
    """Runs a countdown timer for the specified minutes."""
    total_seconds = minutes * 60
    cancelled = False
    print(f"\nStarting {session_type} session ({minutes} minutes). Press Ctrl+C to cancel.")
    try:
        while total_seconds > 0:
            mins, secs = divmod(total_seconds, 60)
            timer_display = f"{session_type}: {mins:02d}:{secs:02d}".ljust(25)
            print(f"\r{timer_display}", end="")
            sys.stdout.flush()
            time.sleep(1)
            total_seconds -= 1
        print("\r" + f"{session_type} session finished!".ljust(25))
    except KeyboardInterrupt:
        print("\r" + f"{session_type} session cancelled.".ljust(25))
        cancelled = True
    if not cancelled:
        print("\a") # Alert Bell
    return not cancelled

def select_task_for_pomodoro(tasks):
    """Lists incomplete tasks and lets the user choose one to work on."""
    print("\n--- Start Pomodoro Session ---")
    incomplete_tasks = [(i, task) for i, task in enumerate(tasks) if not task.get('completed', False)]
    if not incomplete_tasks:
        print("No incomplete tasks to start a Pomodoro for!")
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
            print("Invalid choice.")
            return None
    except ValueError:
        print("Invalid input. Please enter a number.")
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
            cont = input("\nStart next Pomodoro session for this task? (y/n): ").lower()
            if cont != 'y':
                break
        else:
            print("Pomodoro cycle interrupted.")
            break
# --- End of pasted functions ---

def calculate_level(points):
    """Calculates the user's level based on their points and the level thresholds."""
    for level, min_points in reversed(LEVEL_THRESHOLDS):
        if points >= min_points:
            return level
    return 1  # Default to Level 1 if points are below the lowest threshold (shouldn't happen with our thresholds, but safe)

# --- Main Application Loop (Updated for User Info, Points, and Level) ---
if __name__ == "__main__":
    user_id = ""
    while not user_id:
        user_id = input("Enter your User ID (letters/numbers recommended): ").strip()
        if not user_id:
            print("User ID cannot be empty.")

    all_tasks, user_data = load_tasks(user_id)

    while True:
        current_points = user_data.get('points', 0)
        current_level = calculate_level(current_points) # Calculate level *every time* we display the menu
        print(f"\n===== Task Agenda Menu [User: {user_id}] [Level: {current_level}] [Points: {current_points}] =====")
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
            complete_task(all_tasks, user_data) # Pass user_data
        elif choice == '4':
            selected_task = select_task_for_pomodoro(all_tasks)
            if selected_task:
                start_pomodoro_cycle(selected_task)
        elif choice == '5':
            save_tasks(all_tasks, user_data, user_id) # Pass user_data
            print("Data saved. Exiting.")
            break
        elif choice == '6':
            print("Exiting without saving changes.")
            break
        else:
            print("Invalid choice, please try again.")