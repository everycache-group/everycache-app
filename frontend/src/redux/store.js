import { combineReducers, configureStore } from "@reduxjs/toolkit";
import {
  persistStore,
  persistReducer,
  FLUSH,
  REHYDRATE,
  PAUSE,
  PERSIST,
  PURGE,
  REGISTER,
} from "redux-persist";
import authReducer from "./slices/authSlice";
import userReducer from "./slices/userSlice";
import cacheReducer from "./slices/cacheSlice";
import mapReducer from "./slices/mapSlice";
import commentReducer from "./slices/commentSlice";
import navigationReducer from "./slices/navigationSlice";
import storage from "redux-persist/lib/storage";

const persistConfig = {
  key: "root",
  version: 1,
  storage,
  blacklist: ["cache"],
};

const rootReducer = combineReducers({
  auth: authReducer,
  user: userReducer,
  navigation: navigationReducer,
  cache: cacheReducer,
  map: mapReducer,
  comment: commentReducer
});

const persistedReducer = persistReducer(persistConfig, rootReducer);

const store = configureStore({
  reducer: persistedReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER],
      },
    }),
});

let persistor = persistStore(store);

export { store, persistor };
