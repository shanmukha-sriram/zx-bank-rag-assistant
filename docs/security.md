# Security Considerations

## Logging
* **Raw Query Logging:** Unredacted user queries are logged to stdout to assist during local development and debugging. In a production environment, user queries should be sanitized, masked, or hashed to prevent logging PII or sensitive banking information.