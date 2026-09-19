const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { test } = require('node:test');

const html = readFileSync(path.join(__dirname, 'static/index.html'), 'utf8');
const js = readFileSync(path.join(__dirname, 'static/app.js'), 'utf8');

test('English page includes scoped playground credit and accessible controls', () => {
  assert.match(html, /<html lang="en">/);
  assert.match(html, /playground was built by GPT Astra/);
  assert.match(html, /aria-label="Close architecture panel"/);
  assert.match(html, /Generate continuation/);
  assert.doesNotMatch(html, /[çğıİöşüÇĞÖŞÜ]/);
});

test('legacy metadata is translated without changing unknown text or facts', () => {
  assert.match(js, /function englishMetadata\(/);
  // Evaluate the pure presentation helpers, before any DOM or network access.
  const translate = vm.runInNewContext(js.split('  const state = {')[0]
    + 'return englishMetadata; })();');
  assert.equal(translate('GPT-2 · Eğitim öncesi'), 'GPT-2 · Before fine-tuning');
  for (const seed of [12, 13, 14]) {
    assert.equal(translate(`Deney 13 · Başlangıç · Tohum ${seed}`), `Study 13 · Common checkpoint · Seed ${seed}`);
  }
  assert.equal(translate('800 adım; tekrar yöntemlerinden önce'), '800 updates; before replay policies diverge');
  assert.equal(translate('Bilinmeyen model seçimi.'), 'Unknown model selection.');
  assert.equal(translate('İstek bir JSON nesnesi olmalı.'), 'The request must be a JSON object.');
  assert.equal(translate('The capital of Testland is Testville.'), 'The capital of Testland is Testville.');
  assert.equal(translate('Türkçe kullanıcı metni'), 'Türkçe kullanıcı metni');
});

test('English number formatting and presentation-only translation', () => {
  assert.match(js, /Intl.NumberFormat\('en-GB'/);
  assert.match(js, /Intl.DateTimeFormat\('en-GB'/);
  assert.match(js, /setText\(prompt, turn.prompt\)/);
  assert.match(js, /setText\(completion, turn.completion/);
  assert.match(js, /setText\(answer, fact.answer\)/);
});

test('all legacy static Turkish server messages have English equivalents', () => {
  assert.match(js, /function englishMetadata\(/);
  const translate = vm.runInNewContext(js.split('  const state = {')[0]
    + 'return englishMetadata; })();');
  for (const name of ['data.py', 'model.py', 'server.py']) {
    const source = readFileSync(path.join(__dirname, name), 'utf8');
    for (const match of source.matchAll(/'([^'\n]*[çğıİöşüÇĞÖŞÜ][^'\n]*)'/g)) {
      const message = match[1];
      if (message.includes('{') || message === ' (yerel, eğitim yok)') continue;
      assert.notEqual(translate(message), message, `Untranslated metadata in ${name}: ${message}`);
      assert.doesNotMatch(translate(message), /[çğıİöşüÇĞÖŞÜ]/);
    }
  }
});
