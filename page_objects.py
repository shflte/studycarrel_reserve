import arrow

class LOGIN_PAGE:
    username_input = "//input[@name='username']"
    password_input = "//input[@name='password']"

    captcha_img = "//img[@id='captcha_img']"
    captcha_input = "//input[@name='captcha_value']"

    submit_button = "//input[@type='submit']"

class RESERVED_LIST_PAGE:
    iframe = "//iframe"
    add_button = "//input[@name='addbtn']"
    del_button = "//input[@name='delbtn']"

class RESERVE_RELATED_PAGE:
    # notice
    carrel_room_select = "//input[@name='space']"
    agree_check_box = "//input[@name='checkNote']"
    next_button = "//input[@name='sendbtn']"

    # enter reader id
    reader_id_input = "//input[@name='schid' and @type='text']"
    submit_reader_id_button = "//input[@name='schBtn']"

    # select room
    room_label = "//label[@title='{}']"
    room_select = "/input"
    time_slots = "/ancestor::dl/dd"
    confirm_button = "//input[@id='sendbtn']"
    def get_room_select_xpath(room_id):
        return RESERVE_RELATED_PAGE.room_label.format(room_id) + RESERVE_RELATED_PAGE.room_select
    def get_time_slots_xpath(room_id):
        return RESERVE_RELATED_PAGE.room_label.format(room_id) + RESERVE_RELATED_PAGE.time_slots

class DATE_PAGE:
    # request for all available rooms
    request_all_button = "//input[@name='sendAllBtn']"

    select_date_toggle = "//input[@name='sdate']"
    calendar = "//div[@class='calendar']"

    calendar_month = "//a[@title='Today']"
    calendar_date = "//a[.='{}']"
    calendar_next_month = calendar + "//a[@class='monthR']"

    def get_calendar_date_xpath(date: int):
        return DATE_PAGE.calendar + DATE_PAGE.calendar_date.format(date)
