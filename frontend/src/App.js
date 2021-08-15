import './reset.css';
import React from "react";
import { BrowserRouter as Router, Switch, Route} from "react-router-dom";
import Sidebar from "./components/navigation/Sidebar/Sidebar";
import * as Page from './pages/pagesExport';

function App() {
  return (
    <Router>
      <Sidebar />
      <Switch>
        <Route path="/" exact component={ Page.Home } />
        <Route path="/submenu1"  component= { Page.SubMenu1 } />
      </Switch>
    </Router>

        
  );
}

export default App;