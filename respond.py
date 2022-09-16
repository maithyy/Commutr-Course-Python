import process
import request

def get_course_info(course_list: list) -> list:
    json_list = []
    for course in course_list:
        json_list.append(process.course_info(request.get_from_web(request.encode_url(course))))
    return json_list

def optimal_schedules(json_list: list) -> tuple:
    return process.optimized_schedules(process.possible_schedules(process.create_course_combos(json_list)))


    