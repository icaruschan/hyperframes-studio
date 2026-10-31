const fs = require('fs');
const newRaw = JSON.parse(fs.readFileSync('my-video/composition/assets/edit/transcripts/Claude Design footage.json', 'utf8'));
const newWords = (newRaw.words || newRaw.segments.flatMap(s => s.words) || newRaw.words_list || newRaw.transcript).filter(w => w.type === 'word');

const oldT = JSON.parse(fs.readFileSync('my-video/composition/transcript.json', 'utf8'));

// Restore transcript.json to NOT have 'style'
const cleanT = oldT.map((o, i) => ({ id: o.id, text: o.text, start: newWords[i].start, end: newWords[i].end }));
fs.writeFileSync('my-video/composition/transcript.json', JSON.stringify(cleanT, null, 2));

// Prepare styleById mapping
const styleById = {};
oldT.forEach(o => { styleById[o.id] = o.style || 'sans'; });

// Rewrite index.html
let html = fs.readFileSync('my-video/composition/index.html', 'utf8');

// Replace the inline transcript array
html = html.replace(/const transcript = \[\s*[\s\S]*?\];/, 'const transcript = ' + JSON.stringify(cleanT, null, 2) + ';');

// Insert styleById and byId
const additions = `
      const byId = id => transcript.find(w => w.id === id);
      const styleById = ${JSON.stringify(styleById, null, 2)};
`;

html = html.replace(/(const transcript = \[[\s\S]*?\];)/, '$1\n' + additions);

// Update class assignment
html = html.replace(/span\.className = \`word \$\{item\.style\}\`;/, 'span.className = `word ${styleById[item.id]}`;');

// Update card entrances
html = html.replace(/Math\.max\(0, transcript\[0\]\.start \+ AUDIO_OFFSET\)/, "Math.max(0, byId('w0').start + AUDIO_OFFSET)");
html = html.replace(/Math\.max\(0, transcript\[22\]\.start \+ AUDIO_OFFSET\)/, "Math.max(0, byId('w22').start + AUDIO_OFFSET)");

fs.writeFileSync('my-video/composition/index.html', html);
console.log('Update complete');
