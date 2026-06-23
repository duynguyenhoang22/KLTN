import pandas as pd
import numpy as np
import re
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, f1_score, recall_score, precision_score

def tokenize(text):
    # Basic Vietnamese tokenization helper (split by whitespace after stripping punctuation)
    text = str(text).lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    return text.split()

def compute_ttr(texts):
    # Type-Token Ratio
    all_tokens = []
    for t in texts:
        all_tokens.extend(tokenize(t))
    if not all_tokens:
        return 0.0
    return len(set(all_tokens)) / len(all_tokens)

def compute_ngram_diversity(texts, n=3):
    # Proportion of unique n-grams
    all_ngrams = []
    for t in texts:
        tokens = tokenize(t)
        if len(tokens) >= n:
            all_ngrams.extend([tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1)])
    if not all_ngrams:
        return 0.0
    return len(set(all_ngrams)) / len(all_ngrams)

def main():
    print("Loading datasets...")
    df1 = pd.read_csv('data/reference/phase1/vismishds_phase1_final.csv')
    df2 = pd.read_csv('data/reference/phase2/vismish_phase2_final.csv')

    # Identify real data (ground truth baseline)
    df2_real = df2[df2['data_origin'] == 'real'].copy()
    real_smish = df2_real[df2_real['label'] == 1]['content'].tolist()
    real_benign = df2_real[df2_real['label'] == 0]['content'].tolist()

    # Identify synthetic/generated data in Phase 1
    # Phase 1: data_origin == 'synthetic'
    df1_syn = df1[df1['data_origin'] == 'synthetic'].copy()
    syn1_smish = df1_syn[df1_syn['label'] == 1]['content'].tolist()
    syn1_benign = df1_syn[df1_syn['label'] == 0]['content'].tolist()

    # Identify synthetic/generated data in Phase 2
    # Phase 2: data_origin in ['synthetic', 'paraphrased', 'synthetic_hard_positive']
    df2_syn = df2[df2['data_origin'].isin(['synthetic', 'paraphrased', 'synthetic_hard_positive'])].copy()
    syn2_smish = df2_syn[df2_syn['label'] == 1]['content'].tolist()
    syn2_benign = df2_syn[df2_syn['label'] == 0]['content'].tolist()

    print("\n==========================================")
    print("DATASET COMPOSITION COMPARISON")
    print("==========================================")
    print(f"Real Smishing samples: {len(real_smish)}")
    print(f"Real Benign samples:   {len(real_benign)}")
    print("\nPhase 1 Generated:")
    print(f"  - Smishing: {len(syn1_smish)}")
    print(f"  - Benign:   {len(syn1_benign)}")
    print("\nPhase 2 Generated:")
    print(f"  - Smishing: {len(syn2_smish)}")
    print(f"  - Benign:   {len(syn2_benign)}")

    # 1. Length analysis
    print("\n==========================================")
    print("TEXT LENGTH ANALYSIS (Characters)")
    print("==========================================")
    for name, texts in [
        ("Real Smishing (Baseline)", real_smish),
        ("Phase 1 Gen Smishing", syn1_smish),
        ("Phase 2 Gen Smishing", syn2_smish),
        ("Real Benign (Baseline)", real_benign),
        ("Phase 1 Gen Benign", syn1_benign),
        ("Phase 2 Gen Benign", syn2_benign),
    ]:
        lens = [len(str(t)) for t in texts]
        print(f"{name:26s} | Mean: {np.mean(lens):6.2f} | Median: {np.median(lens):5.1f} | Std: {np.std(lens):6.2f} | P90: {np.percentile(lens, 90):5.1f}")

    # 2. Vocabulary & Diversity analysis
    print("\n==========================================")
    print("LEXICAL DIVERSITY & REPETITION")
    print("==========================================")
    for name, texts in [
        ("Real Smishing", real_smish),
        ("Phase 1 Gen Smishing", syn1_smish),
        ("Phase 2 Gen Smishing", syn2_smish),
        ("Real Benign", real_benign),
        ("Phase 1 Gen Benign", syn1_benign),
        ("Phase 2 Gen Benign", syn2_benign),
    ]:
        vocab_size = len(set(token for t in texts for token in tokenize(t)))
        ttr = compute_ttr(texts)
        trigram_div = compute_ngram_diversity(texts, n=3)
        fivegram_div = compute_ngram_diversity(texts, n=5)
        print(f"{name:20s} | Vocab Size: {vocab_size:5d} | TTR: {ttr:.4f} | 3-gram Div: {trigram_div:.4f} | 5-gram Div: {fivegram_div:.4f}")

    # 3. Class leakage (Shortcuts) check
    # Let's see if models trained purely on Phase 1 vs Phase 2 synthetic data perform on Real test data
    # We will use df2_real as our real test set (split 50/50 for tuning/evaluation, or just test on all real data)
    print("\n==========================================")
    print("TRAIN ON SYNTHETIC, TEST ON REAL (TSTR)")
    print("==========================================")
    
    # Train on Phase 1 Synthetic
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 3))
    
    X_train1 = vectorizer.fit_transform(df1_syn['content'].astype(str))
    y_train1 = df1_syn['label'].values
    
    clf1 = LogisticRegression(class_weight='balanced', random_state=42)
    clf1.fit(X_train1, y_train1)
    
    # Test on Real
    X_test_real = vectorizer.transform(df2_real['content'].astype(str))
    y_test_real = df2_real['label'].values
    
    preds1 = clf1.predict(X_test_real)
    print("Classifier trained on Phase 1 Synthetic, tested on Real:")
    print(classification_report(y_test_real, preds1, target_names=["Benign", "Smishing"], digits=4))
    
    # Train on Phase 2 Synthetic
    vectorizer2 = TfidfVectorizer(max_features=5000, ngram_range=(1, 3))
    X_train2 = vectorizer2.fit_transform(df2_syn['content'].astype(str))
    y_train2 = df2_syn['label'].values
    
    clf2 = LogisticRegression(class_weight='balanced', random_state=42)
    clf2.fit(X_train2, y_train2)
    
    X_test_real2 = vectorizer2.transform(df2_real['content'].astype(str))
    preds2 = clf2.predict(X_test_real2)
    print("Classifier trained on Phase 2 Synthetic, tested on Real:")
    print(classification_report(y_test_real, preds2, target_names=["Benign", "Smishing"], digits=4))

if __name__ == '__main__':
    main()
