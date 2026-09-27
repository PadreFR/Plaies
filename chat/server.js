'use strict';

const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const { WebSocketServer } = require('ws');
const { Matchmaker } = require('./lib/matchmaker');
const {
  cleanInterests,
  cleanMessage,
  cleanReason,
  RateLimiter,
  Moderation,
} = require('./lib/moderation');

const TRANSCRIPT_SIZE = 50; // messages kept per conversation, only for reports

const CONTENT_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.ico': 'image/x-icon',
  '.webmanifest': 'application/manifest+json',
};

const SECURITY_HEADERS = {
  'Content-Security-Policy':
    "default-src 'self'; connect-src 'self' ws: wss:; img-src 'self' data:; " +
    "style-src 'self'; script-src 'self'; frame-ancestors 'none'; base-uri 'none'",
  'X-Content-Type-Options': 'nosniff',
  'Referrer-Policy': 'no-referrer',
};

function createChatServer(options = {}) {
  const config = {
    publicDir: path.join(__dirname, 'public'),
    trustProxy: false,
    fallbackMs: 5000,
    tickMs: 1000,
    heartbeatMs: 30000,
    banThreshold: 3,
    reportsFile: null,
    ipSalt: crypto.randomBytes(16).toString('hex'),
    ...options,
  };

  const clients = new Map(); // id -> client
  const moderation = new Moderation({ banThreshold: config.banThreshold, file: config.reportsFile });
  const matchmaker = new Matchmaker({
    fallbackMs: config.fallbackMs,
    canPair: (a, b) => {
      const ca = clients.get(a);
      const cb = clients.get(b);
      return Boolean(ca && cb) && !moderation.isBlocked(ca.key, cb.key);
    },
  });

  const server = http.createServer((req, res) => serveStatic(config.publicDir, req, res));
  const wss = new WebSocketServer({ server, path: '/ws', maxPayload: 8 * 1024 });

  wss.on('connection', (ws, req) => {
    const key = hashIp(clientIp(req, config.trustProxy), config.ipSalt);
    const bannedUntil = moderation.bannedUntil(key);
    if (bannedUntil) {
      send(ws, { type: 'banned', until: bannedUntil });
      ws.close(4003, 'banned');
      return;
    }

    const client = {
      id: crypto.randomUUID(),
      ws,
      key,
      alive: true,
      interests: [],
      partner: null,
      conversation: null,
      limiter: new RateLimiter(),
    };
    clients.set(client.id, client);
    send(ws, { type: 'online', count: clients.size });

    ws.on('pong', () => {
      client.alive = true;
    });
    ws.on('message', (data, isBinary) => {
      if (isBinary) return;
      let msg;
      try {
        msg = JSON.parse(data.toString());
      } catch {
        return;
      }
      if (msg && typeof msg.type === 'string') handle(client, msg);
    });
    ws.on('close', () => {
      leave(client);
      matchmaker.remove(client.id);
      clients.delete(client.id);
    });
  });

  function handle(client, msg) {
    switch (msg.type) {
      case 'start':
        if (msg.adult !== true) {
          send(client.ws, { type: 'error', code: 'adult_required' });
          return;
        }
        client.interests = cleanInterests(msg.interests);
        leave(client);
        enqueue(client);
        return;
      case 'stop':
        leave(client);
        matchmaker.remove(client.id);
        return;
      case 'msg':
        relay(client, msg.text);
        return;
      case 'typing':
        if (client.partner) send(client.partner.ws, { type: 'typing', on: msg.on === true });
        return;
      case 'report':
        report(client, cleanReason(msg.reason));
        return;
    }
  }

  function enqueue(client) {
    const match = matchmaker.add(client.id, client.interests);
    if (match) pair(match);
    else send(client.ws, { type: 'waiting' });
  }

  function pair({ a, b, common }) {
    const ca = clients.get(a);
    const cb = clients.get(b);
    const conversation = { messages: [] };
    ca.partner = cb;
    cb.partner = ca;
    ca.conversation = cb.conversation = conversation;
    send(ca.ws, { type: 'matched', common });
    send(cb.ws, { type: 'matched', common });
  }

  // Ends the client's current conversation, if any, and tells the partner.
  function leave(client) {
    const partner = client.partner;
    if (!partner) return;
    client.partner = partner.partner = null;
    client.conversation = partner.conversation = null;
    send(partner.ws, { type: 'partner_left' });
  }

  function relay(client, raw) {
    const partner = client.partner;
    if (!partner) return;
    if (!client.limiter.take()) {
      send(client.ws, { type: 'error', code: 'rate_limited' });
      return;
    }
    const text = cleanMessage(raw);
    if (!text) return;
    const log = client.conversation.messages;
    log.push({ from: client.id, text, at: Date.now() });
    if (log.length > TRANSCRIPT_SIZE) log.shift();
    send(partner.ws, { type: 'msg', text });
  }

  function report(client, reason) {
    const partner = client.partner;
    if (!partner) return;
    const transcript = client.conversation.messages.map((m) => ({
      from: m.from === client.id ? 'reporter' : 'reported',
      text: m.text,
      at: new Date(m.at).toISOString(),
    }));
    const result = moderation.report({ reporter: client.key, reported: partner.key, reason, transcript });
    leave(client);
    send(client.ws, { type: 'reported' });
    if (result.banned) ban(partner.key, result.until);
  }

  function ban(key, until) {
    for (const client of clients.values()) {
      if (client.key !== key) continue;
      leave(client);
      matchmaker.remove(client.id);
      send(client.ws, { type: 'banned', until });
      client.ws.close(4003, 'banned');
    }
  }

  let lastCount = 0;
  const ticker = setInterval(() => {
    for (const match of matchmaker.tick()) pair(match);
    if (clients.size !== lastCount) {
      lastCount = clients.size;
      for (const client of clients.values()) send(client.ws, { type: 'online', count: lastCount });
    }
  }, config.tickMs);

  const heartbeat = setInterval(() => {
    for (const client of clients.values()) {
      if (!client.alive) {
        client.ws.terminate();
        continue;
      }
      client.alive = false;
      client.ws.ping();
    }
    moderation.prune();
  }, config.heartbeatMs);

  return {
    server,
    listen(port, host) {
      return new Promise((resolve) => server.listen(port, host, () => resolve(server.address())));
    },
    close() {
      clearInterval(ticker);
      clearInterval(heartbeat);
      for (const client of clients.values()) client.ws.terminate();
      wss.close();
      return new Promise((resolve) => server.close(() => resolve()));
    },
  };
}

function send(ws, payload) {
  if (ws.readyState === ws.OPEN) ws.send(JSON.stringify(payload));
}

function clientIp(req, trustProxy) {
  if (trustProxy) {
    const forwarded = req.headers['x-forwarded-for'];
    if (typeof forwarded === 'string' && forwarded) return forwarded.split(',')[0].trim();
  }
  return req.socket.remoteAddress || '';
}

function hashIp(ip, salt) {
  return crypto.createHmac('sha256', salt).update(ip).digest('hex').slice(0, 16);
}

function serveStatic(publicDir, req, res) {
  if (req.method !== 'GET' && req.method !== 'HEAD') {
    res.writeHead(405, { Allow: 'GET, HEAD' }).end();
    return;
  }
  let pathname;
  try {
    pathname = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);
  } catch {
    res.writeHead(400).end();
    return;
  }
  if (pathname === '/healthz') {
    res.writeHead(200, { 'Content-Type': 'text/plain' }).end('ok');
    return;
  }
  if (pathname.endsWith('/')) pathname += 'index.html';
  const filePath = path.join(publicDir, pathname);
  if (!filePath.startsWith(publicDir + path.sep)) {
    res.writeHead(404).end();
    return;
  }
  fs.readFile(filePath, (err, body) => {
    if (err) {
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' }).end('Page introuvable');
      return;
    }
    const type = CONTENT_TYPES[path.extname(filePath)] || 'application/octet-stream';
    res.writeHead(200, { 'Content-Type': type, ...SECURITY_HEADERS });
    res.end(req.method === 'HEAD' ? undefined : body);
  });
}

module.exports = { createChatServer };

if (require.main === module) {
  const port = Number(process.env.PORT) || 3000;
  const options = {
    trustProxy: process.env.TRUST_PROXY === '1',
    banThreshold: Number(process.env.BAN_THRESHOLD) || 3,
    reportsFile: process.env.REPORTS_FILE || path.join(__dirname, 'reports.jsonl'),
  };
  if (process.env.IP_SALT) options.ipSalt = process.env.IP_SALT;
  const chat = createChatServer(options);
  chat.listen(port).then(() => {
    console.log(`Papote écoute sur http://localhost:${port}`);
  });
}
