"""Gerenciador de banco de dados para operações SQLite"""

import sqlite3
import os
from datetime import datetime
from typing import Optional, List, Tuple


class GerenciadorBancoDados:
    """Gerencia todas as operações de banco de dados para o bot"""
    
    def __init__(self, caminho_bd='data/macacolandia.db'):
        """Inicializa o gerenciador de banco de dados"""
        self.caminho_bd = caminho_bd
        os.makedirs(os.path.dirname(self.caminho_bd), exist_ok=True)
        self.inicializar_banco_dados()
    
    def obter_conexao(self):
        """Obtém conexão com o banco de dados"""
        conexao = sqlite3.connect(self.caminho_bd)
        conexao.row_factory = sqlite3.Row
        return conexao
    
    def inicializar_banco_dados(self):
        """Inicializa as tabelas do banco de dados"""
        conexao = self.obter_conexao()
        cursor = conexao.cursor()
        
        # Tabela de usuários
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                coins INTEGER DEFAULT 1000,
                total_won INTEGER DEFAULT 0,
                total_lost INTEGER DEFAULT 0,
                games_played INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_daily TIMESTAMP,
                streak INTEGER DEFAULT 0
            )
        ''')
        
        # Tabela de transações
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                amount INTEGER NOT NULL,
                transaction_type TEXT NOT NULL,
                description TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Tabela de histórico de jogos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                game_type TEXT NOT NULL,
                bet_amount INTEGER NOT NULL,
                result TEXT NOT NULL,
                winnings INTEGER NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Tabela de conquistas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                achievement_name TEXT NOT NULL,
                unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                UNIQUE(user_id, achievement_name)
            )
        ''')
        
        conexao.commit()
        conexao.close()
    
    # Operações de usuário
    def obter_usuario(self, id_usuario: str, nome_usuario: str = None) -> sqlite3.Row:
        """Obtém ou cria um usuário"""
        conexao = self.obter_conexao()
        cursor = conexao.cursor()
        
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (id_usuario,))
        usuario = cursor.fetchone()
        
        if not usuario:
            cursor.execute('''
                INSERT INTO users (user_id, username, coins)
                VALUES (?, ?, 1000)
            ''', (id_usuario, nome_usuario or 'Unknown'))
            conexao.commit()
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (id_usuario,))
            usuario = cursor.fetchone()
        
        conexao.close()
        return usuario
    
    def atualizar_moedas(self, id_usuario: str, quantia: int) -> bool:
        """Atualiza moedas do usuário (pode ser negativo para dedução)"""
        conexao = self.obter_conexao()
        cursor = conexao.cursor()
        
        cursor.execute('SELECT coins FROM users WHERE user_id = ?', (id_usuario,))
        usuario = cursor.fetchone()
        
        if not usuario:
            conexao.close()
            return False
        
        novo_saldo = usuario['coins'] + quantia
        if novo_saldo < 0:
            conexao.close()
            return False
        
        cursor.execute('UPDATE users SET coins = ? WHERE user_id = ?', (novo_saldo, id_usuario))
        conexao.commit()
        conexao.close()
        return True
    
    def transferir_moedas(self, usuario_origem: str, usuario_destino: str, quantia: int) -> Tuple[bool, str]:
        """Transfere moedas entre usuários"""
        if quantia <= 0:
            return False, "Quantidade inválida!"
        
        conexao = self.obter_conexao()
        cursor = conexao.cursor()
        
        # Verifica saldo do remetente
        cursor.execute('SELECT coins FROM users WHERE user_id = ?', (usuario_origem,))
        remetente = cursor.fetchone()
        
        if not remetente or remetente['coins'] < quantia:
            conexao.close()
            return False, "Saldo insuficiente!"
        
        # Atualiza ambos os usuários
        cursor.execute('UPDATE users SET coins = coins - ? WHERE user_id = ?', (quantia, usuario_origem))
        cursor.execute('UPDATE users SET coins = coins + ? WHERE user_id = ?', (quantia, usuario_destino))
        
        # Registra transações
        cursor.execute('''
            INSERT INTO transactions (user_id, amount, transaction_type, description)
            VALUES (?, ?, 'transfer_out', ?)
        ''', (usuario_origem, -quantia, f'Transferência para {usuario_destino}'))
        
        cursor.execute('''
            INSERT INTO transactions (user_id, amount, transaction_type, description)
            VALUES (?, ?, 'transfer_in', ?)
        ''', (usuario_destino, quantia, f'Transferência de {usuario_origem}'))
        
        conexao.commit()
        conexao.close()
        return True, "Transferência realizada com sucesso!"
    
    def adicionar_transacao(self, id_usuario: str, quantia: int, tipo_transacao: str, descricao: str = None):
        """Adiciona um registro de transação"""
        conexao = self.obter_conexao()
        cursor = conexao.cursor()
        
        cursor.execute('''
            INSERT INTO transactions (user_id, amount, transaction_type, description)
            VALUES (?, ?, ?, ?)
        ''', (id_usuario, quantia, tipo_transacao, descricao))
        
        conexao.commit()
        conexao.close()
    
    def obter_historico_transacoes(self, id_usuario: str, limite: int = 10) -> List[sqlite3.Row]:
        """Obtém histórico de transações do usuário"""
        conexao = self.obter_conexao()
        cursor = conexao.cursor()
        
        cursor.execute('''
            SELECT * FROM transactions
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (id_usuario, limite))
        
        transacoes = cursor.fetchall()
        conexao.close()
        return transacoes
    
    # Operações de jogo
    def registrar_jogo(self, id_usuario: str, tipo_jogo: str, valor_aposta: int, 
                      resultado: str, ganhos: int):
        """Registra um resultado de jogo"""
        conexao = self.obter_conexao()
        cursor = conexao.cursor()
        
        # Registra histórico de jogo
        cursor.execute('''
            INSERT INTO game_history (user_id, game_type, bet_amount, result, winnings)
            VALUES (?, ?, ?, ?, ?)
        ''', (id_usuario, tipo_jogo, valor_aposta, resultado, ganhos))
        
        # Atualiza estatísticas do usuário
        cursor.execute('''
            UPDATE users 
            SET games_played = games_played + 1,
                total_won = total_won + ?,
                total_lost = total_lost + ?
            WHERE user_id = ?
        ''', (max(0, ganhos), max(0, -ganhos), id_usuario))
        
        conexao.commit()
        conexao.close()
    
    def obter_historico_jogos(self, id_usuario: str, limite: int = 10) -> List[sqlite3.Row]:
        """Obtém histórico de jogos do usuário"""
        conexao = self.obter_conexao()
        cursor = conexao.cursor()
        
        cursor.execute('''
            SELECT * FROM game_history
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (id_usuario, limite))
        
        jogos = cursor.fetchall()
        conexao.close()
        return jogos
    
    def obter_ranking(self, limite: int = 10) -> List[sqlite3.Row]:
        """Obtém os principais usuários por moedas"""
        conexao = self.obter_conexao()
        cursor = conexao.cursor()
        
        cursor.execute('''
            SELECT user_id, username, coins, games_played, total_won, total_lost
            FROM users
            ORDER BY coins DESC
            LIMIT ?
        ''', (limite,))
        
        lideres = cursor.fetchall()
        conexao.close()
        return lideres
    
    # Operações de conquistas
    def desbloquear_conquista(self, id_usuario: str, nome_conquista: str) -> bool:
        """Desbloqueia uma conquista para um usuário"""
        conexao = self.obter_conexao()
        cursor = conexao.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO achievements (user_id, achievement_name)
                VALUES (?, ?)
            ''', (id_usuario, nome_conquista))
            conexao.commit()
            conexao.close()
            return True
        except sqlite3.IntegrityError:
            # Conquista já desbloqueada
            conexao.close()
            return False
    
    def obter_conquistas_usuario(self, id_usuario: str) -> List[sqlite3.Row]:
        """Obtém todas as conquistas de um usuário"""
        conexao = self.obter_conexao()
        cursor = conexao.cursor()
        
        cursor.execute('''
            SELECT achievement_name, unlocked_at
            FROM achievements
            WHERE user_id = ?
            ORDER BY unlocked_at DESC
        ''', (id_usuario,))
        
        conquistas = cursor.fetchall()
        conexao.close()
        return conquistas
    
    # Operações de recompensa diária
    def reivindicar_recompensa_diaria(self, id_usuario: str) -> Tuple[bool, int, int]:
        """
        Reivindica recompensa diária
        Retorna: (sucesso, moedas_ganhas, sequencia_atual)
        """
        conexao = self.obter_conexao()
        cursor = conexao.cursor()
        
        cursor.execute('SELECT last_daily, streak, coins FROM users WHERE user_id = ?', (id_usuario,))
        usuario = cursor.fetchone()
        
        if not usuario:
            conexao.close()
            return False, 0, 0
        
        agora = datetime.now()
        ultimo_diario = usuario['last_daily']
        
        # Verifica se já reivindicou hoje
        if ultimo_diario:
            ultimo_diario_dt = datetime.fromisoformat(ultimo_diario)
            if (agora - ultimo_diario_dt).days < 1:
                conexao.close()
                return False, 0, usuario['streak']
        
        # Calcula sequência
        sequencia = usuario['streak']
        if ultimo_diario:
            ultimo_diario_dt = datetime.fromisoformat(ultimo_diario)
            if (agora - ultimo_diario_dt).days == 1:
                sequencia += 1
            else:
                sequencia = 1
        else:
            sequencia = 1
        
        # Calcula recompensa (base + bônus de sequência)
        recompensa_base = 100
        bonus_sequencia = min(sequencia * 10, 200)  # Máximo 200 de bônus
        recompensa_total = recompensa_base + bonus_sequencia
        
        # Atualiza usuário
        cursor.execute('''
            UPDATE users
            SET last_daily = ?,
                streak = ?,
                coins = coins + ?
            WHERE user_id = ?
        ''', (agora.isoformat(), sequencia, recompensa_total, id_usuario))
        
        # Registra transação
        cursor.execute('''
            INSERT INTO transactions (user_id, amount, transaction_type, description)
            VALUES (?, ?, 'daily_reward', ?)
        ''', (id_usuario, recompensa_total, f'Recompensa diária (sequência: {sequencia})'))
        
        conexao.commit()
        conexao.close()
        
        return True, recompensa_total, sequencia
