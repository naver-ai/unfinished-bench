# Website updates

**Owner:** Marketing & product management  
**Last edited by:** Thabo Cruz (Product Manager)

## Scope

This covers content in the CMS for the public website: product pages (MC, DU, TX series, laser encoders), news items, and the calibration lab service pages. German and English versions are maintained in parallel. The intranet is not part of this document.

## Who maintains what

| Area | Maintainer |
|---|---|
| Product pages (specs, datasheets, images) | Product Managers (Sonja, Paloma, Thabo) per product line |
| News items and press releases | Press office (Grainne Walsh's team) |
| Calibration lab pages | Test lab team, coordinated through Paloma |
| Site structure, navigation, legal pages | Hana Costa's team |
| Image assets and downloads | Marketing & product management, shared drive folder |

## Content updates

1. Log in to the CMS with your Kessendorf account (single sign-on via the intranet).
2. Navigate to the page tree. Product pages are under **Products > [Series]** ; news items are under **News**.
3. Make your edits in the German version first, then switch the language tab and update the English version. The CMS shows a warning if one language is out of sync — do not publish until both are current.
4. For product pages:
   - Update the technical data table from the PLM export. Check units (N·m, kN, µm) against the German original.
   - Product images must be 1200×800 px minimum, JPEG or WebP, under 400 KB. Upload via the media library, not by pasting into the editor.
   - The "Downloads" section links to the current datasheet PDF in the shared drive. Link to the PDF, do not upload a copy into the CMS.
5. For news items:
   - Title in both languages, body text in both languages. The CMS has a field for the German teaser and the English teaser separately.
   - Publication date is set automatically when you publish; do not backdate.
   - Attach the image as a 16:9 crop. If you do not have an image, leave the field empty — the site will show the default header.
6. Preview the page in both languages using the preview button. Check the rendered page on a phone-width viewport as well.
7. Publish using the **Publish** button. The site updates immediately; there is no staging environment.

## Image and file guidelines

- All images must be licensed for web use. The shared drive folder `_assets_web` contains approved images; use those where possible.
- The press photo archive is for press use; for product pages, take images from `_assets_web`.
- File names: lowercase, no spaces, series and revision included (`tx-900-cover-r3.jpg`).
- Videos (if any) must be hosted on the company video platform; embed via the CMS media block. Do not upload raw video files.

## If it goes wrong

- Published a wrong version? Use the **Revisions** tab on the page to restore the previous revision, then republish.
- Page shows broken layout or missing images? Check the media library first — the asset may have been moved or renamed. If the image is missing from the library, re-upload from the shared drive.
- English and German pages look different in a way you did not intend? Check the language tabs — you may have edited only one. The CMS shows a yellow banner on the page tree when languages are out of sync.
- CMS itself is unresponsive or throws an error? Screenshot it, note the page path, and raise a ticket via the service desk portal. Do not attempt to edit the CMS database directly.
- Link to a datasheet is broken? The PDF may have been replaced in the shared drive. Check the file name in the PLM and update the link.
- Anything looks off on the live site that you cannot explain? Contact Hana Costa's team before publishing further changes.
