import kivy
kivy.require('1.10.0')

import time
import pickle

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from kivy.clock import Clock
from kivy.config import Config

Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', 400)
Config.set('graphics', 'height', 520)
Config.set('graphics', 'minimum_width', 400)
Config.set('graphics', 'minimum_height', 520)


def convert_seconds_to_text(total_seconds):
    days = int(total_seconds // 86400)
    if days == 1:
        word_days = ' day '
    else:
        word_days = ' days '
    days = str(days) + word_days

    hours = int(total_seconds // 3600 % 24)
    if hours == 1:
        word_hours = ' hour '
    else:
        word_hours = ' hours '
    hours = str(hours) + word_hours

    minutes = int(total_seconds // 60 % 60)
    if minutes == 1:
        word_minutes = ' minute '
    else:
        word_minutes = ' minutes '
    minutes = str(minutes) + word_minutes

    seconds = total_seconds % 60
    return '{}{}{}{:.1f} secs'.format(days, hours, minutes, seconds)


class Timer(Label):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.total_seconds = 0
        self.stop_time = time.time()

    def update(self, *args):
        self.total_seconds = time.time() - self.stop_time

        self.text = convert_seconds_to_text(self.total_seconds)


class MainScreen(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.spacing = [1, 1]

        self.start_btn = Button(text='Start', size_hint=(1, .07), font_size=12)
        self.start_btn.bind(on_release=self.clk_start_btn)

        self.timer_name = TextInput(hint_text='Type here what you want to track', size_hint=(.2, .1), font_size=11)

        self.timer = Timer(text='0 days 0 hours 0 minutes 0 secs', size_hint=(.8, .09), font_size=11)

        self.reset_timer_btn = Button(text='Reset', size_hint=(.2, .1), font_size=12)
        self.reset_timer_btn.bind(on_release=self.clk_reset_timer_btn)

        self.save_and_quit_btn = Button(text='Save and Quit', size_hint=(1, .07), font_size=12)
        self.save_and_quit_btn.bind(on_release=self.clk_save_and_quit)

        #self.add_timer_btn = Button(text="Add New Timer", size_hint_y=None)
        #self.add_widget(self.add_timer_btn)
        self.add_widget(self.start_btn)
        self.add_widget(self.timer_name)
        self.add_widget(self.timer)
        self.add_widget(self.reset_timer_btn)
        self.add_widget(self.save_and_quit_btn)

        self.running = False

        self.load_data()

    def clk_start_btn(self, obj):
        if self.running:
            self.running = False
            Clock.unschedule(self.timer.update)
            self.start_btn.text = "Start"
        else:
            self.running = True
            self.timer.stop_time = time.time() - self.timer.total_seconds
            Clock.schedule_interval(self.timer.update, 0.1)
            self.start_btn.text = "Stop"

    def clk_reset_timer_btn(self, obj):
        if self.running:
            self.running = False
            Clock.unschedule(self.timer.update)
            self.start_btn.text = "Start"

        self.timer.total_seconds = 0
        self.timer.text = convert_seconds_to_text(self.timer.total_seconds)

    def clk_save_and_quit(self, *args):
        Clock.unschedule(self.timer.update)
        timer_list = {"total_seconds": self.timer.total_seconds, "timer_name": self.timer_name.text}
        try:
            with open('data', 'wb') as fp:
                pickle.dump(timer_list, fp)
        except Exception as e:
            print("Exception when saving data: {}".format(e))
        else:
            TimeYourselfApp().stop()

    def load_data(self):
        try:
            with open('data', 'rb') as fp:
                timer_list = pickle.load(fp)
                self.timer.total_seconds = timer_list["total_seconds"]
                self.timer_name.text = timer_list["timer_name"]
        except Exception as e:
            print("Exception when loading data: {}".format(e))
            pass

        self.timer.text = convert_seconds_to_text(self.timer.total_seconds)


class TimeYourselfApp(App):
    def build(self):
        self.title = 'Time Yourself'
        return MainScreen()


if __name__ == '__main__':
    TimeYourselfApp().run()
