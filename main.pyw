from Engine import *
import time
import random

directions = {
	"left": (-1, 0),
	"right": (1, 0),
	"up": (0, -1),
	"down": (0, 1),
	"pause": (0, 0)
}

main_window = Window(40, 20)
time.sleep(1)
main_window.set_icon("snake.ico")

game_fps = 120

def is_snake(pos, snake):
	for segment in snake:
		if segment["x"] == pos["x"] and segment["y"] == pos["y"]:
			return True
	return False

def generate_apple(window, apple, snake):
	apple["x"] = random.randint(0, window.w - 1)
	apple["y"] = random.randint(0, window.h - 1)
	if is_snake(apple, snake):
		generate_apple()

def on_board(pos, window):
	if pos["x"] >= 0 and pos["x"] < window.w and pos["y"] >= 0 and pos["y"] < window.h:
		return True
	return False

def start_game():
	keys = {}
	apple = {"x": 0, "y": 0}
	enable = True
	frame_count = 0
	direction_changed = False
	question = True
	speed = 8
	main_window.set_title("Snake on Console Engine")

	direction = directions["pause"]

	snake = [{"x": main_window.w // 2, "y": main_window.h // 2}]
	generate_apple(main_window, apple, snake)

	while enable:
		time.sleep(1 / game_fps if direction == directions["left"] or direction == directions["right"] else 1 / game_fps * 2)

		main_window.fill(Color.default + " ")
		for event in main_window.input_tick():
			if event["type"] == "exit":
				quit()

			elif event["type"] == "keyboard":
				keys[event["key_code"]] = event["key_state"]

				if 83 in keys and keys[83] and direction != directions["up"] and not direction_changed:
					direction = directions["down"]
					direction_changed = True

				if 87 in keys and keys[87] and direction != directions["down"] and not direction_changed:
					direction = directions["up"]
					direction_changed = True

				if 65 in keys and keys[65] and direction != directions["right"] and not direction_changed:
					direction = directions["left"]
					direction_changed = True

				if 68 in keys and keys[68] and direction != directions["left"] and not direction_changed:
					direction = directions["right"]
					direction_changed = True
		
		if frame_count > 5 and direction != directions["pause"]:
			new_pos = {"x": snake[0]["x"] + direction[0], "y": snake[0]["y"] + direction[1]}
			
			#print(is_snake(new_pos), on_board(new_pos))
			if is_snake(new_pos, snake) or not on_board(new_pos, main_window):
				main_window.set_title("You lose")
				enable = False

			snake.insert(0, new_pos)
			
			if apple != new_pos:
				snake.pop()

			else:
				if len(snake) == main_window.w * main_window.h:
					main_window.set_title("You win")
					enable = False
				main_window.set_title(f"Score: {len(snake)}")
				generate_apple(main_window, apple, snake)

			frame_count = 0
			direction_changed = False

		# Apple
		main_window.point(apple["x"], apple["y"], Color.rgb_background(255, 0, 0) + Color.rgb_text(255, 255, 255) + "O")

		# Head
		main_window.point(snake[0]["x"], snake[0]["y"], Color.rgb_background(0, 180, 0) + Color.rgb_text(0, 0, 0) +":")

		# Body
		for segment in snake[1:]:
			main_window.point(segment["x"], segment["y"], Color.rgb_background(0, 255, 0) + Color.rgb_text(0, 100, 0) + "8")

		main_window.print()
		frame_count += 1

	score_label = Label(screen=main_window, x=10, y=5, text=f"Ваш счёт {len(snake)}", style=Style())
	yes_button = Button(screen=main_window, x=5, y=main_window.h // 2, text = "YES", style=Style())
	no_button = Button(screen=main_window, x=20, y=main_window.h // 2, text = "NO", style=Style())

	while question:
		time.sleep(0.1)

		for event in main_window.input_tick():
			if event["type"] == "mouse":
				yes_button.intersection(event["x"], event["y"])
				no_button.intersection(event["x"], event["y"])

				if event["mouse_type"] == 0 and event["mouse_key"] == 1:
					if yes_button.focused:
						question = False
						start_game()

					if no_button.focused:
						question = False
						quit()

		main_window.fill(Color.default + " ")

		yes_button.draw()
		no_button.draw()
		score_label.draw()

		main_window.text(10, 3, "Начать заново?")
		main_window.print()

if __name__ == "__main__":
	start_game()