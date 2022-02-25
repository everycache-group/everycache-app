import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import config from "./../../api/api-config.json";
import ResourceConnector from "../../services/resourceService";
import { PrepareDataSourceTable } from "../../services/dataSourceMapperService";
import { createDataRow } from "../../services/dataSourceMapperService";
import { axiosInstance } from "../../api/api-connector";

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

export const getMyCaches = createAsyncThunk(
  "cache/getMyCaches",
  async (_, { getState }) => {
    const userId = getState().auth.userId;

    const response = await axiosInstance.get(`/api/users/${userId}/caches`);

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

export const createCache = createAsyncThunk(
  "cache/createCache",
  async (cacheData, { dispatch }) => {
    try {
      const response = await cache.create(cacheData);

      const { id, created_on, lon, lat, owner, name, description } =
        response.data.cache;
      const { username } = owner;

      const dataRow = createDataRow(
        id,
        name,
        lon,
        lat,
        username,
        description,
        created_on
      );

      return Promise.resolve(dataRow);
    } catch (_error) {
      return Promise.reject();
    }
  }
);

export const updateCache = createAsyncThunk(
  "cache/updateCache",
  async (cacheDto, thunkAPI) => {
    try {
      const response = await cache.update(cacheDto.id, {
        description: cacheDto.description,
        lat: cacheDto.lat,
        lon: cacheDto.lon,
        name: cacheDto.name,
      });

      const { id, created_on, lon, lat, owner, name, description } =
        response.data.result;
      const { username } = owner;

      const dataRow = createDataRow(
        id,
        name,
        lon,
        lat,
        username,
        description,
        created_on
      );

      return Promise.resolve(dataRow);
    } catch (_error) {
      return Promise.reject();
    }
  }
);

export const deleteCache = createAsyncThunk(
  "cache/delete",
  async (id, thunkAPI) => {
    const response = await cache.remove(id);

    if (response.status == 200){
      return Promise.resolve(id);
    } else {
      return Promise.reject();
    }
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
  selectedCache: null,
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
      state.selectedCache = initialState.selectedCache;
    },
    [getMyCaches.fulfilled]: (state, action) => {
      const { total, pages, next, prev, datasource } = action.payload;
      state.total = total;
      state.pages = pages;
      state.next = next;
      state.prev = prev;
      state.caches = datasource;
      state.loading = false;
      state.selectedCache = initialState.selectedCache;
    },
    [getCaches.rejected]: (state, action) => {
      state = initialState;
    },
    [getCaches.pending]: (state, action) => {
      state.loading = true;
    },
    [getMyCaches.rejected]: (state, action) => {
      state = initialState;
    },
    [getMyCaches.pending]: (state, action) => {
      state.loading = true;
    },
    [createCache.fulfilled]: (state, action) => {
      state.caches.push(action.payload);
    },
    [updateCache.fulfilled]: (state, action) => {
      const index = state.caches.findIndex(
        (item) => item.id == action.payload.id
      );
      const caches = state.caches.slice();
      caches.splice(index, 1, action.payload);
      state.caches = caches;
    },
    [deleteCache.fulfilled]: (state, action) => {
      const id = action.payload;
      const index = state.caches.findIndex(
        (item) => item.id == id
      );
      const caches = state.caches.slice();
      caches.splice(index, 1);
      state.caches = caches;
      state.selectedCache = initialState.selectedCache;
    },
  },
});

export const { selectRow } = cacheSlice.actions;

export default cacheSlice.reducer;
