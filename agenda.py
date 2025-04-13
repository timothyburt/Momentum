# --- Imports ---
import datetime
import json
import os
import re
import sys
import time

# Third-party imports
import colorama
from colorama import Back, Fore, Style, init

# --- Initialize Colorama ---
# init(autoreset=True) automatically resets the style after each print
init(autoreset=True)


# --- Configuration Constants ---
class Config:
    """Groups configuration constants for the application."""

    POMODORO_WORK_MINUTES = 25
    POMODORO_SHORT_BREAK_MINUTES = 5
    POMODORO_LONG_BREAK_MINUTES = 15
    POMODOROS_BEFORE_LONG_BREAK = 4
    POINTS_PER_TASK = 10
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
    ]
    # Task Status Constants
    STATUS_TODO = "Todo"
    STATUS_IN_PROGRESS = "In Progress"
    STATUS_COMPLETED = "Completed"
    VALID_STATUSES = [STATUS_TODO, STATUS_IN_PROGRESS, STATUS_COMPLETED]
    STATUS_DISPLAY_MAP = {
        STATUS_TODO: Fore.WHITE + "[Todo]",
        STATUS_IN_PROGRESS: Fore.YELLOW + "[Prog]",
        STATUS_COMPLETED: Fore.LIGHTBLACK_EX + "[Done]",  # Dim completed
    }
    STATUS_COLOR_MAP = {  # For dimming the whole line
        STATUS_TODO: "",
        STATUS_IN_PROGRESS: "",
        STATUS_COMPLETED: Fore.LIGHTBLACK_EX,
    }


# --- Utility Functions ---
def print_error(message):
    """Prints an error message in red."""
    print(Fore.RED + message)


def print_success(message):
    """Prints a success message in green."""
    print(Fore.GREEN + message)


def print_warning(message):
    """Prints a warning message in yellow."""
    print(Fore.YELLOW + message)


def print_info(message):
    """Prints an informational message in cyan."""
    print(Fore.CYAN + message)


def clean_filename(text_id):
    """Cleans a string to create a safe filename component."""
    text_id = str(text_id).lower()  # Ensure string conversion
    text_id = re.sub(r"[^\w\-]+", "", text_id)
    if not text_id:
        text_id = "default"
    return f"tasks_{text_id}.json"


# --- Task Class ---
class Task:
    """Represents a single task with status."""

    def __init__(
        self,
        id,
        title,
        due_datetime=None,
        project=None,
        priority=None,
        status=Config.STATUS_TODO,
        pomos_completed=0,
    ):
        self.id = id if id else int(time.time() * 1000 + pomos_completed)
        self.title = title
        self.due_datetime = due_datetime
        self.project = project
        self.priority = priority
        # Ensure status is valid, default to Todo if not
        self.status = (
            status if status in Config.VALID_STATUSES else Config.STATUS_TODO
        )
        self.pomodoros_completed = pomos_completed

    def set_status(self, new_status):
        """Sets the task status if valid and changed. Returns True if changed."""
        if new_status in Config.VALID_STATUSES and self.status != new_status:
            self.status = new_status
            return True
        return False

    def to_dict(self):
        """Converts task object to a dictionary for JSON serialization."""
        due_str = (
            self.due_datetime.isoformat() if self.due_datetime else None
        )
        return {
            "id": self.id,
            "title": self.title,
            "due_datetime_str": due_str,
            "project": self.project,
            "priority": self.priority,
            "status": self.status,
            "pomodoros_completed": self.pomodoros_completed,
        }

    @classmethod
    def from_dict(cls, data):
        """Creates a Task object from a dictionary, handling migration."""
        due_datetime = None
        due_datetime_str = data.get("due_datetime_str")
        if due_datetime_str:
            try:
                due_datetime = datetime.datetime.fromisoformat(
                    due_datetime_str
                )
            except (ValueError, TypeError):
                due_datetime = None  # Handle invalid format gracefully

        # --- Status Migration Logic ---
        status = data.get("status")
        if status is None:  # Check if old 'completed' field exists
            if data.get("completed", False):
                status = Config.STATUS_COMPLETED
            else:
                status = Config.STATUS_TODO
        # --- End Migration Logic ---

        # Ensure status is valid after migration or loading
        if status not in Config.VALID_STATUSES:
            status = Config.STATUS_TODO

        return cls(
            id=data.get("id"),
            title=data.get("title", "Untitled Task"),
            due_datetime=due_datetime,
            project=data.get("project"),
            priority=data.get("priority"),
            status=status,
            pomos_completed=data.get("pomodoros_completed", 0),
        )

    def __str__(self):
        """String representation for display using status."""
        status_display = Config.STATUS_DISPLAY_MAP.get(
            self.status, "[????]"
        )  # Get colored status abbreviation
        time_str = (
            self.due_datetime.strftime("%I:%M %p")
            if self.due_datetime
            else "All Day"
        )
        project_str = f" ({self.project})" if self.project else ""
        priority_str = f" [P{self.priority}]" if self.priority else ""
        pomos_str = f" (Pomos: {self.pomodoros_completed})"
        # Apply dimming color to the whole line if completed
        line_color = Config.STATUS_COLOR_MAP.get(self.status, "")
        task_line = (
            f"  {status_display} {time_str.ljust(9)} {self.title}"
            f"{project_str}{priority_str}{pomos_str}"
        )
        # Need to reset color specifically if dimming
        reset_code = Style.RESET_ALL if line_color else ""
        return line_color + task_line + reset_code

    def __repr__(self):
        """Official representation of the Task object."""
        return (
            f"Task(id={self.id}, title='{self.title}', "
            f"status='{self.status}')"
        )


# --- User Class ---
class User:
    """Represents the user and manages their tasks and points."""

    def __init__(self, userid, points=0, tasks=None):
        self.userid = userid
        self.points = points
        self.tasks = tasks if tasks is not None else []  # List of Task objects

    def add_task(self, task):
        """Adds a Task object to the user's list."""
        self.tasks.append(task)

    def remove_task(self, task_id):
        """Removes a task by its ID. Returns True if removed."""
        initial_len = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.id != task_id]
        return len(self.tasks) < initial_len

    def get_task_by_id(self, task_id):
        """Finds a task by its ID."""
        return next((t for t in self.tasks if t.id == task_id), None)

    def get_completed_tasks(self):
        """Returns a sorted list of completed tasks."""
        return sorted(
            [t for t in self.tasks if t.status == Config.STATUS_COMPLETED],
            key=lambda task: task.title.lower(),
        )

    def get_incomplete_tasks(self):
        """Returns a sorted list of incomplete tasks."""
        return sorted(
            [t for t in self.tasks if t.status != Config.STATUS_COMPLETED],
            key=lambda task: (
                task.due_datetime or datetime.datetime.max,
                task.title.lower(),
            ),
        )

    def award_points(self, amount):
        """Adds points to the user's score."""
        if amount > 0:
            self.points += amount

    def calculate_level(self):
        """Calculates the user's level based on their points."""
        current_level = 1
        for level, min_points in Config.LEVEL_THRESHOLDS:
            if self.points >= min_points:
                current_level = level
            else:
                # Since thresholds are sorted, no need to check further
                break
        return current_level

    def to_dict(self):
        """Converts user data to a dictionary for saving."""
        return {
            "user_info": {"userid": self.userid, "points": self.points},
            "tasks": [task.to_dict() for task in self.tasks],
        }

    @classmethod
    def from_dict(cls, data, default_userid):
        """Creates a User object from loaded dictionary data."""
        user_info = data.get("user_info", {})
        userid = user_info.get("userid", default_userid)
        points = user_info.get("points", 0)
        tasks_data = data.get("tasks", [])
        tasks = [Task.from_dict(task_data) for task_data in tasks_data]
        return cls(userid, points, tasks)


# --- Data Persistence Class ---
class DataManager:
    """Handles loading and saving user data."""

    DATA_DIR = "."  # Store data in the current directory

    @staticmethod
    def get_user_filepath(userid):
        """Constructs the filepath for a given userid."""
        # Use the potentially raw userid for filename generation via clean_filename
        filename = clean_filename(userid)
        return os.path.join(DataManager.DATA_DIR, filename)

    @staticmethod
    def load_user(userid_raw):
        """Loads user data, returns a User object."""
        filepath = DataManager.get_user_filepath(userid_raw)
        print(f"--- Loading data for user '{userid_raw}' from {filepath} ---")

        if not os.path.exists(filepath):
            print_warning(
                "No existing data file found for this user. Starting fresh."
            )
            return User(userid_raw)  # Return new user with the raw ID

        try:
            with open(filepath, "r") as f:
                data = json.load(f)

            # Check format and create User object
            if isinstance(data, dict) and (
                "user_info" in data or "tasks" in data
            ):
                user = User.from_dict(data, userid_raw)
                # Ensure user object has the ID they logged in with
                user.userid = userid_raw
                print_success(
                    f"Loaded {len(user.tasks)} tasks. "
                    f"Current points: {user.points}"
                )
                return user
            elif isinstance(data, list):  # Handle old list-only format
                print_warning(
                    "Old tasks format detected. "
                    "Converting and initializing points to 0."
                )
                tasks = [Task.from_dict(task_data) for task_data in data]
                return User(userid_raw, points=0, tasks=tasks)
            else:
                # Unknown format
                print_warning("Unknown data format in file. Starting fresh.")
                return User(userid_raw)

        except (json.JSONDecodeError, IOError, TypeError, KeyError) as e:
            print_error(
                f"Error loading data from {filepath}: {e}. Starting fresh."
            )
            return User(userid_raw)

    @staticmethod
    def save_user(user):
        """Saves the User object's data to a file."""
        # Use the user object's ID for saving (should be the raw one)
        filepath = DataManager.get_user_filepath(user.userid)
        print(f"--- Saving data for user '{user.userid}' to {filepath} ---")
        try:
            data_to_save = user.to_dict()
            # Ensure data directory exists (optional, useful if DATA_DIR changes)
            # os.makedirs(DataManager.DATA_DIR, exist_ok=True)
            with open(filepath, "w") as f:
                json.dump(data_to_save, f, indent=4)
            print_success(
                f"Saved {len(user.tasks)} tasks. Points: {user.points}"
            )
        except IOError as e:
            print_error(f"Error saving data to {filepath}: {e}")
        except Exception as e:
            print_error(f"An unexpected error occurred during save: {e}")

    @staticmethod
    def delete_user_file(userid):
        """Deletes the user's data file."""
        filepath = DataManager.get_user_filepath(userid)
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                print_success(
                    f"Data file {filepath} deleted successfully."
                )
                return True
            except OSError as e:
                print_error(f"Error deleting file {filepath}: {e}")
                return False
        else:
            print_warning(
                f"Data file {filepath} not found. Nothing to delete."
            )
            return False


# --- Core Application Logic Functions ---
def display_agenda(user):
    """Displays the user's task agenda using status."""
    tasks = user.tasks
    if not tasks:
        print("\nNo tasks in your agenda!")
        return

    incomplete_tasks = user.get_incomplete_tasks()
    completed_tasks = user.get_completed_tasks()

    timed_tasks = sorted(
        [t for t in incomplete_tasks if t.due_datetime],
        key=lambda x: x.due_datetime,
    )
    all_day_or_unscheduled = sorted(
        [t for t in incomplete_tasks if not t.due_datetime],
        key=lambda x: x.title.lower(),
    )

    tasks_by_day = {}
    today = datetime.date.today()
    for task in timed_tasks:
        task_date = task.due_datetime.date()
        if task_date not in tasks_by_day:
            tasks_by_day[task_date] = []
        tasks_by_day[task_date].append(task)

    print("\n--- Your Agenda ---")
    sorted_dates = sorted(tasks_by_day.keys())

    # Display Timed Incomplete tasks by Date
    for display_date in sorted_dates:
        header_str = display_date.strftime("%A, %B %d, %Y")
        if display_date == today:
            header_str = f"TODAY - {header_str}"
        elif display_date == today + datetime.timedelta(days=1):
            header_str = f"TOMORROW - {header_str}"
        print(Style.BRIGHT + f"\n--- {header_str} ---")
        for task in tasks_by_day[display_date]:
            print(task)  # Use Task.__str__

    # Display All Day / Unscheduled Incomplete tasks
    if all_day_or_unscheduled:
        print(Style.BRIGHT + "\n--- Unscheduled / All Day Tasks ---")
        for task in all_day_or_unscheduled:
            print(task)

    # Display Completed tasks separately at the end
    if completed_tasks:
        print(Style.BRIGHT + Fore.LIGHTBLACK_EX + "\n--- Completed Tasks ---")
        for task in completed_tasks:
            print(task)


def add_task_interaction(user):
    """Handles the user interaction for adding a new task."""
    print("\n--- Add New Task ---")
    title = input("Task Title: ").strip()
    if not title:
        print_error("Task title cannot be empty.")
        return

    due_date_str = input("Due Date (YYYY-MM-DD) or leave blank: ").strip()
    due_time_str = input("Due Time (HH:MM) or leave blank: ").strip()
    project = input("Project/Category (optional): ").strip()
    priority_str = input(
        "Priority (1=High, 2=Med, 3=Low - optional): "
    ).strip()

    due_datetime = None
    if due_date_str:
        try:
            date_part = datetime.datetime.strptime(
                due_date_str, "%Y-%m-%d"
            ).date()
            if due_time_str:
                time_part = datetime.datetime.strptime(
                    due_time_str, "%H:%M"
                ).time()
                due_datetime = datetime.datetime.combine(date_part, time_part)
            else:
                print_warning(
                    "Date specified without time. Treating as unscheduled."
                )
                due_datetime = None
        except ValueError:
            print_error(
                "Invalid date or time format. Task treated as unscheduled."
            )
            due_datetime = None

    priority = None
    if priority_str.isdigit():
        priority_val = int(priority_str)
        if 1 <= priority_val <= 3:
            priority = priority_val
        else:
            print_warning("Priority must be between 1 and 3. Ignoring.")
    elif priority_str:
        # Only warn if non-empty invalid input was given
        print_warning("Invalid priority value. Ignoring.")

    # Status defaults to Todo in Task constructor
    new_task = Task(
        id=None,
        title=title,
        due_datetime=due_datetime,
        project=project if project else None,
        priority=priority,
    )
    user.add_task(new_task)
    print_success("Task added successfully!")


def prompt_select_tasks(
    task_list, prompt_message, allow_multiple=False, allow_cancel=True
):
    """Displays tasks and prompts for selection. Returns list of Task objects or None."""
    if not task_list:
        print_warning("No tasks available for selection.")
        return None

    print(prompt_message)
    display_map = {}  # display index -> task object
    for i, task in enumerate(task_list):
        display_map[i] = task
        status_str = Config.STATUS_DISPLAY_MAP.get(task.status, task.status)
        print(f"  {i}: {task.title} ({status_str})")

    cancel_prompt = " (or 'c' to cancel)" if allow_cancel else ""
    input_prompt = (
        f"Enter number{'s (e.g., 0, 2)' if allow_multiple else ''}"
        f"{cancel_prompt}: "
    )
    choice_str = input(input_prompt).strip()

    if allow_cancel and choice_str.lower() == "c":
        print("Operation cancelled.")
        return None
    if not choice_str:
        print_warning("No selection made.")
        return None

    selected_tasks = []
    invalid_inputs = []
    chosen_display_indices = set()

    if allow_multiple:
        parts = choice_str.split(",")
        for part in parts:
            part = part.strip()
            if not part:
                continue  # Skip empty parts like in "1,,2"
            if part.isdigit():
                idx = int(part)
                if idx in display_map:
                    chosen_display_indices.add(idx)
                else:
                    invalid_inputs.append(f"'{part}' (out of range)")
            else:
                invalid_inputs.append(f"'{part}' (not a number)")
        # Only proceed if there were no invalid inputs
        if not invalid_inputs:
            selected_tasks = [
                display_map[idx] for idx in sorted(list(chosen_display_indices))
            ]

    else:  # Single selection
        if choice_str.isdigit():
            idx = int(choice_str)
            if idx in display_map:
                selected_tasks = [display_map[idx]]
            else:
                invalid_inputs.append(f"'{choice_str}' (out of range)")
        else:
            invalid_inputs.append(f"'{choice_str}' (not a number)")

    if invalid_inputs:
        print_error(
            "Invalid input detected: " + ", ".join(invalid_inputs)
        )
        return None  # Indicate error

    if not selected_tasks:
        print_warning("No valid tasks selected.")
        return None

    return selected_tasks


def complete_task_interaction(user):
    """Handles interaction for setting tasks to 'Completed' status."""
    print("\n--- Mark Task(s) as Complete ---")
    tasks_to_complete = prompt_select_tasks(
        user.get_incomplete_tasks(),
        "Select task(s) to mark as complete:",
        allow_multiple=True,
        allow_cancel=True,
    )
    if not tasks_to_complete:
        return

    print("\nYou selected:")
    for task in tasks_to_complete:
        print(f"- {task.title}")
    confirm = input(
        Fore.YELLOW
        + f"Mark these {len(tasks_to_complete)} tasks as "
        f"'{Config.STATUS_COMPLETED}'? (y/n): "
    ).lower()
    if confirm != "y":
        print("Completion cancelled.")
        return

    tasks_completed_count = 0
    total_points_earned = 0
    old_level = user.calculate_level()
    for task in tasks_to_complete:
        if task.set_status(Config.STATUS_COMPLETED):
            total_points_earned += Config.POINTS_PER_TASK
            tasks_completed_count += 1

    if tasks_completed_count > 0:
        user.award_points(total_points_earned)
        new_level = user.calculate_level()
        print_success(
            f"\nSet {tasks_completed_count} task(s) to "
            f"'{Config.STATUS_COMPLETED}'."
        )
        print_info(f"You earned {total_points_earned} points.")
        print(f"Total points: {user.points}")
        if new_level > old_level:
            print(Fore.GREEN + Style.BRIGHT + f"\n🎉🎉🎉 Level Up! 🎉🎉🎉")
            print(
                Fore.GREEN + Style.BRIGHT + f"You are now Level {new_level}!"
            )
    else:
        print_warning("No tasks were newly marked as complete.")


def change_task_status_interaction(user):
    """Allows changing status between Todo and In Progress."""
    print("\n--- Change Task Status ---")
    tasks_to_change = prompt_select_tasks(
        user.get_incomplete_tasks(),  # Select from non-completed tasks
        "Select task to change status:",
        allow_multiple=False,
        allow_cancel=True,
    )

    if not tasks_to_change:
        return

    selected_task = tasks_to_change[0]
    current_status = selected_task.status
    next_status = None

    # Determine the next logical status
    if current_status == Config.STATUS_TODO:
        next_status = Config.STATUS_IN_PROGRESS
    elif current_status == Config.STATUS_IN_PROGRESS:
        next_status = Config.STATUS_TODO
    else:
        # Should not happen if selecting from incomplete tasks
        print_warning(
            f"Task '{selected_task.title}' has status '{current_status}'. "
            "Can only toggle Todo/In Progress here."
        )
        return

    confirm = input(
        Fore.YELLOW
        + f"Change status of '{selected_task.title}' from "
        f"'{current_status}' to '{next_status}'? (y/n): "
    ).lower()

    if confirm == "y":
        if selected_task.set_status(next_status):
            print_success(
                f"Task '{selected_task.title}' status changed to '{next_status}'."
            )
        else:
            print_error("Failed to change task status.")
    else:
        print("Status change cancelled.")


def delete_single_completed_task_interaction(user):
    """Handles deleting a single task with 'Completed' status."""
    print("\n--- Delete a Completed Task ---")
    task_to_delete = prompt_select_tasks(
        user.get_completed_tasks(),
        "Select a completed task to delete:",
        allow_multiple=False,
        allow_cancel=True,
    )
    if not task_to_delete:
        return
    selected_task = task_to_delete[0]
    confirm = input(
        Fore.YELLOW
        + f"Are you sure you want to permanently delete "
        f"'{selected_task.title}'? (y/n): "
    ).lower()
    if confirm == "y":
        if user.remove_task(selected_task.id):
            print_success(
                f"Task '{selected_task.title}' deleted successfully."
            )
        else:
            print_error("Error: Could not delete the task.")
    else:
        print("Deletion cancelled.")


def delete_all_completed_tasks_interaction(user):
    """Handles deleting all tasks with 'Completed' status."""
    print("\n--- Delete ALL Completed Tasks ---")
    completed_tasks = user.get_completed_tasks()
    num_completed = len(completed_tasks)

    if num_completed == 0:
        print_warning("No completed tasks found to delete.")
        return

    print_warning(
        Style.BRIGHT
        + f"Warning: You are about to delete {num_completed} completed task(s)."
    )
    confirm = input(
        Fore.YELLOW
        + "This action cannot be undone. Are you absolutely sure? (yes/no): "
    ).lower()

    if confirm == "yes": # Require explicit "yes"
        deleted_count = 0
        ids_to_delete = [task.id for task in completed_tasks]
        for task_id in ids_to_delete:
            if user.remove_task(task_id):
                deleted_count += 1
        if deleted_count > 0:
            print_success(
                f"Successfully deleted {deleted_count} completed task(s)."
            )
        else:
            print_warning("No tasks were deleted.")
    else:
        print("Deletion cancelled.")


def pomodoro_interaction(user):
    """Handles selecting an incomplete task and starting a Pomodoro cycle."""
    print("\n--- Start Pomodoro Session ---")
    task_to_work_on = prompt_select_tasks(
        user.get_incomplete_tasks(),
        "Select task to work on:",
        allow_multiple=False,
        allow_cancel=True,
    )
    if not task_to_work_on:
        return
    selected_task = task_to_work_on[0]
    start_pomodoro_cycle(selected_task)


def run_timer(minutes, session_type="Work"):
    """Runs a countdown timer."""
    total_seconds = minutes * 60
    cancelled = False
    color = Fore.CYAN if session_type == "Work" else Fore.MAGENTA
    print(
        color
        + f"\nStarting {session_type} session ({minutes} minutes). "
        f"Press Ctrl+C to cancel."
    )
    try:
        while total_seconds >= 0:  # Display 00:00 before finishing
            mins, secs = divmod(total_seconds, 60)
            timer_display = f"{session_type}: {mins:02d}:{secs:02d}".ljust(25)
            # Use \r to return to the beginning of the line
            print(color + f"\r{timer_display}", end="")
            sys.stdout.flush()  # Force output flushing
            if total_seconds == 0:
                break # Finish after displaying 00:00
            time.sleep(1)
            total_seconds -= 1
        # Clear line before printing finish message
        print(color + "\r" + " " * 30 + "\r", end="")
        print(color + f"{session_type} session finished!")
    except KeyboardInterrupt:
        # Clear line before printing cancel message
        print(Fore.YELLOW + "\r" + " " * 30 + "\r", end="")
        print(Fore.YELLOW + f"{session_type} session cancelled.")
        cancelled = True

    # Ring bell only if completed normally
    if not cancelled:
        print("\a", end="")  # ASCII Bell character

    return not cancelled


def start_pomodoro_cycle(task):
    """Manages a full Pomodoro cycle, operating on the Task object."""
    if not task:
        return

    print(f"\nSelected Task: {task.title}")
    pomodoro_count_session = 0
    status_changed_by_pomo = False

    # Optionally set status to In Progress when starting
    if task.status == Config.STATUS_TODO:
        if task.set_status(Config.STATUS_IN_PROGRESS):
            print_info(f"Task status set to '{Config.STATUS_IN_PROGRESS}'.")
            status_changed_by_pomo = True

    while True:
        work_completed = run_timer(Config.POMODORO_WORK_MINUTES, "Work")
        if work_completed:
            task.pomodoros_completed += 1
            pomodoro_count_session += 1
            print(
                f"Pomodoro #{pomodoro_count_session} for '{task.title}' "
                f"completed! Total: {task.pomodoros_completed}"
            )

            # Determine break type
            if (
                pomodoro_count_session % Config.POMODOROS_BEFORE_LONG_BREAK
                == 0
            ):
                print("\nTime for a long break!")
                run_timer(Config.POMODORO_LONG_BREAK_MINUTES, "Long Break")
            else:
                print("\nTime for a short break!")
                run_timer(Config.POMODORO_SHORT_BREAK_MINUTES, "Short Break")

            # Ask to continue
            try:
                cont = input(
                    "\nStart next Pomodoro session for this task? (y/n): "
                ).lower()
                if cont != "y":
                    break  # Exit cycle loop
            except EOFError:
                break  # Exit if input stream closes

        else:  # Work session was cancelled
            print("Pomodoro cycle interrupted.")
            # Optionally revert status if auto-set and cancelled?
            if status_changed_by_pomo and task.status == Config.STATUS_IN_PROGRESS:
                task.set_status(Config.STATUS_TODO)
                print_info(f"Task status reverted to '{Config.STATUS_TODO}'.")
            break  # Exit cycle loop


def delete_user_data_interaction(user):
    """Handles the interaction for deleting the current user's data file."""
    print(
        "\n"
        + Fore.RED
        + Style.BRIGHT
        + "--- !!! DANGER ZONE: DELETE USER DATA !!! ---"
    )
    print(
        Fore.YELLOW
        + f"This action will permanently delete all tasks, points, and level "
        f"progress associated with the User ID '{user.userid}'."
    )
    print(Fore.YELLOW + Style.BRIGHT + "This operation cannot be undone.")

    confirm1 = input(
        Fore.YELLOW + "Are you absolutely sure you want to proceed? (yes/no): "
    ).lower()

    if confirm1 == "yes":
        print(
            Fore.YELLOW
            + "\nFor final confirmation, please type your User ID exactly:"
        )
        confirm_userid = input(
            f"Type '{user.userid}' to confirm deletion: "
        ).strip()

        if confirm_userid == user.userid:
            print(Fore.RED + "\nDeleting user data file...")
            if DataManager.delete_user_file(user.userid):
                print_success(
                    f"All data for user '{user.userid}' has been deleted."
                )
                print("Exiting application.")
                sys.exit(0)  # Exit cleanly after deletion
            else:
                # Error message already printed by delete_user_file
                print_error(
                    "Deletion failed. Please check permissions or file status."
                )
                # Allow the app to continue for now
        else:
            print_error("User ID mismatch. Deletion cancelled.")
    else:
        print("Deletion cancelled.")


# --- Main Application Execution ---
def main():
    """Main function to run the application."""
    user_id_raw = ""
    while not user_id_raw:
        user_id_raw = input(
            "Enter your User ID (letters/numbers recommended): "
        ).strip()
        if not user_id_raw:
            print_error("User ID cannot be empty.")

    # Load user data using DataManager, using the raw ID provided
    user = DataManager.load_user(user_id_raw)

    # Define menu structure
    menu_options = {
        "1": ("View Agenda", display_agenda),
        "2": ("Add Task", add_task_interaction),
        "3": ("Complete Task(s)", complete_task_interaction),
        "4": ("Change Task Status", change_task_status_interaction),
        "5": ("Start Pomodoro for Task", pomodoro_interaction),
        "6": ("Delete a Completed Task", delete_single_completed_task_interaction),
        "7": ("Delete ALL Completed Tasks", delete_all_completed_tasks_interaction),
        "8": ("Delete My User Data", delete_user_data_interaction),
        "9": ("Save & Exit", None),  # Special handling
        "0": ("Exit Without Saving", None),  # Special handling
    }

    # Main menu loop
    while True:
        current_level = user.calculate_level()
        header_string = (
            f"\n===== Task Agenda Menu [User: {user.userid}] "
            f"[Level: {current_level}] [Points: {user.points}] ====="
        )
        print(Fore.GREEN + Style.BRIGHT + header_string)

        # Display Menu Options
        for key, (text, _) in menu_options.items():
            print(f"{key}. {text}")

        choice = input("Enter your choice: ").strip()

        if choice in menu_options:
            text, func = menu_options[choice]

            if choice == "9":  # Save & Exit
                DataManager.save_user(user)
                print("Data saved. Exiting.")
                break
            elif choice == "0":  # Exit Without Saving
                print("Exiting without saving changes.")
                break
            elif func is not None:
                # Call the associated function, passing the user object
                func(user) # delete_user_data_interaction handles its own exit
            # else: (Should not be reachable with current menu structure)
            #    print_error("Internal error: Menu action not defined.")

        else:
            print_error("Invalid choice, please try again.")


if __name__ == "__main__":
    main()