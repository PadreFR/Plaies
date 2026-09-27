'use strict';

(() => {
  const $ = (id) => document.getElementById(id);
  const els = {
    home: $('home'),
    chat: $('chat'),
    form: $('start-form'),
    tags: $('tags'),
    interestInput: $('interest-input'),
    adult: $('adult'),
    start: $('start'),
    homeNotice: $('home-notice'),
    onlineCount: $('online-count'),
    status: $('status'),
    report: $('report'),
    log: $('log'),
    typing: $('typing'),
    composer: $('composer'),
    next: $('next'),
    message: $('message'),
    send: $('send'),
    reportDialog: $('report-dialog'),
  };

  const MAX_INTERESTS = 10;
  const STORAGE_KEY = 'papote.interests';
  const BASE_TITLE = document.title;
  const PLACEHOLDER = els.interestInput.placeholder;
  const canAutofocus = window.matchMedia('(pointer: fine)').matches;

  const NEXT_LABELS = { waiting: 'Arrêter', chatting: 'Suivant', ended: 'Nouveau', banned: 'Suivant' };
  const STATUS_LABELS = {
    waiting: 'Recherche d’un inconnu…',
    chatting: 'Vous discutez avec un inconnu.',
    ended: 'Conversation terminée.',
    banned: 'Accès suspendu.',
  };

  let ws = null;
  let reconnectDelay = 1000;
  let state = 'home'; // home | waiting | chatting | ended | banned
  let pendingStart = false;
  let interests = loadInterests();
  let confirmTimer = null;
  let typingSent = false;
  let typingTimer = null;
  let unread = 0;
  // Mirrors the server's rate limit (a bit stricter) so honest users never hit it.
  const bucket = { tokens: 5, last: Date.now() };

  // ---- Connection ----

  function connect() {
    const scheme = location.protocol === 'https:' ? 'wss:' : 'ws:';
    ws = new WebSocket(`${scheme}//${location.host}/ws`);
    ws.addEventListener('open', () => {
      reconnectDelay = 1000;
      if (pendingStart) {
        pendingStart = false;
        sendStart();
      }
    });
    ws.addEventListener('message', (event) => {
      let msg;
      try {
        msg = JSON.parse(event.data);
      } catch {
        return;
      }
      onMessage(msg);
    });
    ws.addEventListener('close', () => {
      ws = null;
      if (state === 'banned') return;
      if (state === 'waiting' || state === 'chatting') {
        system('Connexion perdue.');
        setState('ended');
      }
      setTimeout(connect, reconnectDelay);
      reconnectDelay = Math.min(reconnectDelay * 2, 15000);
    });
  }

  function send(payload) {
    if (!ws || ws.readyState !== WebSocket.OPEN) return false;
    ws.send(JSON.stringify(payload));
    return true;
  }

  function sendStart() {
    if (!send({ type: 'start', adult: true, interests })) pendingStart = true;
  }

  function onMessage(msg) {
    switch (msg.type) {
      case 'online':
        els.onlineCount.textContent = String(msg.count);
        break;
      case 'waiting':
        if (state !== 'waiting') setState('waiting');
        break;
      case 'matched':
        onMatched(Array.isArray(msg.common) ? msg.common : []);
        break;
      case 'msg':
        if (state !== 'chatting') break;
        els.typing.hidden = true;
        bubble('them', String(msg.text));
        notifyUnread();
        break;
      case 'typing':
        if (state !== 'chatting') break;
        stickToBottom(() => {
          els.typing.hidden = !msg.on;
        });
        break;
      case 'partner_left':
        // Both people can press "Next" at once; ours already started a new search.
        if (state !== 'chatting') break;
        system('L’inconnu a quitté la conversation.');
        setState('ended');
        notifyUnread();
        break;
      case 'reported':
        system('Merci, votre signalement a été envoyé. Vous ne serez plus mis en relation avec cette personne.');
        setState('ended');
        break;
      case 'banned':
        onBanned(msg.until);
        break;
      case 'error':
        if (msg.code === 'rate_limited') system('Doucement ! Votre dernier message n’a pas été envoyé.');
        break;
    }
  }

  // ---- States ----

  function setState(next) {
    state = next;
    const chatting = next === 'chatting';
    clearTimeout(typingTimer);
    typingSent = false;
    resetConfirm();
    els.message.disabled = !chatting;
    els.send.disabled = !chatting || !els.message.value.trim();
    els.report.hidden = !chatting;
    els.typing.hidden = true;
    els.next.disabled = next === 'banned';
    els.next.textContent = NEXT_LABELS[next] || 'Suivant';
    els.status.textContent = STATUS_LABELS[next] || '';
  }

  function showChat() {
    els.home.hidden = true;
    els.chat.hidden = false;
    document.body.classList.add('chatting');
  }

  function startSearch() {
    els.log.replaceChildren();
    setState('waiting');
    system('Recherche d’un inconnu…');
    sendStart();
  }

  function onMatched(common) {
    els.log.replaceChildren();
    setState('chatting');
    system('Vous discutez maintenant avec un inconnu. Dites bonjour !');
    if (common.length) system('Vous aimez tous les deux : ', common.join(', '));
    if (canAutofocus) els.message.focus();
    notifyUnread();
  }

  function onBanned(until) {
    const date = new Date(Number(until) || Date.now()).toLocaleString('fr-FR', {
      dateStyle: 'short',
      timeStyle: 'short',
    });
    const text = `Votre accès est suspendu jusqu’au ${date}, à la suite de plusieurs signalements.`;
    setState('banned');
    els.start.disabled = true;
    if (els.chat.hidden) {
      els.homeNotice.textContent = text;
      els.homeNotice.hidden = false;
    } else {
      system(text);
    }
  }

  // ---- "Next" button: a second press within 3 s confirms leaving a chat ----

  function onNext() {
    if (state === 'waiting') {
      pendingStart = false;
      send({ type: 'stop' });
      els.log.replaceChildren();
      system('Recherche arrêtée.');
      setState('ended');
    } else if (state === 'chatting') {
      if (!confirmTimer) {
        els.next.textContent = 'Vraiment ?';
        els.next.classList.add('confirm');
        confirmTimer = setTimeout(resetConfirm, 3000);
        return;
      }
      startSearch();
    } else if (state === 'ended') {
      startSearch();
    }
  }

  function resetConfirm() {
    clearTimeout(confirmTimer);
    confirmTimer = null;
    els.next.classList.remove('confirm');
    if (state === 'chatting') els.next.textContent = NEXT_LABELS.chatting;
  }

  // ---- Messages ----

  function sendMessage() {
    if (state !== 'chatting') return;
    const text = els.message.value.trim();
    if (!text) return;
    if (!takeToken()) {
      system('Doucement ! Attendez un instant avant d’envoyer un autre message.');
      return;
    }
    if (!send({ type: 'msg', text })) return;
    bubble('me', text);
    els.message.value = '';
    autosize();
    els.send.disabled = true;
    stopTyping();
  }

  function takeToken() {
    const now = Date.now();
    bucket.tokens = Math.min(5, bucket.tokens + (now - bucket.last) / 1000);
    bucket.last = now;
    if (bucket.tokens < 1) return false;
    bucket.tokens -= 1;
    return true;
  }

  function onTyping() {
    if (state !== 'chatting') return;
    if (!els.message.value) {
      stopTyping();
      return;
    }
    if (!typingSent) typingSent = send({ type: 'typing', on: true });
    clearTimeout(typingTimer);
    typingTimer = setTimeout(stopTyping, 3000);
  }

  function stopTyping() {
    clearTimeout(typingTimer);
    if (typingSent) send({ type: 'typing', on: false });
    typingSent = false;
  }

  function bubble(who, text) {
    const li = document.createElement('li');
    li.className = `bubble ${who}`;
    const speaker = document.createElement('span');
    speaker.className = 'visually-hidden';
    speaker.textContent = who === 'me' ? 'Vous : ' : 'Inconnu : ';
    li.append(speaker, text);
    stickToBottom(() => els.log.append(li));
  }

  function system(text, strongText) {
    const li = document.createElement('li');
    li.className = 'system';
    li.append(text);
    if (strongText) {
      const strong = document.createElement('strong');
      strong.textContent = strongText;
      li.append(strong);
    }
    stickToBottom(() => els.log.append(li));
  }

  // Runs `change` and keeps the log scrolled to the end, unless the reader
  // had scrolled up to reread something.
  function stickToBottom(change) {
    const log = els.log;
    const atBottom = log.scrollHeight - log.scrollTop - log.clientHeight < 80;
    change();
    if (atBottom) log.scrollTop = log.scrollHeight;
  }

  function autosize() {
    els.message.style.height = 'auto';
    els.message.style.height = `${Math.min(els.message.scrollHeight, 140)}px`;
  }

  function notifyUnread() {
    if (!document.hidden) return;
    unread += 1;
    document.title = `(${unread}) ${BASE_TITLE}`;
  }

  // ---- Interests ----

  function loadInterests() {
    try {
      const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
      return Array.isArray(saved) ? saved.filter((t) => typeof t === 'string').slice(0, MAX_INTERESTS) : [];
    } catch {
      return [];
    }
  }

  function saveInterests() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(interests));
    } catch {
      // Storage unavailable (private browsing): interests just aren't remembered.
    }
  }

  function addInterest(raw) {
    const tag = raw
      .toLowerCase()
      .replace(/[^\p{L}\p{N} _-]/gu, '')
      .replace(/\s+/g, ' ')
      .trim()
      .slice(0, 30);
    if (!tag || interests.includes(tag) || interests.length >= MAX_INTERESTS) return;
    interests.push(tag);
    renderTags();
    saveInterests();
  }

  function removeInterest(tag) {
    interests = interests.filter((t) => t !== tag);
    renderTags();
    saveInterests();
  }

  function renderTags() {
    els.tags.querySelectorAll('.tag').forEach((chip) => chip.remove());
    for (const tag of interests) {
      const chip = document.createElement('span');
      chip.className = 'tag';
      const label = document.createElement('span');
      label.textContent = tag;
      const remove = document.createElement('button');
      remove.type = 'button';
      remove.textContent = '×';
      remove.setAttribute('aria-label', `Retirer ${tag}`);
      remove.addEventListener('click', () => {
        removeInterest(tag);
        els.interestInput.focus();
      });
      chip.append(label, remove);
      els.tags.insertBefore(chip, els.interestInput);
    }
    els.interestInput.placeholder = interests.length ? '' : PLACEHOLDER;
  }

  // ---- Events ----

  els.interestInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ',') {
      e.preventDefault();
      addInterest(els.interestInput.value);
      els.interestInput.value = '';
    } else if (e.key === 'Backspace' && !els.interestInput.value && interests.length) {
      removeInterest(interests[interests.length - 1]);
    }
  });

  // Some mobile keyboards don't report the comma key, so also split on input.
  els.interestInput.addEventListener('input', () => {
    const parts = els.interestInput.value.split(',');
    if (parts.length < 2) return;
    parts.slice(0, -1).forEach(addInterest);
    els.interestInput.value = parts[parts.length - 1];
  });

  els.tags.addEventListener('click', (e) => {
    if (e.target === els.tags) els.interestInput.focus();
  });

  els.adult.addEventListener('change', () => {
    els.start.disabled = !els.adult.checked || state === 'banned';
  });

  els.form.addEventListener('submit', (e) => {
    e.preventDefault();
    if (!els.adult.checked || state === 'banned') return;
    if (els.interestInput.value) {
      addInterest(els.interestInput.value);
      els.interestInput.value = '';
    }
    showChat();
    startSearch();
  });

  els.next.addEventListener('click', onNext);

  els.composer.addEventListener('submit', (e) => {
    e.preventDefault();
    sendMessage();
  });

  els.message.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) {
      e.preventDefault();
      sendMessage();
    }
  });

  els.message.addEventListener('input', () => {
    autosize();
    els.send.disabled = state !== 'chatting' || !els.message.value.trim();
    onTyping();
  });

  document.addEventListener('keydown', (e) => {
    if (e.key !== 'Escape' || els.chat.hidden || els.reportDialog.open) return;
    e.preventDefault();
    onNext();
  });

  els.report.addEventListener('click', () => {
    if (state !== 'chatting') return;
    els.reportDialog.returnValue = '';
    els.reportDialog.showModal();
  });

  els.reportDialog.addEventListener('close', () => {
    if (els.reportDialog.returnValue !== 'send' || state !== 'chatting') return;
    const checked = els.reportDialog.querySelector('input[name="reason"]:checked');
    send({ type: 'report', reason: checked ? checked.value : 'autre' });
  });

  document.addEventListener('visibilitychange', () => {
    if (document.hidden) return;
    unread = 0;
    document.title = BASE_TITLE;
  });

  renderTags();
  connect();
})();
