import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import * as auth from "./../../services/authService";
import jwt_decode from "jwt-decode";

//obsluzyc prommisy w state
export const loginUser = createAsyncThunk(
  "auth/loginUser",
  async (authData, { dispatch }) => {
    const { email, password } = authData;

    const response = await auth.loginUser(email, password);
    const json = await response.json();

    if (!response.ok) {
      return Promise.reject(json);
    }

    const decoded = jwt_decode(json.access_token);

    return Promise.resolve(json);
  }
);

export const logoutUser = createAsyncThunk(
  "auth/logoutUser",
  async (userId, thunkApi) => {}
);

const initialState = {
  logged: false,
  access_token: "",
  refresh_token: "",
};

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    logout(state, action) {
      state.logged = false;
      state.access_token = "";
      state.refresh_token = "";
    },
  },
  extraReducers: {
    [loginUser.fulfilled]: (state, action) => {
      state.logged = true;
      state.access_token = action.payload.access_token;
      state.refresh_token = action.payload.refresh_token;
    },
  },
});

export const { login, logout } = authSlice.actions;

export default authSlice.reducer;
