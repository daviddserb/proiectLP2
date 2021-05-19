import numpy as np
import pygame
import random
from constants import CP


N = 4
grid = np.zeros((N, N), dtype=int)  # initializam grila de (N, N), pentru ca este un patrat de N linii si N coloane si variabilele de timp int
W = 400  # latime
H = W  # inaltime
SPACING = 10
pygame.init()
pygame.display.set_caption("2048")  # titlul jocului
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)  # formatul jocului si marimea caracterelor
screen = pygame.display.set_mode((W, H))

def new_number(k=1):
    free_poss = list(zip(*np.where(grid == 0))) #zip le grupeaza 2 cate 2, adica inainte lista era [(0,0,0,0,1,1,etc...)], acum este [(0,0),(0,1),(0,2),(0,3),(1,0),etc...]
    for pos in random.sample(free_poss, k=k): #cand incepi jocul ai valori pe 2 pozitii (acel k)
        if random.random() < .1: #pentru a fi 4 trebuie ca valoarea sa fie sub 10%
            grid[pos] = 4 #valoarea poate sa fie 4 (probabilitate de sub 10% [acel <.1])
        else:
            grid[pos] = 2 #dar poate sa fie si 2 (probabilitate mai mare - peste 90%)

def _get_nums(this):
    this_n = this[this != 0]  # listele cu cifrele diferite de 0
    this_n_sum = []
    skip = False
    for j in range(len(this_n)):
        if skip:
            skip = False
            continue
        if this_n[j] == this_n[j+1] and j != len(this_n) - 1:  # daca ajungem la ultima pozitie, oprim
            new_n = this_n[j] * 2
            skip = True  # sarim peste cazul cand s-a facut operatia si ignoram al 2-lea numar
        else:
            new_n = this_n[j]
        this_n_sum.append(new_n)  # salveaza suma numerelor
    return np.array(this_n_sum)  # se face lista de tip numpy


def make_move(move):
    for i in range(N):
        if move in 'lr':  # daca este stanga sau dreapta
            this = grid[i, :]  # de la linia i la toate coloanele
        else:  # daca este sus sau jos
            this = grid[:, i]  # ne folosim doar de coloane
        flipped = False
        if move in 'ud':  # daca este sus sau jos
            flipped = True
            this = this[::-1]  # o intoarcem si facem acelasi algoritm ca la stanga sau dreapta
        this_n = _get_nums(this)
        new_this = np.zeros_like(this)  # reinitializam cu 0 pozitiile care s-au mutat
        new_this[:len(this_n)] = this_n  # numerele diferite de 0
        if flipped:
            new_this = new_this[::-1]
        if move in 'lr':
            grid[i, :] = new_this  # salvam liniile in matrice
        else:
            grid[:, i] = new_this

def draw_game(screen, grid, myfont): # marian
    screen.fill(CP['back'])  # culorile din background
    for i in range(N):
        for j in range(N):
            n = grid[i][j]
            rect_x = j * W // N + SPACING  # patratelele de pe linii si coloane
            rect_y = i * H // N + SPACING
            rect_w = W // N - 2 * SPACING  # spatierea patretelor pe latime
            rect_h = H // N - 2 * SPACING  # spatierea patretelor pe inaltime
            pygame.draw.rect(screen,
                         CP[n],
                      pygame.Rect(rect_x, rect_y, rect_w, rect_h),  # toate patratelele cu spatierea pe latime si lungime
                             border_radius=8)  # rotunjirea coltului
            if n == 0:
                continue
            text_surface = myfont.render(f'{n}', True, (0, 0, 0))  #  punem valorile/cifrele prin f de string
            text_rect = text_surface.get_rect(center=(rect_x + rect_w/2,  # punerea cifrelor in mijlocul patratelelor
                                                      rect_y + rect_h/2))
            screen.blit(text_surface, text_rect)  # patratele cu valori