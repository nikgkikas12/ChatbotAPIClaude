import tkinter as tk
import threading
import anthropic
from tkinter import scrolledtext

# Initialize the client correctly
client = anthropic.Anthropic()  # Make sure to add your API key

SYSTEM_PROMPT = "You are a friendly and helpful assistant. Keep your answers concise."


class ChatbotUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ChatBot With AI")
        self.root.geometry("1000x1000")
        self.root.configure(bg="#2E2E2E")

        self.messages = []

        tk.Label(
            root, text="AI ChatBot", font=("Helvetica", 20, "bold"),
            fg="#FFFFFF", bg="#2E2E2E"
        ).pack(pady=10)

        self.chat_area = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, height=30, width=100, font=("Arial", 15),
            bg="#3C3C3C", fg="#E0E0E0", insertbackground="white"
        )
        self.chat_area.pack(pady=90, padx=90)
        self.chat_area.insert(tk.END,
                              "Welcome to MicroChat\n"
                              "Made by nikos21_2\n")
        self.chat_area.config(state="disabled")

        input_frame = tk.Frame(root, bg="#2E2E2E")
        input_frame.pack(pady=5)

        self.input_field = tk.Entry(
            input_frame, width=40, font=('Arial', 11), bg="#4A4A4A", fg="#FFFFFF",
            insertbackground="white"
        )
        self.input_field.pack(side=tk.LEFT, padx=5)
        self.input_field.bind("<Return>", self.send_message)

        # Send button
        self.send_button = tk.Button(
            input_frame, text="Send", command=self.send_message, font=("Arial", 11),
            bg="#4CAF50", fg="#FFFFFF", activebackground="#45A049"
        )
        self.send_button.pack(side=tk.LEFT, padx=5)

        # Clear button
        tk.Button(
            root, text="Clear Chat", command=self.clear_chat, font=("Arial", 11),
            bg="#F44336", fg="#FFFFFF", activebackground="#D32F2F"
        ).pack(pady=5)

    def send_message(self, event=None):
        user_input = self.input_field.get().strip()
        if not user_input:
            return

        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, f"\nYou: {user_input}\n")
        self.chat_area.insert(tk.END, f"Bot: ")
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)
        self.input_field.delete(0, tk.END)

        # Fixed typo: "content" instead of "contect"
        self.messages.append({"role": "user", "content": user_input})
        self.input_field.config(state='disabled')
        self.send_button.config(state='disabled')

        thread = threading.Thread(target=self.stream_response, daemon=True)
        thread.start()

    def stream_response(self):
        full_response = ""
        # Fixed: Use the SYSTEM_PROMPT variable properly
        with client.messages.stream(
                model="claude-sonnet-4-6",  # Fixed model name
                max_tokens=1024,
                system=SYSTEM_PROMPT,  # Removed quotes
                messages=self.messages,
        ) as stream:
            for text in stream.text_stream:
                full_response += text

                # Update UI with each chunk
                self.root.after(0, self.append_text, text)
        # Add assistant response to conversation history
        self.messages.append({"role": "assistant", "content": full_response})

        # Re-enable input
        self.root.after(0, self.finish_response)

    def append_text(self, text):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, text)
        #self.chat_area.see(tk.END)
        #self.chat_area.config(state='disabled')

    def finish_response(self):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, "\n")
        self.chat_area.config(state='disabled')
        self.input_field.config(state='normal')
        #self.send_button.config(state='normal')
        #self.input_field.focus()

    def clear_chat(self):
        self.chat_area.config(state='normal')
        self.chat_area.delete(1.0, tk.END)
        self.chat_area.insert(tk.END,
                              "Welcome to MicroChat!\n"
                              "Ask about microcontrollers.\n")
        self.chat_area.config(state='disabled')
        # Clear message history as well
        self.messages = []


def main():
    root = tk.Tk()
    app = ChatbotUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()