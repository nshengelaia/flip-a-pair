import tkinter as tk
import random
import json
import os
from PIL import Image, ImageTk

# Constants
ASSETS_DIR = "assets"
CARD_WIDTH, CARD_HEIGHT = 150, 200  # 3:4 ratio
CARD_BACK_IMAGE = os.path.join(ASSETS_DIR, "card_back.png")
CARD_IMAGES = [os.path.join(ASSETS_DIR, f"Card{i}.png") for i in range(1, 11)]
TITLE_IMAGE = os.path.join(ASSETS_DIR, "title.png")
BACKGROUND_IMAGE = os.path.join(ASSETS_DIR, "Background.png")
PLAY_BUTTON_IMAGE = os.path.join(ASSETS_DIR, "PlayButton.png")
TIMER_DURATION = 60
HIGH_SCORES_FILE = "high_scores.json"
MAX_HIGH_SCORES = 3

class FlipAPairGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Flip-a-Pair")
        try:
            self.root.state('zoomed')
        except tk.TclError:
            self.root.attributes('-zoomed', True)

        self.score = 0
        self.level = 1
        self.timer = TIMER_DURATION
        self.cards = []
        self.flipped = []
        self.matched = []
        self.high_scores = self.load_high_scores()

        self.card_back_img = ImageTk.PhotoImage(Image.open(CARD_BACK_IMAGE).resize((CARD_WIDTH, CARD_HEIGHT)))
        self.card_images = [ImageTk.PhotoImage(Image.open(path).resize((CARD_WIDTH, CARD_HEIGHT))) for path in CARD_IMAGES]
        self.title_image = ImageTk.PhotoImage(Image.open(TITLE_IMAGE))
        self.bg_img_raw = Image.open(BACKGROUND_IMAGE)
        self.play_button_image = ImageTk.PhotoImage(Image.open(PLAY_BUTTON_IMAGE).resize((270, 105)))

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.start_screen()

    def start_screen(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        bg_resized = self.bg_img_raw.resize((width, height))
        self.background_image = ImageTk.PhotoImage(bg_resized)

        canvas = tk.Canvas(self.main_frame, width=width, height=height, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=self.background_image, anchor="nw")

        canvas.create_image(width // 2, height // 2 - 100, image=self.title_image)
        canvas.create_image(width // 2, height // 2 + 80, image=self.play_button_image, tags="play_button")

        canvas.tag_bind("play_button", "<Button-1>", lambda e: self.setup_game())

    def setup_game(self):
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")
        self.root.update()
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.top_frame = tk.Frame(self.main_frame)
        self.top_frame.pack(pady=10)

        self.score_label = tk.Label(self.top_frame, text=f"Score: {self.score}", font=("Arial", 14))
        self.score_label.pack(side=tk.LEFT, padx=20)

        self.timer_label = tk.Label(self.top_frame, text=f"Time: {self.timer}", font=("Arial", 14))
        self.timer_label.pack(side=tk.LEFT, padx=20)

        self.high_scores_label = tk.Label(self.main_frame, font=("Arial", 12))
        self.high_scores_label.pack(pady=5)

        self.card_frame = tk.Frame(self.main_frame)
        self.card_frame.pack(pady=10)

        self.start_level()
        self.update_timer()

    def start_level(self):
        num_cards = self.level * 2 + 2
        self.create_cards(num_cards)
        self.display_cards(num_cards)

    def create_cards(self, num):
        num_pairs = num // 2
        selected_images = random.sample(self.card_images, num_pairs)
        card_set = selected_images * 2
        random.shuffle(card_set)
        self.cards = card_set
        self.flipped = []
        self.matched = []

    def display_cards(self, num_cards):
        for widget in self.card_frame.winfo_children():
            widget.destroy()

        layout_map = {
            4: (2, 2), 6: (2, 3), 8: (2, 4), 10: (2, 5),
            12: (3, 4), 14: (2, 7), 16: (4, 4), 18: (3, 6), 20: (4, 5)
        }

        rows, cols = layout_map.get(num_cards, (int(num_cards ** 0.5), (num_cards + int(num_cards ** 0.5) - 1) // int(num_cards ** 0.5)))

        self.buttons = []
        for idx in range(num_cards):
            btn = tk.Button(self.card_frame, image=self.card_back_img, command=lambda idx=idx: self.flip_card(idx))
            btn.grid(row=idx // cols, column=idx % cols, padx=5, pady=5)
            self.buttons.append(btn)

    def flip_card(self, idx):
        if idx in self.matched or idx in self.flipped or len(self.flipped) == 2:
            return

        self.buttons[idx].config(image=self.cards[idx])
        self.flipped.append(idx)

        if len(self.flipped) == 2:
            self.root.after(500, self.check_match)

    def check_match(self):
        a, b = self.flipped
        if self.cards[a] == self.cards[b]:
            self.matched.extend([a, b])
            self.score += 10
            self.score_label.config(text=f"Score: {self.score}")
        else:
            self.buttons[a].config(image=self.card_back_img)
            self.buttons[b].config(image=self.card_back_img)

        self.flipped = []

        if len(self.matched) == len(self.cards):
            self.level += 1
            self.start_level()

    def update_timer(self):
        if self.timer > 0:
            self.timer -= 1
            self.timer_label.config(text=f"Time: {self.timer}")
            self.root.after(1000, self.update_timer)
        else:
            self.end_game()

    def end_game(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        title = tk.Label(self.main_frame, text="Game Over", font=("Arial", 24))
        title.pack(pady=20)

        score_label = tk.Label(self.main_frame, text=f"Your score: {self.score}", font=("Arial", 16))
        score_label.pack(pady=10)

        if len(self.high_scores) < MAX_HIGH_SCORES or self.score > self.high_scores[-1]["score"]:
            name_entry_label = tk.Label(self.main_frame, text="You made it to the leaderboard! Enter your nickname:", font=("Arial", 12))
            name_entry_label.pack()
            name_entry = tk.Entry(self.main_frame, font=("Arial", 12))
            name_entry.pack(pady=5)

            def save_and_show():
                name = name_entry.get()
                if name:
                    self.high_scores.append({"name": name, "score": self.score})
                    self.high_scores = sorted(self.high_scores, key=lambda x: x["score"], reverse=True)[:MAX_HIGH_SCORES]
                    self.save_high_scores()
                    self.show_leaderboard()

            submit_button = tk.Button(self.main_frame, text="Submit", command=save_and_show)
            submit_button.pack(pady=5)
        else:
            self.show_leaderboard()

    def show_leaderboard(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text="Leaderboard", font=("Arial", 20)).pack(pady=10)
        for entry in self.high_scores:
            tk.Label(self.main_frame, text=f"{entry['name']}: {entry['score']}", font=("Arial", 14)).pack()

        tk.Button(self.main_frame, text="Play Again", command=self.restart_game).pack(pady=20)

    def restart_game(self):
        self.score = 0
        self.level = 1
        self.timer = TIMER_DURATION
        self.setup_game()

    def load_high_scores(self):
        if os.path.exists(HIGH_SCORES_FILE):
            with open(HIGH_SCORES_FILE, "r") as file:
                return json.load(file)
        return []

    def save_high_scores(self):
        with open(HIGH_SCORES_FILE, "w") as file:
            json.dump(self.high_scores, file, indent=2)

if __name__ == "__main__":
    root = tk.Tk()
    game = FlipAPairGame(root)
    root.mainloop()
