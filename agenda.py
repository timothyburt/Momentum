# --- Imports ---
import datetime
import json
import os
import time
import sys
import re
import colorama
from colorama import Fore, Back, Style, init

# --- Initialize Colorama ---
init(autoreset=True)

# --- Configuration Constants ---
class Config:
	POMODORO_WORK_MINUTES = 25
	POMODORO_SHORT_BREAK_MINUTES = 5
	POMODORO_LONG_BREAK_MINUTES = 15
	POMODOROS_BEFORE_LONG_BREAK = 4
	POINTS_PER_TASK = 10
	LEVEL_THRESHOLDS = [
		(1, 0), (2, 100), (3, 250), (4, 500), (5, 1000),
		(6, 2000), (7, 3500), (8, 5500), (9, 8000), (10, 11000),
		(11, 15000), (12, 20000),
	]

# --- Utility Functions ---
def print_error(message): print(Fore.RED + message)
def print_success(message): print(Fore.GREEN + message)
def print_warning(message): print(Fore.YELLOW + message)
def print_info(message): print(Fore.CYAN + message)

def clean_filename(text_id):
	text_id = text_id.lower()
	text_id = re.sub(r'[^\w\-]+', '', text_id)
	if not text_id: text_id = "default"
	return f"tasks_{text_id}.json"

# --- Task Class ---
class Task:
	def __init__(self, id, title, due_datetime=None, project=None, priority=None, completed=False, pomos_completed=0):
		self.id = id if id else int(time.time() * 1000)
		self.title = title
		self.due_datetime = due_datetime
		self.project = project
		self.priority = priority
		self.completed = completed
		self.pomodoros_completed = pomos_completed
	def mark_complete(self):
		if not self.completed: self.completed = True; return True
		return False
	def is_complete(self): return self.completed
	def to_dict(self):
		return {"id": self.id, "title": self.title, "due_datetime_str": self.due_datetime.isoformat() if self.due_datetime else None,
				"project": self.project, "priority": self.priority, "completed": self.completed, "pomodoros_completed": self.pomodoros_completed}
	@classmethod
	def from_dict(cls, data):
		due_datetime = None
		if data.get('due_datetime_str'):
			try: due_datetime = datetime.datetime.fromisoformat(data['due_datetime_str'])
			except ValueError: due_datetime = None
		return cls(id=data.get('id'), title=data.get('title', 'Untitled Task'), due_datetime=due_datetime, project=data.get('project'),
				priority=data.get('priority'), completed=data.get('completed', False), pomos_completed=data.get('pomodoros_completed', 0))
	def __str__(self):
		status = Fore.LIGHTBLACK_EX + "[X]" if self.completed else "[ ]"
		time_str = self.due_datetime.strftime('%I:%M %p') if self.due_datetime else "All Day"
		project_str = f" ({self.project})" if self.project else ""
		priority_str = f" [P{self.priority}]" if self.priority else ""
		pomos_str = f" (Pomos: {self.pomodoros_completed})"
		task_line = f"  {status} {time_str.ljust(9)} {self.title}{project_str}{priority_str}{pomos_str}"
		return Fore.LIGHTBLACK_EX + task_line if self.completed else task_line
	def __repr__(self): return f"Task(id={self.id}, title='{self.title}')"

# --- User Class ---
class User:
	def __init__(self, userid, points=0, tasks=None):
		self.userid = userid
		self.points = points
		self.tasks = tasks if tasks is not None else []
	def add_task(self, task): self.tasks.append(task)
	def remove_task(self, task_id):
		initial_len = len(self.tasks); self.tasks = [t for t in self.tasks if t.id != task_id]; return len(self.tasks) < initial_len
	def get_task_by_id(self, task_id): return next((t for t in self.tasks if t.id == task_id), None)
	def get_completed_tasks(self): return sorted([t for t in self.tasks if t.is_complete()], key=lambda task: task.title.lower())
	def get_incomplete_tasks(self): return sorted([t for t in self.tasks if not t.is_complete()], key=lambda task: (task.due_datetime or datetime.datetime.max, task.title.lower()))
	def award_points(self, amount):
		if amount > 0: self.points += amount
	def calculate_level(self):
		current_level = 1
		for level, min_points in Config.LEVEL_THRESHOLDS:
			if self.points >= min_points: current_level = level
			else: break
		return current_level
	def to_dict(self): return {"user_info": {"userid": self.userid, "points": self.points}, "tasks": [task.to_dict() for task in self.tasks]}
	@classmethod
	def from_dict(cls, data, default_userid):
		user_info = data.get("user_info", {}); userid = user_info.get("userid", default_userid); points = user_info.get("points", 0)
		tasks_data = data.get("tasks", []); tasks = [Task.from_dict(task_data) for task_data in tasks_data]
		return cls(userid, points, tasks)

# --- Data Persistence Class ---
class DataManager:
	DATA_DIR = "."
	@staticmethod
	def get_user_filepath(userid):
		# Important: Use the original userid for lookup, clean only for filename generation if needed elsewhere
		# For consistency let's ensure the ID used for filename IS the cleaned one used throughout
		# But the USERID stored IN the file should be the original potentially
		filename = clean_filename(userid) # Use the cleaned ID for the filename
		return os.path.join(DataManager.DATA_DIR, filename)
	@staticmethod
	def load_user(userid_raw):
		# Use raw ID for display/storage, cleaned ID for filename
		filepath = DataManager.get_user_filepath(userid_raw)
		print(f"--- Loading data for user '{userid_raw}' from {filepath} ---")
		default_user_info = {"userid": userid_raw, "points": 0}
		if not os.path.exists(filepath):
			print_warning("No existing data file found for this user. Starting fresh.")
			return User(userid_raw)
		try:
			with open(filepath, 'r') as f: data = json.load(f)
			if isinstance(data, dict) and ("user_info" in data or "tasks" in data):
				user = User.from_dict(data, userid_raw) # Pass raw ID as default if missing in file
				# Ensure the loaded user object uses the raw ID provided at login for consistency
				user.userid = userid_raw
				print_success(f"Loaded {len(user.tasks)} tasks. Current points: {user.points}")
				return user
			elif isinstance(data, list):
				print_warning("Old tasks format detected. Converting and initializing points to 0.")
				tasks = [Task.from_dict(task_data) for task_data in data]
				return User(userid_raw, points=0, tasks=tasks)
			else:
				print_warning("Unknown data format in file. Starting fresh.")
				return User(userid_raw)
		except (json.JSONDecodeError, IOError, TypeError, KeyError) as e:
			print_error(f"Error loading data from {filepath}: {e}. Starting fresh.")
			return User(userid_raw)
	@staticmethod
	def save_user(user):
		filepath = DataManager.get_user_filepath(user.userid) # Use the user's stored ID (which should be raw)
		print(f"--- Saving data for user '{user.userid}' to {filepath} ---")
		try:
			data_to_save = user.to_dict()
			with open(filepath, 'w') as f: json.dump(data_to_save, f, indent=4)
			print_success(f"Saved {len(user.tasks)} tasks. Points: {user.points}")
		except IOError as e: print_error(f"Error saving data to {filepath}: {e}")
		except Exception as e: print_error(f"An unexpected error occurred during save: {e}")
	@staticmethod
	def delete_user_file(userid):
		"""Deletes the user's data file."""
		filepath = DataManager.get_user_filepath(userid)
		if os.path.exists(filepath):
			try:
				os.remove(filepath)
				print_success(f"Data file {filepath} deleted successfully.")
				return True
			except OSError as e:
				print_error(f"Error deleting file {filepath}: {e}")
				return False
		else:
			print_warning(f"Data file {filepath} not found. Nothing to delete.")
			return False


# --- Core Application Logic Functions ---
# --- [display_agenda, add_task_interaction, prompt_select_tasks, complete_task_interaction] ---
# --- [delete_single_completed_task_interaction, delete_all_completed_tasks_interaction] ---
# --- [pomodoro_interaction, run_timer, start_pomodoro_cycle] ---
# (These functions remain unchanged from the refactored version, but depend on User/Task classes now)
# --- Paste them here ---
def display_agenda(user):
	tasks = user.tasks
	if not tasks: print("\nNo tasks in your agenda!"); return
	timed_tasks = sorted([t for t in tasks if t.due_datetime], key=lambda x: x.due_datetime)
	all_day_tasks = sorted([t for t in tasks if not t.due_datetime], key=lambda x: x.title.lower())
	tasks_by_day = {}; today = datetime.date.today()
	for task in timed_tasks:
		task_date = task.due_datetime.date()
		if task_date not in tasks_by_day: tasks_by_day[task_date] = []
		tasks_by_day[task_date].append(task)
	print("\n--- Your Agenda ---"); sorted_dates = sorted(tasks_by_day.keys())
	for display_date in sorted_dates:
		header_str = display_date.strftime('%A, %B %d, %Y')
		if display_date == today: header_str = f"TODAY - {header_str}"
		elif display_date == today + datetime.timedelta(days=1): header_str = f"TOMORROW - {header_str}"
		print(Style.BRIGHT + f"\n--- {header_str} ---")
		for task in tasks_by_day[display_date]: print(task)
	if all_day_tasks:
		print(Style.BRIGHT + "\n--- Unscheduled / All Day Tasks ---")
		for task in all_day_tasks:
			status = Fore.LIGHTBLACK_EX + "[X]" if task.is_complete() else "[ ]"
			title_display = task.title; project_str = f" ({task.project})" if task.project else ""
			priority_str = f" [P{task.priority}]" if task.priority else ""; pomos_str = f" (Pomos: {task.pomodoros_completed})"
			task_line = f"  {status} {'No Date'.ljust(9)} {title_display}{project_str}{priority_str}{pomos_str}"
			print(Fore.LIGHTBLACK_EX + task_line if task.is_complete() else task_line)

def add_task_interaction(user):
	print("\n--- Add New Task ---"); title = input("Task Title: ").strip()
	if not title: print_error("Task title cannot be empty."); return
	due_date_str = input("Due Date (YYYY-MM-DD) or leave blank: ").strip(); due_time_str = input("Due Time (HH:MM) or leave blank: ").strip()
	project = input("Project/Category (optional): ").strip(); priority_str = input("Priority (1=High, 2=Med, 3=Low - optional): ").strip()
	due_datetime = None
	if due_date_str:
		try:
			date_part = datetime.datetime.strptime(due_date_str, "%Y-%m-%d").date()
			if due_time_str: time_part = datetime.datetime.strptime(due_time_str, "%H:%M").time(); due_datetime = datetime.datetime.combine(date_part, time_part)
			else: print_warning("Date specified without time. Treating as unscheduled."); due_datetime = None
		except ValueError: print_error("Invalid date or time format. Task treated as unscheduled."); due_datetime = None
	priority = None
	if priority_str.isdigit() and 1 <= int(priority_str) <= 3: priority = int(priority_str)
	elif priority_str: print_warning("Invalid priority value. Ignoring.")
	new_task = Task(id=None, title=title, due_datetime=due_datetime, project=project if project else None, priority=priority)
	user.add_task(new_task); print_success("Task added successfully!")

def prompt_select_tasks(task_list, prompt_message, allow_multiple=False, allow_cancel=True):
	if not task_list: print_warning("No tasks available for selection."); return None
	print(prompt_message); display_map = {}
	for i, task in enumerate(task_list):
		display_map[i] = task; due_str = task.due_datetime.strftime('%Y-%m-%d %H:%M') if task.due_datetime else "No date"
		print(f"  {i}: {task.title} ({due_str})")
	cancel_prompt = " (or 'c' to cancel)" if allow_cancel else ""; input_prompt = f"Enter number{'s (e.g., 0, 2)' if allow_multiple else ''}{cancel_prompt}: "; choice_str = input(input_prompt).strip()
	if allow_cancel and choice_str.lower() == 'c': print("Operation cancelled."); return None
	if not choice_str: print_warning("No selection made."); return None
	selected_tasks = []; invalid_inputs = []
	if allow_multiple:
		parts = choice_str.split(','); chosen_display_indices = set()
		for part in parts:
			part = part.strip()
			if not part: continue
			if part.isdigit():
				idx = int(part)
				if idx in display_map: chosen_display_indices.add(idx)
				else: invalid_inputs.append(f"'{part}' (out of range)")
			else: invalid_inputs.append(f"'{part}' (not a number)")
		if not invalid_inputs: selected_tasks = [display_map[idx] for idx in sorted(list(chosen_display_indices))]
	else:
		if choice_str.isdigit():
			idx = int(choice_str)
			if idx in display_map: selected_tasks = [display_map[idx]]
			else: invalid_inputs.append(f"'{choice_str}' (out of range)")
		else: invalid_inputs.append(f"'{choice_str}' (not a number)")
	if invalid_inputs: print_error("Invalid input detected: " + ", ".join(invalid_inputs)); return None
	return selected_tasks

def complete_task_interaction(user):
	print("\n--- Mark Task(s) as Complete ---")
	tasks_to_complete = prompt_select_tasks(user.get_incomplete_tasks(), "Select task(s) to mark as complete:", allow_multiple=True, allow_cancel=True)
	if not tasks_to_complete: return
	print("\nYou selected:")
	for task in tasks_to_complete: print(f"- {task.title}")
	confirm = input(Fore.YELLOW + f"Mark these {len(tasks_to_complete)} tasks as complete? (y/n): ").lower()
	if confirm != 'y': print("Completion cancelled."); return
	tasks_completed_count = 0; total_points_earned = 0; old_level = user.calculate_level()
	for task in tasks_to_complete:
		if task.mark_complete(): total_points_earned += Config.POINTS_PER_TASK; tasks_completed_count += 1
	if tasks_completed_count > 0:
		user.award_points(total_points_earned); new_level = user.calculate_level()
		print_success(f"\nCompleted {tasks_completed_count} task(s)."); print_info(f"You earned {total_points_earned} points.")
		print(f"Total points: {user.points}")
		if new_level > old_level:
			print(Fore.GREEN + Style.BRIGHT + f"\n🎉🎉🎉 Level Up! 🎉🎉🎉"); print(Fore.GREEN + Style.BRIGHT + f"You are now Level {new_level}!")
	else: print_warning("No tasks were newly marked as complete.")

def delete_single_completed_task_interaction(user):
	print("\n--- Delete a Completed Task ---")
	task_to_delete = prompt_select_tasks(user.get_completed_tasks(), "Select a completed task to delete:", allow_multiple=False, allow_cancel=True)
	if not task_to_delete: return
	selected_task = task_to_delete[0]
	confirm = input(Fore.YELLOW + f"Are you sure you want to permanently delete '{selected_task.title}'? (y/n): ").lower()
	if confirm == 'y':
		if user.remove_task(selected_task.id): print_success(f"Task '{selected_task.title}' deleted successfully.")
		else: print_error("Error: Could not delete the task (maybe it was already removed?).")
	else: print("Deletion cancelled.")

def delete_all_completed_tasks_interaction(user):
	print("\n--- Delete ALL Completed Tasks ---")
	completed_tasks = user.get_completed_tasks(); num_completed = len(completed_tasks)
	if num_completed == 0: print_warning("No completed tasks found to delete."); return
	print_warning(Style.BRIGHT + f"Warning: You are about to delete {num_completed} completed task(s).")
	confirm = input(Fore.YELLOW + "This action cannot be undone. Are you absolutely sure? (yes/no): ").lower()
	if confirm == 'yes':
		deleted_count = 0; ids_to_delete = [task.id for task in completed_tasks]
		for task_id in ids_to_delete:
			if user.remove_task(task_id): deleted_count += 1
		if deleted_count > 0: print_success(f"Successfully deleted {deleted_count} completed task(s).")
		else: print_warning("No tasks were deleted.")
	else: print("Deletion cancelled.")

def pomodoro_interaction(user):
	print("\n--- Start Pomodoro Session ---")
	task_to_work_on = prompt_select_tasks(user.get_incomplete_tasks(), "Select task to work on:", allow_multiple=False, allow_cancel=True)
	if not task_to_work_on: return
	selected_task = task_to_work_on[0]; start_pomodoro_cycle(selected_task)

def run_timer(minutes, session_type="Work"):
	total_seconds = minutes * 60; cancelled = False; color = Fore.CYAN if session_type == "Work" else Fore.MAGENTA
	print(color + f"\nStarting {session_type} session ({minutes} minutes). Press Ctrl+C to cancel.")
	try:
		while total_seconds > 0:
			mins, secs = divmod(total_seconds, 60); timer_display = f"{session_type}: {mins:02d}:{secs:02d}".ljust(25)
			print(color + f"\r{timer_display}", end=""); sys.stdout.flush(); time.sleep(1); total_seconds -= 1
		print(color + "\r" + f"{session_type} session finished!".ljust(25))
	except KeyboardInterrupt: print(Fore.YELLOW + "\r" + f"{session_type} session cancelled.".ljust(25)); cancelled = True
	if not cancelled: print("\a", end="")
	return not cancelled

def start_pomodoro_cycle(task):
	if not task: return
	print(f"\nSelected Task: {task.title}"); pomodoro_count_session = 0
	while True:
		work_completed = run_timer(Config.POMODORO_WORK_MINUTES, "Work")
		if work_completed:
			task.pomodoros_completed += 1; pomodoro_count_session += 1
			print(f"Pomodoro #{pomodoro_count_session} for '{task.title}' completed! Total: {task.pomodoros_completed}")
			if pomodoro_count_session % Config.POMODOROS_BEFORE_LONG_BREAK == 0: print("\nTime for a long break!"); run_timer(Config.POMODORO_LONG_BREAK_MINUTES, "Long Break")
			else: print("\nTime for a short break!"); run_timer(Config.POMODORO_SHORT_BREAK_MINUTES, "Short Break")
			try:
				cont = input("\nStart next Pomodoro session for this task? (y/n): ").lower()
				if cont != 'y': break
			except EOFError: break
		else: print("Pomodoro cycle interrupted."); break
# --- End of pasted functions ---

# --- New Interaction Function: Delete User Data ---
def delete_user_data_interaction(user):
	"""Handles the interaction for deleting the current user's data file."""
	print("\n" + Fore.RED + Style.BRIGHT + "--- !!! DANGER ZONE: DELETE USER DATA !!! ---")
	print(Fore.YELLOW + f"This action will permanently delete all tasks, points, and level progress")
	print(Fore.YELLOW + f"associated with the User ID '{user.userid}'.")
	print(Fore.YELLOW + Style.BRIGHT + "This operation cannot be undone.")

	confirm1 = input(Fore.YELLOW + "Are you absolutely sure you want to proceed? (yes/no): ").lower()

	if confirm1 == 'yes':
		print(Fore.YELLOW + "\nFor final confirmation, please type your User ID exactly:")
		confirm_userid = input(f"Type '{user.userid}' to confirm deletion: ").strip()

		if confirm_userid == user.userid:
			print(Fore.RED + "\nDeleting user data file...")
			if DataManager.delete_user_file(user.userid):
				print_success(f"All data for user '{user.userid}' has been deleted.")
				print("Exiting application.")
				sys.exit(0) # Exit cleanly after deletion
			else:
				# Error message already printed by delete_user_file
				print_error("Deletion failed. Please check permissions or file status.")
				# Allow the app to continue, maybe the file was already gone
		else:
			print_error("User ID mismatch. Deletion cancelled.")
	else:
		print("Deletion cancelled.")

# --- Main Application Execution ---
def main():
	"""Main function to run the application."""
	user_id_raw = ""
	while not user_id_raw:
		user_id_raw = input("Enter your User ID (letters/numbers recommended): ").strip()
		if not user_id_raw: print_error("User ID cannot be empty.")

	user = DataManager.load_user(user_id_raw)

	# Main menu loop
	menu_options = {
		"1": ("View Agenda", display_agenda),
		"2": ("Add Task", add_task_interaction),
		"3": ("Complete Task(s)", complete_task_interaction),
		"4": ("Start Pomodoro for Task", pomodoro_interaction),
		"5": ("Delete a Completed Task", delete_single_completed_task_interaction),
		"6": ("Delete ALL Completed Tasks", delete_all_completed_tasks_interaction),
		"7": ("Delete My User Data", delete_user_data_interaction), # New Option
		"8": ("Save & Exit", None), # Renumbered
		"9": ("Exit Without Saving", None) # Renumbered
	}

	while True:
		current_level = user.calculate_level()
		header_string = f"\n===== Task Agenda Menu [User: {user.userid}] [Level: {current_level}] [Points: {user.points}] ====="
		print(Fore.GREEN + Style.BRIGHT + header_string)
		for key, (text, _) in menu_options.items(): print(f"{key}. {text}")
		choice = input("Enter your choice: ").strip()

		if choice in menu_options:
			text, func = menu_options[choice]
			if choice == "8": # Save & Exit (New Number)
				DataManager.save_user(user)
				print("Data saved. Exiting.")
				break
			elif choice == "9": # Exit Without Saving (New Number)
				print("Exiting without saving changes.")
				break
			elif func is not None:
				# Special handling for delete user which might exit
				if func == delete_user_data_interaction:
					func(user) # This function handles exit internally
				else:
					func(user) # Call other functions normally
			# If func is None and not exit choice (shouldn't happen with current dict)
		else:
			print_error("Invalid choice, please try again.")

if __name__ == "__main__":
	main()