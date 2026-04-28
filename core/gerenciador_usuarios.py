from database.db_handler import db_singleton

def validar_dados_cadastro(nome, email, telefone, senha, confirmar_senha):
    # Valida os dados de cadastro de um novo usuário. Retorna (True, "Sucesso") ou (False, "Mensagem de Erro").
    if not nome or not email or not telefone or not senha:
        return (False, "Erro: Todos os campos são obrigatórios.")
    if "@" not in email or "." not in email or " " in email:
        return (False, "Erro: E-mail inválido!")
    if not telefone.isdigit() or len(telefone) != 11:
        return (False, "Erro: O telefone precisa de exatamente 11 dígitos numéricos.")
    if not (4 <= len(senha) <= 8):
        return (False, "Erro: A senha deve ter entre 4 a 8 caracteres.")
    if not any(caractere.isdigit() for caractere in senha):
        return (False, "Erro: A senha deve conter pelo menos um número.")
    if not any(caractere.isupper() for caractere in senha):
        return (False, "Erro: A senha deve conter pelo menos uma letra maiúscula.")
    if senha != confirmar_senha:
        return (False, "Erro: As senhas não coincidem.")
    
    # Verifica se o email já existe no banco de dados
    conexao = db_singleton.get_connection()
    if not conexao:
        return (False, "Erro: Falha na comunicação com o banco de dados.")

    usuario = conexao.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
    # A conexão não é fechada aqui.
    if usuario:
        return (False, "Erro: Email já cadastrado!")

    return (True, "Validação bem-sucedida.")

def registrar_novo_usuario(nome, email, telefone, senha):
    # Insere um novo usuário no banco de dados.
    conexao = db_singleton.get_connection()
    if not conexao:
        print("ERRO: Não foi possível registrar o usuário pois a conexão com o banco de dados falhou.")
        return

    # Define como admin se for um email específico de controle
    eh_admin = 1 if email == 'admin@voltlink.com' else 0

    conexao.execute("INSERT INTO users (name, email, phone_number, password, is_admin) VALUES (?, ?, ?, ?, ?)", (nome, email, telefone, senha, eh_admin))
    conexao.commit()
    # A conexão não é fechada aqui.

def login_usuario(email, senha):
    """Verifica as credenciais do usuário no banco de dados.
    Retorna (True, user_data_dict) em caso de sucesso,
    ou (False, error_message) em caso de falha."""
    conexao = db_singleton.get_connection()
    if not conexao:
        return (False, "Erro: Falha na comunicação com o banco de dados.")

    # Busca o usuário pelo email
    linha_usuario = conexao.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()

    if not linha_usuario:
        return (False, "Erro: Email não encontrado.")

    """AVISO: Comparação de senha em texto puro. Isto é muito inseguro para produção!
    O ideal é usar hash de senhas (ex: bcrypt), que podemos implementar a seguir."""
    if linha_usuario['password'] == senha:
        # Retorna os dados do usuário como um dicionário para facilitar o acesso
        return (True, dict(linha_usuario))
    else:
        return (False, "Erro: Senha incorreta.")