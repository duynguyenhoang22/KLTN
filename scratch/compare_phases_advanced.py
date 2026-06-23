import pandas as pd
import numpy as np
import re
import math
import random
from collections import Counter
import nltk
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

try:
    smoothing = SmoothingFunction().method1
except:
    smoothing = None

def tokenize(text):
    text = str(text).lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    return text.split()

# 1. Shannon Entropy of N-grams
def shannon_entropy(texts, n=2):
    all_ngrams = []
    for t in texts:
        tokens = tokenize(t)
        if len(tokens) >= n:
            all_ngrams.extend([tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1)])
    if not all_ngrams:
        return 0.0
    counts = Counter(all_ngrams)
    total = sum(counts.values())
    entropy = -sum((count / total) * math.log2(count / total) for count in counts.values())
    return entropy

# 2. Robust Self-BLEU over 3 Seeds with N=500
def calculate_robust_self_bleu(texts, sample_size=500, seeds=[42, 123, 2025], weights=(1/3, 1/3, 1/3)):
    run_scores = []
    
    # If the text corpus is smaller than sample_size, we just compute on all texts once
    if len(texts) <= sample_size:
        tokenized_texts = [tokenize(t) for t in texts]
        bleu_scores = []
        for i, candidate in enumerate(tokenized_texts):
            references = tokenized_texts[:i] + tokenized_texts[i+1:]
            if not candidate or not references:
                continue
            score = sentence_bleu(references, candidate, weights=weights, smoothing_function=smoothing)
            bleu_scores.append(score)
        return np.mean(bleu_scores) if bleu_scores else 0.0

    # Run for each seed
    for seed in seeds:
        random.seed(seed)
        sampled_texts = random.sample(texts, sample_size)
        tokenized_texts = [tokenize(t) for t in sampled_texts]
        bleu_scores = []
        
        for i, candidate in enumerate(tokenized_texts):
            references = tokenized_texts[:i] + tokenized_texts[i+1:]
            if not candidate or not references:
                continue
            try:
                score = sentence_bleu(references, candidate, weights=weights, smoothing_function=smoothing)
                bleu_scores.append(score)
            except:
                pass
        
        mean_run_score = np.mean(bleu_scores) if bleu_scores else 0.0
        run_scores.append(mean_run_score)
        print(f"  - Run with Seed {seed:4d}: Self-BLEU-3 = {mean_run_score:.4f}")
        
    return np.mean(run_scores)

def main():
    print("Loading datasets...")
    df1 = pd.read_csv('data/reference/phase1/vismishds_phase1_final.csv')
    df2 = pd.read_csv('data/reference/phase2/vismish_phase2_final.csv')

    # Extract real smishing (reference baseline)
    df2_real = df2[df2['data_origin'] == 'real'].copy()
    real_smish = df2_real[df2_real['label'] == 1]['content'].astype(str).tolist()

    # Extract synthetic smishing in Phase 1
    df1_syn = df1[(df1['data_origin'] == 'synthetic') & (df1['label'] == 1)].copy()
    syn1_smish = df1_syn['content'].astype(str).tolist()

    # Extract synthetic smishing in Phase 2
    df2_syn = df2[df2['data_origin'].isin(['synthetic', 'paraphrased', 'synthetic_hard_positive']) & (df2['label'] == 1)].copy()
    syn2_smish = df2_syn['content'].astype(str).tolist()

    print("\n==========================================")
    print("1. SHANNON ENTROPY OF N-GRAMS")
    print("==========================================")
    print("Objective: Evaluate vocab variety and combination richness (higher is better).")
    print("Metric: Information Entropy H(X) in bits.")
    
    for name, texts in [
        ("Real Smishing (Baseline)", real_smish),
        ("Phase 1 Gen Smishing", syn1_smish),
        ("Phase 2 Gen Smishing", syn2_smish)
    ]:
        h1 = shannon_entropy(texts, n=1)
        h2 = shannon_entropy(texts, n=2)
        h3 = shannon_entropy(texts, n=3)
        print(f"{name:26s} | Unigram Entropy: {h1:.4f} bits | Bigram Entropy: {h2:.4f} bits | Trigram Entropy: {h3:.4f} bits")

    print("\n==========================================")
    print("2. ROBUST SELF-BLEU DIVERSITY (Sample size = 500, 3 runs)")
    print("==========================================")
    print("Objective: Evaluate boilerplate templates and repetition (lower is better).")
    print("Metric: Mean Self-BLEU-3 across 3 seeds.")
    
    for name, texts in [
        ("Real Smishing (Baseline)", real_smish),
        ("Phase 1 Gen Smishing", syn1_smish),
        ("Phase 2 Gen Smishing", syn2_smish)
    ]:
        print(f"\nComputing for {name} (N_total = {len(texts)})...")
        sb3 = calculate_robust_self_bleu(texts, sample_size=500, seeds=[42, 123, 2025], weights=(1/3, 1/3, 1/3))
        print(f"** {name:26s} | Final Averaged Self-BLEU-3: {sb3:.4f} **")

if __name__ == '__main__':
    main()
