def build_prompt(changes_text):

    return f"""
You are analyzing updates in product documentation.

You are given section-wise differences between
OLD and NEW versions of a documentation article.

TASK:
1. Identify the change:
    - Compare the NEW article sections against the OLD article sections and identify What changed.
    - For example, in the new article sections there might be additional information or some information might be removed compared to the old article sections. Identify these changes.

2. Summarize what changed in the NEW article.
   - Provide a detailed human-readable summary explaining what has changed in the new article.
   - While summarizing the changed, explain the change made to the article in a way that a user can easily understand the difference between the old and new article.
   - Do Not explain the changes section wise.

OUTPUT FORMAT (STRICT):
A detailed summary of What has changed in the new article.
Do not include any other information in the output except the summary of what has changed.
Do not give any heading to the output.


RULES:
- Be concise
- Do not repeat raw OLD/NEW lines
- Do not mention sections unless important
- Focus only on meaningful changes

SECTION DIFFERENCES:

{changes_text}
"""