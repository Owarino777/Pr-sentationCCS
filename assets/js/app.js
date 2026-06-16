/*
 * Logique interactive de la carte de présentation.
 */
(() => {
  'use strict';

  const levels = window.presentationLevels;

  if (!Array.isArray(levels) || levels.length === 0) {
    throw new Error('Les données de présentation sont absentes ou invalides.');
  }

  const mapWidth = 2600;
  const mapHeight = 980;
  const nodes = [...document.querySelectorAll('.node')];
  const avatar = document.getElementById('avatar');
  const worldMap = document.getElementById('worldMap');
  const worldFrame = document.querySelector('.world-frame');
  const infoPanel = document.getElementById('infoPanel');
  const panelContent = document.getElementById('panelContent');
  const progressDots = document.getElementById('progressDots');
  const levelChip = document.getElementById('levelChip');
  const jumpLabel = document.getElementById('jumpLabel');
  const prevButton = document.getElementById('prevButton');
  const nextButton = document.getElementById('nextButton');
  const soundToggle = document.getElementById('soundToggle');

  let currentIndex = 0;
  let soundEnabled = true;
  let audioContext;
  let wheelLock = false;

  function escapeHTML(value) {
    return String(value).replace(/[&<>"']/g, (character) => ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#39;',
    })[character]);
  }

  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
  }

  function ensureAudio() {
    if (!audioContext) {
      audioContext = new (window.AudioContext || window.webkitAudioContext)();
    }

    if (audioContext.state === 'suspended') {
      audioContext.resume();
    }
  }

  function playTone(type = 'move') {
    if (!soundEnabled) {
      return;
    }

    ensureAudio();

    const now = audioContext.currentTime;
    const oscillator = audioContext.createOscillator();
    const gain = audioContext.createGain();

    oscillator.connect(gain);
    gain.connect(audioContext.destination);

    if (type === 'move') {
      oscillator.type = 'square';
      oscillator.frequency.setValueAtTime(520, now);
      oscillator.frequency.exponentialRampToValueAtTime(780, now + 0.1);
      gain.gain.setValueAtTime(0.0001, now);
      gain.gain.exponentialRampToValueAtTime(0.05, now + 0.02);
      gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.14);
      oscillator.start(now);
      oscillator.stop(now + 0.16);
      return;
    }

    oscillator.type = 'triangle';
    oscillator.frequency.setValueAtTime(440, now);
    oscillator.frequency.exponentialRampToValueAtTime(660, now + 0.08);
    oscillator.frequency.exponentialRampToValueAtTime(990, now + 0.16);
    gain.gain.setValueAtTime(0.0001, now);
    gain.gain.exponentialRampToValueAtTime(0.07, now + 0.02);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.22);
    oscillator.start(now);
    oscillator.stop(now + 0.24);
  }

  function buildProgress() {
    progressDots.innerHTML = levels
      .map((_, index) => `<div class="progress-dot ${index === 0 ? 'active' : ''}"></div>`)
      .join('');
  }

  function renderPanel(index) {
    const level = levels[index];
    const bullets = level.bullets.map((item) => `<li>${escapeHTML(item)}</li>`).join('');
    const metaCards = level.meta
      .map(([label, value]) => `
        <div class="meta-card">
          <strong>${escapeHTML(label)}</strong>
          <span>${escapeHTML(value)}</span>
        </div>
      `)
      .join('');

    panelContent.innerHTML = `
      <div class="panel-eyebrow">${escapeHTML(level.world)}</div>
      <h2 id="levelTitle">${escapeHTML(level.title)}</h2>
      <p class="subtitle">${escapeHTML(level.subtitle)}</p>
      <p>${escapeHTML(level.blurb)}</p>
      <ul class="bullet-list">${bullets}</ul>
      <div class="meta-row">${metaCards}</div>
      <div class="panel-actions">
        <button class="action-button primary" id="panelNextButton" type="button">
          Continuer
        </button>
      </div>
    `;

    infoPanel.setAttribute('aria-labelledby', 'levelTitle');

    const panelNextButton = document.getElementById('panelNextButton');
    if (panelNextButton) {
      panelNextButton.disabled = currentIndex === levels.length - 1;
      panelNextButton.textContent = currentIndex === levels.length - 1 ? 'Terminé' : 'Continuer';
      panelNextButton.addEventListener('click', () => goToLevel(currentIndex + 1));
    }
  }

  function updateChip(index) {
    const level = levels[index];
    levelChip.innerHTML = `
      <strong>${escapeHTML(level.world)}</strong>
      <span>${escapeHTML(level.subtitle)}</span>
    `;
    jumpLabel.textContent = `Niveau ${index + 1} / ${levels.length}`;
    document.body.className = `theme-${level.theme}`;
  }

  function updateControls(index) {
    if (prevButton) {
      prevButton.disabled = index === 0;
    }

    if (nextButton) {
      nextButton.disabled = index === levels.length - 1;
    }
  }

  function updateActiveNode(index) {
    nodes.forEach((node, nodeIndex) => {
      const isActive = nodeIndex === index;
      const level = levels[nodeIndex];
      node.classList.toggle('active', isActive);
      node.setAttribute('aria-current', isActive ? 'step' : 'false');
      node.setAttribute('aria-label', `Niveau ${nodeIndex + 1} : ${level.subtitle}`);
    });

    [...progressDots.children].forEach((dot, dotIndex) => {
      dot.classList.toggle('active', dotIndex === index);
    });
  }

  function setAvatar(index) {
    const node = nodes[index];
    const x = parseFloat(node.style.left);
    const y = parseFloat(node.style.top);
    avatar.style.left = `${x}px`;
    avatar.style.top = `${y}px`;
    avatar.classList.remove('bounce');
    void avatar.offsetWidth;
    avatar.classList.add('bounce');
  }

  function updateCamera(index) {
    const frameWidth = worldFrame.clientWidth;
    const frameHeight = worldFrame.clientHeight;
    const scale = Math.max(frameWidth / mapWidth, frameHeight / mapHeight);
    const zoom = Math.min(Math.max(scale * 1.22, 0.58), 1.12);

    const node = nodes[index];
    const x = parseFloat(node.style.left);
    const y = parseFloat(node.style.top);

    const targetScreenX = frameWidth * 0.54;
    const targetScreenY = frameHeight * 0.55;

    const tx = clamp(targetScreenX - x * zoom, frameWidth - mapWidth * zoom - 24, 24);
    const ty = clamp(targetScreenY - y * zoom, frameHeight - mapHeight * zoom - 16, 10);

    worldMap.style.transform = `translate(${tx}px, ${ty}px) scale(${zoom})`;
  }

  function goToLevel(index, withSound = true) {
    currentIndex = clamp(index, 0, levels.length - 1);
    updateChip(currentIndex);
    updateActiveNode(currentIndex);
    updateControls(currentIndex);
    setAvatar(currentIndex);
    updateCamera(currentIndex);
    renderPanel(currentIndex);

    if (infoPanel) {
      infoPanel.scrollTop = 0;
    }

    if (withSound) {
      playTone('move');
    }
  }

  function toggleSound() {
    soundEnabled = !soundEnabled;
    soundToggle.textContent = soundEnabled ? '🔊 Son : ON' : '🔇 Son : OFF';
    soundToggle.setAttribute('aria-pressed', String(soundEnabled));

    if (soundEnabled) {
      playTone('open');
    }
  }

  function handleWheelNavigation(event) {
    if (window.innerWidth <= 1100 || wheelLock || Math.abs(event.deltaY) < 16) {
      return;
    }

    const panel = event.target.closest ? event.target.closest('.info-panel') : null;
    if (panel) {
      const canScrollDown = panel.scrollTop + panel.clientHeight < panel.scrollHeight - 2;
      const canScrollUp = panel.scrollTop > 2;

      if ((event.deltaY > 0 && canScrollDown) || (event.deltaY < 0 && canScrollUp)) {
        return;
      }
    }

    wheelLock = true;
    goToLevel(event.deltaY > 0 ? currentIndex + 1 : currentIndex - 1);
    setTimeout(() => {
      wheelLock = false;
    }, 420);
  }

  nodes.forEach((node, index) => {
    node.addEventListener('click', () => goToLevel(index));
    node.addEventListener('keydown', (event) => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        goToLevel(index);
      }
    });
  });

  if (prevButton) {
    prevButton.addEventListener('click', () => goToLevel(currentIndex - 1));
  }

  if (nextButton) {
    nextButton.addEventListener('click', () => goToLevel(currentIndex + 1));
  }

  if (soundToggle) {
    soundToggle.addEventListener('click', toggleSound);
  }

  window.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowRight') {
      goToLevel(currentIndex + 1);
    } else if (event.key === 'ArrowLeft') {
      goToLevel(currentIndex - 1);
    }
  });

  window.addEventListener('wheel', handleWheelNavigation, { passive: true });
  window.addEventListener('resize', () => updateCamera(currentIndex));

  buildProgress();
  goToLevel(0, false);
})();
