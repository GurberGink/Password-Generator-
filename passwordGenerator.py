# Required imports 
import secrets
import pandas as pd
from openpyxl.utils import get_column_letter
from datetime import datetime
from pathlib import Path

# Character pools
upper_letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") 
lower_letters = list("abcdefghijklmnopqrstuvwxyz") 
digits = list("0123456789") 
special_char = ['!','#','$','%','&','(',')','*','+','-','.','/']

# Generates a secure password of given length
def generate_password(length : int) -> str:
    
    # Validation check: Password must be at least four characters
    if length < 4:
        raise ValueError("Enter a value of at least [4] or greater: ")
    
    # Ensures at least one character from each category
    characters = [
        secrets.choice(upper_letters),
        secrets.choice(lower_letters),
        secrets.choice(digits),
        secrets.choice(special_char),
    ]
    
    # Combined pool of all allowed characters for random selection
    all_characters = upper_letters + lower_letters + digits + special_char
    
    # Fill remaining length with random characters 
    for _ in range(length - 4):
        characters.append(secrets.choice(all_characters))
        
        
    # Fisher Yates shuffle for unbiased randomness
    for i in range((length)-1, 0, -1):
        j = secrets.randbelow(i + 1)
        characters[i], characters[j] = characters[j], characters[i]
        
    # Convert character list into a single string password    
    return "".join(characters)

# Automatically resize Excel columns based on their content
def autosize_columns(df, ws):
    
    # Iterate through DataFrame columns with 1-based index for Excel
    for i, col in enumerate(df.columns, 1):
        
        # Determine max width from column data or header
        max_length = max(df[col].astype(str).map(len).max(), len(col))
        
        # Apply width with small padding
        ws.column_dimensions[get_column_letter(i)].width = max_length + 2

def main():
    
    # Prompt user for the website associated with the password
    website = input("Please enter the website/link you would like the password to correlate to: ")
    
    # Loop until valid password length is entered
    while True:
        try:
             # Attempt to convert user input to an integer
            length = int(input("What is the desired length of the password? Minimum length =  [4]: "))
            
            # Enforce minimum length requirement
            if length < 4:
                
                print("The length must be at least [4]")
                # ask again if too short
                continue 
            # exit loop when valid
            break
        
        # Handle non-numeric input
        except ValueError:
            print("Please enter a numerical character with the value of at least [4]")
            
    # Generate password using validated length
    generated_password = generate_password(length)
    
    # Display result to user
    print("Generated password: ", generated_password)
    
    # Path to the Excel file where passwords are stored
    excel_path = Path("Password_log.xlsx")
    
    # Name of the worksheet inside the Excel file
    sheet_name = "Sheet1"
    
    # Create a one-row DataFrame representing the new log entry
    #Includes current timestamp, website, and generated password
    new_row = pd.DataFrame([{
        "Timestamp" : datetime.now().isoformat(timespec = "Seconds"),
        "Website" : website,
        "Password" : generated_password
    }])
    
    # Check if the Excel file already exists on disk
    if excel_path.exists():
        try:
            # Read the existing sheet into a DataFrame
            df_existing = pd.read_excel(excel_path, sheet_name=sheet_name)

            # Combine old data with the new row (stack rows)
            # ignore_index=True resets row numbering cleanly
            df_final = pd.concat([df_existing, new_row], ignore_index=True)

        # If the sheet name doesn't exist or can't be read
        except ValueError:
            # Fall back to using only the new row
            df_final = new_row

        # Open Excel in append mode (file already exists)
        mode = "a"

        # When writing, replace the sheet's contents with df_final
        if_sheet_exists = "replace"

    # If the Excel file does NOT exist
    else:
        # No previous data, so final data is just the new row
        df_final = new_row

        # Create a brand-new Excel file
        mode = "w"

        # No sheet-existence rule needed in write mode
        if_sheet_exists = None
         



    