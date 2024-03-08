from address_book import AddressBook, Record
from datetime import datetime, timedelta


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"Give me the necessary and correct data."
        except KeyError as e:
            return f"Contact {e} not found."
        except IndexError:
            return "Incomplete command."
    return inner

@input_error
def add_contact(args, book):
    username, *phones = args
    if len(args) < 2:
        raise ValueError
    if username in book:
        return 'This name was added. Please enter another name or use the command "change".'
    for phone in phones:
        is_duplicate = False
        for record in book.values():
            if phone in [p.value for p in record.phones]:
                is_duplicate = True  
                break 
        if is_duplicate:
            return "This number was saved with another name."
    else:
        contact = Record(username)
        for phone in phones:
            contact.add_phone(phone)
        book.add_record(contact)
        return "Contact added."

@input_error
def change_contact(args, book: AddressBook):
    username, old_phone, new_phone = args    
    if username not in book.data:
        raise KeyError(username)
    record = book.find(username)
    if new_phone in book.values():
        return f"This number was saved with another name."
    if not new_phone.isdigit() or not (len(new_phone) == 10):
        return 'Enter the correct phone in number format from 5 to 12 characters.'  
    if old_phone not in [phone.value for phone in record.phones]:
        return "Old phone number does not match any phone number associated with this contact."
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."

@input_error          
def show_phone(args, book: AddressBook):
    username = args[0]
    if username in book:
        record = book.find(username)
        return '; '.join(phone.value for phone in record.phones)
    else:
        raise KeyError(username)

@input_error
def show_all(book):
    if book:
       return '\n'.join([str(record) for record in book.values()])
    else:
       return 'Your contact list is empty.'  

@input_error
def add_birthday( args, book ):
    username, birthday = args
    if username not in book.data:
        raise KeyError(username)
    birthday = datetime.strptime(birthday, "%d.%m.%Y").date()
    today = datetime.today().date() 
    if birthday > today:
        return 'You specified a date in the future'
    if birthday < datetime.strptime('01.01.1900', "%d.%m.%Y").date():
        return "Write correct birthday's day after 01.01.1900"
    record = book.find(username)
    return record.add_birthday(birthday.strftime("%d.%m.%Y"))

@input_error
def show_birthday(args, book):
    username = args[0]
    if username not in book.data:
        raise KeyError(username)
    record = book.find(username)
    try:
        return f"The birthday {record.name} is {record.birthday.value}"
    except:
        return 'Contact is missing birthday'




@input_error
def birthdays_next_week(book):
    return book.get_birthdays_per_week()

def delete_contact(args, book):
    username = args[0]
    if username not in book.data:
        raise KeyError(username)
    record = book.delete(username)
    return 'Contact deleted'


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
            print(add_birthday(args, contacts))
        elif command == 'show-birthday':
            print(show_birthday(args, contacts))
        elif command == 'birthdays':
            print(contacts.get_birthdays_per_week())
        elif command == 'delete':
            print(delete_contact(args, contacts))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()