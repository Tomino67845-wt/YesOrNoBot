import random

RESPONSES = [
    ("Yeah", 20),
    ("YES", 15),
    ("HELL YEAH!", 10),
    ("Of course", 5),
    ("Nope", 25),
    ("Nah", 15),
    ("NAH BRO", 10),
]

def answer_question(user_input):
    if user_input.strip().endswith("?"):
        options, weights = zip(*RESPONSES)
        return random.choices(options, weights=weights, k=1)[0]
    return "That's not a question."

print("RNG Yes/No Bot is running!! (Type 'quit' to exit)\n")

while True:
    user_input = input("Ask a question: ")
    if user_input.lower() == "quit":
        break
    
    reply = answer_question(user_input)
    print(f"Bot: {reply}\n")