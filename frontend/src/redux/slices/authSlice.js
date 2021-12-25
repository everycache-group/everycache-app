import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import * as authService from "./../../services/authService";
import { getUser } from "../slices/userSlice";
import jwt_decode from "jwt-decode";
import { FaWindows } from "react-icons/fa";

//obsluzyc prommisy w state
export const loginUser = createAsyncThunk(
  "auth/loginUser",
  async ({ email, password }, { dispatch }) => {
    const response = await authService.loginUser(email, password);
    const json = await response.json();

    if (!response.ok) {
      return Promise.reject(json);
    }

    const decodedToken = jwt_decode(json.access_token);
    window.sessionStorage.setItem("user-access-token", json.access_token);
    window.sessionStorage.setItem("user-refresh-token", json.refresh_token);

    dispatch(getUser(decodedToken.sub));

    json.userId = decodedToken.sub;
    return Promise.resolve(json);
  }
);

export const logoutUser = createAsyncThunk(
  "auth/logoutUser",
  async (_, { getState }) => {
    //auth.logoutUser();

    const auth = getState().auth;

    if (auth.logged) {
      console.log("logout start");
      const response = await authService.logoutUser(auth.access_token);
      console.log(response);
    }

    window.sessionStorage.removeItem("user-access-token");
    window.sessionStorage.removeItem("user-refresh-token");

    return Promise.resolve();
  }
);

const initialState = {
  logged: false,
  access_token: "",
  refresh_token: "",
  userId: "",
};

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    logout(state, action) {
      state.logged = false;
      state.access_token = "";
      state.refresh_token = "";
      state.userId = "";
    },
  },
  extraReducers: {
    [loginUser.fulfilled]: (state, action) => {
      state.logged = true;
      state.access_token = action.payload.access_token;
      state.refresh_token = action.payload.refresh_token;
      state.userId = action.payload.userId;
    },
    [logoutUser.fulfilled]: (state, action) => {
      state.logged = false;
      state.access_token = "";
      state.refresh_token = "";
      state.userId = "";
    },
  },
});

export const { login, logout } = authSlice.actions;

export default authSlice.reducer;
