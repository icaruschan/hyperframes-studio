import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const HTML_PATH = resolve(__dirname, '../index.html');
const html = readFileSync(HTML_PATH, 'utf8');

test('Property 2: Preservation - Out-of-Scope Behavior Unchanged', () => {
  // 1. AUDIO_OFFSET
  assert.match(html, /const AUDIO_OFFSET = -0\.05;/);
  
  // 2. Timeline registration
  assert.match(html, /window\.__timelines\["main"\] = tl;/);
  
  // 3. Caption pop tween
  assert.match(html, /tl\.fromTo\(span,\s*\{\s*scale: 0\.8,\s*opacity: 0,\s*y: 10\s*\},\s*\{\s*scale: 1\.0,\s*opacity: 1,\s*y: 0,\s*duration: 0\.12,\s*\/\*\s*Fast snapping entrance\s*\*\/\s*ease: "back\.out\(1\.5\)"\s*\},\s*popTime\s*\);/m);

  // 4. Caption hide tween
  assert.match(html, /tl\.to\(span, \{\s*opacity: 0,\s*scale: 0\.9,\s*duration: 0\.06,\s*\/\*\s*Instantaneous snap-out\s*\*\/\s*ease: "power2\.in"\s*\}, hideTime\);/m);

  // 5. Caption set hard kill
  assert.match(html, /tl\.set\(span, \{ opacity: 0, visibility: "hidden" \}, hideTime \+ 0\.06\);/);

  // 6. Claude card entrance and exit tweens
  assert.match(html, /tl\.fromTo\("#claude-ui",\s*\{ opacity: 0, y: 60, scale: 0\.8, rotate: -5 \},\s*\{\s*opacity: 1,\s*y: 0,\s*scale: 1,\s*rotate: 0,\s*duration: 0\.8,\s*ease: "back\.out\(1\.2\)"\s*\},\s*Math\.max\(0,\s*.*?\s*\+ AUDIO_OFFSET\)\s*\);/m);
  assert.match(html, /tl\.to\("#claude-ui", \{\s*opacity: 0,\s*y: -40,\s*scale: 0\.9,\s*duration: 0\.4,\s*ease: "power3\.inOut"\s*\}, 3\.5\);/m);

  // 7. Figma card entrance and exit tweens
  assert.match(html, /tl\.fromTo\("#figma-ui",\s*\{ opacity: 0, y: 60, scale: 0\.8, rotate: 5 \},\s*\{\s*opacity: 1,\s*y: 0,\s*scale: 1,\s*rotate: 0,\s*duration: 0\.8,\s*ease: "back\.out\(1\.2\)"\s*\},\s*Math\.max\(0,\s*.*?\s*\+ AUDIO_OFFSET\)\s*\);/m);
  assert.match(html, /tl\.to\("#figma-ui", \{\s*opacity: 0,\s*y: -40,\s*scale: 0\.9,\s*duration: 0\.4,\s*ease: "power3\.inOut"\s*\}, 9\.5\);/m);

  // 8. Video push-ins
  assert.match(html, /tl\.fromTo\(videoEl,\s*\{ scale: 1\.0 \},\s*\{ scale: 1\.04, duration: 2\.3, ease: "power1\.out" \},\s*0\s*\);/m);
  assert.match(html, /tl\.to\(videoEl, \{\s*scale: 1\.12,\s*duration: 0\.4,\s*ease: "back\.out\(1\.1\)"\s*\}, 2\.3\);/m);
  assert.match(html, /tl\.to\(videoEl, \{\s*scale: 1\.15,\s*duration: 3\.3,\s*ease: "power1\.out"\s*\}, 2\.7\);/m);
  assert.match(html, /tl\.to\(videoEl, \{\s*scale: 1\.03,\s*duration: 0\.6,\s*ease: "power2\.inOut"\s*\}, 5\.6\);/m);
  assert.match(html, /tl\.to\(videoEl, \{\s*scale: 1\.09,\s*duration: 0\.5,\s*ease: "back\.out\(1\.2\)"\s*\}, 8\.8\);/m);
  assert.match(html, /tl\.to\(videoEl, \{\s*scale: 1\.11,\s*duration: 1\.7,\s*ease: "power1\.out"\s*\}, 9\.3\);/m);
});
