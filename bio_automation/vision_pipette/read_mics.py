import speech_recognition as sr

# Initialize the recognizer
recognizer = sr.Recognizer()

# List all available microphones
mic_list = sr.Microphone.list_microphone_names()
print("Available microphones:")
for i, mic_name in enumerate(mic_list):
    print(f"{i}: {mic_name}")

