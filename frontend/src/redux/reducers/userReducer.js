import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";

const initialState = {
    logged: false,
    access_token: "",
    refresh_token: "",
}

const userSlice = createSlice({
    name: 'user',
    initialState,
    reducers: {
        login: state => {

        }

        
    }

});

export default userSlice.reducer;