from persistente import *
from interface import WidgetInterface
from PyQt5.QtWidgets import QApplication

# Carrega tarefas do arquivo
load_task_list('task_bank.txt')

# Solicita ao usuário que insira tarefas
#get_user_tasks()

# Salva tarefas no arquivo
save_task_list('task_bank.txt')

## Bloco de chamada da interface gráfica
def startInterface():
    app = QApplication([])
    widget = WidgetInterface()
    widget.show()
    app.exec_()

if __name__ == '__main__':
    startInterface()
## Fim do bloco