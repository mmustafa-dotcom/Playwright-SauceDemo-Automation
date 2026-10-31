import string

import numpy as np


def split_text(text, num_chunks):
    text = text.translate(str.maketrans("", "", string.punctuation))
    words = text.lower().split()
    chunks = np.array_split(words, num_chunks)
    return [" ".join(chunk) for chunk in chunks]


def mapper(chunk):
    return [(word, 1) for word in chunk.split()]


def combiner(mapped_chunk):
    combined = {}

    for word, count in mapped_chunk:
        combined[word] = combined.get(word, 0) + count

    return list(combined.items())


def map_combine(chunk):
    """Mapper + combiner executed together inside the worker process."""
    return combiner(mapper(chunk))


def grouping(combined_chunks):
    grouped = {}

    for chunk in combined_chunks:
        for word, count in chunk:
            if word not in grouped:
                grouped[word] = []
            grouped[word].append(count)

    return grouped


def reducer(grouped):
    reduced = {}

    for word, counts in grouped.items():
        reduced[word] = sum(counts)

    return reduced


if __name__ == "__main__":
    text = (
        "Data science is a new science that is not necesserely "
        "about data, as computer science is not necesserely about computers, "
        "such as mathematical science is not merely about numbers"
    )

    chunks = split_text(text, 3)
    mapped_chunks = [mapper(chunk) for chunk in chunks]
    combined_chunks = [combiner(chunk) for chunk in mapped_chunks]
    grouped = grouping(combined_chunks)
    result = reducer(grouped)

    print("Chunks:", chunks)
    print("Mapped chunks:", mapped_chunks)
    print("Combined chunks:", combined_chunks)
    print("Grouped values:", grouped)
    print("Final result:", result)
