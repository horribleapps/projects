import speech_recognition as sr

# Initialize the recognizer
recognizer = sr.Recognizer()

# List all available microphones
mic_list = sr.Microphone.list_microphone_names()
print("Available microphones:")
for i, mic_name in enumerate(mic_list):
    print(f"{i}: {mic_name}")

# Use the desired microphone as source (change the index to the correct one)
mic_index = 2  # Change this to the index of your microphone
with sr.Microphone(device_index=mic_index) as source:
    print("Say something!")
    audio_data = recognizer.listen(source)

# Recognize the speech
try:
    text = recognizer.recognize_google(audio_data)
    print("You said:", text)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError:
    print("Could not request results from Google Speech Recognition service")
