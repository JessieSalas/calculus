from kivy.app import App
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ObjectProperty

from parser import *

class Avocado(FloatLayout):

    welcome = StringProperty()

    solution1 = StringProperty()
    solution2 = StringProperty()
    solution3 = StringProperty()
    solution4 = StringProperty()
    solution5 = StringProperty()
    solution6 = StringProperty()
    solution7 = StringProperty()

    dy = StringProperty()

    def solver(self, sentence, leaner):
        ex = extractRelationships(tag(sentence))
        solution = solve(ex, leaner)
        self.dy = ex['RATE']
        self.solution1 = solution[0]
        self.solution2 = solution[1]
        self.solution3 = solution[2]
        self.solution4 = solution[3]
        self.solution5 = solution[4]
        self.solution6 = solution[5]
        self.solution7 = solution[6]

    def lame(self):
        print("yeah")

    def list_notebooks(self):
        notes = self.get_notebooks()
        with self.canvas:
            layout = GridLayout(rows = len(notes))
            layout.size = self.size
            for note in notes:
                bot = Button(text=note,pos_hint_x = .7, width=100)
                bot.bind(on_press=self.lame)
                layout.add_widget(bot)


class Interface(App):
    def build(self):
        self.Instance = Avocado()
        return self.Instance

if __name__ == '__main__':
    Interface().run()
