import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import * as user from "./../../services/userService";
import { loginUser } from "./authSlice";

const initialState = {
  username: "",
  role: "",
};

export const createUser = createAsyncThunk(
  "user/createUser",
  async (userData, { dispatch }) => {
    const response = await user.create(userData);

    const json = await response.json();

    if (!response.ok) {
      return Promise.reject(json);
    }

    dispatch(
      loginUser({
        email: userData.email,
        password: userData.password,
      })
    );

    return Promise.resolve(json);
  }
);

export const getUser = createAsyncThunk(
  "user/get",
  async (userId, { dispatch }) => {
    const response = await user.get(userId);
    const json = await response.json();

    if (!response.ok) {
      return Promise.reject(json);
    }

    return Promise.resolve(json);
  }
);

const userSlice = createSlice({
  name: "user",
  initialState,
  reducers: {
    logout(state, action) {
      state.email = "";
      state.username = "";
      state.role = "";
    },
  },
  extraReducers: {
    [getUser.fulfilled]: (state, action) => {
      const { username, role } = action.payload.user;
      state.username = username;
      state.role = role;
    },
  },
});

export const { logout } = userSlice.actions;

export default userSlice.reducer;
