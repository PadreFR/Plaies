'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const WebSocket = require('ws');
const { createChatServer } = require('../server');

// A WebSocket client that queues incoming messages so tests can await them.
function connect(url, ip) {
  const ws = new WebSocket(url, { headers: { 'x-forwarded-for': ip } });
  const inbox = [];
  const waiters = [];
  ws.on('message', (data) => {
    const msg = JSON.parse(data.toString());
    if (msg.type === 'online') return;
    const i = waiters.findIndex((w) => w.type === msg.type);
    if (i >= 0) waiters.splice(i, 1)[0].resolve(msg);
    else inbox.push(msg);
  });
  const client = {
    ws,
    send: (payload) => ws.send(JSON.stringify(payload)),
    next(type, timeoutMs = 2000) {
      const i = inbox.findIndex((m) => m.type === type);
      if (i >= 0) return Promise.resolve(inbox.splice(i, 1)[0]);
      return new Promise((resolve, reject) => {
        const waiter = { type, resolve };
        waiters.push(waiter);
        setTimeout(() => {
          const j = waiters.indexOf(waiter);
          if (j >= 0) {
            waiters.splice(j, 1);
            reject(new Error(`no "${type}" message within ${timeoutMs} ms`));
          }
        }, timeoutMs);
      });
    },
    inbox,
    closed: new Promise((resolve) => ws.on('close', (code) => resolve(code))),
  };
  return new Promise((resolve, reject) => {
    ws.on('open', () => resolve(client));
    ws.on('error', reject);
  });
}

async function withServer(options, fn) {
  const chat = createChatServer({ trustProxy: true, tickMs: 20, fallbackMs: 100, ...options });
  const { port } = await chat.listen(0, '127.0.0.1');
  try {
    await fn({ url: `ws://127.0.0.1:${port}/ws`, http: `http://127.0.0.1:${port}` });
  } finally {
    await chat.close();
  }
}

test('pairs two people, relays messages and typing, and handles "next"', () =>
  withServer({}, async ({ url }) => {
    const a = await connect(url, '10.0.0.1');
    const b = await connect(url, '10.0.0.2');

    a.send({ type: 'start', adult: true, interests: ['Musique', 'cinéma'] });
    await a.next('waiting');
    b.send({ type: 'start', adult: true, interests: ['musique'] });
    assert.deepEqual(await a.next('matched'), { type: 'matched', common: ['musique'] });
    assert.deepEqual(await b.next('matched'), { type: 'matched', common: ['musique'] });

    a.send({ type: 'typing', on: true });
    assert.equal((await b.next('typing')).on, true);
    a.send({ type: 'msg', text: '  Salut <b>toi</b> !  ' });
    assert.equal((await b.next('msg')).text, 'Salut <b>toi</b> !');
    b.send({ type: 'msg', text: 'Bonjour' });
    assert.equal((await a.next('msg')).text, 'Bonjour');

    b.send({ type: 'start', adult: true, interests: [] });
    await a.next('partner_left');
    await b.next('waiting');

    a.ws.close();
    b.ws.close();
  }));

test('refuses to start without the adult confirmation', () =>
  withServer({}, async ({ url }) => {
    const a = await connect(url, '10.0.0.1');
    a.send({ type: 'start', interests: [] });
    assert.equal((await a.next('error')).code, 'adult_required');
    a.ws.close();
  }));

test('falls back to a random partner when no interest matches', () =>
  withServer({}, async ({ url }) => {
    const a = await connect(url, '10.0.0.1');
    const b = await connect(url, '10.0.0.2');
    a.send({ type: 'start', adult: true, interests: ['échecs'] });
    b.send({ type: 'start', adult: true, interests: ['surf'] });
    assert.deepEqual((await a.next('matched')).common, []);
    await b.next('matched');
    a.ws.close();
    b.ws.close();
  }));

test('limits how fast someone can send messages', () =>
  withServer({}, async ({ url }) => {
    const a = await connect(url, '10.0.0.1');
    const b = await connect(url, '10.0.0.2');
    a.send({ type: 'start', adult: true });
    b.send({ type: 'start', adult: true });
    await a.next('matched');
    for (let i = 0; i < 8; i++) a.send({ type: 'msg', text: `message ${i}` });
    assert.equal((await a.next('error')).code, 'rate_limited');
    a.ws.close();
    b.ws.close();
  }));

test('a report ends the chat, blocks the pair and can ban', () =>
  withServer({ banThreshold: 1 }, async ({ url }) => {
    const a = await connect(url, '10.0.0.1');
    const b = await connect(url, '10.0.0.2');
    a.send({ type: 'start', adult: true });
    b.send({ type: 'start', adult: true });
    await a.next('matched');
    b.send({ type: 'msg', text: 'message déplacé' });
    await a.next('msg');

    a.send({ type: 'report', reason: 'harcelement' });
    await a.next('reported');
    assert.ok((await b.next('banned')).until > Date.now());
    assert.equal(await b.closed, 4003);

    const again = await connect(url, '10.0.0.2');
    await again.next('banned');
    assert.equal(await again.closed, 4003);
    a.ws.close();
  }));

test('people who reported each other are not paired again', () =>
  withServer({ banThreshold: 99 }, async ({ url }) => {
    const a = await connect(url, '10.0.0.1');
    const b = await connect(url, '10.0.0.2');
    a.send({ type: 'start', adult: true });
    b.send({ type: 'start', adult: true });
    await a.next('matched');
    a.send({ type: 'report', reason: 'spam' });
    await a.next('reported');
    await b.next('partner_left');

    a.send({ type: 'start', adult: true });
    await a.next('waiting');
    b.send({ type: 'start', adult: true });
    await b.next('waiting');
    await new Promise((resolve) => setTimeout(resolve, 250));
    assert.equal(a.inbox.some((m) => m.type === 'matched'), false);

    const c = await connect(url, '10.0.0.3');
    c.send({ type: 'start', adult: true });
    await c.next('matched');
    a.ws.close();
    b.ws.close();
    c.ws.close();
  }));

test('serves the page and refuses paths outside public/', () =>
  withServer({}, async ({ http }) => {
    const page = await fetch(`${http}/`);
    assert.equal(page.status, 200);
    assert.match(page.headers.get('content-type'), /text\/html/);
    assert.match(page.headers.get('content-security-policy'), /default-src 'self'/);
    assert.equal((await fetch(`${http}/..%2fserver.js`)).status, 404);
    assert.equal((await fetch(`${http}/healthz`)).status, 200);
  }));
