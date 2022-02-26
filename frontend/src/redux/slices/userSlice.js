import {
  createAsyncThunk,
  createSlice
} from "@reduxjs/toolkit";
import ResourceConnector from "../../services/resourceService";
import {
  loginUser
} from "./authSlice";
import config from "./../../api/api-config.json";

const initialState = {
  username: "",
  role: "",
  id: "",
  email: "",
  users: [],
  loading: false,
  selectedUser: null
};

const user = new ResourceConnector(config.resources.user);

export const getUsers = createAsyncThunk(
  "user/getUsers",
  async (_, {
    dispatch
  }) => {
    const response = await user.get();

    const {
      data
    } = response;

    const results = data.results

    const datasource = data.results;
    //const datasource = JSON.parse(); //PrepareDataSourceTable(data.results);

    const {
      total,
      pages,
      next,
      prev
    } = data;

    const payload = {
      total,
      pages,
      next,
      prev,
      datasource,
    };

    return Promise.resolve(data);
  }
);

export const createUser = createAsyncThunk(
  "user/createUser",
  async (userData, {
    dispatch
  }) => {
    const response = await user.create(userData);

    if (response.status !== 200) {
      return Promise.reject();
    }

    const {
      data
    } = response;

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
  async (userId, {
    dispatch
  }) => {
    const response = await user.get(userId);

    const {
      data
    } = response;


    if (response.status !== 200) {
      return Promise.reject();
    }

    return Promise.resolve(data.user);
  }
);

export const updateUser = createAsyncThunk(
  "user/update",
  async (userData, {rejectWithValue}) => {
    const {id, ...data} = userData;
    try{
      const response = await user.update(id, data);
      const {data: outData} = response;
      return Promise.resolve(outData.user);
    }
    catch(e) {
      return rejectWithValue({"payload": e.response?.data?.msg ?? "Could not update user due to an error!"});
    }
  }
);



export const deleteUser = createAsyncThunk(
  "user/delete",
  async (userId, {
    dispatch
  }) => {
    const response = await user.remove(userId);

    if (response.status !== 200) {
      return Promise.reject(userId);
    }

    return Promise.resolve(userId);
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
    selectRow: (state, action) => {
      state.selectedUser = state.users.find(
        (user) => user.id === action.payload
      );
    },
    selectSelf: (state, action) => {
      const {id, username, email, role} = state;
      state.selectedUser = {id, username, email, role};
    },
  },
  extraReducers: {
    [getUser.fulfilled]: (state, action) => {
      const {
        id,
        username,
        role,
        email
      } = action.payload;
      state.id = id
      state.username = username;
      state.role = role;
      state.email = email;
    },
    [getUsers.fulfilled]: (state, action) => {
      const {
       results
      } = action.payload;
      state.users = results;
      state.loading = false;
    },
    [getUsers.rejected]: (state, action) => {
      state.users = initialState.users;
      state.loading = initialState.loading;
    },
    [getUsers.pending]: (state, action) => {
      state.loading = true;
      state.users = [];
      state.selectedUser = initialState.selectedUser;
    },
    [updateUser.fulfilled]: (state, action) => {
      const index = state.users.findIndex(
        (item) => item.id === action.payload.id
      );

      const currIndex = state.users.findIndex(
        (item) => item.username === state.username
      );

      const users = state.users.slice()
      if (index == currIndex){
        state.username = action.payload.username;
        state.role = action.payload.role;
      }

      users.splice(index, 1, action.payload);
      state.users = users;
      state.selectedUser = action.payload;
    },
    [deleteUser.fulfilled]: (state, action) => {
      const index = state.users.findIndex(
        (item) => item.id === action.payload
      );
      const users = state.users.slice()
      users.splice(index, 1);
      state.users = users;
      //state.selectedUser = initialState.selectedUser;
    },

  },
});

export const {
  logout,
  selectRow,
  selectSelf
} = userSlice.actions;

export default userSlice.reducer;
