import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  settings: {
    center: [50, 50],
    zoom: 13,
  },
  commentList : {
    open: false
  }
};

const mapSlice = createSlice({
  name: "map",
  initialState,
  reducers: {
    changeZoom(state, action) {
      state.settings.zoom = action.payload;
    },
    changeCenter(state, action) {
      state.settings.center = action.payload;
    },
    changeCommentListOpen(state, action) {
      state.commentList.open = action.payload;
    }
  },
});

export const { changeZoom, changeCenter, changeCommentListOpen } = mapSlice.actions;

export default mapSlice.reducer;
