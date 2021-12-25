import React, { useState } from "react";
import * as Style from "./style";
import Box from "@mui/material/Box";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import { Redirect } from "react-router";
import { useSelector } from "react-redux";
import Login from "./../../components/auth/login/Login";

function AuthenticationPage() {
  const [tabIndex, setTabIndex] = useState(1);

  const handleTabChange = (e, newValue) => {
    setTabIndex(newValue);
  };

  const logged = useSelector((state) => state.auth.logged);

  if (logged) return <Redirect to="/" />;

  return (
    <Style.AuthWrapper>
      <Style.AuthContainer>
        <Login />
      </Style.AuthContainer>
    </Style.AuthWrapper>
  );
}

export default AuthenticationPage;
