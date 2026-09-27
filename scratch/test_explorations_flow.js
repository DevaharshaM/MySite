const fs = require('fs');

// Read explorations/index.html
const html = fs.readFileSync('explorations/index.html', 'utf8');

// Check static HTML before JS runs
console.log('=== TEST A: STATIC HTML INSPECTION (BEFORE JS) ===');
const blogListMatch = html.match(/<div id="blogList"[^>]*>([\s\S]*?)<\/div>/);
if (!blogListMatch) {
  console.error('[FAIL] Could not find #blogList in explorations/index.html');
  process.exit(1);
}

const blogListContent = blogListMatch[1].trim();
if (blogListContent.length === 0) {
  console.error('[FAIL] #blogList is EMPTY in explorations/index.html!');
  process.exit(1);
}
console.log('[PASS] #blogList is NOT empty. Length:', blogListContent.length);

const cardMatches = [...blogListContent.matchAll(/<a href="([^"]+)" class="blog-card"[^>]*>([\s\S]*?)<\/a>/g)];
console.log(`[PASS] Found ${cardMatches.length} pre-rendered cards in #blogList.`);

cardMatches.forEach((card, idx) => {
  const href = card[1];
  const body = card[2];
  const titleMatch = body.match(/class="blog-title"[^>]*>([^<]+)<\//);
  const subtitleMatch = body.match(/class="blog-subtitle"[^>]*>([^<]+)<\//);
  const dateMatch = body.match(/<span>([^<]+)<\/span>/);
  const tagsMatch = [...body.matchAll(/class="tag"[^>]*>([^<]+)<\/span>/g)].map(m => m[1]);

  console.log(`  Card ${idx + 1}:`);
  console.log(`    Title: ${titleMatch ? titleMatch[1] : 'MISSING'}`);
  console.log(`    Subtitle: ${subtitleMatch ? subtitleMatch[1] : 'MISSING'}`);
  console.log(`    Date: ${dateMatch ? dateMatch[1] : 'MISSING'}`);
  console.log(`    Tags: [${tagsMatch.join(', ')}]`);
  console.log(`    href: ${href}`);
});

