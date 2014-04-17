from random import shuffle
import time

class Deck:
	def deal(self):
		if len(self.cards) == 0: 
			self.cards = range(0, 52)
			shuffle(self.cards)
		return self.cards.pop()
	def __init__(self):
		self.cards = []

class Player:
	def get_card(self, card):
		self.hand.append(card)
	def score_hand(self):
		self.value = 0
		# Convert cards into ranks, and then reverse sort so that we decide
		# what to do with aces (zeroes) last
		cards = sorted(map(lambda x: x % 13, self.hand), reverse=True)
		for card in cards:
			if card >= 10:
				self.value += 10
			elif card == 0 and self.value > 10:
				self.value += 1
			elif card == 0 and self.value <= 10:
				self.value += 11
			else:
				self.value += card + 1
		return self.value
	def clear_hand(self):
		self.hand = []
	def render_cards(self, most_recent_only = False):
		if(most_recent_only):
			print_hand = [self.hand[-1]]
		else:
			print_hand = self.hand
		for card in print_hand:
			face = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'][card % 13]
			suit = ['C', 'S' , 'D', 'H'][card // 13]
			print face + suit
		if(not most_recent_only):	
			print "Total: {}".format(self.score_hand())
	def __init__(self):
		self.hand = []	
		
class Human(Player):
	def wager(self):
		self.bet = input("How much do you want to wager? ")
		while self.bet < 1:
			print "You need to wager at least 1 slip of gold pressed Latinum"
			self.bet = input("How much do you want to wager? ")
		while self.bet > self.pot:
			print "You don't have that much to wager "
			self.bet = input("How much do you want to wager? ")
		self.pot -= self.bet
	def win(self):
		print "You win this hand!"
		self.pot += 2 * self.bet
	def lose(self):
		print "You lost this time"
	def draw(self):
		print "Both you and the dealer got blackjack. You recover your bet"
		self.pot += self.bet
	def __init__(self):
		self.pot = 100
		self.hand = []	

def main():
	dealer = Player()
	player = Human()
	deck = Deck()
	while player.pot > 0:
		print "You have {} slips of gold pressed Latinum".format(player.pot)
		player.wager()
		dealer.get_card(deck.deal())
		print "The dealer's card: "
		dealer.render_cards()
		player.get_card(deck.deal())
		player.get_card(deck.deal())
		
		move = 1
		while move == 1:
			print "Your cards: "
			player.render_cards()
			if player.score_hand() <= 21:
				move = input("Do you want to hit(1) or stand(0)? ")
				if move == 1:
					player.get_card(deck.deal())
			else:
				time.sleep(1)
				move = 0
		
		print "Dealer's turn"
		dealer.render_cards(most_recent_only=True)
		time.sleep(1.5)
		while dealer.score_hand() < 17:
			dealer.get_card(deck.deal())
			dealer.render_cards(most_recent_only=True)
			time.sleep(1.5)
		
		print "Your hand: "
		player.render_cards()
		print "You have a score of {}, while the dealer has {}".format(player.value, dealer.value)
		
		if dealer.value == 21 and player.value == 21:
			player.draw()
		elif dealer.value <= 21 and dealer.value >= player.value:
			player.lose()
		elif player.value > 21:
			print "You bust!"
			player.lose()
		else:
			player.win()
		player.clear_hand()
		dealer.clear_hand()
	print "You're out of Latinum! See you next time!"
			
if __name__ == "__main__":
    main()

		
		
		
		
		
		
		
		
		
		