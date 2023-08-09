import sys
import time
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QListWidget, QTimeEdit
from PyQt5.QtCore import QTimer, Qt
from persistente import *

class WidgetInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Tarefas')
        #Dimenções da janela
        self.setGeometry(1600, 40, 300, 400)
        
        layout = QVBoxLayout()

        ## Bloco exibe o relogio no widget
        self.time_label = QLabel(self)
        #centraliza o texto horizontalmente
        self.time_label.setAlignment(Qt.AlignHCenter)
        layout.addWidget(self.time_label)

        self.update_time()  # Inicializa o label com a hora atual

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Atualiza a cada 1 segundos

        ## Bloco dos textos
        # Bloco listagem de tarefas
        self.task_list = QListWidget(self)
        layout.addWidget(self.task_list)
        # Lê o conteúdo do arquivo de persistencia
        try:
            with open('task_bank.txt', 'r') as file:
                for line in file:
                    task = line.strip()
                    self.task_list.addItem(task)
        except FileNotFoundError:
            pass  # Arquivo não existe ainda, pode ser a primeira execução

        ## Bloco Entrada de tarefas
        self.task_entry = QLineEdit(self)
        layout.addWidget(self.task_entry)
        #Adição da hora marcada
        self.time_entry = QTimeEdit(self)
        layout.addWidget(self.time_entry)
        
        ## Bloco de botão de adicinar tarefa
        self.add_button = QPushButton("Adicionar Tarefa", self)
        self.add_button.clicked.connect(self.add_task)
        layout.addWidget(self.add_button)
        
        self.setLayout(layout)

        self.tasks = [load_task_list]

    def update_time(self):
        current_time = time.strftime('%H:%M:%S')
        self.time_label.setText(f'Hora atual: {current_time}')

    # Função de adição de tarefa a lista de tarefas
    def add_task(self):
        #Pega o texto da tarefa digitada
        task = self.task_entry.text()
        #Pega o horário da tarefa digitada
        time = self.time_entry.time().toString("HH:mm")
        # Combinação de hora e tarefa
        full_task = f"{time} - {task}"  
        self.task_list.addItem(full_task)
        self.tasks.append(full_task)
        self.task_entry.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = WidgetInterface()
    widget.show()
    sys.exit(app.exec_())