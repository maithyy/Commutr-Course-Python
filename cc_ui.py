def welcome_message():
    print("\nWelcome to Commutr Course on Python!\n")
    print("Given a set of classes from you, we'll construct an optimal commuter schedule for you!")
    print("Classes will be optimized prioritizing being on campus for the least amount of days,\nand then by being on campus for the least amount of time.")
    print()

def prompt_classes():
    class_list = []

    print(f"Class {len(class_list) + 1} Information")
    deptcode = input("Department code (EX: COMPSCI, ICS, MATH): ")
    coursenum = input("Course number (EX: 161, 31, 2A): ")
    class_list.append((deptcode, coursenum))

    while True:
        answer = input("\nWould you like to add more classes? (Y/N): ")
        if answer.upper() == "N":
            break
        print(f"\nClass {len(class_list) + 1} Information")
        deptcode = input("Department code (EX: COMPSCI, ICS, MATH): ")
        coursenum = input("Course number (EX: 161, 31, 2A): ")
        class_list.append((deptcode, coursenum))

    return class_list

def print_schedule(schedule: list[dict]):
    if schedule == []:
        print("There is no possible schedule in which your classes do not overlap.")
    for course in schedule:
        print("this da course!!!/n/n")
        print(course)
        print(f"{course['days']} {course['display_time'].lstrip()}")
        print(f"{course['sectionType']}: {course['course_title']}")
        print(f"{course['name']}")
        print(f"{course['sectionCode']}")
        print()
