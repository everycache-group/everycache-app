import {
  createAsyncThunk,
  createSlice
} from "@reduxjs/toolkit";
import ResourceConnector from "../../services/resourceService";
import config from "./../../api/api-config.json";
import {prepareErrorPayload} from "../../services/errorMessagesService"
import { axiosInstance } from "../../api/api-connector";

const initialState = {
  comments: []
};

const comment = new ResourceConnector(config.resources.comments);

export const getComments = createAsyncThunk(
  "comment/getComments",
  async (cacheId, {
    rejectWithValue
  }) => {
    try{
      const response = await axiosInstance.get(`/api/caches/${cacheId}/comments?desc=1&order_by=created_on`);
      return Promise.resolve(response.data);
    }
    catch(e) {
      return rejectWithValue(prepareErrorPayload(e.response, "Could not get comments for cache!"));
    };
  }
);

export const addComment = createAsyncThunk(
  "comment/addComment",
  async (addCommentDto, {
    rejectWithValue
  }) => {
    const {cacheId, ...data} = addCommentDto;
    try{
      const response = await axiosInstance.post(`/api/caches/${cacheId}/comments`, data);
      return Promise.resolve(response.data);
    }
    catch(e) {
      return rejectWithValue(prepareErrorPayload(e.response, "Could not get comments for cache!"));
    };
  }
);

export const updateComment = createAsyncThunk(
  "comment/update",
  async (editCommentDto, {
    rejectWithValue
  }) => {
    const {id, ...data} = editCommentDto;
    try{
      const response = await comment.update(id, data);
      return Promise.resolve(response.data);
    }
    catch(e) {
      return rejectWithValue(prepareErrorPayload(e.response, "Could not update comment!"));
    };
  }
);

export const deleteComment = createAsyncThunk(
  "comment/delete",
  async (commentId, {
    rejectWithValue
  }) => {
    try{
      const response = await comment.remove(commentId);
      return Promise.resolve(commentId);
    }
    catch(e) {
      return rejectWithValue(prepareErrorPayload(e.response, "Could not delete comment!"));
    };
  }
);


const commentSlice = createSlice({
  name: "comment",
  initialState,
  reducers: {},
  extraReducers: {
    [getComments.fulfilled]: (state, action) => {
      state.comments = action.payload.results;
    },
    [addComment.fulfilled]: (state, action) => {
      const comments = state.comments.slice();
      comments.unshift(action.payload.cache_comment)
      state.comments = comments;
    },
    [updateComment.fulfilled]: (state, action) => {
      const cache_comment = action.payload.cache_comment;
      const index = state.comments.findIndex(
        (item) => item.id == cache_comment.id
      );
      const comments = state.comments.slice();
      comments.splice(index, 1, cache_comment);
      state.comments = comments;
    },
    [deleteComment.fulfilled]: (state, action) => {
      const index = state.comments.findIndex(
        (item) => item.id == action.payload
      );
      const comments = state.comments.slice();
      comments.splice(index, 1);
      state.comments = comments;
    },
  },
});

export default commentSlice.reducer;
