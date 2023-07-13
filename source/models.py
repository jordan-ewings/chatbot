import openai
import re
from markupsafe import Markup

###########################################################

# content = "Certainly! Here's a simple Python function that generates a random number using the `random` module:\n```python\nimport random\n\ndef generate_random_number():\n    return random.randint(1, 100)\n```\nIn this example, the `random.randint()` function generates a random integer between 1 and 100 (you can adjust the range based on your needs). You can call `generate_random_number()` to get a random number."
# content = "Certainly! Here's a Python function that generates a random number:\n\n```python\nimport random\n\ndef generate_random_number():\n    return random.randint(1, 100)\n```\n\nExplanation:\n- The `import random` statement allows us to use the functions provided by the built-in random module in Python.\n- The `generate_random_number` function is defined with no additional parameters.\n- The `random.randint(1, 100)` function call returns a random integer between 1 and 100 (inclusive). You can modify the range as per your requirements.\n\nUsage:\nYou can call the `generate_random_number()` function wherever you need to generate a random number. For example:\n\n```python\nrandom_number = generate_random_number()\nprint(random_number)\n```\n\nThis will print a random number between 1 and 100 each time the function is called."
# clean = re.sub("\\n```(.*?)\\n```\\n", r"_CODEBLOCK_CBSTART_<pre><code>\1</code></pre>_CODEBLOCK_", content, flags=re.DOTALL)
# clean_spl = clean.split("_CODEBLOCK_")
# clean_spl2 = []
# for i in clean_spl:
#     if re.findall("^CBSTART_", i):
#         j = re.sub("^CBSTART_", "", i)
#     else:
#         j = re.sub("\\n", "<br>", i)
#     clean_spl2.append("<p>"+j+"</p>")


# re.split('(\\n)```', content)

# htmlcode = re.sub("\n```(.+)```\n", r"</p><br><pre><code>###\0</code></pre><br><p>", content)
# re.finditer("```", content)


def content_web(content):
    # clean = re.sub("\\n```(.+?)\\n```\\n", r"_CODEBLOCK_CBSTART_<pre><code>\1</code></pre>_CODEBLOCK_", content, flags=re.DOTALL)
    clean = re.sub("\\n```(.+?)\\n```\\n", r"_CODEBLOCK_CBSTART_\1_CODEBLOCK_", content, flags=re.DOTALL)
    clean_spl = clean.split("_CODEBLOCK_")
    clean_spl2 = []
    for i in clean_spl:
        if re.findall("^CBSTART_", i):
            j = Markup.escape(i)
            j = re.sub("^CBSTART_", "", j)
            j = "<pre><code>"+j+"</code></pre>"
            j = Markup(j)
        else:
            j = Markup.escape(i)
            j = re.sub("\\n", "<br>", j)
            j = "<p>"+j+"</p>"
            j = Markup(j)

        clean_spl2.append(j)
    
    clean_web = ''.join([m for m in clean_spl2])
    return Markup(clean_web)

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
            "content": content,
            "content_web": content_web(content)
        })
    

    def submit(self):

        messages_use = []
        for i in self.messages:
            messages_use.append({
                "role": i.get("role"),
                "content": i.get("content")
            })

        resp = openai.ChatCompletion.create(
            model=self.model,
            messages=messages_use,
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
        self.add("assistant", asst)

