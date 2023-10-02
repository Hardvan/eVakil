from googletrans import Translator
from gtts import gTTS
import os


# ? Language mapping
LANG_MAP = {"English": "en",
            "Hindi": "hi",
            "Marathi": "mr",
            "Gujarati": "gu",
            "Kannada": "kn",
            "Tamil": "ta",
            "Telugu": "te",
            "Malayalam": "ml",
            "Bengali": "bn",
            "Japanese": "ja",
            }

# Dictionary to cache translations
translation_cache = {}


def translate_message(text, lang):

    # Check if the translation is already in the cache
    if (text, lang) in translation_cache:
        return translation_cache[(text, lang)]

    translator = Translator()
    translation = translator.translate(text, src="en", dest=LANG_MAP[lang])

    # Cache the translation
    translation_cache[(text, lang)] = translation.text

    return translation.text


def make_audio(text, lang, audio_path=None, regen=False):

    if audio_path is None:
        raise ValueError("Audio path not provided.")

    # Audio file not present or REGEN_AUDIO flag is True
    if (not os.path.exists(audio_path)) or (regen):

        tts = gTTS(text=text, lang=LANG_MAP[lang], slow=False)
        tts.save(audio_path)

    return audio_path


if __name__ == "__main__":

    import time

    # Check the running time for translate_message
    print("=====================================")
    print("Running time for translate_message()")
    print("=====================================")
    text = "Hello, how are you?" * 100
    print("Text length:", len(text))

    # Test 1: Without caching (same translation request)
    print("\nTest 1: Without caching")
    start = time.time()
    translation_1 = translate_message(text, "Hindi")
    end = time.time()
    ms = (end - start) * 1000
    print(f"Time taken without caching (Test 1): {ms:.2f}ms")

    # Test 2: Without caching (different translation request)
    print("\nTest 2: Without caching (different request)")
    start = time.time()
    translation_2 = translate_message(text, "Marathi")
    end = time.time()
    ms = (end - start) * 1000
    print(f"Time taken without caching (Test 2): {ms:.2f}ms")

    # Test 3: With caching (same translation request)
    print("\nTest 3: With caching")
    start = time.time()
    translation_3 = translate_message(text, "Hindi")
    end = time.time()
    ms = (end - start) * 1000
    print(f"Time taken with caching (Test 3): {ms:.2f}ms")

    # Check the running time for make_audio
    print("\n\n=====================================")
    print("Running time for make_audio()")
    print("=====================================")
    text = "Hello, how are you?" * 10
    print("Text length:", len(text))

    # Test 4: Without caching (same translation request)
    print("\nTest 4: Without caching")
    start = time.time()
    audio_path_1 = make_audio(
        text, "Hindi", audio_path="./static/audio/test_1.mp3")
    end = time.time()
    ms = (end - start) * 1000
    print(f"Time taken without caching (Test 4): {ms:.2f}ms")

    # Test 5: Without caching (different translation request)
    print("\nTest 5: Without caching (different request)")
    start = time.time()
    audio_path_2 = make_audio(
        text, "Marathi", audio_path="./static/audio/test_2.mp3")
    end = time.time()
    ms = (end - start) * 1000
    print(f"Time taken without caching (Test 5): {ms:.2f}ms")

    # Test 6: With caching (same translation request)
    print("\nTest 6: With caching")
    start = time.time()
    audio_path_1 = make_audio(
        text, "Hindi", audio_path="./static/audio/test_1.mp3")
    end = time.time()
    ms = (end - start) * 1000
    print(f"Time taken with caching (Test 6): {ms:.2f}ms")

    # Delete the audio files
    os.remove("./static/audio/test_1.mp3")
    os.remove("./static/audio/test_2.mp3")

    """
    Output:
    =====================================
    Running time for translate_message()
    =====================================
    Text length: 1900

    Test 1: Without caching
    Time taken without caching (Test 1): 348.10ms

    Test 2: Without caching (different request)
    Time taken without caching (Test 2): 266.46ms

    Test 3: With caching
    Time taken with caching (Test 3): 0.00ms


    =====================================
    Running time for make_audio()
    =====================================
    Text length: 190

    Test 4: Without caching
    Time taken without caching (Test 4): 6084.29ms

    Test 5: Without caching (different request)
    Time taken without caching (Test 5): 6714.04ms

    Test 6: With caching
    Time taken with caching (Test 6): 0.00ms
    """
