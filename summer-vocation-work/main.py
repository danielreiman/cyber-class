# # Name: Daniel Reiman

def exAandB():
  number_input = input("Enter a number(5 digit number): ")
  number = int(number_input) # Get the intiger values in the input
  number_length = len(number_input) # Get the length of the input

  # B
  while number_length != 5:
    print("Invalid number, only number with 5 digits is acceptable") # Show invalid input message

    try:
      number_input = input("Try again, reenter a number (with 5 digit number): ")
      number = int(number_input)
    except:
      print("Error: The input is not a valid integer")

    number_length = len(number_input)

  # A1
  print("----- A1 -----")

  print(f"Number: {number}")

  # A2
  print("----- A2 -----")

  temp = number
  digit = 0
  for _ in range(5):
    digit = temp % 10 # Get the last digit of the number
    print(digit)
    temp //= 10  # Get the value as intiger (not as float)

  # A3
  print("----- A3 -----")

  sum = 0
  temp = number
  for _ in range(5):
    digit = temp % 10
    sum += digit
    temp //= 10 # Get the value as intiger (not as float)

  print(f"The sum of the digits in the number is {sum}")

def exC():
  text_input = input("Enter a text you want to translate to Bet Language: ")
  vowels = ['a', 'e', 'i', 'o', 'u']
  result = "" # The converted text will be stored here
  for letter in text_input:
    if letter in vowels: # Check if the letter is a vowel
      result += letter + "b" + letter
    else:
      result += letter

  print(result)

def exD():
  source_file_path = input("Enter a source file path (.txt): ")
  solutions_file_path = input("Enter a blank solutions file path (.txt): ")

  file_solutions = open(solutions_file_path, "w") # Open the solutions (blank) file for writing
  file_source = open(source_file_path, "r") # Open the source file for reading


  file_source_lines = file_source.readlines() # Read lines from the source file

  for line in file_source_lines:
    first_number, operator, second_number = line.split()
    first_number = int(first_number)
    second_number = int(second_number)
    if operator == "+":
      result = first_number + second_number
    elif operator == "-":
      result = first_number - second_number
    elif operator == "*":
      result = first_number * second_number
    elif operator == "/":
      try:
        result = first_number / second_number
      except ZeroDivisionError:
        result = "Error: Division by zero"
    else:
      result = "Error: Unknown operator (This program only recognize these operators: +, -, *, /)"
    file_solutions.write(f"{first_number} {operator} {second_number} = {result}" + "\n")
  file_solutions.close()

# Comment the function you don't want to run
if __name__ == "__main__":
  exAandB() # Exercises A (1-3) and B

  exC() # Exercise C

  exD() # Exercise D