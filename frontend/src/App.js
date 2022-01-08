import "./reset.css";
import React from "react";
import { useSelector } from "react-redux";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Sidebar from "./components/navigation/Sidebar/Sidebar";
import * as Page from "./pages/pagesExport";
import ProtectedRoute from "./components/shared/routes/ProtectedRoute";
import NotFoundRoute from "./components/shared/routes/NotFoundRoute";

function App() {
  const logged = useSelector((state) => state.auth.logged);

  //const lastPath = useSelector((state) => state.navigation.lastPath);

  //useEffect(() => {}, []);

  // useEffect(() => {}, []);

  return (
    <>
      <Router>
        {logged && <Sidebar />}
        <Switch>
          <Route path="/auth" exact component={Page.Auth} />
          <ProtectedRoute path="/" exact component={Page.Home} />
          <ProtectedRoute path="/map" component={Page.Map} />
          <NotFoundRoute />
        </Switch>
      </Router>
    </>
  );
}

export default App;
