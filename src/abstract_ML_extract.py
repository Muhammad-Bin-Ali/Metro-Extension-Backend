from transformers import BartForConditionalGeneration, BartTokenizer
from parse_article import parse
import torch

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
        device = "cuda:0" if torch.cuda.is_available() else "cpu"

        tokenizer=BartTokenizer.from_pretrained('facebook/bart-large-cnn') #getting pretrained BART tokenizer (facebook/bart-large-cnn)
        model=BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn').to(device) #getting pretrained BART model (facebook/bart-large-cnn)
      

        sents = break_article(text)
        summary = []

        for sent in sents:
            sent = " ".join([str(i) for i in sent]) 

            #text cleanup
            sent = sent.encode("ascii", "ignore")
            sent = sent.decode()
        
            # Encoding the inputs and passing them to model.generate()
            inputs = tokenizer.encode_plus(sent, max_length=1024, return_tensors='pt').to(device)
            summary_ids = model.generate(input_ids = inputs['input_ids'], min_length=30)

            # Decoding and printing the summary
            summary.append(tokenizer.decode(summary_ids[0], skip_special_tokens=True))

        return " ".join([str(i).strip() for i in summary])
            
    except: 
        return False
    
if __name__ == "__main__":
    text = parse("https://www.ctvnews.ca/world/syria-executes-24-people-over-last-year-s-deadly-wildfires-1.5632335")
    print(get_summary(text))
    # print(torch.cuda.is_available())