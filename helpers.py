def load(file_name: str):
    try:
        with open(file_name, "r") as file:
            data = file.read()
            return data
    except IOError as e:
        print(f"Erro no carregamento de arquivo: {e}")

def save(file_name: str, content: str):
    try:
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(content)
    except IOError as e:
        print(f"Erro ao salvar arquivo: {e}")