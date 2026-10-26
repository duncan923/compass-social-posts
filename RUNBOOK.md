# Monday content pack runbook

The Monday scheduled task follows this file. It builds 14 posts for Tuesday to Monday, gets Dunc's approval in chat, then schedules everything in Buffer with no further action from him.

## 1. Gather (read only)

- Context files: Compass Estates folder `Claude Context` (about-me.md, my-voice.md, my-rules.md, brand.md, market-context.md).
- Live stock: HubSpot deals in stage Live (5436543209) and Under Offer (5667338443). Cross-check against compass-estates.co.uk listings. If the two disagree, use the website and flag the mismatch on the approval page.
- Home Report values: the HubSpot deal property `home_report_value`.
- Previous angles: the last 8 weeks of `weeks/*/week.json` in this repo, plus the Facebook weekly log.md. Never repeat a hook, headline or angle.
- Photos:
  - Property photos: the Listings Marketing Materials folder on Dunc's computer, one subfolder per property.
  - Generic seller photos: the same folder.
  - Stage only the files you need into the container.
- Design system: artifact https://claude.ai/artifact/UGEgL5GU7yFyC9uvD3gXPz.
  - Read `project/README.md`, `templates/social-templates/SocialTemplates.dc.html` and `assets/*`.
  - Fetch `fonts/IvarSoft-Medium.otf` from that artifact. It is licensed, so never commit it here.
- Open fonts: `npm pack @fontsource/instrument-sans@5.1.0 @fontsource/cormorant-garamond@5.1.0`, then untar each into `$CS_FONTS/fontsource-<name>-5.1.0`.

## 2. Plan the week

- 14 posts: 2 a day at 08:00 and 13:00 UK time, Tuesday to Monday.
- Every live property appears at least once.
- Seller posts:
  - At least 1 valuation promotion.
  - Seller tips (Scottish process explainers).
  - Proof posts covering price, marketing, speed and reviews.
  - Brand posts.
- Hard rules:
  - Never state a price against the Home Report value unless the price is BELOW it.
  - No "homes sold" volume claims.
  - No award claims (the award belonged to the Compass group, not Dunc personally).
  - Every seller post needs a strong photo plus extra info: a 3-column gold strip of facts or figures.
  - Never invent features. Use only facts from the listing, HubSpot or Dunc.
  - Scottish terms only: settle, take entry, closing date, missives, Home Report, LBTT. Never completes, completion, conveyancer or stamp duty.
  - The CGI kitchen for 7 Moat Drive must be labelled CGI.

## 3. Build

1. Write `posts.py` for the week. Copy `tools/example-week/posts.py` for the schema. Template keys are T1 (listing), SELLER, REVIEW2 and STAT.
2. Set the environment variables:
   ```
   export CS_WEEK=<work dir with posts.py>
   export CS_DS=<design system project dir>
   export CS_FONTS=<fonts dir>
   export CS_PHOTOS=<staged property photos dir>
   export CS_STOCK=<staged generic photos dir>
   export CS_TITLE="Compass Week NN Posts"
   ```
3. Run the scripts:
   ```
   python3 tools/captions.py   # must print "ok" for every post. Fix any QC issue it reports
   python3 tools/render.py     # writes 1080x1350 PNGs to $CS_WEEK/out
   ```
4. Convert each PNG to `post-NN.jpg` at quality 90 in `$CS_WEEK/site/posts/`.
5. Run `python3 tools/page.py` and publish `$CS_WEEK/site/index.html` as an artifact. Look at every image before publishing.

Caption rules (design system section 8.3):

- Order: hook, body, buyer CTA, listing URL, council tax band, seller line, max 3 hashtags.
- No emoji, no exclamation marks, no em dashes. Never write "D&G".
- Facebook valuation link: `duncanure.co.uk/valuation?utm_source=facebook`.
- Instagram: say "link in bio".

## 4. Approval

Send Dunc the approval page link and stop. Make changes he asks for, then re-render and republish. Do nothing in Buffer until he replies "approved" (or "approve all").

## 5. Publish (after approval only)

1. Copy the JPGs and `week.json` to `weeks/<Tuesday date>/` in this repo.
2. Commit and push to `main`.
3. Image URLs follow this pattern: `https://raw.githubusercontent.com/duncan923/compass-social-posts/main/weeks/<date>/post-NN.jpg`. Check that each returns HTTP 200 before scheduling.
4. Create the Buffer posts:
   - Organisation 5f4fbe48d5b15e05cd4d6783. Facebook channel 68347a369c617476ae07cc30. Instagram channel 68347ee39c617476ae53daa6.
   - Settings: `schedulingType: automatic`, `mode: customScheduled`, `dueAt` with the correct UK offset (+00:00 in GMT, +01:00 in BST).
   - Facebook metadata: `{"facebook":{"type":"post"}}`
   - Instagram metadata: `{"instagram":{"type":"post","shouldShareToFeed":true}}`
5. Before creating anything, query the scheduled posts for the week and skip any slot that already has a post on that channel. This stops duplicates if a run is retried.
6. Verify the result: exactly 14 Facebook and 14 Instagram posts at the planned times.
7. Report back in one line.

Never publish now, delete posts or send messages without Dunc's explicit instruction.
