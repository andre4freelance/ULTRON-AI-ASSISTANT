import speech_recognition as sr

print("🔍 Daftar perangkat microphone:")
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"{index}: {name}")
