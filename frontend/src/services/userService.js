import * as api from "./../api/api-core";

const userResource = api.resources.user;

//tested
export async function create(userData) {
  return await api.create(userResource, userData);
}

//TODO check it
export async function get(userId) {
  return await api.get(userResource, userId);
}

//TODO check it
export async function getAll() {
  return await api.get(userResource);
}

export async function update(userId, userData) {
  return await api.update(userResource, userId, userData);
}

//TODO check it
export async function remove(userId) {
  return await api.remove(userResource, userId);
}
