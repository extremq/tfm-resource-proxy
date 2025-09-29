# Transformice resources proxy
This is a proxy for downloading any assets from `transformice.com/*`. 
Used for [extremq/tfm-browser](https://github.com/extremq/tfm-browser) so you don't need to run a server.

Use `Transformice-Url: /example-file.ext` as a header to get a resource. Example:

```bash
curl -H "Transformice-Url: /img/i1.jpg"  https://tfm-resource-proxy.vercel.app/api/proxy --output img.jpg
```

Made for easy deployment to vercel.

