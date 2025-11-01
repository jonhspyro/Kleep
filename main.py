from kleep.core.handle_info import kleep
import sys

def handle_command(command: str):
    """
    Handle user commands.
    """
    match command:
        case "kleep":
            try:
                kleep()
            except Exception as e:
                print(f"\n[!] Error while running Kleep: {e}\n")
        case "quit":
            print("Exiting Kleep... See you later!")
            sys.exit(0)
        case _:
            print("Invalid command, type 'kleep' or 'quit'.")

def main():

    print("Welcome to Kleep!\n")

    while True:
        try:
            command = input("Enter command ( kleep | quit ): ").strip().lower()
            handle_command(command)
        except (KeyboardInterrupt, EOFError):
            print("\nExiting without Kleeping :(")
            sys.exit(0)

if __name__ == "__main__":
    if getattr(sys, "frozen", False):
        if hasattr(sys, "_kleep_already_running"):
            sys.exit(0)
        sys._kleep_already_running = True
    main()



    