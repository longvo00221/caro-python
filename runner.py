import pygame
import sys
import time
import os
import tictactoe as ttt

pygame.init()
size = width, height = 600, 400

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode(size)

mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)
result_written = False
view_history_clicked = False
user = None
board = ttt.initial_state()
ai_turn = False


def load_game_history():
    if os.path.exists('game_results.txt'):
        with open('game_results.txt', 'r') as results_file:
            return results_file.readlines()
    else:
        return None
def write_game_result(winner):
    with open('game_results.txt', 'a+') as results_file:
        game_number = sum(1 for line in results_file)
        game_number += 1  
 
        if winner is None:
            results_file.write(f"Game result: Tie.\n")
        else:
            results_file.write(f"Game result: {winner} wins.\n")
def view_game_history():
    global screen
    screen.fill(black) 

    game_history = load_game_history()

    if game_history:
        for i, result in enumerate(game_history):
            result_text = mediumFont.render(result, True, white)
            screen.blit(result_text, (50, 50 + i * 40))
    else:
        no_history_text = mediumFont.render("No game history found.", True, white)
        screen.blit(no_history_text, (50, 50))


    backButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
    back = mediumFont.render("Back to Main", True, black)
    backRect = back.get_rect()
    backRect.center = backButton.center
    pygame.draw.rect(screen, white, backButton)
    screen.blit(back, backRect)

    pygame.display.flip() 

   
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if backButton.collidepoint(mouse):
                    return
        

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(black)

    if user is None:

        title = largeFont.render("Play Tic-Tac-Toe", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        playX = mediumFont.render("Play as X", True, black)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, white, playXButton)
        screen.blit(playX, playXRect)
        viewHistoryButton = pygame.Rect(width / 3, height - 130, width / 3, 50)
        viewHistory = mediumFont.render("View History", True, black)
        viewHistoryRect = viewHistory.get_rect()
        viewHistoryRect.center = viewHistoryButton.center
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if viewHistoryButton.collidepoint(mouse) and not view_history_clicked:
                view_game_history()
                view_history_clicked = True
            elif playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.X
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.O
        else:
            view_history_clicked = False
        pygame.draw.rect(screen, white, viewHistoryButton)
        screen.blit(viewHistory, viewHistoryRect)
        playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
        playO = mediumFont.render("Play as O", True, black)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, white, playOButton)
        screen.blit(playO, playORect)

        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.X
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.O

    else:

        tile_size = 80
        tile_origin = (width / 2 - (1.5 * tile_size),
                       height / 2 - (1.5 * tile_size))
        tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                pygame.draw.rect(screen, white, rect, 3)

                if board[i][j] != ttt.EMPTY:
                    move = moveFont.render(board[i][j], True, white)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        game_over = ttt.terminal(board)
        player = ttt.player(board)

        if game_over:
            if not result_written: 
                winner = ttt.winner(board)
                write_game_result(winner)
                result_written = True
            if winner is None:
                title = f"Game Over: Tie."
            else:
                title = f"Game Over: {winner} wins."
        elif user == player:
            title = f"Play as {user}"
        else:
            title = f"Computer thinking..."
        title = largeFont.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)
        restartIcon = pygame.image.load('icon/reload-ico-2.png')
        restartIcon = restartIcon.convert_alpha()
        restartIcon = pygame.transform.scale(restartIcon, (40, 40)) 
        restartButton = pygame.Rect(20, 20, 40, 40)
        restart = mediumFont.render("Restart Game", True, black)
        restartRect = restart.get_rect()
        restartRect.center = restartButton.center
        screen.blit(restartIcon, restartButton)
        if user != player and not game_over:
            if ai_turn:
                time.sleep(0.5)
                move = ttt.minimax(board)
                board = ttt.result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    if (board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse)):
                        board = ttt.result(board, (i, j))
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if restartButton.collidepoint(mouse):
                time.sleep(0.2)
                user = None
                board = ttt.initial_state()
                ai_turn = False
                result_written = False
        if game_over:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = mediumFont.render("Play Again", True, black)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, white, againButton)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    board = ttt.initial_state()
                    ai_turn = False
                    result_written = False

    pygame.display.flip()
