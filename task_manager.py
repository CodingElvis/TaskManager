#SE Bootcamp T26 - Capstone Project Three
"""
This task manager program has been written by David Lewis to meet the requirements of Hyperion 
Dev's software engineering bootcamp, Capstone Two and Capstone Three assignments.  
Acknowledgement: it follows template guidance; most notes removed for ease of reading
"""

"""
Note: Amendments to previous submission
1. added omitted functionality - edit task due date under "view mine" option
2. fixed zero division error occurring when generating reports and a registered user had no tasks allocated
3. added a new get_date() function to get the user to enter a date and ensure its correctly formatted, to avoid duplicating this code
4. added main() function as suggested, and put login and core menu into functions called by main()
"""

#=====importing libraries===========

import datetime
 
#=====Functions===========

"""********DATA MANAGEMENT FUNCTIONS********"""

'''These four functions contain the code for getting and maintaining the task data and user
database.  If we want to alter the core source filenames, these functions are what 
needs to be edited.  (Filenames of output report are handled separately under "generate reports".

get_tasks() and get_users() are called at the start of the program to populate our data dictionaries.
write_tasks() and write_users() are called whenever we edit data so the source files and the data
in memory stay aligned.

'''
#this function gets the task data from the source file. It sets up the core dictionary of data
def get_tasks():
    dict={}
    with open ('tasks.txt', 'r') as file:
        #we loop through the file, using enumerate so that every task gets assigned a unique number
        #this can be interpreted as a task id and used as a key in this main dictionary
        for num, line in enumerate(file):
            #we split the data for each task into a list
            line=line.strip("\n")
            splitline = line.split(", ")
            # and use it in a dictionary as the value associated with the relevant task id as the key
            dict[num] = splitline
        #we then return the dictionary
        return dict

# this function writes the task data to source file, and is called whenever we amend task data
def write_tasks():
    with open('tasks.txt', 'w') as file:
        # for each entry in our task dictionary we create a string in the necessary format and write to file
        for key in task_dict:
            string= ", ".join(task_dict[key])
            file.write(f"{string}\n")

#this function gets the user data from the source file. It sets up the user dictionary for the log in process
def get_users():
    dict={}
    with open('user.txt', 'r') as file:
        # we iterate through lines in the file, aplitting each into a list with [username, password]
        for line in file:
            line = line.strip("\n")
            splitline = line.split(", ")
            # we use username, password as the key value pair in a user dictionary
            dict[splitline[0]] = splitline[1]
        # we then return the dictionary
        return dict

#this function writes user data to file.  It is called whenever we amend user data
def write_users():
    with open('user.txt', 'w') as file:
        #we loop through the user dictionary creating and writing to file the correct string for each user
        for key in user_dict:
            string = key + ", " + user_dict[key]
            file.write(f"{string}\n")      


"""*******INPUT DATE FUNCTION*******"""
#This function gets the user to input a date in the correct format for the program and returns it as a string

def get_date():

    #we get the day, checking first that its an integer then its a plausible integer, and re-asking until it is
    while True:
        date_day_string = input("Date (day): ")
        if date_day_string.isnumeric() == False:
            print ("Not an integer, we need an integer here. Please try again.")
            continue
        date_day = int(date_day_string)
        if not 0 < date_day < 32:
            print ("Not a valid number. A month has between 1 and 31 days. Please try again.")
            continue
        #if we get here we have a day between 1 and 31 inc and can break this loop
        break
                
    #we get the month, checking its in the correct 3 letter format
    while True:
        date_month_string = input("Month (abbreviated): ")
        months= ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        if not date_month_string in months:
            print ("Please enter month in correct format ie one of the following including capital")
            print (months)
            continue
        else:
            break

    #we get the year checking that its an integer greater than 2000 and less than 2200
    while True:
        date_year_string = input("Year (4 digits): ")
        if date_year_string.isnumeric() == False:
            print ("Not an integer, we need an integer here. Please try again.")
            continue
        date_year=int(date_year_string)
        if not 2000 < date_year < 2200:
            print ("Lets not rewrite ancient history or predict the far future. Year should be between 2000 and 2200.")
            continue
        #at this point we should have a sensible year and can break the loop
        else:
            break


    #we combine the data into a string in the correct format and return it
    date_string = f"{date_day} {date_month_string} {date_year}"
    return date_string

#
"""*******USER REGISTRATION FUNCTION*******"""
# This function will be called when the admin user selects the option of adding a new user

def reg_user():
        print()
        print("--------------Registering new user--------------")
        print()
        
        #we set up a while true loop to ask for the new user's data
        # the loop allows us to re=ask for data if unacceptable data are entered
        while True:
            new_name=input("Please enter new username: ")
            new_password=input("Please enter the new password: ")
            confirm_password=input("Please confirm new password: ")
            
        #we check that the chosen name isn't already in-use and restart the loop if it is
            if new_name in user_dict:
                print("Username already in use; user registration failed.  Please try again.")
                print()
                continue  

        #if the password and password confirm don't match we flag this and restart the loop
            elif new_password != confirm_password:
                print ("Passwords don't match; user registration failed.  Please try again." )
                print()
                continue
            
            elif ", " in new_name or ", " in new_password:
                print ("Please select name or password without \", \". Registation failed. Please try again.")
                print()
                continue

            # if we reach this point we should have valid new user data and can break this loop
            else:
                break
            
        #we add the user's details to our dictionary of users
        user_dict[new_name] = new_password

        # having amended the user dictionary we write the contents to file to ensure file and memory remain aligned
        write_users()

        #we print a confirmation and then we will return to the main menu
        print()
        print (f"{new_name} successfully registered as user")
        print()
        print()

"""*******ADD TASK FUNCTION*******"""
#This function will be called when the user selects the option of adding a new task

def add_task():
    print()
    print("--------------Adding new task--------------")

        #first we ask which user will be assigned the new task
    while True:
        victim = input("Who will be assigned the task? (enter username): ")
                
        #we check that the user being assigned the task is a registered user and re-ask until a valid entry is offered
        if victim not in user_dict:
            print("Not a valid username. Please try again.")
            continue
        #if we get to here we have a valid username and we can proceed to the next step
        break
                          
    #We get the title and description of the task
    # we dont want these strings to contain ", " as this might mess with
    # our method for getting data from the source file into memory
    # we replace ", " with " " to sidestep any such problem
    new_task_title = input("Please enter a title for the new task: ")
    if ", " in new_task_title:
        new_task_title = new_task_title.replace (", ", " ")
    new_task_description = input("Please enter a description of the new task: ")
    if ", " in new_task_description:
        new_task_description = new_task_description.replace (", ", " ")

    #we now ask for the task's due date - as day, month, year following the date format in the initial tasks list                
    print ("Please enter task due date using date, month (3 letters) and year (4 digits)")
    new_task_due_date = get_date()
    
    #for the assigned date we use datetime to get today's date and format it into the dd / mon /year format 
    assigned_date_date= datetime.date.today()
    assigned_date_string = assigned_date_date.strftime("%d %b %Y")

    #finally we put the new task into our main dictionary, and write data to file
    #we take task id as being the next task (as indexed from zero) beyond the current dictionary, ie same as current len() 
    taskid=len(task_dict)
    task_dict[taskid] = [victim, new_task_title, new_task_description, assigned_date_string, new_task_due_date, "No"]
    write_tasks()

    print()
    print (f"\"{new_task_title}\" successfully added as a task for {victim}")
    print()


"""*******VIEW ALL FUNCTION*******"""
#This function will be called if the user selects the option to view all tasks

def view_all():
    print()
    print ("--------------Displaying all tasks---------------")
    print()

    # we run a for loop that loops through each entry of our task dictionary of the file ie each task
    for key in task_dict:                
        # then we print output text in a suitable format drawing on each data field where needed
        print ("-------------------------------------------------")
        print(f"Task id: \t\t{key}")
        print(f"Title:\t\t\t{task_dict[key][1]}")
        print(f"Assigned to:\t\t{task_dict[key][0]}")
        print(f"Date assigned:\t\t{task_dict[key][3]}")
        print(f"Due date:\t\t{task_dict[key][4]}")
        print(f"Task complete?\t\t{task_dict[key][5]}")
        print(f"Task description:\n {task_dict[key][2]}")
        print("-------------------------------------------------")
        print()
    print()

"""*******VIEW MINE FUNCTION*******"""
#This function will be called if a user selects the menu option to view tasks assigned to them

def view_mine():
    print()
    print(f"--------------Displaying tasks assigned to {user_name}--------------")
    print()

    # Below, we're going to let the user select tasks in order to modify them
    #we'll need to track which tasks they can select, so we set up a list, initially empty
    valid_choices=[]

    #We now loop through the task dictionary.  We sklp tasks allocated to other users. We print to 
    #screen tasks allocated to the logged in user
    for key in task_dict:
        if user_name != task_dict[key][0]:
            continue
        print ("-------------------------------------------------")
        print(f"Task id:\t\t{key}")
        print(f"Title:\t\t\t{task_dict[key][1]}")
        print(f"Assigned to:\t\t{task_dict[key][0]}")
        print(f"Date assigned:\t\t{task_dict[key][3]}")
        print(f"Due date:\t\t{task_dict[key][4]}")
        print(f"Task complete?\t\t{task_dict[key][5]}")
        print(f"Task description:\n {task_dict[key][2]}")
        print("-------------------------------------------------")
        print()

        # when we've printed to screen we also put the taskid in our control list of selectable tasks
        valid_choices.append(key)
    
    print()
    #when we've printed everything we present the user with the option of quitting or selecting task to edit
    while True:    
        mine_choice = input("Enter a task id number to edit or \"-1\" to return to main menu: ")
        
        #if the user chooses to quit we break the loop, causing return to main menu
        if mine_choice == "-1":
            break
        #'we check that an integer has been entered
        if mine_choice.isnumeric() == False:
            print ("Not a valid entry. Please try again.")
            continue
        
        # we cast to integer and check that the integer corresponds to a task assigned to this user
        mine_choice = int(mine_choice)
        if not mine_choice in valid_choices:
            print ("Not a valid entry. Please try again.")
            continue

        # we check that the selected task is not already complete; and raise an error if it is
        if task_dict[mine_choice][5].lower() == "yes":
            print ("Tasks already completed cannot be edited.  Please try again.")
            continue

        #if we reach here we have a valid choice and proceed to offer editing options
        print (f"Editing task {mine_choice}")
        while True:
            print ("Option 1. Mark complete\nOption 2. Re-assign task\nOption 3. Edit due date")
            menu_choice=input("Please enter 1 2 or 3: ")

            #if the user selects 1 to mark the task completed we edit our data, 
            #write to file and print a confirmation          
            if menu_choice == "1":
                task_dict[mine_choice][5] = "Yes"
                write_tasks()
                print(f"Task {mine_choice} marked as complete")
                print()
                
                #then we break to return to the task selection menu
                break
            
            #if the user chooses to reassign a task this code runs
            if menu_choice == "2":
                while True:
                    
                    # we ask for the new user to be assigned the task and check they're a registered user
                    new_victim = input ("Enter user who will now be assigned the task: ")
                    if new_victim not in user_dict:
                        print ("Not a registered user.  Please try again")
                        continue
                    
                    # if they are a registered user we amend our data, write to file and print a confirmation
                    else:
                        task_dict[mine_choice][0] = new_victim
                        write_tasks()
                        print (f"Task {mine_choice} re-assigned to {new_victim}")
                        print()
                        
                        # we break out of the loop asking for the new user
                        break
                #then we also break back to the task selection menu (we only reach this 
                # point if the task has been amended successfully
                break
            
            if menu_choice == "3":
               
                #we now ask for the task's due date - as day, month, year following the date format in the initial tasks list                
                print ("Please enter new task due date using date, month (3 letters) and year (4 digits)")
                amend_task_due_date = get_date()

                #now we amend the date in the task description
                task_dict[mine_choice][4] = amend_task_due_date
                write_tasks()
                print (f"Task {mine_choice} assigned new due date of {amend_task_due_date}")
                print()
                    
                #we have now amended the task and break back to the task selection menu
                break

            #we get here if the user hasnt correctly selected option 1 2 or 3
            else:
                print("Not a valid option. Please try again.")

"""*******GENERATE REPORTS FUNCTION*******"""
# This function will be called if the user selects the menu option to generate reports
def generate_reports():

#First we collate the required data about tasks

    total_tasks = 0
    completed_tasks = 0
    uncompleted_tasks = 0
    uncompleted_overdue_tasks = 0

    # we loop through our task dictionary
    for entry in task_dict:
        
        #we increment total tasks on every entry
        total_tasks +=1

        #we check if a task is marked complete, and increment completed_tasks if so
        if task_dict[entry][5].lower() == "yes":
            completed_tasks +=1
        
        #otherwise the task must be incomplete; we increment uncompleted_tasks
        else: 
            uncompleted_tasks += 1

            #if so we get today's date, and convert our date string into a date object using datetime module
            today = datetime.datetime.today()
            due_date_object = datetime.datetime.strptime (task_dict[entry][4], "%d %b %Y")

            # if the due date is in the past (ie today is bigger than it) we increment overdue tasks
            if today > due_date_object:
                uncompleted_overdue_tasks += 1
    
    #now we generate the task overview txt file
    #if we have zero tasks tracked, we skip the percentage calculations as they would require division by zero, 
    # causing an error and being mathematical nonsense
    with open("task_overview.txt", "w") as file:
        file.write ("------------------------------------------------------------\n")
        file.write ("OVERVIEW OF TOTAL TASKS TRACKED\n\n")
        file.write (f"Total tasks tracked:               {total_tasks}\n")
        if total_tasks !=0:
            file.write (f"Of which completed:                {completed_tasks}\t{round(100*completed_tasks/total_tasks, 1)}%\n")
            file.write (f"Of which still incomplete:         {uncompleted_tasks}\t{round(100*uncompleted_tasks/total_tasks, 1)}%\n")
            file.write ("------------------------------------------------------------\n")
            file.write (f"Tasks both overdue and incomplete: {uncompleted_overdue_tasks}\t{round(100*uncompleted_overdue_tasks/total_tasks, 1)}%\n")
        else:
            file.write (f"Of which completed:                {completed_tasks}\tna\n")
            file.write (f"Of which still incomplete:         {uncompleted_tasks}\tna\n")
            file.write ("------------------------------------------------------------\n")
            file.write (f"Tasks both overdue and incomplete: {uncompleted_overdue_tasks}\tna\n")

        file.write ("------------------------------------------------------------\n")
        file.write ("Note: all percentages are of total tasks tracked")


#Now we collate the additional data we will need to consider tasks by user
# here its easier to write to the file straight away so we dont need to retain info about previous users

    # we generate the file and add some headings
    with open('user_overview.txt', 'w') as file:
        file.write ("------------------------------------------------------------\n")
        file.write ("OVERVIEW OF TASKS TRACKED, BY USER\n")
        file.write(f"Total users registered:                 {len(user_dict)}\n")
        file.write(f"Total tasks tracked:                    {total_tasks}\n")
        file.write ("------------------------------------------------------------\n")

        #we create a for loop that runs through our dictionary of users in turn
        for user in user_dict:

            # we set up variables to count the user's tasks
            user_tasks = 0
            user_complete = 0
            user_incomplete = 0
            user_overdue = 0

            # now loop through our task dictionary, checking if a task is assigned to the user currently being analysed
            for task in task_dict:
                if task_dict[task][0] == user:

                    #if it is we incremeent the user's tasks, and then increment complete/incomplete/overdue as appropriate
                    user_tasks += 1
                    if task_dict[task][5].lower() == "yes":
                        user_complete +=1
                    else: 
                        user_incomplete += 1
                        today = datetime.datetime.today()
                        due_date_object = datetime.datetime.strptime(task_dict[task][4], "%d %b %Y")
                        if today > due_date_object:
                            user_overdue += 1
                            
            #then we add the activity analysis for that user to our report
            file.write("\n")
            file.write ("------------------------------------------------------------\n")
            file.write(f"Activity by user name:                    {user}\n")
            file.write(f"User tasks assigned:                      {user_tasks}\n")
            if total_tasks != 0:
                file.write(f"   percentage of total tasks:             {round(100*user_tasks/total_tasks,1)}%\n")
            else:
                file.write(f"   percentage of total tasks:             na\n")
            file.write ("\n")
            if user_tasks != 0:
                file.write(f"Percentage of user's tasks complete:      {round(100*user_complete/user_tasks, 1)}%\n")
                file.write(f"Percentage of user's tasks incomplete:    {round(100*user_incomplete/user_tasks, 1)}%\n")
                file.write(f"Percentage of user's tasks overdue:       {round(100*user_overdue/user_tasks, 1)}%\n")
            else:
                file.write(f"Percentage of user's tasks complete:      na\n")
                file.write(f"Percentage of user's tasks incomplete:    na\n")
                file.write(f"Percentage of user's tasks overdue:       na\n")

            file.write ("------------------------------------------------------------\n")

            #then the loop continues to analyse the activity of next user in user_dict 
            # or reverts to the main menu with if we're through all users




"""*******DISPLAY STATISTICS FUNCTION*******"""
#this function will be called if the user selects the menu option to display statistics

def display_statistics():

#we need to read the statistics from the generated reports
# we could check if generated reports are present, but even if they exist they could be out of date
# to avoid this we choose to generate the reports whenever this function is called before reading the files and printing to screen
    generate_reports()

        #first we read and display the task overview file

    with open('task_overview.txt', 'r') as file:
        text = file.read()
        print(text)

    print("\n\n")

        #then we do the same for the user overview file
    with open ('user_overview.txt', 'r') as file:
        text = file.read()
        print (text)
            


"""*******LOGIN FUNCTION*******"""

def login():
    #we set up an "infinite" loop asking the user for login credentials
    while True:
        user_name = input("Please enter your user name: ")
        user_password = input("Please enter your password: ")
        
        # if the username is invalid we say so and rerun the loop
        if user_name not in user_dict:
            print("Invalid user name. Please try again")
            continue
        
        #if the password is incorrect we say so and rerun the loop
        if user_password != user_dict[user_name]:
            print("Incorrect password.  Please try again")  
            continue

        #if we reach this point we have a valid login and so we break out of our loop and welcome the user
        break
    print()
    print(f"Welcome {user_name}. You are now logged in.")
    print()
    return user_name


"""*******MENU FUNCTION*******"""
#we now enter the core loop of the program, which presents a menu of options to the user
#we run this as a "while True" loop allowing the user to perform indefinitely many actions
#this section has been customised according to Part 2 of the task, which gives only the user "admin" certain access
def menu():

    while True:
        # we check if the user is "admin" and if so we show their full menu of options
        # we get their choice of action (cast to lower case to minimise data entry "mistakes")
        if user_name == "admin":
            menu = input('''Select one of the following options:
    r  -  Register a user
    a  -  Add a task
    va -  View all tasks
    vm -  View my tasks
    ds -  Display statistics
    gr -  Generate reports
    e  -  Exit
    : ''').lower()

        #if the user isnt named "admin" we do the same with a more restricted menu
        if user_name != "admin":
            menu = input('''Select one of the following options:
    a  -  Add a task
    va -  View all tasks
    vm -  View my tasks
    gr -  Generate reports
    e  -  Exit
    : ''').lower()
        
        if menu == 'r':
            if user_name != "admin":
                print("You have tried to pick an option only available to admin.  Please select a valid option.")
            else:
                reg_user()

        elif menu == 'a':
            add_task()

        elif menu == 'va':
            view_all()
            
        elif menu == 'vm':
            view_mine()

        elif menu == "ds":

            if user_name != "admin":
                print("You have tried to pick an option only available to admin.  Please select a valid option.")
            else:
                display_statistics()

        elif menu == "gr":
            generate_reports()

        #this code runs if the user chooses to exit
        elif menu == 'e':
            print('Goodbye!!!')
            exit()
                    
        #this code runs if none of the menu options has been correctly selected
        else:
            print("You have made a wrong choice. Please try again.")


"""*******MAIN FUNCTION*******"""
#this function is called when we run the program
#first it populates our task data and user data as global variables, by calling the data management functions
#then it runs the login process and sets username of the logged in user as a global variable
#finally it calls the main menu loop of the program
def main():
    global task_dict
    task_dict = get_tasks()
    global user_dict
    user_dict = get_users()
    global user_name
    user_name=login()
    menu()

"""++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""
###we call main function
main()


