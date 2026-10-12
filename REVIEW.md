# CW3 review notes

- 32 public routes captured from live navigation and the source sitemap, including Home, Hire, Work, Blog, About, Privacy, four categories, four posts, and linked template/project and utility pages.
- 168 Webflow assets captured by the crawler plus four local Inter font files. All 165 `/assets/` references in generated HTML/CSS resolve to local files.
- Gantari is used for headings; Inter is used for paragraph text.
- The Webflow branding badge, duplicate header hover logo, and footer Author placeholder link are removed from the local copy.
- Local menu animation, navigation, Work form validation, and success/error display logic checked. Every captured route responds locally.
- At a 390 px viewport, every captured route fits without horizontal overflow after two narrow-screen fixes.
- The only source form is on `/work`; its label suggests resume upload, but no upload control exists in the source.
- The source `/hire` Google appointment iframe displays “Appointment not found”.
- Source template copy and placeholder links are retained where no finished content exists. The two obvious footer mislinks for Hire and About are corrected to their existing pages.
- Supabase migration and Vercel environment values are prepared, but no database changes or deployment have occurred.

The supplied recording could not be opened through the available browser interface because local-file navigation was blocked. The live Webflow interactions were checked directly instead.
