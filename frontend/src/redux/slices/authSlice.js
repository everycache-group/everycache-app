import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import jwt_decode from "jwt-decode";
import { login, logout, refresh } from "../../api/api-core";
import { getUser } from "../slices/userSlice";

//obsluzyc promisy w state
export const loginUser = createAsyncThunk(
  "auth/loginUser",
  async ({ email, password }, { dispatch }) => {
    const response = await login(email, password);

    if (response.status !== 200) {
      return Promise.reject(response.data);
    }

    const { data } = response;
    const decodedToken = jwt_decode(data.access_token);

    dispatch(getUser(decodedToken.sub));
    data.userId = decodedToken.sub;

    return Promise.resolve(data);
  }
);

export const logoutUser = createAsyncThunk(
  "auth/logoutUser",
  async (_, { getState }) => {
    const auth = getState().auth;

    if (auth.logged) {
      const response = await logout(auth.access_token);
    }

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
