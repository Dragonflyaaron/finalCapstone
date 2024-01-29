# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os 
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Making sure we have the required txt files for the code to run with
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass
# Define required functions

# Function to create a dictionary of username/password combinations
def username_check():

    # Declare local variables
    users = {}

    #access "users.txt" file in read mode
    with open("user.txt", "r") as user_file:

        # Run through the "user.txt" file to check for matching combination
        for line in user_file:
            user_check = line.strip("\n")

            # Prevent range out of bound errors as caused by empty lines
            if user_check != "":
                user_check = user_check.split(";")
                users.update({user_check[0]: user_check[1]})
    
    return users


# Function to create a list of tasks
def task_check():

    # Declare local variables
    tasks = []
    count = 1

    # Access "tasks.txt" file in read mode
    with open("tasks.txt", "r") as task_file:

        # Run through file to check for matching combinantion
        for line in task_file:
            
            task_check = line.strip("\n")

            # Prevent range out of bound errors as caused by empty lines
            if task_check != "":
                task_check = [task_check.split(";") + [count]]
                tasks.extend(task_check) 
                count += 1

    return tasks


# Function for logging on to task manager program by matching username/password
def login():

    # Get username and password from user

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    print()

    # Call username_check to compare login details 
    user_list = username_check()

    if curr_user in user_list and user_list.get(curr_user) == curr_pass:
        print(f"Welcome {curr_user}!\n")
        return curr_user
    
    
    else:
        print("Your username/password combination is incorrect, please ensure your caps lock is off and try again.\n")
        return "null"
    

# Function for displaying the appropriate menu to user
def menu():

    # Declare local variable
    menu_loop = True

    # Loop for returning to the menu until user chooses to exit
    while menu_loop:
        print('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports''')
        
        # Only show the display statistics option if admin is logged in
        if admin_rights:
            print ("ds - Display Statistics")

        print("e - exit\n")
        selection = input().lower()
        print()

        # If-elif-else statement for calling the selected function

        if selection == "r":
            reg_user()

        elif selection == "a":
            add_task()

        elif selection == "va":
            view_all()

        elif selection == "vm":
            view_mine()
        
        elif selection == "gr":
            generate_reports()

        elif selection == "ds" and admin_rights:
            display_statistics()

        elif selection == "e":
            menu_loop = False
            print ("\nGoodbye\n")
            login()

            

        else:
            print("Invalid selection, please try again.")


# Function to register a new user to "user.txt" file
def reg_user():

    # Declare local variables
    
    user_loop = True
    
    user_list = username_check()

    # Loop to ensure correct details are added
    while (user_loop):

        # Access "user.txt in append mode"
        with open("user.txt", "a") as user_data:

            # Select new username
            new_username = input("Enter new username or type 'e' to exit:\n")

            # Check that username doesn't exist
            if new_username in user_list:
                print("Username already in use, Please try a different username.\n")
            elif new_username.lower() == "e":
                menu() 
            
            else: 
                new_password = input(f"New password for {new_username}:\n")
                confirm_password = input("Confirm Password:\n")

                if new_password == confirm_password:
                    user_data.write(f"\n{new_username}; {new_password}\n")
                    print (f"\nNew User {new_username} added!")
                    print()
                    user_loop = False

                else:
                    print("Your password confirmation does not match. Please try again.\n")


# Function to add a task to the "tasks.txt" file
def add_task():

    # Declare local variables
    user_loop = True

    # Call username_check for validating
    user_list = username_check()

    # Access the "tasks.txt" file in append mode
    with open("tasks.txt", "a") as task_file:

        # Get the task information from the user
        while (user_loop):
            task_username = input("Name of person assigned to task:\n")

            # Make sure that user exists in "user.txt" file
            if task_username in user_list:
                user_loop = False
            else:
                print("User does not exist. Please enter a valid username.\n")

        task_title = input("Title of Task:\n")
        task_description = input("Description of Task:\n")

        # Get assigned date from local time
        task_assigned_date = date.today()
        while True:
            try:

                task_due_date = input("Due date of task (YYYY-MM-DD):\n")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break
            
            except ValueError:
                print("Invalid datetime format. Please use the format specified")
        task_completed = "No"
        due_date = due_date_time.strftime(DATETIME_STRING_FORMAT)

        task_file.write(f"\n{task_username};{task_title};{task_description};{task_assigned_date};{due_date};{task_completed}")
    print(f"\nTask: '{task_title}' for '{task_username}' sucessfully added!\n")


# Function to view all tasks within the "tasks.txt" file
def view_all():

    # Get list of tasks by calling task_check 
    tasks = task_check()
    if os.path.getsize("tasks.txt") == 0:
        print("\nNo tasks assigned, Please type 'a' to assign user a task\n")
        

    # Loop through each task to print them
    else:
        for i in range(0, len(tasks)):
         
            print("-"*50)
            print(f"Task:\t\t\t{tasks[i][1]}")
            print(f"Assigned to:\t\t{tasks[i][0]}")
            print(f"Date assigned:\t\t{tasks[i][3]}")
            print(f"Due date:\t\t{tasks[i][4]}")
            print(f"Task complete?\t\t{tasks[i][5]}")
            print(f"Task description:\n{tasks[i][2]}")

            print("-"*50)
            print("\nEnd of tasks\n")


# Function to view all tasks assigned to the current user within the "tasks.txt" file
def view_mine():

    # Get list of tasks by calling task_check
    tasks = task_check()
    if os.path.getsize("tasks.txt") == 0:
        print("\nNo tasks assigned, Please type 'a' to assign user a task\n")

    # Similiar to the view_all function, loop through each task to print them

    for i in range(0, len(tasks)):
        if user not in tasks[i][0]:
            print(f"\nNo Tasks assigned to {user}\n")

        # If user and assigned user are the same, then print in friendly way
        if user == tasks[i][0]:
            print("-"*50)
            print(f"Task reference:\t\t{tasks[i][6]}")
            print(f"Task:\t\t\t{tasks[i][1]}")
            print(f"Assigned to:\t\t{tasks[i][0]}")
            print(f"Date assigned:\t\t{tasks[i][3]}")
            print(f"Due date:\t\t{tasks[i][4]}")
            print(f"Task complete?\t\t{tasks[i][5]}")
            print(f"Task description:\n{tasks[i][2]}")

            print("-"*50)
            print()

            # Run Function to choose to edit or mark complete
            select_task()


# Function to select a task
def select_task():

    # Get list of tasks by calling task_check
    tasks = task_check()

    # Declare local variables
    task_selection = True

    # Loop to get task number input
    while(task_selection):

        task_number = input("Please enter your task refrence number or '-1' to return to the menu:\n")

        try:
            task_number = int(task_number)

        except:
            print("Invalid input\n")

        if task_number == -1:
            print()
            task_selection = False
            return
        
        else:
            for i in range(0, len(tasks)):

                # If user and assigned user match plus task number matches task ref, allow user to edit or mark
                if task_number == tasks[i][6] and tasks[i][5].lower() == "yes":
                    print(f"task reference {task_number} is already complete, no further editing is permitted\n")

                elif user == tasks[i][0] and task_number == tasks[i][6]:
                    task_modify = input("Please enter 'mt' to mark task as complete or 'et' to edit task.\n").lower()
                    print()

                    if task_modify != "mt" and task_modify != "et":
                        print ("Invalid input.\n")

                    elif task_modify == "mt":
                        mark_task(task_number)
                        print(f"Task {task_number} marked complete!\n")
                        return
                    
                    else:
                        edit_task(task_number)
                        return


# Function to mark task as complete
def mark_task(task_number):

    # Get list of tasks by calling task_check
    tasks = task_check()

    # Declare local variiables
    task_string = ""

    # Check for matching task number and change completed to "yes"

    for i in range(0, len(tasks)):
        if task_number == tasks[i][6]:
            tasks[i][5] = "Yes"

        # Remove number added in by task_check()
            
        tasks[i].pop()

        # Store each task in a variable to be written to "tasks.txt" file

        task_string += ";".join(tasks[i]) + "\n"

        # Open "tasks.txt" in write mode and write the "task_string" to file
        with open("tasks.txt", "w") as task_file:
            task_file.write(task_string)


# Function to edit assigned user or due date
def edit_task(task_number):

    # Get list of users and tasks by calling on the specific functions
    tasks = task_check()
    user_list = username_check()

    # Declare local variables
    task_string = ""

    edit = True

    # Check if user would like to edit assigned person or due date
    while(edit):
        edit_choice = input("Please enter 'user' to edit task assignment, 'date' to edit due date or 'both' to edit both:\n").lower()

        if edit_choice != "user" and edit_choice != "date" and edit_choice != "both":
            print("Invalid Option\n")

        elif edit_choice == "user":

            # Have enter the newly assugned user, checking they exist
            user_update = input("Please enter the username for the person you wish this task assigned to:\n")

            if user_update in user_list:
                for i in range(0, len(tasks)):
                    if task_number == tasks[i][6]:
                        tasks[i][0] = user_update
                        print(f"\nTask ref {task_number} assigned to {user_update}\n")

                        # Remove number added in from task_check
                        tasks[i].pop()

                        task_string += ";".join(tasks[i]) + "\n"

                    edit = False
                    
            else:
                print("Username does not exist\n")

        # Have user enter new due date
                        
        elif edit_choice == "date":
            while True:
                try:
                    
                    date_update = input("Please enter the new due date for the task (YYYY-MM-DD):\n")
                    due_date_update = datetime.strptime(date_update, DATETIME_STRING_FORMAT)
                    break
                
                except ValueError:
                    print("Invalid datetime format. Please use the format specified")

            new_date = due_date_update.strftime(DATETIME_STRING_FORMAT)
            
            for i in range(0, len(tasks)):
                if task_number == tasks[i][6]:
                    tasks[i][4] = new_date
                    print(f"\nTask ref {task_number} updated due date is now {new_date}\n")
                tasks[i].pop()

                task_string += ";".join(tasks[i]) + "\n"

                edit = False

        elif edit_choice == "both":
            user_update = input("Please enter the username for the person you wish this task assigned to:\n")
            if user_update in user_list:
                for i in range(0, len(tasks)):
                    if task_number == tasks[i][6]:
                        tasks[i][0] = user_update
                        while True:
                            try:
                    
                                date_update = input("Please enter the new due date for the task (YYYY-MM-DD):\n")
                                due_date_update = datetime.strptime(date_update, DATETIME_STRING_FORMAT)
                                break
                
                            except ValueError:
                                print("Invalid datetime format. Please use the format specified")

                        new_date = due_date_update.strftime(DATETIME_STRING_FORMAT)
                
                        for i in range(0, len(tasks)):
                            if task_number == tasks[i][6]:
                                tasks[i][4] = new_date
                                print(f"\nTask Ref {task_number} assigned to {user_update} with updated due date {new_date}\n")

                    tasks[i].pop()

                    task_string += ";".join(tasks[i]) + "\n"

                    edit = False
            else:
                print("Username does not exist\n")

    # Open "tasks.txt" file in write mode and write the task_string to it
    with open("tasks.txt", "w") as task_file:
        task_file.write(task_string)


# Function to generate 2 files: "Task_overview.txt" and "user_overview.txt"
def generate_reports():
    
    # Get tasks and user list by calling functions
    tasks = task_check()
    users = username_check()

    # Convert dict "users" to a list of key values
    users = [*users]

    # Declare local variables
    total = len(tasks)
    total_users = len(users)
    complete = 0
    incomplete = 0
    overdue = 0
    percent_incomplete = 0
    percent_overdue = 0

    # Find and keep count of all tasks, both incomplete and overdue
    for i in range(0, total):
        if tasks[i][5].lower() == "yes":
            complete += 1
        elif tasks[i][5].lower() == "no" and datetime.strptime(tasks[i][4], DATETIME_STRING_FORMAT) < datetime.now():
            incomplete += 1
            overdue += 1
            percent_incomplete = (incomplete / total) * 100
            percent_overdue = (overdue / total) * 100

        elif tasks[i][5].lower() == "no":
            incomplete += 1
            percent_incomplete = (incomplete / total) * 100

    # Generate "task_overview.txt" in an easy to read manner
    with open("task_overview.txt", "w") as task_overview_file:
        task_overview_file.write(f"Number of tasks\t\t\t: {total}\n")
        task_overview_file.write(f"Number of completed\t\t: {complete}\n")
        task_overview_file.write(f"Number of incomplete\t\t: {incomplete}\n")
        task_overview_file.write(f"Number overdue\t\t\t: {overdue}\n")
        task_overview_file.write(f"Percentage incomplete\t\t: {percent_incomplete:.2f}%\n")
        task_overview_file.write(f"Percentage overdue\t\t: {percent_overdue:.2f}%\n")

    # Generate "user_overview.txt" in an easy to read manner
    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write(f"Total users\t: {total_users}\n")
        user_overview_file.write(f"Total tasks\t: {total}\n\n")

        # Loop through users to seperate tasks by assigned user
        for i in range(0, total_users):

            # Local variables declared within loop to prevent double counting
            user_tasks = 0
            completed = 0
            not_complete = 0
            user_overdue = 0
            task_percent = 0
            complete_percent = 0
            incomplete_percent = 0
            overdue_percent = 0

            # Loop through set user to find relevant information, count tasks, completed and not, and due date
            for j in range(0, total):
                if users[i] == tasks[j][0] and tasks[j][5].lower() == "yes":
                    user_tasks += 1
                    completed += 1

                # datetime.strip converts the string format into date object, allowing comparison with current time
                # datetime.today() not suited due to time element not generating as like strptime()
                elif users[i] == tasks[j][0] and tasks[j][5].lower() == "no" and datetime.strptime(tasks[j][4], DATETIME_STRING_FORMAT) < datetime.now():
                    user_tasks += 1
                    not_complete += 1
                    user_overdue += 1

                elif users[i] == tasks[j][0] and tasks[j][5].lower() == "no":
                    user_tasks += 1
                    not_complete += 1

                # Calculate user percentage, ensuring 0 does not result in a divide by 0 error
                task_percent = (user_tasks / total) * 100
                if user_tasks != 0:
                    complete_percent = (completed / user_tasks) * 100
                    incomplete_percent = (not_complete / user_tasks) * 100
                    overdue_percent = (user_overdue / user_tasks) * 100

            # Write the results to file before moving to next user
            user_overview_file.write("-" * 50 + "\n")
            user_overview_file.write(f"User: {users[i]}\n\n")
            user_overview_file.write(f"Number of user tasks\t\t: {user_tasks}\n")
            user_overview_file.write(f"Percentage of total tasks\t: {task_percent:.2f}%\n")
            user_overview_file.write(f"Percentage completed\t\t: {complete_percent:.2f}%\n")
            user_overview_file.write(f"Percentage incomplete\t\t: {incomplete_percent:.2f}%\n")
            user_overview_file.write(f"Percentage overdue\t\t: {overdue_percent:.2f}%\n")
    print("\nReports have been generated!\n")


# Function to print the files "task_overview.txt" and "user_overview.txt" to the screen
def display_statistics():

    # Check that files have been generated
    if (os.path.exists('./task_overview.txt') == False) or (os.path.exists('./user_overview.txt') == False):
        generate_reports()

    # Print both files to screen
    with open('task_overview.txt', 'r') as task_overview_file:
        for line in task_overview_file:
                print(line, end = '')

    print()

    with open('user_overview.txt', 'r') as user_overview_file:
        for line in user_overview_file:
            print(line, end = '')

    print()

    print("\nEnd of files\n")
    

# Global variables
login_menu = True
admin_rights = False

# The main program for initialising
# If admin logs in, assign admin rights

while (login_menu):
    user = login() # Calling our login function

    if user == "admin":
        admin_rights = True
        login_menu = False # closing our login menu
    
    elif user != "null": # allowing them to log in without admin if details are correct
        login_menu = False

#initialising menu
menu()

