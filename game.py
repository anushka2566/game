import pygame
import random
import sys
import time
import os

pygame.init()

# ---------------- Window setup ----------------
WIDTH, HEIGHT = 960, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hacker vs Defender (QA Mode)")

clock = pygame.time.Clock()

# ---------------- Colors ----------------
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (200,0,0)
GREEN = (0,200,0)
YELLOW = (255,200,0)
GRAY = (180,180,180)

# ---------------- Fonts ----------------
FONT = pygame.font.SysFont("arial", 24)
BIGFONT = pygame.font.SysFont("arial", 40, bold=True)

# ---------------- Game state ----------------
money = 100
score = 0
hacker_steps = 0
MAX_HACKER_STEPS = 5  # On step 6, hacker reaches defender

# ---------------- QUESTIONS (50 one-word cyber security Q&A) ----------------
QUESTIONS = [
    ("Unwanted software secretly installed?", "spyware"),
    ("Attack tricking DNS requests?", "pharming"),
    ("Attack between two parties’ communication?", "mitm"),
    ("Hidden small data-stealing program?", "rootkit"),
    ("Protecting data during transfer?", "cryptography"),
    ("Random code to strengthen passwords?", "salt"),
    ("Unique user login identity?", "username"),
    ("Code executed on buffer overflow?", "shellcode"),
    ("Security of cloud storage is called?", "cloudsecurity"),
    ("Security process after incident?", "forensics"),
    ("The first phase of hacking?", "reconnaissance"),
    ("Security test to find weaknesses?", "audit"),
    ("Fake Wi-Fi hotspot attack?", "eviltwin"),
    ("Tool to capture network packets?", "wireshark"),
    ("Document stating security rules?", "policy"),
    ("Backup stored at a remote site?", "offsite"),
    ("Cyber law in India?", "itact"),
    ("Unique value generated from data?", "hash"),
    ("Weakest security link?", "human"),
    ("Email with malicious link?", "phishing"),
    ("Attack using multiple compromised computers?", "botnet"),
    ("Fake message appearing genuine?", "hoax"),
    ("Guessing personal info to hack password?", "social"),
    ("Process of proving ownership?", "verification"),
    ("Attack that locks out legitimate users?", "dos"),
    ("Small text file stored by websites?", "cookie"),
    ("Hidden tracking cookie?", "spycookie"),
    ("Protocol for secure email?", "smtps"),
    ("Weakness due to poor coding?", "bug"),
    ("Small malicious ad on websites?", "malvertising"),
    ("Fake pop-up warning?", "scareware"),
    ("Cybercrime stealing card data?", "skimming"),
    ("Secretly mining cryptocurrency on others devices?", "cryptojacking"),
    ("Attack exploiting buffer size?", "overflow"),
    ("Publicly available security issue notice?", "advisory"),
    ("Extra security beyond password?", "2fa"),
    ("Google tool for safe browsing?", "safesearch"),
    ("Illegal software copy?", "piracy"),
    ("Cybersecurity framework by US gov?", "nist"),
    ("Security rating of systems?", "score"),
    ("Cyber attack on critical infrastructure?", "cyberwarfare"),
    ("Fake login page for stealing credentials?", "spoof"),
    ("Passwordless login method?", "otp"),
    ("Temporary one-time password?", "token"),
    ("Security model: never trust, always verify?", "zerotrust"),
    ("Attacks exploiting day-old flaws?", "zeroday"),
    ("Unauthorized software running on device?", "rogueware"),
    ("Hacker challenge platform?", "ctf"),
    ("Automated security testing tool?", "scanner"),
    ("Agreement on proper use of IT resources?", "aup")
]

# Challenge state
challenge_active = False
current_question = ""
current_answer = ""
typed_answer = ""
challenge_start = 0.0
CHALLENGE_DURATION = 60.0
last_challenge_time = 0.0
CHALLENGE_COOLDOWN = 25.0

# Game over flag
game_over = False

# ---------------- Images ----------------
HACKER_IMG = "hacker.png"
DEFENDER_IMG = "defender.png"
if os.path.exists(HACKER_IMG) and os.path.exists(DEFENDER_IMG):
    hacker_img = pygame.image.load(HACKER_IMG)
    defender_img = pygame.image.load(DEFENDER_IMG)
    hacker_img = pygame.transform.scale(hacker_img, (80, 80))
    defender_img = pygame.transform.scale(defender_img, (80, 80))
else:
    hacker_img = None
    defender_img = None

# Positions
HACKER_START_X = 100
DEFENDER_X = WIDTH - 200
IMAGE_Y = HEIGHT - 120
STEP_SIZE = (DEFENDER_X - HACKER_START_X) // MAX_HACKER_STEPS

# Smooth movement variables
hacker_pos = HACKER_START_X
hacker_target_pos = HACKER_START_X
HACKER_SPEED = 300  # pixels per second

# ---------------- Functions ----------------
def start_challenge():
    global challenge_active, current_question, current_answer, typed_answer, challenge_start, last_challenge_time
    question, answer = random.choice(QUESTIONS)
    current_question = question
    current_answer = answer.lower().strip()
    typed_answer = ""
    challenge_active = True
    challenge_start = time.time()
    last_challenge_time = challenge_start

def end_challenge(correct: bool):
    global challenge_active, hacker_steps, score, money, hacker_target_pos
    challenge_active = False
    if correct:
        score += 10
        money += 20
    else:
        hacker_steps += 1
        hacker_target_pos = HACKER_START_X + STEP_SIZE * hacker_steps

def draw_text_center(surface, text, y, font, color=WHITE):
    txt = font.render(text, True, color)
    surface.blit(txt, (WIDTH//2 - txt.get_width()//2, y))

# ---------------- Main loop ----------------
running = True
while running:
    dt = clock.tick(60) / 1000.0  # seconds

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_over:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif challenge_active:
                if event.key == pygame.K_BACKSPACE:
                    typed_answer = typed_answer[:-1]
                elif event.key == pygame.K_RETURN:
                    if typed_answer.lower().strip() == current_answer:
                        end_challenge(True)
                    else:
                        end_challenge(False)
                else:
                    if len(event.unicode) == 1 and event.unicode.isprintable():
                        typed_answer += event.unicode
            else:
                if event.key == pygame.K_SPACE:
                    start_challenge()

    # Auto challenge
    if (not challenge_active) and (time.time() - last_challenge_time >= CHALLENGE_COOLDOWN):
        start_challenge()

    # Challenge timeout
    if challenge_active and (time.time() - challenge_start >= CHALLENGE_DURATION):
        end_challenge(False)

    # Game over condition
    if hacker_steps > MAX_HACKER_STEPS:
        game_over = True

    # ---------------- Smooth hacker movement ----------------
    if hacker_pos < hacker_target_pos:
        hacker_pos += HACKER_SPEED * dt
        if hacker_pos > hacker_target_pos:
            hacker_pos = hacker_target_pos
    elif hacker_pos > hacker_target_pos:
        hacker_pos -= HACKER_SPEED * dt
        if hacker_pos < hacker_target_pos:
            hacker_pos = hacker_target_pos

    # ---------------- Draw screen ----------------
    screen.fill(BLACK)
    # HUD
    screen.blit(FONT.render(f"Money: {money}    Score: {score}", True, WHITE), (20,20))
    screen.blit(FONT.render(f"Hacker Steps: {hacker_steps} / {MAX_HACKER_STEPS+1}", True, RED if hacker_steps > MAX_HACKER_STEPS else WHITE), (20,50))
    # Images
    if hacker_img:
        screen.blit(hacker_img, (int(hacker_pos), IMAGE_Y))
    else:
        pygame.draw.circle(screen, RED, (int(hacker_pos)+40, IMAGE_Y+40), 40)
    if defender_img:
        screen.blit(defender_img, (DEFENDER_X, IMAGE_Y))
    else:
        pygame.draw.rect(screen, GREEN, (DEFENDER_X, IMAGE_Y, 80, 80))
    # Challenge box
    if challenge_active:
        overlay = pygame.Surface((WIDTH-200, 200))
        overlay.set_alpha(220)
        overlay.fill((50,50,50))
        screen.blit(overlay, (100, HEIGHT//2 - 150))
        draw_text_center(screen, "HACKER CHALLENGE!", HEIGHT//2 - 120, BIGFONT, YELLOW)
        screen.blit(FONT.render("Q: " + current_question, True, WHITE), (120, HEIGHT//2 - 60))
        pygame.draw.rect(screen, WHITE, (120, HEIGHT//2 - 10, WIDTH-240, 40), 2)
        screen.blit(FONT.render(typed_answer, True, WHITE), (130, HEIGHT//2 - 5))
        remaining = max(0, int(CHALLENGE_DURATION - (time.time() - challenge_start)))
        screen.blit(FONT.render(f"Time left: {remaining}s — Press Enter when done", True, YELLOW), (120, HEIGHT//2 + 50))
    else:
        screen.blit(FONT.render("Press SPACE for next challenge (auto after cooldown)", True, GRAY), (20, HEIGHT - 40))
    # Game over screen
    if game_over:
        draw_text_center(screen, "GAME OVER — Hacker Wins!", HEIGHT//2 - 40, BIGFONT, RED)
        draw_text_center(screen, f"Final Score: {score}", HEIGHT//2 + 10, FONT, WHITE)
        draw_text_center(screen, "Press ESC to quit", HEIGHT//2 + 60, FONT, WHITE)
    pygame.display.flip()

pygame.quit()
sys.exit()