# Metro-SimpliRead-Backend

The server source code for Metropolitan SimpliRead.

Using Facebook's BERT model, the server is able to take any webpage and provide a grammatically cohesive summary. Beautiful Soup is used to parse webpages and PyMongo is used to connect with a MongoDB Atlas Cluster. The cluster contains user information such as their unique Google ID and their saved summaries. 

Built using:
- RESTFUL Flask library
- Beautiful Soup
- Python Hugging Face
- PyMongo

## Challenges

The biggest challenge that I ran into was implementing the natural language processing. I tried many different models such as Google's Pegasus, T5, and other variations of the BART transformer. However, a common problem amongst them was that they all produced a very short summary (1-2 sentences). As a result, the summary just didn't provide any meaningful information. Once I finally stumbled across the Facebook-cnn-large model (trained using CNN's news dataset), I still had to fine-tune it and play with the parameters to make it produce a usable body of text. 

## Future Goals

The backend is largely complete. My next step is to deploy it. This has been especially difficult as the majority of the cloud hosting platforms don't offer free tiers that meet the technical requirements of the server. As such, I'm looking to deploy this on a Linux virtual machine. 
