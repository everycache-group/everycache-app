import { createSlice } from "@reduxjs/toolkit";

const initialState = {
    logged: false,
    access_token: "",
    refresh_token: "",
}

const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        login(state, action) {
            state.logged = true;
            state.access_token = action.payload.access_token;
            state.refresh_token = action.payload.refresh_token;
        },

        logout(state, action) {
            state.logged = false;
            state.access_token = "";
            state.refresh_token = "";
        }
    }
   
});

export const { login, logout } = authSlice.actions;

export default authSlice.reducer;