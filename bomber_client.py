#!/usr/bin/env python3
# -*- coding: Utf-8 -*
# Author: aurelien.esnard@u-bordeaux.fr

from model import *
from view import *
from keyboard import *
from network import *
import threading
import socket
import sys
import pygame

### python version ###
print("python version: {}.{}.{}".format(sys.version_info[0], sys.version_info[1], sys.version_info[2]))
print("pygame version: ", pygame.version.ver)

################################################################################
#                                 MAIN                                         #
################################################################################

# parse arguments
if len(sys.argv) != 4:
    print("Usage: {} host port nickname".format(sys.argv[0]))
    sys.exit()
host = sys.argv[1]
port = int(sys.argv[2])
nickname = sys.argv[3]

# initialization
pygame.display.init()
pygame.font.init()
clock = pygame.time.Clock()

model = Model()

client = NetworkClientController(model, host, port, nickname)

kb = KeyboardController(client)

# Run first tick for gathering info before display
threading.Thread(None, client.tick,None ,(1000,)).start()

while(not client.ready):
    i = None

view = GraphicView(model, nickname)
# main loop
while True:
    # make sure game doesn't run at more than FPS frames per second
    dt = clock.tick(FPS)
    if not kb.tick(dt): break
    model.tick(dt)
    view.tick(dt)
    threading.Thread(None, client.tick,None ,(dt,)).start()

# quit
print("Game Over!")
pygame.quit()
