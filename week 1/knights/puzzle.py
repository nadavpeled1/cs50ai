from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# knights always say the truth, knaves always lie
# Basic Sentences we know:
#  1. you have to be a knight Xor Knave (only one):
#  v1 is a Knight -> V1 statement is true
#  v1 is a Knave <-> Not(V1 statement)

knowledgeBase = And(
    Or(AKnight, AKnave),  # will be Knight or Knave
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    Not(And(AKnight, AKnave)),  # cannot be knight and knave at the same time
    Not(And(BKnight, BKnave)),
    Not(And(CKnight, CKnave)),
)
# Puzzle 0
# A says "I am both a knight and a knave."
# human logic: if A would be a knight, it means he is both knight and knave ->  Impossible -> A is ling -> A is a Knave

knowledge0 = And(
    knowledgeBase,
    Implication(AKnight, And(AKnight, AKnave)),  # A Knight -> his statement is true
    Implication(AKnave, Not(And(AKnight, AKnave))),  # A Knave -> his statement is a lie
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    knowledgeBase,
    Implication(AKnight, And(AKnave, BKnave)),
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    knowledgeBase,
    # "We are the same kind."
    Implication(AKnight,
                And(Biconditional(AKnave, BKnave), Biconditional(AKnight, BKnight))),
    Implication(AKnave,
                Not(And(Biconditional(AKnave, BKnave), Biconditional(AKnight, BKnight)))),
    #  "We are of different kinds."
    Implication(BKnight, AKnave),
    Implication(BKnave, Not(AKnave))
)

# Puzzle 3

knowledge3 = And(
    knowledgeBase,
    # A says either "I am a knight." or "I am a knave.", but you don't know which.
    # if he is a knave, he should say "im a knight"
    # if he is a knight, he should say "im a knight"
    Implication(AKnight, Or(AKnight, AKnave)),
    Implication(AKnave, Not(Or(AKnight, AKnave))),

    # B says "A said 'I am a knave'."
    # Bknight -> A really said "A Knave"
    Or(
        Implication(BKnight, Or(
            Implication(AKnight, AKnave),  # AKnight -> he's statement true
            Implication(AKnave, Not(AKnave))  # AKnave -> Not(A statement)
        )
                ),
        # BKnave, A did not say "A Knave" (so we know A said "A knight")
        Implication(BKnave, Not(Or(
                    Implication(AKnight, AKnave),  # AKnight -> he's statement true
                             Implication(AKnave, Not(AKnave))  # AKnave -> Not(A statement)
                            ))
        )
    ),
    # B says "C is a knave."
    Implication(BKnight, CKnave),
    Implication(BKnave, Not(CKnave)),
    # C says "A is a knight."
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
