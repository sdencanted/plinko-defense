from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button 


class MyLabel(Label):

    def __init__(self, **kwargs):
        Label.__init__(self, **kwargs)
        self.bind(size=self.setter('text_size'))
        self.padding = (20, 20)


class Investment(App):

    def build(self):
        layout = GridLayout(cols=2,rows=5)
        l1 = MyLabel(text="Investment Ammount",
                     font_size=24, halign='left', valign='middle')

        layout.add_widget(l1)
        pass
        btn = Button(text="Calculate", on_press=self.calculate, font_size=24)
        layout.add_widget(btn)

        self.i = TextInput(font_size=150,
                      size_hint_y=None,
                      height=200)

        self.y = TextInput(font_size=150,
                      size_hint_y=None,
                      height=200)

        self.m = TextInput(font_size=150,
                      size_hint_y=None,
                      height=200)

        layout.add_widget(self.i)
        layout.add_widget(self.y)
        layout.add_widget(self.m)

        self.txt_future_val=MyLabel(text="stonks",
                     font_size=24, halign='left', valign='middle')
        layout.add_widget(self.txt_future_val)
        return layout

    def calculate(self, instance):
        inv_amt = float(self.i.text)
        years = float(self.y.text)
        mth_int_rate = float(self.m.text)
        self.txt_future_val.text = str(inv_amt*years*mth_int_rate)





Investment().run()
