import React from "react";
import ReactDOM from "react-dom";
import App from "./App.js";
import { store, persistor } from "./redux/store";
import { Provider } from "react-redux";
import { PersistGate } from "redux-persist/integration/react";
import { SnackbarProvider } from "notistack";
import Slide from "@mui/material/Slide";
import setupInterceptors from "./api/setupInterceptors";

ReactDOM.render(
  <React.StrictMode>
    <Provider store={store}>
      <PersistGate loading={null} persistor={persistor}>
        <SnackbarProvider
          maxSnack={3}
          anchorOrigin={{
            vertical: "bottom",
            horizontal: "center",
          }}
          TransitionComponent={Slide}
        >
          <App />
        </SnackbarProvider>
      </PersistGate>
    </Provider>
  </React.StrictMode>,
  document.getElementById("root")
);

setupInterceptors(store);
