import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import config from "./../../api/api-config.json";
import ResourceConnector from "../../services/resourceService";
import { PrepareDataSourceTable } from "../../services/dataSourceMapperService";

const cache = new ResourceConnector(config.resources.cache);

export const getCaches = createAsyncThunk(
  "cache/getCaches",
  async (userId, { dispatch }) => {
    const response = await cache.get(userId);

    const { data } = response;

    const datasource = PrepareDataSourceTable(data.results);

    const { total, pages, next, prev } = data;

    const payload = {
      total,
      pages,
      next,
      prev,
      datasource,
    };

    return Promise.resolve(payload);
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
  selectedCache: {},
};

const cacheSlice = createSlice({
  name: "cache",
  initialState,
  reducers: {
    selectRow: (state, action) => {
      state.selectedCache = state.caches.find(
        (cache) => cache.id === action.payload
      );
    },
  },
  extraReducers: {
    [getCaches.fulfilled]: (state, action) => {
      const { total, pages, next, prev, datasource } = action.payload;
      state.total = total;
      state.pages = pages;
      state.next = next;
      state.prev = prev;
      state.caches = datasource;
      state.loading = false;
    },
    [getCaches.rejected]: (state, action) => {
      state = initialState;
    },
    [getCaches.pending]: (state, action) => {
      state.loading = true;
    },
  },
});

export const { selectRow } = cacheSlice.actions;

export default cacheSlice.reducer;
