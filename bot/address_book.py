from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, name):
        super().__init__(name)

class Phone(Field):
    def __init__(self, phone):
        if len(phone) == 10:
            super().__init__(phone)
        else:
            raise ValueError('Enter the correct phone in number format 10 characters.')

class Birthday(Field):
    def __init__(self, birthday):
        try:
            datetime.strptime(birthday, "%d.%m.%Y")
            super().__init__(birthday)
        except ValueError:
            raise ValueError("Invalid date format. Please use DD.MM.YYYY")
        

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, *phones):
        for phone in phones:
            self.phones.append(Phone(phone))
    
    def edit_phone(self, old_phone, new_phone):
        for number in self.phones:
            if number.value == old_phone:
                number.value = new_phone
                return
    
    def remove_phone(self, phone):
        for number in self.phones:
            if number.value == phone:
                self.phones.remove(phone) 
                return 'Phone number was removed'            
            else:
                raise KeyError("The specified phone number doesn't exist.")
    
    def add_birthday(self, birthday):
        try:
            self.birthday = Birthday(birthday)
            return 'Birthday added'
        except ValueError:
            return "Use date format DD.MM.YYYY"

    def __str__(self):
            return f"{self.name.value} : {'; '.join(p.value for p in self.phones)}"
        

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            return self.data.get(name)
        else:
            raise KeyError("The specified name doesn't exist.")
    
    def delete(self, name):
        if name in self.data:
            self.data.pop(name)
        else:
            raise KeyError("The specified name doesn't exist.")
    
    
    def get_birthdays_per_week(self):
        today = datetime.today().date() 
        end_of_week = today + timedelta(days=6)    

        birthdays = {
            'Monday' : [],
            'Tuesday' : [],
            'Wednesday' : [],
            'Thursday' : [],
            'Friday' : [],
            }

        for user in self.data.values():
            user_birthday = datetime.strptime(user.birthday.value, "%d.%m.%Y").date()
            birthday_this_year = user_birthday.replace(year=today.year)    

            if today <= birthday_this_year <= end_of_week and not today.weekday() == 6 and not today.weekday() == 0:
                if birthday_this_year.weekday() == 1:
                    birthdays['Tuesday'].append(user.name.value)
                elif birthday_this_year.weekday() == 2:
                    birthdays['Wednesday'].append(user.name.value)
                elif birthday_this_year.weekday() == 3:
                    birthdays['Thursday'].append(user.name.value)
                elif birthday_this_year.weekday() == 4:
                    birthdays['Friday'].append(user.name.value)
                else:
                    birthdays['Monday'].append(user.name.value)
            elif today <= birthday_this_year <= end_of_week and today.weekday() == 6 or today.weekday() == 0:
                if birthday_this_year.weekday() == 1:
                    birthdays['Tuesday'].append(user.name.value)
                elif birthday_this_year.weekday() == 2:
                    birthdays['Wednesday'].append(user.name.value)
                elif birthday_this_year.weekday() == 3:
                    birthdays['Thursday'].append(user.name.value)
                elif birthday_this_year.weekday() == 4:
                    birthdays['Friday'].append(user.name.value)
                elif birthday_this_year.weekday() == 5:
                    continue
                elif birthday_this_year.weekday() == 6:
                    continue
                else:
                    birthdays['Monday'].append(user.name.value)
                
        result = ""
        for day, names in birthdays.items():
            if names:
                result += f"{day}: {', '.join(names)}\n"
        result = result.rstrip()
        

        if not any(names for names in birthdays.values()):
            return 'No birthdays this week'

        return result 
    

