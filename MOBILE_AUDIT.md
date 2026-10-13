# Mobile review — 2026-10-13

## Coverage

Reviewed all 32 captured routes in the local browser at 320, 390, 480, 600, 768, 820, and 1024 CSS-pixel viewport widths. Representative pages were also inspected visually after Webflow's entrance animations settled: Home, About, Work, Hire, Blog, Privacy, a long article, a category, a project, and the link page.

## Changes

- Removed horizontal scrolling caused by testimonial cards, long URLs and article text, oversized hero headings at the 480–820px transition, and two template sections sized to the full viewport including the scrollbar.
- Scaled long article titles and intermediate-width hero headings so they wrap as words within the screen.
- Stacked About's text and photos through the tablet portrait breakpoint to prevent the copy from sitting over photos.
- Kept testimonial text within its cards and preserved full-width Work form fields with 16px input text.
- Enlarged mobile menu controls to at least 48px high, added keyboard operation and expanded state to the main menu, and kept focus visible.
- Improved contrast of the alternate template logo and empty-category message on dark pages.

## Readback

- No horizontal overflow on the 32 routes at the reviewed widths after the animations settle. The 1024px template sections were checked again after their width fix.
- The main mobile menu opens with Enter and closes with Escape; its expanded state updates. The Work inputs remain 50px high with 16px text.
- The long article title fits at 320px without splitting words in the middle, and the image begins within the first screen.

The source Hire appointment embed still reports “Appointment not found.” Several source template and category pages still contain placeholder content; this review only addresses their mobile layout and legibility.

References: [WCAG 2.2 Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html), [web.dev accessible tap targets](https://web.dev/articles/accessible-tap-targets).
