import urllib.parse
import random
from database.db_handler import db_singleton

def adicionar_eletroposto(nome, endereco, total_carregadores, carregadores_disponiveis, potencia_maxima_kw):
    # Cadastra um novo eletroposto no banco de dados.
    conexao = db_singleton.get_connection()
    if not conexao:
        return (False, "Erro: Falha na comunicação com o banco de dados.")
    
    try:
        conexao.execute("INSERT INTO stations (name, address, total_chargers, available_chargers, max_power_kw) VALUES (?, ?, ?, ?, ?)", (nome, endereco, total_carregadores, carregadores_disponiveis, potencia_maxima_kw))
        conexao.commit()
        return (True, "Eletroposto cadastrado com sucesso!")
    except Exception as e:
        return (False, f"Erro ao cadastrar eletroposto: {e}")

def obter_eletropostos_proximos(endereco_atual, limite=3):
    # Busca eletropostos e simula a distância até o endereço atual.
    conexao = db_singleton.get_connection()
    if not conexao: return []
    
    eletropostos = conexao.execute("SELECT * FROM stations").fetchall()
    
    resultados = []
    for ep in eletropostos:
        dicionario_ep = dict(ep)
        # Simulando uma distância aleatória entre 1km e 15km
        dicionario_ep['distancia_km'] = round(random.uniform(1.0, 15.0), 1)
        resultados.append(dicionario_ep)
    
    # Ordena da menor distância para a maior e retorna o limite (3)
    resultados.sort(key=lambda x: x['distancia_km'])
    return resultados[:limite]

def gerar_link_mapas(origem, destino):
    # Gera uma URL de rotas do Google Maps baseada na origem e destino.
    url_base = "https://www.google.com/maps/dir/?api=1"
    origem_codificada = urllib.parse.quote(origem)
    destino_codificado = urllib.parse.quote(destino)
    return f"{url_base}&origin={origem_codificada}&destination={destino_codificado}"

def obter_todos_eletropostos():
    # Retorna todos os eletropostos cadastrados.
    conexao = db_singleton.get_connection()
    if not conexao: return []
    return conexao.execute("SELECT * FROM stations").fetchall()

def atualizar_carregadores_disponiveis(id_eletroposto, carregadores_disponiveis):
    # Atualiza a quantidade de carregadores disponíveis de um eletroposto.
    conexao = db_singleton.get_connection()
    if not conexao:
        return (False, "Erro: Falha na comunicação com o banco de dados.")
    try:
        conexao.execute("UPDATE stations SET available_chargers = ? WHERE id = ?", (carregadores_disponiveis, id_eletroposto))
        conexao.commit()
        return (True, "Status de carregadores atualizado com sucesso!")
    except Exception as e:
        return (False, f"Erro ao atualizar carregadores: {e}")

def adicionar_avaliacao(id_eletroposto, nome_usuario, nota, comentario):
    # Adiciona uma avaliação a um eletroposto.
    conexao = db_singleton.get_connection()
    if not conexao:
        return (False, "Erro: Falha na comunicação com o banco de dados.")
    try:
        conexao.execute("INSERT INTO reviews (station_id, user_name, rating, comment) VALUES (?, ?, ?, ?)", (id_eletroposto, nome_usuario, nota, comentario))
        conexao.commit()
        return (True, "Avaliação enviada com sucesso!")
    except Exception as e:
        return (False, f"Erro ao enviar avaliação: {e}")

def obter_avaliacoes_eletroposto(id_eletroposto):
    # Retorna todas as avaliações de um eletroposto específico.
    conexao = db_singleton.get_connection()
    if not conexao: return []
    return conexao.execute("SELECT * FROM reviews WHERE station_id = ? ORDER BY created_at DESC", (id_eletroposto,)).fetchall()

def obter_media_avaliacoes_eletroposto(id_eletroposto):
    # Retorna a média de avaliações de um eletroposto.
    conexao = db_singleton.get_connection()
    if not conexao: return 0.0
    resultado = conexao.execute("SELECT AVG(rating) as media_notas FROM reviews WHERE station_id = ?", (id_eletroposto,)).fetchone()
    if resultado and resultado['media_notas']:
        return round(resultado['media_notas'], 1)
    return 0.0