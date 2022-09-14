from re import X
import urllib.request
import urllib.error
from pathlib import Path
import json
import sys
from itertools import combinations, product

def get_from_web(url: str) -> dict or list:
    '''
    Requests JSON formatted data from the API identified by the
    given URL and returns the data as a Python object
    '''
    response = None

    try:
        request = urllib.request.Request(url)

        response = urllib.request.urlopen(request)

    except urllib.error.HTTPError as exception:
        print_web_error_message(exception.getcode(), url, 'NOT 200')

    except (urllib.error.URLError, ValueError):
        print_web_error_message(None, url, 'NETWORK')

    try:
        json_data = response.read().decode(encoding='utf-8')
        data = _convert_data(json_data)
        return data

    except (json.JSONDecodeError, ValueError):
        print_web_error_message(response.getcode(), url, 'FORMAT')

    finally:
        if response:
            response.close()
            
    
def print_web_error_message(status: int or None, url: str, error: str) -> None:
    '''
    Prints failure message identifying the status of the HTTP request, if applicable,
    and the specific URL and error that caused failure
    '''
    print('FAILED')
    if status is not None:
        print(f'{status} {url}')
    else:
        print(url)
    print(error)
    sys.exit(1)
    
def _convert_data(data: str):
    '''Converts the given JSON formatted data to a Python object'''
    converted_data = json.loads(data)

    # Raises ValueError if json.loads returns an empty object
    if not converted_data:
        raise ValueError
    return converted_data 
'''
To-do
- rework convert time
- rework time overlap
'''

def convert_time(time: str): #time is in str format 5:00p and then converted to 1700, edge cases- no leading 0
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

    return (start_num*60+start_min, end_num*60+end_min)



def time_overlap(course_1, course_2):  # time is in ' 5:00- 5:50p'
    if course_1 == [] or course_2 == []:
        return False

    s_1, e_1 = course_1['times']
    s_2, e_2 = course_2['times']

    return s_1 <= s_2 <= e_1 or s_2 <= s_1 <= e_2  



def course_info(data):
    course_sections = {}

    sections = data['schools'][0]['departments'][0]['courses'][0]['sections']

    
    for sect in sections:
        
        section_num = sect['sectionNum']
        section_code = sect['sectionCode']
        section_type = sect['sectionType']
        days = sect['meetings'][0]['days']
        times = sect['meetings'][0]['time']
        display_time = sect['meetings'][0]['time']
        instructor_name = sect['instructors'][0]
        building = sect['meetings'][0]['bldg']
        section_type = sect['sectionType']
        course_title = data['schools'][0]['departments'][0]['courses'][0]['courseTitle']
        
        if section_type not in

        '''
        if times == "TBA":
            return [[],[]]
        
        times = convert_time(times)

        details = {
            'sectionNum': section_num,
            'sectionCode': section_code,
            'sectionType': section_type,
            'days': days,
            'times': times,
            'display_time': display_time,
            'instructor_name': instructor_name,
            'building': building,
            'section_type': section_type,
            'course_title': course_title
            }
        '''

    return course_sections


# def course_info(data):
#     course_sections = []

#     sections = data['schools'][0]['departments'][0]['courses'][0]['sections']
#     inner = []
#     secondary = []
#     starting_section = "A"
    
#     for sect in sections:
#         section_num = sect['sectionNum']
#         section_code = sect['sectionCode']
#         section_type = sect['sectionType']
#         days = sect['meetings'][0]['days']
#         times = convert_time(sect['meetings'][0]['time'])
#         if section_num.isnumeric():
#             section_num = starting_section + section_num
#         details = {
#             'sectionNum': section_num,
#             'sectionCode': section_code,
#             'sectionType': section_type,
#             'days': days,
#             'times': times
#             }
        
#         if section_num.isalpha():
#             if secondary:
#                 inner.append(secondary)
#                 course_sections.append(inner)
#                 inner = []
#             starting_section = section_num
#             inner.append(details)
#             secondary = []
#         else:
#             secondary.append(details)

#     if not course_sections:
#         return [[details, secondary]]
    
#     return course_sections


def create_course_combos(course_names):
    course_combos = []
    for course_name in course_names:
        possibles = []
        for lec, discussions_list in course_name:
            if discussions_list:
                for discussion in discussions_list:
                    possibles.append([lec, discussion])
            else:
                possibles.append([lec])
        course_combos.append(possibles)
    return course_combos


def possible_schedules(course_combos):
    possible = []
    for schedule in product(*course_combos):
        # checks overlap for all combos
        # assumes 3 courses

        if len(schedule[0]) == 1:
            schedule[0].append([])
        if len(schedule[1]) == 1:
            schedule[1].append([])
        if len(schedule[2]) == 1:
            schedule[2].append([])

        if not (time_overlap(schedule[0][0], schedule[1][0])
                or time_overlap(schedule[0][0], schedule[1][1])
                or time_overlap(schedule[0][0], schedule[2][0])
                or time_overlap(schedule[0][0], schedule[2][1])

                or time_overlap(schedule[0][1], schedule[1][0])
                or time_overlap(schedule[0][1], schedule[1][1])
                or time_overlap(schedule[0][1], schedule[2][0])
                or time_overlap(schedule[0][1], schedule[2][1])

                or time_overlap(schedule[1][0], schedule[2][0])
                or time_overlap(schedule[1][0], schedule[2][1])

                or time_overlap(schedule[1][1], schedule[2][0])
                or time_overlap(schedule[1][1], schedule[2][1])
        ):
            possible.append(schedule)

    return possible

def get_time_days(schedule):
    total_time = 0
    days = 0
    
    day_times = {'M':[], 'Tu':[], 'W':[], 'Th':[], 'F':[]}
    # day_gaps = {'M':[], 'Tu':[], 'W':[], 'Th':[], 'F':[]}
    
    for course in schedule:
        for key in day_times:
            if key in course[0]['days']:
                day_times[key].append(course[0]['times'])

    for times in day_times.values():
        if times:
            days += 1
            times.sort()
            total_time += times[-1][1] - times[0][0]

    return schedule, days, total_time/days 

def optimized_schedules(possible_schedules):
    schedules_data = []
    for schedule in possible_schedules:
        schedules_data.append(get_time_days(schedule))

    schedules_data = sorted(schedules_data, key=lambda x: x[1], reverse= True)
    schedules_data = sorted(schedules_data, key=lambda x: x[2])
    
    return schedules_data


course_1 = course_info(get_from_web('https://api.peterportal.org/rest/v0/schedule/soc?term=20222%20Fall&department=CHEM&courseNumber=1C'))
course_2 = course_info(get_from_web('https://api.peterportal.org/rest/v0/schedule/soc?term=20222%20Fall&department=ANTHRO&courseNumber=2A'))
course_3 = course_info(get_from_web('https://api.peterportal.org/rest/v0/schedule/soc?term=20222%20Fall&department=HISTORY&courseNumber=15C'))

print(course_1)

'''

x = create_course_combos([course_1, course_2, course_3])
y = possible_schedules(x)

# for i in product(*x):
#     print(i)

for s in possible_schedules(x):
    print(s)

# for s in possible_schedules(x):
#     print(get_time_days(s))

'''