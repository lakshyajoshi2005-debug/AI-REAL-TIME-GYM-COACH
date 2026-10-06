from services.config.workout_config import PROMPT


class LLMCoach:
    def __init__(self, groq_client):
        self.client = groq_client
        # Groq client ko self.client mein store kar diya.
        # Ab baaki methods is client ko use kar sakte hain.

        self.history = []    # saves responses in order to improve model responses.
        self.system_prompt = PROMPT

    def give_feedback(self, event, issue):
        prompt = f"Event: {event}"

        if issue:
            prompt += f"\nIssue: {issue}"

        messages = [
            {"role": "system", "content": self.system_prompt},
            *self.history[-10:],    # gives last 10 array variable values like negative feedback .  
            {"role": "user", "content": prompt},
        ]

        # Groq API ko request bhej rahe hain.
        # Yahin actual LLM call ho raha hai.
        response = self.client.chat.completions.create(   #passing messages to client
            model="openai/gpt-oss-120b",
            messages=messages,
            temperature=0.4,    # 0 -1 1 means llm will use new words . 
        )

        text = response.choices[0].message.content.strip()

        self.history.append({"role": "user", "content": prompt})
        self.history.append({"role": "assistant", "content": text})

        return text