from colorama import Fore, Style, init

def main():
    init(autoreset=True)
    print(f"{Fore.GREEN}{Style.BRIGHT}Hello, World!")
    print(f"{Fore.BLUE}This is a simple colorful console app!")

if __name__ == "__main__":
    main()
