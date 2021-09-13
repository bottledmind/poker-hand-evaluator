# Poker Hand Strength Evaluator

### Poker Games

Supported poker games:
* Texas Hold'em - input is a board of 5 cards, and multiple hands of 2 cards each.

  A value of a Texas Hold'em hand is the best possible value out of all possible subsets of
  5 cards from the 7 cards which are formed by 5 board cards and 2 hand cards.

  See [Texas Hold'em rules](https://en.wikipedia.org/wiki/Texas_hold_%27em).

* Omaha Hold'em - input is a board of 5 cards, and multiple hands of 4 cards each.

  A value of an Omaha Hold'em hand is the best possible value out of all possible 5 card combinations
  which are formed from 3 out of 5 board cards and 2 out of 4 hand cards.

  See [Omaha Hold'em rules](https://en.wikipedia.org/wiki/Omaha_hold_%27em).

* Five Card Draw - input is multiple hands of 5 cards each.

  A value of a Five Card Draw hand is the value of the 5 hand cards.

  See [Five Card Draw rules](https://en.wikipedia.org/wiki/Five-card_draw).


## Implementation

### Input

The input is read as a string:

```
<game-type> [<5 board cards>] <hand 1> <hand 2> <...> <hand N>
```

...where:

* `game-type` specifies the game type for this test case, one of:
  * `texas-holdem` - for Texas Hold'em
  * `omaha-holdem` - for Omaha Hold'em
  * `five-card-draw` - for Five Card Draw

* `<5 board cards>` is a 10 character string where each 2 characters encode a card, only used for Texas and
  Omaha Hold' ems

* `<hand X>` is a 4, 8 or 10 character string (depending on game type) where each 2 characters encode a card
* `<card>` is a 2 character string with the first character representing the rank
  (one of `A`, `K`, `Q`, `J`, `T`, `9`, `8`, `7`, `6`, `5`, `4`, `3`, `2`) and the second character representing
  the suit (one of `h`, `d`, `c`, `s`). Jokers are not used.

### Output

The output is returned as a string:

```
<hand block 1> <hand block 2> <...> <hand block n>
```
... where:

* `<hand block 1>` is the hand block with the weakest value
* `<hand block 2>` is the hand block with the second weakest value
* ... and so forth.
* `<hand block n>` is the hand block with the strongest value

Each hand block consists of one or multiple hands (each represented by 4, 8 or 10 character string, depending
on game type, with 2 characters to encode a card) with equal hand value.

In case there are multiple hands with the same value on the same board they should are ordered alphabetically
and separated by `=` signs.

The order of the cards in each hand should remains the same as in the input, e.g., `2h3s` isn't reordered into
`3s2h`.

#### Examples

Example input:
```
texas-holdem 4cKs4h8s7s Ad4s Ac4d As9s KhKd 5d6d
texas-holdem 2h3h4h5d8d KdKs 9hJh
omaha-holdem 3d3s4d6hJc Js2dKd8c KsAsTcTs Jh2h3c9c Qc8dAd6c 7dQsAc5d
five-card-draw 7h4s4h8c9h Tc5h6dAc5c Kd9sAs3cQs Ah9d6s2cKh 4c8h2h6c9c
```

Example output:
```
Ac4d=Ad4s 5d6d As9s KhKd
KdKs 9hJh
Qc8dAd6c KsAsTcTs Js2dKd8c 7dQsAc5d Jh2h3c9c
4c8h2h6c9c Ah9d6s2cKh Kd9sAs3cQs 7h4s4h8c9h Tc5h6dAc5c
```
## Limitations
Currently there's no input validation