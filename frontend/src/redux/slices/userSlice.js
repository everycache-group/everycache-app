import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import * as user from "./../../services/userService";
import { loginUser } from "./authSlice";

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

const initialState = {
  email: "",
  username: "",
  role: "",
};

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
    [createUser.fulfilled]: (state, action) => {
      state.email = action.payload.email;
      state.username = action.payload.username;
      state.role = action.payload.role;
    },
  },
});

export const { logout } = userSlice.actions;

export default userSlice.reducer;
