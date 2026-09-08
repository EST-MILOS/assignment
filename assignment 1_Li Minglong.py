# Name: Li Minglong
# Assignment One
# ddl is 22/9/2026 23:59pm

# Task A: Simple Calculator
print("Simple Calculator")

try:
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))
    op = input("Choose operation (+, -, *, /): ").strip()

    if op == "+":
        print("Result:", num1 + num2)
    elif op == "-":
        print("Result:", num1 - num2)
    elif op == "*":
        print("Result:", num1 * num2)
    elif op == "/":
        if num2 == 0:
            print("Cannot divide by zero.")
        else:
            print("Result:", num1 / num2)
    else:
        print("Invalid operation")
except ValueError:
    print("Please enter valid numbers.")


# Task B: Question Answering Bot
print("\nQuestion Answering Bot")
question = input("Ask me something: ").strip().lower()

if "hello" in question:
    print("Bot: Hello! Nice to meet you.")
elif "python" in question:
    print("Bot: Python is a language.")
elif "jetson" in question:
    print("Bot: Jetson Nano is an AI computer.")
elif "ai" in question:
    print("Bot: AI means Artificial Intelligence.")
elif "name" in question:
    print("Bot: My name is Python Bot.")
else:
    print("Bot: Sorry, I don't understand.")
