# Google API Authentication on Render (Headless)

Because Render is a headless environment, the default `run_local_server()` flow for Google OAuth will not work.

## Recommended Approach: Token Persistence

1.  **Run Locally First**: Run the application on your local machine.
2.  **Authenticate**: Complete the OAuth flow in your browser.
3.  **Find `token.json`**: The app will generate a `token.json` (or similar) file.
4.  **Base64 Encode**: Encode the contents of your `token.json` to a Base64 string.
    ```bash
    base64 -i token.json
    ```
5.  **Add Secret**: Create an environment variable on Render called `GOOGLE_TOKEN_BASE64` and paste the string.
6.  **Update Code**: Modify your MCP servers to read from this environment variable if the file is missing.

## Alternative: Service Account

1.  Go to [Google Cloud Console](https://console.cloud.google.com/).
2.  Create a **Service Account**.
3.  Download the JSON key.
4.  Add the JSON content as a Secret File on Render named `service_account.json`.
5.  Update `gmail_server.py` to use `service_account.from_json_keyfile_name()`.

> [!NOTE]
> Service accounts cannot easily "act as" a regular user unless Domain-Wide Delegation is set up (Workspace only). For personal Gmail, the Token Persistence method is usually easier.
