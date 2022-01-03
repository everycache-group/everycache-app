import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { resources } from "./../../api/api-config.json";

const getCaches = createAsyncThunk(
  "cache/getCaches",
  async (_, { dispatch }) => {
    const response = await cache.getAll();

    const json = await response.json();

    dispatch();

    return await Promise.resolve();
  }
);

const initialState = {
  caches: [],
};

const cacheSlice = createSlice({
  name: "cache",
  initialState,
  reducers: {},
  extraReducers: {},
});

export const {} = navigationSlice.actions;
export default navigationSlice.reducer;
