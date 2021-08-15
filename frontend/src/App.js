import './reset.css';
import React from "react";
import { BrowserRouter as Router, Switch, Route} from "react-router-dom";
import Sidebar from "./components/navigation/Sidebar/Sidebar";

function App() {
  return (
    <Router>
      <Sidebar />
      
    </Router>

        
  );
}

export default App;