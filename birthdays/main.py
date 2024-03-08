from datetime import datetime, timedelta

users_list = [
    {"name": "Bill Gates", "birthday": datetime(1955, 10, 28)},
    {"name": "Olga Ivanova", "birthday": datetime(1978, 2, 25)},
    {"name": "Mark Stown", "birthday": datetime(1999, 2, 21)},
    {"name": "Alina Snow", "birthday": datetime(1982, 2, 23)},
    {"name": "Malus Klein", "birthday": datetime(1988, 3, 1)},
    {"name": "Billy Snail", "birthday": datetime(1992, 3, 2)},
    {"name": "Anton Wills", "birthday": datetime(1994, 2, 28)},
]

birthday_day = {
    'Monday' : [],
    'Tuesday' : [],
    'Wednesday' : [],
    'Thursday' : [],
    'Friday' : [],
}

def get_birthdays_per_week(users):
    today = datetime.today().date() 
    end_of_week = today + timedelta(days=6)
    

    for user in users:
        user_birthday = user["birthday"].date() 
        birthday_this_year = user_birthday.replace(year=today.year)

        '''
            If today is Sunday, we don't include future Saturday in tomorrow Monday.
            If today is Monday, we don't include future Sunday in today.    
        '''     

        if today <= birthday_this_year <= end_of_week and not today.weekday() == 6 and not today.weekday() == 0:
            if birthday_this_year.weekday() == 1:
                birthday_day['Tuesday'].append(user['name'])
            elif birthday_this_year.weekday() == 2:
                birthday_day['Wednesday'].append(user['name'])
            elif birthday_this_year.weekday() == 3:
                birthday_day['Thursday'].append(user['name'])
            elif birthday_this_year.weekday() == 4:
                birthday_day['Friday'].append(user['name'])
            else:
                birthday_day['Monday'].append(user['name'])
        if today <= birthday_this_year <= end_of_week and today.weekday() == 6 or today.weekday() == 0:
            if birthday_this_year.weekday() == 1:
                birthday_day['Tuesday'].append(user['name'])
            elif birthday_this_year.weekday() == 2:
                birthday_day['Wednesday'].append(user['name'])
            elif birthday_this_year.weekday() == 3:
                birthday_day['Thursday'].append(user['name'])
            elif birthday_this_year.weekday() == 4:
                birthday_day['Friday'].append(user['name'])
            elif birthday_this_year.weekday() == 5:
                continue
            elif birthday_this_year.weekday() == 6:
                continue
            else:
                birthday_day['Monday'].append(user['name'])
            
    for day, names in birthday_day.items():
            if names:
                print(f"{day}: {', '.join(names)}")

    if not any(names for names in birthday_day.values()):
        print('No birthdays this week')
    


get_birthdays_per_week(users_list)