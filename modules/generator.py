from huggingface_hub import InferenceClient
class PoemGenerator:
    def __init__(self, db_manager, client):
        self.db_manager = db_manager
        self.client = InferenceClient("mistralai/Mixtral-8x7B-Instruct-v0.1")

    def format_prompt(self, theme, nb_syllabes, style, message):
        prompt = f"Create a poem in French on the theme {theme}, preferably in {nb_syllabes} syllables. In the style of the poet {style}. It should end with a dot.  <s> [INST] {message} [/INST]"
        return prompt

    def generate_poem(self, theme, syl, style, temperature=0.9, max_new_tokens=256, top_p=0.95, repetition_penalty=1.0):
        temperature = float(temperature)
        if temperature < 1e-2:
            temperature = 1e-2
        top_p = float(top_p)

        generate_kwargs = dict(
            temperature=temperature,
            max_new_tokens=max_new_tokens,
            top_p=top_p,
            repetition_penalty=repetition_penalty,
            do_sample=True,
            seed=42,
        )

        formatted_prompt = self.format_prompt(theme, syl, style, message="your_message_here")
        stream = self.client.text_generation(
            formatted_prompt,
            **generate_kwargs,
            stream=True,
            details=True,
            return_full_text=False
        )

        output = ""
        for response in stream:
            output += response.token.text

        return output
