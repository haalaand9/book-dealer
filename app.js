const bookGrid = document.getElementById('bookGrid');
const rangeLabel = document.getElementById('rangeLabel');
const topTitle = document.getElementById('topTitle');
const totalSales = document.getElementById('totalSales');
const avgSales = document.getElementById('avgSales');
const audioToggle = document.getElementById('audioToggle');

const audioState = {
  ctx: null,
  gainNode: null,
  intervalId: null,
  enabled: false,
};

const notes = [220, 261.63, 293.66, 329.63, 293.66, 261.63, 220, 196];

const startLoFi = () => {
  if (!audioState.ctx) {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    const ctx = new AudioCtx();
    const gainNode = ctx.createGain();
    gainNode.gain.value = 0.045;
    gainNode.connect(ctx.destination);

    audioState.ctx = ctx;
    audioState.gainNode = gainNode;
  }

  if (audioState.ctx.state === 'suspended') {
    audioState.ctx.resume();
  }

  if (!audioState.intervalId) {
    let step = 0;
    audioState.intervalId = window.setInterval(() => {
      const now = audioState.ctx.currentTime;
      const osc = audioState.ctx.createOscillator();
      const osc2 = audioState.ctx.createOscillator();
      const filter = audioState.ctx.createBiquadFilter();

      osc.type = 'triangle';
      osc2.type = 'sine';
      filter.type = 'lowpass';
      filter.frequency.value = 1100;

      osc.frequency.setValueAtTime(notes[step % notes.length], now);
      osc2.frequency.setValueAtTime(notes[step % notes.length] / 2, now);

      const oscGain = audioState.ctx.createGain();
      oscGain.gain.setValueAtTime(0.04, now);
      oscGain.gain.exponentialRampToValueAtTime(0.0001, now + 0.45);

      const oscGain2 = audioState.ctx.createGain();
      oscGain2.gain.setValueAtTime(0.02, now);
      oscGain2.gain.exponentialRampToValueAtTime(0.0001, now + 0.7);

      osc.connect(filter);
      filter.connect(oscGain);
      oscGain.connect(audioState.gainNode);

      osc2.connect(oscGain2);
      oscGain2.connect(audioState.gainNode);

      osc.start(now);
      osc2.start(now);
      osc.stop(now + 0.45);
      osc2.stop(now + 0.7);
      step += 1;
    }, 420);
  }

  audioState.enabled = true;
  audioToggle.textContent = '■ Lo-fi off';
};

const stopLoFi = () => {
  if (audioState.intervalId) {
    window.clearInterval(audioState.intervalId);
    audioState.intervalId = null;
  }

  if (audioState.ctx) {
    audioState.ctx.suspend();
  }

  audioState.enabled = false;
  audioToggle.textContent = '▶ Lo-fi on';
};

if (audioToggle) {
  audioToggle.addEventListener('click', () => {
    if (audioState.enabled) {
      stopLoFi();
    } else {
      startLoFi();
    }
  });
}

const formatDate = (value) => {
  const date = new Date(value + 'T00:00:00');
  return date.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
};

const formatRangeLabel = (startDate, endDate) => {
  const startText = startDate.toLocaleDateString(undefined, {
    month: 'short',
    day: 'numeric',
  });
  const endText = endDate.toLocaleDateString(undefined, {
    month: 'short',
    day: 'numeric',
  });
  return `${startText} - ${endText}`;
};

const escapeHtml = (value) => {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
};

const render = (dataset) => {
  const { books, purchases } = dataset;
  const today = new Date();
  const cutoff = new Date(today);
  cutoff.setDate(today.getDate() - 4);
  cutoff.setHours(0, 0, 0, 0);

  const counts = new Map();

  for (const purchase of purchases) {
    const purchaseDate = new Date(purchase.date + 'T00:00:00');
    if (purchaseDate >= cutoff && purchaseDate <= today) {
      const currentCount = counts.get(purchase.bookId) || 0;
      counts.set(purchase.bookId, currentCount + purchase.quantity);
    }
  }

  const ranking = books
    .map((book) => ({
      ...book,
      sales: counts.get(book.id) || 0,
    }))
    .sort((a, b) => {
      if (b.sales !== a.sales) return b.sales - a.sales;
      return a.title.localeCompare(b.title);
    })
    .slice(0, 25);

  if (ranking.length) {
    const topBook = ranking[0];
    const total = ranking.reduce((sum, book) => sum + book.sales, 0);
    const average = Math.round(total / ranking.length);

    rangeLabel.textContent = formatRangeLabel(cutoff, today);
    topTitle.textContent = `${topBook.title}`;
    totalSales.textContent = `${total} sales`;
    avgSales.textContent = `${average}/book`;
  }

  bookGrid.innerHTML = ranking
    .map((book, index) => {
      const priceLabel = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
      }).format(book.price);

      const coverMarkup = book.cover
        ? `<img class="book-cover" src="${book.cover}" alt="${escapeHtml(book.title)} cover" loading="lazy" />`
        : `<div class="book-cover no-cover">No cover</div>`;

      const description = book.description
        ? book.description
        : 'Popular book data pulled from OpenLibrary.';

      const published = book.publishedYear ? ` • ${book.publishedYear}` : '';
      const vibeLabel = ['teen favorite', 'cozy binge', 'late-night read', 'dreamy vibe', 'spark notes'][index % 5];

      return `
        <article class="book-card" style="--delay:${index * 100}ms">
          <div class="rank-pill">#${index + 1}</div>
          <div class="book-visual">${coverMarkup}</div>
          <div class="book-info">
            <h2>${escapeHtml(book.title)}</h2>
            <p class="author">by ${escapeHtml(book.author)}</p>
            <p class="summary summary-preview">${escapeHtml(description)}</p>
            <div class="summary-actions">
              <button class="summary-toggle" type="button" data-book="${escapeHtml(book.title)}">
                Show summary
              </button>
            </div>
            <div class="summary-panel" hidden>
              <p>${escapeHtml(description)}</p>
            </div>
            <div class="meta-row">
              <span class="tag">${escapeHtml(book.genre)}</span>
              <span class="vibe-tag">${vibeLabel}</span>
            </div>
            <div class="year-row">${escapeHtml(published)}</div>
            <div class="sales">
              <strong>${book.sales}</strong>
              <span class="sub">purchases in 5 days</span>
            </div>
          </div>
        </article>
      `;
    })
    .join('');
};

fetch('data/purchases.json')
  .then((response) => {
    if (!response.ok) {
      throw new Error('Unable to load purchase data');
    }
    return response.json();
  })
  .then((dataset) => {
    render(dataset);

    document.querySelectorAll('.summary-toggle').forEach((button) => {
      button.addEventListener('click', () => {
        const article = button.closest('.book-card');
        const panel = article.querySelector('.summary-panel');
        const preview = article.querySelector('.summary-preview');
        const isHidden = panel.hasAttribute('hidden');

        panel.hidden = !isHidden;
        button.textContent = isHidden ? 'Hide summary' : 'Show summary';
        preview.hidden = isHidden;
        preview.textContent = isHidden ? preview.textContent : preview.textContent;
      });
    });
  })
  .catch((error) => {
    bookGrid.innerHTML = `<p style="padding:20px; color:#7a5641;">Unable to load book data: ${error.message}</p>`;
    console.error(error);
  });
