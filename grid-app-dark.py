#grid-app-dark.py

import tkinter as tk

class HoverGridApp:
    def __init__(self, root, grid_size=8, box_size=80):
        """
        Creates a dark-themed grid UI where boxes highlight on hover.

        :param root: Tkinter root window
        :param grid_size: Number of rows and columns (square grid)
        :param box_size: Size of each box in pixels
        """
        self.grid_size = grid_size
        self.box_size = box_size
        self.canvas_size = grid_size * box_size
        
        # Colors (Dark Theme)
        self.bg_color = "#2d2d2d"  # Dark background
        self.grid_color = "#1e1e1e"  #  Darker for grid lines
        self.hover_color = "#3a86ff"  # Bright blue highlight
        self.text_color = "#ffffff"  # White text

        # Configure window
        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size, bg=self.bg_color, highlightthickness=0)
        self.canvas.pack()

        # Store rectangles and track the current highlighted cell
        self.rects = {}
        self.active_cell = None

        # Draw grid
        self.draw_grid()

        # Bind mouse movement
        self.canvas.bind("<Motion>", self.on_mouse_move)

        # Mouse position label (Dark text)
        self.mouse_label = tk.Label(root, text="Mouse Position: (0,0)", fg=self.text_color, bg=self.bg_color, font=("Arial", 12))
        self.mouse_label.pack(pady=10)

        # Apply dark theme to the root window
        root.configure(bg=self.bg_color)

    def draw_grid(self):
        """Draws the grid lines and stores rectangle objects."""
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x1, y1 = i * self.box_size, j * self.box_size
                x2, y2 = x1 + self.box_size, y1 + self.box_size
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, outline=self.grid_color, fill=self.bg_color)
                self.rects[(i, j)] = rect

    def on_mouse_move(self, event):
        """Handles mouse movement and highlights the hovered cell."""
        x, y = event.x, event.y
        i, j = x // self.box_size, y // self.box_size

        # Update the mouse position label
        self.mouse_label.config(text=f"Mouse Position: ({x},{y})")

        # If the mouse moves into a new cell, highlight it
        if (i, j) != self.active_cell:
            # Reset previous highlight
            if self.active_cell:
                self.canvas.itemconfig(self.rects[self.active_cell], fill=self.bg_color)
            
            # Highlight new cell
            if (i, j) in self.rects:
                self.canvas.itemconfig(self.rects[(i, j)], fill=self.hover_color)
                self.active_cell = (i, j)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Hover Grid Test - Dark Mode")
    app = HoverGridApp(root, grid_size=8, box_size=80)  # Adjust grid size & box size as needed
    root.mainloop()
