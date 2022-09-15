def welcome_message():
    print("Welcome to Commutr Course on Python!")

def print_schedule(schedule: list[dict]):
    for course in schedule:
        print(f"{course['days']} {course['display_time'].lstrip()}")
        print(f"{course['sectionType']}: {course['course_title']}")
        print(f"{course['name']}")
        print(f"{course['sectionCode']}")
        print()
