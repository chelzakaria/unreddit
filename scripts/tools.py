from tqdm import tqdm
import fasttext

fasttext_model = fasttext.load_model("../lid.176.bin")


def detect_language(docs: list) -> dict:
    """
    Detects the language of the documents using fasttext model
    Args:
        docs: list of documents
    Returns:
        dict: dictionary of documents and their corresponding language
    """
    _dict = {}
    for doc in tqdm(docs):
        try:
            _dict[doc] = fasttext_model.predict(doc.replace("\n", " "))
        except:
            _dict[doc] = None
    return _dict


def get_language_ratio(docs: dict, threshold: float = 0.0) -> dict:
    """
    Get the ratio of languages in the documents
    Args:
        docs: dictionary of documents and their corresponding language
    Returns:
        dict: dictionary of languages and their corresponding ratio
    """
    languages = {}
    for _, doc in docs.items():
        if doc[0] in languages:
            languages[doc[0]] += 1
        else:
            languages[doc[0]] = 1

    for lang in languages:
        languages[lang] = languages[lang] / len(docs)

    # languages = dict(sorted(languages.items(), key=lambda item: item[1], reverse=True))

    return {k: v for k, v in languages.items() if v > threshold}
