import './reset.css';
import React from "react";
import { useEffect } from 'react';
import { useSelector } from 'react-redux';
import { BrowserRouter as Router, Switch, Route} from "react-router-dom";
import Sidebar from "./components/navigation/Sidebar/Sidebar";
import * as Page from './pages/pagesExport';
import ProtectedRoute from './Routes/ProtectedRoute';


function App() {

   const isAuth =  useSelector(state => state.user.isAuth);

  //only for testing redux store
  useEffect(() => {

    console.clear();
    console.log(isAuth);

  },[]);



  return (
    <Router>
      {isAuth && <Sidebar />}
      <Switch>
        <Route path='/auth' component={Page.Auth} />
        <ProtectedRoute path="/" exact component={ Page.Home } />
        <ProtectedRoute path="/submenu1"  component= { Page.SubMenu1 } />
      </Switch>
    </Router>

  );
}

export default App;