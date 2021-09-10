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
    # try:
    # tokenizer=BartTokenizer.from_pretrained('sshleifer/distilbart-cnn-12-6') #getting pretrained BART tokenizer
    # model=BartForConditionalGeneration.from_pretrained('sshleifer/distilbart-cnn-12-6') #getting pretrained BART model

    sents = break_article(text)
    summary = []
    summarizer = pipeline("summarization")
    
    for sent in sents:
        sent = " ".join([str(i) for i in sent]) 

        #text cleanup
        sent = sent.encode("ascii", "ignore")
        sent = sent.decode()

        # # Encoding the inputs and passing them to model.generate()
        # # inputs = tokenizer.batch_encode_plus([sent], return_tensors='pt', max_length=1024, truncation=True) 
        # inputs = tokenizer.__call__([sent], is_split_into_words=True, max_length=1024, return_tensors='pt')
        # summary_ids = model.generate(inputs['input_ids'])

        # # Decoding and printing the summary
        # summary.append(tokenizer.decode(summary_ids[0], skip_special_tokens=True))
        summ_text = summarizer(sent, do_sample=False)
        summary.append(summ_text[0]['summary_text'])

    return " ".join([str(i).strip() for i in summary])
        
    # except: 
    #     return False
    
if __name__ == "__main__":
    text = parse("https://www.cbc.ca/radio/thecurrent/the-current-for-sept-8-2021-1.6167882/former-afghanistan-correspondent-reflects-on-what-he-once-believed-was-a-noble-war-1.6168383")

    print(get_summary(text))