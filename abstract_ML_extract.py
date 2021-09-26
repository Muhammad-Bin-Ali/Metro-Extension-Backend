from transformers import BartForConditionalGeneration, BartTokenizer, pipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from parse_article import parse

#breaks text into chunks of 1024 words
def break_article(text):
    text = text.split(" ") #splits text into words
    sents = []
    breaks = len(text) // 800

    #creates groupings of 1024 words (if applicable)
    for i in range(1, breaks+1): 
        sent = text[(i-1)*800:i*800]
        sents.append(sent)


    sents.append(text[800*breaks+1:]) #appends the remaining words
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
            inputs = tokenizer.encode_plus(sent, max_length=1024, return_tensors='pt')
            summary_ids = model.generate(input_ids = inputs['input_ids'], min_length=30)

            # Decoding and printing the summary
            summary.append(tokenizer.decode(summary_ids[0], skip_special_tokens=True))

        return " ".join([str(i).strip() for i in summary])
            
    except: 
        return False
    
if __name__ == "__main__":
    text = parse("https://www.ctvnews.ca/politics/two-michaels-land-safely-in-canada-after-nearly-three-years-of-detention-in-china-1.5600335")
    print(get_summary(text))