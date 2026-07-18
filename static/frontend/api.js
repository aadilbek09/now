/* ===== API CONFIGURATION ===== */
var API_BASE = (function() {
  var stored = localStorage.getItem('api_base_url');
  if (stored) return stored;
  if (window.API_BASE_URL) return window.API_BASE_URL;
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    return 'http://127.0.0.1:8000';
  }
  // Production: use same origin (Django serves both API and frontend)
  return window.location.origin;
})();

function getToken() { return localStorage.getItem('access_token'); }
function getRefreshToken() { return localStorage.getItem('refresh_token'); }
function setTokens(access, refresh) {
  localStorage.setItem('access_token', access);
  if (refresh) localStorage.setItem('refresh_token', refresh);
}
function clearTokens() {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('user');
}
function getUser() {
  try { return JSON.parse(localStorage.getItem('user')); } catch(e) { return null; }
}
function setUser(user) { localStorage.setItem('user', JSON.stringify(user)); }

function apiFetch(path, opts) {
  opts = opts || {};
  var headers = opts.headers || {};
  if (!headers['Content-Type'] && !(opts.body instanceof FormData)) {
    headers['Content-Type'] = 'application/json';
  }
  var token = getToken();
  if (token) headers['Authorization'] = 'Bearer ' + token;
  opts.headers = headers;
  return fetch(API_BASE + path, opts).then(function(res) {
    if (res.status === 401) {
      return refreshAccessToken().then(function(newToken) {
        if (newToken) {
          headers['Authorization'] = 'Bearer ' + newToken;
          opts.headers = headers;
          return fetch(API_BASE + path, opts).then(function(r2) {
            if (!r2.ok) throw r2;
            return r2.json();
          });
        }
        throw new Error('Unauthorized');
      });
    }
    if (res.status === 204) return null;
    if (!res.ok) throw res;
    return res.json();
  });
}

function refreshAccessToken() {
  var refresh = getRefreshToken();
  if (!refresh) return Promise.resolve(null);
  return fetch(API_BASE + '/accounts/auth/refresh', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh: refresh })
  }).then(function(res) {
    if (!res.ok) { clearTokens(); return null; }
    return res.json();
  }).then(function(data) {
    if (data && data.access) {
      setTokens(data.access, data.refresh || getRefreshToken());
      return data.access;
    }
    return null;
  }).catch(function() { return null; });
}

function apiGet(path) { return apiFetch(path); }
function apiPost(path, body) {
  return apiFetch(path, { method: 'POST', body: JSON.stringify(body) });
}
function apiPut(path, body) {
  return apiFetch(path, { method: 'PUT', body: JSON.stringify(body) });
}
function apiPatch(path, body) {
  return apiFetch(path, { method: 'PATCH', body: JSON.stringify(body) });
}
function apiDelete(path) {
  return apiFetch(path, { method: 'DELETE' });
}

function apiPostFormData(path, formData) {
  return apiFetch(path, { method: 'POST', body: formData });
}

function apiPutFormData(path, formData) {
  return apiFetch(path, { method: 'PUT', body: formData });
}

function apiPatchFormData(path, formData) {
  return apiFetch(path, { method: 'PATCH', body: formData });
}

/* ===== PRODUCT DETAIL MODAL (shared) ===== */
var currentProductId = null;

function openProduct(item) {
  var modal = document.getElementById('productModal');
  if (!modal) {
    console.error('productModal not found');
    return;
  }
  var imgEl = document.getElementById('productModalImg');
  var catEl = document.getElementById('productModalCategory');
  var nameEl = document.getElementById('productModalName');
  var descEl = document.getElementById('productModalDesc');
  var priceEl = document.getElementById('productModalPrice');
  var orderBtn = document.getElementById('productModalOrder');

  var id = item.getAttribute('data-id');
  var name = item.getAttribute('data-name') || '';
  var price = item.getAttribute('data-price') || '';
  var category = item.getAttribute('data-category') || '';
  var desc = item.getAttribute('data-description') || 'Ta\'rif mavjud emas.';
  var img = item.getAttribute('data-img') || (item.querySelector('img') ? item.querySelector('img').src : '');
  if (!img) img = 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=600&q=80';

  currentProductId = id;

  imgEl.src = img;
  imgEl.alt = name;
  catEl.textContent = category;
  nameEl.textContent = name;
  descEl.textContent = desc;
  priceEl.textContent = price;

  orderBtn.onclick = function() {
    var msg = 'Salem! Men buyurtpa berejaqman:\n\n' + name + ' - ' + price + '\n\nKategoriya: ' + category + '\n\nTelefon: +998912555309 yoki +998933350805';
    window.open('https://wa.me/998912555309?text=' + encodeURIComponent(msg), '_blank');
  };

  if (document.getElementById('productLikeBtn')) {
    document.getElementById('productLikeBtn').className = 'product-like';
    document.getElementById('productDislikeBtn').className = 'product-dislike';
    document.getElementById('productLikeCount').textContent = '0';
    document.getElementById('productDislikeCount').textContent = '0';
  }

  var stars = document.querySelectorAll('#productStars .star');
  stars.forEach(function(s) { s.className = 'star'; });
  if (document.getElementById('productStarsLabel')) {
    document.getElementById('productStarsLabel').textContent = 'Baha beriw';
  }

  if (document.getElementById('productCommentInput')) {
    document.getElementById('productCommentInput').value = '';
  }
  var commentsEl = document.getElementById('productComments');
  commentsEl.innerHTML = '<p style="text-align:center;color:#999;font-size:13px;">Izohlar yuklanmoqda...</p>';

  if (id) {
    apiGet('/menu/products/' + id + '/comments').then(function(comments) {
      var arr = Array.isArray(comments) ? comments : [];
      if (!arr.length) {
        commentsEl.innerHTML = '<p style="text-align:center;color:#999;font-size:13px;">Hali izohlar yo\'q.</p>';
        return;
      }
      commentsEl.innerHTML = arr.map(function(c) {
        return '<div class="product-comment-item">' +
          '<p style="font-size:12px;color:#999;">' + (c.created_at ? new Date(c.created_at).toLocaleDateString() : '') + '</p>' +
          '<p>' + (c.text || '') + '</p>' +
        '</div>';
      }).join('');
    }).catch(function() {
      commentsEl.innerHTML = '<p style="text-align:center;color:#999;font-size:13px;">Izohlarni yuklashda xatolik.</p>';
    });

    apiGet('/menu/products/' + id).then(function(p) {
      if (p && p.name) {
        nameEl.textContent = p.name;
        if (p.description) descEl.textContent = p.description;
        if (p.category_name) catEl.textContent = p.category_name;
      }
    }).catch(function() {
      console.warn('Mahsulot tafsilotlarini yuklab bo\'lmadi:', id);
    });
  } else {
    commentsEl.innerHTML = '<p style="text-align:center;color:#999;font-size:13px;">Hali izohlar yo\'q.</p>';
  }

  modal.classList.add('open');
}
