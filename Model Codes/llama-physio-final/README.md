---
base_model: TinyLlama/TinyLlama-1.1B-Chat-v1.0
library_name: peft
pipeline_tag: text-generation
tags:
- base_model:adapter:TinyLlama/TinyLlama-1.1B-Chat-v1.0
- lora
- transformers
---
# Fine-tuned Physiotherapy Model

## How to Use

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

# Load base model
base_model = AutoModelForCausalLM.from_pretrained(
    "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    device_map="cpu"
)

# Load fine-tuned adapters
model = PeftModel.from_pretrained(base_model, "./llama-physio-final")
tokenizer = AutoTokenizer.from_pretrained("./llama-physio-final")

# Generate
prompt = """<|system|>
You are an expert physiotherapist.</s>
<|user|>
Create exercise plan for knee pain</s>
<|assistant|>"""

inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=200)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```
### Framework versions

- PEFT 0.17.1