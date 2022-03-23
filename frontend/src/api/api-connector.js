import config from "./api-config.json";
import axios from "axios";

export const axiosInstance = axios.create({
  baseURL: getBaseUrl(),
  timeout: 2000,
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
});

export async function sendRequest(action, resource, id = null, params) {
  const endpoint = createEndpoint(resource, id);

  const response = await axiosInstance(endpoint, {
    method: action,
    data: JSON.stringify(params),
  });

  return Promise.resolve(response);
}

const createEndpoint = (resource, id = null) =>
  id ? `/${resource}/${id}` : `/${resource}`;

function getBaseUrl() {
  const {
    REACT_APP_BACKEND_API_SCHEME: scheme,
    REACT_APP_BACKEND_API_HOST: host,
    REACT_APP_BACKEND_API_PORT: port
  } = process.env;

  const url = `${scheme ?? "http"}://${host ?? "localhost"}`;
  if (port !== undefined || host === "localhost"){
    url += `:${port ?? 5000}`;
  }
  
  return url;
}
