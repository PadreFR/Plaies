'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const { Matchmaker } = require('../lib/matchmaker');

function clock(start = 0) {
  let now = start;
  return { now: () => now, advance: (ms) => (now += ms) };
}

test('pairs two people without interests right away', () => {
  const mm = new Matchmaker();
  assert.equal(mm.add('a'), null);
  assert.deepEqual(mm.add('b'), { a: 'a', b: 'b', common: [] });
  assert.equal(mm.size, 0);
});

test('prefers a shared interest over the oldest person waiting', () => {
  const mm = new Matchmaker();
  mm.add('old');
  mm.add('music-fan', ['musique']);
  assert.deepEqual(mm.add('newcomer', ['cinéma', 'musique']), {
    a: 'music-fan',
    b: 'newcomer',
    common: ['musique'],
  });
  assert.ok(mm.has('old'));
});

test('someone with interests waits, then falls back to anyone', () => {
  const t = clock();
  const mm = new Matchmaker({ fallbackMs: 5000, now: t.now });
  mm.add('a', ['échecs']);
  assert.equal(mm.add('b'), null, 'a is not open to random partners yet');
  assert.deepEqual(mm.tick(), []);
  t.advance(5000);
  assert.deepEqual(mm.tick(), [{ a: 'a', b: 'b', common: [] }]);
  assert.equal(mm.size, 0);
});

test('never pairs people that canPair rejects', () => {
  const mm = new Matchmaker({ canPair: (x, y) => !(x === 'a' && y === 'b') && !(x === 'b' && y === 'a') });
  mm.add('a');
  assert.equal(mm.add('b'), null);
  assert.deepEqual(mm.add('c'), { a: 'a', b: 'c', common: [] });
  assert.ok(mm.has('b'));
});

test('re-adding someone does not pair them with themselves', () => {
  const mm = new Matchmaker();
  mm.add('a');
  assert.equal(mm.add('a'), null);
  assert.equal(mm.size, 1);
});

test('remove takes someone out of the queue', () => {
  const mm = new Matchmaker();
  mm.add('a');
  assert.equal(mm.remove('a'), true);
  assert.equal(mm.add('b'), null);
});
