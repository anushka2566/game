import random

# Sample question bank (expand as needed)
QUESTIONS = [
    {
        "q": "What is phishing?",
        "options": ["A cyber attack using emails", "A type of antivirus", "A password manager", "A firewall method"],
        "answer": 0
    },
    {
        "q": "What does VPN stand for?",
        "options": ["Very Private Network", "Virtual Private Network", "Verified Public Network", "Variable Protocol Network"],
        "answer": 1
    },
    {
        "q": "Which is a strong password?",
        "options": ["password123", "admin", "Qw!9z#7lK", "userpass"],
        "answer": 2
    },
    {
        "q": "What is two-factor authentication?",
        "options": [
            "Using two passwords",
            "Requiring two forms of identification",
            "Logging in twice",
            "Using two emails"
        ],
        "answer": 1
    },
    {
        "q": "What is a firewall?",
        "options": [
            "A physical wall in buildings",
            "A device that stores data",
            "A security system for networks",
            "An email filter"
        ],
        "answer": 2
    },
    {
        "q": "What does SSL secure?",
        "options": [
            "Wi-Fi signals",
            "Website connections",
            "Printer data",
            "USB drives"
        ],
        "answer": 1
    },
    {
        "q": "What is ransomware?",
        "options": [
            "A type of hardware",
            "A virus that demands payment",
            "A safe browser",
            "A backup tool"
        ],
        "answer": 1
    },
    {
        "q": "DDoS stands for?",
        "options": [
            "Distributed Denial of Service",
            "Direct Disk Operating System",
            "Data Download Service",
            "Digital Domain of Security"
        ],
        "answer": 0
    },
    {
        "q": "What is malware?",
        "options": [
            "Malicious software",
            "A secure browser",
            "A firewall",
            "A password manager"
        ],
        "answer": 0
    },
    {
        "q": "Which is a sign of a phishing site?",
        "options": [
            "HTTPS in the URL",
            "No spelling errors",
            "Odd-looking URLs",
            "A padlock icon"
        ],
        "answer": 2
    }
]

# -------------- Common logic --------------
class GameState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.hacker_steps = 0
        self.max_steps = 6
        self.score = 0
        self.current_q = None
        self.used_q = set()
        self.pick_question()
        self.game_over = False
        self.message = ""
        self.selected_option = -1

    def pick_question(self):
        available = [i for i in range(len(QUESTIONS)) if i not in self.used_q]
        if not available:
            self.used_q = set()
            available = list(range(len(QUESTIONS)))
        idx = random.choice(available)
        self.current_q = QUESTIONS[idx]
        self.used_q.add(idx)
        self.selected_option = -1

    def answer(self, option):
        if self.game_over:
            return
        if option == self.current_q["answer"]:
            self.score += 1
            self.message = "Correct! +1 coin."
        else:
            self.hacker_steps += 1
            self.message = f"Wrong! Hacker moves forward. Correct: {self.current_q['options'][self.current_q['answer']]}"
        if self.hacker_steps >= self.max_steps:
            self.game_over = True
            self.message += " Game over!"
        else:
            self.pick_question()

# -------------- Arcade version --------------
def run_arcade_version():
    import arcade
    import os

    SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600
    STEP_SIZE = (600 - 100) // 6
    HACKER_START_X = 100
    DEFENDER_X = 600
    HACKER_Y = 320

    # Check for assets
    HACKER_IMG = "assets/hacker.png"
    DEFENDER_IMG = "assets/defender.png"
    ANIMATE = os.path.exists(HACKER_IMG) and os.path.exists(DEFENDER_IMG)

    class GameWindow(arcade.Window):
        def __init__(self):
            super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Hacker vs Defender (Arcade)")
            arcade.set_background_color(arcade.color.DARK_BLUE)
            self.state = GameState()
            self.hacker_pos = HACKER_START_X

        def on_draw(self):
            arcade.start_render()
            # Draw hacker
            if ANIMATE:
                arcade.draw_scaled_texture_rectangle(self.hacker_pos, HACKER_Y, arcade.load_texture(HACKER_IMG), 0.3)
            else:
                arcade.draw_circle_filled(self.hacker_pos, HACKER_Y, 40, arcade.color.RED)
                arcade.draw_text("Hacker", self.hacker_pos - 35, HACKER_Y - 60, arcade.color.WHITE, 16, bold=True)
            # Draw defender
            if ANIMATE:
                arcade.draw_scaled_texture_rectangle(DEFENDER_X, HACKER_Y, arcade.load_texture(DEFENDER_IMG), 0.3)
            else:
                arcade.draw_rectangle_filled(DEFENDER_X, HACKER_Y, 80, 80, arcade.color.GREEN)
                arcade.draw_text("Defender", DEFENDER_X - 40, HACKER_Y - 60, arcade.color.WHITE, 16, bold=True)

            # Draw UI
            arcade.draw_text(f"Coins: {self.state.score}", 10, SCREEN_HEIGHT - 40, arcade.color.YELLOW, 20)
            arcade.draw_text(f"Hacker Steps: {self.state.hacker_steps}/6", 10, SCREEN_HEIGHT - 70, arcade.color.WHITE, 18)

            # Draw question
            if not self.state.game_over:
                arcade.draw_text("Question:", 200, 480, arcade.color.CYAN, 22)
                arcade.draw_text(self.state.current_q['q'], 200, 450, arcade.color.WHITE, 20, width=600)
                # Draw options
                for i, opt in enumerate(self.state.current_q['options']):
                    opt_color = arcade.color.LIGHT_GREEN if self.state.selected_option == i else arcade.color.ASH_GREY
                    arcade.draw_rectangle_filled(220, 400 - i*60, 600, 45, opt_color)
                    arcade.draw_text(f"{chr(65+i)}) {opt}", 240, 385 - i*60, arcade.color.BLACK, 18)
                arcade.draw_text(self.state.message, 200, 220, arcade.color.YELLOW_ORANGE, 17)
            else:
                arcade.draw_text("GAME OVER!", 330, 350, arcade.color.RED, 40)
                arcade.draw_text(f"Total Coins: {self.state.score}", 330, 300, arcade.color.YELLOW, 30)
                arcade.draw_text("Press R to restart.", 330, 250, arcade.color.WHITE, 20)

        def on_key_press(self, key, modifiers):
            if self.state.game_over:
                if key == arcade.key.R:
                    self.state.reset()
                    self.hacker_pos = HACKER_START_X
                return
            if arcade.key.A <= key <= arcade.key.D:
                idx = key - arcade.key.A
                self.state.selected_option = idx
                self.state.answer(idx)
                self.hacker_pos = HACKER_START_X + STEP_SIZE * self.state.hacker_steps

    arcade.run(GameWindow())

# -------------- Pygame version --------------
def run_pygame_version():
    import pygame
    import sys
    import os

    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600
    WHITE = (255, 255, 255)
    DARK_BLUE = (20, 20, 80)
    RED = (200, 40, 40)
    GREEN = (40, 200, 60)
    YELLOW = (230, 230, 40)
    CYAN = (40, 200, 200)
    LIGHT_GREEN = (120, 240, 140)
    ORANGE = (255, 185, 60)
    BLACK = (20, 20, 20)
    STEP_SIZE = (600 - 100) // 6
    HACKER_START_X = 100
    DEFENDER_X = 600
    HACKER_Y = 320

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Hacker vs Defender (Pygame)")
    font = pygame.font.SysFont("arial", 24)
    big_font = pygame.font.SysFont("arial", 40)

    # Animation/images
    HACKER_IMG = "assets/hacker.png"
    DEFENDER_IMG = "assets/defender.png"
    ANIMATE = os.path.exists(HACKER_IMG) and os.path.exists(DEFENDER_IMG)
    if ANIMATE:
        hacker_img = pygame.transform.scale(pygame.image.load(HACKER_IMG), (80, 80))
        defender_img = pygame.transform.scale(pygame.image.load(DEFENDER_IMG), (80, 80))

    def draw_text(surface, text, pos, color, fontx=font):
        surface.blit(fontx.render(text, True, color), pos)

    state = GameState()
    hacker_pos = HACKER_START_X
    clock = pygame.time.Clock()

    while True:
        screen.fill(DARK_BLUE)
        # Draw hacker
        if ANIMATE:
            screen.blit(hacker_img, (hacker_pos - 40, HACKER_Y - 40))
        else:
            pygame.draw.circle(screen, RED, (hacker_pos, HACKER_Y), 40)
            draw_text(screen, "Hacker", (hacker_pos - 35, HACKER_Y - 60), WHITE)
        # Draw defender
        if ANIMATE:
            screen.blit(defender_img, (DEFENDER_X - 40, HACKER_Y - 40))
        else:
            pygame.draw.rect(screen, GREEN, (DEFENDER_X - 40, HACKER_Y - 40, 80, 80))
            draw_text(screen, "Defender", (DEFENDER_X - 40, HACKER_Y - 60), WHITE)

        draw_text(screen, f"Coins: {state.score}", (10, 10), YELLOW)
        draw_text(screen, f"Hacker Steps: {state.hacker_steps}/6", (10, 40), WHITE)

        if not state.game_over:
            draw_text(screen, "Question:", (200, 30), CYAN, font)
            draw_text(screen, state.current_q['q'], (200, 60), WHITE, font)
            for i, opt in enumerate(state.current_q['options']):
                rect = pygame.Rect(220, 110 + i*70, 600, 50)
                color = LIGHT_GREEN if state.selected_option == i else WHITE
                pygame.draw.rect(screen, color, rect)
                draw_text(screen, f"{chr(65+i)}) {opt}", (230, 120 + i*70), BLACK)
            draw_text(screen, state.message, (200, 400), ORANGE)
        else:
            draw_text(screen, "GAME OVER!", (330, 350), RED, big_font)
            draw_text(screen, f"Total Coins: {state.score}", (330, 300), YELLOW, big_font)
            draw_text(screen, "Press R to restart.", (330, 250), WHITE, font)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if state.game_over:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    state.reset()
                    hacker_pos = HACKER_START_X
            else:
                if event.type == pygame.KEYDOWN:
                    if pygame.K_a <= event.key <= pygame.K_d:
                        idx = event.key - pygame.K_a
                        state.selected_option = idx
                        state.answer(idx)
                        hacker_pos = HACKER_START_X + STEP_SIZE * state.hacker_steps
        clock.tick(30)

# -------------- Launcher --------------
def main():
    print("Select graphics library to use:")
    print("1. Arcade")
    print("2. Pygame")
    lib = input("Enter 1 or 2: ").strip()
    if lib == "1":
        run_arcade_version()
    elif lib == "2":
        run_pygame_version()
    else:
        print("Invalid selection.")

if __name__ == "__main__":
    main()