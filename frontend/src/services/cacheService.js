import * as api from "./../api/api-core";

const cacheResource = api.resources.cache;

export async function getAll() {
  return await api.get(cacheResource);
}

// TODO create update delete getone
export async function getCache(cacheId) {
  return await api.get(cacheResource, cacheId);
}

export async function create(cacheData) {
  return await api.create(cacheResource, cacheData);
}

export async function update(cacheId, cacheData) {
  return await api.update(cacheResource, cacheId, cacheData);
}

export async function remove(cacheId) {
  return await api.remove(cacheResource, cacheId);
}
