import cc_ui
import request
import respond

if __name__ == "__main__":
    schedule_num = 0
    cc_ui.welcome_message()
    course_list = cc_ui.prompt_classes()
    json_data = respond.get_course_info(course_list)
    schedules = respond.optimal_schedules(json_data)

    
    schedule_tuple = schedules[schedule_num]
    print("\nMost optimal schedule")
    print("muh time gap is", schedule_tuple[2])
    cc_ui.schedule_stats(schedule_tuple)
    cc_ui.print_schedule(schedule_tuple[0])

    while True:
        if input("Would you like to see the next optimal schedule? (Y/N): ").upper() == "N":
            break
        schedule_num += 1

        schedule_tuple = schedules[schedule_num]
        print(f"\nSchedule {schedule_num + 1}")
        print("muh time gap is", schedule_tuple[2])
        cc_ui.schedule_stats(schedule_tuple)
        cc_ui.print_schedule(schedule_tuple[0])

