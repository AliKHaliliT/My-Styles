HEADERS_CONTENT = (
"""
# Response Headers

To enhance security, traceability, and performance, all API responses include standardized HTTP headers categorized by their architectural responsibility.

## Observability Headers

These headers aid in debugging, monitoring, and request correlation across distributed systems.

| Header         | Description                                                                                                 |
|----------------|-------------------------------------------------------------------------------------------------------------|
| `x-request-id` | A unique identifier assigned to each request. Useful for tracing logs and correlating client-server events. |

## Security Headers

These headers enforce transport security and protect the client/browser from common web vulnerabilities.

| Header                      | Description                                                                                                 |
|-----------------------------|-------------------------------------------------------------------------------------------------------------|
| `strict-transport-security` | Enforces HTTPS connections to protect data integrity and confidentiality.                                   |
| `x-content-type-options`    | Set to `nosniff` to prevent browsers from MIME-sniffing responses and reduce XSS risks.                     |
| `permissions-policy`        | Controls which features and APIs the browser can access (e.g., geolocation, camera, microphone).            |
| `referrer-policy`           | Controls how much referrer information is sent with requests to enhance user privacy.                        |
| `x-frame-options`           | Prevents the site from being embedded in frames or iframes, mitigating clickjacking attacks.                |
| `x-xss-protection`          | Enables the browser's built-in XSS filter to block reflected XSS attacks.                                   |
| `x-download-options`        | Instructs browsers not to execute downloads in the context of the site, reducing drive-by attacks.          |
| `x-dns-prefetch-control`    | Controls whether the browser is allowed to perform DNS prefetching, reducing navigation pattern leaks.      |

## Isolation Headers

Modern headers designed to provide site isolation, protecting against side-channel attacks and controlling cross-origin interactions.

| Header                         | Description                                                                                                 |
|--------------------------------|-------------------------------------------------------------------------------------------------------------|
| `cross-origin-resource-policy` | Restricts how resources are shared across origins to prevent unauthorized data leaks.                        |
| `cross-origin-opener-policy`   | Ensures top-level documents do not share a browsing context group with cross-origin documents.               |
| `cross-origin-embedder-policy` | Prevents a document from loading cross-origin resources that do not explicitly grant permission.            |
| `origin-agent-cluster`         | Provides a hint to the browser to isolate the origin into its own process for enhanced security.             |

## Cache Control Headers

These headers manage how responses are stored by browsers and intermediary proxies.

| Header                      | Description                                                                                                 |
|-----------------------------|-------------------------------------------------------------------------------------------------------------|
| `cache-control` / `pragma`  | Prevents sensitive API data from being cached in the browser or via intermediary CDNs/caches.               |

"""
)
