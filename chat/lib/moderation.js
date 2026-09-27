'use strict';

const fs = require('node:fs');

const MAX_INTERESTS = 10;
const MAX_INTEREST_LENGTH = 30;
const MAX_MESSAGE_LENGTH = 1000;
const REPORT_REASONS = ['spam', 'harcelement', 'sexuel', 'mineur', 'autre'];
const DAY_MS = 24 * 60 * 60 * 1000;

// Lowercases, strips punctuation and deduplicates the interest tags a client
// sends, keeping at most MAX_INTERESTS of them.
function cleanInterests(input) {
  if (!Array.isArray(input)) return [];
  const tags = new Set();
  for (const raw of input) {
    if (typeof raw !== 'string') continue;
    const tag = raw
      .normalize('NFKC')
      .toLowerCase()
      .replace(/[^\p{L}\p{N} _-]/gu, '')
      .replace(/\s+/g, ' ')
      .trim()
      .slice(0, MAX_INTEREST_LENGTH);
    if (tag) tags.add(tag);
    if (tags.size >= MAX_INTERESTS) break;
  }
  return [...tags];
}

// Removes control characters (except newlines and tabs), collapses long runs
// of blank lines and truncates to MAX_MESSAGE_LENGTH.
function cleanMessage(input) {
  if (typeof input !== 'string') return '';
  return input
    .replace(/\r\n?/g, '\n')
    .replace(/[\u0000-\u0008\u000B-\u001F\u007F]/g, '')
    .replace(/\n{3,}/g, '\n\n')
    .trim()
    .slice(0, MAX_MESSAGE_LENGTH);
}

function cleanReason(input) {
  return REPORT_REASONS.includes(input) ? input : 'autre';
}

// Token bucket: allows bursts of `capacity` actions, then one every `refillMs`.
class RateLimiter {
  constructor({ capacity = 5, refillMs = 800, now = Date.now } = {}) {
    this.capacity = capacity;
    this.refillMs = refillMs;
    this.now = now;
    this.tokens = capacity;
    this.last = now();
  }

  take() {
    const now = this.now();
    this.tokens = Math.min(this.capacity, this.tokens + (now - this.last) / this.refillMs);
    this.last = now;
    if (this.tokens < 1) return false;
    this.tokens -= 1;
    return true;
  }
}

// Keeps track of reports, bans and pairs that must not meet again. People are
// identified by an opaque key (a hash of their IP address), never a raw IP.
class Moderation {
  constructor({ banThreshold = 3, windowMs = DAY_MS, banMs = DAY_MS, file = null, now = Date.now } = {}) {
    this.banThreshold = banThreshold;
    this.windowMs = windowMs;
    this.banMs = banMs;
    this.file = file;
    this.now = now;
    this.reports = new Map(); // reported key -> Map(reporter key -> time)
    this.bans = new Map(); // key -> ban end time
    this.blocks = new Map(); // "reporter|reported" -> time
  }

  // Records a report. Returns { banned, until } — banned is true when enough
  // distinct people reported the same key within the window.
  report({ reporter, reported, reason, transcript = [] }) {
    const now = this.now();
    this.blocks.set(`${reporter}|${reported}`, now);

    let reporters = this.reports.get(reported);
    if (!reporters) this.reports.set(reported, (reporters = new Map()));
    reporters.set(reporter, now);

    this._append({ at: new Date(now).toISOString(), reporter, reported, reason, transcript });

    const recent = [...reporters.values()].filter((time) => now - time < this.windowMs).length;
    if (recent < this.banThreshold) return { banned: false };
    const until = now + this.banMs;
    this.bans.set(reported, until);
    return { banned: true, until };
  }

  // Returns the ban end time for a key, or 0 when it is not banned.
  bannedUntil(key) {
    const until = this.bans.get(key);
    if (!until) return 0;
    if (until > this.now()) return until;
    this.bans.delete(key);
    return 0;
  }

  // True when one of the two reported the other recently.
  isBlocked(a, b) {
    return this._blockActive(`${a}|${b}`) || this._blockActive(`${b}|${a}`);
  }

  // Forgets expired bans, blocks and reports so memory does not grow forever.
  prune() {
    const now = this.now();
    for (const [key, until] of this.bans) if (until <= now) this.bans.delete(key);
    for (const [pair, time] of this.blocks) if (now - time >= this.windowMs) this.blocks.delete(pair);
    for (const [reported, reporters] of this.reports) {
      for (const [reporter, time] of reporters) if (now - time >= this.windowMs) reporters.delete(reporter);
      if (reporters.size === 0) this.reports.delete(reported);
    }
  }

  _blockActive(pair) {
    const time = this.blocks.get(pair);
    return time !== undefined && this.now() - time < this.windowMs;
  }

  _append(entry) {
    if (!this.file) return;
    fs.appendFile(this.file, JSON.stringify(entry) + '\n', (err) => {
      if (err) console.error('Impossible d’enregistrer le signalement :', err.message);
    });
  }
}

module.exports = {
  MAX_MESSAGE_LENGTH,
  REPORT_REASONS,
  cleanInterests,
  cleanMessage,
  cleanReason,
  RateLimiter,
  Moderation,
};
