import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)

lemmatizer = WordNetLemmatizer()

def preprocess(text):
    tokens = word_tokenize(text.lower())
    return [lemmatizer.lemmatize(t) for t in tokens]

def get_intent(lemmas):
    if any(w in lemmas for w in ['search', 'buy', 'find', 'need']):
        return 'search_items'
    elif any(w in lemmas for w in ['view', 'cart', 'basket']):
        return 'view_cart'
    elif any(w in lemmas for w in ['remove', 'delete']):
        return 'remove_item'
    elif any(w in lemmas for w in ['checkout', 'place', 'order']):
        return 'checkout'
    elif any(w in lemmas for w in ['help', 'support']):
        return 'support'
    elif any(w in lemmas for w in ['exit', 'quit', 'bye']):
        return 'exit'
    return 'unknown'

# Simulated inventory and cart
inventory = {
    "milk": 50,
    "bread": 40,
    "eggs": 60,
    "rice": 80,
    "oil": 100
}
cart = {}

def blinkit_chatbot():
    print("🛍️ Welcome to Blinkit AI Chatbot!")
    print("Say things like 'I want to buy milk', 'view my cart', or 'place order'.")

    while True:
        user_input = input("\nYou: ")
        lemmas = preprocess(user_input)
        intent = get_intent(lemmas)

        if intent == 'search_items':
            print("🧾 Available items:")
            for item, price in inventory.items():
                print(f"- {item.title()} - ₹{price}")
            selected = input("Type item name to add to cart: ").lower()
            if selected in inventory:
                qty = int(input(f"How many {selected}? "))
                cart[selected] = cart.get(selected, 0) + qty
                print(f"✅ {qty} {selected}(s) added to cart.")
            else:
                print("❌ Item not found.")

        elif intent == 'view_cart':
            if cart:
                print("🛒 Your cart:")
                total = 0
                for item, qty in cart.items():
                    price = inventory[item] * qty
                    print(f"- {item.title()} x{qty} = ₹{price}")
                    total += price
                print(f"💰 Total: ₹{total}")
            else:
                print("🪹 Your cart is empty.")

        elif intent == 'remove_item':
            if cart:
                print("🗑️ Items in cart:")
                for item in cart:
                    print(f"- {item}")
                remove = input("Enter item name to remove: ").lower()
                if remove in cart:
                    del cart[remove]
                    print(f"❌ Removed {remove} from cart.")
                else:
                    print("❌ Item not found in cart.")
            else:
                print("🪹 Cart is already empty.")

        elif intent == 'checkout':
            if cart:
                print("🧾 Placing your order...")
                cart.clear()
                print("🎉 Order placed! Delivery within 15 minutes.")
            else:
                print("❗Cart is empty. Add items before checkout.")

        elif intent == 'support':
            print("☎️ Connecting to customer support...")

        elif intent == 'exit':
            print("👋 Thanks for using Blinkit Chatbot. Happy shopping!")
            break

        else:
            print("🤖 Sorry, I didn't get that. Try saying 'buy rice' or 'view cart'.")

# Run it
if __name__ == "__main__":
    blinkit_chatbot()
