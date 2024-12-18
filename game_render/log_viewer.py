import os
import re


class LogViewer:
    def __init__(self, log, x, y, width, height, font):
        self.font = font
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.log = log
        self.scroll_offset = 0

    def get_text_to_show(self, turn):
        text = []
        last_index = 0
        for i, log_entry in enumerate(self.log):
            if get_turn(log_entry) == -1:
                if last_index <= turn:
                    text[last_index] += log_entry
                continue
            elif get_turn(log_entry) <= turn:
                text.append(log_entry)
            else:
                break
            last_index = i
        return text

    def get_text_to_print(self, turn):
        text = []
        last_index = 0
        for i, log_entry in enumerate(self.log):
            if get_turn(log_entry) == -1:
                if last_index <= turn and text:
                    text[-1] += log_entry
                elif not text:
                    text.append(log_entry)
                continue
            elif get_turn(log_entry) == turn:
                text.append(log_entry)
            elif get_turn(log_entry) > turn:
                break
            last_index = i
        return text

    def draw(self, turn, screen, color):
        lines_to_display = self.height // self.font.get_height()

        text = self.get_text_to_show(turn)

        y_offset = self.y + self.height - self.font.get_height()
        for i in range(len(text) - 1, -1, -1):
            if i >= len(text) - self.scroll_offset - lines_to_display:
                text_surface = self.font.render(text[i], True, color)
                screen.blit(text_surface, (self.x, y_offset))
                y_offset -= text_surface.get_height()

            if y_offset < self.y:
                break

    def print_log_entries(self, turn):
        try:
            text = self.get_text_to_print(turn)
            for l in text:
                print(l)
        except Exception as e:
            print(f"Something went wrong: {e}")


def get_turn(log_entry):
    match = re.search(r"at turn (\d+)", log_entry)
    if match:
        turn_value = match.group(1)
        return int(turn_value)
    return -1

