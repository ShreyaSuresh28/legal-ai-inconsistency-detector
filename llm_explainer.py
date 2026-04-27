from groq import Groq

client = Groq(api_key="YOUR_GROQ_API_KEY")

def explain_issue(row):
    prompt = f"""
Explain HR/legal issue:

Data:
{row.to_dict()}

Issues:
{row.get('Issues')}

Give:
- Explanation
- Risk level
- Fix
"""

    res = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content
