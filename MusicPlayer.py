# version 1.0.1 (2-17-22)
import sys

sys.path.insert(0, ".venv/lib/python3.12/site-packages")
import os
import logging
import random
import time
from os import listdir

import pygame
import pygame_menu
import pygame_menu.controls as ctrl

logging.basicConfig()
LOGGER = logging.getLogger()

if sys.platform != "win32":
    ctrl.KEY_APPLY = pygame.K_a
    ctrl.KEY_BACK = pygame.K_b

root_folder = "./music/"

musics: list[str] = listdir(root_folder)
musics = list(filter(lambda p: p.endswith(".mp3"), musics))
LOGGER.info(f"Found {musics=}")


pygame.init()
pygame.display.set_icon(pygame.image.load("A/play.png"))
w = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Music Player")
img1 = pygame.transform.scale(pygame.image.load("A/prev.png"), (100, 100))
img2 = pygame.transform.scale(pygame.image.load("A/pause.png"), (100, 100))
img3 = pygame.transform.scale(pygame.image.load("A/play.png"), (100, 100))
img4 = pygame.transform.scale(pygame.image.load("A/next.png"), (100, 100))
img5 = pygame.transform.scale(pygame.image.load("A/shufOFF.png"), (32, 32))
img6 = pygame.transform.scale(pygame.image.load("A/shufON.png"), (32, 32))
img7 = pygame.transform.scale(pygame.image.load("A/sound.png"), (32, 32))
g = True

font1 = pygame.font.SysFont("Comic Sans MS", 20)
player = True
r = random.choice(list(range(len(musics))))
rr = 0
err = ""
shuf = False
vol = 150


csound = None
channel = pygame.mixer.Channel(0)


def random_song():
    r = random.choice(list(range(len(musics))))
    csound = pygame.mixer.Sound(root_folder + musics[r])
    # csound.set_volume((vol-94)/251)
    channel.play(csound)


menu = pygame_menu.Menu(
    "Welcome",
    600,
    400,
    theme=pygame_menu.themes.THEME_BLUE,
    onclose=pygame_menu.events.CLOSE,
)


def play(m):
    global csound
    if csound:
        csound.stop()

    LOGGER.info("Playing %s", m)
    csound = pygame.mixer.Sound(root_folder + m)
    channel.play(csound)
    menu.close()


# menu2  = pygame_menu.Menu('Welcome', 600, 400, theme=pygame_menu.themes.THEME_BLUE, onclose=pygame_menu.events.BACK)
# menu2.add.button('Something', random_song)


for m in musics:
    menu.add.button(m, play, m)

# menu.add.button('Submenu', menu2)
menu.add.button("Quit", pygame_menu.events.EXIT)


try:
    csound = pygame.mixer.Sound(root_folder + musics[r])
    # csound.set_volume((vol-94)/251)
    channel.play(csound)
except:
    LOGGER.error("Failed to load music", exc_info=True)
    exit()
while g:
    time.sleep(0)
    for event in pygame.event.get():
        LOGGER.debug(event)
        if event.type == pygame.QUIT:
            g = False
            csound.stop()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                csound.stop()

                r = (r + 1) % len(musics)
                csound = pygame.mixer.Sound(root_folder + musics[r])
                channel.play(csound)
            elif event.key == pygame.K_y:
                csound.stop()

                r = (r - 1) % len(musics)
                csound = pygame.mixer.Sound(root_folder + musics[r])
                channel.play(csound)
            elif event.key == pygame.K_x:
                menu.enable()
                menu.mainloop(w)

    w.fill((10, 10, 10))

    (mx, my) = pygame.mouse.get_pos()
    (m1, m2, m3) = pygame.mouse.get_pressed()
    m1r = m1
    if m1 == 1 and mm1 == 1:
        m1 = 0
    else:
        if m1 == 1:
            mm1 = 1
        else:
            mm1 = 0
    if m1 == 1:
        if my > 47:
            if mx < 120:
                if shuf:
                    r = random.randint(0, len(musics) - 1)
                else:
                    r = r - 1
                    if r > len(musics) - 1:
                        r = 0
                try:
                    csound = pygame.mixer.Sound(root_folder + musics[r])
                    # csound.set_volume((vol-94)/251)
                    channel.play(csound)
                    player = True
                    err = ""
                except:
                    # print("Failed to load music")
                    err = "Failed to load music "
            elif mx > 240:
                if shuf:
                    r = random.randint(0, len(musics) - 1)
                else:
                    r = r + 1
                    if r > len(musics) - 1:
                        r = 0
                try:
                    csound = pygame.mixer.Sound(root_folder + musics[r])
                    # csound.set_volume((vol-94)/251)
                    channel.play(csound)
                    player = True
                    err = ""
                except:
                    # print("Failed to load music")
                    err = "Failed to load music "
            else:
                if player:
                    player = False
                    channel.pause()
                else:
                    player = True
                    channel.unpause()
        else:
            if mx < 52:
                if shuf:
                    shuf = False
                else:
                    shuf = True
    if mx > 52 and my < 47 and m1r == 1:
        vol = mx
        if vol < 94:
            vol = 94
        if vol > 345:
            vol = 345
        # csound.set_volume((vol-94)/251)
    if not (channel.get_busy()):
        if shuf:
            r = random.randint(0, len(musics) - 1)
        else:
            r = r + 1
            if r > len(musics) - 1:
                r = 0
        try:
            csound = pygame.mixer.Sound(root_folder + musics[r])
            # csound.set_volume((vol-94)/251)
            channel.play(csound)
            player = True
            err = ""
        except:
            # print("Failed to load music")
            err = "Failed to load music "
    w.blit(img1, (10, 52))
    w.blit(img4, (250, 52))
    pygame.draw.line(w, (200, 200, 200), (94, 26), (345, 26), 5)
    pygame.draw.circle(w, (150, 150, 150), (vol, 26), 10)
    if shuf:
        w.blit(img6, (10, 10))
    else:
        w.blit(img5, (10, 10))
    if player:
        w.blit(img3, (130, 52))
    else:
        w.blit(img2, (130, 52))
    w.blit(img7, (52, 10))
    frnd = font1.render("Now playing : " + err + musics[r], True, (200, 200, 200))
    w.blit(frnd, (360 - rr % (frnd.get_width() + 360), 152))
    rr = rr + 1

    # w.blit(background, (0, 0))
    # render_menu(w, menu_items, menu_positions, font1)
    pygame.display.flip()

pygame.quit()
