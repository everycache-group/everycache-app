import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import ResourceConnector from "../../services/resourceService";
import { loginUser } from "./authSlice";
import config from "./../../api/api-config.json";

const initialState = {
  username: "",
  role: "",
};

const user = new ResourceConnector(config.resources.user);

export const createUser = createAsyncThunk(
  "user/createUser",
  async (userData, { dispatch }) => {
    const response = await user.create(userData);

    if (response.status !== 200) {
      return Promise.reject();
    }

    const { data } = response;

    dispatch(
      loginUser({
        email: userData.email,
        password: userData.password,
      })
    );

    return Promise.resolve(data);
  }
);

export const getUser = createAsyncThunk(
  "user/get",
  async (userId, { dispatch }) => {
    console.log(userId);
    const response = await user.get(userId);

    const { data } = response;

    if (response.status !== 200) {
      return Promise.reject();
    }

    return Promise.resolve(data);
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
      const { username, role } = action.payload;
      state.username = username;
      state.role = role;
    },
  },
});

export const { logout } = userSlice.actions;

export default userSlice.reducer;
