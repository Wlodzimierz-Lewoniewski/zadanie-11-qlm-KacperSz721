import math
import re
from collections import Counter
LAMBDA_VALUE = 0.5

def freq_of_terms(inputed_documents):
    freq_context = Counter()

    terms_list = [Counter(tokenize_input(doc)) for doc in inputed_documents]
    freq_context.update(term for term_freq in terms_list for term in term_freq)
    return terms_list, freq_context

def tokenize_input(input):
    return re.sub(r"[^\w\s]", "", input.lower()).split()

def get_q_like(inputed_documents, q, freq_term, freq_context):
    results = []
    input_tokenized = tokenize_input(q)
    context_len = sum(value for value in freq_context.values())

    def get_p_t(term, freq_term, len_input_doc, freq_context, context_len):
        p_td_value = freq_term[term] / len_input_doc if len_input_doc > 0 else 0
        p_tc_value = freq_context[term] / context_len if context_len > 0 else 0
        return LAMBDA_VALUE * p_td_value + (1 - LAMBDA_VALUE) * p_tc_value

    for index, freq_term in enumerate(freq_term):
        len_input_doc = sum(value for value in freq_term.values())
        result = sum(math.log(p_t)
                     if (p_t := get_p_t(term, freq_term, len_input_doc, freq_context, context_len)) > 0
                     else float('-inf') for term in input_tokenized)
        results.append((index, result))

    results.sort(key=lambda x: (-x[1], x[0]))
    return results

def query_like_model(q, inputed_documents):
    freq_term, freq_context = freq_of_terms(inputed_documents)
    results = get_q_like(inputed_documents, q, freq_term, freq_context)
    output = [res_index for res_index, i in results]
    print(output)

def main():
    docs = int(input())
    inputed_documents =  [input() for _ in range(docs)]
    q = input()

    query_like_model(q, inputed_documents)

if __name__ == "__main__":
    main()

