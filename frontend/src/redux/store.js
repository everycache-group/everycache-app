import { combineReducers, createStore } from "redux";
import userReducer from "./reducers/userReducer";

const reducers = combineReducers({
    user: userReducer
}, {});

export default createStore(reducers);
