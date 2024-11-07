     

# ........................................................................................................
# SQlite to make Database.................................................................................
# ........................................................................................................

import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)......................................
conn = sqlite3.connect('password_manager.db')
cursor = conn.cursor()

# Create the Users table..................................................................................
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL
)
''')

# Create the Services table..............................................................................
cursor.execute('''
CREATE TABLE IF NOT EXISTS services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    service_name TEXT NOT NULL,
    service_username TEXT NOT NULL,
    service_password TEXT NOT NULL,
    FOREIGN KEY (username) REFERENCES users(username)
)
''')

# Commit the changes and close the connection............................................................
conn.commit()
conn.close()

print("Database and tables created successfully.")


# Password_validator function............................................................................



def countlen(password):
    if len(password) >= 8 :       #.... len()....... function to check the lenth of a string
        return True 

def alphabet(password):
    if password.isalpha() :       #.... isalpha()....to check as if all characters of a string are alphabets
        return True 

def number(password):
    if password.isdigit() :       #.... isdigit().....to check as if all characters of a string are numbers
        return True

def alphanumeric(password) :      #.... isalnum().....to check as if all characters of a string are alphabet and numbers but not space or any fucking other character
    if password.isalnum():
        return True




def validator(password):
    if countlen(password) and alphanumeric(password) and not alphabet(password) and not number(password):
        return True
    else:
        return False

# hashing function .....................................................................................

import bcrypt

def hash_password(password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def verify_password(input_password, hashed_password):
    # Verify if the input password matches the hashed password
    return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password)


# profile menu to call add read and delete function on DB...............................................

def profile(username):
    print("press r to read")
    print("press a to add")
    print("press d to delete")
    print("press e to Exit") 
    
    profile_input = str(input())
    profile_menu_list = ["r", "a", "d" , "e"]
    while profile_input not in profile_menu_list :
        print("press r to read")
        print("press a to add")
        print("press d to delete")
        print("press e to Exit") 
        profile_input = str(input())    

    if profile_input == "r" :
        read_services(username)
       

    if profile_input == "a" :

        service_name = input("Enter the service name: ")
        service_username = input("Enter the service username: ")
        service_password = input("Enter the service password: ")
        add_service(username, service_name, service_username, service_password)
        
    if profile_input == "d" :
        
        service_name = input("Enter the service name you want to delete: ")
        delete_service(username , service_name)

    if profile_input == "e" :
        shot_down()

        
# Add function TO DB............................................................................

       
def add_service(username, service_name, service_username, service_password):
    # Connect to the SQLite database
    conn = sqlite3.connect('password_manager.db')
    cursor = conn.cursor()

    # Insert the service details into the Services table
    cursor.execute('''
        INSERT INTO services (username, service_name, service_username, service_password) 
        VALUES (?, ?, ?, ?)
    ''', (username, service_name, service_username, service_password))

    conn.commit()
    print(f"Service '{service_name}' added successfully for user '{username}'.")

    # Close the connection
    conn.close()

    profile(username)
           
# Read function from DB.........................................................................
    
def read_services(username):
    # Connect to the SQLite database
    conn = sqlite3.connect('password_manager.db')
    cursor = conn.cursor()

    # Retrieve all services for the specified user
    cursor.execute('''
        SELECT service_name, service_username, service_password 
        FROM services 
        WHERE username = ?
    ''', (username,))

    services = cursor.fetchall()

    if services:
        print(f"Services for user '{username}':")
        for service in services:
            print(f"Service Name: {service[0]}, Username: {service[1]}, Password: {service[2]}")

        profile(username)   
    else:
        print(f"No services found for user '{username}'.")
        

    # Close the connection
    conn.close()
    
    profile(username)

# delete function from DB........................................................................

def delete_service(username, service_name):
    # Connect to the SQLite database
    conn = sqlite3.connect('password_manager.db')
    cursor = conn.cursor()

    # Delete the specified service for the user
    cursor.execute('''
        DELETE FROM services 
        WHERE username = ? AND service_name = ?
    ''', (username, service_name))

    if cursor.rowcount > 0:
        print(f"Service '{service_name}' has been deleted successfully for user '{username}'.")
        pass
    else:
        print(f"Service '{service_name}' not found for user '{username}'.")

    conn.commit()
    # Close the connection
    conn.close()

    profile(username)


# Shotdown function to exit the program...........................................................

def shot_down() :
      print("are you sure ? ")  
      print("press y : yes    press n : no")
      E = str(input())
      shot_down_list = [ "y" , "n"]
      while E not in shot_down_list :
          print("  y   or    n  ")
          E = str(input())
      if E == "y" :
          
      
          exit()
      if E == "n" :
          main_menu()
      

# Sign_in function based on SQlite DB............................................................

    
def sign_in(username, input_password):
    # Connect to the SQLite database
    conn = sqlite3.connect('password_manager.db')
    cursor = conn.cursor()

    # Check if the username exists and retrieve the password
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    
    hashed_password =  cursor.fetchone()

    
    print(hashed_password)
    
    verify_password(input_password,hashed_password[0])

    print(verify_password(input_password,hashed_password[0]))

    if verify_password(input_password,hashed_password[0]) == True :
        print("sign in successful ! wellcome, " + username )
        profile(username)

    else :
        print("invalid username or password. please try again ")
        username = str(input("Enter your username: "))
        input_password = str(input("Enter your password: "))
        sign_in(username, input_password)

           


# Sign_up function based on SQlite DB............................................................

            
def sign_up(username, password):
    # Connect to the SQLite database
    conn = sqlite3.connect('password_manager.db')
    cursor = conn.cursor()

    # Check if the username already exists
    cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        print("Username already exists. Please choose a different username.")
    else:
        # Insert the new user into the Users table and hash related password
        hashed_password = hash_password(password)
        print("Hashed Password:", hashed_password)
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        print("User registered successfully!")

    # Close the connection
    conn.close()
    main_menu()
    
    
# main menu ....................................................................................

def main_menu():
    print("sign in: press 1   sign up: press 2   exit: press 3") 

# this piece of code limits input to 1 or 2 or 3................................................

    main_menu_input = str(input())
    main_menu_list = [ "1", "2", "3" ]
    while main_menu_input not in main_menu_list :
        print("sign in: press 1   sign up: press 2   exit: press 3") 
        main_menu_input = str(input())
        
           
# option for sign-in ...........................................................................
        
    if main_menu_input == "1":
        
        username = str(input("Enter your username: "))
        input_password = str(input("Enter your password: "))
        sign_in(username, input_password)  


# option for sign-up ...........................................................................
            
    if main_menu_input == "2":
        
        username = str(input("Choose a username: "))
        password = str(input("enter your password : "))
        
        print(validator(password)) # this peace of code exhibits a visual output for the returned True or False by validator function

       
    
        while validator(password) == False :
            
            print("your password must be minimum 8 character and consists of alphabets and numbers only")
            username = str(input("Choose a username: "))
            password = str(input("enter your password : "))
            validator(password)
            
        else :
            
            print("your password is eligible")  # if password is eligible then you can turn the wheel (calling another function) by this pattern
            sign_up(username, password)

            


# option for shoting down .......................................................................

    if main_menu_input == "3":
        shot_down()
        

###>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>########
###>>>>>>>>>>>>>>>>>>>>>>>>>>>>> program starts here >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>########
###>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>########
        
main_menu()






    
