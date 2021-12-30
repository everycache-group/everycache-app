import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";

const getCaches = createAsyncThunk(
  "cache/getCaches",
  async (userid, { dispatch }) => {}
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
