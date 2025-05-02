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
    if any(w in lemmas for w in ['search', 'bus', 'book', 'find']):
        return 'book_ticket'
    elif any(w in lemmas for w in ['cancel','delete', 'remove']):
        return 'cancel_ticket'
    elif any(w in lemmas for w in ['view', 'ticket', 'status', 'booking']):
        return 'view_ticket'
    elif any(w in lemmas for w in ['help', 'support']):
        return 'support'
    elif any(w in lemmas for w in ['exit', 'quit', 'bye']):
        return 'exit'
    return 'unknown'

# Simulated ticket store
ticket = {}

def redbus_chatbot():
    print("🧠 Welcome to RedBus AI Chatbot!")
    print("Say something like 'book a bus', 'view my booking', 'cancel ticket', or 'exit'.")

    while True:
        user_input = input("\nYou: ")
        lemmas = preprocess(user_input)
        intent = get_intent(lemmas)

        if intent == 'book_ticket':
            source = input("🚌 Source city: ")
            dest = input("🏁 Destination city: ")
            date = input("📅 Travel date (YYYY-MM-DD): ")
            buses = ["Red Travels - 8 AM - ₹500", "Blue Bus - 10 AM - ₹550", "GreenLine - 6 PM - ₹600"]
            print(f"\n🔍 Available buses from {source} to {dest} on {date}:")
            for i, b in enumerate(buses, 1):
                print(f"{i}. {b}")
            choice = int(input("Select bus (1-3): "))
            ticket['id'] = '12345'
            ticket['info'] = f"{buses[choice - 1]} | {source} ➡ {dest} on {date}"
            print(f"🎫 Ticket booked successfully! Your Ticket ID is {ticket['id']}")

        elif intent == 'view_ticket':
            if ticket:
                tid = input("🔍 Enter Ticket ID: ")
                if ticket.get('id') == tid:
                    print(f"📄 Ticket {tid} Details:\n{ticket['info']}\nStatus: ✅ Confirmed")
                else:
                    print("❌ Ticket not found.")
            else:
                print("📭 No active ticket to view.")

        elif intent == 'cancel_ticket':
            if ticket:
                tid = input("🔍 Enter Ticket ID: ")
                if ticket.get('id') == tid:
                    print(f"📄 Ticket {tid} Details:\n{ticket['info']}\nStatus: ✅ Confirmed")
                    confirm = input("Are you sure you want to cancel? (yes/no): ").lower()
                    if confirm == 'yes':
                        ticket.clear()
                        print("❌ Ticket cancelled and removed from the system.")
                    else:
                        print("✅ Cancellation aborted.")
                else:
                    print("❌ Invalid Ticket ID.")
            else:
                print("📭 No active ticket to cancel.")

        elif intent == 'support':
            print("☎️ Connecting to customer support... Please wait.")
            break

        elif intent == 'exit':
            print("👋 Thank you for using RedBus. Safe travels!")
            break

        else:
            print("🤖 Sorry, I didn't understand that. Try saying 'book a bus' or 'view ticket'.")

# Run the chatbot
if __name__ == "__main__":
    redbus_chatbot()
