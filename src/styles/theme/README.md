# Dark-® theme

Dark-® (Dark-R, written Dark-® in Enterprsr) is the Enterprise-R web theme: the brand palette, type and components as plain CSS.

Dark-® is futuristic with a hint of retro, on a fresh palette you don't often see in everyday interfaces. It is made for night mode and for night-light filters that warm the screen in the evening. Its purples and magentas carry a lot of blue, so Dark-® changes more than most themes when the night light comes on.

The theme targets WCAG 2.2 AA; the website showcase lists the contrast scores.

It needs no framework and no build step. Any page or app can use it with `<link>` tags, in this order. Keep `theme/` and `fonts/` side by side, as in the assets:

```html
<link rel="stylesheet" href="theme/palette.css">
<link rel="stylesheet" href="theme/base.css">
<link rel="stylesheet" href="theme/components.css">
<link rel="stylesheet" href="theme/doc.css">
<script src="theme/rows.js"></script>
<script src="theme/guard.js"></script>
```

`doc.css` is optional: include it only on pages that hold documents. `rows.js` is optional too: include it only on pages that use `.r-rows`. It runs on `DOMContentLoaded` (or immediately if the document is already ready) and enhances every `.r-rows` it finds. To enhance a list added later, call `rRows.enhance(element)` or `rRows.enhanceAll(container)`. `guard.js` is optional: include it once on pages that should guard button clicks. It listens on the document and applies to every `button` and `input` of type button, submit or reset, not to links. Add `.r-unguarded` on a control or an ancestor (for example a nav) to opt out.

## Files

| File | What it is | State |
|---|---|---|
| `palette.css` | The `--ui-*` colour variables, the striped gradient and the separator. Generated from `palette/palette.json`; `build.sh` copies it here in `dist/theme/`. | Shipped |
| `base.css` | Fonts and plain HTML elements: body, headings h1-h6 (a ladder of colours; Audiowide for h1-h3 and Rajdhani uppercase for h4-h6 by default; `--r-font-heading` (h1, and the default for h2-h3), `--r-font-sub` (h2-h3) and `--r-font-minor` (h4-h6) switch each tier), text, lists, quotes, marks, details, figures, tables (rounded outline, header row, row dividers; corner cell radii account for a caption so a filled header stays inside the curve), links, the separator rule, code and keys (Monaspace Neon, `--r-font-mono`), form fields and field groups, radios and checkboxes (Dark-R field look, `--r-choice-*`), progress and meter, dialog, media that scale down, focus ring, text selection. Element selectors sit inside `:where()`, so they weigh nothing and an app's own rules win. Role variables start with `--r-` (text, heading, link, focus, field highlight, choice tokens, font stacks). It loads its fonts from `../fonts/woff2/`, the existing fonts export next to `theme/`. This is the web scale. | Shipped |
| `doc.css` | The document scale, for long text, scoped to `.r-doc`: Audiowide for h1, Rajdhani for h2-h6, Saira for the body (`--r-font-doc`), at most `--r-doc-measure` (68ch) wide. It loads Saira from `../fonts/woff2/`. | Shipped |
| `components.css` | Buttons (`.r-btn`) with the current page (`aria-current="page"`) and the form roles `.r-primary`, `.r-clear` (also any reset button) and `.r-cancel`; no role class is generic. Width and padding are `--r-btn-min`, `--r-btn-pad-x`, `--r-btn-pad-b`, `--r-btn-pad-flat`, `--r-btn-pad-curve` and `--r-btn-tracking`; below `40rem` the min-width and padding scale down, the label stays end-aligned, and curved group ends keep enough inset to clear `--r-pill-r`. Pill groups (`.r-group`, including a single button with both ends curved), dropdown menus (`.r-menu`, `.r-menu-list`, `.r-to-right`), slanted breadcrumbs (`.r-crumbs`, with `.r-crumb-root` for the ® root; crumbs size to their label, `min-width: 0`) and separators (`.r-sep`, `.r-striped`) number columns in tables (`.r-num`), panels and cards (`.r-panel`, `.r-card` with `.r-active` and `.r-selected`), status pills (`.r-pill`), notification boxes (`.r-notice` with `.r-ok`, `.r-warn`, `.r-error`), the terminal panel for text over a picture (`.r-term`), the prompt (`.r-prompt`), the update glow (`.r-glow`, `.r-glow-run`), a brief iridescent border that marks a box that just changed, and the dynamic list (`.r-rows`, with `.r-vh` for its live region). The markup for each is in a comment above its rules. | Shipped |
| `rows.js` | Plain script that enhances any `.r-rows` fieldset: add and remove, keyboard, live-region announcements and `data-name` templates. No dependencies, no build step. | Shipped |
| `guard.js` | Plain script that guards button clicks. After the pointer stops moving, `--r-guard-gap1` (300ms) passes, then clicks are accepted for `--r-guard-gap2` (10s); then they stay off until the pointer moves and stops again. An accepted click turns clicks off for `--r-guard-cool` (400ms), then off until movement again. Touch and keyboard use the cooldown only. Acceptance is decided on button press, not release; a discarded press also suppresses the click. A discarded click flashes the waiting cursor until the button is clickable, or briefly if it cannot become clickable without movement. Opt out with `.r-unguarded` on the button or an ancestor. No dependencies, no build step. | Shipped |
| `icons/` | Waiting icons: `icons/wait.svg` (animated) and `icons/wait-static.svg` (the full W, unanimated, 128). `icons/wait-cursor.svg` is the same W at 32 CSS px for the `.r-wait` cursor (hotspot 16 16, `progress` fallback). Disabled controls use that cursor too, never the system not-allowed pointer. `--r-icon-wait`, `--r-icon-wait-static` and `--r-icon-wait-cursor` in `base.css`. | Shipped |

The showcase of the website, [project-www](https://github.com/enterprise-r/project-www), shows every element and component.


## Typography

Two heading scales share the fonts. Both use Monaspace Neon (`--r-font-mono`) for code.

- **Web** (`base.css`): the default for pages and apps. Audiowide for h1-h3, Rajdhani for h4-h6 and for text.
- **Document** (`doc.css`, inside `.r-doc`): for long text. Audiowide for h1 only, Rajdhani for h2-h6, Saira for the body.

`palette/typography.odt` sets both scales side by side.

## Buttons, pills and choices

On a wide screen `.r-btn` uses `--r-btn-min` (7rem) and even `--r-btn-pad-x` (0.75rem), with the label tucked to the end (`justify-content: flex-end`), so spare width sits on the start side. Below `40rem` those become `--r-btn-min: 4.75rem`, `--r-btn-pad-x: 0.6rem`, `--r-btn-pad-flat: 0.5rem` and `--r-btn-pad-curve: max(var(--r-btn-pad-x), calc(var(--r-pill-r) * 0.7))`, with tracking `--r-btn-tracking: 0.08em`. Height stays `--r-btn-h` (2rem). Breadcrumbs (`.r-crumbs`) do not use the min-width; they size to their label.

Radios and checkboxes share `--r-choice-size` (1.5rem), `--r-choice-bg`, `--r-choice-border`, `--r-choice-checked`, `--r-choice-mark`, `--r-choice-radius` and `--r-choice-dot`. They use the same field look as text inputs (`appearance: none`, Lighter fill, Dark border, the field focus ring). A checked radio draws a sage inner dot; a checked checkbox a sage fill and a dark check; an indeterminate checkbox a sage dash. Forced colours revert to the native control.

## Dynamic list

`.r-rows` is a fieldset of rows with a quiet add/remove control in a left column the size of a radio (`--r-choice-size`). The × and + are Audiowide, in Clear (`--r-clear`); hover turns × red (and that row's field borders, with no ring around the row) and + sage (and shows a reserved ghost row whose fields use `--r-clear`). Include `theme/rows.js` on the page.

```html
<fieldset class="r-rows">
  <legend>Team members</legend>
  <div class="r-rows-head" aria-hidden="true"><span></span><span>Name</span><span>Role</span></div>
  <div class="r-rows-list">
    <div class="r-row">
      <span class="r-row-bubble"><button type="button" class="r-row-remove"><span class="r-row-glyph" aria-hidden="true">×</span></button></span>
      <input data-name="team[{i}][name]" data-label="Name, row {n}" placeholder="Name" autocomplete="off">
      <input data-name="team[{i}][role]" data-label="Role, row {n}" placeholder="Role" autocomplete="off">
    </div>
  </div>
  <div class="r-rows-foot">
    <span class="r-row-bubble"><button type="button" class="r-row-add" aria-label="Add row"><span class="r-row-glyph" aria-hidden="true">+</span></button></span>
    <div class="r-row-ghost" aria-hidden="true">
      <input placeholder="Name" disabled tabindex="-1" aria-hidden="true" autocomplete="off">
      <input placeholder="Role" disabled tabindex="-1" aria-hidden="true" autocomplete="off">
    </div>
  </div>
  <p class="r-rows-live r-vh" aria-live="polite"></p>
</fieldset>
```

- `data-name` and optional `data-id` / `data-label` on each field are templates. `{i}` is the 0-based index, `{n}` the 1-based row number. The script writes `name`, `id` and `aria-label` from them whenever rows change.
- Optional attributes on the fieldset: `data-remove` (default `Remove row {n}`, used for the × button's `aria-label`), `data-added` and `data-removed` (live-region announcements, default `Row added` and `Row removed`).
- Keyboard: Enter in the last row adds a row and focuses its first field. Backspace at the start of an empty row (every field blank, more than one row) removes it and focuses the previous row's last field.
- The last remaining row cannot be removed, and its remove control is hidden. The ghost row is not in the tab order (`disabled`, `tabindex="-1"`, `aria-hidden`). `.r-vh` hides the live region visually. Reduced motion drops the row-in animation; forced colours keep the control edges visible.

## Rules

- Standard CSS only: no preprocessor, no nesting, no framework scoping. Newer features need a fallback for browsers without them.
- Colours come only from `--ui-*` variables. To change a colour, change `palette/palette.json`.
- Every class starts with `r-`, so the theme cannot clash with an app's own classes. Custom properties the theme adds for roles start with `--r-`.
- Site-specific parts (a site's title bar, footer and pages) stay in that site.
