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
    if any(w in lemmas for w in ['book', 'service', 'repair', 'technician']):
        return 'book_service'
    elif any(w in lemmas for w in ['status', 'check', 'track']):
        return 'track_service'
    elif any(w in lemmas for w in ['cancel']):
        return 'cancel_service'
    elif any(w in lemmas for w in ['help', 'support']):
        return 'support'
    elif any(w in lemmas for w in ['exit', 'bye', 'quit']):
        return 'exit'
    return 'unknown'

# Simulated booking store
booking = {}

def ifb_service_chatbot():
    print("🧠 Welcome to IFB Washing Machine Service Centre Chatbot!")
    print("Say things like 'book a service', 'track my request', or 'cancel appointment'.")

    while True:
        user_input = input("\nYou: ")
        lemmas = preprocess(user_input)
        intent = get_intent(lemmas)

        if intent == 'book_service':
            name = input("👤 Your Name: ")
            city = input("🏙️ City: ")
            issue = input("⚙️ Describe the issue: ")
            date = input("📅 Preferred service date (YYYY-MM-DD): ")
            booking['id'] = 'SRV001'
            booking['details'] = f"{name} | {city} | Issue: {issue} | Date: {date}"
            print(f"✅ Service booked successfully! Your Service ID is {booking['id']}")

        elif intent == 'track_service':
            if booking:
                bid = input("🔍 Enter Service ID: ")
                if bid == booking.get('id'):
                    print(f"📄 Service {bid} Details:\n{booking['details']}\nStatus: 🛠️ Scheduled")
                else:
                    print("❌ Service ID not found.")
            else:
                print("📭 No active service booking to track.")

        elif intent == 'cancel_service':
            if booking:
                bid = input("🔍 Enter Service ID: ")
                if bid == booking.get('id'):
                    confirm = input("Are you sure you want to cancel the service? (yes/no): ").lower()
                    if confirm == 'yes':
                        booking.clear()
                        print("❌ Service booking cancelled.")
                    else:
                        print("✅ Cancellation aborted.")
                else:
                    print("❌ Invalid Service ID.")
            else:
                print("📭 No active service booking to cancel.")

        elif intent == 'support':
            print("☎️ Connecting you to an IFB customer support representative...")
            break

        elif intent == 'exit':
            print("👋 Thank you for using IFB Service Centre Chatbot. Have a great day!")
            break

        else:
            print("🤖 Sorry, I didn’t understand. Try saying 'book a service' or 'track my request'.")

# Run chatbot
if __name__ == "__main__":
    ifb_service_chatbot()
