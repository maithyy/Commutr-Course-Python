from cc_ui import welcome_message
import cc_request


import cc_ui as UI

if __name__ == "__main__":
    UI.welcome_message()
    class_list = UI.prompt_classes()
    #print(cc_request.encode_url(class_list))