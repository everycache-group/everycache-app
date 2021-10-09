import * as api from "../api/api-core";

export async function loginUser(email, password, callback) {
  const response = await api.login(email, password);

  const json = await response.json();

  if (response.ok) {
    callback(json);
  } else {
    Promise.reject(json);
  }
}

export async function logoutUser(token) {
  return await api.logout();
}
