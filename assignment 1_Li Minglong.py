# Name: Li Minglong
# Assignment One
# ddl is 22/9/2026 23:59pm

# Task A: Simple Calculator
def run_calculator():
    print("\nSimple Calculator")

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
def run_qa_bot():
    print("\nQuestion Answering Bot")
    question_count = 0
    topics = "hello, python, jetson, ai, or name"

    while True:
        if question_count == 0:
            question = input(f"Ask me about {topics}: ").strip().lower()
        else:
            question = input(
                f"Ask me about {topics} (type 'exit' to end): "
            ).strip().lower()

        if question_count > 0 and question == "exit":
            print(f"You asked {question_count} question(s). Goodbye!")
            break

        question_count += 1

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


while True:
    print("\nAssignment 1 Menu")
    print("1. Simple Calculator")
    print("2. Question Answering Bot")
    print("0. Exit Program")
    choice = input("Choose an option: ").strip()

    if choice == "1":
        run_calculator()
    elif choice == "2":
        run_qa_bot()
    elif choice == "0":
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please enter 1, 2, or 0.")
