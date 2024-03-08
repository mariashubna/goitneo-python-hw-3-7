from address_book import AddressBook, Record

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me correct data."
        except KeyError as e:
            return f"Contact {e} not found."
        except IndexError:
            return "Incomplete command."

    return inner

@input_error
def add_contact(args, book):
    username, phone = args
    if username in book:
        return 'This name was added. Please enter another name or use the command "change".'
    if phone in book.values():
        return "This number was saved with another name."
    else:
        contact = Record(username)
        contact.add_phone(phone)
        book.add_record(contact)
        return "Contact added."

@input_error
def change_contact(book: AddressBook, args):
    username, old_phone, new_phone = args
    if username not in book.data:
        raise KeyError(username)
    if new_phone in book.values():
        return f"This number was saved with another name."
    if not new_phone.isdigit() or not (len(new_phone) == 10):
        return 'Enter the correct phone in number format from 5 to 12 characters.'  
    if old_phone in book.values():
        record = book.find(username)
        record.edit_phone(old_phone, new_phone)
        return "Contact updated."

@input_error          
def show_phone(book: AddressBook, args):
    username = args[0]
    if username in book:
        record = book.find(username)
        return '; '.join(phone.value for phone in record.phones)
    else:
        raise KeyError(username)

@input_error
def show_all(book):
    if book:
       return '\n'.join([f"{name} : {phone}" for name, phone in book.items()])
    else:
       return 'Your contact list is empty.'  

@input_error
def add_birthday(book, args):
    username, birthday = args
    record = book.find(username)
    return record.add_birthday(birthday)

@input_error
def show_birthday(book, args):
    username = args[0]
    record = book.find(username)
    return record.show_birthday()

@input_error
def birthdays_next_week(book):
    return book.get_birthdays_per_week()


def main():
    contacts = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        elif command == 'add-birthday':
            print(add_birthday(args, AddressBook()))
        elif command == 'show-birthday':
            print(show_birthday(args, AddressBook()))
        elif command == 'birthdays':
            print(AddressBook().get_birthdays_per_week())
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()