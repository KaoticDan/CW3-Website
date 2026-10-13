# Performance review — 2026-10-13

## Supplied live baseline

The supplied GTmetrix report for `https://cw3-website.vercel.app/` measured a 92% Performance score and 97% Structure score. Its largest contentful paint was 1.5 s, total blocking time was 137 ms, layout shift was 0, and the page transferred 2.47 MB in 51 requests. It highlighted missing image dimensions, image payload, font loading, and JavaScript execution as opportunities.

## Local changes

- Replaced 69 large JPEG/opaque PNG assets with WebP where the result was at least 15% smaller. Across those assets, bytes fell from 7,322,507 to 4,608,900 (37%). Original files remain in `public/assets` for rebuilds and comparison.
- The homepage's unique raster references now total 2,025,294 bytes instead of 2,305,555 bytes, a 280,261 byte reduction before browser loading behavior, caching, or transfer compression.
- Added intrinsic width and height to local raster and SVG image elements so the browser can reserve their aspect ratios before loading. No homepage image is left without both dimensions.
- Removed the WebFont.js loader that downloaded extra Inter, Montserrat, and Urbanist font files. The existing local Inter faces remain, while Gantari remains local in the captured stylesheet. Testimonial and link-page text now use Inter.
- Kept the Webflow interaction script because it drives the source animations and navigation. Removing it would change site behavior.

## Local readback

At 390 CSS px, the Home and Work pages have no broken images or horizontal overflow; the mobile menu opens. The homepage's computed heading and paragraph families are Gantari and Inter. All optimized files and asset references resolve locally.

The changes have not been deployed. A new GTmetrix score requires publishing this version and retesting the production URL; the local byte comparison is not a measured score prediction.
