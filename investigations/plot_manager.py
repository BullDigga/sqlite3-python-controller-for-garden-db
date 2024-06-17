import matplotlib.pyplot as plt
import itertools
import os


class PlotBuilder:
    def __init__(self, title, xlabel, ylabel):
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.fig, self.ax = plt.subplots()
        self.styles = itertools.cycle(['-', '--', '-.', ':'])
        self.markers = itertools.cycle(['o', 's', '^', 'D', 'v', 'h', '*'])
        self.colors = itertools.cycle(['b', 'g', 'r', 'c', 'm', 'y', 'k'])
        self.series_count = 0

    def add_series(self, x, y, label):
        """Добавляет новый ряд данных на график"""
        style = next(self.styles)
        color = next(self.colors)
        marker = None if len(x) >= 10 else next(self.markers)
        self.ax.plot(x, y, label=label, linestyle=style, color=color, marker=marker)
        self.series_count += 1

    def save(self, filename, format='png'):
        """Сохраняет график в файл"""
        self.ax.set_title(self.title)
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)
        self.ax.legend()
        self.fig.tight_layout()

        valid_formats = ['png', 'svg', 'pdf', 'ps', 'eps']
        if format not in valid_formats:
            raise ValueError(f"Invalid format: {format}. Choose from {valid_formats}.")

        base, ext = os.path.splitext(filename)
        if ext[1:] not in valid_formats:
            filename = f"{base}.{format}"

        self.fig.savefig(filename)
        print(f"Graph saved as {filename}")


if __name__ == "__main__":
    # Пример использования PlotBuilder
    pb = PlotBuilder("Sample Graph", "X-axis", "Y-axis")

    x = [1, 2, 3, 4, 5]
    y1 = [1, 4, 9, 16, 25]
    y2 = [1, 2, 3, 4, 5]

    pb.add_series(x, y1, "Series 1")
    pb.add_series(x, y2, "Series 2")

    pb.save("sample_graph", format="svg")
