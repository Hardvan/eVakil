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
    """Translate the given text to the given language. If the translation is
    already in the cache, it will not be translated again.

    Args:
        text (str): Text to be translated.
        lang (str): Language to translate to.

    Returns:
        str: Translated text.
    """

    # Check if the translation is already in the cache
    cache_key = (text, lang)
    if cache_key in translation_cache:
        return translation_cache[cache_key]

    translator = Translator()
    translation = translator.translate(text, src="en", dest=LANG_MAP[lang])

    # Cache the translation
    translation_cache[cache_key] = translation.text

    return translation.text


# Dictionary to cache audio files
audio_cache = {}


def make_audio(text, lang, audio_path=None, regen=False):
    """Generate an audio file for the given text in the given language and
    save it to the specified path. If the audio file is already in the cache,
    it will not be generated again unless regen is set to True.

    Args:
        text (str): Text to be converted to audio.
        lang (str): Language of the text.
        audio_path (str, optional): Path to save the audio file. Defaults to None.
        regen (bool, optional): If True, the audio file will be regenerated even
                                if it is already in the cache. Defaults to False.

    Raises:
        ValueError: If audio_path is not provided.

    Returns:
        str: Path to the generated audio file.
    """

    if audio_path is None:
        raise ValueError("Audio path not provided.")

    # Check if the audio is already in the cache
    cache_key = (text, lang)
    if not regen and cache_key in audio_cache:
        return audio_cache[cache_key]

    # Generate the audio file
    tts = gTTS(text=text, lang=LANG_MAP[lang], slow=False)
    tts.save(audio_path)

    # Cache the audio file
    audio_cache[cache_key] = audio_path

    return audio_path


if __name__ == "__main__":
    """
    Test the functions in this module.
    """

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
