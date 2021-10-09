import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  email: "",
  username: "",
  role: "",
};

const userSlice = createSlice({
  name: "user",
  initialState,
  reducers: {
    login(state, action) {
      state.email = action.payload.email;
      state.username = action.payload.username;
      state.role = action.payload.role;
    },

    logout(state, action) {
      state.email = "";
      state.username = "";
      state.role = "";
    },
  },
});

export const { login, logout } = userSlice.actions;

export default userSlice.reducer;
