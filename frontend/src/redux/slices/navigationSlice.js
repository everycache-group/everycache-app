import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  lastPage: "/",
  sidebarVisible: false,
};

const navigationSlice = createSlice({
  name: "navigation",
  initialState,
  reducers: {
    setPage(state, action) {
      state.lastPage = action.payload.lastPage;
    },
    toggleSidebar(state, action) {
      state.sidebarVisible = action.payload;
    },
  },
});

export const { setPage, toggleSidebar } = navigationSlice.actions;
export default navigationSlice.reducer;
