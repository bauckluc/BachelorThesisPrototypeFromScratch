import time
from openai import OpenAI
from apiKey import OPENAI_KEY

client = OpenAI(api_key=OPENAI_KEY)

# Vorbereitungen (einmalig)
assistant_id = "asst_nah37WsEZ9Jvqg94do3K3afo"

# Thread erstellen
thread = client.beta.threads.create()
thread_id = thread.id
print(f"Thread gestartet mit ID: {thread_id}")

# Chatloop starten
while True:
    user_input = input("\nDu: ")

    if user_input.lower() in {"exit", "quit", "bye"}:
        print("Chatbot beendet. Bis bald!")
        break

    # Neue Nachricht hinzufügen
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_input
    )

    # Run starten
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

    # Auf Fertigstellung warten
    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        if run_status.status == "completed":
            break
        time.sleep(1)  # Kurzes Warten vor erneutem Check

    # Antwort ausgeben
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    assistant_messages = [
        msg for msg in messages.data if msg.role == "assistant"
    ]

    if assistant_messages:
        latest_reply = assistant_messages[0].content[0].text.value
        print(f"\nAssistant: {latest_reply}")
    else:
        print("\nAssistant: (keine Antwort erhalten)")
