from database.db_handler import db_singleton

def adicionar_cartao(id_usuario, tipo_metodo, nome_cartao, numero_cartao, validade_cartao, cvv):
    # Valida e salva um novo cartão no banco de dados.
    if not nome_cartao:
        return (False, "Erro: O nome não pode estar vazio.")
    if len(numero_cartao) != 16 or not numero_cartao.isdigit():
        return (False, "Erro: Cartão inválido! Digite os 16 números.")
    if "/" not in validade_cartao or len(validade_cartao) != 5:
        return (False, "Erro: Formato de validade inválido (use MM/AA).")
    if len(cvv) != 3 or not cvv.isdigit():
        return (False, "Erro: CVV inválido!")

    conexao = db_singleton.get_connection()
    if not conexao: return (False, "Erro de banco de dados.")

    # Por segurança, guardamos apenas os 4 últimos dígitos do cartão
    numero_mascarado = "**** **** **** " + numero_cartao[-4:]

    try:
        conexao.execute("INSERT INTO payment_methods (user_id, method_type, card_name, card_number, card_expiry) VALUES (?, ?, ?, ?, ?)",
                     (id_usuario, tipo_metodo, nome_cartao, numero_mascarado, validade_cartao))
        conexao.commit()
        return (True, f"Cartão de {tipo_metodo} cadastrado com sucesso!")
    except Exception as e:
        return (False, f"Erro ao salvar cartão: {e}")

def obter_metodos_pagamento(id_usuario):
    """Retorna todas as formas de pagamento de um usuário."""
    conexao = db_singleton.get_connection()
    if not conexao: return []
    return conexao.execute("SELECT * FROM payment_methods WHERE user_id = ?", (id_usuario,)).fetchall()

def remover_metodo_pagamento(id_usuario, id_metodo):
    """Remove uma forma de pagamento."""
    conexao = db_singleton.get_connection()
    try:
        conexao.execute("DELETE FROM payment_methods WHERE id = ? AND user_id = ?", (id_metodo, id_usuario))
        conexao.commit()
        return (True, "Forma de pagamento removida com sucesso!")
    except Exception as e:
        return (False, f"Erro ao remover: {e}")

def atualizar_cartao(id_usuario, id_metodo, nome_cartao, numero_cartao, validade_cartao, cvv):
    """Edita os dados de um cartão cadastrado."""
    if not nome_cartao:
        return (False, "Erro: O nome não pode estar vazio.")
    if len(numero_cartao) != 16 or not numero_cartao.isdigit():
        return (False, "Erro: Cartão inválido! Digite os 16 números.")
    if "/" not in validade_cartao or len(validade_cartao) != 5:
        return (False, "Erro: Formato de validade inválido (use MM/AA).")
    if len(cvv) != 3 or not cvv.isdigit():
        return (False, "Erro: CVV inválido!")

    conexao = db_singleton.get_connection()
    numero_mascarado = "**** **** **** " + numero_cartao[-4:]
    try:
        conexao.execute("UPDATE payment_methods SET card_name = ?, card_number = ?, card_expiry = ? WHERE id = ? AND user_id = ?", (nome_cartao, numero_mascarado, validade_cartao, id_metodo, id_usuario))
        conexao.commit()
        return (True, "Cartão atualizado com sucesso!")
    except Exception as e:
        return (False, f"Erro ao atualizar: {e}")