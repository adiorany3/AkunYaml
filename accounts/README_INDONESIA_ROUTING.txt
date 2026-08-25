Indonesia Routing Policy v4.3

Purpose:
- Keep Indonesian exit nodes for applications requiring Indonesia region.
- Preserve global nodes for normal browsing.

Detection rule:
1. Resolve node endpoint.
2. GeoIP country check.
3. Validate latency.
4. Put matching nodes into indonesia_nodes.yaml.

Do not rely only on server name because many VPS use misleading labels.
