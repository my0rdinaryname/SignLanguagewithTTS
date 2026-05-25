import pyttsx3
import time
import sys
import subprocess

def test_tts():
    print("Testing TTS system...\n")
    
    try:
        # Initialize engine with error handling
        engine = pyttsx3.init()

        # Helper: cross-platform speak that uses macOS `say` (blocking) for reliability
        def speak(text, voice_name=None, rate=None, volume=None):
            """Speak `text` blocking-ly.

            On macOS prefer the `say` command because pyttsx3 with the NSSpeech
            backend can return before audio finishes. On other platforms use
            pyttsx3's engine methods.
            """
            if sys.platform == "darwin":
                cmd = ["say"]
                if voice_name:
                    # `say` expects the visible voice name (e.g. "Alex", "Victoria")
                    cmd += ["-v", voice_name]
                if rate:
                    cmd += ["-r", str(int(rate))]
                # Use subprocess.run which blocks until speaking completes
                try:
                    subprocess.run(cmd + [text], check=False)
                except Exception:
                    # Fallback to pyttsx3 if say fails
                    if voice_name:
                        # try mapping to engine voice id later
                        pass
                    engine.say(text)
                    engine.runAndWait()
            else:
                # pyttsx3 path
                if voice_name:
                    # try to match by visible name to available voices
                    for v in voices:
                        if v.name.lower() == voice_name.lower() or v.id == voice_name:
                            engine.setProperty('voice', v.id)
                            break
                if rate is not None:
                    engine.setProperty('rate', rate)
                if volume is not None:
                    engine.setProperty('volume', volume)
                engine.say(text)
                engine.runAndWait()

        # Set nsss driver to fix macOS timing issues (keep a sane default rate)
        engine.setProperty('rate', 150)  # Slower for better reliability

        print("✓ TTS engine initialized\n")
        
        # Get and display current properties
        print("Current TTS Properties:")
        rate = engine.getProperty('rate')
        volume = engine.getProperty('volume')
        voice = engine.getProperty('voice')
        print(f"  Rate: {rate} words/min")
        print(f"  Volume: {volume}")
        print(f"  Voice ID: {voice}\n")
        
        # Display available voices
        voices = engine.getProperty('voices')
        print(f"✓ Found {len(voices)} available voices:")
        for i, v in enumerate(voices):
            print(f"  [{i}] {v.name} - {v.id}")
            print(f"      Languages: {v.languages}")
        print()
        
        # Test 1: Basic speech
        print("Test 1: Basic Speech")
        print("🔊 Speaking...")
        speak("Hello, this is a basic text to speech test.")
        time.sleep(0.2)
        print("✓ Completed\n")
        
        # Test 2: Adjust speech rate
        print("Test 2: Different Speech Rates")
        original_rate = engine.getProperty('rate')
        
        engine.setProperty('rate', original_rate - 50)
        print("🔊 Speaking slowly...")
        speak("This is slow speech.", rate=original_rate - 50)
        time.sleep(0.2)

        engine.setProperty('rate', original_rate + 50)
        print("🔊 Speaking fast...")
        speak("This is fast speech.", rate=original_rate + 50)
        time.sleep(0.2)
        
        engine.setProperty('rate', original_rate)  # Reset
        print("✓ Completed\n")
        
        # Test 3: Adjust volume
        print("Test 3: Different Volumes")
        engine.setProperty('volume', 0.5)
        print("🔊 Speaking at 50% volume...")
        speak("This is at half volume.", volume=0.5)

        engine.setProperty('volume', 1.0)
        print("🔊 Speaking at 100% volume...")
        speak("This is at full volume.", volume=1.0)
        print("✓ Completed\n")
        
        # Test 4: Different voices (if available)
        if len(voices) > 1:
            print("Test 4: Different Voices")
            for i in range(min(2, len(voices))):
                engine.setProperty('voice', voices[i].id)
                print(f"🔊 Using voice: {voices[i].name}")
                # On macOS we pass the human-friendly name to `say`
                speak(f"Hello, I am voice number {i}.", voice_name=voices[i].name, rate=None)
            print("✓ Completed\n")
        
        # Test 5: Digit recognition scenario
        print("Test 5: Digit Recognition Scenario")
        digits = [0, 1, 2, 3, 4, 5]
        for digit in digits:
            print(f"🔊 Announcing digit: {digit}")
            speak(f"The number is {digit}")
        print("✓ Completed\n")
        
        # Test 6: Queue multiple sentences
        print("Test 6: Queued Speech")
        print("🔊 Speaking multiple sentences...")
        # Queue multiple sentences; speak will block per sentence on macOS
        speak("First sentence.")
        speak("Second sentence.")
        speak("Third sentence.")
        print("✓ Completed\n")
        
        print("=" * 50)
        print("All TTS tests completed successfully! ✓")
        
    except Exception as e:
        print(f"❌ TTS Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_tts()