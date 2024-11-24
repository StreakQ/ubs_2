import sys
from PyQt6.QtWidgets import (QMainWindow, QTableWidget, QTableWidgetItem, QApplication, QDialog, QLabel, QVBoxLayout,
                             QMessageBox, QTextEdit, QLineEdit, QPushButton)
from PyQt6 import uic
import matplotlib.pyplot as plt
import networkx as nx
from PyQt6.QtGui import QPixmap


class ImageDialog(QDialog):
    def __init__(self, image_path):
        super().__init__()
        self.setWindowTitle("Graph Image")
        layout = QVBoxLayout()
        label = QLabel(self)
        pixmap = QPixmap(image_path)
        label.setPixmap(pixmap)
        layout.addWidget(label)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        self.setup_ui()
        self.show()

    def setup_ui(self):
        self.Amatrix = self.findChild(QTableWidget, "Amatrix")
        self.shortest_way = self.findChild(QTextEdit, "last_node_txt")
        self.std_input.clicked.connect(self.standart_input)
        self.make_std_graph.clicked.connect(lambda: self.make_standart_graph(self.Amatrix))
        self.make_orient_graph_btn.clicked.connect(lambda: self.make_orient_graph(self.Amatrix))
        self.make_short_way_btn.clicked.connect(self.find_shortest_path)

        self.Amatrix.setRowCount(17)
        self.Amatrix.setColumnCount(17)
        for i in range(17):
            self.Amatrix.setColumnWidth(i, 30)
            self.Amatrix.setRowHeight(i, 30)

    def standart_input(self):
        matrix = [
            [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  # 1
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],  # 2
            [0, 0, 0, 0, 4, 0, 5, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0],  # 3
            [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  # 4
            [0, 0, 0, 3, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 5
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0],  # 6
            [2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 7
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0],  # 8
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 3, 0],  # 9
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],  # 10
            [3, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 11
            [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 2, 0],  # 12
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],  # 13
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],  # 14
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 15
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0],  # 16
            [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 17
        ]
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                item = QTableWidgetItem(str(matrix[i][j]))
                self.Amatrix.setItem(i, j, item)

    def extract_data_from_table(self, table):
        matr = []
        for i in range(table.rowCount()):
            row = []
            for j in range(table.columnCount()):
                item = table.item(i, j)
                row.append(int(item.text()))
            matr.append(row)
        return matr

    def get_edges_from_table(self, table):
        matr = self.extract_data_from_table(table)
        edges = []
        for i in range(len(matr)):
            for j in range(len(matr[0])):
                if matr[i][j] != 0:
                    crt = (i + 1, j + 1, matr[i][j])
                    edges.append(crt)
        return edges

    def find_levels(self, graph):
        levels = {}  # Словарь для хранения уровней
        visited = set()  # Множество для отслеживания посещенных узлов
        in_degree = {node: 0 for node in graph.nodes()}  # Входящие дуги для каждого узла

        # Подсчитываем входящие дуги для каждого узла
        for u, v in graph.edges():
            in_degree[v] += 1

        current_level = 0

        while len(visited) < len(graph.nodes()):
            # Находим узлы текущего уровня
            current_level_nodes = [node for node in graph.nodes() if in_degree[node] == 0 and node not in visited]

            # Добавляем узлы текущего уровня в словарь уровней
            levels[current_level] = current_level_nodes

            # Обновляем входящие дуги для соседей
            for node in current_level_nodes:
                visited.add(node)
                for neighbor in graph.successors(node):
                    in_degree[neighbor] -= 1  # Уменьшаем количество входящих дуг для соседей

            current_level += 1  # Переход к следующему уровню

        return levels

    def define_node_positions(self, levels):
        pos = {}
        for level, nodes in levels.items():
            for i, node in enumerate(nodes):
                pos[node] = (level, i)
        return pos

    def find_shortest_path(self):
        # Получаем номер узла, до которого нужно найти кратчайший путь
        target_node = self.shortest_way.toPlainText()
        if not target_node.isdigit() or int(target_node) < 1 or int(target_node) > 17:
            QMessageBox.warning(self, "Ошибка ввода", "Введите корректный номер узла (от 1 до 17).")
            return

        target_node = int(target_node)
        # Получаем граф из таблицы
        edges = self.get_edges_from_table(self.Amatrix)
        G = nx.DiGraph()
        G.add_weighted_edges_from(edges)

        # Находим уровни графа
        levels = self.find_levels(G)
        pos = self.define_node_positions(levels)

        # Определяем узлы нулевого уровня
        zero_level_nodes = levels.get(0, [])
        if not zero_level_nodes:
            QMessageBox.warning(self, "Ошибка", "Нет узлов на нулевом уровне.")
            return

        # Используем первый узел нулевого уровня в качестве источника
        source_node = zero_level_nodes[0]

        # Используем алгоритм Дейкстры для нахождения кратчайшего пути
        try:
            shortest_path = nx.dijkstra_path(G, source=source_node, target=target_node)
            shortest_path_length = nx.dijkstra_path_length(G, source=source_node, target=target_node)
            QMessageBox.information(self, "Кратчайший путь",
                                    f"Кратчайший путь до узла {target_node}: {shortest_path}\nДлина пути: {shortest_path_length}")

            # Рисуем граф с выделенным кратчайшим путем
            plt.figure(figsize=(12, 10))
            nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1000, font_size=14, font_color='black',
                    font_weight='bold', edge_color='black', arrows=True)
            edge_labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

            # Выделяем кратчайший путь
            path_edges = list(zip(shortest_path[:-1], shortest_path[1:]))
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)

            plt.savefig("shortest_path.png")
            dialog = ImageDialog("shortest_path.png")
            dialog.exec()
        except nx.NetworkXNoPath:
            QMessageBox.warning(self, "Ошибка", f"Кратчайший путь до узла {target_node} не существует.")

    def make_standart_graph(self, table):
        edges = self.get_edges_from_table(table)
        G = nx.DiGraph()
        # nodes = list(range( 1, 18))
        # G.add_nodes_from(nodes)
        G.add_weighted_edges_from(edges)

        # Рисуем граф
        plt.figure(figsize=(12, 10))
        pos = nx.spring_layout(G, k=0.5)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1000, font_size=14, font_color='black',
                font_weight='bold', edge_color='black', arrows=True)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        plt.savefig("directed_graph_17_nodes.png")
        dialog = ImageDialog("directed_graph_17_nodes.png")
        dialog.exec()

    def make_orient_graph(self, table):
        G = nx.DiGraph()
        edges = self.get_edges_from_table(table)
        G.add_weighted_edges_from(edges)

        levels = self.find_levels(G)
        pos = self.define_node_positions(levels)

        # Рисуем граф
        try:
            plt.figure(figsize=(12, 10))
            nx.draw_networkx_nodes(G, pos, node_size=300)
            nx.draw_networkx_edges(G, pos, arrows=True)
            nx.draw_networkx_labels(G, pos, font_family='sans-serif', font_size=10, font_color='black',
                                    font_weight='bold')
            edge_labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
            plt.axis('off')
            plt.savefig("orient_graph_17_nodes.png")
            print("Graph saved successfully.")
        except Exception as e:
            print(f"Error while drawing the graph: {e}")

        dialog = ImageDialog("orient_graph_17_nodes.png")
        dialog.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())