from transformers import GPT2LMHeadModel, GPT2Tokenizer
import pyttsx3

def gptvoice(prompt):
   
    model_name = 'gpt2'
    model = GPT2LMHeadModel.from_pretrained(model_name)
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)

   
    inputs = tokenizer.encode("tell "+prompt, return_tensors='pt')

    
    outputs = model.generate(
        inputs, 
        max_length=200, 
        num_return_sequences=1, 
        no_repeat_ngram_size=2, 
        early_stopping=True, 
        temperature=0.7,  
        top_k=50,         
        top_p=0.95,       
        do_sample=True    
    )

    
    engine = pyttsx3.init()

    
    for i, output in enumerate(outputs):
        
        story = tokenizer.decode(output, skip_special_tokens=True)
        
       
        print(f"Story {i + 1}:\n{story}\n")
        
        
        engine.say(story)

   
    engine.runAndWait()


