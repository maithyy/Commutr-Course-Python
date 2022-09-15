from re import L, X
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
- handle no data from api
- figure out ics link i 4got lolz
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

    return (start_num*60*60+start_min, end_num*60*60+end_min)



def time_overlap(course_1, course_2):  # time is in ' 5:00- 5:50p'
    if "TBA" in [course_1['display_time'], course_2['display_time']]:
        return False

    s_1, e_1 = convert_time(course_1['display_time'])
    s_2, e_2 = convert_time(course_2['display_time'])

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
        course_title = data['schools'][0]['departments'][0]['courses'][0]['courseTitle']

        if times != "TBA":
            times = convert_time(times)
        else:
            times = (-1, -1)
        
        details = {
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


def create_course_combos(all_courses):
    answer = []
    for course in all_courses:
        answer.append(list(product(*course.values())))
    return answer

def _flatten(course_combos):
    if type(course_combos) != dict and list(course_combos) == []:
        return []
    elif type(course_combos) == dict:
        return [course_combos]
    if type(course_combos) != dict:
        return _flatten(course_combos[0]) + _flatten(course_combos[1:])
    return course_combos[:1] + _flatten(course_combos[1:])

def check_possible(schedule):
    for i in range(len(schedule)):
        for j in range(i + 1, len(schedule)):
            if time_overlap(schedule[i], schedule[j]):
                return False
    return True


def possible_schedules(course_combos):
    possible = []
    for schedule in product(*course_combos):
        schedule = _flatten(schedule)
        if not check_possible(schedule):
            possible.append(schedule)

    return possible

def get_time_days(schedule):
    total_time = 0
    time_gap = 0
    
    day_times = {}

    for course in schedule:
        if course['days'] in day_times:
            day_times[course['days']].append(course)
        else:
            day_times[course['days']] = [course]
    
    for day in day_times.values():
        latest = max(course['times'][1] for course in day)
        earliest = min(course['times'][0] for course in day)
        time_gap += (latest-earliest)

    return schedule, len(day_times), time_gap

def optimized_schedules(possible_schedules):
    schedules_data = []
    for schedule in possible_schedules:
        schedules_data.append(get_time_days(schedule))

    schedules_data = sorted(schedules_data, key=lambda x: x[1], reverse= True)
    schedules_data = sorted(schedules_data, key=lambda x: x[2])
    
    return schedules_data


course_1 = course_info(get_from_web('https://api.peterportal.org/rest/v0/schedule/soc?term=20222%20Fall&department=HIST&courseNumber=15C'))
course_2 = course_info(get_from_web('https://api.peterportal.org/rest/v0/schedule/soc?term=20222%20Fall&department=I%262%SCI&courseNumber=51'))
course_3 = course_info(get_from_web('https://api.peterportal.org/rest/v0/schedule/soc?term=20222%20Fall&department=I%262%SCI&courseNumber=45C'))

x = create_course_combos([course_1, course_2, course_3])
y = possible_schedules(x)
z = optimized_schedules(y)

print(z[0])