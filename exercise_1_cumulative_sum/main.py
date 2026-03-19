"""
Exercise 1: Cumulative Sum with Live Graph
===========================================
A PyQt5 + pyqtgraph application that captures numeric key presses (1-5),
maintains a running cumulative sum, and displays a real-time step-function
graph over a 30-second sliding window.

Controls:
    - Keys 1-5: Add the pressed number to the cumulative sum
    - R key or Reset button: Reset the sum to zero
    - Esc key or Exit button: Close the application

"""

import sys
import time
from typing import List, Tuple

import numpy as np
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
import pyqtgraph as pg


class CumulativeSumApp(QMainWindow):
    """Main application window for the cumulative sum with live graph.

    The application captures key presses for digits 1-5, accumulates their
    values, and plots the sum history as a step function over a 30-second
    sliding window that updates in real time.

    Attributes:
        WINDOW_SECONDS: Duration of the visible time window in the graph.
        REFRESH_RATE_MS: Graph refresh interval in milliseconds (~30 FPS).
    """

    WINDOW_SECONDS: int = 30
    REFRESH_RATE_MS: int = 33  # ~30 Hz

    def __init__(self) -> None:
        super().__init__()
        self._cumulative_sum: int = 0
        self._start_time: float = time.time()
        # History stores (absolute_timestamp, sum_value) pairs
        self._history: List[Tuple[float, int]] = [(self._start_time, 0)]

        self._init_ui()
        self._init_timer()

    def _init_ui(self) -> None:
        """Build the user interface: sum label, plot widget, and buttons."""
        self.setWindowTitle("Cumulative Sum — Live Graph")
        self.setMinimumSize(800, 500)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # --- Sum display ---
        self._sum_label = QLabel("Cumulative Sum: 0")
        self._sum_label.setAlignment(Qt.AlignCenter)
        self._sum_label.setStyleSheet(
            "font-size: 28px; font-weight: bold; padding: 10px;"
        )
        layout.addWidget(self._sum_label)

        # --- Live graph (pyqtgraph) ---
        self._plot_widget = pg.PlotWidget()
        self._plot_widget.setBackground("w")
        self._plot_widget.setLabel("left", "suma acumulada")
        self._plot_widget.setLabel("bottom", "tiempo (s)")
        self._plot_widget.setXRange(-self.WINDOW_SECONDS, 0)
        self._plot_widget.showGrid(x=True, y=True, alpha=0.3)
        # Orange pen to match the style shown in the assignment examples
        self._curve = self._plot_widget.plot(
            pen=pg.mkPen(color="#E8743B", width=2)
        )
        layout.addWidget(self._plot_widget)

        # --- Buttons ---
        btn_layout = QHBoxLayout()

        self._reset_btn = QPushButton("Reset (R)")
        self._reset_btn.setStyleSheet("padding: 8px 20px; font-size: 14px;")
        self._reset_btn.clicked.connect(self._reset)
        btn_layout.addWidget(self._reset_btn)

        self._exit_btn = QPushButton("Exit (Esc)")
        self._exit_btn.setStyleSheet("padding: 8px 20px; font-size: 14px;")
        self._exit_btn.clicked.connect(self.close)
        btn_layout.addWidget(self._exit_btn)

        layout.addLayout(btn_layout)

        # --- Instructions ---
        instructions = QLabel(
            "Press keys 1-5 to add to the sum  |  R = Reset  |  Esc = Exit"
        )
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("color: #666; padding: 5px;")
        layout.addWidget(instructions)

    def _init_timer(self) -> None:
        """Start a QTimer that refreshes the graph at ~30 FPS."""
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_plot)
        self._timer.start(self.REFRESH_RATE_MS)

    # ---- Event handling ----

    def keyPressEvent(self, event) -> None:
        """Handle key press events for digit keys 1-5, R, and Escape."""
        key = event.key()

        if Qt.Key_1 <= key <= Qt.Key_5:
            value = key - Qt.Key_0  # Convert key code to integer 1-5
            self._cumulative_sum += value
            self._history.append((time.time(), self._cumulative_sum))
            self._sum_label.setText(
                f"Cumulative Sum: {self._cumulative_sum}"
            )
        elif key == Qt.Key_R:
            self._reset()
        elif key == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

    # ---- Actions ----

    def _reset(self) -> None:
        """Reset the cumulative sum to zero and record it in the history."""
        self._cumulative_sum = 0
        self._history.append((time.time(), 0))
        self._sum_label.setText("Cumulative Sum: 0")

    # ---- Graph update ----

    def _update_plot(self) -> None:
        """Refresh the graph with the cumulative sum over the last 30 seconds.

        The graph is drawn as a step function (staircase): horizontal lines
        between events, with vertical jumps at each keypress or reset.
        Only data within the 30-second sliding window is displayed.
        """
        now = time.time()
        cutoff = now - self.WINDOW_SECONDS

        # Prune history: keep the last point before cutoff (for left-edge
        # anchoring) and all points within the window.
        pruned: List[Tuple[float, int]] = []
        for i, (t, v) in enumerate(self._history):
            if t >= cutoff:
                # Include the point just before cutoff to anchor left edge
                if i > 0 and self._history[i - 1][0] < cutoff:
                    pruned.append(self._history[i - 1])
                pruned.extend(self._history[i:])
                break

        if not pruned:
            # All points are older than 30s; use the last known value
            pruned = [self._history[-1]] if self._history else [(now, 0)]

        self._history = pruned  # Keep memory bounded

        # Build step-function data points (relative time where 0 = now)
        x_data: List[float] = []
        y_data: List[float] = []

        for i, (t, v) in enumerate(pruned):
            rel_t = max(t - now, -self.WINDOW_SECONDS)

            if i > 0:
                # Horizontal line: extend previous value to this timestamp
                x_data.append(rel_t)
                y_data.append(pruned[i - 1][1])

            # Vertical jump to new value
            x_data.append(rel_t)
            y_data.append(v)

        # Extend the last value to the current moment (t=0)
        x_data.append(0.0)
        y_data.append(pruned[-1][1])

        self._curve.setData(x_data, y_data)
        self._plot_widget.setXRange(-self.WINDOW_SECONDS, 0)


def main() -> None:
    """Entry point: create the application and show the main window."""
    app = QApplication(sys.argv)
    window = CumulativeSumApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
