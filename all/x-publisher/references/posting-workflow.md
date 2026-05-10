# X Publisher Posting Workflow

Use this workflow when preparing an X post or thread from Codex.

1. Draft the post text first. Put the concrete shipped thing, result, or useful idea in the first sentence.
2. Validate the text locally:

   ```bash
   python scripts/x_publish.py validate --text "Post text" --url "https://example.com"
   ```

3. If the post is too long, tighten the wording before choosing a thread.
4. Generate the composer URL:

   ```bash
   python scripts/x_publish.py intent --text "Post text" --url "https://example.com"
   ```

5. Open the composer only after checking the generated URL:

   ```bash
   python scripts/x_publish.py intent --text "Post text" --url "https://example.com" --open
   ```

6. For long drafts, save the text to a UTF-8 Markdown or text file and run:

   ```bash
   python scripts/x_publish.py thread --file post.md --url "https://example.com"
   ```

The browser composer is the publishing confirmation step. The user must review and click Post manually.

## Notes

- V1 does not post through the API.
- V1 does not need API keys, OAuth credentials, or paid X API access.
- Local character counting is conservative and intended to prevent obvious failures before the composer opens.
