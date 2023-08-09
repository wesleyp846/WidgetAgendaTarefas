import sys
import time
import threading
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QListWidget, QTimeEdit
from PyQt5.QtCore import Qt, QTimer, QTime

class TaskSchedulerWidget(QWidget):
    def __init__(self):
        super().__init__()
        # Define um título para o Widget    
        self.setWindowTitle('Tarefas')
        #self.setWindowFlags(Qt.Tool)
        # Atributo que o deixa transparente na tela
        #self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(1600, 40, 300, 400)

        #Carregamento das tarefas agendadas
        self.load_tasks_from_file()

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
        #Adição da hora marcada
        self.time_entry = QTimeEdit(self)
        layout.addWidget(self.time_entry)
        

        ## Bloco de botão de adicinar tarefa
        self.add_button = QPushButton("Adicionar Tarefa", self)
        self.add_button.clicked.connect(self.add_task)
        layout.addWidget(self.add_button)

        self.setLayout(layout)
        
        ## Termino dos blocos
        self.tasks = [self.tasks]
        self.task_thread = None

        #atualiza o relógio a cada 1000 milesegundo (1 segundo)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    ## Blocos de funcionalidades

    #carregamento das tarefas anteriores
    def load_tasks_from_file(self):
        try:
            with open('tasks.txt', 'r') as file:
                for line in file:
                    self.taskss.append(line.strip())
        except FileNotFoundError:
            pass  # Arquivo não existe ainda, pode ser a primeira execução

    #função de salvamento das tarefas ao fechar
    def closeEvent(self, event):
        self.save_tasks_to_file()
        super().closeEvent(event)

    def save_tasks_to_file(self):
        with open('tasks.txt', 'w') as file:
            for task in self.tasks:
                file.write(task + '\n')

    # Função que cria o relógio
    def update_time(self):
        current_time = QTime.currentTime()
        formatted_time = current_time.toString("HH:mm:ss")
        self.label.setText("Hora atual: " + formatted_time)

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

    # Função de exibir a notificação quando ha tarefa ativa
    def execute_task(self, full_task):
        # Separar a hora da tarefa
        task = full_task.split(" - ")[1]  
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
        # Obter a hora da tarefa
        target_time = task.split(" - ")[0]  
        while True:
            current_time = time.strftime('%H:%M')
            if current_time == target_time:
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
