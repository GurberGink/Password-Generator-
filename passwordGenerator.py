import secrets 

upperLetters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") 
lowerLetters = list("abcdefghijklmnopqrstuvwxyz") 
digits = list("0123456789") 
specialChar = ['!','#','$','%','&','(',')','*','+','-','.','/']

def generatePassword(length : int) -> str:
    if length < 4:
        raise ValueError("Enter a value greater than 4: ")
    
    characters = [
        secrets.choice(upperLetters),
        secrets.choice(lowerLetters),
        secrets.choice(digits),
        secrets.choice(specialChar),
    ]
    
    allCharacters = upperLetters + lowerLetters + digits + specialChar
    
    for _ in range(length - 4):
        characters.append(secrets.choice(allCharacters))
        
    for i in range((length)-1, 0, -1):
        j = secrets.randbelow(i + 1)
        characters[i], characters[j] = characters[j], characters[i]
        
    return "".join(characters)