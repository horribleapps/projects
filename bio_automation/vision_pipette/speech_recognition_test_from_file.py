import speech_recognition as sr
recognizer = sr.Recognizer()
audio_file = sr.AudioFile('output.wav')
with audio_file as source:
    audio_data = recognizer.record(source)
try:
    text = recognizer.recognize_google(audio_data)
    print("Recognized Text:", text)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError:
    print("Could not request results from Google Speech Recognition service")
