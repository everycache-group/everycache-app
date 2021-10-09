import * as api from "../api/api-core";

export async function loginUser(email, password, callback) {
  return await api.login(email, password);
}

export async function logoutUser(token) {
  return await api.logout();
}
