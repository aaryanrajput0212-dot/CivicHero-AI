/* ═══════════════════════════════════════════
   CivicHero AI — app.js
═══════════════════════════════════════════ */

// ── Toast Notification ───────────────────────
function showToast(message, type = 'success') {
  const inner = document.getElementById('toast-inner');
  const msg   = document.getElementById('toast-msg');
  const icon  = document.getElementById('toast-icon');
  if (!inner || !msg) return;

  const icons = { success: 'check-circle', error: 'x-circle', info: 'info' };
  const colors = {
    success: 'background:#111827',
    error:   'background:#EF4444',
    info:    'background:#2563EB',
  };

  msg.textContent = message;
  inner.style.cssText = `${colors[type] || colors.success};color:white;display:flex;align-items:center;gap:12px;padding:14px 20px;border-radius:16px;min-width:280px;box-shadow:0 8px 32px rgba(0,0,0,0.25)`;

  // Update icon
  if (icon) {
    icon.setAttribute('data-lucide', icons[type] || 'check-circle');
    if (typeof lucide !== 'undefined') lucide.createIcons();
  }

  // Animate in
  inner.style.transform = 'translateY(0)';
  inner.style.opacity   = '1';
  inner.style.transition = 'all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)';

  // Animate out
  clearTimeout(window._toastTimer);
  window._toastTimer = setTimeout(() => {
    inner.style.transform = 'translateY(80px)';
    inner.style.opacity   = '0';
  }, 3000);
}

// ── Mobile Sidebar ───────────────────────────
function toggleSidebar() {
  const sidebar  = document.getElementById('sidebar');
  const overlay  = document.getElementById('sidebar-overlay');
  if (!sidebar) return;
  sidebar.classList.toggle('open');
  overlay.classList.toggle('hidden');
}

// ── Upvote (global) ──────────────────────────
async function handleUpvote(id, btn) {
  if (btn.dataset.voted) return;
  btn.dataset.voted = '1';
  try {
    const res  = await fetch(`/api/upvote/${id}`, { method: 'POST' });
    const data = await res.json();
    const cnt  = document.getElementById('upvote-count-' + id);
    if (cnt) cnt.textContent = data.upvotes;
    btn.classList.add('text-primary', 'border-primary');
    showToast('👍 Upvoted! Helping prioritize this issue.', 'success');
  } catch(e) {
    showToast('Failed to upvote. Please try again.', 'error');
  }
}

// ── Button Ripple Effect ─────────────────────
document.addEventListener('click', function(e) {
  const btn = e.target.closest('.btn-primary, .btn-outline');
  if (!btn) return;
  const rect   = btn.getBoundingClientRect();
  const ripple = document.createElement('span');
  ripple.style.cssText = `
    position:absolute;
    width:1px;height:1px;
    background:rgba(255,255,255,0.5);
    border-radius:50%;
    transform:scale(0);
    left:${e.clientX - rect.left}px;
    top:${e.clientY - rect.top}px;
    animation:ripple 0.5s ease-out forwards;
    pointer-events:none;
  `;
  if (!btn.style.position || btn.style.position === 'static') btn.style.position = 'relative';
  btn.style.overflow = 'hidden';
  btn.appendChild(ripple);
  setTimeout(() => ripple.remove(), 600);
});

// Add ripple keyframe
const style = document.createElement('style');
style.textContent = `
  @keyframes ripple {
    to { transform:scale(200); opacity:0; }
  }
`;
document.head.appendChild(style);

// ── Smooth Page Transitions ──────────────────
document.addEventListener('DOMContentLoaded', () => {
  document.body.style.opacity = '0';
  document.body.style.transition = 'opacity 0.2s ease';
  requestAnimationFrame(() => { document.body.style.opacity = '1'; });
});

document.querySelectorAll('a[href]').forEach(link => {
  if (link.href.startsWith(window.location.origin) && !link.href.includes('#') && !link.target) {
    link.addEventListener('click', function(e) {
      if (e.metaKey || e.ctrlKey) return;
      e.preventDefault();
      document.body.style.opacity = '0';
      setTimeout(() => { window.location = this.href; }, 180);
    });
  }
});

// ── Auto-dismiss flash messages ──────────────
document.querySelectorAll('.flash-msg').forEach(msg => {
  setTimeout(() => {
    msg.style.transition = 'all 0.3s ease';
    msg.style.opacity = '0';
    msg.style.transform = 'translateY(-8px)';
    setTimeout(() => msg.remove(), 300);
  }, 5000);
});

// ── Number formatting for stat cards ─────────
document.querySelectorAll('.stat-number[data-count]').forEach(el => {
  const target = parseInt(el.dataset.count || el.dataset.suffix || el.textContent);
  if (isNaN(target)) return;
  let current = 0;
  const step  = Math.max(1, Math.ceil(target / 60));
  const suffix = el.dataset.suffix || '';
  const timer = setInterval(() => {
    current = Math.min(current + step, target);
    el.textContent = current.toLocaleString() + suffix;
    if (current >= target) clearInterval(timer);
  }, 20);
});

// ── Active nav link highlight ─────────────────
(function() {
  const path  = window.location.pathname;
  document.querySelectorAll('.sidebar-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href === path || (href !== '/' && path.startsWith(href))) {
      link.classList.add('active');
    }
  });
})();

console.log('%c🏙️ CivicHero AI', 'font-size:18px;font-weight:bold;color:#16A34A');
console.log('%cBuilt for Google for Developers x Coding Ninjas Vibe2Ship Hackathon', 'color:#2563EB');
