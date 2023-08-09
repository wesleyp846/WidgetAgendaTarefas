task_list = []

# Função para ler tarefas do arquivo, se existir
def load_task_list(file_name):
    try:
        with open(file_name, 'r') as file:
            for line in file:
                task_list.append(line.strip())
        print("Tarefas carregadas com sucesso.")
    except FileNotFoundError:
        print("Arquivo de tarefas não encontrado.")

# Função para solicitar ao usuário que insira tarefas
def get_user_tasks():
    while True:
        task = input("Digite uma tarefa (ou 's' para sair): ")
        if task.lower() == 's':
            break
        task_list.append(task)

# Função para salvar as tarefas no arquivo
def save_task_list(file_name):
    with open(file_name, 'w') as file:
        for task in task_list:
            file.write(task + '\n')
    print("Tarefas salvas com sucesso.")