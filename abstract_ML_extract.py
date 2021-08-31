from transformers import BartForConditionalGeneration, BartTokenizer
from parse_article import parse

#breaks text into chunks of 1024 words
def break_article(text):
    text = text.split(" ") #splits text into words
    sents = []
    breaks = len(text) // 1024

    #creates groupings of 1024 words (if applicable)
    for i in range(1, breaks+1): 
        sent = text[(i-1)*1024:i*1024+1]
        sents.append(sent)

    sents.append(text[1024*breaks+1:]) #appends the remaining words

    return sents

def get_summary(text):
    try:
        tokenizer=BartTokenizer.from_pretrained('facebook/bart-large-cnn') #getting pretrained BART tokenizer
        model=BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn') #getting pretrained BART model

        sents = break_article(text)
        summary = []

        for sent in sents:
            sent = " ".join([str(i) for i in sent]) 
            
            #text cleanup
            sent = sent.encode("ascii", "ignore")
            sent = sent.decode()

            # Encoding the inputs and passing them to model.generate()
            inputs = tokenizer.batch_encode_plus([sent], return_tensors='pt', max_length=1024, truncation=True) 
            summary_ids = model.generate(inputs['input_ids'], early_stopping = True, min_length = 150)

            # Decoding and printing the summary
            summary.append(tokenizer.decode(summary_ids[0], skip_special_tokens=True))

        return " ".join([str(i).strip() for i in summary])
        
    except: 
        return False
    
    
