from transformers import BartForConditionalGeneration, BartTokenizer


def break_article(text):
    text = text.split(" ")
    sents = []
    breaks = len(text) // 1024

    for i in range(1, breaks+1):
        sent = text[(i-1)*1024:i*1024+1]
        sents.append(sent)

    sents.append(text[1024*breaks+1:])

    return sents

def get_summary(text):
    tokenizer=BartTokenizer.from_pretrained('facebook/bart-large-cnn') #getting pretrained BART tokenizer
    model=BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn') #getting pretrained BART model

    sents = break_article(text)

    for sent in sents:
        sent = " ".join([str(i) for i in sent])
        
        # Encoding the inputs and passing them to model.generate()
        inputs = tokenizer.batch_encode_plus([sent], return_tensors='pt', max_length=1024, truncation=True) 
        summary_ids = model.generate(inputs['input_ids'], early_stopping = True, min_length = 150)

        # Decoding and printing the summary
        bart_summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        print(bart_summary)
        print()

if __name__ == "__main__":
    text = "Just testing it out"
    get_summary(text)

#Work on fixing max_length