import os

def transcribe(id, input, model):
    audio = f"{id}.wav"
    file = open(audio, "wb")
    file.write(input)
    file.close()
    input_result = model.transcribe(audio)
    translated_result = model.transcribe(audio,task="translate")
    os.remove(audio)
    return {
        'english_text': translated_result['text'].strip(),
        'input_language': translated_result['language'],
        'input_text': input_result['text'].strip()
    }

def translate(text, output_lang, model_tr, tokenizers):
    try:
        tokenizer = tokenizers[output_lang]
        encoded_msg = tokenizer(text, return_tensors="pt")
        generated_tokens = model_tr.generate(**encoded_msg, forced_bos_token_id=tokenizer.get_lang_id(output_lang))
        texts_tr = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
        return texts_tr[0]
    except KeyError as ke: # catches if output_language is not a supported tokenizer language
        print('The language you selected is not supported. Please try again.')
        raise ke
