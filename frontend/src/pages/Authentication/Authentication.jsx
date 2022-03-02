import React, { useState } from "react";
import * as Style from "./style";
import { Redirect } from "react-router";
import { useSelector } from "react-redux";
import Tab from "@mui/material/Tab";
import Tabs from "@mui/material/Tabs";
import Register from "../../components/auth/register/Register";
import Login from "../../components/auth/login/Login";

function AuthenticationPage() {
  const [selectedTab, setSelectedTab] = useState(0);

  const handleChange = (event, newValue) => {
    setSelectedTab(newValue);
  };

  const logged = useSelector((state) => state.auth.logged);

  if (logged) return <Redirect to="/" />;

  return (
    <Style.AuthWrapper>
      <Style.AuthContainer>
        <Tabs value={selectedTab} onChange={handleChange}>
          <Tab label="LOGIN" />
          <Tab label="REGISTER" />
        </Tabs>
        {selectedTab === 0 && <Login />}
        {selectedTab === 1 && <Register />}
      </Style.AuthContainer>
    </Style.AuthWrapper>
  );
}

export default AuthenticationPage;
