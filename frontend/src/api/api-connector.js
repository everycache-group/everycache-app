import config from "./api-config.json";

const { protocol, machine, port } = config.connection;
const apiUrl = `${protocol}://${machine}:${port}`;

export async function sendRequest(action, resource, id = null, params) {
  const endpoint = createEndpoint(resource, id);

  const fetchOptions = createfetchOptions(action, params);

  return await fetch(endpoint, fetchOptions);
}

function createfetchOptions(action, params) {
  const options = {};

  if (action) options.method = action;

  if (params) options.body = JSON.stringify(params);

  const headers = new Headers();

  headers.append("Content-Type", "application/json");
  headers.append("Accept", "application/json");

  const token = window.sessionStorage.getItem("user-access-token");

  if (token) {
    headers.append("Access-Control-Allow-Origin", "*");
    headers.append("Access-Control-Allow-Headers", "Authorization");
    headers.append("Authorization", `Bearer ${token}`);
  }

  options.headers = headers;
  return options;
}

function createEndpoint(resource, id = null) {
  let endpoint = `${apiUrl}/${resource}`;

  if (id) {
    endpoint += `/${id}`;
  }

  return endpoint;
}
