# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from datetime import datetime

from fuzzywuzzy import fuzz
import pandas as pd
import re


def is_product_available(product_name):
    # Load the data from the .csv file using pandas
    data = pd.read_csv('crawl.csv')
    # Find the closest match to the user's input using fuzzy string matching
    best_match_score = 0
    best_match_index = -1
    for i, name in enumerate(data['Name']):
        name = re.sub(r'\([^)]*\)', '', name)
        score = fuzz.token_set_ratio(product_name, name)
        if score > best_match_score:
            best_match_score = score
            best_match_index = i
    print(product_name)
    # If there is no close match, return a message indicating the product is not found
    if best_match_score < 80:
        return f"Xin lỗi, hiện shop đang không có sản phẩm này, hoặc có thể bạn đang gõ sai tên sản phẩm chăng?"
    
    # If there is a close match, get the availability status of the closest match
    product = data.iloc[best_match_index]
    if product['Status']:
        price = product['Price']
        summary = product['Summary']
        name = product['Name']
        return f"Vâng, hiện shop đang có sản phẩm này, đây là 1 số thông tin thêm về sản phẩm:\n- Tên: {name}\n- Giá: {price}\n- Cấu hình:\n{summary} with best_score:{best_match_score}"
    else:
        return f"Xin lỗi, hiện sản phẩm này đang hết hàng, bạn có thể tham khảo các sản phẩm khác hoặc có thể liên hệ chúng mình trong tương lai"


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        current_time = datetime.now()
        dispatcher.utter_message(text=f"Bây giờ là {current_time.time()} anh nhé")

        return []
    
class ActionCheckProductAvailability(Action):
    def name(self) -> Text:
        return "action_check_product_availability"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        product_name = tracker.get_slot('product_name')
        p_pronouns = tracker.get_slot("p_pronouns")
        message = is_product_available(product_name)
        dispatcher.utter_message(text=message)
        return []
    
class ActionAbleToBuyOffline(Action):

    def name(self) -> Text:
        return "action_able_to_buy_offline"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        current_time = datetime.now().time()
        start_time = datetime.strptime("07:30:00", "%H:%M:%S").time()
        end_time = datetime.strptime("20:30:00", "%H:%M:%S").time()
        message = 'Bây giờ là '
        message += current_time.strftime("%Hh%M")
        if start_time <= current_time <= end_time:
            message += f" vẫn nằm trong khoảng thời gian làm việc của shop (từ 7h30 đến 20h30), nên bạn có thể ghé mua trực tiếp ngay bây giờ nhé!!"
        else:
            message += f" nằm ngoài thời gian làm việc của shop (từ 7h30 đến 20h30), bạn vui lòng quay lại sau nhé!!"

        dispatcher.utter_message(text=message)
        return []
    
class ActionAbleToBuyOnline(Action):

    def name(self) -> Text:
        return "action_able_to_buy_online"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=f"Ok, bạn có thể điền vào link sau để hoàn tất mua hàng online nhé: 'http://form.muaonline.com/buy'")

        return []
