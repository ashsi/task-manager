#=====Import Libraries===========
import datetime

#====Long String Constants====

message_menu = """Select one of the following Options below:
a - Add a task
va - View all tasks
vm - View my tasks
e - Exit
: """

message_menu_admin = """Select one of the following Options below:
r - Register a user
s - View statistics
a - Add a task
va - View all tasks
vm - View my tasks
e - Exit
: """

message_r_try_again = """Select an option:
t             - Try again to register a user
any other key - Return to menu
: """

#====Functions====

def update_user_db():
    with open("data/user.txt", "r") as user_f:
        for credentials in user_f:
            raw_user, raw_pw = credentials.split(", ")
            raw_pw = raw_pw.strip("\n")
            user_db[raw_user] = raw_pw

def display_stats(num_tasks, num_users):
    print("--" * 31)
    print("Statistics")
    print(f"Total number of tasks:\t\t{num_tasks}")
    print(f"Total number of users:\t\t{num_users}")
    print("--" * 31)

def display_task(task_list, position):
    print("--" * 11 + f"[{position}]" + "--" * 11)
    print(f"Task:\t\t\t\t {task_list[1]}")
    print(f"Assigned to:\t\t {task_list[0]}")
    print(f"Date assigned:\t\t {task_list[3]}")
    print(f"Due date:\t\t\t {task_list[4]}")
    print(f"Task Complete?\t\t {task_list[5]}")
    print(f"Task description:\n{task_list[2]}")
    print("--" * 24 + "\n")

#====Main Program====
#====Login Section====
user_db = dict()
user = ""

update_user_db()

"""
User logs into program with a username and password.
Requirement: Password must match existing username in user_db (which takes user details from user.txt).
"""
valid_credentials = False
while not valid_credentials:
    print("--" * 12 + " Task Manager " + "--" * 12)
    user = input("Enter your username: ")
    if user not in user_db.keys():
        print("Error: The username you entered is not in the database.")
        continue
    pw = input("Enter your password: ")
    if user_db[user] == pw:
        valid_credentials = True
    else:
        print("Error: The password you entered does not match the username.")

#====Application Loop====
while True:
    # Present menu to user
    print("--" * 31)
    if user == "admin":
        menu_options = message_menu_admin
    else:
        menu_options = message_menu
    menu = input(menu_options).lower()

    if menu == 'r':
        """ 
        Add new user credentials to the user.txt file. 
        Requirements: Only admin can register a new user.
                      Username for new user must not already exist.
                      Password must be confirmed.
        """
        while True:
            if user != "admin":
                print("Only the admin can register new users.")
                break
            print("Registering a new user.")
            new_user = input("Enter a new username: ")
            if new_user in user_db:
                print("Error: That username already exists.")
                next_step = input(message_r_try_again).lower()
                if next_step == 't':
                    continue
                else:
                    break
            else:
                new_pw = input("Enter a password: ")
                confirm_pw = input("Confirm password: ")
                if new_pw != confirm_pw:
                    print("Error: The passwords do not match.")
                    next_step = input(message_r_try_again).lower()
                    if next_step == 't':
                        continue
                    else:
                        break
                else:
                    with open("data/user.txt", "a") as f:
                        f.write("\n" + new_user + ", " + new_pw)
                    update_user_db()
                    print("User successfully registered.")
                    break

    elif menu == 's':
        """ 
        Display the total number of tasks and the total number of users.
        Requirement: Only admin can see these statistics.
        """
        if user != "admin":
            print("Only the admin can see task manager statistics.")
            break
        else:
            total_tasks = 0
            with open("data/tasks.txt", "r") as tasks_f:
                for line in tasks_f:
                    total_tasks += 1
            total_users = len(user_db)
            display_stats(total_tasks, total_users)

    elif menu == 'a':
        """
        Add a new task to tasks.txt using input from the user.
        """
        print("Adding a new task.")
        username = input("Enter the username of the person to whom the task is assigned\n: ")
        title = input("Enter the title of the task\n: ")
        desc = input("Enter a description of the task\n: ")
        due_date = input("Enter the task's due date in the format YYYY-MM-DD\n: ")
        curr_date = datetime.date.today()
        task_complete = "No"
        with open("data/tasks.txt", "a") as tasks_f:
            tasks_f.write(f"\n{username}, {title}, {desc}, {due_date}, {curr_date}, {task_complete}")

    elif menu == 'va':
        """
        Show all tasks saved in tasks.txt
        """
        print("Showing all tasks.")
        with open("data/tasks.txt", "r") as tasks_f:
            for num, task in enumerate(tasks_f, 1):
                task_split = task.split(", ")
                task_split[0] = task_split[0].strip("\n")
                task_split[-1] = task_split[-1].strip("\n")
                display_task(task_split, num)

    elif menu == 'vm':
        """
        Show tasks assigned to the user that is logged in.
        """
        print("Showing your tasks.")
        num_tasks = 0
        with open("data/tasks.txt", "r") as tasks_f:
            for task in tasks_f:
                task_split = task.split(", ")
                task_split[0] = task_split[0].strip("\n")
                if user != task_split[0]:
                    continue
                task_split[-1] = task_split[-1].strip("\n")
                num_tasks += 1
                display_task(task_split, num_tasks)

    elif menu == 'e':
        """
        Quit the program.
        """
        print('Goodbye!')
        exit()

    else:
        """
        User entered a menu option that does not exist.
        """
        print("That choice is unavailable. Please try again.")
