# Modularization Blueprint: Separating markup, styling, and logic

This document provides a precise, step-by-step architectural blueprint to separate the monolithic `index.html` into a clean, modern three-layer structure:
1. **`index.html`** (Structural markup only)
2. **`style.css`** (Design and presentation styles)
3. **`script.js`** (Interactive behavior, pagination, rendering engines, and data stores)

By separating these concerns, we improve readability, make maintenance easier, and prepare the site for scalability, all while keeping the critical content data arrays 100% intact.

---

## 📂 Proposed File Structure

After the separation, your project root directory will look like this:
```
MySite/
├── index.html       # Cleaned HTML page templates & page divisions
├── style.css        # Extracted site-wide CSS styles & animations
├── script.js        # Core interaction logic & data arrays (nodes, modalData, etc.)
└── Images/          # Asset directory (retained)
```

---

## 1. Extracting CSS to `style.css`

Create a new file named `style.css` in the project root directory.

### ✂️ What to extract from `index.html`
Move the entire contents located inside the `<style>` tags (originally from line 11 to line 187) into `style.css`. Do **not** include the `<style>` and `</style>` tags in your CSS file.

### 📝 Content of `style.css`
The file should begin with the reset rules and CSS variables, followed by component classes, media queries, and animations:

```css
*, *::before, *::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

body {
  background: #0F172A;
  color: #E2E8F0;
  font-family: 'DM Sans', sans-serif;
  min-height: 100vh;
  overflow-x: hidden;
}

:root {
  --blue: #3B82F6;
  --blue-dim: #1D4ED8;
  --blue-glow: rgba(59, 130, 246, 0.15);
  --surface: #1E293B;
  --surface2: #263244;
  --border: rgba(148, 163, 184, 0.12);
  --muted: #64748B;
  --text: #E2E8F0;
  --mono: 'IBM Plex Mono', monospace;
}

/* ... include all NAV, PAGE SYSTEM, HERO, ABOUT, JOURNEY, FOOTER, ANIMATIONS, BLOG, and MODAL styles ... */
/* ... include all media queries (@media(max-width:900px), @media(max-width:640px), @media(max-width:380px)) ... */
```

---

## 2. Extracting JS & Data to `script.js`

Create a new file named `script.js` in the project root directory.

### ✂️ What to extract from `index.html`
Move the entire contents located inside the `<script>` tags (originally from line 443 to line 951) into `script.js`. Do **not** include the `<script>` and `</script>` tags in your JavaScript file.

### ⚠️ Crucial: Keep Data Arrays Intact
Make sure the following data structures are moved exactly as they are defined, preserving every field, object, and array entry:

1. **`nodes`** (Career milestones for Foundations, Systems, Intelligence, and Current Focus)
2. **`modalData`** (Interactive Systems Tree layer descriptions)
3. **`blogPosts`** (Articles, writeups, and sections under the Exploration tab)
4. **`demoPosts`** (Technical Edge AI project walk-throughs)

### 💡 Optimization Note (Fixing Implicit Global)
In the original `index.html`, the variable `activeNode` was used dynamically but never explicitly declared with `let`, `const`, or `var` in the global scope (making it an implicit global). 
> [!TIP]
> To enforce clean code practices, declare `activeNode` explicitly at the top of your `script.js` file:
> ```javascript
> let activeNode = 0; // Explicitly initialized to index 0 (Foundations)
> ```

### 📝 Structure of `script.js`
Your JS file should follow this logical layout:

```javascript
// ─── STATE & GLOBAL VARIABLES ──────────────────────────────────────────────
let activeNode = 0; // Explicit declaration (recommended optimization)
const BLOGS_PER_PAGE = 6;
let currentBlogPage = 1;
let currentDemoPage = 1;
let selectedCategoryFilter = null;
let selectedDemoCategoryFilter = null;
let currentSortOrder = "newest";
let currentDemoSortOrder = "newest";

// ─── DATA ARRAYS (PRESERVED INTACT) ──────────────────────────────────────────
const nodes = [
  {
    badge: "BTech · ECE",
    heading: "Foundations",
    desc: "Where it all began — understanding the physical layer of computation...",
    connector: { icon: "⬡", label: "Connects to Systems", text: "..." },
    cards: [ ... ]
  },
  // ... rest of the node elements
];

const modalData = {
  Matter: { title: "Matter", description: "...", explores: [ ... ] },
  // ... rest of the modal categories
};

const blogPosts = [
  {
    id: "chemistry-intelligence-part1",
    category: "Matter",
    series: "The Chemistry of Intelligence",
    part: 1,
    title: "Part 1 — Why Silicon?",
    // ... all sections and closing paragraphs
  },
  // ... rest of the blog posts
];

const demoPosts = [
  {
    id: "edge-ai-uno-mpu6050",
    category: "Intelligence",
    series: "Edge AI Prototypes",
    title: "Intelligence Under Constraint",
    // ... all sections and code blocks
  }
];

// ─── INTERACTION & RENDER FUNCTIONS ─────────────────────────────────────────
function showPage(page) { ... }
function openModal(nodeKey) { ... }
function closeModal(event) { ... }
function filterLayerRoute(category, targetPage) { ... }
function clearBlogFilter() { ... }
function clearDemoFilter() { ... }
function clearBlogFilterAndGoHome() { ... }
function clearDemoFilterAndGoHome() { ... }
function handleSortChange(type) { ... }
function renderBlogs(page) { ... }
function renderDemos(page) { ... }
function renderPagination(totalPages, type) { ... }
function openItem(id, type) { ... }
function renderJourney() { ... }
function setNode(i) { activeNode = i; renderJourney(); }
function submitFeedback() { ... }
function escHtml(str) { ... }

// ─── INITIALIZATION ──────────────────────────────────────────────────────────
renderBlogs(1);
renderDemos(1);
```

---

## 3. Updating `index.html`

Once the stylesheet and script files have been created, update your main `index.html` file to remove the inline elements and reference the external files instead.

### ➕ Include the External Stylesheet
In the `<head>` block, remove the `<style>...</style>` block and link to `style.css` directly below the Google Fonts links:

```html
  <!-- Google Fonts Connections -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Syne:wght=600;700;800&family=DM+Sans:wght=300;400;500&family=IBM+Plex+Mono:wght=400;500&display=swap" rel="stylesheet" />
  
  <!-- External Premium Stylesheet -->
  <link rel="stylesheet" href="style.css" />
</head>
```

### ➕ Include the External Script
At the bottom of the `<body>`, remove the `<script>...</script>` block entirely and link to your external JavaScript file just before the closing `</body>` tag:

```html
  <!-- External Behavior and Logic -->
  <script src="script.js"></script>
</body>
</html>
```

---

## 4. Verification Checklist

After performing the separation, verify that the application remains fully functional:
* [ ] Open `index.html` in a web browser and check that all styling looks identical to the original version.
* [ ] Verify that clicking the navigation links (Home, Exploration, Demonstration, About, Contact) transitions pages correctly.
* [ ] Open the **Explorations** and **Demos** tabs to check if `blogPosts` and `demoPosts` render perfectly with correct pagination.
* [ ] Open the **Interactive Career Journey** under the "About" or "Journey" view and ensure clicking Foundations, Systems, Intelligence, or Current Focus updates the cards and descriptions without console errors.
* [ ] Open the browser developer console (F12) to ensure there are no `ReferenceError` or `SyntaxError` logs.
