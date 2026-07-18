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
