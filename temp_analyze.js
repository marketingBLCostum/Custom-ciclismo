const fs = require('fs');
const path = require('path');
const base = 'c:\\LORENZO\\5 SPORT PER SITO CUSTOM\\CICLISMO - Copia';

function getAllHtmlFiles(dir) {
  let results = [];
  const list = fs.readdirSync(dir);
  for (const file of list) {
    const fullPath = path.join(dir, file);
    const stat = fs.statSync(fullPath);
    if (stat.isDirectory()) {
      results = results.concat(getAllHtmlFiles(fullPath));
    } else if (file.endsWith('.html')) {
      results.push(fullPath);
    }
  }
  return results;
}

const htmlFiles = getAllHtmlFiles(base);
const missingImages = [];
const missingLinks = [];
const srcRegex = /src\s*=\s*"([^"]+)"/gi;
const hrefRegex = /href\s*=\s*"([^"]+)"/gi;

for (const htmlFile of htmlFiles) {
  const content = fs.readFileSync(htmlFile, 'utf-8');
  const relDir = path.dirname(htmlFile);

  let match;
  while ((match = srcRegex.exec(content)) !== null) {
    const src = match[1];
    if (/^https?:\/\//.test(src) || /^\/\//.test(src) || /^mailto:/.test(src) || /^tel:/.test(src) || /^#/.test(src)) continue;
    const fullPath = path.resolve(relDir, src);
    if (!fs.existsSync(fullPath)) {
      missingImages.push({ file: htmlFile, src: src, resolved: fullPath });
    }
  }

  while ((match = hrefRegex.exec(content)) !== null) {
    const href = match[1];
    if (/^https?:\/\//.test(href) || /^\/\//.test(href) || /^mailto:/.test(href) || /^tel:/.test(href) || /^#/.test(href) || /^javascript:/.test(href)) continue;
    const fullPath = path.resolve(relDir, href);
    if (!fs.existsSync(fullPath)) {
      missingLinks.push({ file: htmlFile, href: href, resolved: fullPath });
    }
  }
}

console.log('=== MISSING IMAGES ===');
for (const m of missingImages) {
  console.log(m.file + ' -> ' + m.src + ' (resolved: ' + m.resolved + ')');
}

console.log('\n=== MISSING LINKS ===');
for (const m of missingLinks) {
  console.log(m.file + ' -> ' + m.href + ' (resolved: ' + m.resolved + ')');
}

console.log('\nTotal HTML files: ' + htmlFiles.length);
console.log('Total missing images: ' + missingImages.length);
console.log('Total missing links: ' + missingLinks.length);
