import datetime
import json
import os

TASKS_FILE = 'tasks.json'

def load_tasks():
    """Loads tasks from a JSON file."""
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, 'r') as f:
            tasks_data = json.load(f)
            # Convert date/time strings back to datetime objects
            for task in tasks_data:
                if task.get('due_datetime_str'):
                    task['due_datetime'] = datetime.datetime.fromisoformat(task['due_datetime_str'])
                else:
                    task['due_datetime'] = None # Handle tasks without specific time (All Day concept)
                # Ensure 'completed' key exists
                if 'completed' not in task:
                    task['completed'] = False
            return tasks_data
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading tasks: {e}. Starting with an empty list.")
        return []

def save_tasks(tasks):
    """Saves tasks to a JSON file."""
    try:
        # Prepare tasks for JSON serialization (convert datetime to string)
        tasks_to_save = []
        for task in tasks:
            task_copy = task.copy()
            if task_copy.get('due_datetime'):
                task_copy['due_datetime_str'] = task_copy['due_datetime'].isoformat()
            # Remove the actual datetime object before saving
            task_copy.pop('due_datetime', None)
            tasks_to_save.append(task_copy)

        with open(TASKS_FILE, 'w') as f:
            json.dump(tasks_to_save, f, indent=4)
    except IOError as e:
        print(f"Error saving tasks: {e}")

def display_agenda(tasks):
    """Sorts tasks and displays them grouped by day."""
    if not tasks:
        print("\nNo tasks in your agenda!")
        return

    # Separate tasks with and without specific due dates/times
    timed_tasks = [t for t in tasks if t.get('due_datetime')]
    all_day_tasks = [t for t in tasks if not t.get('due_datetime')] # Simplified: treat no date as 'unscheduled' for now

    # Sort timed tasks chronologically
    timed_tasks.sort(key=lambda x: x['due_datetime'])

    # Group tasks by day
    tasks_by_day = {}
    today = datetime.date.today()

    # Add timed tasks to groups
    for task in timed_tasks:
        task_date = task['due_datetime'].date()
        if task_date not in tasks_by_day:
            tasks_by_day[task_date] = []
        tasks_by_day[task_date].append(task)

    # Add all-day/unscheduled tasks conceptually (could refine grouping)
    # For simplicity here, we'll just list them separately after timed tasks
    # A better approach might group them under specific assigned dates if the model supported that

    print("\n--- Your Agenda ---")

    # Display tasks sorted by date
    sorted_dates = sorted(tasks_by_day.keys())

    for display_date in sorted_dates:
        # --- Date Header ---
        header = display_date.strftime('%A, %B %d, %Y') # e.g., Saturday, April 12, 2025
        if display_date == today:
            header = f"TODAY - {header}"
        elif display_date == today + datetime.timedelta(days=1):
            header = f"TOMORROW - {header}"
        print(f"\n--- {header} ---")

        # --- Tasks for the day ---
        for i, task in enumerate(tasks_by_day[display_date]):
            status = "[X]" if task.get('completed', False) else "[ ]"
            time_str = task['due_datetime'].strftime('%I:%M %p') # e.g., 10:30 AM
            title = task.get('title', 'No Title')
            project = f" ({task['project']})" if task.get('project') else ""
            priority = f" [P{task['priority']}]" if task.get('priority') else "" # P1, P2, P3 etc.
            print(f"  {status} {time_str.ljust(9)} {title}{project}{priority}") # Basic formatting

    # Display unscheduled tasks (tasks without a date/time)
    if all_day_tasks:
        print("\n--- Unscheduled / All Day Tasks ---")
        for i, task in enumerate(all_day_tasks):
             status = "[X]" if task.get('completed', False) else "[ ]"
             title = task.get('title', 'No Title')
             project = f" ({task['project']})" if task.get('project') else ""
             priority = f" [P{task['priority']}]" if task.get('priority') else ""
             print(f"  {status} {' '.ljust(9)} {title}{project}{priority}") # Use spaces for alignment


def add_task(tasks):
    """Prompts user for task details and adds it to the list."""
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
                # If only date is given, store it - maybe treat as 'All Day' for that date?
                # For now, storing just date part isn't fully supported by display logic easily.
                # Let's require time if date is given for this simple version, or handle it better in display
                 print("Warning: Time not specified. Task will be treated as unscheduled for now if time is missing.")
                 # Or: due_datetime = datetime.datetime.combine(date_part, datetime.time.min) # Start of day
        except ValueError:
            print("Invalid date or time format. Please use YYYY-MM-DD and HH:MM.")
            # Decide if task should still be added as unscheduled or abort
            # For simplicity, let's add it as unscheduled if date/time is invalid
            due_datetime = None


    priority = None
    if priority_str.isdigit():
        priority = int(priority_str)

    new_task = {
        "id": len(tasks) + 1, # Simple ID generation
        "title": title,
        "due_datetime": due_datetime,
        "project": project if project else None,
        "priority": priority,
        "completed": False
    }
    tasks.append(new_task)
    print("Task added successfully!")

def complete_task(tasks):
    """Lists incomplete tasks and marks the selected one as complete."""
    print("\n--- Mark Task as Complete ---")
    incomplete_tasks = [(i, task) for i, task in enumerate(tasks) if not task.get('completed', False)]

    if not incomplete_tasks:
        print("No tasks to complete!")
        return

    # Display only incomplete tasks for selection
    # Sort them by due date for easier identification
    incomplete_tasks.sort(key=lambda item: item[1].get('due_datetime') or datetime.datetime.max)

    print("Select task to mark as complete:")
    display_map = {} # Map display index to original task index
    for display_index, (original_index, task) in enumerate(incomplete_tasks):
        display_map[display_index] = original_index
        due_str = task['due_datetime'].strftime('%Y-%m-%d %H:%M') if task.get('due_datetime') else "No date"
        print(f"  {display_index}: {task['title']} ({due_str})")

    try:
        choice = int(input("Enter task number: "))
        if choice in display_map:
            original_task_index = display_map[choice]
            tasks[original_task_index]['completed'] = True
            print(f"Task '{tasks[original_task_index]['title']}' marked as complete.")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input. Please enter a number.")


# --- Main Application Loop ---
if __name__ == "__main__":
    all_tasks = load_tasks()

    while True:
        print("\n===== Task Agenda Menu =====")
        print("1. View Agenda")
        print("2. Add Task")
        print("3. Complete Task")
        print("4. Save & Exit")
        print("5. Exit Without Saving")

        choice = input("Enter your choice: ")

        if choice == '1':
            display_agenda(all_tasks)
        elif choice == '2':
            add_task(all_tasks)
        elif choice == '3':
            complete_task(all_tasks)
        elif choice == '4':
            save_tasks(all_tasks)
            print("Tasks saved. Exiting.")
            break
        elif choice == '5':
            print("Exiting without saving.")
            break
        else:
            print("Invalid choice, please try again.")