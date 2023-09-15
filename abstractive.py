import transformers
#from transformers import PegasusForConditionalGeneration, AutoTokenizer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

#model_name = "google/pegasus-xsum"
#tokenizer =  AutoTokenizer.from_pretrained(model_name)


def summarize(text):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    #model = PegasusForConditionalGeneration.from_pretrained(model_name).to(device)
    tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-xsum-12-1")
    model = AutoModelForSeq2SeqLM.from_pretrained("sshleifer/distilbart-xsum-12-1")
    text = "summarize the following text: " +text
    inputs = tokenizer(text, max_length=1024, return_tensors="pt")
    #summary_ids = model.generate(inputs["input_ids"])
    summary_ids = model.generate(inputs["input_ids"], num_beams=2, min_length=0, max_length=20)
    summary = tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
    return summary