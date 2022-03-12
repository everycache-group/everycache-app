import {
  createAsyncThunk,
  createSlice
} from "@reduxjs/toolkit";
import ResourceConnector from "../../services/resourceService";
import {
  loginUser
} from "./authSlice";
import config from "./../../api/api-config.json";
import {prepareErrorPayload} from "../../services/errorMessagesService"
import { axiosInstance } from "../../api/api-connector";

const initialState = {
  username: "",
  role: "",
  id: "",
  email: "",
  verified: false,
  users: [],
  loading: false,
  selectedUser: null,
  ratings: {}
};

const user = new ResourceConnector(config.resources.user);

export const activateUser = createAsyncThunk(
  "user/activate",
  async (token, {
    rejectWithValue
  }) => {
    try{
      const response = await axiosInstance.post(`/auth/activate/${token}`);
      return Promise.resolve(response.data);
    }
    catch(e) {
      return rejectWithValue(prepareErrorPayload(e.response, "Could not activate user!"));
    };
  }
);


export const getRatings = createAsyncThunk(
  "user/getRatings",
  async (_, {
    rejectWithValue, getState
  }) => {
    try{
      const userId = getState().user.id;
      const response = axiosInstance.get(`/api/users/${userId}/visits`);
      return Promise.resolve(response);
    }
    catch(e) {
      console.log(e);
      return rejectWithValue(prepareErrorPayload(e.response, "Could not get user ratings!"));
    };
  }
);


export const addRating = createAsyncThunk(
  "user/addRating",
  async ({ cache_id, rating }, { rejectWithValue }) => {
    try {
      const response = axiosInstance.post(`/api/caches/${cache_id}/visits`, {
        rating: JSON.stringify(rating),
      });

      return Promise.resolve(response);
    } catch (e) {
      return rejectWithValue(prepareErrorPayload(e, "Could not rate given cache!"));
    }
  }
);

export const updateRating = createAsyncThunk(
  "user/updateRating",
  async ({ visit_id, rating }, { rejectWithValue }) => {
    try {
      const response = axiosInstance.put(`/api/cache_visits/${visit_id}`, {
        rating: JSON.stringify(rating),
      });

      return Promise.resolve(response);
    } catch (e) {
      return rejectWithValue(prepareErrorPayload(e, "Could not change rating!"));
    }
  }
);


export const getUsers = createAsyncThunk(
  "user/getUsers",
  async (_, {
    rejectWithValue
  }) => {
    try{
      const response = await user.get();
      return Promise.resolve(response.data);
    }
    catch(e) {
      return rejectWithValue(prepareErrorPayload(e.response, "Could not get users!"));
    };
  }
);

export const createUser = createAsyncThunk(
  "user/createUser",
  async (userData, {rejectWithValue, dispatch}) => {
    try{
      const response = await user.create(userData);
      dispatch(
        loginUser({
          email: userData.email,
          password: userData.password,
        }))
          .unwrap()
          .then((result) => {
            const {userId} = result;
            dispatch(getUser(userId))
          });

      return Promise.resolve(response.data);
    }
    catch(e) {
      return rejectWithValue(prepareErrorPayload(e.response, "Could not create user!"));
    };
  }
);

export const getUser = createAsyncThunk(
  "user/get",
  async (userId, { rejectWithValue }) => {
    try{
      const response = await user.get(userId);
      return Promise.resolve(response.data.user);
    }
    catch(e) {
      return rejectWithValue(prepareErrorPayload(e.response, "Could not get user data!"));
    };
  }
);

export const updateUser = createAsyncThunk(
  "user/update",
  async (userData, {rejectWithValue}) => {
    const {id, ...data} = userData;
    try{
      const response = await user.update(id, data);
      return Promise.resolve(response.data.user);
    }
    catch(e) {
      return rejectWithValue(prepareErrorPayload(e.response, "Could not update user!"));
    };
  }
);



export const deleteUser = createAsyncThunk(
  "user/delete",
  async (userId, { rejectWithValue }) => {
    try{
      const response = await user.remove(userId);
      return Promise.resolve(userId);
    }
    catch(e) {
      return rejectWithValue(prepareErrorPayload(e.response, "Could not delete user!"));
    };
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
      const {id, username, email, role, verified} = state;
      state.selectedUser = {id, username, email, role, verified};
    },
  },
  extraReducers: {
    [getUser.fulfilled]: (state, action) => {
      const {
        id,
        username,
        role,
        email,
        verified
      } = action.payload;
      state.id = id
      state.username = username;
      state.role = role;
      state.email = email;
      state.verified = verified;
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
        state.email = action.payload.email;
        state.id = action.payload.id;
        state.verified = action.payload.verified;
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
      state.selectedUser = initialState.selectedUser;
    },
    [getRatings.fulfilled]: (state, action) => {
      state.ratings = action.payload.data.results;
    },
    [addRating.fulfilled]: (state, action) => {
      state.ratings.push(action.payload.data.cache_visit);
    },
    [updateRating.fulfilled]: (state, action) => {
      const cacheVisit = action.payload.data.cache_visit;
      const index = state.ratings.findIndex(
        (item) => item.id === cacheVisit.id
      )
      const newRatings = state.ratings.slice();
      newRatings[index] = cacheVisit;

      state.ratings = newRatings;
    }
  },
});

export const {
  logout,
  selectRow,
  selectSelf
} = userSlice.actions;

export default userSlice.reducer;
