import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import jwt_decode from "jwt-decode";
import { login, logout } from "../../api/api-core";
import { getUser, logout as userLogout } from "../slices/userSlice";
import {prepareErrorPayload} from "../../services/errorMessagesService"

export const loginUser = createAsyncThunk(
  "auth/loginUser",
  async ({ email, password }, { rejectWithValue }) => {
    try {
      const response = await login(email, password);
      const { data } = response;
      const decodedToken = jwt_decode(data.access_token);

      data.userId = decodedToken.sub;
      return Promise.resolve(data);
    } catch (e) {
      return rejectWithValue(prepareErrorPayload(e.response, "Could not log in!"))
    }
  }
);

export const logoutUser = createAsyncThunk(
  "auth/logoutUser",
  async (_, { getState, dispatch, rejectWithValue }) => {
    try {
      const auth = getState().auth;

      if (auth.logged) {
        const response = await logout(auth.access_token);
        dispatch(userLogout());
      }
      return Promise.resolve();
    }
    catch (e) {
      return rejectWithValue(prepareErrorPayload(e.response, "Could not log out!"))
    }
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
    refreshToken: (state, action) => {
      state.access_token = action.payload;
    },
  },
  extraReducers: {
    [loginUser.fulfilled]: (state, action) => {
      state.logged = true;
      state.access_token = action.payload.access_token;
      state.refresh_token = action.payload.refresh_token;
      state.userId = action.payload.userId;
    },
    [logoutUser.rejected]: (state, action) => {
      state.logged = false;
      state.access_token = "";
      state.refresh_token = "";
      state.userId = "";
    },
    [logoutUser.fulfilled]: (state, action) => {
      state.logged = false;
      state.access_token = "";
      state.refresh_token = "";
      state.userId = "";
    },
  },
});

export const { refreshToken } = authSlice.actions;

export default authSlice.reducer;
