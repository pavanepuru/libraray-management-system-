/**
 * Mayura Library Management System - Peacock Interactive Logic
 */

document.addEventListener('DOMContentLoaded', () => {
  initSearchFilters();
  initModals();
});

// Toast System
function showToast(message, type = 'success') {
  let toast = document.getElementById('peacockToast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'peacockToast';
    toast.className = 'peacock-toast';
    document.body.appendChild(toast);
  }

  const icon = type === 'success' ? '🦚' : '⚠️';
  toast.innerHTML = `<span style="font-size: 1.3rem;">${icon}</span> <span>${message}</span>`;
  toast.className = `peacock-toast show ${type}`;

  setTimeout(() => {
    toast.classList.remove('show');
  }, 3500);
}

// Modal Manager
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add('show');
    document.body.style.overflow = 'hidden';
  }
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove('show');
    document.body.style.overflow = 'auto';
  }
}

function initModals() {
  document.querySelectorAll('.peacock-modal-backdrop').forEach(backdrop => {
    backdrop.addEventListener('click', (e) => {
      if (e.target === backdrop) {
        backdrop.classList.remove('show');
        document.body.style.overflow = 'auto';
      }
    });
  });
}

// Live Search & Filter
function initSearchFilters() {
  // Books Search
  const bookSearchInput = document.getElementById('bookSearch');
  const categoryFilter = document.getElementById('categoryFilter');
  if (bookSearchInput || categoryFilter) {
    const filterBooks = () => {
      const query = (bookSearchInput ? bookSearchInput.value : '').toLowerCase().trim();
      const cat = (categoryFilter ? categoryFilter.value : 'all').toLowerCase();

      document.querySelectorAll('.book-item-card, .book-row').forEach(el => {
        const title = el.getAttribute('data-title') || '';
        const author = el.getAttribute('data-author') || '';
        const category = el.getAttribute('data-category') || '';
        const isbn = el.getAttribute('data-isbn') || '';

        const matchesText = title.includes(query) || author.includes(query) || isbn.includes(query);
        const matchesCat = (cat === 'all') || category === cat;

        if (matchesText && matchesCat) {
          el.style.display = '';
        } else {
          el.style.display = 'none';
        }
      });
    };

    if (bookSearchInput) bookSearchInput.addEventListener('input', filterBooks);
    if (categoryFilter) categoryFilter.addEventListener('change', filterBooks);
  }

  // Students Search
  const studentSearchInput = document.getElementById('studentSearch');
  if (studentSearchInput) {
    studentSearchInput.addEventListener('input', () => {
      const q = studentSearchInput.value.toLowerCase().trim();
      document.querySelectorAll('.student-item-card, .student-row').forEach(el => {
        const roll = (el.getAttribute('data-roll') || '').toLowerCase();
        const name = (el.getAttribute('data-name') || '').toLowerCase();
        const branch = (el.getAttribute('data-branch') || '').toLowerCase();

        if (roll.includes(q) || name.includes(q) || branch.includes(q)) {
          el.style.display = '';
        } else {
          el.style.display = 'none';
        }
      });
    });
  }

  // Issue Manager Search
  const issueSearchInput = document.getElementById('issueSearch');
  if (issueSearchInput) {
    issueSearchInput.addEventListener('input', () => {
      const q = issueSearchInput.value.toLowerCase().trim();
      document.querySelectorAll('.issue-row').forEach(el => {
        const roll = (el.getAttribute('data-roll') || '').toLowerCase();
        const student = (el.getAttribute('data-student') || '').toLowerCase();
        const book = (el.getAttribute('data-book') || '').toLowerCase();
        const status = (el.getAttribute('data-status') || '').toLowerCase();

        if (roll.includes(q) || student.includes(q) || book.includes(q) || status.includes(q)) {
          el.style.display = '';
        } else {
          el.style.display = 'none';
        }
      });
    });
  }
}

// Issue Book Student Preview
function updateStudentPreview(selectElement) {
  const selectedOption = selectElement.options[selectElement.selectedIndex];
  const infoBox = document.getElementById('studentPreviewBox');
  if (!infoBox) return;

  if (selectedOption && selectedOption.value) {
    const name = selectedOption.getAttribute('data-name');
    const branch = selectedOption.getAttribute('data-branch');
    const year = selectedOption.getAttribute('data-year');

    infoBox.innerHTML = `
      <div style="display: flex; gap: 12px; align-items: center;">
        <div style="background: rgba(0, 245, 212, 0.15); width: 42px; height: 42px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; color: var(--peacock-cyan); border: 1px solid var(--peacock-cyan);">
          ${name.charAt(0)}
        </div>
        <div>
          <div style="font-weight: 700; color: #fff;">${name}</div>
          <div style="font-size: 0.8rem; color: var(--peacock-gold);">${selectedOption.value} • ${year} • ${branch}</div>
        </div>
      </div>
    `;
    infoBox.style.display = 'block';
  } else {
    infoBox.style.display = 'none';
  }
}

// Book Preview when Issuing
function updateBookPreview(selectElement) {
  const selectedOption = selectElement.options[selectElement.selectedIndex];
  const infoBox = document.getElementById('bookPreviewBox');
  if (!infoBox) return;

  if (selectedOption && selectedOption.value) {
    const avail = parseInt(selectedOption.getAttribute('data-avail') || 0);
    const shelf = selectedOption.getAttribute('data-shelf') || 'Main Section';

    let badgeClass = avail > 0 ? 'badge-emerald' : 'badge-crimson';
    let stockText = avail > 0 ? `${avail} copies in stock` : 'Out of stock';

    infoBox.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 0.85rem; color: var(--text-muted);">Location: <strong style="color: #fff;">${shelf}</strong></span>
        <span class="badge ${badgeClass}">${stockText}</span>
      </div>
    `;
    infoBox.style.display = 'block';
  } else {
    infoBox.style.display = 'none';
  }
}

// Open Digital Library Card Modal
function viewStudentCard(studentId) {
  fetch(`/api/students/${studentId}`)
    .then(res => res.json())
    .then(data => {
      if (data.error) {
        showToast(data.error, 'error');
        return;
      }

      const s = data.student;
      document.getElementById('cardStudentName').textContent = s.name;
      document.getElementById('cardRollNumber').textContent = s.roll_number;
      document.getElementById('cardBranch').textContent = s.branch;
      document.getElementById('cardYear').textContent = s.year_of_study;
      document.getElementById('cardEmail').textContent = s.email;
      document.getElementById('cardPhone').textContent = s.phone;
      document.getElementById('cardBarcode').textContent = `*${s.roll_number}*`;
      document.getElementById('cardAvatarInitial').textContent = s.name.charAt(0);

      // Populate current active loans
      const loansContainer = document.getElementById('cardActiveLoans');
      if (loansContainer) {
        if (data.active_issues && data.active_issues.length > 0) {
          loansContainer.innerHTML = data.active_issues.map(iss => `
            <div style="padding: 6px 10px; background: rgba(0, 245, 212, 0.08); border-radius: 6px; margin-bottom: 6px; font-size: 0.8rem; display: flex; justify-content: space-between;">
              <span style="color: #fff;">📚 ${iss.book_title}</span>
              <span style="color: var(--peacock-gold);">Due: ${iss.due_date}</span>
            </div>
          `).join('');
        } else {
          loansContainer.innerHTML = '<div style="color: var(--text-dim); font-size: 0.8rem; font-style: italic;">No active books currently borrowed.</div>';
        }
      }

      openModal('studentCardModal');
    })
    .catch(err => {
      console.error(err);
      showToast('Error loading student card details.', 'error');
    });
}

// Return Book Action
function processReturn(issueId) {
  if (!confirm('Mark this book as returned and restore inventory?')) return;

  fetch(`/api/return/${issueId}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        showToast('Book returned successfully! Inventory restored.', 'success');
        setTimeout(() => location.reload(), 800);
      } else {
        showToast(data.message || 'Error processing return', 'error');
      }
    })
    .catch(() => showToast('Network error processing return', 'error'));
}

// Renew Book Action
function processRenew(issueId) {
  fetch(`/api/renew/${issueId}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        showToast(`Book renewed! New due date: ${data.new_due_date}`, 'success');
        setTimeout(() => location.reload(), 800);
      } else {
        showToast(data.message || 'Error renewing book', 'error');
      }
    })
    .catch(() => showToast('Network error renewing book', 'error'));
}

// Pay Fine Action
function payFine(issueId) {
  fetch(`/api/pay-fine/${issueId}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        showToast('Fine cleared successfully! Receipt recorded.', 'success');
        setTimeout(() => location.reload(), 800);
      } else {
        showToast(data.message || 'Error paying fine', 'error');
      }
    })
    .catch(() => showToast('Network error recording fine payment', 'error'));
}

// Print Digital Card
function printCard() {
  window.print();
}
