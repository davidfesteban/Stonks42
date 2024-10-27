from threading import Thread
from typing import List
import matplotlib.pyplot as plt

class LossLineChart:
    _losses: List
    _plot_interval: int

    def __init__(self):
        self._losses = []
        self._plot_interval = 100
        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], marker='o', linestyle='-', color='b')  # Initial empty line plot
        self.ax.set_title("Average Loss per Epoch")
        self.ax.set_xlabel("Epoch")
        self.ax.set_ylabel("Average Loss")
        self.ax.grid(True)

    def add(self, epoch: int, value: float) -> None:
        self._losses.append((epoch, value))

        if epoch % self._plot_interval == 0:
            Thread(target=self.plot).start()

    def plot(self) -> None:
        epochs, avg_losses = zip(*self._losses)
        self.line.set_data(epochs, avg_losses)
        self.ax.relim()
        self.ax.autoscale_view()
        plt.draw()
        plt.pause(0.001)
