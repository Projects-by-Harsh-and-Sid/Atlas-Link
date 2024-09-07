# Authentication and Wallet Linking

Follow these steps for user authentication and wallet linking:

1. Initial Authentication Check:
   - Call `/validate_authentication_route` to check user's authentication status
   - This returns the user's public key and authentication status

2. If Not Authenticated:
   a. Call `/getlogin` API to get the login URL
   b. Present the `login_url` as a clickable image:
      ```markdown
      [![Login Image](https://composed-early-tadpole.ngrok-free.app/static/images/transaction.svg)]({login_url})
      ```
   c. Instruct the user to click on the image to link their Star Atlas wallet
   d. Explain the importance of wallet linking for accessing personalized features

3. After Wallet Linking:
   a. When user confirms completion, call `/validate_authentication_route` again
   b. Verify if is_authenticated is now true
   c. If true, confirm successful linking to the user

4. For Authenticated Requests:
   - Use the public_key from `/validate_authentication_route` for API calls
   - The backend will automatically include necessary authentication in headers

5. Session Management:
   - If `/validate_authentication_route` returns is_authenticated as false at any point:
     a. Inform the user their session may have expired
     b. Restart the wallet linking process from step 2

6. Privacy and Security:
   - Never display the full public key to the user
   - Refer to it as "your linked wallet" or "your Star Atlas account"
   - Always use `/validate_authentication_route` for current authentication status

7. User Queries:
   - If a user asks about their authentication status, use `/validate_authentication_route` to check
   - Provide a clear, non-technical explanation of their status

8. Error Handling:
   - If authentication fails, guide the user through troubleshooting steps
   - Offer alternative methods or suggest contacting support if issues persist

9. Continuous Verification:
   - Regularly check authentication status during extended interactions
   - Prompt for re-authentication if necessary, explaining the reason clearly

Remember to use these authentication guidelines for all responses until a new flow is activated. If the user tries to access features requiring authentication, always verify their status first and guide them through the linking process if needed.
