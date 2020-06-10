// #[macro_use]
// extern crate rulinalg;
// use rulinalg::matrix::Matrix;

mod game;
mod moves;
mod tree_search;

use game::{Game, Status};
use moves::possible_moves;
use tree_search::const_depth_search;

fn main() {
    let mut game = Game::new();
    println!("{:?}", game);

    loop {
        let my_move = const_depth_search(&game.board, 2);
        println!("{:?}", my_move);
        game.make_move(my_move);
        println!("{:?}", game);
        if let Status::Ended = game.status {
            println!("score: {}", game.score);
            break;
        }
    }
}

// TODO

// [X] make an implementation of gridentify
//   [X] board
//   [X] move generation
//   [X] making moves
//   [X] generating random tiles
//   [X] detecting game finish

// [ ] make a tree search func
//   [X] func for generating all possible boards
//   [X] const depth tree search
//     [X] explore all boards for all moves
//   [ ] depth first exploration
//     [ ] estimate probable "goodness" of moves and add to stack
//     [ ] pop best looking move from stack and try it
//     [ ] repeat until time / computation limit reached

// [ ] optimizations
//   [ ] don't generate all possible boards
//     [ ] just pretend newly generated tiles are off-limits
//     [ ] use wildcards to reduce branching factor and allow for planning with 
//   [ ] don't look for moves of all lengths
//     [ ] max length 8?
//     [ ] 5, 7 do not not seem useful since prime

// [ ] hardcoded bot
//   [ ] static board evaluation

// [ ] make neural network
//   [ ] move eval (to explore moves)
//   [ ] static board eval

// [ ] train neural network
//   [ ] train on hardcoded bot
//   [ ] amplification & distillation
//     [ ] use more processing to get better moves
//     [ ] train on amplified network
