import tiktoken


def token_counter(prompt: str) -> int:
    encoder = tiktoken.encoding_for_model("gpt-3.5-turbo")
    token_list = encoder.encode(prompt)
    count = len(token_list)
    return count