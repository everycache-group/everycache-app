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

  return (
    <>
      <Router>
        {logged && <Sidebar />}
        <Switch>
          <Route path="/auth" exact component={Page.Auth} />
          <Route path="/activate/:token" component={Page.Activation} />
          <ProtectedRoute path="/" exact component={Page.Home} />
          <ProtectedRoute path="/mymap" exact component={Page.MyMap} />
          <ProtectedRoute path="/map" component={Page.Map} />
          <ProtectedRoute path="/users" component={Page.Users} />
          <NotFoundRoute />
        </Switch>
      </Router>
    </>
  );
}

export default App;
