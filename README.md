# CW3 website recreation

Local replica of the public [CW3 Webflow site](https://cw3-v1.webflow.io/), captured on 2026-10-12. The public pages, hierarchy, copy, Webflow interactions, and site assets are retained for review before Vercel deployment.

## Review locally

Run `node dev.mjs` from this folder, then open `http://127.0.0.1:3000`. The preview serves the same clean paths as the source site. The source HTML is in `source/`, the runnable site is in `public/`, and `source/inventory.json` maps each downloaded asset to its public URL.

## Rebuild the capture

Run `python capture.py`, then `python prepare.py`. The first command reads public pages and assets from Webflow; the second produces the reviewable static site and applies the small local fixes.

## Form storage after review

The Work page's original form contains name, email, and phone fields. It does **not** contain a resume upload, despite its “Submit Resume” button label. The local copy submits those fields to `api/work-submission.mjs`; the endpoint reports a configuration error until the following release steps are complete:

1. Apply `supabase/cw3_work_submissions.sql` to project `ykucsvjjynbmwfwvscbf`.
2. Set `SUPABASE_URL` and `SUPABASE_SECRET_KEY` in the CW3 Vercel project. The secret key must remain server-side.
3. Deploy and verify a real submission in `public.cw3_work_submissions`.

The Hire page retains its original Google appointment embed. The source embed currently says “Appointment not found”; its owner must repair the calendar schedule for booking to work.

## Deploy configuration

`vercel.json` configures the `public/` static output and clean URLs. The root `api/` folder holds the Vercel Function for the Work form. Deployment and Supabase setup remain pending.
