import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { resources } from "./../../api/api-config.json";
import ResourceConnector from "../../services/resourceService";
import mockCache from "./../../data/mockCache.json";
import getStoredState from "redux-persist/es/getStoredState";

const cache = new ResourceConnector(resources.cache);

export const getCaches = createAsyncThunk(
  "cache/getCaches",
  async (_, { dispatch }) => {
    // const response = await cache.getAll();

    // const json = await response.json();

    const json = mockCache;
    return await Promise.resolve(json);
  }
);

const initialState = {
  total: 0,
  pages: 0,
  pagination: {
    next: "",
    prev: "",
  },
  caches: [],
  loading: false,
};

const cacheSlice = createSlice({
  name: "cache",
  initialState,
  extraReducers: {
    [getCaches.fulfilled]: (state, action) => {
      const { total } = action.payload;
    },
    [getCaches.rejected]: (state, action) => {
      state = initialState;
    },
    [getCaches.pending]: (state, action) => {
      state.loading = true;
    },
  },
});

export default cacheSlice.reducer;
