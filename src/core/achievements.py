"""Achievement definitions and management"""

from typing import Dict, List, Callable
from src.database.db_manager import DatabaseManager


class Achievement:
    """Achievement definition"""
    
    def __init__(self, name: str, title: str, description: str, 
                 emoji: str, condition: Callable, reward: int = 0):
        self.name = name
        self.title = title
        self.description = description
        self.emoji = emoji
        self.condition = condition
        self.reward = reward


class AchievementManager:
    """Manages achievements and checks"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.achievements = self._define_achievements()
    
    def _define_achievements(self) -> Dict[str, Achievement]:
        """Define all achievements"""
        achievements = {
            # Conquistas Iniciais
            'first_game': Achievement('first_game', 'Debutante', 'Deu a primeira jogada', '🎮', lambda u: u['games_played'] >= 1, 100),
            'beginner': Achievement('beginner', 'Novato', 'Jogou 5 vezes', '🌱', lambda u: u['games_played'] >= 5, 50),
            'getting_started': Achievement('getting_started', 'Pegando o Jeito', 'Jogou 10 vezes', '🎯', lambda u: u['games_played'] >= 10, 100),
            
            # Conquistas de Jogos
            'casual_player': Achievement('casual_player', 'Jogador Casual', 'Jogou 25 vezes', '🎲', lambda u: u['games_played'] >= 25, 200),
            'regular': Achievement('regular', 'Frequentador', 'Jogou 50 vezes', '🎪', lambda u: u['games_played'] >= 50, 500),
            'veteran': Achievement('veteran', 'Veterano Raiz', 'Jogou 100 vezes', '🎖️', lambda u: u['games_played'] >= 100, 1000),
            'expert': Achievement('expert', 'Especialista', 'Jogou 250 vezes', '🏅', lambda u: u['games_played'] >= 250, 2500),
            'master': Achievement('master', 'Mestre do Cassino', 'Jogou 500 vezes', '👑', lambda u: u['games_played'] >= 500, 5000),
            'legend': Achievement('legend', 'Lenda Viva', 'Jogou 1000 vezes', '⭐', lambda u: u['games_played'] >= 1000, 10000),
            'god_tier': Achievement('god_tier', 'Deus do Jogo', 'Jogou 2500 vezes', '🌟', lambda u: u['games_played'] >= 2500, 25000),
            'unstoppable': Achievement('unstoppable', 'Imparável', 'Jogou 5000 vezes', '💫', lambda u: u['games_played'] >= 5000, 50000),
            
            # Conquistas de Moedas
            'first_coins': Achievement('first_coins', 'Conseguiu Grana', 'Tenha 100 moedas', '🪙', lambda u: u['coins'] >= 100, 50),
            'getting_rich': Achievement('getting_rich', 'Ficando Rico', 'Tenha 500 moedas', '💵', lambda u: u['coins'] >= 500, 100),
            'moneybags': Achievement('moneybags', 'Cheio da Grana', 'Tenha 1.000 moedas', '💰', lambda u: u['coins'] >= 1000, 200),
            'wealthy': Achievement('wealthy', 'Próspero', 'Tenha 5.000 moedas', '💎', lambda u: u['coins'] >= 5000, 500),
            'high_roller': Achievement('high_roller', 'Apostador VIP', 'Tenha 10.000 moedas', '🎰', lambda u: u['coins'] >= 10000, 1000),
            'tycoon': Achievement('tycoon', 'Magnata', 'Tenha 25.000 moedas', '🏦', lambda u: u['coins'] >= 25000, 2500),
            'millionaire': Achievement('millionaire', 'Milionário', 'Tenha 50.000 moedas', '🤑', lambda u: u['coins'] >= 50000, 5000),
            'multi_millionaire': Achievement('multi_millionaire', 'Multimilionário', 'Tenha 100.000 moedas', '💸', lambda u: u['coins'] >= 100000, 10000),
            'billionaire': Achievement('billionaire', 'Bilionário', 'Tenha 500.000 moedas', '🏰', lambda u: u['coins'] >= 500000, 50000),
            'trillionaire': Achievement('trillionaire', 'Trilionário', 'Tenha 1.000.000 moedas', '👑', lambda u: u['coins'] >= 1000000, 100000),
            
            # Conquistas de Vitórias
            'first_win': Achievement('first_win', 'Primeira Vitória', 'Ganhe seu primeiro jogo', '🎉', lambda u: u['games_won'] >= 1, 100),
            'lucky_one': Achievement('lucky_one', 'Sortudo', 'Ganhe 5 vezes', '🍀', lambda u: u['games_won'] >= 5, 100),
            'winner': Achievement('winner', 'Vencedor', 'Ganhe 10 vezes', '🏆', lambda u: u['games_won'] >= 10, 200),
            'champion': Achievement('champion', 'Campeão', 'Ganhe 25 vezes', '🥇', lambda u: u['games_won'] >= 25, 500),
            'big_winner': Achievement('big_winner', 'Grande Vencedor', 'Ganhe 50 vezes', '🎊', lambda u: u['games_won'] >= 50, 1000),
            'dominator': Achievement('dominator', 'Dominador', 'Ganhe 100 vezes', '👊', lambda u: u['games_won'] >= 100, 2000),
            'conqueror': Achievement('conqueror', 'Conquistador', 'Ganhe 250 vezes', '⚔️', lambda u: u['games_won'] >= 250, 5000),
            'destroyer': Achievement('destroyer', 'Destruidor', 'Ganhe 500 vezes', '💥', lambda u: u['games_won'] >= 500, 10000),
            
            # Conquistas de Ganhos Totais
            'small_profit': Achievement('small_profit', 'Lucrinho', 'Ganhe 1.000 moedas no total', '💵', lambda u: u['total_won'] >= 1000, 100),
            'good_profit': Achievement('good_profit', 'Bom Lucro', 'Ganhe 5.000 moedas no total', '💰', lambda u: u['total_won'] >= 5000, 250),
            'big_profit': Achievement('big_profit', 'Lucrão', 'Ganhe 10.000 moedas no total', '💎', lambda u: u['total_won'] >= 10000, 500),
            'huge_profit': Achievement('huge_profit', 'Lucro Absurdo', 'Ganhe 25.000 moedas no total', '🤑', lambda u: u['total_won'] >= 25000, 1000),
            'massive_profit': Achievement('massive_profit', 'Lucro Monstro', 'Ganhe 50.000 moedas no total', '💸', lambda u: u['total_won'] >= 50000, 2500),
            'insane_profit': Achievement('insane_profit', 'Lucro Insano', 'Ganhe 100.000 moedas no total', '🏆', lambda u: u['total_won'] >= 100000, 5000),
            
            # Conquistas de Streak (Sequência Diária)
            'consistent': Achievement('consistent', 'Consistente', '3 dias seguidos', '📅', lambda u: u['streak'] >= 3, 100),
            'dedicated': Achievement('dedicated', 'Dedicado', '5 dias seguidos', '🔥', lambda u: u['streak'] >= 5, 250),
            'lucky_streak': Achievement('lucky_streak', 'Sequência de Sorte', '7 dias seguidos', '🍀', lambda u: u['streak'] >= 7, 500),
            'committed': Achievement('committed', 'Comprometido', '10 dias seguidos', '💪', lambda u: u['streak'] >= 10, 1000),
            'persistent': Achievement('persistent', 'Persistente', '15 dias seguidos', '🎯', lambda u: u['streak'] >= 15, 1500),
            'unstoppable_streak': Achievement('unstoppable_streak', 'Imparável', '21 dias seguidos', '⚡', lambda u: u['streak'] >= 21, 2500),
            'month_streak': Achievement('month_streak', 'Mês Inteiro', '30 dias seguidos', '📆', lambda u: u['streak'] >= 30, 5000),
            'two_months': Achievement('two_months', 'Dois Meses', '60 dias seguidos', '🌟', lambda u: u['streak'] >= 60, 10000),
            'three_months': Achievement('three_months', 'Três Meses', '90 dias seguidos', '💫', lambda u: u['streak'] >= 90, 20000),
            'half_year': Achievement('half_year', 'Meio Ano', '180 dias seguidos', '👑', lambda u: u['streak'] >= 180, 50000),
            'full_year': Achievement('full_year', 'Ano Completo', '365 dias seguidos', '🏆', lambda u: u['streak'] >= 365, 100000),
            
            # Conquistas Especiais de Jogos Específicos (DESABILITADAS - precisam de tracking específico)
            # 'coinflip_fan': Achievement('coinflip_fan', 'Fã de Cara ou Coroa', 'Jogue Coinflip 50 vezes', '🪙', lambda u: True, 500),
            # 'wheel_lover': Achievement('wheel_lover', 'Viciado na Roda', 'Jogue Wheel 50 vezes', '🎡', lambda u: True, 500),
            # 'plinko_master': Achievement('plinko_master', 'Mestre do Plinko', 'Jogue Plinko 50 vezes', '🎯', lambda u: True, 500),
            # 'limbo_god': Achievement('limbo_god', 'Deus do Limbo', 'Jogue Limbo 50 vezes', '🎲', lambda u: True, 500),
            # 'scratch_addict': Achievement('scratch_addict', 'Viciado em Raspadinha', 'Jogue Scratch 50 vezes', '🎫', lambda u: True, 500),
            # 'keno_expert': Achievement('keno_expert', 'Expert em Keno', 'Jogue Keno 50 vezes', '🎱', lambda u: True, 500),
            # 'baccarat_pro': Achievement('baccarat_pro', 'Profissa do Baccarat', 'Jogue Baccarat 50 vezes', '🎴', lambda u: True, 500),
            # 'hilo_king': Achievement('hilo_king', 'Rei do Hi-Lo', 'Jogue Hi-Lo 50 vezes', '🃏', lambda u: True, 500),
            # 'tower_climber': Achievement('tower_climber', 'Escalador de Torre', 'Jogue Tower 50 vezes', '🗼', lambda u: True, 500),
            # 'poker_shark': Achievement('poker_shark', 'Tubarão do Poker', 'Jogue Video Poker 50 vezes', '🎰', lambda u: True, 500),
            
            # Conquistas de Apostas Altas (DESABILITADAS - precisam de tracking específico)
            # 'brave_bet': Achievement('brave_bet', 'Aposta Corajosa', 'Aposte 1.000 em um jogo', '🎲', lambda u: True, 500),
            # 'risky_bet': Achievement('risky_bet', 'Aposta Arriscada', 'Aposte 5.000 em um jogo', '💎', lambda u: True, 1000),
            # 'all_in': Achievement('all_in', 'All In', 'Aposte 10.000 em um jogo', '🔥', lambda u: True, 2500),
            # 'whale': Achievement('whale', 'Baleia', 'Aposte 25.000 em um jogo', '🐋', lambda u: True, 5000),
            # 'mega_whale': Achievement('mega_whale', 'Mega Baleia', 'Aposte 50.000 em um jogo', '🐳', lambda u: True, 10000),
            
            # Conquistas de Multiplicadores (DESABILITADAS - precisam de tracking específico)
            # 'double_win': Achievement('double_win', 'Dobrou', 'Ganhe com 2x', '✌️', lambda u: True, 100),
            # 'triple_win': Achievement('triple_win', 'Triplicou', 'Ganhe com 3x', '🔺', lambda u: True, 200),
            # 'big_multi': Achievement('big_multi', 'Multiplicador Grande', 'Ganhe com 10x', '🎊', lambda u: True, 500),
            # 'huge_multi': Achievement('huge_multi', 'Multi Enorme', 'Ganhe com 25x', '💥', lambda u: True, 1000),
            # 'insane_multi': Achievement('insane_multi', 'Multi Insano', 'Ganhe com 50x', '🌟', lambda u: True, 2500),
            # 'godlike_multi': Achievement('godlike_multi', 'Multi Divino', 'Ganhe com 100x+', '👑', lambda u: True, 5000),
            
            # Conquistas de Perdas (DESABILITADAS - precisam de tracking de sequências)
            # 'bad_luck': Achievement('bad_luck', 'Azar Brabo', 'Perca 5 vezes seguidas', '😅', lambda u: True, 100),
            # 'really_unlucky': Achievement('really_unlucky', 'Muito Azarado', 'Perca 10 vezes seguidas', '😬', lambda u: True, 200),
            'disaster': Achievement('disaster', 'Desastre', 'Perca 1.000 moedas no total', '💀', lambda u: u['total_lost'] >= 1000, 100),
            'bankruptcy': Achievement('bankruptcy', 'Falência', 'Perca 5.000 moedas no total', '☠️', lambda u: u['total_lost'] >= 5000, 250),
            'rock_bottom': Achievement('rock_bottom', 'No Fundo do Poço', 'Perca 10.000 moedas no total', '🕳️', lambda u: u['total_lost'] >= 10000, 500),
            
            # Conquistas Divertidas/Meme (DESABILITADAS - precisam de tracking de horário/data)
            # 'night_owl': Achievement('night_owl', 'Coruja Noturna', 'Jogue às 3h da manhã', '🦉', lambda u: True, 500),
            # 'early_bird': Achievement('early_bird', 'Madrugador', 'Jogue às 6h da manhã', '🐔', lambda u: True, 500),
            # 'workday_gambler': Achievement('workday_gambler', 'Jogando no Trampo', 'Jogue em horário comercial', '💼', lambda u: True, 300),
            # 'weekend_warrior': Achievement('weekend_warrior', 'Guerreiro de Fim de Semana', 'Jogue 10 jogos no sábado', '🎉', lambda u: True, 500),
            # 'christmas_gambler': Achievement('christmas_gambler', 'Apostador de Natal', 'Jogue no Natal', '🎄', lambda u: True, 1000),
            # 'new_year_luck': Achievement('new_year_luck', 'Sorte de Ano Novo', 'Jogue no Ano Novo', '🎆', lambda u: True, 1000),
            
            # Conquistas Sociais (DESABILITADAS - precisam de tracking de transferências)
            # 'social_player': Achievement('social_player', 'Jogador Social', 'Transfira moedas 5 vezes', '🤝', lambda u: True, 200),
            # 'generous': Achievement('generous', 'Generoso', 'Transfira 1.000 moedas', '💝', lambda u: True, 500),
            # 'philanthropist': Achievement('philanthropist', 'Filantropo', 'Transfira 5.000 moedas', '🎁', lambda u: True, 1000),
            # 'robin_hood': Achievement('robin_hood', 'Robin Hood', 'Transfira 10.000 moedas', '🏹', lambda u: True, 2500),
            
            # Conquistas de Velocidade (DESABILITADAS - precisam de tracking temporal)
            # 'speed_player': Achievement('speed_player', 'Jogador Rápido', 'Jogue 10 jogos em 1 hora', '⚡', lambda u: True, 500),
            # 'marathon': Achievement('marathon', 'Maratonista', 'Jogue 50 jogos em um dia', '🏃', lambda u: True, 2000),
            # 'ultra_marathon': Achievement('ultra_marathon', 'Ultra Maratonista', 'Jogue 100 jogos em um dia', '🏃‍♂️', lambda u: True, 5000),
            
            # Conquistas de Precisão (DESABILITADAS - precisam de tracking específico)
            # 'perfect_guess': Achievement('perfect_guess', 'Chute Perfeito', 'Acerte no primeiro try', '🎯', lambda u: True, 200),
            # 'lucky_seven': Achievement('lucky_seven', 'Sete da Sorte', 'Ganhe com número 7', '🍀', lambda u: True, 777),
            # 'jackpot_hunter': Achievement('jackpot_hunter', 'Caçador de Jackpot', 'Ganhe um jackpot', '💰', lambda u: True, 5000),
            
            # Conquistas Extremas (DESABILITADAS - precisam de lógica complexa)
            # 'never_give_up': Achievement('never_give_up', 'Nunca Desiste', 'Continue jogando com menos de 100 moedas', '💪', lambda u: True, 500),
            # 'comeback_king': Achievement('comeback_king', 'Rei da Virada', 'Volte de 0 para 10.000 moedas', '👑', lambda u: True, 5000),
            # 'phoenix': Achievement('phoenix', 'Fênix', 'Renasça das cinzas 3 vezes', '🔥', lambda u: True, 2500),
            
            # Conquistas de Colecionador (DESABILITADAS - precisam contar achievements)
            # 'collector': Achievement('collector', 'Colecionador', 'Desbloqueie 10 conquistas', '📚', lambda u: True, 500),
            # 'achievement_hunter': Achievement('achievement_hunter', 'Caçador de Conquistas', 'Desbloqueie 25 conquistas', '🏹', lambda u: True, 1000),
            # 'completionist': Achievement('completionist', 'Completista', 'Desbloqueie 50 conquistas', '💯', lambda u: True, 5000),
            # 'perfectionist': Achievement('perfectionist', 'Perfeccionista', 'Desbloqueie 75 conquistas', '⭐', lambda u: True, 10000),
            # 'god_of_achievements': Achievement('god_of_achievements', 'Deus das Conquistas', 'Desbloqueie 100 conquistas', '👑', lambda u: True, 25000),
            
            # Conquistas Secretas/Easter Eggs (DESABILITADAS - precisam de tracking específico)
            # 'secret_1': Achievement('secret_1', 'Descobridor', 'Encontrou um segredo', '🔍', lambda u: True, 1000),
            # 'secret_2': Achievement('secret_2', 'Detetive', 'Encontrou todos os segredos', '🕵️', lambda u: True, 5000),
            'lucky_number': Achievement('lucky_number', 'Número da Sorte', 'Ganhe exatamente 6.969 moedas', '😏', lambda u: u['coins'] == 6969, 6969),
            'illuminati': Achievement('illuminati', 'Illuminati Confirmado', 'Tenha exatamente 666 ou 777 moedas', '👁️', lambda u: u['coins'] in [666, 777], 1000),
            
            # 🔥 CONQUISTAS MEME 2025 🔥
            
            # Davi Brito Memes
            'davi_brito': Achievement('davi_brito', 'Davi Brito', 'Perca tudo depois de ganhar muito', '🏆', lambda u: u['total_won'] >= 10000 and u['coins'] < 100, 2024),
            'nao_sabia': Achievement('nao_sabia', 'Eu Não Sabia', 'Perca 1.000 moedas em um dia', '🤷', lambda u: u['total_lost'] >= 1000, 500),
            'campeao_sem_grana': Achievement('campeao_sem_grana', 'Campeão Sem Grana', 'Ganhe 100 jogos mas tenha menos de 500 moedas', '💸', lambda u: u['games_won'] >= 100 and u['coins'] < 500, 1000),
            
            # Brainrot / Gen Z
            'skibidi_toilet': Achievement('skibidi_toilet', 'Skibidi Toilet', 'Jogue 69 vezes', '🚽', lambda u: u['games_played'] == 69, 690),
            'rizz_god': Achievement('rizz_god', 'Rizz God', 'Ganhe 777 moedas exatas', '😎', lambda u: u['coins'] == 777, 777),
            'sigma_grindset': Achievement('sigma_grindset', 'Sigma Grindset', 'Jogue 500 vezes', '💪', lambda u: u['games_played'] >= 500, 5000),
            'alpha_male': Achievement('alpha_male', 'Alpha Male', 'Ganhe 100 jogos', '🗿', lambda u: u['games_won'] >= 100, 2000),
            'based': Achievement('based', 'Based', 'Tenha exatamente 1.337 moedas', '🧠', lambda u: u['coins'] == 1337, 1337),
            'gigachad': Achievement('gigachad', 'Gigachad', 'Ganhe 1.000 jogos', '💎', lambda u: u['games_won'] >= 1000, 10000),
            'no_cap': Achievement('no_cap', 'No Cap', 'Ganhe 50.000 moedas no total', '🧢', lambda u: u['total_won'] >= 50000, 5000),
            'its_giving': Achievement('its_giving', 'Its Giving Broke', 'Tenha menos de 10 moedas', '💀', lambda u: u['coins'] < 10, 100),
            'slay': Achievement('slay', 'Slay Queen', 'Mantenha 10 dias de streak', '👑', lambda u: u['streak'] >= 10, 1000),
            'lowkey_highkey': Achievement('lowkey_highkey', 'Lowkey Highkey Rich', 'Tenha entre 99k e 101k moedas', '💅', lambda u: 99000 <= u['coins'] <= 101000, 5000),
            
            # Memes BR 2025
            'simplesmente': Achievement('simplesmente', 'Simplesmente', 'Jogue 100 vezes', '🤙', lambda u: u['games_played'] >= 100, 1000),
            'choquei': Achievement('choquei', 'Choquei', 'Ganhe 25.000 moedas no total', '😱', lambda u: u['total_won'] >= 25000, 2500),
            'receba': Achievement('receba', 'RECEBA!', 'Ganhe 250 jogos', '🎯', lambda u: u['games_won'] >= 250, 5000),
            'se_vira': Achievement('se_vira', 'Se Vira nos 30', 'Tenha menos de 30 moedas', '🎭', lambda u: u['coins'] < 30, 300),
            'birl': Achievement('birl', 'BIRL!', 'Ganhe 1.000 jogos (bodybuilder mindset)', '💪', lambda u: u['games_won'] >= 1000, 13000),
            'suave': Achievement('suave', 'Suave na Nave', 'Mantenha streak de 7 dias', '🛸', lambda u: u['streak'] >= 7, 700),
            'calma_calabreso': Achievement('calma_calabreso', 'Calma Calabreso', 'Perca 5.000 moedas no total', '🌶️', lambda u: u['total_lost'] >= 5000, 500),
            'eitaaaa': Achievement('eitaaaa', 'Eitaaaa!', 'Tenha exatamente 420 moedas', '🌿', lambda u: u['coins'] == 420, 420),
            'paia': Achievement('paia', 'Paia Demais', 'Perca 100 jogos', '😬', lambda u: (u['games_played'] - u['games_won']) >= 100, 1000),
            
            # Números Mágicos / Memes
            'ordem_e_progresso': Achievement('ordem_e_progresso', 'Ordem e Progresso', 'Tenha exatamente 1.889 moedas', '🇧🇷', lambda u: u['coins'] == 1889, 1889),
            'bolovo': Achievement('bolovo', 'Bolovo', 'Tenha exatamente 17 moedas', '🥚', lambda u: u['coins'] == 17, 170),
            'cinquentinha': Achievement('cinquentinha', 'Cinquentinha', 'Tenha exatamente 50 moedas', '🏍️', lambda u: u['coins'] == 50, 500),
            'stonks': Achievement('stonks', 'Stonks', 'Ganhe 10.000 moedas no total', '📈', lambda u: u['total_won'] >= 10000, 1000),
            'not_stonks': Achievement('not_stonks', 'Not Stonks', 'Perca 10.000 moedas no total', '📉', lambda u: u['total_lost'] >= 10000, 1000),
            
            # Zueiras Específicas
            'zika_virus': Achievement('zika_virus', 'Zika Vírus', 'Tenha exatamente 2.016 moedas', '🦟', lambda u: u['coins'] == 2016, 2016),
            'mente_milionaria': Achievement('mente_milionaria', 'Mente Milionária', 'Perca tudo mas continue jogando', '🧠', lambda u: u['total_lost'] >= 1000 and u['games_played'] >= 50, 500),
            'vish_kk': Achievement('vish_kk', 'Vish kk', 'Tenha exatamente 88 moedas', '🍑', lambda u: u['coins'] == 88, 880),
            'caiu_na_vila': Achievement('caiu_na_vila', 'Caiu na Vila o Peixe Fuzila', 'Ganhe 500 jogos', '🐟', lambda u: u['games_won'] >= 500, 5000),
            'maizena': Achievement('maizena', 'Maizena', 'Tenha exatamente 99 moedas', '🌽', lambda u: u['coins'] == 99, 990),
            'toin': Achievement('toin', 'Toin', 'Jogue 1.000 vezes', '💰', lambda u: u['games_played'] >= 1000, 10000),
            'vapo_vapo': Achievement('vapo_vapo', 'Vapo Vapo', 'Ganhe 50 jogos', '💨', lambda u: u['games_won'] >= 50, 500),
            'apenas': Achievement('apenas', 'Apenas', 'Tenha exatamente 1 moeda', '1️⃣', lambda u: u['coins'] == 1, 100),
            
            # Referências Nerds
            'over_9000': Achievement('over_9000', 'Its Over 9000!', 'Tenha mais de 9.000 moedas', '🐉', lambda u: u['coins'] > 9000, 9001),
            'ordem_66': Achievement('ordem_66', 'Ordem 66', 'Tenha exatamente 66 moedas', '⚔️', lambda u: u['coins'] == 66, 660),
            'respawn': Achievement('respawn', 'Respawn', 'Volte a jogar depois de ficar sem moedas', '♻️', lambda u: u['games_played'] >= 10 and u['total_lost'] >= 100, 100),
            'gg_ez': Achievement('gg_ez', 'GG EZ', 'Ganhe 100 jogos', '🎮', lambda u: u['games_won'] >= 100, 1000),
            'noob': Achievement('noob', 'Noob', 'Jogue 5 vezes e não ganhe nenhuma', '🤡', lambda u: u['games_played'] >= 5 and u['games_won'] == 0, 500),
            'hacker': Achievement('hacker', 'Hacker (ou sortudo)', 'Ganhe 25 jogos com streak alto', '👨‍💻', lambda u: u['games_won'] >= 25 and u['streak'] >= 5, 2500),
            
            # Conquistas Irônicas
            'todo_dia_isso': Achievement('todo_dia_isso', 'Todo Dia Isso', 'Jogue por 30 dias seguidos', '😩', lambda u: u['streak'] >= 30, 3000),
            'paciencia': Achievement('paciencia', 'Paciência de Jó', 'Jogue 2.000 vezes', '🧘', lambda u: u['games_played'] >= 2000, 20000),
            'perdemo': Achievement('perdemo', 'Perdemo', 'Tenha 0 moedas', '☠️', lambda u: u['coins'] == 0, 1000),
            'confusion': Achievement('confusion', 'Confusion', 'Ganhe e perca 10k moedas cada', '❓', lambda u: u['total_won'] >= 10000 and u['total_lost'] >= 10000, 2000),
            'tanto_faz': Achievement('tanto_faz', 'Tanto Faz', 'Jogue 500 vezes com saldo médio', '🤷‍♂️', lambda u: u['games_played'] >= 500 and 1000 <= u['coins'] <= 10000, 5000),
        }
        return achievements
    
    def check_achievements(self, user_id: str, username: str) -> List[Achievement]:
        """Check and unlock new achievements for a user"""
        user = self.db.get_user(user_id, username)
        user_stats = dict(user)
        
        unlocked = []
        
        for achievement in self.achievements.values():
            if achievement.condition(user_stats):
                if self.db.unlock_achievement(user_id, achievement.name):
                    # Achievement just unlocked, give reward
                    if achievement.reward > 0:
                        self.db.update_coins(user_id, achievement.reward)
                        self.db.add_transaction(
                            user_id, 
                            achievement.reward, 
                            'achievement',
                            f'Conquista desbloqueada: {achievement.title}'
                        )
                    unlocked.append(achievement)
        
        return unlocked
    
    def get_achievement(self, name: str) -> Achievement:
        """Get achievement by name"""
        return self.achievements.get(name)
    
    def get_all_achievements(self) -> List[Achievement]:
        """Get all achievements"""
        return list(self.achievements.values())
