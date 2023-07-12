import openai

###########################################################

class ChatSession:
    def __init__(self,
                 model="gpt-3.5-turbo",
                 n=1,
                 max_tokens=1000,
                 temperature=1,
                 top_p=1,
                 stop=None,
                 stream=True):
        self.model = model
        self.messages = []
        self.n = n
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.stop = stop
        self.stream = stream

    def add(self, role, content):
        self.messages.append({
            "role": role,
            "content": content
        })

    def submit(self):

        resp = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
            n=self.n,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            top_p=self.top_p,
            stop=self.stop,
            stream=self.stream
        )

        content = []
        if not self.stream:
            resp = [resp]
        
        for r in resp:
            if self.stream:
                output = r['choices'][0]['delta']
            else:
                output = r['choices'][0]['message']

            if "content" in output:
                content.append(output["content"])
        
        asst = ''.join([m for m in content])

        self.messages.append({
            "role": "assistant",
            "content": asst
        })

        return asst
