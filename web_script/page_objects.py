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

    confirm_button = "//input[@name='setbtn']"

    reservation_list = "//tbody//tr"
    reservation_time = "/td[5]"
    reserved_room = "/td[3]"
    reservation_status = "/td[6]/span"
    reservation_cancel_checkbox = "//input"

    def get_reservation_time_xpath(index: int):
        return RESERVED_LIST_PAGE.reservation_list + f"[{index}]" + RESERVED_LIST_PAGE.reservation_time
    
    def get_reserved_room_xpath(index: int):
        return RESERVED_LIST_PAGE.reservation_list + f"[{index}]" + RESERVED_LIST_PAGE.reserved_room
    
    def get_reservation_status_xpath(index: int):
        return RESERVED_LIST_PAGE.reservation_list + f"[{index}]" + RESERVED_LIST_PAGE.reservation_status
    
    def get_reservation_cancel_checkbox_xpath(index: int):
        return RESERVED_LIST_PAGE.reservation_list + f"[{index}]" + RESERVED_LIST_PAGE.reservation_cancel_checkbox

class RESERVE_RELATED_PAGE:
    # notice
    carrel_room_select = "//input[@name='space']"
    agree_check_box = "//input[@name='checkNote']"
    next_button = "//input[@name='sendbtn']"

    # enter reader id
    reader_id_input = "//input[@name='schid' and @type='text']"
    submit_reader_id_button = "//input[@name='schBtn']"

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

class TIME_SLOT_PAGE:
    room_panel = "//span[@title='{}']/ancestor::dl"
    choose_room = "//input[@name='deviceid']"
    time_slot_block = "//span[.='{}']/ancestor::dd"
    time_slot_checkbox = "//input"
    time_slot_list = "//dd"
    submit_button = "//input[@name='sendbtn']"
    block_begin_time = "//span[1]"

    def get_time_slot_list_xpath(room_id: str):
        return TIME_SLOT_PAGE.room_panel.format(room_id) + TIME_SLOT_PAGE.time_slot_list

    def get_time_slots_block_xpath_with_index(room_id: str, index: int):
        return TIME_SLOT_PAGE.room_panel.format(room_id) + TIME_SLOT_PAGE.time_slot_list + f"[{index}]"

    def get_time_slots_block_xpath_begin_time(room_id: str, index: int):
        return TIME_SLOT_PAGE.get_time_slots_block_xpath_with_index(room_id, index + 1) + TIME_SLOT_PAGE.block_begin_time

    def get_choose_room_xpath(room_id: str):
        return TIME_SLOT_PAGE.room_panel.format(room_id) + TIME_SLOT_PAGE.choose_room

    def get_time_slots_block_xpath_with_time(room_id: str, time_slot: str):
        return TIME_SLOT_PAGE.room_panel.format(room_id) + TIME_SLOT_PAGE.time_slot_block.format(time_slot)

    def get_time_slots_checkbox_xpath(room_id: str, time_slot: str):
        return TIME_SLOT_PAGE.get_time_slots_block_xpath_with_time(room_id, time_slot) + TIME_SLOT_PAGE.time_slot_checkbox

    def get_submit_button_xpath(room_id: str):
        return TIME_SLOT_PAGE.room_panel.format(room_id) + TIME_SLOT_PAGE.submit_button
