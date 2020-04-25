from kivy.app import App
from kivy.uix.label import Label


class SlideDetectApp(App):
    def build(self):
        self.lab = Label(text="pootis")
        self.lab.bind(on_touch_move=self.detect)
        return self.lab
        pass

    def detect(self, instance, touch):
        # if not instance.collide_point(touch.x, touch.y):
        #   return False

        if touch.dx < -40:
            self.lab.text="pootis left"
            pass
        if touch.dx > 40:
            self.lab.text="pootis right"
            pass
        if touch.dy < -40:
            self.lab.text="pootis down"
            pass
        if touch.dy > 40:
            self.lab.text="pootis up"
            pass
        return True


SlideDetectApp().run()
