import sys
import time
import threading
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QListWidget
from PyQt5.QtCore import Qt, QTimer

class TaskSchedulerWidget(QWidget):
    def __init__(self):
        super().__init__()
        # Define um título para o Widget 
        self.setWindowTitle('Tarefas')
        #self.setWindowFlags(Qt.Tool)
        # Atributo que o deixa transparente na tela
        #self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(1600, 40, 300, 400)

        layout = QVBoxLayout()

        ## Bloco de título
        self.label = QLabel("Tarefas do dia", self)
        #centraliza o texto horizontalmente
        self.label.setAlignment(Qt.AlignHCenter)
        layout.addWidget(self.label)

        ## Bloco do relógio
        self.clock_label = QLabel(self)
        self.clock_label.setAlignment(Qt.AlignHCenter)
        layout.addWidget(self.clock_label)

        ## Bloco listagem de tarefas
        self.task_list = QListWidget(self)
        layout.addWidget(self.task_list)

        ## Bloco Entrada de tarefas
        self.task_entry = QLineEdit(self)
        layout.addWidget(self.task_entry)

        ## Bloco de botão de adicinar tarefa
        self.add_button = QPushButton("Adicionar Tarefa", self)
        self.add_button.clicked.connect(self.add_task)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

        ## Termino dos blocos
        self.tasks = []
        self.task_thread = None

        #atualiza o relógio a cada 1000 milesegundo (1 segundo)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    ## Blocos de funcionalidades

    # Função que cria o relógio
    def update_time(self):
        current_time = time.strftime('%H:%M:%S')
        self.clock_label.setText(current_time)

    # Função de adição de tarefa a lista de tarefas
    def add_task(self):
        task = self.task_entry.text()
        self.task_list.addItem(task)
        self.tasks.append(task)
        self.task_entry.clear()

    # Função de exibir a notificação quando ha tarefa ativa
    def execute_task(self, task):
        self.show_notification(task)

    # Percorre todas as tarefas na lista, cria uma nova thread para cada tarefa e inicia essa thread. 
    # Isso permite que cada tarefa seja agendada para ser executada em paralelo, sem bloquear o fluxo principal do programa. 
    # Cada thread executa a função self.run_schedule, que verifica periodicamente a hora atual e executa a tarefa se a hora corresponder ao agendamento.
    def schedule_tasks(self):
        for task in self.tasks:
            task_thread = threading.Thread(target=self.run_schedule, args=(task,))
            task_thread.start()

    # Responsável por verificar continuamente se é o momento de executar uma tarefa agendada
    def run_schedule(self, task):
        while True:
            current_time = time.strftime('%H:%M')
            if current_time == '11:15':
                self.execute_task(task)
            time.sleep(60)  # Verificar a cada minuto

    # Exibe a janela de notificação da tarefa quando chega a hora dela ser executada 
    def show_notification(self, task):
        notification_widget = QWidget(self, Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        notification_widget.setGeometry(100, 100, 250, 80)
        notification_widget.setStyleSheet("background-color: #EAEAEA; border: 1px solid black;")
        notification_label = QLabel(task, notification_widget)
        notification_label.setAlignment(Qt.AlignCenter)
        notification_label.setStyleSheet("font-size: 14px;")
        notification_widget.show()
        # fecha a jalela em 5 segundos
        notification_widget.closeLater = notification_widget.startTimer(5000)

    # Fechar as janelas de notificação após um determinado período de tempo
    def timerEvent(self, event):
        if event.timerId() == self.sender().closeLater:
            self.sender().killTimer(event.timerId())
            self.sender().close()

# Padrao comum em PyQt para iniciar a execução da interface gráfica.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = TaskSchedulerWidget()
    widget.show()
    widget.schedule_tasks()
    sys.exit(app.exec_())
