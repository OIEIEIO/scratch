import tkinter as tk

class GridApp:
    def __init__(self, root, grid_size=(6, 6), width=1360, height=500):
        self.root = root
        self.grid_size = grid_size
        self.width = width
        self.height = height
        self.root.title("Hover Grid Test - Dark Mode")
        self.root.geometry(f"{self.width}x{self.height}")  # Set initial size

        # Create resizable canvas
        self.canvas = tk.Canvas(root, bg="#222222", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)  # Allow window resizing

        # Track highlighted cell
        self.highlighted_cell = None

        # Draw the grid
        self.draw_grid()

        # Bind events
        self.canvas.bind("<Motion>", self.on_hover)
        self.canvas.bind("<Button-1>", self.on_click)
        self.root.bind("<Configure>", self.on_resize)  # Handle window resizing

    def draw_grid(self):
        """Draws a dynamic grid based on grid_size and current window size."""
        self.canvas.delete("all")  # Clear old grid
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        # Calculate dynamic cell size
        self.cell_width = width // self.grid_size[0]
        self.cell_height = height // self.grid_size[1]

        # Draw the grid
        self.cell_rects = {}  # Store references to each cell
        for col in range(self.grid_size[0]):
            for row in range(self.grid_size[1]):
                x0, y0 = col * self.cell_width, row * self.cell_height
                x1, y1 = x0 + self.cell_width, y0 + self.cell_height
                rect_id = self.canvas.create_rectangle(
                    x0, y0, x1, y1, outline="#444444", fill="#222222", tags="cell"
                )
                self.cell_rects[(row, col)] = rect_id  # Store reference

        # Display mouse position text
        self.mouse_label = self.canvas.create_text(10, height - 10, anchor="sw", fill="white", font=("Arial", 12), text="Mouse Position: (0,0)")

    def on_hover(self, event):
        """Handles mouse hover, highlights the cell under the cursor."""
        col, row = event.x // self.cell_width, event.y // self.cell_height

        # Only update if we're over a new cell
        if (row, col) != self.highlighted_cell:
            self.highlighted_cell = (row, col)

            # Reset all cells to default dark mode color
            for key, rect_id in self.cell_rects.items():
                self.canvas.itemconfig(rect_id, fill="#222222")

            # Highlight the hovered cell in blue
            if (row, col) in self.cell_rects:
                self.canvas.itemconfig(self.cell_rects[(row, col)], fill="blue")

        # Update mouse position text
        self.canvas.itemconfig(self.mouse_label, text=f"Mouse Position: ({event.x},{event.y})")

    def on_click(self, event):
        """Handles mouse click and marks the exact clicked position."""
        self.canvas.delete("click_marker")  # Remove old click markers

        # Draw a red dot exactly where the user clicked
        dot_size = 6
        self.canvas.create_oval(event.x - dot_size, event.y - dot_size, event.x + dot_size, event.y + dot_size, fill="red", tags="click_marker")

        print(f"🖱 Clicked at Exact Position ({event.x}, {event.y}) in Grid Cell ({event.y // self.cell_height}, {event.x // self.cell_width})")

    def on_resize(self, event):
        """Redraws grid dynamically when window is resized."""
        self.draw_grid()

if __name__ == "__main__":
    root = tk.Tk()
    app = GridApp(root, grid_size=(6, 6), width=1360, height=500)
    root.mainloop()
