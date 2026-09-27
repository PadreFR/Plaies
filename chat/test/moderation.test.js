'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const { cleanInterests, cleanMessage, cleanReason, RateLimiter, Moderation } = require('../lib/moderation');

test('cleanInterests normalises, deduplicates and caps tags', () => {
  assert.deepEqual(cleanInterests(['  Musique ', 'musique', 'Jeux   vidéo!', '<b>', 42]), ['musique', 'jeux vidéo', 'b']);
  assert.equal(cleanInterests(Array.from({ length: 20 }, (_, i) => `t${i}`)).length, 10);
  assert.deepEqual(cleanInterests('musique'), []);
});

test('cleanMessage strips control characters and truncates', () => {
  assert.equal(cleanMessage('  salut\u0000 !\r\n\n\n\nça va ?  '), 'salut !\n\nça va ?');
  assert.equal(cleanMessage('x'.repeat(5000)).length, 1000);
  assert.equal(cleanMessage({}), '');
});

test('cleanReason only accepts known reasons', () => {
  assert.equal(cleanReason('spam'), 'spam');
  assert.equal(cleanReason('rm -rf'), 'autre');
});

test('RateLimiter allows a burst then refills over time', () => {
  let now = 0;
  const limiter = new RateLimiter({ capacity: 2, refillMs: 1000, now: () => now });
  assert.equal(limiter.take(), true);
  assert.equal(limiter.take(), true);
  assert.equal(limiter.take(), false);
  now += 1000;
  assert.equal(limiter.take(), true);
});

test('Moderation bans after enough distinct reporters and blocks the pair', () => {
  let now = 0;
  const mod = new Moderation({ banThreshold: 2, windowMs: 1000, banMs: 5000, now: () => now });
  assert.deepEqual(mod.report({ reporter: 'r1', reported: 'x', reason: 'spam' }), { banned: false });
  assert.equal(mod.isBlocked('x', 'r1'), true);
  assert.deepEqual(mod.report({ reporter: 'r1', reported: 'x', reason: 'spam' }), { banned: false }, 'same reporter twice');
  assert.deepEqual(mod.report({ reporter: 'r2', reported: 'x', reason: 'spam' }), { banned: true, until: 5000 });
  assert.equal(mod.bannedUntil('x'), 5000);
  now = 5000;
  assert.equal(mod.bannedUntil('x'), 0);
  assert.equal(mod.isBlocked('x', 'r1'), false, 'blocks expire with the window');
});

test('Moderation.prune forgets expired entries', () => {
  let now = 0;
  const mod = new Moderation({ banThreshold: 1, windowMs: 1000, banMs: 1000, now: () => now });
  mod.report({ reporter: 'r', reported: 'x', reason: 'spam' });
  now = 1000;
  mod.prune();
  assert.equal(mod.reports.size, 0);
  assert.equal(mod.bans.size, 0);
  assert.equal(mod.blocks.size, 0);
});
