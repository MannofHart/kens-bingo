# [START tts_synthesize_ssml]
def synthesize_ssml(ssml, file_name):
    """Synthesizes speech from the input string of ssml.
    Note: ssml must be well-formed according to:
        https://www.w3.org/TR/speech-synthesis/
    Example: <speak>Hello there.</speak>
    """
    from google.cloud import texttospeech
    from pydub import AudioSegment
    import os
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.types.SynthesisInput(ssml=ssml)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE,
        name='en-US-Wavenet-D'
    )

    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    response = client.synthesize_speech(input_text, voice, audio_config)

    # The response's audio_content is binary.
    with open(f'{file_name}.mp3', 'wb') as out:
        out.write(response.audio_content)
        print(f'Audio content written to file {file_name}.mp3')
    sound = AudioSegment.from_mp3(f'{file_name}.mp3')
    sound.export(f'{file_name}.wav', format="wav")
    os.remove(f'{file_name}.mp3')
# [END tts_synthesize_ssml]

filepath = 'phrases.txt'
with open(filepath) as fp:
   line = fp.readline().strip()
   line_count = 1
   while line:
       letter = ''
       if line_count in range(1, 16):
           letter = 'B'
       elif line_count in range(16, 31):
           letter = 'I'
       elif line_count in range(31, 46):
           letter = 'N'
       elif line_count in range(46, 61):
           letter = 'G'
       elif line_count in range(61, 75):
           letter = '0'
       synthesize_ssml(
           f'<speak> <emphasis level=\"strong\">{letter} <break time=\"400ms\"/> {line_count}</emphasis> <break time=\"1000ms\"/>{line}</speak>',
           f'assets/{line_count}'
       )
       line = fp.readline().strip()
       line_count += 1