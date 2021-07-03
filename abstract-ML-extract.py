from transformers import BartForConditionalGeneration, BartTokenizer, BartConfig

# Loading the model and tokenizer for bart-large-cnn

tokenizer=BartTokenizer.from_pretrained('facebook/bart-large-cnn')
model=BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

original_text="Musk was born to a Canadian mother and South African father and raised in Pretoria, South Africa. He briefly attended the University of Pretoria before moving to Canada aged 17 to attend Queen's University. He transferred to the University of Pennsylvania two years later, where he received bachelor's degrees in economics and physics. He moved to California in 1995 to attend Stanford University but decided instead to pursue a business career, co-founding the web software company Zip2 with brother Kimbal. The startup was acquired by Compaq for $307 million in 1999. Musk co-founded online bank X.com that same year, which merged with Confinity in 2000 to form PayPal. The company was bought by eBay in 2002 for $1.5 billion."
# Encoding the inputs and passing them to model.generate()
inputs = tokenizer.batch_encode_plus([original_text],return_tensors='pt', max_length=30)
summary_ids = model.generate(inputs['input_ids'], early_stopping=True)

# Decoding and printing the summary
bart_summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
print(bart_summary)