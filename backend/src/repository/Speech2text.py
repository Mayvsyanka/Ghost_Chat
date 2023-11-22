import librosa
from transformers import SpeechT5Processor, SpeechT5ForSpeechToText


async def speech2text(file_path):

    print("start")

    waveform, original_sample_rate = librosa.load(
        file_path, sr=None, mono=True)

    expected_sample_rate = 16000


    if original_sample_rate != expected_sample_rate:
        waveform = librosa.resample(
            waveform, orig_sr=original_sample_rate, target_sr=expected_sample_rate)


    processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_asr")
    model = SpeechT5ForSpeechToText.from_pretrained("microsoft/speecht5_asr")


    inputs = processor(audio=waveform.tolist(),
                       sampling_rate=expected_sample_rate, return_tensors="pt")
    predicted_ids = model.generate(**inputs, max_length=1000)


    transcription = processor.batch_decode(
        predicted_ids, skip_special_tokens=True)
    return (transcription[0])

