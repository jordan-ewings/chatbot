import openai
import re
from markupsafe import Markup

###########################################################


def content_web(content):
    clean = content.replace("\r\n", "\n")
    clean = re.sub("\\n```(.+?)\\n```\\n", r"_CODEBLOCK_CBSTART_\1_CODEBLOCK_", clean, flags=re.DOTALL)
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
            j = re.sub("`(.+?)`", r"<b>`\1`</b>", j)
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

