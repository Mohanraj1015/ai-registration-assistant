# ============================================================
# AI REGISTRATION ASSISTANT
# Free Online AI & Data Science Internship
# Task ID: AI-SS-001
# ============================================================

# Install/import required libraries
import nltk
import re
import json

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords


# ============================================================
# DOWNLOAD NLTK RESOURCES
# ============================================================

nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)


# ============================================================
# REGISTRATION ASSISTANT CLASS
# ============================================================

class RegistrationAssistant:

    def __init__(self):

        # NLP tools
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words("english"))

        # Student information
        self.user_data = {
            "name": "",
            "email": "",
            "field": "",
            "experience": ""
        }

        # Registration status
        self.registration_complete = False

        # Intent patterns
        self.intents = {

            "greeting": [
                "hi",
                "hello",
                "hey",
                "good morning",
                "good evening"
            ],

            "register": [
                "register",
                "registration",
                "apply",
                "join",
                "sign up"
            ],

            "help": [
                "help",
                "support",
                "guide",
                "assist"
            ],

            "status": [
                "status",
                "application status",
                "registration status"
            ],

            "thank_you": [
                "thank",
                "thanks",
                "thank you"
            ]
        }


    # ========================================================
    # NLP PREPROCESSING
    # ========================================================

    def preprocess_text(self, text):

        # Convert text to lowercase
        text = text.lower()

        # Remove unwanted special characters
        text = re.sub(r"[^a-zA-Z0-9@\s.]", "", text)

        # Tokenization
        tokens = word_tokenize(text)

        # Remove stopwords and lemmatize
        tokens = [
            self.lemmatizer.lemmatize(token)
            for token in tokens
            if token not in self.stop_words
        ]

        return tokens


    # ========================================================
    # INTENT CLASSIFICATION
    # ========================================================

    def classify_intent(self, text):

        text_lower = text.lower()
        tokens = self.preprocess_text(text)

        for intent, patterns in self.intents.items():

            for pattern in patterns:

                # Check complete words
                pattern_regex = r"\b" + re.escape(pattern) + r"\b"

                if re.search(pattern_regex, text_lower):
                    return intent

                if pattern in tokens:
                    return intent

        return "unknown"


    # ========================================================
    # NAME EXTRACTION
    # ========================================================

    def extract_name(self, text):

        patterns = [
            r"\bmy name is\s+([A-Za-z]+(?:\s+[A-Za-z]+)*)",
            r"\bi am\s+([A-Za-z]+(?:\s+[A-Za-z]+)*)",
            r"\bi'm\s+([A-Za-z]+(?:\s+[A-Za-z]+)*)"
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:
                return match.group(1).strip()

        return None


    # ========================================================
    # EMAIL EXTRACTION
    # ========================================================

    def extract_email(self, text):

        email_pattern = (
            r"\b[A-Za-z0-9._%+-]+"
            r"@[A-Za-z0-9.-]+\."
            r"[A-Za-z]{2,}\b"
        )

        match = re.search(email_pattern, text)

        if match:
            return match.group(0)

        return None


    # ========================================================
    # FIELD EXTRACTION
    # ========================================================

    def extract_field(self, text):

        text_lower = text.lower()

        fields = {

            "data science": "data science",

            "computer science": "computer science",

            "artificial intelligence":
                "artificial intelligence",

            "machine learning":
                "machine learning",

            "computer engineering":
                "computer engineering",

            "engineering":
                "engineering",

            "ai": "ai"
        }

        # Check longer phrases first
        sorted_fields = sorted(
            fields.items(),
            key=lambda x: len(x[0]),
            reverse=True
        )

        for phrase, field_name in sorted_fields:

            # Complete word matching
            pattern = r"\b" + re.escape(phrase) + r"\b"

            if re.search(pattern, text_lower):

                return field_name

        return None


    # ========================================================
    # EMAIL VALIDATION
    # ========================================================

    def validate_email(self, email):

        pattern = (
            r"^[A-Za-z0-9._%+-]+"
            r"@[A-Za-z0-9.-]+\."
            r"[A-Za-z]{2,}$"
        )

        return bool(re.match(pattern, email))


    # ========================================================
    # SAVE REGISTRATION DATA
    # ========================================================

    def save_registration(self):

        with open(
            "registration_data.json",
            "w"
        ) as file:

            json.dump(
                self.user_data,
                file,
                indent=4
            )


    # ========================================================
    # GENERATE RESPONSE
    # ========================================================

    def get_response(self, user_input):

        # ----------------------------------------------------
        # Extract information from user input
        # ----------------------------------------------------

        name = self.extract_name(user_input)

        email = self.extract_email(user_input)

        field = self.extract_field(user_input)


        # ----------------------------------------------------
        # Save extracted information
        # ----------------------------------------------------

        if name:
            self.user_data["name"] = name

        if email:

            if self.validate_email(email):

                self.user_data["email"] = email

            else:

                return (
                    "The email address looks invalid. "
                    "Please provide a valid email."
                )

        if field:
            self.user_data["field"] = field


        # ----------------------------------------------------
        # Detect intent
        # ----------------------------------------------------

        intent = self.classify_intent(user_input)


        # ----------------------------------------------------
        # Greeting
        # ----------------------------------------------------

        if intent == "greeting":

            return (
                "Hello! 👋\n"
                "I am the AI Registration Assistant.\n"
                "I can help you with student registration."
            )


        # ----------------------------------------------------
        # Registration
        # ----------------------------------------------------

        if intent == "register":

            return (
                "Sure! Let's start your registration. 😊\n"
                "Please provide your full name.\n\n"
                "Example: My name is Mohan"
            )


        # ----------------------------------------------------
        # Help
        # ----------------------------------------------------

        if intent == "help":

            return (
                "I can help you with:\n"
                "1. Student Registration\n"
                "2. Personal Information\n"
                "3. Field of Study\n"
                "4. Registration Status\n"
                "5. General Guidance"
            )


        # ----------------------------------------------------
        # Application Status
        # ----------------------------------------------------

        if intent == "status":

            return (
                "Your registration application is currently "
                "being processed."
            )


        # ----------------------------------------------------
        # Thank You
        # ----------------------------------------------------

        if intent == "thank_you":

            return (
                "You're welcome! 😊\n"
                "Is there anything else I can help you with?"
            )


        # ----------------------------------------------------
        # Ask for missing name
        # ----------------------------------------------------

        if self.user_data["name"] == "":

            return (
                "Please tell me your full name.\n"
                "Example: My name is Mohan"
            )


        # ----------------------------------------------------
        # Ask for missing email
        # ----------------------------------------------------

        if self.user_data["email"] == "":

            return (
                f"Nice to meet you, "
                f"{self.user_data['name']}! 👋\n"
                "Please provide your email address."
            )


        # ----------------------------------------------------
        # Ask for missing field
        # ----------------------------------------------------

        if self.user_data["field"] == "":

            return (
                "Thank you! 👍\n"
                "Now please tell me your field of study.\n\n"
                "Example: Data Science"
            )


        # ----------------------------------------------------
        # Complete Registration
        # ----------------------------------------------------

        if (
            self.user_data["name"] != ""
            and self.user_data["email"] != ""
            and self.user_data["field"] != ""
        ):

            self.registration_complete = True

            # Save data
            self.save_registration()

            return (
                "\n🎉 REGISTRATION COMPLETED SUCCESSFULLY! 🎉\n"
                "\n"
                f"Name   : {self.user_data['name']}\n"
                f"Email  : {self.user_data['email']}\n"
                f"Field  : {self.user_data['field']}\n"
                "\n"
                "Your registration data has been saved "
                "to registration_data.json.\n"
            )


        # ----------------------------------------------------
        # Unknown input
        # ----------------------------------------------------

        return (
            "I'm not sure I understood that. 🤔\n"
            "Please type 'help' to see what I can do."
        )


# ============================================================
# CREATE ASSISTANT
# ============================================================

assistant = RegistrationAssistant()


# ============================================================
# START CHATBOT
# ============================================================

print("=" * 55)
print("🤖 AI REGISTRATION ASSISTANT")
print("=" * 55)

print(
    "Welcome! I can help you with student registration."
)

print(
    "Type 'help' for assistance."
)

print(
    "Type 'exit' to close the assistant."
)

print("=" * 55)


# ============================================================
# CHAT LOOP
# ============================================================

while True:

    user_input = input("\nYou: ")

    # Exit command
    if user_input.lower().strip() in [
        "exit",
        "quit",
        "bye"
    ]:

        print(
            "\nAssistant: "
            "Thank you for using the AI Registration Assistant. "
            "Goodbye! 👋"
        )

        break


    # Generate response
    response = assistant.get_response(user_input)

    print("\nAssistant:", response)
