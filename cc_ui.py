'''
To-do list:
- Handle incorrect deptcode by checking if any number in it or check if in existing list of deptcodes
'''

def welcome_message():
    print("\nWelcome to Commutr Course on Python!\n")
    print("Given a set of classes from you, we'll construct an optimal commuter schedule for you!")
    print("Classes will be optimized prioritizing being on campus for the least amount of days,\nand then by being on campus for the least amount of time.")
    print()

def prompt_classes():
    class_list = []

    print(f"Class {len(class_list) + 1} Information")
    deptcode = input("Department code (EX: COMPSCI, ICS, MATH): ")
    if deptcode == "ICS":
        deptcode = "I&C SCI"
    coursenum = input("Course number (EX: 161, 31, 2A): ")
    class_list.append((deptcode, coursenum))

    while True:
        answer = input("\nWould you like to add more classes? (Y/N): ")
        while answer.upper() not in ["Y", "N"]:
            print("Incorrect input! Please input only Y or N.")
            answer = input("\nWould you like to add more classes? (Y/N): ")
        if answer.upper() == "N":
            break
        print(f"\nClass {len(class_list) + 1} Information")
        deptcode = input("Department code (EX: COMPSCI, ICS, MATH): ")
        if deptcode == "ICS":
            deptcode = "I&C SCI"
        coursenum = input("Course number (EX: 161, 31, 2A): ")
        class_list.append((deptcode, coursenum))

    return class_list

def print_schedule(schedule: list[dict]):
    if schedule == []:
        print("There is no possible schedule in which your classes do not overlap.")
    for course in schedule:
        print(f"\n{course['days']} {course['display_time'].lstrip()}")
        print(f"{course['sectionType']}: {course['course_title']}")
        print(f"{course['name']}")
        print(f"{course['sectionCode']}")
    print()

def schedule_stats(schedule_tuple: tuple):
    print(f"{schedule_tuple[1]} day(s) on campus each week.")
    seconds = schedule_tuple[2]
    print(f"{seconds // 3600} hour(s), {(seconds % 60)//60} minutes, and {(seconds % 3600)} seconds spent on campus each week.")
