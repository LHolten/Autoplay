use std::collections::HashSet;
use crate::messages::GameMessage;
use crate::card::*;
use crate::action::*;

pub struct Game {
    pub my_hand: HashSet<Card>,
    pub deck_size: u32,
    pub center: Vec<Card>,
    pub unseen_cards: HashSet<Card>,
    pub players: Vec<PlayerInfo>,
    pub current_player_index: usize,
    pub has_moves: bool
}

impl Game {
    pub fn new() -> Game {
        Game {
            my_hand: HashSet::new(),
            deck_size: 56,
            center: Vec::new(),
            unseen_cards: HashSet::new(),
            players: Vec::new(),
            current_player_index: 0,
            has_moves: true,
        }
    }

    pub fn start(&mut self, players: Vec<String>) {
        self.players = players.iter().enumerate().map(
            |(i, name)| PlayerInfo {
                name: name.to_string(),
                index: i,
                hand_size: 2,
                known_hand: HashSet::new()
            }).collect();
        self.unseen_cards = Game::get_start_deck()
        // we don't have to deal with deck size, etc. because that will be updated in update()
    }

    pub fn update(&mut self, message: GameMessage) {
        // this will be set but will not be directly used in Game
        // the bot will set game.players[bot.index] = game.my_hand
        self.my_hand = message.hand.iter().map(|card| Card::from(card.to_string())).collect();

        // parse game state
        let game_state = message.game_state;
        self.has_moves = game_state.has_moves;
        self.deck_size = game_state.deck_size;
        self.current_player_index = game_state.current_player;

        // let current_player = &game_state.players[self.current_player_index];
        let previous_player_index = (self.current_player_index + self.players.len() - 1) % self.players.len();
        let previous_player = &game_state.players[previous_player_index];
        self.players[previous_player_index].hand_size = previous_player.hand_size;

        // use previous action to update known cards
        if let Some(previous_action) = &previous_player.last_action {
            println!("{0} played: {1:?}", previous_player.name, previous_action);
            let action_taken = Action::from(previous_action);
            action_taken.update_info(self, previous_player_index);

        } else {
            println!("{} played: no previous action", previous_player.name);
        }

        println!("---");

        // print centre and deck
        let center = &game_state.center;
        println!("center: {:?}", center);
        let deck_size = game_state.deck_size;
        println!("deck size: {}", deck_size);
    }

    fn get_start_deck() -> HashSet<Card> {
        let mut start_deck: HashSet<Card> = HashSet::new();
        for &suit in [Suit::Club, Suit::Heart, Suit::Spade, Suit::Diamond].iter() {
            start_deck.extend((2..15).map(|value| Card::SuitCard {suit, value}).collect::<HashSet<Card>>());
        }
        start_deck.extend((1..5).map(|id| Card::Joker {id}));
        start_deck
    }
}

pub struct PlayerInfo {
    pub name: String,
    pub index: usize,
    pub hand_size: u32,
    pub known_hand: HashSet<Card>
}