export function addItem(key, value) {
  localStorage.setItem(key, value);
}

export function getItem(key) {
  return localStorage.getItem(key);
}

export function clearCache() {
  localStorage.removeItem("chat_app_access_token");
  localStorage.removeItem("chat_app_refresh_token");
  localStorage.clear();
}
