'use strict';

// Pairs people waiting for a conversation.
//
// Two people are paired right away when they share at least one interest.
// Otherwise a person becomes "open" to any partner once they have no
// interests, or once they have waited `fallbackMs` — so that a rare interest
// never means waiting forever. The oldest waiting person is served first.
class Matchmaker {
  constructor({ fallbackMs = 5000, now = Date.now, canPair = () => true } = {}) {
    this.fallbackMs = fallbackMs;
    this.now = now;
    this.canPair = canPair;
    this.waiting = new Map(); // id -> { id, interests: Set, since }
  }

  get size() {
    return this.waiting.size;
  }

  has(id) {
    return this.waiting.has(id);
  }

  // Adds someone to the queue. Returns { a, b, common } if they were paired
  // immediately, or null if they now wait.
  add(id, interests = []) {
    this.waiting.delete(id);
    const entry = { id, interests: new Set(interests), since: this.now() };
    const found = this._findPartner(entry);
    if (found) {
      this.waiting.delete(found.other.id);
      return { a: found.other.id, b: id, common: found.common };
    }
    this.waiting.set(id, entry);
    return null;
  }

  remove(id) {
    return this.waiting.delete(id);
  }

  // Pairs people whose fallback delay has run out. Call this periodically.
  tick() {
    const matches = [];
    for (const entry of this.waiting.values()) {
      if (!this._isOpen(entry)) continue;
      const found = this._findPartner(entry);
      if (!found) continue;
      this.waiting.delete(entry.id);
      this.waiting.delete(found.other.id);
      matches.push({ a: entry.id, b: found.other.id, common: found.common });
    }
    return matches;
  }

  _findPartner(entry) {
    let fallback = null;
    for (const other of this.waiting.values()) {
      if (other.id === entry.id || !this.canPair(entry.id, other.id)) continue;
      const common = [...entry.interests].filter((tag) => other.interests.has(tag));
      if (common.length > 0) return { other, common };
      if (!fallback && this._isOpen(entry) && this._isOpen(other)) {
        fallback = { other, common };
      }
    }
    return fallback;
  }

  _isOpen(entry) {
    return entry.interests.size === 0 || this.now() - entry.since >= this.fallbackMs;
  }
}

module.exports = { Matchmaker };
