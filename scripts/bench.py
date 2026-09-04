"""Speed benchmark: how fast is one fine-tuning step of GPT-2 on MPS?"""
import time, torch
from transformers import AutoModelForCausalLM, AutoTokenizer

name = "gpt2"
tok = AutoTokenizer.from_pretrained(name)
model = AutoModelForCausalLM.from_pretrained(name).to("mps")
model.train()
opt = torch.optim.AdamW(model.parameters(), lr=1e-4)
for B, L in [(16, 64), (16, 96), (32, 64)]:
    x = torch.randint(0, 50257, (B, L), device="mps")
    # warmup
    for _ in range(3):
        loss = model(input_ids=x, labels=x).loss; loss.backward(); opt.step(); opt.zero_grad()
    torch.mps.synchronize(); t = time.time()
    n = 10
    for _ in range(n):
        loss = model(input_ids=x, labels=x).loss; loss.backward(); opt.step(); opt.zero_grad()
    torch.mps.synchronize()
    print(f"B={B} L={L}: {(time.time()-t)/n*1000:.0f} ms/step")
