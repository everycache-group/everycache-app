import config from "./api-config.json";
import { sendRequest } from "./api-connector";

export const resources = config.resources;

const methods = config.methods;

export async function get(resource, id = null) {
  return await sendRequest(methods.get, resource, id);
}

export async function create(resource, params) {
  return await sendRequest(methods.post, resource, null, params);
}

export async function update(resource, id, params) {
  return await sendRequest(methods.put, resource, id, params);
}

export async function remove(resource, id) {
  return await sendRequest(methods.delete, resource, id);
}

export async function login(email, password) {
  return await sendRequest(methods.post, resources.login, null, {
    email,
    password,
  });
}

export async function logout() {
  return await sendRequest(methods.delete, resources.logout, null);
}

export async function refresh() {
  return await sendRequest(methods.post, resources.refresh);
}
