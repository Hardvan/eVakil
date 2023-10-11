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
    if not regen and cache_key in audio_cache and os.path.exists(audio_cache[cache_key]):
        return audio_cache[cache_key]

    # Generate the audio file
    tts = gTTS(text=text, lang=LANG_MAP[lang], slow=False)
    tts.save(audio_path)

    # Cache the audio file
    audio_cache[cache_key] = audio_path

    return audio_path


def test_translate_message():
    """Test the translate_message function.

    Output:
    =====================================
    Running time for translate_message()
    =====================================
    Text length: 1900

    Test 1: Without caching
    Time taken without caching (Test 1): 2185.41ms

    Test 2: Without caching (different request)
    Time taken without caching (Test 2): 1658.46ms

    Test 3: With caching
    Time taken with caching (Test 3): 0.00ms
    """

    import time

    LINE = "====================================="

    # Check the running time for translate_message
    print(LINE)
    print("Running time for translate_message()")
    print(LINE)
    text = "Hello, how are you?" * 100
    print("Text length:", len(text))

    # Test 1: Without caching (same translation request)
    print("\nTest 1: Without caching")
    start = time.time()
    translate_message(text, "Hindi")
    end = time.time()
    ms = (end - start) * 1000
    print(f"Time taken without caching (Test 1): {ms:.2f}ms")

    # Test 2: Without caching (different translation request)
    print("\nTest 2: Without caching (different request)")
    start = time.time()
    translate_message(text, "Marathi")
    end = time.time()
    ms = (end - start) * 1000
    print(f"Time taken without caching (Test 2): {ms:.2f}ms")

    # Test 3: With caching (same translation request)
    print("\nTest 3: With caching")
    start = time.time()
    translate_message(text, "Hindi")
    end = time.time()
    ms = (end - start) * 1000
    print(f"Time taken with caching (Test 3): {ms:.2f}ms")


def test_make_audio():
    """Test the make_audio function.

    Output:
    =====================================
    Running time for make_audio()
    =====================================
    Text length: 190

    Test 1: Without caching
    Time taken without caching (Test 1): 4388.61ms

    Test 2: Without caching (different request)
    Time taken without caching (Test 2): 4768.54ms

    Test 3: With caching
    Time taken with caching (Test 3): 0.00ms
    """

    import time

    LINE = "====================================="

    # Check the running time for make_audio
    print("\n")
    print(LINE)
    print("Running time for make_audio()")
    print(LINE)
    text = "Hello, how are you?" * 10
    print("Text length:", len(text))

    # Test 1: Without caching (same translation request)
    print("\nTest 1: Without caching")
    start = time.time()
    audio_path_1 = make_audio(
        text, "Hindi", audio_path="./static/audio/test_1.mp3")
    end = time.time()
    ms = (end - start) * 1000
    print(f"Time taken without caching (Test 1): {ms:.2f}ms")

    # Test 2: Without caching (different translation request)
    print("\nTest 2: Without caching (different request)")
    start = time.time()
    audio_path_2 = make_audio(
        text, "Marathi", audio_path="./static/audio/test_2.mp3")
    end = time.time()
    ms = (end - start) * 1000
    print(f"Time taken without caching (Test 2): {ms:.2f}ms")

    # Test 3: With caching (same translation request)
    print("\nTest 3: With caching")
    start = time.time()
    audio_path_1 = make_audio(
        text, "Hindi", audio_path=audio_path_1)
    end = time.time()
    ms = (end - start) * 1000
    print(f"Time taken with caching (Test 3): {ms:.2f}ms")

    # Delete the audio files
    os.remove(audio_path_1)
    os.remove(audio_path_2)


def display_cache():

    LINE = "====================================="

    print("\n")
    print(LINE)
    print("Cache contents")
    print(LINE)
    print("Translation cache:", translation_cache)
    print("Audio cache:", audio_cache)


if __name__ == "__main__":

    test_translate_message()
    test_make_audio()
    # display_cache()
