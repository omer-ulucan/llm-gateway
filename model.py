from llama_cpp import Llama

_llm = None

def get_model():
    global _llm
    if _llm is None:
        _llm = Llama.from_pretrained(
            repo_id="bartowski/Qwen_Qwen3.5-2B-GGUF",
            filename="Qwen_Qwen3.5-2B-Q4_K_M.gguf",
            verbose=False,
            n_ctx=8192,
            chat_format="chatml",
        )
    
    return _llm