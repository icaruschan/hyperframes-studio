/**
 * Bug condition exploration test for the caption-sync-fix bugfix spec.
 *
 * Property 1 (Bug Condition): For every word `i` in transcript.json, the GSAP
 * main timeline's caption pop position equals Math.max(0, transcript[i].start +
 * AUDIO_OFFSET) within 1e-3 seconds, and analogously for the hide position vs
 * transcript[i].end. The #claude-ui entrance position equals
 * Math.max(0, transcript.byId('w0').start  + AUDIO_OFFSET) within 1e-3 seconds.
 * The  #figma-ui entrance position equals
 * Math.max(0, transcript.byId('w22').start + AUDIO_OFFSET) within 1e-3 seconds.
 *
 * Validates: Requirements 1.1, 1.2, 1.3, 1.4 (and after the fix: 2.1, 2.2,
 * 2.3, 2.4).
 *
 * BUGFIX WORKFLOW NOTE: This test is EXPECTED TO FAIL on the unfixed code.
 * Failure surfaces the counterexamples that prove the bug exists. After the
 * fix is applied (task 3.1), the SAME test should pass.
 *
 * Implementation strategy (per design.md): instead of running GSAP in jsdom,
 * parse the inline transcript array and the two card-entrance position
 * expressions directly out of index.html. The bug lives entirely in static
 * timing values, so a structural parse is sufficient and deterministic.
 */

import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const COMPOSITION_DIR = resolve(__dirname, '..');
const HTML_PATH = resolve(COMPOSITION_DIR, 'index.html');
const TRANSCRIPT_PATH = resolve(COMPOSITION_DIR, 'transcript.json');

const TOLERANCE_SECONDS = 1e-3;

// ----- Read inputs -------------------------------------------------------

const html = readFileSync(HTML_PATH, 'utf8');
/** @type {Array<{id:string,text:string,start:number,end:number}>} */
const transcript = JSON.parse(readFileSync(TRANSCRIPT_PATH, 'utf8'));
const transcriptById = Object.fromEntries(transcript.map((w) => [w.id, w]));

// ----- Extract AUDIO_OFFSET from index.html -----------------------------

const audioOffsetMatch = html.match(/AUDIO_OFFSET\s*=\s*(-?\d*\.?\d+)/);
assert.ok(
  audioOffsetMatch,
  'Could not locate `AUDIO_OFFSET = <number>` literal in index.html',
);
const AUDIO_OFFSET = Number(audioOffsetMatch[1]);

// ----- Extract the inline `const transcript = [...]` array -------------

const inlineTranscriptMatch = html.match(
  /const\s+transcript\s*=\s*(\[[\s\S]*?\])\s*;/,
);
assert.ok(
  inlineTranscriptMatch,
  'Could not locate `const transcript = [...]` array in index.html',
);
/** @type {Array<{id:string,text:string,start:number,end:number,style:string}>} */
const inlineTranscript = JSON.parse(inlineTranscriptMatch[1]);
const inlineById = Object.fromEntries(inlineTranscript.map((w) => [w.id, w]));

// ----- Extract the card-entrance position expressions ------------------

/**
 * Find `tl.fromTo("<selector>", { ... }, { ... }, <positionExpr>);` and return
 * the numeric value of <positionExpr> evaluated with the real AUDIO_OFFSET.
 *
 * The position expression is captured as a balanced `Math.max(0, ...)` call so
 * that nested parens (e.g. `Math.max(0, 0.15 + AUDIO_OFFSET)`) are handled.
 */
function extractCardEntrancePosition(selector) {
  const anchorRe = new RegExp(
    `tl\\.fromTo\\(\\s*["']${selector.replace(
      /[.#]/g,
      '\\$&',
    )}["']`,
  );
  const anchorMatch = anchorRe.exec(html);
  assert.ok(
    anchorMatch,
    `Could not find tl.fromTo("${selector}", ...) in index.html`,
  );

  // Walk forward from the anchor and balance parens to find the end of the
  // tl.fromTo(...) call.
  const start = anchorMatch.index;
  // Find the opening paren of `fromTo(`
  const openParenIdx = html.indexOf('(', start);
  let depth = 0;
  let end = -1;
  const commas = []; // indices of top-level commas inside the call
  for (let i = openParenIdx; i < html.length; i++) {
    const ch = html[i];
    if (ch === '(') {
      depth++;
    } else if (ch === ')') {
      depth--;
      if (depth === 0) {
        end = i;
        break;
      }
    } else if (ch === ',' && depth === 1) {
      commas.push(i);
    }
  }
  assert.notStrictEqual(
    end,
    -1,
    `Could not balance parens for tl.fromTo("${selector}", ...) call`,
  );
  assert.ok(
    commas.length >= 3,
    `tl.fromTo("${selector}", ...) call did not have 4 arguments`,
  );

  // The position is the LAST top-level argument: between the last top-level
  // comma and the closing paren.
  const lastComma = commas[commas.length - 1];
  const positionExpr = html.slice(lastComma + 1, end).trim();

  // Evaluate it with AUDIO_OFFSET in scope. The expression is fully sourced
  // from index.html (no test input), so this is just a numeric calculator.
  // eslint-disable-next-line no-new-func
  const fn = new Function('AUDIO_OFFSET', 'transcript', 'byId', `return (${positionExpr});`);
  const byId = id => inlineById[id];
  const value = fn(AUDIO_OFFSET, inlineTranscript, byId);
  assert.equal(
    typeof value,
    'number',
    `Position expression for ${selector} did not evaluate to a number: ${positionExpr}`,
  );
  return { value, expr: positionExpr };
}

const claudeEntrance = extractCardEntrancePosition('#claude-ui');
const figmaEntrance = extractCardEntrancePosition('#figma-ui');

// ----- Reconstruct the timeline positions index.html actually produces --
//
// index.html builds caption tweens via:
//   const popTime  = Math.max(0, item.start + AUDIO_OFFSET);
//   const hideTime = Math.max(0, item.end   + AUDIO_OFFSET);
//   tl.fromTo(span, ..., popTime);
//   tl.to(span, ..., hideTime);
// where `item` is drawn from the INLINE transcript array. So the timeline's
// actual pop/hide positions are computed from the inline array, while the
// expected positions are computed from transcript.json (the source of truth).

function actualCaptionPop(id) {
  const w = inlineById[id];
  return Math.max(0, w.start + AUDIO_OFFSET);
}
function actualCaptionHide(id) {
  const w = inlineById[id];
  return Math.max(0, w.end + AUDIO_OFFSET);
}
function expectedFromSource(value) {
  return Math.max(0, value + AUDIO_OFFSET);
}

// ----- Property-based assertions ---------------------------------------
//
// "Input domain" = every word in transcript.json (w0..w32) for caption
// pop/hide, plus the two glass-card entrances keyed to w0 and w22. The
// domain is finite, so we iterate exhaustively and aggregate every
// counterexample so the user gets the full picture.

const counterexamples = [];

for (const source of transcript) {
  // Caption pop alignment
  const expectedPop = expectedFromSource(source.start);
  if (!(source.id in inlineById)) {
    counterexamples.push({
      kind: 'caption-pop',
      id: source.id,
      text: source.text,
      expected: expectedPop,
      actual: 'MISSING',
      delta: NaN,
    });
  } else {
    const actualPop = actualCaptionPop(source.id);
    const dPop = actualPop - expectedPop;
    if (Math.abs(dPop) > TOLERANCE_SECONDS) {
      counterexamples.push({
        kind: 'caption-pop',
        id: source.id,
        text: source.text,
        expected: expectedPop,
        actual: actualPop,
        delta: dPop,
      });
    }
  }

  // Caption hide alignment
  const expectedHide = expectedFromSource(source.end);
  if (source.id in inlineById) {
    const actualHide = actualCaptionHide(source.id);
    const dHide = actualHide - expectedHide;
    if (Math.abs(dHide) > TOLERANCE_SECONDS) {
      counterexamples.push({
        kind: 'caption-hide',
        id: source.id,
        text: source.text,
        expected: expectedHide,
        actual: actualHide,
        delta: dHide,
      });
    }
  }
}

// #claude-ui entrance keyed to w0
{
  const w0 = transcriptById['w0'];
  assert.ok(w0, 'w0 not found in transcript.json');
  const expected = expectedFromSource(w0.start);
  const delta = claudeEntrance.value - expected;
  if (Math.abs(delta) > TOLERANCE_SECONDS) {
    counterexamples.push({
      kind: 'card-entrance',
      selector: '#claude-ui',
      wordId: 'w0',
      text: w0.text,
      expected,
      actual: claudeEntrance.value,
      delta,
      expr: claudeEntrance.expr,
    });
  }
}

// #figma-ui entrance keyed to w22
{
  const w22 = transcriptById['w22'];
  assert.ok(w22, 'w22 not found in transcript.json');
  const expected = expectedFromSource(w22.start);
  const delta = figmaEntrance.value - expected;
  if (Math.abs(delta) > TOLERANCE_SECONDS) {
    counterexamples.push({
      kind: 'card-entrance',
      selector: '#figma-ui',
      wordId: 'w22',
      text: w22.text,
      expected,
      actual: figmaEntrance.value,
      delta,
      expr: figmaEntrance.expr,
    });
  }
}

// ----- Reporting --------------------------------------------------------

function fmtSec(v) {
  return typeof v === 'number' ? v.toFixed(4) + 's' : String(v);
}
function fmtDelta(v) {
  if (typeof v !== 'number' || Number.isNaN(v)) return 'n/a';
  const ms = v * 1000;
  const sign = ms >= 0 ? '+' : '';
  return `${sign}${ms.toFixed(1)}ms`;
}
function describeCounterexample(c) {
  const tag =
    c.kind === 'card-entrance'
      ? `${c.kind} ${c.selector} (keyed to ${c.wordId} "${c.text}")`
      : `${c.kind} ${c.id} "${c.text}"`;
  return `${tag}: expected ${fmtSec(c.expected)}, actual ${fmtSec(
    c.actual,
  )}, delta ${fmtDelta(c.delta)}`;
}

// Always log the parsed inputs so the orchestrator and user can see them
// regardless of pass/fail.
console.log(
  `[caption-sync] AUDIO_OFFSET = ${AUDIO_OFFSET} (parsed from index.html)`,
);
console.log(
  `[caption-sync] transcript.json: ${transcript.length} words; inline transcript: ${inlineTranscript.length} words`,
);
console.log(
  `[caption-sync] #claude-ui entrance position: ${claudeEntrance.value.toFixed(
    4,
  )}s  (expr: ${claudeEntrance.expr})`,
);
console.log(
  `[caption-sync] #figma-ui  entrance position: ${figmaEntrance.value.toFixed(
    4,
  )}s  (expr: ${figmaEntrance.expr})`,
);
if (counterexamples.length > 0) {
  console.log(
    `\n[caption-sync] ${counterexamples.length} counterexample(s):`,
  );
  for (const c of counterexamples) {
    console.log('  - ' + describeCounterexample(c));
  }
  console.log('');
}

// ----- The property test itself ----------------------------------------

test(
  'Property 1: GSAP main timeline positions track transcript.json within 1e-3s',
  () => {
    if (counterexamples.length === 0) return;
    const lines = counterexamples.map((c) => '  - ' + describeCounterexample(c));
    assert.fail(
      `${counterexamples.length} timeline position(s) disagree with ` +
        `transcript.json + AUDIO_OFFSET (${AUDIO_OFFSET}s) by more than ` +
        `${TOLERANCE_SECONDS}s:\n${lines.join('\n')}`,
    );
  },
);
