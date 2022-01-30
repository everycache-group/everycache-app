import { axiosInstance } from "./api-connector";
import { refreshToken } from "../redux/slices/authSlice";
import config from "./api-config.json";
import axios from "axios";

const setup = (store) => {
  axiosInstance.interceptors.request.use(
    (config) => {
      const token = store.getState().auth.access_token;

      if (token) {
        config.headers["Access-Control-Allow-Origin"] = "*";
        config.headers["Access-Control-Allow-Headers"] = "Authorization";
        config.headers["Authorization"] = `Bearer ${token}`;
      }

      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

  const { dispatch } = store;

  axiosInstance.interceptors.response.use(
    (response) => response,
    async (error) => {
      const originalConfig = error.config;

      if (originalConfig.url !== config.resources.login && error.response) {
        if (error.response.status === 401 && !originalConfig._retry) {
          originalConfig._retry = true;
          try {
            const refToken = store.getState().auth.refresh_token;
            const response = await axios.post(
              config.resources.refresh,
              {},
              {
                headers: {
                  Authorization: `Bearer ${refToken}`,
                },
                baseURL: originalConfig.baseURL,
              }
            );

            const { access_token } = response.data;

            dispatch(refreshToken(access_token));

            return axiosInstance(originalConfig);
          } catch (_error) {
            return Promise.reject(_error);
          }
        }
      }
      return Promise.reject(error);
    }
  );
};

export default setup;
