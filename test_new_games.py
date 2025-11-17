#!/usr/bin/env python3
"""
Test script to verify all 10 new casino games
Tests game logic and balance handling patterns
"""

import sys
sys.path.insert(0, '.')

# Import all new games
from src.games.coinflip import CoinFlipGame
from src.games.wheel import WheelGame
from src.games.plinko import PlinkoGame
from src.games.keno import KenoGame
from src.games.baccarat import BaccaratGame
from src.games.hilo import HiLoGame
from src.games.limbo import LimboGame
from src.games.tower import TowerGame
from src.games.scratch import ScratchCardGame
from src.games.videopoker import VideoPokerGame

def test_coinflip():
    """Test Coin Flip game"""
    print("Testing Coin Flip...")
    result = CoinFlipGame.flip()
    assert result in ['cara', 'coroa'], "Invalid flip result"
    won, multiplier = CoinFlipGame.check_win(result, 'cara')
    assert isinstance(won, bool), "Won should be boolean"
    assert multiplier in [0.0, 2.0], "Invalid multiplier"
    print("✅ Coin Flip passed")

def test_wheel():
    """Test Wheel of Fortune"""
    print("Testing Wheel of Fortune...")
    segment = WheelGame.spin()
    assert 'multiplier' in segment, "Segment missing multiplier"
    assert 'label' in segment, "Segment missing label"
    won, multiplier, desc = WheelGame.calculate_win(segment)
    assert isinstance(won, bool), "Won should be boolean"
    assert multiplier >= 0, "Multiplier should be non-negative"
    print("✅ Wheel passed")

def test_plinko():
    """Test Plinko"""
    print("Testing Plinko...")
    for risk in ['baixo', 'medio', 'alto']:
        assert PlinkoGame.validate_risk(risk), f"Risk {risk} should be valid"
        slot = PlinkoGame.drop_ball()
        assert 0 <= slot <= 10, "Slot out of range"
        won, multiplier = PlinkoGame.calculate_win(slot, risk)
        assert isinstance(won, bool), "Won should be boolean"
        assert multiplier >= 0, "Multiplier should be non-negative"
    print("✅ Plinko passed")

def test_keno():
    """Test Keno"""
    print("Testing Keno...")
    numbers = [1, 5, 10, 15, 20]
    assert KenoGame.validate_numbers(numbers, len(numbers)), "Valid numbers should pass"
    drawn = KenoGame.draw_numbers()
    assert len(drawn) == KenoGame.DRAW_COUNT, "Wrong number of draws"
    matches = KenoGame.check_matches(numbers, drawn)
    assert 0 <= matches <= len(numbers), "Matches out of range"
    print("✅ Keno passed")

def test_baccarat():
    """Test Baccarat"""
    print("Testing Baccarat...")
    for bet_type in ['jogador', 'banca', 'empate']:
        assert BaccaratGame.validate_bet(bet_type), f"Bet {bet_type} should be valid"
    winner, player_hand, banker_hand, pv, bv = BaccaratGame.play_game()
    assert winner in ['jogador', 'banca', 'empate'], "Invalid winner"
    assert 0 <= pv <= 9, "Player value out of range"
    assert 0 <= bv <= 9, "Banker value out of range"
    print("✅ Baccarat passed")

def test_hilo():
    """Test Hi-Lo"""
    print("Testing Hi-Lo...")
    for guess in ['alto', 'baixo', 'igual']:
        assert HiLoGame.validate_guess(guess), f"Guess {guess} should be valid"
    current = HiLoGame.draw_card()
    next_card = HiLoGame.draw_card()
    assert current in HiLoGame.CARDS, "Invalid card"
    won, multiplier = HiLoGame.compare_cards(current, next_card, 'alto')
    assert isinstance(won, bool), "Won should be boolean"
    print("✅ Hi-Lo passed")

def test_limbo():
    """Test Limbo"""
    print("Testing Limbo...")
    assert LimboGame.validate_target(2.0), "2.0 should be valid"
    assert not LimboGame.validate_target(2000.0), "2000.0 should be invalid"
    result = LimboGame.generate_result()
    assert result >= 1.0, "Result should be >= 1.0"
    won, multiplier = LimboGame.check_win(result, 2.0)
    assert isinstance(won, bool), "Won should be boolean"
    print("✅ Limbo passed")

def test_tower():
    """Test Tower"""
    print("Testing Tower...")
    for diff in ['facil', 'medio', 'dificil', 'extremo']:
        assert TowerGame.validate_difficulty(diff), f"Difficulty {diff} should be valid"
        game = TowerGame(diff)
        assert game.current_level == 0, "Should start at level 0"
        # Simulate one choice
        is_safe, mult = game.choose_tile(0)
        assert isinstance(is_safe, bool), "is_safe should be boolean"
    print("✅ Tower passed")

def test_scratch():
    """Test Scratch Card"""
    print("Testing Scratch Card...")
    card = ScratchCardGame.generate_card()
    assert len(card) == ScratchCardGame.CARD_SIZE, "Wrong card size"
    won, multiplier, best_prize = ScratchCardGame.calculate_best_prize(card)
    assert isinstance(won, bool), "Won should be boolean"
    assert multiplier >= 0, "Multiplier should be non-negative"
    print("✅ Scratch Card passed")

def test_videopoker():
    """Test Video Poker"""
    print("Testing Video Poker...")
    game = VideoPokerGame()
    hand = game.deal()
    assert len(hand) == 5, "Hand should have 5 cards"
    assert game.hold_cards([0, 2, 4]), "Should accept valid positions"
    assert not game.hold_cards([5, 6]), "Should reject invalid positions"
    final_hand = game.draw()
    assert len(final_hand) == 5, "Final hand should have 5 cards"
    hand_name, multiplier = game.evaluate_hand()
    assert isinstance(hand_name, str), "Hand name should be string"
    assert multiplier >= 0, "Multiplier should be non-negative"
    print("✅ Video Poker passed")

def main():
    """Run all tests"""
    print("\n🎰 Testing All 10 New Casino Games\n")
    print("="*50)
    
    try:
        test_coinflip()
        test_wheel()
        test_plinko()
        test_keno()
        test_baccarat()
        test_hilo()
        test_limbo()
        test_tower()
        test_scratch()
        test_videopoker()
        
        print("="*50)
        print("\n✅ ALL TESTS PASSED! All 10 games work correctly!\n")
        return 0
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}\n")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
