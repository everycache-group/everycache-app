import "./reset.css";
import React from "react";
import { useEffect } from "react";
import { useSelector } from "react-redux";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  useHistory,
} from "react-router-dom";
import Sidebar from "./components/navigation/Sidebar/Sidebar";
import * as Page from "./pages/pagesExport";
import ProtectedRoute from "./Routes/ProtectedRoute";
import { PersistGate } from "redux-persist/integration/react";

function App() {
  const logged = useSelector((state) => state.auth.logged);

  const history = useHistory();

  //only for testing redux store
  useEffect(() => {
    window.onbeforeunload = function () {
      window.location.reload(history.push("/submenu1"));
    };
    return () => {
      window.onbeforeunload = null;
    };
  }, []);

  return (
    <>
      <Router>
        {logged && <Sidebar />}
        <Switch>
          <Route path="/auth" exact component={Page.Auth} />
          <ProtectedRoute path="/" exact component={Page.Home} />
          <ProtectedRoute path="/submenu1" component={Page.SubMenu1} />
        </Switch>
      </Router>
    </>
  );
}

export default App;
