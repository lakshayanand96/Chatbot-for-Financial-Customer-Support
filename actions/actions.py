# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions



from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import requests
import sqlite3
import speech_recognition as sr
from translate import Translator


class Actionsavefirstname(Action):

    def name(self) -> Text:
        return "action_save_firstname"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(tracker.get_slot('firstname'))
        return [SlotSet('firstname',tracker.latest_message['text'])]

class Actionsavelastname(Action):

    def name(self) -> Text:
        return "action_save_lastname"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_template("utter_to_ask", tracker)
        print(tracker.get_slot('lastname'))

        return [SlotSet('lastname',tracker.latest_message['text'])]



def datastore(firstname, lastname):
    conn=sqlite3.connect('cov.db')
    mycursor = conn.cursor()
    mycursor.execute("""CREATE TABLE IF NOT EXISTS my_info (Name TEXT, HomeState TEXT);""")
    mycursor.execute("INSERT INTO my_info VALUES (?,?)",(firstname,lastname))
    conn.commit()
    print(mycursor.rowcount,"record inserted")


class ActionStore(Action):

    def name(self) -> Text:
        return "action_store"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: 
        x=tracker.get_slot('firstname')
        y=tracker.get_slot('lastname')
        datastore(x,y)
        dispatcher.utter_message("Thank you! Your information is saved.")
        print(x)
        print(y)
        return []








      




# class ActionVoiceData(Action):

#     def name(self) -> Text:
#         return "action_activate_voice"
    
#     bot_message = ""
#     message=""

#     r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": "Hello"})
#     print("Bot says, ",end=' ')
#     for i in r.json():
#       bot_message = i['text']
#       print(f"{bot_message}")


#     while bot_message != "Bye" or bot_message!='thanks':

#         r = sr.Recognizer()  # initialize recognizer
#         with sr.Microphone() as source:  # mention source it will be either Microphone or audio files.
#             print("Ask anything about COVID-19 :")
#             audio = r.listen(source)  # listen to the source
#             try:
#                 message = r.recognize_google(audio)  # use recognizer to convert our audio into text part.
#                 print("You said : {}".message)
#             except:
#                 print("Sorry could not recognize your voice")  # In case of voice not recognized  clearly
#         if len(message)==0:
#             continue
#         print("Sending message now...")

#         r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": message})

#         print("Bot says, ",end=' ')
#         for i in r.json():
#             bot_message = i['text']
#             print(f"{bot_message}")
