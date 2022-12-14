from request import get_from_web
from itertools import product
import cc_ui as UI

'''
To-do
- handle no data from api
- figure out ics link i 4got lolz I%26C%20SCI
'''

def course_info(data) -> dict:
    '''
    Given a json dict, return a dictionary where the
    keys correspond to different section types
    and the values are lists of dictionaries
    of the specific section.
    '''
    course_sections = {}
    sections = data['schools'][0]['departments'][0]['courses'][0]['sections']
    name = f"{data['schools'][0]['departments'][0]['courses'][0]['deptCode']} {data['schools'][0]['departments'][0]['courses'][0]['courseNumber']}"

    for sect in sections:
        section_num = sect['sectionNum']
        section_code = sect['sectionCode']
        section_type = sect['sectionType']
        days = sect['meetings'][0]['days']
        times = sect['meetings'][0]['time']
        display_time = sect['meetings'][0]['time']
        instructor_name = sect['instructors'][0]
        building = sect['meetings'][0]['bldg']
        course_title = data['schools'][0]['departments'][0]['courses'][0]['courseTitle']

        if times != "TBA":
            times = convert_time(times)
        else:
            times = (-1, -1)
        
        details = {
            'name': name,
            'sectionNum': section_num,
            'sectionCode': section_code,
            'sectionType': section_type,
            'days': days,
            'display_time': display_time,
            'times': times,
            'instructor_name': instructor_name,
            'building': building,
            'course_title': course_title
            }
        
        if section_type not in course_sections:
            course_sections[section_type] = [details]
        else:
            course_sections[section_type].append(details)

    return course_sections


def create_course_combos(all_courses: list) -> list:
    '''
    Given a list of all the course info dictionaries, return a nested list of course combinations.
    '''
    answer = []
    for course in all_courses:
        answer.append(list(product(*course.values())))
    return answer

def _flatten(course_combos):
    '''
    Flattens nested tuples of lists to a single list of schedule dictionaries.
    '''
    if type(course_combos) != dict and list(course_combos) == []:
        return []
    elif type(course_combos) == dict:
        return [course_combos]
    if type(course_combos) != dict:
        return _flatten(course_combos[0]) + _flatten(course_combos[1:])
    return course_combos[:1] + _flatten(course_combos[1:])

def convert_time(time: str) -> tuple:
    '''
    Given a string in the example form ' 5:00-7:00p', return a two tuple consisting of the start and end time in seconds.
    '''
    if time[-1] == 'p':
        start, end = time[:-1].split('-')
    else:
        start,end = time.split('-')
    start_num = int(start.split(':')[0].strip())
    start_min = int(start.split(':')[1].strip())
    end_num = int(end.split(":")[0].strip())
    end_min = int(end.split(':')[1].strip())
        
    if time[-1] == 'p':
        if start_num <= end_num:
            start_num += 12
        end_num += 12

    return ((start_num*60*60)+(start_min * 60), (end_num*60*60)+(end_min*60))

def time_overlap(course_1: dict, course_2: dict) -> bool:
    '''
    Given two course schedule dictionaries, return True if their times overlap and False otherwise.
    '''
    if "TBA" in [course_1['display_time'], course_2['display_time']]:
        return False

    s_1, e_1 = convert_time(course_1['display_time'])
    s_2, e_2 = convert_time(course_2['display_time'])
    
    return s_1 <= s_2 <= e_1 or s_2 <= s_1 <= e_2  

def check_possible(schedule: list) -> bool:
    '''
    Given a schedule (list of different classes with its own dictionary),
    return False if the schedule has a time overlap, else True.
    '''
    for i in range(len(schedule)):
        for j in range(i + 1, len(schedule)):
            if time_overlap(schedule[i], schedule[j]):
                return False
    return True

def possible_schedules(course_combos: list) -> list:
    '''
    Given a list of schedules (list of different classes with its own dictionary),
    returns a list of possible schedules.
    '''
    possible = []
    for schedule in product(*course_combos):
        schedule = _flatten(schedule)
        if check_possible(schedule):
            possible.append(schedule)
    return possible

def get_time_days(schedule) -> tuple:
    '''
    Given a schedule (list of different classes with its own dictionary),
    returns the schedule, the number of days on campus it requires you,
    and the combined time it requires you to be on campus.
    '''
    time_gap = 0
    days_on_campus = 0
    day_times = {"M": [], "Tu": [], "W": [], "Th": [], "F": []}

    for day in day_times:
        for course in schedule:
            if day in course['days']:
                day_times[day].append(course)
    
    for day in day_times.values():
        if day:
            latest = max(course['times'][1] for course in day)
            earliest = min(course['times'][0] for course in day)
            time_gap += (latest-earliest)
    
    for lst in day_times.values():
        if lst:
            days_on_campus += 1

    return schedule, days_on_campus, time_gap

def optimized_schedules(possible_schedules: list) -> list:
    '''
    Given a list of possible schedules, returns a list
    sorted by most optimal (least days on campus and
    then least time on campus).
    '''
    schedules_data = []
    for schedule in possible_schedules:
        schedules_data.append(get_time_days(schedule))

    schedules_data = sorted(schedules_data, key=lambda x: x[2])
    schedules_data = sorted(schedules_data, key=lambda x: x[1])
    
    return schedules_data

if __name__ == "__main__":
    print(convert_time(" 5:00-7:00p"))
    '''
    course_1 = course_info(get_from_web('https://api.peterportal.org/rest/v0/schedule/soc?term=20222%20Fall&department=STATS&courseNumber=67'))
    course_2 = course_info(get_from_web('https://api.peterportal.org/rest/v0/schedule/soc?term=20222%20Fall&department=I%26C%20SCI&courseNumber=6B'))
    course_3 = course_info(get_from_web('https://api.peterportal.org/rest/v0/schedule/soc?term=20222%20Fall&department=COMPSCI&courseNumber=122A'))
    course_4 = course_info(get_from_web('https://api.peterportal.org/rest/v0/schedule/soc?term=20222%20Fall&department=IN4MATX&courseNumber=43'))

    x = create_course_combos([course_1, course_2, course_3, course_4])
    y = possible_schedules(x)
    z = optimized_schedules(y)

    UI.print_schedule(z[0][0])
    '''