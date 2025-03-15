import tkinter as tk

# VM Screen Resolution
VM_WIDTH = 1360
VM_HEIGHT = 768

# Grid Settings (auto-fit to screen)
GRID_ROWS = 6  # Adjust as needed
GRID_COLS = 6  # Adjust as needed
BOX_WIDTH = VM_WIDTH // GRID_COLS
BOX_HEIGHT = VM_HEIGHT // GRID_ROWS

# Tkinter App
class GridApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hover Grid Test - Dark Mode")
        self.root.geometry(f"{VM_WIDTH}x{VM_HEIGHT}")
        self.root.configure(bg="#222222")

        self.canvas = tk.Canvas(self.root, width=VM_WIDTH, height=VM_HEIGHT, bg="#222222", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.boxes = []
        for row in range(GRID_ROWS):
            row_boxes = []
            for col in range(GRID_COLS):
                x1, y1 = col * BOX_WIDTH, row * BOX_HEIGHT
                x2, y2 = x1 + BOX_WIDTH, y1 + BOX_HEIGHT
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill="#333333", outline="#444444")
                row_boxes.append(rect)
            self.boxes.append(row_boxes)

        self.canvas.bind("<Motion>", self.on_hover)
        self.mouse_position_label = tk.Label(self.root, text="Mouse Position: (0,0)", fg="white", bg="#222222")
        self.mouse_position_label.pack(side="bottom", fill="x")

    def on_hover(self, event):
        """Handles mouse movement and highlights the hovered box."""
        row = event.y // BOX_HEIGHT
        col = event.x // BOX_WIDTH

        # Reset colors
        self.canvas.itemconfig("all", fill="#333333")

        # Highlight the hovered box
        if 0 <= row < GRID_ROWS and 0 <= col < GRID_COLS:
            self.canvas.itemconfig(self.boxes[row][col], fill="#0066FF")

        # Update mouse position label
        self.mouse_position_label.config(text=f"Mouse Position: ({event.x},{event.y})")

# Run the App
if __name__ == "__main__":
    root = tk.Tk()
    app = GridApp(root)
    root.mainloop()
