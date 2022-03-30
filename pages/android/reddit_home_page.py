import logging
import re
import sys
from time import sleep

from selenium.webdriver.common.by import By
from utils.base_page import BasePage

logger = logging.getLogger('behaving')


class RedditHomePage(BasePage):
    # Reddit home page
    skip_login_link_loc = (By.ID, "com.reddit.frontpage:id/skip_button")

    # Alert message modal
    alert_msg_title_loc = (By.ID, "com.reddit.frontpage:id/alertTitle")
    alert_msg_yes_button_loc = (By.ID, "android:id/button1")
    alert_msg_no_button_loc = (By.ID, "android:id/button2")

    # Searched result list
    search_view_loc = (By.ID, "com.reddit.frontpage:id/search_view")
    search_field_loc = (By.ID, "com.reddit.frontpage:id/search")
    search_results_loc = (By.CLASS_NAME, "android.widget.RelativeLayout")
    search_results_name_loc = (By.ID, "com.reddit.frontpage:id/community_name")

    # subreddit page
    profile_name_loc = (By.ID, "com.reddit.frontpage:id/profile_name")
    layout_loc = (By.CLASS_NAME, "android.widget.LinearLayout")
    link_title_loc = (By.ID, "com.reddit.frontpage:id/link_title")

    def skip_on_board_page(self):
        if self.is_element_found(*self.skip_login_link_loc):
            self.find_element(*self.skip_login_link_loc).click()
        elif self.is_element_found(*self.search_view_loc):
            pass
        # Sometime  an alert modal pops up
        elif self.is_alert_modal_displayed(self):
            self.dismiss_altert_modal(self)
        else:
            self.fail("STDOUT: Can't find on board page. \n")
        return

    def input_searched_term(self, searched_term):
        if self.is_element_found(*self.search_view_loc):
            self.find_element(*self.search_view_loc).click()
            self.send_keys(searched_term, *self.search_field_loc)
        elif self.is_alert_modal_displayed(self):
            self.dismiss_altert_modal(self)
        else:
            self.fail("STDOUT: Can't find search field. \n")
        return

    def check_searched_result_is_displayed(self, searched_term):
        names_array = self.fetch_elements_name(*self.search_results_name_loc)
        if names_array is None:
            self.fail("STDOUT: Can't find searched result: %s. \n" % searched_term)
            return False
        for i in range(names_array.__len__()):
            result_name = names_array[i]
            if searched_term == result_name[2:]:
                return True
        self.fail("STDOUT: Can't find searched result: %s. \n" % searched_term)
        return False

    def is_alert_modal_displayed(self):
        if self.is_element_found(*self.alert_msg_title_loc):
            return True
        return False

    def dismiss_altert_modal(self):
        self.find_element(*self.alert_msg_yes_button_loc).click()

    def tap_on_the_searched_result(self, searched_term):
        names_array = self.fetch_elements_name(*self.search_results_name_loc)
        if names_array is None:
            self.fail("STDOUT: Can't find searched result: %s. \n" % searched_term)
            return
        for i in range(names_array.__len__()):
            search_result_name = names_array[i]
            if searched_term == search_result_name[2:]:
                if self.find_the_specific_tapable_element(i, *self.search_results_name_loc) is not None:
                    self.find_the_specific_tapable_element(i, *self.search_results_name_loc).click()
                    return
        self.fail("STDOUT: Can't tap on the searched result: %s. \n" % searched_term)
        return

    def check_specific_term_in_top_posted_title(self, check_term):
        sleep(20)
        title_names = self.fetch_elements_name(*self.link_title_loc)
        if title_names is None:
            return False
        if check_term in title_names[0]:
            sys.stdout.write(
                "\n\n Top posted title : \"%s\" contains CHECK TERM : \"%s\". \n\n " % (title_names[0], check_term))
            return True
        sys.stdout.write(
            "\n\n Top posted title : \"%s\" does not contain CHECK TERM : \"%s\". \n\n " % (title_names[0], check_term))
        return False
