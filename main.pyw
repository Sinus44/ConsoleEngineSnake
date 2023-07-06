from Engine import *
import time
import random

class Menu(Scene):
	def select(self):
		self.frame = Frame(window=self.window, style=self.style)
		self.border = Border(window=self.window, style=self.style)

		self.title_label = Label(window=self.window, x=self.window.w // 2 - 4, y=3, text=f"Snake Game", style=self.style)
		self.start_button = Button(window=self.window, x=self.window.w // 2  - 3, y=6, text="Start", style=self.style, on_left_click=self.start_button_left_click)
		self.options_button = Button(window=self.window, x=self.window.w // 2 - 4, y=8, text="Options", style=self.style, on_left_click=self.options_button_left_click)
		self.quit_button = Button(window=self.window, x=self.window.w // 2 - 2, y=10, text="Quit", style=self.style, on_left_click=self.quit_button_left_click)

	def start_button_left_click(self, event):
		self.scene_control.set("game")

	def quit_button_left_click(self, event):
		self.app.stop()

	def options_button_left_click(self, event):
		self.scene_control.set("options")

	def draw(self):
		for event in self.window.input_tick():
			self.title_label.event(event)
			self.start_button.event(event)
			self.options_button.event(event)
			self.quit_button.event(event)

			if event["type"] == "exit":
				self.app.enable = False

		self.frame.draw()
		self.border.draw()
		self.title_label.draw()
		self.start_button.draw()
		self.options_button.draw()
		self.quit_button.draw()
		self.window.print()

class Game(Scene):
	def select(self):
		self.directions = {
			"left": (-1, 0),
			"right": (1, 0),
			"up": (0, -1),
			"down": (0, 1),
			"pause": (0, 0)
		}

		self.keys = {}
		self.key_changed = True
		self.apple = {"x": 0, "y": 0}
		self.frame_count = 0
		self.question = True
		self.pause = False
		self.speed = 8
		self.direction = self.directions["pause"]
		self.current_direction = self.direction

		self.snake = [{"x": self.window.w // 2, "y": self.window.h // 2}]
		self.generate_apple()

	def generate_apple(self):
		self.apple["x"] = random.randint(0, self.window.w - 1)
		self.apple["y"] = random.randint(0, self.window.h - 1)
		if self.is_snake(self.apple):
			self.generate_apple()

	def is_snake(self, pos):
		for segment in self.snake:
			if segment["x"] == pos["x"] and segment["y"] == pos["y"]:
				return True
		return False

	def on_board(self, pos):
		if pos["x"] >= 0 and pos["x"] < self.window.w and pos["y"] >= 0 and pos["y"] < self.window.h:
			return True
		return False

	def draw(self):
		self.window.fill(Symbol(background_color=Color.default, char=" "))

		for event in self.window.input_tick():
			if event["type"] == "exit":
				self.app.enable = False

			elif event["type"] == "keyboard":
				self.key_changed = (event["key_state"] != self.keys[event["key_code"]]) if event["key_code"] in self.keys else True
				self.keys[event["key_code"]] = event["key_state"] 

				if not self.pause:
					if 83 in self.keys and self.keys[83]:
						self.direction = self.directions["down"]

					if 87 in self.keys and self.keys[87]:
						self.direction = self.directions["up"]

					if 65 in self.keys and self.keys[65]:
						self.direction = self.directions["left"]

					if 68 in self.keys and self.keys[68]:
						self.direction = self.directions["right"]

				if 32 in self.keys and self.keys[32] and self.key_changed:
					self.pause = not self.pause

		if not self.pause:
			if self.frame_count > 21 - min(max(self.app.hardness, 0), 20) and self.direction != self.directions["pause"]:
				if (self.current_direction == self.directions["left"] or self.current_direction == self.directions["pause"]) and self.direction != self.directions["right"]:
					self.current_direction = self.direction

				if (self.current_direction == self.directions["right"] or self.current_direction == self.directions["pause"]) and self.direction != self.directions["left"]:
					self.current_direction = self.direction

				if (self.current_direction == self.directions["down"] or self.current_direction == self.directions["pause"]) and self.direction != self.directions["up"]:
					self.current_direction = self.direction

				if (self.current_direction == self.directions["up"] or self.current_direction == self.directions["pause"]) and self.direction != self.directions["down"]:
					self.current_direction = self.direction

				new_pos = {"x": self.snake[0]["x"] + self.current_direction[0], "y": self.snake[0]["y"] + self.current_direction[1]}
				
				if self.is_snake(new_pos) or (not self.on_board(new_pos) and self.app.walls):
					self.window.set_title(f"You lose, Score {len(self.snake)}")
					self.scene_control.set("menu")

				self.snake.insert(0, new_pos)
				
				if self.apple != new_pos:
					self.snake.pop()

				else:
					if len(self.snake) == self.window.w * self.window.h:
						self.window.set_title("You win")
						self.scene_control.set("menu")
					self.window.set_title(f"Score: {len(self.snake)}")
					self.generate_apple()

				self.frame_count = 0
				self.direction_changed = False

			# Apple
			self.window.point(self.apple["x"], self.apple["y"], Symbol(background_color=Color.rgb_background(255, 0, 0), text_color= Color.rgb_text(255, 255, 255), char="O"))

			# Head
			self.window.point(self.snake[0]["x"], self.snake[0]["y"], Symbol(background_color=Color.rgb_background(0, 180, 0), text_color=Color.rgb_text(0, 0, 0), char=":"))

			# Body
			for segment in self.snake[1:]:
				self.window.point(segment["x"], segment["y"], Symbol(background_color=Color.rgb_background(0, 255, 0), text_color=Color.rgb_text(0, 100, 0), char="8"))

			self.window.print()
			self.frame_count += 1

class Options(Scene):
	def select(self):
		self.frame = Frame(window=self.window, style=self.style)
		self.border = Border(window=self.window, style=self.style)
		self.back_button = Button(window=self.window, x=1, y=1, text="Back", style=self.style, on_left_click=self.back_button_left_click)
		self.hardness_label_hint = Label(window=self.window, x=1, y=3, text="Hardness: ", style=self.style)
		self.hardness_label = Label(window=self.window, x=12, y=3, style=self.style)
		
		self.hardness_sub_button = Button(window=self.window, x=11, y=3, style=self.style, on_left_click=self.hardness_sub_button_left_click)
		self.hardness_sub_button.format = lambda: "-"
		
		self.hardness_add_button = Button(window=self.window, x=14, y=3, style=self.style, on_left_click=self.hardness_add_button_left_click)
		self.hardness_add_button.format = lambda: "+"

		self.walls_checkbox = Checkbox(window=self.window, x=1, y=5, text="Walls", style=self.style, checked=self.app.walls, on_change=self.walls_checkbox_change)

		self.mouse_key = -1

	def back_button_left_click(self, event):
		self.scene_control.set("menu")

	def hardness_sub_button_left_click(self, event):
		self.app.hardness -= 1
		if self.app.hardness < 2:
			self.hardness_sub_button.block()
		else:
			self.hardness_add_button.enable = True

	def hardness_add_button_left_click(self, event):
		self.app.hardness += 1
		if self.app.hardness > 19:
			self.hardness_add_button.block()
		else:
			self.hardness_sub_button.enable = True

	def walls_checkbox_change(self, event):
		#self.walls_checkbox.click()
		self.app.walls = bool(self.walls_checkbox)

	def draw(self):
		for event in self.window.input_tick():
			self.back_button.event(event)
			self.hardness_sub_button.event(event)
			self.hardness_add_button.event(event)
			self.walls_checkbox.event(event)

			if event["type"] == "exit":
				self.app.enable = False

		self.hardness_label.text = self.app.hardness

		self.frame.draw()
		self.border.draw()

		self.hardness_label_hint.draw()
		self.hardness_sub_button.draw()
		self.hardness_add_button.draw()
		self.hardness_label.draw()
		self.walls_checkbox.draw()

		self.back_button.draw()
		self.window.print()

class SnakeGame:
	def __init__(self, w:int=40, h:int=20, hardness:int=15):
		self.hardness = hardness
		self.enable = False
		self.walls = True
		self.style = Style()

		self.window = Window(w, h)
		time.sleep(0.1)
		self.window.set_icon("snake.ico")
		self.window.set_title("Snake on Console Engine")

		self.scene_control = Scene_Control()
		self.scene_control.add_from_dict({
			"menu": Menu(window=self.window, scene_control=self.scene_control, app=self, style=self.style),
			"game": Game(window=self.window, scene_control=self.scene_control, app=self, style=self.style),
			"options": Options(window=self.window, scene_control=self.scene_control, app=self, style=self.style)
		})

		self.scene_control.set("menu")

	def run(self):
		if not self.enable:
			self.enable = True
			self.scene_control.play()

	def stop(self):
		self.scene_control.stop()

if __name__ == "__main__":

	snake_game = SnakeGame()
	snake_game.run()
