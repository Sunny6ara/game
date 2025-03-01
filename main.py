# main.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.properties import StringProperty
import random

class NumberGuessingGame(BoxLayout):
    message = StringProperty("Apna naam daalein:")

    def __init__(self, **kwargs):
        super(NumberGuessingGame, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        # Naam input ke liye
        self.name_input = TextInput(multiline=False, size_hint=(1, None), height=40)
        self.add_widget(self.name_input)

        self.name_button = Button(text="Naam Submit Karein", size_hint=(1, None), height=40)
        self.name_button.bind(on_press=self.submit_name)
        self.add_widget(self.name_button)

        self.info_label = Label(text=self.message)
        self.add_widget(self.info_label)

        # Guess input aur button (initially disable)
        self.guess_input = TextInput(multiline=False, size_hint=(1, None), height=40)
        self.guess_input.disabled = True
        self.add_widget(self.guess_input)

        self.guess_button = Button(text="Guess Submit Karein", size_hint=(1, None), height=40)
        self.guess_button.bind(on_press=self.check_guess)
        self.guess_button.disabled = True
        self.add_widget(self.guess_button)

        # Leaderboard dictionary (ephemeral)
        self.leaderboard = {}

    def submit_name(self, instance):
        self.player_name = self.name_input.text.strip()
        if not self.player_name:
            self.info_label.text = "Kripya ek valid naam daalein!"
            return
        self.info_label.text = f"Swagat hai {self.player_name}! Ab Difficulty choose karein: Easy, Medium, Hard"
        # Naam input aur button hata dein
        self.remove_widget(self.name_input)
        self.remove_widget(self.name_button)

        # Difficulty selection ke liye buttons add karein
        self.diff_layout = BoxLayout(size_hint=(1, None), height=40, spacing=10)
        self.easy_btn = Button(text="Easy")
        self.medium_btn = Button(text="Medium")
        self.hard_btn = Button(text="Hard")
        self.easy_btn.bind(on_press=self.set_difficulty)
        self.medium_btn.bind(on_press=self.set_difficulty)
        self.hard_btn.bind(on_press=self.set_difficulty)
        self.diff_layout.add_widget(self.easy_btn)
        self.diff_layout.add_widget(self.medium_btn)
        self.diff_layout.add_widget(self.hard_btn)
        self.add_widget(self.diff_layout)

    def set_difficulty(self, instance):
        difficulty = instance.text
        self.difficulty = difficulty
        if difficulty == "Easy":
            self.min_num = 1
            self.max_num = 50
            self.max_attempts = 10
        elif difficulty == "Medium":
            self.min_num = 1
            self.max_num = 100
            self.max_attempts = 7
        elif difficulty == "Hard":
            self.min_num = 1
            self.max_num = 200
            self.max_attempts = 5

        self.secret_number = random.randint(self.min_num, self.max_num)
        self.attempts = 0
        self.score = 0
        self.info_label.text = f"Guess karo number {self.min_num} se {self.max_num} ke beech. Attempts bache: {self.max_attempts}"
        self.guess_input.disabled = False
        self.guess_button.disabled = False

        # Difficulty buttons hata dein
        self.remove_widget(self.diff_layout)

    def check_guess(self, instance):
        guess_text = self.guess_input.text.strip()
        if not guess_text.isdigit():
            self.info_label.text = "Kripya ek valid number daalein!"
            return
        guess = int(guess_text)
        self.attempts += 1
        attempts_left = self.max_attempts - self.attempts

        if guess == self.secret_number:
            # Score calculation: jitne zyada attempts bach gaye, utna score
            self.score = attempts_left * 10
            self.info_label.text = (f"Badhiya {self.player_name}! Aapne {self.attempts} attempts me number guess kar liya. "
                                     f"Aapka score: {self.score}")
            # Leaderboard update
            self.leaderboard[self.player_name] = self.score
            self.info_label.text += f"\nLeaderboard: {self.leaderboard}"
            self.guess_input.disabled = True
            self.guess_button.disabled = True
        elif guess < self.secret_number:
            hint = "Bahut chota!"
            # Hint: agar secret number even hai toh
            if self.secret_number % 2 == 0:
                hint += " Hint: Number even hai."
            self.info_label.text = f"{hint} Attempts bache: {attempts_left}"
        else:
            hint = "Bahut bada!"
            # Hint: agar secret number odd hai toh
            if self.secret_number % 2 != 0:
                hint += " Hint: Number odd hai."
            self.info_label.text = f"{hint} Attempts bache: {attempts_left}"

        if attempts_left <= 0 and guess != self.secret_number:
            self.info_label.text = f"Game Over! Sahi number tha {self.secret_number}. Agli baar koshish karein!"
            self.guess_input.disabled = True
            self.guess_button.disabled = True

class NumberGuessApp(App):
    def build(self):
        return NumberGuessingGame()

if __name__ == "__main__":
    NumberGuessApp().run()
